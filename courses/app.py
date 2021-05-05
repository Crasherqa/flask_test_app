from dataclasses import dataclass
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@dataclass
class Courses(db.Model):
    id: int
    title: str
    start_date: datetime
    end_date: datetime
    lectures_count: int

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    end_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    lectures_count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Course %r>' % self.id


@app.route('/courses', methods=['POST'])
def create_course():
    title = request.json['title']

    try:
        start_date = request.json['start_date']
        start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M")
    except Exception as e:
        return make_response(jsonify(message=f'Invalid start_date value\n {e}'), 400)

    try:
        end_date = request.json['end_date']
        end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M")
    except Exception as e:
        return make_response(jsonify(message=f'Invalid end_date value\n {e}'), 400)

    try:
        lectures_count = request.json['lectures_count']
        lectures_count = int(lectures_count)
    except Exception as e:
        return make_response(jsonify(message=f'Invalid lecture_count value\n {e}'), 400)

    courses = Courses(title=title, start_date=start_date, end_date=end_date, lectures_count=lectures_count)
    try:
        db.session.add(courses)
        db.session.commit()
        return make_response(jsonify(course_id=courses.id,
                                     message=f'The {title} course was created and will begin on {start_date}'), 200)
    except Exception as e:
        return make_response(jsonify(message=f"Something went wrong\n {e}"), 400)


@app.route('/courses', methods=['GET'])
def get_courses():
    if len(request.args) > 0:
        found_courses = None
        find_by_name = request.args.get('find_by_name', type=str)
        order_by = request.args.get('order_by', type=str)

        if find_by_name and order_by:
            if order_by in Courses.__table__.columns:
                found_courses = Courses.query.filter(Courses.title.contains(find_by_name)).order_by(order_by).all()
            else:
                return make_response(jsonify(message=f'Invalid order_by param'), 400)
        elif order_by and find_by_name is None:
            if order_by in Courses.__table__.columns:
                found_courses = Courses.query.order_by(order_by).all()
            else:
                return make_response(jsonify(message=f'Invalid order_by param'), 400)
    else:
        found_courses = Courses.query.all()
    return make_response(jsonify(found_courses), 200)


@app.route('/courses/<int:course_id>', methods=['GET'])
def get_courses_by_id(course_id):
    course = Courses.query.get_or_404(course_id, f'The course with ID: {course_id} was not found')
    return make_response(jsonify(course=course.title, start_date=course.start_date, end_date=course.end_date,
                                 lectures_count=course.lectures_count), 200)


@app.route('/course/<int:course_id>', methods=['PATCH'])
def patch_course(course_id):
    course = Courses.query.get_or_404(course_id, f'The course with ID: {course_id} was not found')

    req = request.get_json(force=True)

    if 'title' in req:
        title = request.json['title']
        course.title = title
    if 'start_date' in req:
        try:
            start_date = request.json['start_date']
            start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M")
            course.start_date = start_date
        except Exception as e:
            return make_response(jsonify(message=f'Invalid start_date value\n {e}'), 400)
    if 'end_date' in req:
        try:
            end_date = request.json['end_date']
            end_date = datetime.strptime(end_date, "%Y-%m-%d %H:%M")
            course.end_date = end_date
        except Exception as e:
            return make_response(jsonify(message=f'Invalid end_date value\n {e}'), 400)
    if 'lectures_count' in req:
        try:
            lectures_count = request.json['lectures_count']
            lectures_count = int(lectures_count)
            course.lectures_count = lectures_count
        except Exception as e:
            return make_response(jsonify(message=f'Invalid lecture_count value\n {e}'), 400)

    try:
        db.session.commit()
        return make_response(jsonify(course_id=course.id, message=f'The course ID: {course.id} was updated'), 201)
    except Exception as e:
        return make_response(jsonify(message=f"Something went wrong\n {e}"), 404)


@app.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_courses(course_id):
    course = Courses.query.get_or_404(course_id, f'The course with ID: {course_id} was not found')
    try:
        db.session.delete(course)
        db.session.commit()
        print('DELETED')
        return make_response(jsonify(message=f'The course ID: {course.id} was Deleted'), 204)
    except Exception as e:
        return make_response(jsonify(message=f"Something went wrong\n {e}"), 404)


if __name__ == "__main__":
    course = Courses(title='Yalantis Python School',
                     start_date=datetime.strptime('2021-06-19 19:00', "%Y-%m-%d %H:%M"),
                     end_date=datetime.strptime('2021-09-19 12:00', "%Y-%m-%d %H:%M"),
                     lectures_count=20)
    db.create_all()
    db.session.add(course)
    db.session.commit()
    app.run()

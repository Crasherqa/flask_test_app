# YALANTIS TEST 

***Install:***
1. `Install python 3.8`
2. `pip install -r requirements.txt`

***Run application:***
1. `python3 courses/app.py`

***Run test:***
**TBD**
1. `pytest tests/`

## **Application supporting http methods**

1. Create a course:
    _**POST /courses**_ 

    **Request body:**
   
    `{
        "title": "String",
        "start_date": "2021-06-19 08:00",
        "end_date": "2021-08-19 11:00",
        "lectures_count": int
    }`


2. Get all courses:
    _**GET /courses**_ 
   
    **Support parameters**: 
   
    1. find_by_name:
        _**GET /courses?find_by_name={Name}**_
       
    2. order_by (title; start_date; end_date; lectures_count):
        _**GET /courses?find_by_name=Test&order_by=start_date**_ 


3. Get course by ID:
    _**GET /courses/{course_id}**_
   

4. Update course by ID:
    _**PATCH /courses/{course_id}**_ 
   
   **Request body:**
   
    `{
        "title": "String",
        "start_date": "2021-06-19 08:00",
        "end_date": "2021-08-19 11:00",
        "lectures_count": int
    }`
   
5. Delete course by ID:
    _**DELETE /courses/{course_id}**_ 
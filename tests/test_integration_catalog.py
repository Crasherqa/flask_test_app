from api_helper import *


class TestCrud:
    def test_create_course(self, create_test_course):
        course_id = create_test_course
        assert is_course_exists(course_id)

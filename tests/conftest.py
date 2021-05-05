import pytest
from api_helper import *
from datetime import datetime


@pytest.fixture(autouse=True)
def init_app():
    pass


@pytest.fixture
def create_test_course():
    user_id = create_course(title='Test Course',
                            start_date=datetime.strptime('2021-06-19 19:00', "%Y-%m-%d %H:%M"),
                            end_date=datetime.strptime('2021-09-19 12:00', "%Y-%m-%d %H:%M"),
                            lectures_count=20)
    yield user_id
    delete_course(user_id)

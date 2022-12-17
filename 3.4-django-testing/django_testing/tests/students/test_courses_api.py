import pytest
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Course


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_retrieve(client, course_factory):
    course = course_factory(_quantity=1)

    response = client.get(f'/api/v1/courses/{course[0].id}/')
    data = response.json()

    assert response.status_code == 200
    assert data['name'] == course[0].name


@pytest.mark.django_db
def test_list(client, course_factory):
    courses = course_factory(_quantity=10)

    response = client.get('/api/v1/courses/')
    data = response.json()

    assert response.status_code == 200
    for i, course in enumerate(data):
        assert course['name'] == courses[i].name


@pytest.mark.django_db
def test_filter_id(client, course_factory):
    courses = course_factory(_quantity=10)

    response = client.get(f'/api/v1/courses/?id={courses[2].id}')
    data = response.json()

    assert response.status_code == 200
    assert data[0]['name'] == courses[2].name


@pytest.mark.django_db
def test_filter_name(client, course_factory):
    courses = course_factory(_quantity=10)

    response = client.get(f'/api/v1/courses/?name={courses[2].name}')
    data = response.json()

    assert response.status_code == 200
    assert data[0]['id'] == courses[2].id

@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()

    response = client.post('/api/v1/courses/', data={'name': 'test name'})

    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_update_course(client, course_factory):
    course = course_factory(_quantity=1)

    response = client.patch(f'/api/v1/courses/{course[0].id}/', data={'name': 'test updated name'})
    response_get = client.get(f'/api/v1/courses/{course[0].id}/')
    data = response.json()

    assert response.status_code == 200
    assert response_get.status_code == 200
    assert data['name'] == 'test updated name'


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory(_quantity=1)

    response = client.delete(f'/api/v1/courses/{course[0].id}/')
    response_get = client.get(f'/api/v1/courses/{course[0].id}/')

    assert response.status_code == 204
    assert response_get.status_code == 404

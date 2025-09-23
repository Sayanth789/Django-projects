import requests

username = 'your_username'
password = 'your_password'

base_url = 'http://127.0.0.1:8000/api/'
url = f'{base_url}courses/'
all_courses = []

# Fetch all courses
while url is not None:
    print(f'Loading courses from {url}')
    r = requests.get(url)
    response = r.json()
    url = response['next']
    all_courses += response['results']

print(f'Available courses: {", ".join([c["title"] for c in all_courses])}')

# Enroll in all courses
for course in all_courses:
    course_id = course['id']
    course_title = course['title']
    r = requests.post(
        f'{base_url}courses/{course_id}/enroll/',
        auth=(username, password)
    )
    if r.status_code == 200:
        print(f'Successfully enrolled in {course_title}')
    else:
        print(f'Failed to enroll in {course_title}: {r.status_code}')

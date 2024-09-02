# Question and Answer Social Website

## Project description

The project consists of a simple Q&A social networking website.

The application was developed using Python, Django, Javascript, PostgreSQL.

## Functionalities

The system must allow users to:

- log into their account by entering their email and password
- edit their profile information, such as username and icon
- send and receive questions
- send anonymous questions
- choose whether they want to receive anonymous questions or not
- follow other users
- block other users (they will not be able to access the user page)
- silence other users (they will not be able to send the user any question)
- like posts
- share posts

The system must send notifications when a user receive new followers or a question they’ve made is answered.

## Database

- Profile: username, email, password, icon, following, blocked, silenced, question_helper, allow_anon_questions
- Question: sent_by, sent_to, body, created_at, is_anon, is_answered
- Answer: question, body
- Post: answer, author, liked, shared, created_at

## Quick start

Inside the app folder:

```
pip install -r requirements.txt

python manage.py runserver
```

Go to 'http://localhost:8000/'

## Mockups

### Main Page

![Alt text](https://github.com/ericarfs/django-social-media-website/blob/main/mockups/MainPage.png?raw=true)

### Login Page

![Alt text](https://github.com/ericarfs/django-social-media-website/blob/main/mockups/LoginPage.png?raw=true)

### Register Page

![Alt text](https://github.com/ericarfs/django-social-media-website/blob/main/mockups/SignUpPage.png?raw=true)

### Home

![Alt text](https://github.com/ericarfs/django-social-media-website/blob/main/mockups/Home.png?raw=true)

### Profile

![Alt text](https://github.com/ericarfs/django-social-media-website/blob/main/mockups/Profile.png?raw=true)

### Notifications

![Alt text](https://github.com/ericarfs/django-social-media-website/blob/main/mockups/Notifications.png?raw=true)

### Inbox

![Alt text](https://github.com/ericarfs/django-social-media-website/blob/main/mockups/Inbox.png?raw=true)

### Reply

![Alt text](https://github.com/ericarfs/django-social-media-website/blob/main/mockups/Reply.png?raw=true)

### Post

![Alt text](https://github.com/ericarfs/django-social-media-website/blob/main/mockups/Post.png?raw=true)

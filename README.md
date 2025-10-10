# Python-Django social networking application

- This project started from [New Social Network 2018 - PHP Social Network Project](https://www.youtube.com/playlist?list=PLxefhmF0pcPkg0Tkdt3wcuQ4LRDw81xI7) by Coding Cafe, but I converted it to a Python-Django project.
- The project includes core functions of a **social media app**, including **profile management**, **posting**, **commenting**, **messaging**, and **search capabilities**, all accessible to **authenticated** users. 
- The app prioritizes **user interaction** and a **secure login system** to maintain a personalized user experience.


## Key learning outcomes

1. Understanding Framework Paradigm Differences between PHP & Django
   - PHP to Django Structure
   - Routing and URL Handling
   - Templating System

2. Database Layer and ORM Transition
   - From SQL Queries to ORM
   - Model Design
   - Data Relationships (`OneToMany` and `ManyToMany`)

3. Authentication and Authorization in Django
   - Built-in Auth System

4. Handling Forms and Validation
   - From HTML + PHP POST Handling to Django Forms
   - Security Features

5. Static Files and Templates
   - Template Inheritance
   - Static File Management

6. Deployment and Environment Setup
   - From PHP Hosting to Python Environment
   - Database Migration

7. Project Organization and Maintainability


## Differences from original tutorial

### Original covered: 

1. **User Authentication**:
   - **Login Requirement**: Many functions are protected by requiring users to log in to access certain pages.
   - **Logout**: The logout function allows users to log out and then redirects them to the main page.

2. **Profile and User Information**:
   - **Home and Profile Pages**: The Home and Profile buttons display the main dashboard and individual user profiles, respectively.
   - **Update Profile Image and Cover**: Allow users to update their profile images and cover photos.
   - **Edit Profile**: Renders a page allowing users to edit their profile information.
   - **Find People**: Serves as a user discovery feature, allowing users to view other members and possibly connect with them.

3. **Posts and Interactions**:
   - **Create and Edit Posts**: Allow users to create new posts and provide functionality for editing existing posts.
   - **Delete Posts**: Allow users to delete their posts, with redirection based on the context (home or profile).
   - **Post View and Comments**: Displays a single post in detail, and enables users to add comments on that post.
   - **My Posts**: Shows all posts created by the logged-in user on a personalized page.

4. **Messaging**:
   - **User Messaging**: Provides a messaging interface, allowing users to communicate privately with each other.
     
5. **Search Functionality**:
   - **Post Search**: Allows users to search for posts.

6. **Account Management**:
   - **Forgot and Change Password**: These functions provide interfaces for resetting or changing passwords, which are essential for account security.


### My Additions: 
- Redesigned main page, navigation bar, and pagination
- Restyled signup, login, post upload form, and password recovery pages

## How to run
Follow these steps to set up and run the Django project locally.

### 1. **Clone the Repository**

```bash
git clone https://github.com/webQbe/social_network-django.git
cd social_network-django
```
---

### 2. **Create and Activate a Virtual Environment**

#### On Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```
---

### 3. **Install Dependencies**

Make sure you have **pip** installed, then run:

```bash
pip install -r requirements.txt
```
---

### 5. **Apply Database Migrations**

```bash
python manage.py migrate
```
---

### 6. **Create a Superuser (Admin Account)**

```bash
python manage.py createsuperuser
```

Follow the prompts to set up an admin username, email, and password.
---

### 7. **Run the Development Server**

```bash
python manage.py runserver
```
---
Then open your browser and go to:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**



## Notes
* Ensure you have **Python 3.9+** and **MySQL or SQLite** configured properly.
* Update `DATABASES` in `settings.py` if you want to connect to a MySQL database:

  ```python
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.mysql',
          'NAME': 'your_database_name',
          'USER': 'your_username',
          'PASSWORD': 'your_password',
          'HOST': 'localhost',
          'PORT': '3306',
      }
  }
  ```

---


## Credits & license
- Inspired by: [New Social Network 2018 - PHP Social Network Project](https://www.youtube.com/playlist?list=PLxefhmF0pcPkg0Tkdt3wcuQ4LRDw81xI7)
- Author: Coding Cafe
- This repo contains original code I wrote as well as parts adapted from the tutorial. Check LICENSE.









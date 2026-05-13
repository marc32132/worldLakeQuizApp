## 🌍 Lakes of the World Quiz – Django App

Description:
A web application built with Django that allows users to take a quiz about lakes' location around the world. The data was collected from the International Lake Environment Committee Foundation. The quiz generates 5 questions with 4 multiple-choice answers. Users can also browse all lakes and their locations with a search function. It supports both guests and registered users.

### 🛠 Technologies

Backend: Python 3.11+, Django  
Database: Oracle ATP / SQLite3 (optional)  
Version control: Git  


### ⚡ Features

Generates a quiz with 5 questions and 4 multiple-choice answers  
Supports both guests and registered users  
Browse all lakes and their locations with a search function  
Simple and user-friendly web interface  

### 🖼️ Core Interface Views

<details>
<summary><b>🏠 Click to view Home Pages for guest and authenticated user</b></summary>

![Front Page](.github/assets/FrontPage.png)
![Front Page](.github/assets/FrontPage_LoggedUser.png)
</details>

<details>
<summary><b>🔍 Click to view Lake Browsing Page</b></summary>

![Lake Browsing Page](.github/assets/LakeBrowsingPage.png)
</details>

<details>
<summary><b>✍️ Click to view Quiz Page</b></summary>

![Quiz Page 1](.github/assets/Quiz_1.png)
![Quiz Page 2](.github/assets/Quiz_2.png)
</details>

<details>
<summary><b>🏆 Click to view Quiz Results Page and Saved Results Page (for logged in user)</b></summary>

![Results Page](.github/assets/QuizResults.png)
![Saved Results Page](.github/assets/QuizResults_SavedForUser.png)
</details>

<details>
<summary><b>🔐 Click to view SignUp and SignIn Pages</b></summary>

![Front Page](.github/assets/SignUp.png)
![Front Page](.github/assets/SignIn.png)
</details>


### 🚀 Local Setup

Clone the repository
```
git clone https://github.com/marc32132/worldLakeQuizApp.git
cd worldLakeQuizApp
```
Create and activate a virtual environment

```
python -m venv venv 
source venv/bin/activate  # Linux / macOS 
venv\Scripts\activate     # Windows
```
Install dependencies
```
pip install -r requirements.txt
```
⚠️ **Database Setup Note**  

- The app is configured to use **Oracle ATP** by default.  
- To run locally with the included sample data, use **SQLite3** instead.  

**Steps:**
1. Open `worldLakeQuizApp/settings.py`.  
2. Comment out the Oracle section and uncomment the SQLite3 section:

```
# SQLite3 (for local testing with included data)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        ...
    }
}


# Oracle (default)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        ...
    }
}
```
Run the migrations and insert data:
```
python manage.py migrate
python manage.py import_csv
```


Run the Django server
```
python manage.py runserver
```
Open your browser at: `http://127.0.0.1:8000/`




 
📌GitHub:  
https://github.com/marc32132

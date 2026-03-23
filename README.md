## 🌍 Lakes of the World Quiz – Django App

Description:
A web application built with Django that allows users to take a quiz about lakes around the world. The data was collected via web scraping from the International Lake Environment Committee Foundation. The quiz generates 5 questions with 4 multiple-choice answers. Users can also browse all lakes and their locations with a search function.

### 🛠 Technologies

Backend: Python 3.11+, Django  
Database: OracleSQL  
Version control: Git  


### ⚡ Features

Generates a quiz with 5 questions and 4 multiple-choice answers  
Browse all lakes and their locations  
Search for specific lakes  
Simple and user-friendly web interface  


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
App currently is meant to work with OracleSQL database but you can comment the part of the code that sets the database as Oracle 
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        ...
    }
}
```
and uncomment the part that sets the database as sqlite3 
```
DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.sqlite3',
         ...
     }
}
```

Run the Django server
```
python manage.py runserver
```
Open your browser at: `http://127.0.0.1:8000/`




 
📌GitHub:  
https://github.com/marc32132

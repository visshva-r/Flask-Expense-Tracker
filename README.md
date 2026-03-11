# Personal Finance Analytics Dashboard

A full-stack web application built with Python and Flask designed to help users securely track, categorize, and visualize their daily financial transactions. 

## System Architecture
* **Backend:** Python, Flask 
* **Database:** SQLite / SQLAlchemy ORM (`models.py`)
* **Routing & Logic:** Modularized Blueprints/Routes (`routes.py`)
* **Frontend:** HTML5, CSS3, Jinja2 Templating (`base.html`, `dashboard.html`)
* **Security:** Secure user authentication, password hashing, and form validation (`forms.py`)

## Core Features
* **User Authentication:** Secure login and registration system protecting personal financial data.
* **Transaction Management:** Full CRUD operations for adding, updating, and deleting daily expenses.
* **Analytics Dashboard:** Dynamic data visualization providing actionable insights into spending habits and categorized expenses.

## Local Setup & Installation
1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment and install dependencies: 
   ```bash
   pip install -r requirements.txt
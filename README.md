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
* **Transaction Management:** Add, edit, and delete daily expenses per user.
* **Analytics Dashboard:** Dynamic pie chart visualization providing insights into spending by category.
* **CSV Export:** One-click export of your expense history as a CSV file.

## Local Setup & Installation

1. Clone the repository.
2. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the environment and install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. (Optional but recommended) Configure environment variables in a `.env` file or your shell:

   - `SECRET_KEY` – secret key for Flask sessions (default: `dev-secret-key-change-me`)
   - `DATABASE_URL` – database URL (default: `sqlite:///expenses.db`)

5. Run the application:

   ```bash
   python run.py
   ```

6. Open your browser and navigate to `http://127.0.0.1:5000/`.

## Testing

From the project root, run the full route and page tests:

```bash
python tests/test_routes.py
```

This checks every page (index, login, register, dashboard, add/edit/delete expense, export CSV, logout) and verifies redirects and 404 handling.

## Live Demo

[flask-expense-tracker-e5tn.onrender.com](https://flask-expense-tracker-e5tn.onrender.com)
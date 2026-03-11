from app import create_app
from app import db

app = create_app()

# This tells SQLAlchemy to create the database and tables if they don't exist yet
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
"""
Full demo test of every page and route. Run from project root:
  python tests/test_routes.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_all_pages():
    from app import create_app, db
    from app.models import User, Expense
    from werkzeug.security import generate_password_hash

    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as c:
        with app.app_context():
            db.create_all()
            if User.query.filter_by(username='testuser').first() is None:
                u = User(
                    username='testuser',
                    password=generate_password_hash('testpass123', method='pbkdf2:sha256'),
                )
                db.session.add(u)
                db.session.commit()

        # ----- Index -----
        r = c.get('/')
        assert r.status_code == 200, f'GET / failed: {r.status_code}'
        assert b'Expense Tracker' in r.data or b'Welcome' in r.data

        # ----- Login (GET) -----
        r = c.get('/login')
        assert r.status_code == 200, f'GET /login failed: {r.status_code}'

        # ----- Register (GET) -----
        r = c.get('/register')
        assert r.status_code == 200, f'GET /register failed: {r.status_code}'

        # ----- Login (POST) -----
        r = c.post('/login', data={'username': 'testuser', 'password': 'testpass123'}, follow_redirects=True)
        assert r.status_code == 200, f'POST /login failed: {r.status_code}'
        assert b'Dashboard' in r.data or b'Add' in r.data or b'expense' in r.data.lower()

        # ----- Dashboard (GET) -----
        r = c.get('/dashboard')
        assert r.status_code == 200, f'GET /dashboard failed: {r.status_code}'

        # ----- Add expense -----
        r = c.post('/dashboard', data={'amount': '25.50', 'category': 'Food'}, follow_redirects=True)
        assert r.status_code == 200, f'POST /dashboard failed: {r.status_code}'

        with app.app_context():
            u = User.query.filter_by(username='testuser').first()
            assert u is not None, 'Test user should exist'
            exp = Expense.query.filter_by(user_id=u.id).first()
            assert exp is not None, 'Expense should exist after add'
            exp_id = exp.id

        # ----- Edit expense (GET) -----
        r = c.get(f'/expense/{exp_id}/edit')
        assert r.status_code == 200, f'GET /expense/{exp_id}/edit failed: {r.status_code}'

        # ----- Edit expense (POST) -----
        r = c.post(f'/expense/{exp_id}/edit', data={'amount': '30.00', 'category': 'Travel'}, follow_redirects=True)
        assert r.status_code == 200, f'POST /expense/{exp_id}/edit failed: {r.status_code}'

        # ----- Export CSV -----
        r = c.get('/export')
        assert r.status_code == 200, f'GET /export failed: {r.status_code}'
        assert 'text/csv' in r.headers.get('Content-Type', '') or b'Category' in r.data

        # ----- Delete expense -----
        r = c.post(f'/expense/{exp_id}/delete', follow_redirects=True)
        assert r.status_code == 200, f'POST /expense/{exp_id}/delete failed: {r.status_code}'

        # ----- Logout -----
        r = c.get('/logout', follow_redirects=True)
        assert r.status_code == 200, f'GET /logout failed: {r.status_code}'

        # ----- Dashboard without login -> redirect -----
        r = c.get('/dashboard', follow_redirects=False)
        assert r.status_code == 302, f'GET /dashboard (no auth) should redirect: {r.status_code}'
        assert 'login' in r.headers.get('Location', '').lower()

        # ----- Edit non-existent expense -> 404 -----
        r = c.post('/login', data={'username': 'testuser', 'password': 'testpass123'}, follow_redirects=True)
        r = c.get('/expense/99999/edit')
        assert r.status_code == 404, f'GET /expense/99999/edit should 404: {r.status_code}'

    print('All route tests passed.')


if __name__ == '__main__':
    test_all_pages()

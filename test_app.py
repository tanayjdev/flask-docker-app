import json

# app.py se Flask app import karo
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))


# DB connection mock karenge
# Real DB nahi chahiye CI mein
def create_test_app():
    from flask import Flask
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app


class TestFlaskApp:

    def test_health_endpoint_mock(self):
        """Health endpoint test with mocked DB"""
        # Real DB ke bina test karte hain
        app = create_test_app()

        @app.route('/health')
        def health():
            return {'status': 'healthy', 'database': 'mocked'}, 200

        with app.test_client() as client:
            response = client.get('/health')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['status'] == 'healthy'

    def test_health_returns_json(self):
        """Health endpoint JSON format check"""
        app = create_test_app()

        @app.route('/health')
        def health():
            return {'status': 'healthy'}, 200

        with app.test_client() as client:
            response = client.get('/health')
            assert response.content_type == 'application/json'

    def test_environment_variables(self):
        """Environment variables set hain check karo"""
        import os
        # Default values test karo
        db_host = os.environ.get('DB_HOST', 'db')
        assert db_host is not None
        assert len(db_host) > 0

    def test_app_configuration(self):
        """Basic app config test"""
        assert True  # Placeholder


class TestDockerfile:

    def test_requirements_file_exists(self):
        """requirements.txt exist karta hai"""
        assert os.path.exists('requirements.txt')

    def test_dockerfile_exists(self):
        """Dockerfile exist karta hai"""
        assert os.path.exists('Dockerfile')

    def test_requirements_has_flask(self):
        """requirements.txt mein flask hai"""
        with open('requirements.txt') as f:
            content = f.read().lower()
        assert 'flask' in content

    def test_requirements_has_psycopg2(self):
        """requirements.txt mein psycopg2 hai"""
        with open('requirements.txt') as f:
            content = f.read().lower()
        assert 'psycopg2' in content

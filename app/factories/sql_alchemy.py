from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def setup_sql_alchemmy(app):
    db.init_app(app)
    with app.app_context():
        # Create all tables
        db.create_all()
    return app

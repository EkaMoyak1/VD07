from app import db, create_app
import os

def init_db():
    app = create_app()
    with app.app_context():
        db_path = os.path.join(app.instance_path, 'site.db')
        if not os.path.exists(db_path):
            db.create_all()
            print(f"База данных создана в {db_path}")
        else:
            print("База данных уже существует")

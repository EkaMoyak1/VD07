from app import create_app
from app.database import init_db
import os

app = create_app()

if __name__ == '__main__':
    # Проверка и создание БД при запуске
    if not os.path.exists('instance/site.db'):
        init_db()
    app.run(debug=True)

from app import app
from app.db import db

db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

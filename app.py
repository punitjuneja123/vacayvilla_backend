from routes.users import users_bp
from routes.property import property_bp
from flask import Flask
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv
from flask_cors import CORS
load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = 'sql6.freesqldatabase.com'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)


# routes
@app.route('/')
def welcome():
    return 'Welcome to Vacayvilla'


app.register_blueprint(users_bp, mysql=mysql)
app.register_blueprint(property_bp, mysql=mysql)


if __name__ == '__main__':
    app.run(debug=True)

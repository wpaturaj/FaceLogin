from configparser import ConfigParser
from app import create_app,db


config_object = ConfigParser()
config_object.read("config.ini")

appka=create_app(config_object['DATABASE'])

db.create_all(app=appka)

if __name__ == '__main__':
	appka.secret_key = config_object['AWS']['secretkey']
	appka.config['SESSION_TYPE'] = config_object['AWS']['filesystem']
	appka.run(debug=True)
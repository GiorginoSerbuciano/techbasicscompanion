import os

class Config:
	SECRET_KEY = os.environ.get('TBCOMP_SECRET_KEY')
	SQLALCHEMY_DATABASE_URI= os.environ.get('TBCOMP_SQLALCHEMY_DATABASE_URI')
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_POST = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('TBCOMP_MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('TBCOMP_MAIL_PASSWORD')
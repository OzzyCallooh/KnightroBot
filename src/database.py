from config import config, verify_config

import sys

import sqlalchemy
from sqlalchemy import Column, DateTime, String, BigInteger, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

verify_config([
	'database',
	'database.uri',
	'database.trackModifications'
])

Base = declarative_base()

engine = create_engine(
	config['database']['uri'],
	pool_recycle=60*3,
	echo=False
)
dbsession = sessionmaker(bind=engine)

def init():
	try:
		Base.metadata.create_all(engine)
		print("Database initialized")
	except sqlalchemy.exc.OperationalError as e:
		print('Problem while connecting to database:\n{}'.format(str(e)))
		sys.exit(1)
"""
	Configuration file loader

	Usage:
		from config import config, verify_config
		verify_config(['debug_mode'])
		print('Debug mode: ' + str(config['debug_mode']))
"""

import sys, json

# The global config map
config = None

# Exceptions
class ConfigError(Exception):
	pass

class MissingConfigError(ConfigError):
	def __init__(self, key):
		self.key = key
		self.message = 'Missing key in configuration: {}'.format(key)

def verify_config(config_fields):
	"""Verifies that the given fields are included in the configuration file"""
	try:
		# Verify required data exists
		for field in config_fields:
			base = config
			for s in field.split('.'):
				if s not in base:
					raise MissingConfigError(field)
				else:
					base = base[s]
	except MissingConfigError as e:
		print('Configuration is missing key: {}'.format(e))
		sys.exit(1)

def load_config():
	global config

	# Get config file name from command line argument
	config_filename = 'config.json'
	if len(sys.argv) >= 2:
		config_filename = sys.argv[1]
	else:
		print('Provide the config filename as a command line argument')
		sys.exit(1)

	try:
		# Open and read file
		with open(config_filename) as f:
			config = json.loads(f.read())
		config['config_filename'] = config_filename
	except FileNotFoundError as e:
		print('Configuration file not found: {filename}'.format(filename=config_filename))
		sys.exit(1)
	except json.JSONDecodeError as e:
		print('Error while parsing {filename}: {error}'.format(filename=config_filename, error=e))
		sys.exit(1)
	except Exception as e:
		print('Other error while reading configuration: {}'.format(e))
		sys.exit(1)

load_config()

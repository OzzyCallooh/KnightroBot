import os

def get_relative_filename(filename):
	return os.path.join(os.path.dirname(__file__), filename)

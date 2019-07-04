from fasteners import InterProcessLock
from config import config, verify_config

verify_config(['lock_file'])

LOCK_FILE = config['lock_file']

lockyboy = InterProcessLock(LOCK_FILE)

def do_the_brew():
	print('Starting KnightroBot...')
	from knightrobot import main
	main()

gotten = lockyboy.acquire(blocking=False)
try:
	if gotten:
		print('Lock obtained')
		do_the_brew()
	else:
		print('Lock not obtained')
finally:
	if gotten:
		lockyboy.release()


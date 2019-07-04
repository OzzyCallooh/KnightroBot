PYTHON='python'
CONFIG_FILE=config/dev.config.json
LOCK_FILE = 'KnightroBot.lock'
DB_FILE = 'test.sqlite.db'
START_SCRIPT = 'src/knightrobot.py'

clean:
	rm -f $(LOCK_FILE)
	rm -f $(DB_FILE)

run:
	$(PYTHON) $(START_SCRIPT) $(CONFIG_FILE)
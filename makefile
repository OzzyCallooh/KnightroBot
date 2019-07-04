CONFIG_FILE=config/dev.config.json
LOCK_FILE = 'KnightroBot.lock'
DB_FILE = 'test.sqlite.db'

clean:
	rm $(LOCK_FILE)
	rm $(DB_FILE)

run:
	python src/startup.py $(CONFIG_FILE)
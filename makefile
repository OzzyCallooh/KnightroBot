PYTHON='python'
CONFIG_FILE=config/dev.config.json
START_SCRIPT = 'src/knightrobot.py'

clean:
	rm -rf src/__pycache__

run:
	$(PYTHON) $(START_SCRIPT) $(CONFIG_FILE)
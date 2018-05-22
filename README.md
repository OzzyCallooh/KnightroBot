# KnightroBot

![Knightro](img/Knightro.jpg)

KnightroBot is a bot for the [Telegram](http://telegram.org/) chat platform, designed to be a utility for the [UCF Furs](http://ucffurs.org/) group. Written by [Ozzy Callooh](http://t.me/OzzyC), he bears no affiliation to [UCF](http://ucf.edu) itself.

## Using the Bot

KnightroBot provides a few utilities for campus information.

* **/start** - Shows welcome message
* **/help** - Displays available commands
* **/about** - Displays about information
* **/garage** - Get the current status of each garage on campus
* **/garage &gt;letter&lt;** - Get the current status of a specific garage
* **/whereis &gt;location&lt;** - Search the campus directory for &gt;location&lt;

## Dependencies

KnightroBot is programmed in Python 3. He uses the following dependencies, which can be installed using `pip`.

* [Fasteners](https://fasteners.readthedocs.io) - `fasteners`
* [Requests](http://docs.python-requests.org) - `requests`
* [Python Telegram Bot](http://python-telegram-bot.org) - `python-telegram-bot`
* [SQLAlchemy](http://sqlalchemy.org) - `sqlalchemy`

## Configuration

KnightroBot uses [JSON](http://json.org) configuration files, usually with a name like `*.config.json` (`dev.config.json` and `prod.config.json` are good config file names for testing and production environments, respectively). The file [sample.config.json](sample.config.json) provides an example configuration file with notes on each parameter. Most notably, the Telegram bot token should be pasted in the configuration file.

## Running the Bot

KnightroBot uses the [Fasteners](https://fasteners.readthedocs.io) library to prevent multiple copies of itself from running at once. Run the bot using Python 3 via the command line:

```shell
python startup.py dev.config.json
```
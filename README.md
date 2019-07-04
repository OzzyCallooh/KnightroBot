# KnightroBot

![Knightro](img/Knightro.jpg)

[KnightroBot](http://t.me/KnightroBot) is a bot for the [Telegram](http://telegram.org/) chat platform, designed to be a utility for the [UCF Furs](http://ucffurs.org/) group. Written by [Ozzy Callooh](http://t.me/OzzyC), he bears no affiliation to [UCF](http://ucf.edu) itself.

## Using the Bot

[Click this link to message the bot!](http://t.me/KnightroBot) KnightroBot provides a few utilities for campus information.

* **/start** - Shows welcome message
* **/help** - Displays available commands
* **/about** - Displays about information
* **/garage** - Get the current status of each garage on campus
* **/garage &lt;letter&gt;** - Get the current status of a specific garage
* **/whereis &lt;location&gt;** - Search the campus directory for &lt;location&gt;

## Dependencies

KnightroBot is programmed in Python 3. He uses the following dependencies, which can be installed using `pip`.

* [Requests](http://docs.python-requests.org) - `requests`
* [Python Telegram Bot](http://python-telegram-bot.org) - `python-telegram-bot`

## Configuration

KnightroBot uses [JSON](http://json.org) configuration files, usually with a name like `*.config.json` (`dev.config.json` and `prod.config.json` are good config file names for testing and production environments, respectively). The file [sample.config.json](sample.config.json) provides an example configuration file with notes on each parameter. Most notably, the Telegram bot token should be pasted in the configuration file.

## Running the Bot

Run the bot using Python 3 and provide a JSON configuration file as the first argument.

```shell
python startup.py dev.config.json
```

Previously, KnightroBot used the [Fasteners](https://fasteners.readthedocs.io) library and an intermediate startup script to prevent multiple copies of itself from running at once.
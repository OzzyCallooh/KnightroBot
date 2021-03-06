# knightrobot.py
# Ozzy Callooh

import logging
from math import floor

from telegram import ChatAction
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler
from telegram.ext.filters import Filters

from config import config, verify_config
from parking import command_garage
from navigation import load_locations, command_whereis
from privileges import privileged_command
from util import logged_command, send_action

@logged_command
@send_action(ChatAction.TYPING)
def command_start(bot, update):
	update.message.reply_text(config['knightro']['start'], parse_mode='MARKDOWN', disable_web_page_preview=True)

@logged_command
@send_action(ChatAction.TYPING)
def command_help(bot, update):
	update.message.reply_text(config['knightro']['help'], parse_mode='MARKDOWN', disable_web_page_preview=True)

@logged_command
@send_action(ChatAction.TYPING)
def command_about(bot, update):
	update.message.reply_text(config['knightro']['about'], parse_mode='MARKDOWN', disable_web_page_preview=True)

@logged_command
@send_action(ChatAction.TYPING)
def command_alert(bot, update):
	update.message.reply_text(config['knightro']['alert'], parse_mode='MARKDOWN', disable_web_page_preview=True)

def handle_new_chat_member(bot, update):
	if len(update.message.new_chat_members) <= 0:
		return

	# Ignore bot additions
	has_non_bot = False
	for user in update.message.new_chat_members:
		if user.is_bot and user.id == bot.id:
			pass
		if not user.is_bot:
			has_non_bot = True
			break
	if not has_non_bot:
		return

	update.message.reply_text(config['knightro']['welcome'], parse_mode='MARKDOWN', disable_web_page_preview=True)

def handle_error(bot, update, tg_error):
	update.message.reply_text(config['knightro']['errormsg'], parse_mode='MARKDOWN', disable_web_page_preview=True)

def main():
	verify_config([
		'logging',
		'logging.level',
		'telegram',
		'telegram.token',
		'knightro',
		'knightro.welcome',
		'knightro.start',
		'knightro.help',
		'knightro.alert',
		'knightro.about'
	])

	# Logging
	logging.basicConfig(
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
		level=config['logging']['level']
	)

	# Initializations
	load_locations()

	# Create the updater and get the dispatcher
	updater = Updater(token=config['telegram']['token'])
	dispatcher = updater.dispatcher

	# Handlers
	dispatcher.add_handler(CommandHandler('start', command_start))
	dispatcher.add_handler(CommandHandler('about', command_about))
	dispatcher.add_handler(CommandHandler('help', command_help))
	dispatcher.add_handler(CommandHandler('alert', command_alert))
	dispatcher.add_handler(CommandHandler('garage', command_garage, pass_args=True))
	dispatcher.add_handler(CommandHandler('whereis', command_whereis, pass_args=True))
	dispatcher.add_handler(MessageHandler(
		callback=handle_new_chat_member,
		filters=Filters.status_update.new_chat_members
	))
	dispatcher.add_error_handler(handle_error)

	# Start
	if config['telegram']['use_webhook']:
		verify_config([
			'telegram.webhook',
			'telegram.webhook.host',
			'telegram.webhook.internal_port',
			'telegram.webhook.cert',
			'telegram.webhook.key'
		])
		logging.info('Using webhook')
		updater.start_webhook(
			listen='127.0.0.1',
			port=config['telegram']['webhook']['internal_port'],
			url_path=config['telegram']['token']
		)
		updater.bot.set_webhook(
			url='https://' + config['telegram']['webhook']['host'] + \
			    '/' + config['telegram']['token'],
			certificate=open(config['telegram']['webhook']['cert'], 'rb')
		)
	else:
		logging.info('Start polling')
		updater.start_polling()
	logging.info('Updater idling')
	updater.idle()
	logging.info('Exiting')

if __name__ == '__main__':
	main()
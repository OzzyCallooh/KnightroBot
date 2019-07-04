# knightrobot.py
# Ozzy Callooh

import logging
from math import floor

from telegram import ChatAction
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, CallbackQueryHandler

import database
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
@privileged_command('operator')
def command_kill(bot, update):
	update.message.reply_text(config['knightro']['kill'], parse_mode='MARKDOWN', disable_web_page_preview=True)	

def handler_button(bot, update):
	pass
	#rsvp.handler_button(bot, update)
	#polls.handler_button(bot, update)

def main():
	verify_config([
		'logging',
		'logging.level',
		'telegram',
		'telegram.token',
		'knightro',
		'knightro.start',
		'knightro.help',
		'knightro.about',
		'knightro.kill'
	])

	# Logging
	logging.basicConfig(
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
		level=config['logging']['level']
	)

	# Initializations
	load_locations()
	database.init()

	# Create the updater and get the dispatcher
	updater = Updater(token=config['telegram']['token'])
	dispatcher = updater.dispatcher

	# Handlers
	dispatcher.add_handler(CommandHandler('start', command_start))
	dispatcher.add_handler(CommandHandler('about', command_about))
	dispatcher.add_handler(CommandHandler('help', command_help))
	dispatcher.add_handler(CommandHandler('kill', command_kill))
	dispatcher.add_handler(CommandHandler('garage', command_garage, pass_args=True))
	dispatcher.add_handler(CommandHandler('whereis', command_whereis, pass_args=True))
	dispatcher.add_handler(CallbackQueryHandler(handler_button))

	# Module dispatcher command setup 
	#rsvp.init_db()
	#rsvp.setup_dispatcher(dispatcher)
	#polls.setup_dispatcher(dispatcher)
	# Start
	logging.debug('Go knights!')

	if config['telegram']['use_webhook']:
		verify_config([
			'telegram.webhook',
			'telegram.webhook.host',
			'telegram.webhook.internal_port',
			'telegram.webhook.cert',
			'telegram.webhook.key'
		])
		logging.debug('Using webhook')
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
		logging.debug('Start polling')
		updater.start_polling()
	updater.idle()

	logging.debug('Charge on!')

if __name__ == '__main__':
	main()
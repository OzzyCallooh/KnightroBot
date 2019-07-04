# knightrobot.py
# Ozzy Callooh

import logging
from math import floor
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, CallbackQueryHandler

import database
from config import config, verify_config
from parking import command_garage
from navigation import command_whereis
from privileges import privileged_command

def command_start(bot, update):
	update.message.reply_text(config['knightro']['start'], parse_mode='MARKDOWN', disable_web_page_preview=True)

def command_help(bot, update):
	update.message.reply_text(config['knightro']['help'], parse_mode='MARKDOWN', disable_web_page_preview=True)

def command_about(bot, update):
	update.message.reply_text(config['knightro']['about'], parse_mode='MARKDOWN', disable_web_page_preview=True)

@privileged_command('operator')
def command_kill(bot, update):
	update.message.reply_text(config['knightro']['kill'], parse_mode='MARKDOWN', disable_web_page_preview=True)	

def handler_button(bot, update):
	pass
	#rsvp.handler_button(bot, update)
	#polls.handler_button(bot, update)

def main():
	verify_config([
		'debug_mode',
		'telegram',
		'telegram.token',
		'knightro',
		'knightro.start',
		'knightro.help',
		'knightro.about',
		'knightro.kill'
	])

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

	# Logs
	logging.basicConfig(
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
		level=logging.DEBUG if config['debug_mode'] else logging.INFO
	)

	# Start
	print('Go Knights!')
	try:
		updater.start_polling()
		updater.idle()
	except KeyboardInterrupt:
		print('Keyboard interrupted')
	finally:
		print('Charge On!')
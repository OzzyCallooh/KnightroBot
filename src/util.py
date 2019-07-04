import os
import logging
from functools import wraps

def logged_command(func):
	@wraps(func)
	def wrapped(bot, update, *args, **kwargs):
		msg = '[user:{userid}{username},chat:{chatid}]: ' + update.message.text
		logging.info(msg.format(
			userid=update.effective_user.id,
			username=('(@' + update.effective_user.username + ')') \
				if update.effective_user.username != None \
				and len(update.effective_user.username) > 0 \
				else '',
			chatid=',' + str(update.effective_chat.id)
		))
		return func(bot, update, *args, **kwargs)
	return wrapped

def get_relative_filename(filename):
	return os.path.join(os.path.dirname(__file__), filename)

import json
import logging

from config import config, verify_config
from util import get_relative_filename

verify_config([
	'navigation',
	'navigation.locations_file',
	'navigation.map_link'
])

LOCATIONS_FILENAME = config['navigation']['locations_file']

locations = []

class Location:
	@staticmethod
	def search(text):
		text = text.lower().strip()
		keywords = text.split()
		#print('Searching locations for "{}"'.format(text))
		bestScore = 0
		bestLoc = None
		for loc in locations:
			score = 0
			if loc.abbr == text:
				#print('Exact match via abbr')
				score += 200
			elif loc.nameLower == text:
				#print('Exact match via name')
				score += 180
			elif loc.titleLower == text:
				#print('Exact match via title')
				score += 160
			else:
				for keyword in keywords:
					keywordFound = False
					if keyword in loc.idLower:
						score += 6 * len(keyword)
						keywordFound = True
					if keyword in loc.nameLower:
						score += 5 * len(keyword)
						keywordFound = True
					if keyword in loc.titleLower:
						score += 4 * len(keyword)
						keywordFound = True
					if keyword in loc.descriptionLower:
						score += 1 * len(keyword)
						keywordFound = True
					if not keywordFound:
						score -= 10
			if score > bestScore:
				bestScore = score
				bestLoc = loc
		if bestLoc:
			#print('Selected best location with score {}:'.format(bestScore))
			#print('id={}\ntitle={}\nname={}\ndescr={}'.format(bestLoc.id, bestLoc.titleLower, bestLoc.nameLower, bestLoc.descriptionLower))
			pass
		return (bestLoc, score)

	def __init__(self, raw_data):
		self.id = raw_data.get('id', '-1')
		if self.id:
			self.idLower = self.id.lower()
		else:
			self.idLower = '~'

		self.abbr = raw_data.get('abbreviation')
		if self.abbr != None:
			self.abbr = self.abbr.lower()

		self.title = raw_data.get('title', '')
		if self.title:
			self.titleLower = self.title.lower()
		else:
			self.titleLower = ''

		self.name = raw_data.get('name', '')
		if self.name:
			self.nameLower = self.name.lower()
		else:
			self.nameLower = ''

		self.description = raw_data.get('description', '')
		if self.description:
			self.descriptionLower = self.description.lower()
		else:
			self.descriptionLower = ''

		self.googlemap_point = raw_data.get('googlemap_point')

		if type(self.googlemap_point) == list:
			self.latitude = float(self.googlemap_point[0])
			self.longitude = float(self.googlemap_point[1])

		self.profile_link = raw_data.get('profile_link')


def load_locations():
	loc_data = None
	with open(get_relative_filename(LOCATIONS_FILENAME)) as f:
		loc_data = json.loads(f.read())
	for raw_data in loc_data:
		locations.append(Location(raw_data))
	logging.info('Loaded {} locations'.format(len(locations)))

def command_whereis(bot, update, args=None):
	#print('/whereis')
	if len(args) < 1:
		update.message.reply_text('Format: /whereis <place>', quote=False)
		return
	place = ' '.join(args)
	loc, score = Location.search(place)
	if loc and loc.googlemap_point != None:
		#update.message.reply_text('Found {name}!'.format(name=loc.name))
		out = '*Found place*: {}'.format(loc.title)
		if loc.profile_link:
			linkText = loc.title
			if linkText == None or len(linkText) == 0:
				linkText = loc.name
			out = '*Found place*: [{linkText}]({link})'.format(linkText=linkText, link=loc.profile_link)

		out += ' ([Map]({maplink}))'.format(maplink=config['navigation']['map_link'] + '/?show=' + loc.id)

		update.message.reply_text(out, parse_mode='Markdown', disable_web_page_preview=True)
		update.message.reply_location(quote=False, latitude=loc.latitude, longitude=loc.longitude)
	else:
		update.message.reply_text('No search results. Try simpler or fewer keywords. [UCF Campus Map]({maplink})'.format(maplink=config['navigation']['map_link']), parse_mode='Markdown', disable_web_page_preview=True)
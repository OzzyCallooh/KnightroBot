from math import floor
import re
import requests
from operator import attrgetter

from config import config, verify_config
from util import logged_command
from mwt import MWT

verify_config([
	'parking',
	'parking.url',
	'parking.location_ids',
	'parking.cache_time',
	'navigation.map_link'
])

PARKING_URL = config['parking']['url'] # http://secure.parking.ucf.edu/GarageCount/
LOCATION_IDS = config['parking']['location_ids']
MAP_LINK = config['navigation']['map_link']

class Garage():
	def __init__(self, name, avail, total):
		self.name = name
		self.avail = avail
		self.total = total

	def __str__(self):
		return '{name}\t{percentFull}%\t{avail}/{total}'.format(
			name=self.name,
			avail=self.avail,
			total=self.total,
			percentFull=floor((1 - self.avail / self.total) * 100)
		)

	def getLocationId(self):
		return LOCATION_IDS.get(self.name, -1)

	def getMarkdownName(self):
		locId = self.getLocationId()
		if locId != -1:
			return '[Garage {name}]({maplink}/?show={id})'.format(
				maplink=MAP_LINK,
				name=self.name,
				id=locId
			)
		else:
			return 'Garage {name}'.format(self.name)

class CapacityReport():
	regex_capacities = re.compile(r'\<strong\>([0-9]+)\<\/strong\>\/([0-9]+)')
	regex_names = re.compile(r'Garage ([^\<]+)\<\/td\>')

	def __init__(self, pageText):
		self.garages = []
		capacitiesStr = CapacityReport.regex_capacities.findall(pageText)
		capacitiesInt = []
		garage_names = CapacityReport.regex_names.findall(pageText)

		# First one is "Name" from "Garage Name" (the header)
		if garage_names[0] == 'Name':
			garage_names.pop(0)

		for capacity in capacitiesStr:
			capacitiesInt.append((int(capacity[0]), int(capacity[1])))

		for i in range(0, len(capacitiesInt)):
			self.garages.append(Garage(garage_names[i], capacitiesInt[i][0], capacitiesInt[i][1]))

	def __str__(self):
		s = 'Garage\tFull%\tSpots\n'
		for cap in self.garages:
			s += str(cap) + '\n'
		return s

	@classmethod
	@MWT(config['parking']['cache_time'])
	def fetch(cls):
		try:
			resp = requests.get(PARKING_URL, timeout=5)
			if resp != None and resp.status_code == 200:
				return CapacityReport(resp.text)
		except Exception:
			return None

@logged_command
def command_garage(bot, update, args=None):
	report = CapacityReport.fetch()
	if report:
		#out = '[Live Garage Status](http://secure.parking.ucf.edu/GarageCount/):\n'
		out = ''
		header = False
		report.garages.sort(key=attrgetter('avail'), reverse=True)
		filled = []
		garageSelected = None
		for garage in report.garages:
			if len(args) >= 1 and args[0].lower() == garage.name.lower():
				garageSelected = garage
				break
			if garage.avail > 0:
				if not header:
					out += '`Garage Free Full`'
					header = True
				out += '\n`{name: >6} {spaces} {percFull}`'.format(
					name=garage.name,
					percFull=('{perc:>2}').format(
						perc=str(floor(100 - garage.avail/garage.total*100)) + '%'
					) if garage.avail != 0 else 'FULL',
					spaces=('{:>4}').format(garage.avail) if garage.avail != 0 else ''
				)
			else:
				filled.append(garage)
		if len(filled) > 0:
			if len(filled) != len(report.garages):
				out += '\n`FULL: ' + ', '.join([garage.name for garage in filled]) + '`'
			else:
				out += '\nAll garages are full. Have you considered [Park and Ride](https://parking.ucf.edu/parkandride/)?'
		out += '\n[Live Status]({})\n'.format(PARKING_URL)

		if garageSelected:
			#out = '[Live Garage Status](http://secure.parking.ucf.edu/GarageCount/):'
			out = ''
			out += '{name} is *{perc}* full.'.format(
				name=garageSelected.getMarkdownName(),
				perc=str(floor(100 - garageSelected.avail/garageSelected.total*100)) + '%'
			)
			out += '\n{taken} of {avail} spots are taken.'.format(
				taken=garageSelected.total - garageSelected.avail,
				avail=garageSelected.total
			)
		elif len(args) >= 1:
			out = 'Unknown garage \"{}\".\n'.format(args[0]) + out
		update.message.reply_text(out, parse_mode='MARKDOWN', quote=False, disable_web_page_preview=True)
		#bot.send_message(text=out, parse_mode='Markdown')

	else:
		update.message.reply_text('Garage report not available at the moment.')


if __name__ == '__main__':
	report = CapacityReport.fetch()
	print(report)
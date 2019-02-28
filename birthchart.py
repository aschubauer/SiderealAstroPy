from globalinit import *

class Birthchart:

	def __init__(self, name, dt, lat, lng, hsys='W', sidereal=True):
		""" Birthchart constructor: name (string), datetime object (UT), latitude, longitude, 
			house system for house cusps, sidereal mode (default) """
		self.chartOwner = name
		self.birthTime = dt
		timedifftup = dt.timetuple()[:6] #year, month, day, hour, minute, second
		jt = swe.utc_to_jd(*timedifftup, swe.GREG_CAL) #convert to Julian time
		planetpos = [swe.calc_ut(jt[1], i, flag=int(sidereal)*swe.FLG_SIDEREAL) for i in range(len(PLANETKEY))]
		self.planets = {planetName: (planetpos[i], swe.split_deg(planetpos[i][0],8)) for i, planetName in enumerate(PLANETKEY)}
		cuspdegs, angledegs = swe.houses_ex(jt[1], lat, lng, hsys=hsys.encode(), flag=int(sidereal)*swe.FLG_SIDEREAL)
		self.houseCusps = tuple((cuspdegs[i], swe.split_deg(cuspdegs[i],8)) for i in range(len(cuspdegs)))
		self.angles = {angleName: (angledegs[i], swe.split_deg(angledegs[i],8)) for i, angleName in enumerate(ANGLEKEY)}
		self.sect = 'Day' if (self.angles['Ascendant'][0] - self.planets['Sun'][0][0]) % 360 <= 180 else 'Night'
		self.lots = {}


	def calculateLots(self):
		""" calculates various Dorothean lots plus others from Valens and Paulus """
		asc = self.angles['Ascendant'][0]
		self.lots = { 'Fortune': (asc + self.planets['Moon'][0][0] - self.planets['Sun'][0][0]) % 360 if self.sect == 'Day' \
								else (asc + self.planets['Sun'][0][0] - self.planets['Moon'][0][0]) % 360,
					'Spirit': (asc + self.planets['Sun'][0][0] - self.planets['Moon'][0][0]) % 360 if self.sect == 'Day' \
								else (asc + self.planets['Moon'][0][0] - self.planets['Sun'][0][0]) % 360,
					'Father1': (asc + self.planets['Saturn'][0][0] - self.planets['Sun'][0][0]) % 360 if self.sect == 'Day' \
								else (asc + self.planets['Sun'][0][0] - self.planets['Saturn'][0][0]) % 360,
					'Father2': (asc + self.planets['Jupiter'][0][0] - self.planets['Mars'][0][0]) % 360 if self.sect == 'Day' \
								else (asc + self.planets['Mars'][0][0] - self.planets['Jupiter'][0][0]) % 360,
					'Mother': (asc + self.planets['Moon'][0][0] - self.planets['Venus'][0][0]) % 360 if self.sect == 'Day' \
								else (asc + self.planets['Venus'][0][0] - self.planets['Moon'][0][0]) % 360,
					'Siblings': (asc + self.planets['Saturn'][0][0] - self.planets['Jupiter'][0][0]) % 360 if self.sect == 'Day' \
								else (asc + self.planets['Jupiter'][0][0] - self.planets['Saturn'][0][0]) % 360,
					'Wedding (men)': (asc + self.planets['Venus'][0][0] - self.planets['Saturn'][0][0]) % 360 if self.sect == 'Day' \
								else (asc + self.planets['Saturn'][0][0] - self.planets['Venus'][0][0]) % 360,
					'Wedding (women)': (asc + self.planets['Saturn'][0][0] - self.planets['Venus'][0][0]) % 360 if self.sect == 'Day' \
								else (asc + self.planets['Venus'][0][0] - self.planets['Saturn'][0][0]) % 360,
					'Pleasure & wedding': (asc + self.houseCusps[6][0] - self.planets['Venus'][0][0]) % 360 }
		self.lots['Eros_Valens'] = (asc + self.lots['Spirit'] - self.lots['Fortune']) % 360 if self.sect == 'Day' \
							else (asc + self.lots['Fortune'] - self.lots['Spirit']) % 360
		self.lots['Necessity_Valens'] = (asc + self.lots['Fortune'] - self.lots['Spirit']) % 360 if self.sect == 'Day' \
							else (asc + self.lots['Spirit'] - self.lots['Fortune']) % 360
		self.lots['Eros_Paulus'] = (asc + self.planets['Venus'][0][0] - self.lots['Spirit']) % 360 if self.sect == 'Day' \
							else (asc + self.lots['Spirit'] - self.planets['Venus'][0][0]) % 360
		self.lots['Necessity_Paulus'] = (asc + self.lots['Fortune'] - self.planets['Mercury'][0][0]) % 360 if self.sect == 'Day' \
							else (asc + self.planets['Mercury'][0][0] - self.lots['Fortune']) % 360
		self.lots['Courage'] = (asc + self.lots['Fortune'] - self.planets['Mars'][0][0]) % 360 if self.sect == 'Day' \
							else (asc + self.planets['Mars'][0][0] - self.lots['Fortune']) % 360
		self.lots['Victory'] = (asc + self.planets['Jupiter'][0][0] - self.lots['Spirit']) % 360 if self.sect == 'Day' \
							else (asc + self.lots['Spirit'] - self.planets['Jupiter'][0][0]) % 360
		self.lots['Nemesis'] = (asc + self.lots['Fortune'] - self.planets['Saturn'][0][0]) % 360 if self.sect == 'Day' \
							else (asc + self.planets['Saturn'][0][0] - self.lots['Fortune']) % 360
		house2sign = SIGNKEY[swe.split_deg(self.houseCusps[1][0],8)[4]]
		house2ruler = RULERS[house2sign]
		self.lots['Assets'] = (asc + self.houseCusps[1][0] - self.planets[house2ruler][0][0]) % 360

		for lot in self.lots:
			self.lots[lot] = (self.lots[lot], swe.split_deg(self.lots[lot],8))
		
		self.ZR = {}


	def calculateZR(self, lotname, maxage=100):
		""" calculates all zodiacal releasing periods and subperiods (L1 = longest to L4 = shortest)
			for a particular lot from birth to maxage """
		if not self.lots:
			self.calculateLots()
		enddt = self.birthTime + timedelta(days=365.25*maxage)
		l1_start = self.birthTime
		l1_sign = SIGNKEY[self.lots[lotname][1][4]]
		l1 = []
		l2 = []
		l3 = []
		l4 = []
		while l1_start < enddt:
			l1_period = ZR_PERIODS[l1_sign]
			l1.append((l1_start, l1_sign))
			l2_start = l1_start
			l1_start += timedelta(days=360*l1_period)
			l2_startsign = l2_sign = l1_sign
			lb2 = False
			while l2_start < l1_start and l2_start < enddt:
				l2_period = ZR_PERIODS[l2_sign]
				l2.append((l2_start, l2_sign))
				l3_start = l2_start
				l2_start += timedelta(days=30*l2_period)
				l3_startsign = l3_sign = l2_sign
				lb3 = False
				while l3_start < l2_start and l3_start < l1_start and l3_start < enddt:
					l3_period = ZR_PERIODS[l3_sign]
					l3.append((l3_start, l3_sign))
					l4_start = l3_start
					l3_start += timedelta(days=2.5*l3_period)
					l4_startsign = l4_sign = l3_sign
					lb4 = False
					while l4_start < l3_start and l4_start < l2_start and l4_start < l1_start and l4_start < enddt:
						l4_period = ZR_PERIODS[l4_sign]
						l4.append((l4_start, l4_sign))
						l4_start += timedelta(hours=5*l4_period)
						l4_sign = SIGNKEY[(SIGNKEY.index(l4_sign)+1) % 12]
						if l4_sign == l4_startsign and not lb4:	#loosing of the bond
							l4_sign = SIGNKEY[(SIGNKEY.index(l4_sign)+6) % 12]
							lb4 = True
					l3_sign = SIGNKEY[(SIGNKEY.index(l3_sign)+1) % 12]
					if l3_sign == l3_startsign and not lb3:	#loosing of the bond
						l3_sign = SIGNKEY[(SIGNKEY.index(l3_sign)+6) % 12]
						lb3 = True
				l2_sign = SIGNKEY[(SIGNKEY.index(l2_sign)+1) % 12]
				if l2_sign == l2_startsign and not lb2:	#loosing of the bond
					l2_sign = SIGNKEY[(SIGNKEY.index(l2_sign)+6) % 12]
					lb2 = True
			l1_sign = SIGNKEY[(SIGNKEY.index(l1_sign)+1) % 12]
		self.ZR[lotname] = {'L1': l1, 'L2': l2, 'L3': l3, 'L4': l4}
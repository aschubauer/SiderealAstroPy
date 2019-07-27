# coding: utf-8
from globalinit import *

#LOCALTIMEDIFF = timedelta(hours = -4)
""" The lines below get local time from a time format string (Python 3 only).
	Local time can be hard-coded by entering the difference from UTC in the commented-out line above. """
FORMAT = '%Y-%m-%dT%H:%M:%S%z'
date = datetime.strptime(time.strftime(FORMAT, time.localtime()),FORMAT)
LOCALTIMEDIFF = timedelta(hours = int(date.tzname()[3:6]))


def twoPlanetsDistance(planet1, planet2, dt, sidereal=True):
	"""
	Helper function - computes the distance between two planets forming an aspect to one another.

	Takes as input 2 planet names as strings and a datetime object (in universal time) representing the date
	and time at which to calculate the planets' positions and how far they are from aspect with each other.
	Returns how close the planets are to aspect in degrees, the degree value of the closest aspect, and position
	and speed of both planets from swe.calc_ut().
	"""
	p1_i = PLANETKEY.index(planet1)
	p2_i = PLANETKEY.index(planet2)
	timedifftup = dt.timetuple()[:6] #year, month, day, hour, minute, second
	jt = swe.utc_to_jd(*timedifftup, swe.GREG_CAL) #convert to Julian time
	p1_coord = swe.calc_ut(jt[1], p1_i, flag=int(sidereal)*swe.FLG_SIDEREAL+swe.FLG_SPEED) #get position of planet1
	p1_x = p1_coord[0] #planet1's position (longitude/right ascension)
	p1_v = p1_coord[3] #planet1's speed in longitude/right ascension (deg/day)
	p2_coord = swe.calc_ut(jt[1], p2_i, flag=int(sidereal)*swe.FLG_SIDEREAL+swe.FLG_SPEED) #get same values for planet2
	p2_x = p2_coord[0]
	p2_v = p2_coord[3]
	diff = p1_x - p2_x
	angle = min(abs(diff),360-abs(diff)) #calculate angle between planets' positions
	dist, asp_i = min((abs(angle-ASPECTS[i]),i) for i in range(len(ASPECTS))) #planets' distance from their closest aspect and which aspect
	aspect = ASPECTS[asp_i]
	p1_ahead = round((p2_x+angle)%360,2) == round(p1_x,2) #p1 is ahead when it is the planet that is further along in the zodiac given angle <= 180° between p1 & p2
	perfecting = p1_ahead == ((angle > aspect and p2_v > p1_v) or (angle < aspect and p1_v > p2_v)) #if p1 is ahead, aspect is perfecting when this expression evaluates to true
																									#the converse is true when p2 is ahead
	return dist, ASPECTS[asp_i], p1_x, p2_x, p1_v, p2_v, perfecting


ALPHA = 0.75 #keeps Moon aspects from being missed by the following function

def getNextAspect(planet1, planet2, dt, sidereal=True):
	"""
	Finds the next aspect that will perfect between two planets.

	Given the input of two planet names (strings) and a datetime object (in universal time) from which to
	calculate the next aspect that will perfect, returns a datetime object representing when the perfection
	happens, the location of the two planets (degrees out of 360), and the aspect in number of degrees.

	"""
	retvals = twoPlanetsDistance(planet1, planet2, dt, sidereal=sidereal)
	dist, aspect, p1_x, p2_x, p1_v, p2_v = retvals[:6]
	while round(dist, 3) != 0:
		if dist < abs(p1_v) or dist < abs(p2_v): #if aspect is less than a day from perfection
			delta_t = min((dist / abs(p2_v - p1_v)), (dist / abs(p1_v + p2_v))) #step forward a small amount of time
			if planet1 == 'Moon' or planet2 == 'Moon': #decrease time step further to not skip over Moon aspect
				delta_t *= ALPHA
		else:
			delta_t = 1
		dt += timedelta(days=delta_t)
		retvals = twoPlanetsDistance(planet1, planet2, dt, sidereal=sidereal)
		dist, aspect, p1_x, p2_x, p1_v, p2_v = retvals[:6]
	return dt, p1_x, p2_x, aspect


def getAllNextAspects(start_dt, n, sidereal=True):
	"""
	Finds and returns all aspects that will perfect within n days of start_dt.

	start_dt is a datetime object in universal time; n is an integer. Returns list of aspect tuples sorted
	by date and time.

	"""
	end_dt = start_dt + timedelta(days=n)
	ASPECTS = []
	for i, planet1 in enumerate(PLANETKEY[:-1]): #the last planet will never be 1st in the pair
		for planet2 in PLANETKEY[i+1:]: #to avoid duplicate checks, second planet is always later in list
			dt = start_dt
			while dt <= end_dt:
				retvals = twoPlanetsDistance(planet1, planet2, dt, sidereal=sidereal)
				dist, aspect, p1_x, p2_x, p1_v, p2_v = retvals[:6]
				if dist < abs(p1_v)*n or dist < abs(p2_v)*n: #if planets could maybe perfect aspect within n days
					nextAspect = getNextAspect(planet1, planet2, dt, sidereal=sidereal)
					if nextAspect[0] < end_dt: #check if next aspect is actually within time window
						ASPECTS.append((*nextAspect, planet1, planet2))
						dt = nextAspect[0]+timedelta(days=1) #move forward 1 day - no two planets perfect another aspect in <1 day
					else:
						dt = end_dt+timedelta(hours=1) #if next aspect for these planets is outside window, exit while loop
				else: #step forward 1 day, keep checking for these 2 planets in case of significant speed changes in time window
					dt += timedelta(days=1)
	return sorted(ASPECTS)


def getNextIngress(planetName, start_dt, sidereal=True):
	"""
	Returns the datetime and sign index of next ingress of planetName into a different sign, starting from dt.

	"""
	p_i = PLANETKEY.index(planetName)
	dt = start_dt
	timedifftup = dt.timetuple()[:6] #year, month, day, hour, minute, second
	jt = swe.utc_to_jd(*timedifftup, swe.GREG_CAL) #convert to Julian time
	p_coord = swe.calc_ut(jt[1], p_i, flag=int(sidereal)*swe.FLG_SIDEREAL+swe.FLG_SPEED) #get location info for planet
	p_x = p_coord[0] #longitudinal location in degrees
	p_v = p_coord[3] #longitudinal speed in deg/day
	p_pos = swe.split_deg(p_x,8) #split location into degrees, min, sec, sign
	current_sign_i = p_pos[4] #index of current sign
	prev_sign_i = (current_sign_i - 1) % 12 #index of previous sign (possible for ingress)
	next_sign_i = (current_sign_i + 1) % 12 #index of next sign (more likely for ingress)
	sign_limits = (SIGNCUSPS[current_sign_i],SIGNCUSPS[current_sign_i]+30,0) #possible degrees that p can traverse to ingress; 360°=0°
	if p_v < 0:							#initialize dist based on best guess due to planetary position
		dist = sign_limits[0] - p_x 	#dist is the distance between planet and cusp of sign it will ingress into
	if p_v > 0:
		dist = sign_limits[1] - p_x
	# iters = 0 <--- used for debugging
	while round(dist, 3) != 0:
		if sign_limits[0] < p_x < sign_limits[1]: #if planet is within current sign, step forward in time
			delta_t = abs(min(abs(sign_limits[i] - p_x) for i in range(3))/p_v)
		else: #if planet has moved out of current sign, step backward in time to capture ingress
			delta_t = -abs(min(abs(sign_limits[i] - p_x) for i in range(3))/p_v)
		if abs(p_v) < 0.3: 				#if planet near station, p_v really small so delta_t needs to be reduced
			delta_t *= abs(p_v) * 3		#these values work well for Mercury through Saturn
		if dt + timedelta(days=delta_t) > start_dt:
			dt += timedelta(days=delta_t)	# move forward or backward in time a reasonable amount
		else:
			dt += timedelta(days=1)
		timedifftup = dt.timetuple()[:6] #year, month, day, hour, minute, second
		jt = swe.utc_to_jd(*timedifftup, swe.GREG_CAL) #convert to Julian time
		p_coord = swe.calc_ut(jt[1], p_i, flag=int(sidereal)*swe.FLG_SIDEREAL+swe.FLG_SPEED) #get location info for planet
		p_x = p_coord[0]
		p_v = p_coord[3]
		if p_v < 0:							#update dist based on updated understanding of planet's position
			dist = sign_limits[0] - p_x 	#if retrograde, planet will ingress into earlier sign
		if p_v > 0:
			dist = sign_limits[1] - p_x 	#if direct, planet will ingress into later sign
		# iters += 1
		# if iters >= 200: <--- this is helpful for debugging
		# 	print('Leaving loop for',planetName,'at pos',p_x,'dist',dist,'after 200 iterations')
		# 	break
	p_pos = swe.split_deg(round(p_x,2)%360,8) #once we've found ingress, round off position to get sign
	ingress_sign_i = p_pos[4] #get index of ingress sign
	if current_sign_i == ingress_sign_i: #if we're at 0° of the sign we started in, we're ingressing into the earlier sign
		ingress_sign_i = prev_sign_i
	return dt, ingress_sign_i


def printAllNextTransits(start_dt, n, sidereal=True):
	print('Transits for next',n,'days:')
	print()
	end_dt = start_dt+timedelta(days=n)
	aspectList = getAllNextAspects(start_dt, n, sidereal=sidereal)
	ingressList = []

	for idx, next_aspect in enumerate(aspectList):
		p1_pos, p2_pos = (swe.split_deg(next_aspect[i],8) for i in range(1,3)) #split p1_x and p2_x into SIGNKEY, degrees
		strfmt = ' '.join((next_aspect[4],'at',str(p1_pos[0])+'°',str(p1_pos[1])+"'"+str(p1_pos[2])+'"',SIGNKEY[p1_pos[4]],\
				ASPECTKEY[ASPECTS.index(next_aspect[3])],\
				next_aspect[5],'at',str(p2_pos[0])+'°',str(p2_pos[1])+"'"+str(p2_pos[2])+'"',SIGNKEY[p2_pos[4]]))
		aspectList[idx] = ((next_aspect[0],strfmt))

	for planetName in PLANETKEY:
		dt = start_dt
		while start_dt <= dt <= end_dt:
			new_dt, next_sign_i = getNextIngress(planetName, dt, sidereal=sidereal)
			strfmt = planetName+' ingresses '+SIGNKEY[next_sign_i]
			if new_dt < end_dt:
				ingressList.append((new_dt, strfmt))
			dt = new_dt + timedelta(hours=1)
	transits = sorted(aspectList + ingressList)
	for transit in transits:
		print((transit[0]+LOCALTIMEDIFF).strftime('%a %b %d %I:%M %p'),'-',transit[1])
		print()
	return


def printNextIngressAllPlanets(dt, sidereal=True):
	print('Next ingress for all planets from',(dt+LOCALTIMEDIFF).strftime('%a %b %d %Y %X'),'–')
	print()
	for planet in PLANETKEY:
		new_dt, next_sign_i = getNextIngress(planet, dt, sidereal=sidereal)
		print(planet,'ingresses',SIGNKEY[next_sign_i],'on',(new_dt+LOCALTIMEDIFF).strftime('%a %b %d, %Y at %I:%M %p'),'ET')
		print()


def printPlanetPositions(dt, orb, sidereal=True):
	dt_tup = dt.timetuple()[:6]
	jt = swe.utc_to_jd(*dt_tup,swe.GREG_CAL)
	planetpos = list(swe.calc_ut(jt[1], i, flag=int(sidereal)*swe.FLG_SIDEREAL+swe.FLG_SPEED) for i in range(len(PLANETKEY)))
	planetSigns = list(swe.split_deg(planetpos[i][0],8) for i in range(len(planetpos)))

	for i in range(len(PLANETKEY)):
		print(PLANETKEY[i]+':',str(planetSigns[i][0])+'°',str(planetSigns[i][1])+"'"+\
			str(planetSigns[i][2])+'"',SIGNKEY[planetSigns[i][4]],'   speed:',round(planetpos[i][3],3),'deg/day')

	perfectList = []
	print('\nAspects within '+str(orb)+'° orb:')
	for i, planet1 in enumerate(PLANETKEY[:-1]): #the last planet will never be 1st in the pair
		for planet2 in PLANETKEY[i+1:]: #to avoid duplicate checks, second planet is always later in list
			dist, aspect, p1_x, p2_x, p1_v, p2_v, perfecting = twoPlanetsDistance(planet1, planet2, dt, sidereal=sidereal)
			if round(dist, 2) <= orb:
				distfloor = int(dist)
				distsplit = (distfloor, int((dist-distfloor)*60))
				p1_pos, p2_pos = swe.split_deg(p1_x, 8), swe.split_deg(p2_x, 8)
				if perfecting:
					perfectstr = 'perfecting'
				else:
					perfectstr = 'separating'
				perfectList.append((dist,planet1+' at '+str(p1_pos[0])+'° '+str(p1_pos[1])+"'"+str(p1_pos[2])+'" '+SIGNKEY[p1_pos[4]]+' '+
					str(distsplit[0])+'° '+str(distsplit[1])+"'"+' from '+ASPECTKEY[ASPECTS.index(aspect)]+' '+
					planet2+' at '+str(p2_pos[0])+'° '+str(p2_pos[1])+"'"+str(p2_pos[2])+'" '+SIGNKEY[p2_pos[4]]+' ('+perfectstr+')'))
	perfectList.sort()
	for dist, printstr in perfectList:
		print(printstr)
	print()


def main(sidereal=True):

	if input("Enter 'Z' to switch to tropical zodiac: ").upper() == 'Z':
		sidereal = False

	now = datetime.utcnow()
	# nowtup = now.timetuple()[:6] # get year --> second values in a tuple

	print()
	print('Current time:',(now+LOCALTIMEDIFF).strftime('%a %b %d %Y %X'))
	print()
	printPlanetPositions(now, 3, sidereal=sidereal)
	# jt = swe.utc_to_jd(*nowtup,swe.GREG_CAL)
	# planetpos = list(swe.calc_ut(jt[1], i, flag=int(sidereal)*swe.FLG_SIDEREAL+swe.FLG_SPEED) for i in range(len(PLANETKEY)))
	# planetSigns = list(swe.split_deg(planetpos[i][0],8) for i in range(len(planetpos)))

	# for i in range(len(PLANETKEY)):
	# 	print(PLANETKEY[i]+':',str(planetSigns[i][0])+'°',str(planetSigns[i][1])+"'"+\
	# 		str(planetSigns[i][2])+'"',SIGNKEY[planetSigns[i][4]],'   speed:',round(planetpos[i][3],3),'deg/day')
	# print()

	print('Enter one of the following commands:')
	print('T            n -- see all transits for the next n days (n is an integer); if n not provided, defaults to 3')
	print('T mm/dd/yyyy n -- see all transits for the next n days from the specified date (12 a.m. local time)')
	print('I              -- see the next ingress for all planets from current date and time')
	print('I mm/dd/yyyy   -- see the next ingress for all planets from the specified date (12 a.m. local time)')
	print('D mm/dd/yyyy   -- see positions and speeds of all planets at the specified date (12 a.m. local time)')
	print('D              -- see positions and speeds of all planets now')
	print('Z              -- switch zodiacs')
	print('\nEnter Q to quit.')
	print()

	while True:
		valid = True
		ndays = 0
		usedate = 0
		now = datetime.utcnow()
		try:
			cmd, *flags = input('>>> ').split()
			if cmd.upper() == 'Q':
				break
		except ValueError:
			print('Try again.\n')
			continue
		try:
			cmd = cmd.upper()
			if cmd not in ('D','I','T','Z'):
				print('Try again.\n')
				continue
		except AttributeError:
			print('Try again.\n')
			continue
		if cmd == 'Z':
			sidereal = not sidereal
			if sidereal:
				print('Switched to sidereal zodiac.\n')
			else:
				print('Switched to tropical zodiac.\n')
		for i, flag in enumerate(flags):
			try:
				ndays = int(flag)
			except ValueError:
				try:
					usedate = datetime.strptime(flag,'%m/%d/%Y')
				except:
					valid = False
					print('Try again.\n')
					continue

		if valid:
			print()

			if ndays:
				n = ndays
			else:
				n = 3

			if not usedate:
				usedate = now
			else:
				usedate -= LOCALTIMEDIFF

			if cmd == 'T':
				printAllNextTransits(usedate, n, sidereal=sidereal)
				continue
			elif cmd == 'I':
				printNextIngressAllPlanets(usedate, sidereal=sidereal)
				continue
			elif cmd == 'D':
				print('\nPlanetary positions for:',(usedate+LOCALTIMEDIFF).strftime('%a %b %d %Y %X'),'\n')
				printPlanetPositions(usedate, 3, sidereal=sidereal)



if __name__ == "__main__":
	main()

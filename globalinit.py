import swisseph as swe
import time
from datetime import datetime, timedelta

swe.set_ephe_path('~/Projects/swe_unix_src_2.07.01') #set the filepath to your Swiss Ephemeris download
swe.set_sid_mode(swe.SIDM_LAHIRI) #uses Hindu-Lahiri ayanamsa for sidereal zodiac

SIGNKEY=('Aries', #0
		'Taurus', #1
		'Gemini', #2
		'Cancer', #3
		'Leo', #4
		'Virgo', #5
		'Libra', #6
		'Scorpio', #7
		'Sagittarius', #8
		'Capricorn', #9
		'Aquarius', #10
		'Pisces') #11

SIGNCUSPS=tuple(30*x for x in range(12)) #degree value of all sign cusps from 0° = 0° Aries to 330° = 0° Pisces

PLANETKEY=('Sun', #0
		'Moon', #1
		'Mercury', #2
		'Venus', #3
		'Mars', #4
		'Jupiter', #5
		'Saturn') #6

RULERS={'Aries': 'Mars', 'Taurus': 'Venus', 'Gemini': 'Mercury', 'Cancer': 'Moon', 'Leo': 'Sun', \
		'Virgo': 'Mercury', 'Libra': 'Venus', 'Scorpio': 'Mars', 'Sagittarius': 'Jupiter', \
		'Capricorn': 'Saturn', 'Aquarius': 'Saturn', 'Pisces': 'Jupiter'}

ASPECTS=(0,60,90,120,180)
ASPECTKEY=('CONJUNCT','sextile','SQUARE','trine','OPPOSITE')

ANGLEKEY = ('Ascendant','Midheaven','ARMC','vertex','equatorial ascendant',\
			'co-ascendant (Koch)','co-ascendant (Munkasey)','polar ascendant (Munkasey)')
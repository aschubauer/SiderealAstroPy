# SiderealAstroPy
Astrology calculations that use either the tropical or sidereal (Hindu-Lahiri ayanamsa) zodiac. Written in Python 3.

Uses the pyswisseph library. You will need to download the Swiss Ephemeris files in addition to installing pyswisseph.

When run, transits.py provides a simple command-line interface through which to interact with its functions.

To run the zodiacal releasing calculator as an executable without installing Python or pyswisseph, download the .zip file, navigate to dist/zrcsv, and run zodiacal-releasing-calculator. The calculator saves .csv files of zodiacal releasing periods (over a 100-year lifetime) in a folder called Zodiacal Releasing in your home directory. You will need to enter the chart owner's birth time in Universal Time and the latitude and longitude of their birth place.

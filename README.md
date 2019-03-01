# SiderealAstroPy
Astrology functions made to use either the tropical or sidereal zodiac. Written in Python 3.

Uses the pyswisseph library. You will need to both download the Swiss Ephemeris files and install pyswisseph. I recommend using pipenv for dependency management along with a virtual environment.

When run, transits.py provides a simple command-line interface through which to interact with its functions.

To run ZRCSV as an executable without installing Python or pyswisseph, download the dist/zrcsv directory and run the zrcsv file. This provides a command-line interface for generating zodiacal releasing periods over a 100-year lifetime as a .csv file. You will need to enter the chart owner's birth time in Universal Time and the latitude and longitude of their birth place.

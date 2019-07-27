# SiderealAstroPy
Astrology calculations that use either the tropical or sidereal (Hindu-Lahiri ayanamsa) zodiac. Written in Python 3.

Installation instructions:
1. Read the Swiss Ephemeris license information: https://www.astro.com/swisseph/swephinfo_e.htm
2. Download the latest Swiss Ephemeris source package: https://www.astro.com/ftp/swisseph/
3. Install pyswisseph via pip or pipenv.
4. Create a file called my_ephe_path.py in your SiderealAstroPy directory to define the following variable:
    ```
    EPHE_PATH = 'filepath/of/your/SwissEphemeris/src'
    ```

When run, transits.py provides a command-line interface through which to interact with its functions.

To run the zodiacal releasing calculator as an executable without installing Python or pyswisseph, download zrcsv.zip, open the folder, and run zodiacal-releasing-calculator. The calculator saves .csv files of zodiacal releasing periods (over a 100-year lifetime) in a folder called Zodiacal Releasing in your home directory. You will need to enter the chart owner's birth time in Universal Time and the latitude and longitude of their birth place.

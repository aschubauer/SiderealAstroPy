# SiderealAstroPy
Astrology calculations that use either the tropical or sidereal (Hindu-Lahiri ayanamsa) zodiac. Written in Python 3.

Installation instructions:
1. Read the Swiss Ephemeris license information: https://www.astro.com/swisseph/swephinfo_e.htm
2. Download the latest Swiss Ephemeris source package: https://www.astro.com/ftp/swisseph/
3. If using pip, install ```pyswisseph==2.00.00-2```. To keep your pyswisseph installation separate for this project, install <a href="https://pipenv.pypa.io/en/latest/basics/#">Pipenv</a> and run ```pipenv install``` inside this project directory.
<br /><i>This project is not yet compatible with pyswisseph version 2.08.00 and above.</i>
4. Create a file called my_ephe_path.py in your SiderealAstroPy directory to define the following variable:
    ```
    EPHE_PATH = 'filepath/of/your/SwissEphemeris/src'
    ```

When run, transits.py provides a command-line interface through which to interact with its functions.

To run the zodiacal releasing calculator as an executable without installing Python or pyswisseph, download zrcsv.zip, open the folder, and run zodiacal-releasing-calculator. The calculator saves .csv files of zodiacal releasing periods (over a 100-year lifetime) in a folder called Zodiacal Releasing in your home directory. You will need to enter the chart owner's birth time in Universal Time and the latitude and longitude of their birth place.

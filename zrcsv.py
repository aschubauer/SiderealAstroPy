import csv, datetime

from birthchart import Birthchart


name = input("Chart owner's name: ")
while True:
    byear = input("Birth year (UT): ")
    bmonth = input("Birth month (UT): ")
    bday = input("Birth day (UT): ")
    bhr = input("Birth hour (UT): ")
    bmin = input("Birth minute (UT): ")
    try:
        bdate = datetime.datetime(int(byear),int(bmonth),int(bday),int(bhr),int(bmin),0)
        break
    except:
        print("Invalid input. Please try again.")
        continue
lat = int(input("Latitude of birth location: "))
lng = int(input("Longitude of birth location: "))
sid = input("Sidereal? (y/n): ") == "y"
print()

native = Birthchart(name, bdate, lat, lng, sidereal=sid)
native.calculateLots()
print("Lots calculated:")
for key in native.lots.keys():
    print(key)
print()
lot = input("Lot to release from: ")
while True:
    try:
        native.calculateZR(lot)
        break
    except:
        print("Not a valid lot. \n")
        lot = input("Lot to release from: ")
        continue

savefile = name+"_"+lot
if sid:
    savefile += "_sid"
savefile += ".csv"
with open(savefile, 'w', newline='') as csvfile:
    fieldnames = ['Level','Start Date','Sign']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for level in native.ZR[lot]:
        writer.writerows([{'Level': level, 'Start Date': dt, 'Sign': sign} for dt, sign in native.ZR[lot][level]])

print("File created successfully: "+savefile)
# coding: utf-8
import os, csv, datetime, pickle

from birthchart import Birthchart

OUTPUT_DIR = "Zodiacal Releasing/"
SAVED_FILEPATH = OUTPUT_DIR+"zr-profiles.pck"

def getSavedProfiles():
    try:
        with open(SAVED_FILEPATH, 'rb') as pckfile:
            return pickle.load(pckfile)
    except FileNotFoundError:
        return []

def saveProfilesBeforeClosing(list_of_birthcharts):
    with open(SAVED_FILEPATH, 'wb') as pckfile:
        pickle.dump(list_of_birthcharts, pckfile, pickle.HIGHEST_PROTOCOL)

def loadChart(native: Birthchart, sid: bool):
    if sid != native.sid:
        native = Birthchart(native.name, native.birthTime, native.lat, native.lng, sidereal=sid)

    print(native.name,"has a",native.sect.lower(),"chart.")
    print()
    native.calculateLots()
    print("Lots calculated:")
    for lot in native.lots.keys():
        print(lot + ' - ' + str(native.lots[lot]['deg']) + '° ' + str(native.lots[lot]['min']) + "' " + str(native.lots[lot]['sign']))
    print()
    print("Commands:\nS - switch profiles\nD - delete this profile\nQ - quit")
    print()

    while True:
        while True:
            lot_input = input("Lot to release from: ")
            if lot_input.lower() == 'q':
                return 'exit'
            if lot_input.lower() == 'd':
                print('Profile for',native.name,'deleted.')
                print()
                return 'delete'
            if lot_input.lower() == 's':
                return None
            lot = [lot for lot in native.lots.keys() if lot.lower() == lot_input.lower()]
            if lot:
                lot = lot[0]
                native.calculateZR(lot)
            else:
                print("Not a valid lot.")
                lot = input("Lot to release from: ")
                continue

            if not os.path.exists(OUTPUT_DIR):
                os.makedirs(OUTPUT_DIR)
            savefile = OUTPUT_DIR+native.name+"_"+lot
            if sid:
                savefile += "_sid"
            savefile += ".csv"
            with open(savefile, 'w', newline='') as csvfile:
                headers = ['Level','Start Date','Sign','Note']
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                for level in native.ZR[lot]:
                    writer.writerows([{'Level': level, 'Start Date': dt, 'Sign': sign, 'Note': note} for dt, sign, note in native.ZR[lot][level]])
            print("File created: "+savefile)

def getSid():
    while True:
        sid_input = input("Sidereal? (Y/N): ")[0].lower()
        if sid_input not in ("y","n"):
            continue
        else:
            sid = sid_input == "y"
            break
    return sid

def enterNewChart():
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
        except ValueError:
            print("Please enter a valid date.")
            continue

    while True:
        try:
            lat = float(input("Latitude of birth location: "))
            lng = float(input("Longitude of birth location: "))
            break
        except ValueError:
            print("Please enter a valid decimal value.")
            continue
    sid = getSid()

    while True:
        save_input = input("Save birth data for " + name + "? (Y/N): ")[0].lower()
        if save_input not in ("y","n"):
            continue
        else:
            save = save_input == "y"
            break
    print()

    return Birthchart(name, bdate, lat, lng, sidereal=sid), sid, save

def main():
    profiles = getSavedProfiles()
    save = False

    while True:
        if profiles:
            tab = '\t'
            print('Saved profiles:')
            print('ID','Name','Time (UT)','Latitude','Longitude', sep=tab+tab)
            for i, p in enumerate(profiles):
                print(i+1, p.name, p.birthTime.isoformat(sep=' ',timespec='minutes')+tab+str(p.lat), p.lng, sep=tab+tab)
            print()
            while True:
                id_input = input("Enter an ID or Name to use an existing profile, or N to create a new profile: ")
                if id_input.lower() == 'n':
                    native, sid, save = enterNewChart()
                    if save:
                        profiles.append(native)
                    break
                else:
                    profile = [p for p in profiles if p.name.lower() == id_input.lower() or str(profiles.index(p)+1) == id_input]
                    if not profile:
                        continue
                    else:
                        native = profile[0]
                        sid = getSid()
                        break

        else:
            profiles = []
            native, sid, save = enterNewChart()
            if save:
                profiles.append(native)

        print()
        exit = loadChart(native, sid)
        if exit == 'exit':
            break
        elif exit == 'delete':
            profiles.remove(native)
            save = True
        
    if save:
        saveProfilesBeforeClosing(profiles)


if __name__ == "__main__":
    main()
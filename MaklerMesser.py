# Why are only some values in string concatenation explicitly converted to a str() in this program?
# Using '+' instead of ',' to concatenate strings makes Python add the values together,
# which doesn't work for strings and ints for example. Reduces readability, of course. #TypeError

import sys;

# This class is pretty much obsolete after adding TeilFläche and will be removed
class Raum:
    def __init__(self, raumZahl: int):
        self.raumZahl = raumZahl; # Same value as TeilFläche.raumNummer

# TeilFläche.teilFläche automatically calculates itself and can be refreshed with refreshKeys(iterable, key: str, refresherKey: str, updaterKey: str);
class TeilFläche:
    teilFlächenNummer: int = 0;
    raumNummerKomparator: int = 1;

    def __init__(self, raumNummer: int, teilFlächenLänge: float, teilFlächenBreite: float):
        self.__class__.teilFlächenNummer += 1;
        if raumNummer > self.__class__.raumNummerKomparator:
            self.__class__.teilFlächenNummer = 1;

        self.raumNummer = raumNummer;
        self.teilFlächenNummer = self.__class__.teilFlächenNummer;
        self.teilFlächenLänge = teilFlächenLänge;
        self.teilFlächenBreite = teilFlächenBreite;
        self.teilFläche = teilFlächenLänge * teilFlächenBreite;

        self.__class__.raumNummerKomparator = raumNummer;
    def __str__(self):
        return str(("Raum:", self.raumNummer, "Teilfläche:", self.teilFlächenNummer, "Fläche der Teilfläche:", self.teilFläche, "Länge:", self.teilFlächenLänge, "Breite:", self.teilFlächenBreite));

zustimmungsArgumente = ["ja", "j", "yes", "y", "1", ""];

# Only used in dbg(), may be removed later; IGNORE
dbgRaumListe=[Raum(1), Raum(2), Raum(3)];

# Only used in dbg(), may be removed later; IGNORE
dbgTeilFlächenListe=[
                TeilFläche(1, 1, 1),                 # [0] Room 1, Area 1
                TeilFläche(1, 2, 2),                 # [1] Room 1, Area 2
                TeilFläche(2, 3, 3),                 # [2] Room 2, Area 1
                TeilFläche(2, 4, 4),                 # [3] Room 2, Area 2
                TeilFläche(2, 5, 5),                 # [4] Room 2, Area 3
                TeilFläche(3, 6, 6),                 # [5] Room 3, Area 1
                TeilFläche(3, 7, 7),                 # [6] Room 3, Area 2
                TeilFläche(3, 8, 8)                  # [7] Room 3, Area 3
                ];

def clearScr() -> None:
    import os
    os.system("cls||clear"); # Simplistic method to clear the console, if cls doesn't work run clear, and vice versa.

# This function returns the index of the first occurrence of a key with specific value in an array of objects
# 
# array[];
# i = 1; j = 0;
#
# for i < 10:
#     array[j] = Object(a: i, b: i, c: i, d: i, e: i, f: i);
#     i *= 2; j += 1;
#
# getStartIndex(array, "a", 8);
#
# The index will be 3, in this case as the third Object in this array will have the values
# array[1] = Object(a: 4, b: 4, c: 4, d: 4, e: 4, f: 4);
# array[2] = Object(a: 8, b: 8, c: 8, d: 8, e: 8, f: 8); <---
#
# Returns 0 if empty, index starts at 0.
def getStartIndex(iterable: list, key: str, value: any) -> int:
    for item in iterable:
        if getattr(item, key) == value:
            return iterable.index(item);
    return 0;

# Returns the amount of keys with a specific value in an array of objects.
# Returns 0 if empty, index starts at 0.
def getCount(iterable: list, key: str, value: any) -> int:
    count = 0;
    for item in iterable:
        if getattr(item, key) == value:
            count += 1;
    return count;

# Returns the amount of individually keyed objects
# Meaning if a list is 1, 2, 3, 3, 4, 4, 5, it'll return 5, for example
def getIndividualCount(iterable: list, key: str) -> int:
    individualKeys: list = [];
    for item in iterable:
        if getattr(item, key) in individualKeys:
            continue;
        individualKeys.append(getattr(item, key));
    return len(individualKeys);

# This is a bad name as the function only multiplies two keys to set a third.
# This function is only used to recalculate TeilFläche.teilFläche after creation.
def refreshKeys(iterable: list, key: str, refresherKey: str, updaterKey: str) -> list:
    for item in iterable:
        setattr(item, key, getattr(item, refresherKey) * getattr(item, updaterKey))
    return iterable;

# This function would be used to update room designations after a rooms values have been deleted
# TODO: get index missing value and only decrease above rooms designations
def updateRoomDesignations(iterable: list) -> list:
    for item in iterable:
        setattr(item, "raumZahl", getattr(item, "raumZahl") - 1);
    return iterable;

# Safely gets input of any type
# getInput("Enter your age", int); would try for int(response)
# getInput("Enter your age", str); would try for str(response)
def getInput(prompt: str, dataType: any, clear: bool = True) -> any:
    while True:
        if clear:
            clearScr();
        response = input(prompt);
        try:
            return dataType(response);  # This equates to int(response) if dataType transferred is int. This works with all types theoretically.
        except ValueError:
            match dataType.__name__: # Implement valid descriptions for different types, or don't, the default case _: handles every unimplemented case
                case "float":
                    print("Bitte geben Sie eine valide Zahl ein.");
                case "str":
                    print("Bitte geben Sie valide Symbole ein.");
                case _:
                    print("Bitte versuchen Sie es erneut.");

# Arguments starting at listOnly can be supplied to test different zones in this function
# e.g. leaving zimmerWahl None, but setting teilFlächenWahl, would let you enter a zimmerWahl and skip the prompt for teilFlächenWahl
# Use explicitly named arguments for easier usage
def numberEditor(raumListe: list, teilFlächenListe: list, listOnly: bool = False, zimmerWahl = None, teilFlächenWahl = None, wertWahl = None, neueLänge = None, neueBreite = None) -> tuple:
    for Zimmer in raumListe:
        raumFläche = 0;
        for TeilFläche in teilFlächenListe:
            if TeilFläche.raumNummer == Zimmer.raumZahl:
                raumFläche += TeilFläche.teilFläche;
        print(
              "Zimmer: [" + str(Zimmer.raumZahl) + "]",
              str(raumFläche) + "m²"
              );
    if listOnly:
        input();
        return;

    zimmerWahl = zimmerWahl or getInput("Welches Zimmer wollen Sie bearbeiten?: ", int, False);

    j = 0;
    startingPoint = getStartIndex(teilFlächenListe, "raumNummer", zimmerWahl);
    for TeilFläche in teilFlächenListe:
        if TeilFläche.raumNummer == zimmerWahl:
            j += 1;
            print(
                "Teilfläche [" + str(j) + "] Länge:",
                str(TeilFläche.teilFlächenLänge),
                "Breite:",
                str(TeilFläche.teilFlächenBreite)
                );
    
    while True:
        teilFlächenAuswahl = teilFlächenWahl or getInput("Welche dieser Teilflächen wollen Sie bearbeiten?: ", int, False);
        teilFlächenWahl = teilFlächenAuswahl + startingPoint - 1;
        if teilFlächenWahl >= j + startingPoint or teilFlächenWahl < startingPoint:
            print("Teilfläche ist nicht in Liste.");
            teilFlächenWahl = None;
            continue;
        else:
            break;

    print("Raum", zimmerWahl, "Teilfläche", str(teilFlächenAuswahl),
          "[" + str(teilFlächenWahl + 1) + "|" + str(len(teilFlächenListe)) + "]",
          "[L]änge:", str(teilFlächenListe[teilFlächenWahl].teilFlächenLänge), "[B]reite:", str(teilFlächenListe[teilFlächenWahl].teilFlächenBreite));

    while True:
        wertWahl = wertWahl or getInput("Welchen dieser Werte wollen Sie bearbeiten? [l|b|(d zum Löschen des Eintrags)]: ", str, False).lower();
        match wertWahl:
            case "l":
                neueLänge = neueLänge or getInput("Welche Länge wollen Sie statt " + str(teilFlächenListe[teilFlächenWahl].teilFlächenLänge) + " eintragen?: ", float, False);
                teilFlächenListe[teilFlächenWahl].teilFlächenLänge = neueLänge;
                break;
            case "b":
                neueBreite = neueBreite or getInput("Welchen Breite wollen Sie statt " + str(teilFlächenListe[teilFlächenWahl].teilFlächenBreite) + " eintragen?: ", float, False);
                teilFlächenListe[teilFlächenWahl].teilFlächenBreite = neueBreite;
                break;
            case "d":
                teilFlächenListe.pop(teilFlächenWahl);
                if getCount(teilFlächenListe, "raumNummer", zimmerWahl) == 0:
                    raumListe.pop(zimmerWahl - 1);
                break;
            case "n":
                break;
            case _:
                print("Bitte geben Sie eine der angegebenen Optionen (l|b|d) ein");
                continue;
    
    return (raumListe, teilFlächenListe);

def getRaum(raumListe: list = [], teilFlächenListe: list = []) -> tuple:
    raumAnzahl = 0;

    while True:
        raumAnzahl += 1;
        raumLänge = raumBreite = raumFläche = 0;

        while True:
            raumLänge = getInput("Geben Sie die Länge des Raumes oder der Teilfläche in m² ein: ", float);
            raumBreite = getInput("Geben Sie die Breite des Raumes oder der Teilfläche in m² ein: ", float);
            raumFläche += raumLänge * raumBreite;

            teilFlächenVorhanden = getInput("Sind weitere Teilflächen vorhanden? [J/n]: ", str).lower();
            if teilFlächenVorhanden in zustimmungsArgumente:
                teilFlächenListe.append(TeilFläche(raumAnzahl, raumLänge, raumBreite));
                continue;
            else:
                break;
        teilFlächenListe.append(TeilFläche(raumAnzahl, raumLänge, raumBreite));
        raumListe.append(Raum(raumAnzahl));

        mehrRäume = getInput("Sind weitere Räume vorhanden? [J/n]: ", str).lower();
        if mehrRäume in zustimmungsArgumente:
            continue;
        else:
            break;
    return (raumListe, teilFlächenListe);

def calculateResult(teilFlächenListe: list = []) -> list:
    gebäudeFläche = 0;
    teilFlächenListe = refreshKeys(teilFlächenListe, "teilFläche", "teilFlächenLänge", "teilFlächenBreite");
    anzahlRäume = getIndividualCount(teilFlächenListe, "raumNummer");
    for i in range(1, anzahlRäume + 1):
        raumFläche = 0;
        for teilFläche in teilFlächenListe:
            if teilFläche.raumNummer == i:
                raumFläche += teilFläche.teilFläche;
        print("Die Fläche für Raum", i, "beträgt:", str(raumFläche) + "m²");
        gebäudeFläche += raumFläche;
    print("Die gesamte Fläche des Gebäudes beträgt:", str(gebäudeFläche) + "m²");
    print("Die durchschnittliche Fläche eines Raumes beträgt:", str(gebäudeFläche / (anzahlRäume if anzahlRäume > 0 else 1)) + "m²");
    return (teilFlächenListe);

def dbg(dbgListOnly = False, dbgZimmerWahl = None, dbgTeilFlächenWahl = None, dbgWertWahl = None, dbgNeueLänge = None, dbgNeueBreite = None) -> tuple:
    clearScr();
    (raumListe, teilFlächenListe) = numberEditor(
        raumListe=dbgRaumListe,                         # Predefined at top, CTRL+Click to find.
        teilFlächenListe=dbgTeilFlächenListe,           # Predefined at top, CTRL+Click to find.
        listOnly=dbgListOnly,
        zimmerWahl=dbgZimmerWahl,
        teilFlächenWahl=dbgTeilFlächenWahl,
        wertWahl=dbgWertWahl,
        neueLänge=dbgNeueLänge,
        neueBreite=dbgNeueBreite
        );

    teilFlächenListe = calculateResult(teilFlächenListe);
    exit(0);

def main() -> int:
    if (len(sys.argv) > 1):
        match sys.argv[1]:
            case "-dO": dbg(dbgListOnly=False, dbgZimmerWahl=2, dbgTeilFlächenWahl=1, dbgWertWahl="b", dbgNeueLänge=4, dbgNeueBreite=5);  # Use py/python/python3 MaklerMesser.py -dO to run a test run with the following predefined settings
            case "-dTFL":
                for item in dbgTeilFlächenListe:
                    print(item); # Use py/python/python3 MaklerMesser.py -dTFL to print the insides of dbgTeilFlächenListe
                return 0;
            case "-dGIC":
                print("Filled list:", getIndividualCount(dbgTeilFlächenListe, "raumNummer"));
                print("Empty list:", getIndividualCount([], ""));
                return 0;
            case _: dbg();  # Use py/python/python3 MaklerMesser.py with any other argument to run a test run with predefined arrays but no options

    (raumListe, teilFlächenListe) = getRaum();
    
    while True:
        clearScr();
        teilFlächenListe = refreshKeys(teilFlächenListe, "teilFläche", "teilFlächenLänge", "teilFlächenBreite");
        zahlenEditor = getInput("Wollen Sie die Eingaben anpassen? [J/n/(a zum Ansehen)]: ", str);
        if zahlenEditor in zustimmungsArgumente:
            (raumListe, teilFlächenListe) = numberEditor(raumListe, teilFlächenListe);
        elif zahlenEditor == "a":
            numberEditor(raumListe, teilFlächenListe, True);
        else:
            break;

    teilFlächenListe = calculateResult(teilFlächenListe);
    return 0;

if __name__ == "__main__":
    main();
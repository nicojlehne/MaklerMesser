# Why are only some values in string concatenation explicitly converted to a str() in this program?
# Using '+' instead of ',' to concatenate strings makes Python add the values together,
# which doesn't work for strings and ints for example. Reduces readability, of course. #TypeError

import time, math, pathlib

def isLinux():
    from sys import platform
    if platform == "linux" or platform == "linux2" or platform == "cygwin":
        return 1;
    elif platform == "win32":
        return 0;
    else:
        return 666;

isLinux: int = int(isLinux())
if isLinux:
    from getch import getch # getch module has to be installed manually with pip (ONLY: Linux)
else:
    import msvcrt # Windows supporting implementation of getch

# TeilFläche.teilFläche automatically calculates itself on entry and can be refreshed with refreshArea(iterable, key: str, refresherKey: str, updaterKey: str);
class TeilFläche:
    teilFlächenNummer: int = 0;
    gebäudeNummerKomparator: int = 1;
    raumNummerKomparator: int = 1;
    raumName: str = None;
    gebäudeName: str = None;

    def __init__(self, gebäudeNummer: int, raumNummer: int):
        self.__class__.teilFlächenNummer += 1;
        if raumNummer > self.__class__.raumNummerKomparator:
            self.__class__.teilFlächenNummer = 1;
            self.__class__.raumName = None;
        if gebäudeNummer > self.__class__.gebäudeNummerKomparator:
            self.__class__.raumNummerKomparator = 1;
            self.__class__.teilFlächenNummer = 1;
            self.__class__.gebäudeName = None;

        self.gebäudeNummer: int = gebäudeNummer;
        self.gebäudeName: str = self.__class__.gebäudeName if self.gebäudeName else getInput("Geben Sie den Namen des Gebäudes ein: ", str);
        self.raumNummer: int = raumNummer;
        self.raumName: str = self.__class__.raumName if self.__class__.raumName else getInput("Geben Sie den Namen des Raumes ein: ", str);
        self.teilFlächenNummer: int = self.__class__.teilFlächenNummer;
        self.teilFlächenLänge: float = getInput("Geben Sie die Länge des Raumes oder der Teilfläche in m² ein: ", float);
        self.teilFlächenBreite: float = getInput("Geben Sie die Breite des Raumes oder der Teilfläche in m² ein: ", float);
        self.teilFläche: float = self.teilFlächenLänge * self.teilFlächenBreite;

        self.__class__.gebäudeName = self.gebäudeName;
        self.__class__.gebäudeNummerKomparator = gebäudeNummer;
        self.__class__.raumName = self.raumName;
        self.__class__.raumNummerKomparator = raumNummer;
    def __str__(self): # This affects how the object looks when using print() for example
        return str(("Gebäude: ", self.gebäudeNummer, self.gebäudename, "Raum:", self.raumNummer, self.raumName, "Teilfläche:", self.teilFlächenNummer, "Fläche der Teilfläche:", self.teilFläche, "Länge:", self.teilFlächenLänge, "Breite:", self.teilFlächenBreite));

class ANSIString:
    def __init__(self, text, foregroundColor = None, backgroundColor = None, mode = None):
        self.text = text;
        self.foregroundColor = foregroundColor;
        self.backgroundColor = backgroundColor;
        self.mode =  mode;
    def __str__(self):
        ansiSequence = f"\033[{str(self.foregroundColor)}";
        if self.backgroundColor:
            ansiSequence += f";{self.backgroundColor}";
        if self.mode:
            ansiSequence += f";{self.mode}";
        ansiSequence += "m";
        return f"{ansiSequence}{self.text}\033[0m"

zustimmungsArgumente = ["ja", "j", "yes", "y", "1", ""]; # makes it easier to check input against confirmation

def clearScr() -> None:
    import os
    os.system("cls||clear"); # Simplistic method to clear the console, if cls doesn't work run clear, and vice versa.

# This function returns the index of the first occurrence of a key with specific value in an array of objects.
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

# Returns the amount of individually keyed objects
# Meaning if a list is 1, 2, 3, 3, 4, 4, 5, it'll return 5, for example
def getIndividualCount(iterable: list, key: str) -> int:
    individualKeys: list = [];
    for item in iterable:
        if getattr(item, key) in individualKeys:
            continue;
        individualKeys.append(getattr(item, key));
    return len(individualKeys);

# This function is only used to recalculate TeilFläche.teilFläche after creation.
def refreshArea(iterable: list, areaKey: str, multiplikand: str, multiplikator: str) -> list:
    for item in iterable:
        setattr(item, areaKey, getattr(item, multiplikand) * getattr(item, multiplikator))
    return iterable;

# This function would be used to update room designations after a rooms values have been deleted
def updateRoomDesignations(iterable: list, deletedRoom: int) -> list:
    for item in iterable:
        if getattr(item, "raumNummer") == deletedRoom:    # Check if room actually missing and immediately return if that's the case
            return iterable;
    for item in iterable:
        if getattr(item, "raumNummer") > deletedRoom:
            setattr(item, "raumNummer", getattr(item, "raumNummer") - 1);
    return iterable;

def nuGetch(prompt):
    if prompt:
        print(prompt);
    match isLinux:
        case 1:
            return getch();
        case 0:
            return msvcrt.getch();
        case _:
            raise TypeError("Unsupported OS", isLinux);

# Safely gets input of any type
# getInput("Enter your age", int); would try for int(response)
# getInput("Enter your age", str); would try for str(response)
def getInput(prompt: str, dataType: any, getch = False, clear: bool = True) -> any:
    while True:
        if clear:
            clearScr();
        if getch:
            response = nuGetch(prompt);
        else:
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
            clear = False;

# Arguments starting at listOnly can be supplied to test different zones in this function
# e.g. leaving zimmerWahl None, but setting teilFlächenWahl, would let you enter a zimmerWahl and skip the prompt for teilFlächenWahl
# Use explicitly named arguments for easier usage
def numberEditor(teilFlächenListe: list, listOnly: bool = False, zimmerWahl = None, teilFlächenWahl = None, wertWahl = None, neueLänge = None, neueBreite = None) -> list:
    anzahlRäume: int = getIndividualCount(teilFlächenListe, key="raumNummer");
    for i in range(1, anzahlRäume + 1):
        raumFläche: float = 0;
        for TeilFläche in teilFlächenListe:
            if TeilFläche.raumNummer == i:
                raumFläche += TeilFläche.teilFläche;
        print("Zimmer: [" + str(i) + "]",
              str(raumFläche) + "m²");
    if listOnly:
        input();
        return;

    zimmerWahl: int = zimmerWahl or getInput("Welches Zimmer wollen Sie bearbeiten?: ", int, clear=False);

    j: int = 0;
    startingPoint: int = getStartIndex(teilFlächenListe, key="raumNummer", value=zimmerWahl);
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
        teilFlächenAuswahl: int = teilFlächenWahl or getInput("Welche dieser Teilflächen wollen Sie bearbeiten?: ", int, clear=False);
        teilFlächenWahl: int = teilFlächenAuswahl + startingPoint - 1;
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
        match wertWahl or getInput("Welchen dieser Werte wollen Sie bearbeiten? [l|b|(d zum Löschen des Eintrags)]: ", str, getch=True, clear=False).lower():
            case "l":
                teilFlächenListe[teilFlächenWahl].teilFlächenLänge = neueLänge or getInput("Welche Länge wollen Sie statt " + str(teilFlächenListe[teilFlächenWahl].teilFlächenLänge) + " eintragen?: ", float, clear=False);
                break;
            case "b":
                teilFlächenListe[teilFlächenWahl].teilFlächenBreite = neueBreite or getInput("Welchen Breite wollen Sie statt " + str(teilFlächenListe[teilFlächenWahl].teilFlächenBreite) + " eintragen?: ", float, clear=False);
                break;
            case "d":
                teilFlächenListe.pop(teilFlächenWahl);
                updateRoomDesignations(teilFlächenListe, deletedRoom=zimmerWahl); # This does nothing if all rooms still have at least one partial area
                break;
            case "n":
                break;
            case _:
                print("Bitte geben Sie eine der angegebenen Optionen (l|b|d) ein");
                continue;
    return teilFlächenListe;

def getTeilFläche(teilFlächenListe: list = []) -> list:
    raumAnzahl: int = 0;
    gebäudeAnzahl: int = 0;
    while True:
        gebäudeAnzahl += 1;
        while True:
            raumAnzahl += 1;
            while True:
                teilFlächenListe.append(TeilFläche(gebäudeAnzahl, raumAnzahl));
                if getInput("Sind weitere Teilflächen vorhanden? [J/N]: ", str, getch=True).lower() in zustimmungsArgumente:
                    continue;
                else:
                    break;
            if getInput("Sind weitere Räume vorhanden? [J/N]: ", str, getch=True).lower() in zustimmungsArgumente:
                continue;
            else:
                break;
        if getInput("Sind weitere Gebäude vorhanden? [J/N]: ", str, getch=True).lower() in zustimmungsArgumente:
            continue;
        else:
            break;
    return teilFlächenListe;

def calculateResult(teilFlächenListe: list = []) -> list:
    gebäudeFläche: float = 0;
    teilFlächenListe = refreshArea(teilFlächenListe, areaKey="teilFläche", multiplikand="teilFlächenLänge", multiplikator="teilFlächenBreite");
    anzahlRäume: int = getIndividualCount(teilFlächenListe, key="raumNummer");
    for i in range(1, anzahlRäume + 1):
        raumFläche: float = 0;
        for teilFläche in teilFlächenListe:
            if teilFläche.raumNummer == i:
                raumFläche += teilFläche.teilFläche;
        print("Die Fläche für Raum " + str(teilFlächenListe[i].raumName) + "(" + str(i) + ")", "beträgt:", str(raumFläche) + "m²", str(teilFlächenListe[i].gebäudeName));
        gebäudeFläche += raumFläche;
    print("Die gesamte Fläche des Gebäudes beträgt:", str(gebäudeFläche) + "m²");
    print("Die durchschnittliche Fläche eines Raumes beträgt:", str(gebäudeFläche / (anzahlRäume if anzahlRäume > 0 else 1)) + "m²"); # Don't get confused, this just gets rid of div/0
    return teilFlächenListe;

def saveAs(teilFlächenListe: list = [], fileType: str = "csv") -> None:
    if len(teilFlächenListe) <= 0:
        print("Couldn't save succesfully, please try again.");
        return
    outputFile = open("teilFlaechenListe_" + str(math.ceil(time.time())) + "." + fileType, "a");
    listKeys = teilFlächenListe[0].__dict__.keys();
    for key in listKeys:
        outputFile.write(key + ";");
    outputFile.write("\n");
    for teilFläche in teilFlächenListe:
        for key in listKeys:
            outputFile.write(str(getattr(teilFläche, key)) + ";");
        outputFile.write("\n");
    print("Gespeichert in: " + outputFile.name);

def importFile(file) -> list:
    outputFile = open(file, "r");

def listDirectory(path = ".") -> list:
    return pathlib.Path(path).glob("*");

def walkDirectory(files = [], mode = "r"):
    fileChosen = None;
    selectedLine = 0;
    while not fileChosen:
        clearScr();
        key = None;
        files = listDirectory();
        for index, file in enumerate(files):
            if index == selectedLine:
                print(f"{ANSIString(file, 30, 47)}");
            else:
                print(file);
        files = listDirectory();
        while key == None:
            key = ord(nuGetch());
            if key == 224:
                key = ord(nuGetch());
                match key:
                    case 65:
                        selectedLine -= 1;
                        break;
                    case 66:
                        selectedLine += 1;
                        break;
                    case 72:
                        selectedLine -= 1;
                        break;
                    case 80:
                        selectedLine += 1;
                        break;
                    case _:
                        break;
            elif key == 27:
                key = ord(nuGetch());
                if key == 91:
                    key = ord(nuGetch());
                    match key:
                        case 65:
                            if selectedLine - 1 < 0:
                                break;
                            selectedLine -= 1;
                            break;
                        case 66:
                            if selectedLine + 1 > index:
                                break;
                            selectedLine += 1;
                            break;                    
                break;
            elif key == 10:
                return open(list(files)[selectedLine], mode);
            else:
                key = None;
                break;

def main() -> int:
    teilFlächenListe: list = getTeilFläche();
    
    while True:
        teilFlächenListe = refreshArea(teilFlächenListe, "teilFläche", "teilFlächenLänge", "teilFlächenBreite");
        zahlenEditor: str = getInput("Wollen Sie die Eingaben anpassen? [J|n|(a zum Ansehen)]: ", str, getch=True);
        if zahlenEditor in zustimmungsArgumente:
            teilFlächenListe = numberEditor(teilFlächenListe);
        elif zahlenEditor == "a":
            numberEditor(teilFlächenListe, listOnly=True);
        else:
            break;

    teilFlächenListe = calculateResult(teilFlächenListe);
    if getInput("Wollen Sie das Ergebnis als CSV-Datei speichern? (J|n): ", str, getch=True, clear=False) in zustimmungsArgumente:
        saveAs(teilFlächenListe=teilFlächenListe, fileType="csv");
    return 0;

if __name__ == "__main__":
    main();
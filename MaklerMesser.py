# Why are only some values in string concatenation explicitly converted to a str() in this program?
# Using '+' instead of ',' to concatenate strings makes Python add the values together,
# which doesn't work for strings and ints for example. Reduces readability, of course. #TypeError

import sys;

zustimmungsArgumente = ["ja", "j", "yes", "y", "1", ""];

class Raum:
    def __init__(self, raumZahl: int):
        self.raumZahl = raumZahl;

class TeilFläche:
    def __init__(self, raumNummer: int, teilFlächenNummer: int, teilFlächenLänge: float, teilFlächenBreite: float):
        self.raumNummer = raumNummer;
        self.teilFlächenNummer = teilFlächenNummer;
        self.teilFlächenLänge = teilFlächenLänge;
        self.teilFlächenBreite = teilFlächenBreite;
        self.teilFläche = teilFlächenLänge * teilFlächenBreite;
    def __str__(self):
        return str(("Raum:", self.raumNummer, "Teilfläche:", self.teilFläche, "Länge:", self.teilFlächenLänge, "Breite:", self.teilFlächenBreite));

def clearScr():
    import os
    os.system("cls||clear");

def getStartIndex(iterable, key, value):
    for item in iterable:
        if getattr(item, key) == value:
            return iterable.index(item);

def getInput(prompt: str, dataType):
    while True:
        response = input(prompt);
        try:
            return dataType(response);  # This equates to int(response) if dataType transferred is int. This works with all types theoretically.
        except ValueError:
            match dataType.__name__:
                case "float":
                    print("Bitte geben Sie eine valide Zahl ein.");
                case "str":
                    print("Bitte geben Sie valide Symbole ein.");
                case _:
                    print("Bitte versuchen Sie es erneut.");

def numberEditor(raumListe: list, teilFlächenListe: list, listOnly: bool = False, zimmerWahl = None, teilFlächenWahl = None, wertWahl = None, neueLänge = None, neueBreite = None):
    for Zimmer in raumListe:
        raumFläche = 0;
        for TeilFläche in teilFlächenListe:
            if TeilFläche.raumNummer == Zimmer.raumZahl:
                raumFläche += TeilFläche.teilFläche;
        print(
              "Zimmer: [" +
              str(Zimmer.raumZahl) +
              "]",
              str(raumFläche) + "m²"
              );
    if listOnly:
        input();
        return;

    zimmerWahl = getInput("Welches Zimmer wollen Sie bearbeiten?: ", int) if zimmerWahl is None else zimmerWahl;

    j = 0;
    startingPoint = getStartIndex(teilFlächenListe, "raumNummer", zimmerWahl);
    print("Starting point is:", startingPoint);
    for TeilFläche in teilFlächenListe:
        if TeilFläche.raumNummer == zimmerWahl:
            j += 1;
            print(
                "Teilfläche [" +
                str(j) +
                "] Länge:",
                str(TeilFläche.teilFlächenLänge),
                "Breite:",
                str(TeilFläche.teilFlächenBreite)
                );
    
    while True:
        teilFlächenAuswahl = getInput("Welche dieser Teilflächen wollen Sie bearbeiten?: ", int);
        teilFlächenWahl = teilFlächenAuswahl + startingPoint - 1 if teilFlächenWahl is None else teilFlächenWahl;
        if teilFlächenWahl >= j + startingPoint or teilFlächenWahl < startingPoint:
            print("Teilfläche ist nicht in Liste.");
            teilFlächenWahl = None;
            continue;
        else:
            break;

    print("Raum", zimmerWahl, "Teilfläche", str(teilFlächenAuswahl),
          "[" + str(teilFlächenWahl + 1) + "/" + str(len(teilFlächenListe)) + "]",
          "[L]änge:", str(teilFlächenListe[teilFlächenWahl].teilFlächenLänge), "[B]reite:", str(teilFlächenListe[teilFlächenWahl].teilFlächenBreite));

    while True:
        wertWahl = getInput("Welchen dieser Werte wollen Sie bearbeiten? [l/b/(d zum Löschen des Eintrags)]: ", str).lower() if wertWahl is None else wertWahl;
        match wertWahl:
            case "l":
                neueLänge = getInput("Welchen Wert wollen Sie statt " + str(teilFlächenListe[teilFlächenWahl].teilFlächenLänge) + " eintragen?: ", float) if neueLänge is None else neueLänge;
                teilFlächenListe[teilFlächenWahl].teilFlächenLänge = neueLänge;
                break;
            case "b":
                neueBreite = getInput("Welchen Wert wollen Sie statt " + str(teilFlächenListe[teilFlächenWahl].teilFlächenBreite) + " eintragen?: ", float) if neueBreite is None else neueBreite;
                print(teilFlächenListe[teilFlächenWahl].teilFlächenBreite)
                print(teilFlächenListe[teilFlächenWahl]);
                teilFlächenListe[teilFlächenWahl].teilFlächenBreite = neueBreite;
                print(teilFlächenListe[teilFlächenWahl].teilFlächenBreite)
                print(teilFlächenListe[teilFlächenWahl]);
                break;
            case "d":
                teilFlächenListe.pop(teilFlächenWahl);
                if len(teilFlächenListe) < 2:
                    raumListe.pop(zimmerWahl - 1);
                break;
            case _:
                print("Bitte geben Sie eine der angegebenen Optionen (l/b/d) ein");
    
    return (raumListe, teilFlächenListe);

def getRaum(raumListe: list = [], teilFlächenListe: list = []):
    raumAnzahl = 0;

    while True:
        raumAnzahl += 1;
        raumLänge = raumBreite = raumFläche = teilFlächenZahl = 0;

        while True:
            teilFlächenZahl += 1;
            raumLänge = getInput("Geben Sie die Länge des Raumes oder der Teilfläche in m² ein: ", float);
            raumBreite = getInput("Geben Sie die Breite des Raumes oder der Teilfläche in m² ein: ", float);
            raumFläche += raumLänge * raumBreite;

            teilFlächenVorhanden = getInput("Sind weitere Teilflächen vorhanden? [J/n]: ", str).lower();
            if teilFlächenVorhanden in zustimmungsArgumente:
                teilFlächenListe.append(TeilFläche(raumAnzahl, teilFlächenZahl, raumLänge, raumBreite));
                continue;
            else:
                break;
        teilFlächenListe.append(TeilFläche(raumAnzahl, teilFlächenZahl, raumLänge, raumBreite));
        raumListe.append(Raum(raumAnzahl));

        mehrRäume = getInput("Sind weitere Räume vorhanden? [J/n]: ", str).lower();
        if mehrRäume in zustimmungsArgumente:
            continue;
        else:
            break;
    return (raumListe, teilFlächenListe);
############################################################################################################
###
#

#
###
##########################################################################################################################################
def main():
    gebäudeFläche = 0;
    if (len(sys.argv) > 1):
        if (sys.argv[1] == "-d"):
            clearScr();
            (raumListe, teilFlächenListe) = numberEditor(raumListe=[
                Raum(1),
                Raum(2),
                Raum(3)
                ], teilFlächenListe=[
                TeilFläche(1, 1, 1, 1),                 # [0] Room 1, Area 1
                TeilFläche(1, 2, 2, 2),                 # [1] Room 1, Area 2
                TeilFläche(2, 1, 3, 3),                 # [2] Room 2, Area 1
                TeilFläche(2, 2, 4, 4),                 # [3] Room 2, Area 2
                TeilFläche(2, 3, 5, 5),                 # [4] Room 2, Area 3
                TeilFläche(3, 1, 6, 6),                 # [5] Room 3, Area 1
                TeilFläche(3, 2, 7, 7),                 # [6] Room 3, Area 2
                TeilFläche(3, 3, 8, 8)                  # [7] Room 3, Area 3
                ],
                listOnly=False,
                zimmerWahl=2,
                #teilFlächenWahl=2,
                teilFlächenWahl=None,
                wertWahl="b",
                neueLänge=4,
                neueBreite=5
                );

            for Zimmer in raumListe:
                raumFläche = 0;
                for TeilFlaeche in teilFlächenListe:
                    if TeilFlaeche.raumNummer == Zimmer.raumZahl:
                        raumFläche += TeilFlaeche.teilFläche;
                print("Die Fläche für Raum", Zimmer.raumZahl, "beträgt:", str(raumFläche) + "m²");
                gebäudeFläche += raumFläche;
            print("Die gesamte Fläche des Gebäudes beträgt:", str(gebäudeFläche) + "m²");
            print("Der Durchschnitt der Fläche des Gebäudes beträgt:", str(gebäudeFläche / (len(raumListe) if len(raumListe) > 0 else 1)) + "m²");
            return;

    (raumListe, teilFlächenListe) = getRaum();
    
    while True:
        clearScr();
        zahlenEditor = getInput("Wollen Sie die Eingaben anpassen? [J/n/(a zum Ansehen)]: ", str);
        if zahlenEditor in zustimmungsArgumente:
            (raumListe, teilFlächenListe) = numberEditor(raumListe, teilFlächenListe);
        elif zahlenEditor == "a":
            numberEditor(raumListe, teilFlächenListe, True);
        else:
            break;

    for Zimmer in raumListe:
        raumFläche = 0;
        for TeilFlaeche in teilFlächenListe:
            if TeilFlaeche == Zimmer.raumZahl:
                raumFläche += TeilFlaeche.teilFläche;
        print("Die Fläche für Raum", Zimmer.raumZahl, "beträgt:", str(raumFläche) + "m²");
        gebäudeFläche += raumFläche;
    print("Die gesamte Fläche des Gebäudes beträgt:", str(gebäudeFläche) + "m²");
    print("Der Durchschnitt der Fläche des Gebäudes beträgt:", str(gebäudeFläche / (len(raumListe) if len(raumListe) > 0 else 1)) + "m²");
##########################################################################################################################################
###
#

if __name__ == "__main__":
    main();
class Geraet:
    def __init__(self, marke , gewicht, einkaufspreis, verkaufspreis):
        self.marke = marke
        self.gewicht = gewicht
        self.einkaufspreis = einkaufspreis
        self.verkaufspreis = verkaufspreis

class Fernseher(Geraet):
    def __init__(self, marke, gewicht, einkaufspreis, verkaufspreis, auflösung):
        super().__init__(marke, gewicht, einkaufspreis, verkaufspreis)
        self.auflösung = auflösung

class Notebook(Geraet):
    def __init__(self, marke, gewicht, einkaufspreis, verkaufspreis, prozessor):
        super().__init__(marke, gewicht, einkaufspreis, verkaufspreis)
        self.prozessor = prozessor

class Regal:
    maxgewicht = 50

    def __init__(self,regalnummer):
        self.regalnummer = regalnummer
        self.gesamtGewicht = 0
        self.gerateListe = []


    def einlagern(self, geraet):
        if self.gesamtGewicht + geraet.gewicht <= self.maxgewicht:
            self.gerateListe.append(geraet)
            self.gesamtGewicht += geraet.gewicht
            print(f"Einlagerung des {geraet.marke} Erfolgreich")
        else:
            print("Regal zu Schwer")

    def anzeigen(self):
        print(f"Inhalt von Regal {self.regalnummer}:")
        for geraet in self.gerateListe:
            print(f"{geraet.marke} und {geraet.gewicht} und {geraet.einkaufspreis} und {geraet.verkaufspreis}")

    def anzahl_fernseher(self):
        return sum(isinstance(geraet, Fernseher) for geraet in self.gerateListe)

    def anzahl_notebooks(self):
        return sum(isinstance(geraet, Notebook) for geraet in self.gerateListe)

    def potenzieller_gewinn(self):
        return sum(geraet.verkaufspreis - geraet.einkaufspreis for geraet in self.gerateListe)
    

class LagerverwaltungTest:
    def main(self):

        regal1 = Regal(1)

        fernseher1 = Fernseher("Samsung", 15, 1000, 1500, "4K")
        fernseher2 = Fernseher("LG", 20, 1200, 1800, "HD")
        notebook1 = Notebook("Lenovo", 5, 800, 1200, "Intel i7")
        notebook2 = Notebook("Dell", 3, 900, 1400, "AMD Ryzen")

        regal1.einlagern(fernseher1)
        regal1.einlagern(notebook1)
        regal1.einlagern(fernseher2)
        regal1.einlagern(notebook2)

        regal1.anzeigen()
        print("Anzahl Fernseher:", regal1.anzahl_fernseher())
        print("Potenzieller Gewinn:", regal1.potenzieller_gewinn())

if __name__ == "__main__":
    lagerverwaltung_test = LagerverwaltungTest()
    lagerverwaltung_test.main()
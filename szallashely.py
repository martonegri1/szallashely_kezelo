import psycopg2

conn = psycopg2.connect(
    host = "localhost",
    database = "postgres",
    user = "postgres",
    password = "admin",
    port = "5432"
)

print('A kapcsolat sikeresen létrejött')

cur = conn.cursor()

class Szallashely():
    def __init__(self, azonosito, fajta, cim):
        self.azonosito = self.azonosito_beallitasa(azonosito)
        self.fajta = self.fajta_beallitasa(fajta)
        self.cim = cim

    def azonosito_beallitasa(self, azonosito):
        helyes_azonosito = azonosito.strip()
        if not helyes_azonosito:
            raise ValueError("Az azonosító megadása kötelező!")

        if len(helyes_azonosito) != 8:
            raise ValueError("Az azonosító 8 karaktert kell, hogy tartalmazzon!")
        return helyes_azonosito

    def fajta_beallitasa(self, fajta):
        helyes_fajta = ["üzleti", "sport", "gyógy", "egyéb"]
        if fajta not in helyes_fajta:
            raise ValueError("A fajta nem megfelelő!")
        return fajta

class Epitett_szallashely(Szallashely):
    def __init__(self, azonosito, fajta, cim, ar, ertekeles):
        super().__init__(azonosito, fajta, cim)
        self.ar = self.ar_beallitasa(ar)
        self.ertekeles = self.ertekeles_beallitasa(ertekeles)

    def ertekeles_beallitasa(self, ertekeles):
        if type(ertekeles) is not int:
            raise ValueError("Az étékelés csak egész szám lehet!")
        if ertekeles < 1 or ertekeles > 5:
            raise ValueError("Az értékelés 1 és 5 közötti szám lehet!")
        return ertekeles

    def ar_beallitasa(self, ar):
        if type(ar) is not int:
            raise ValueError("Az ár csak egész szám lehet!")
        if ar <= 0:
            raise ValueError("Az ár csak poziív szám lehet!")
        return ar

    def ar_szamitasa(self):
        vegso_ar = self.ar + (self.ar//10 * self.ertekeles)
        return vegso_ar


class Szalloda(Epitett_szallashely):
    def __init__(self, azonosito, fajta, cim, ar, ertekeles, wellness):
        super().__init__(azonosito, fajta, cim, ar, ertekeles)
        self.wellness = self.wellness_beallitasa(wellness)

    def wellness_beallitasa(self, wellness):
        if not isinstance(wellness, bool):
            raise ValueError("Csak igen vagy nem lehet!")
        return wellness

class Panzio(Epitett_szallashely):
    def __init__(self, azonosito, fajta, cim, ar, ertekeles, reggeli):
        super().__init__(azonosito, fajta, cim, ar, ertekeles)
        self.reggeli = self.reggeli_beallitasa(reggeli)

    def reggeli_beallitasa(self, reggeli):
        if not isinstance(reggeli, bool):
            raise ValueError("Csak igen vagy nem lehet!")
        return reggeli

class Camping(Szallashely):
    def __init__(self, azonosito, fajta, cim, vizpart):
        super().__init__(azonosito, fajta, cim)
        self.vizpart = self.vizpart_beallitasa(vizpart)

    def vizpart_beallitasa(self, vizpart):
        if not isinstance(vizpart, bool):
            raise ValueError("Csak igen vagy nem lehet!")
        return vizpart

    def ar_szamitasa(self):
        if self.vizpart:
            ar = 5000
        else:
            ar = 3500
        return ar

class Cim():
    def __init__(self, iranyitoszam, telepules, kozterulet_neve, hazszam):
        self.iranyitoszam = self.iranyitoszam_beallitasa(iranyitoszam)
        self.telepules = self.telepules_beallitasa(telepules)
        self.kozterulet_neve = self.kozterulet_beallitasa(kozterulet_neve)
        self.hazszam = self.hazszam_beallitasa(hazszam)

    def iranyitoszam_beallitasa(self,iranyitoszam):
        if type(iranyitoszam) is not int:
            raise ValueError("Az irányítószám csak egész szám lehet!")
        if iranyitoszam < 1000 or iranyitoszam > 9999:
            raise ValueError("Az irányítószám helytelen!")
        return iranyitoszam

    def telepules_beallitasa(self,telepules):
        if type(telepules) is not str:
            raise ValueError("A település csak szöveg lehet!")
        helyes_telepules = telepules.strip()
        if not helyes_telepules:
            raise ValueError("A település megadása kötelező!")
        return helyes_telepules

    def kozterulet_beallitasa(self,kozterulet_neve):
        if type(kozterulet_neve) is not str:
            raise ValueError("A közterület neve csak szöveg lehet!")
        helyes_kozterulet_neve = kozterulet_neve.strip()
        if not helyes_kozterulet_neve:
            raise ValueError("A közterület nevének megadása kötelező!")
        return helyes_kozterulet_neve

    def hazszam_beallitasa(self, hazszam):
        if type(hazszam) is not str:
            raise ValueError("A házszám csak szöveg lehet!")
        helyes_hazszam = hazszam.strip()
        if not helyes_hazszam:
            raise ValueError("A házszám megadása kötelező!")
        return helyes_hazszam


cim1 = Cim(1014, "Budapest", "Úri utca", "45")
cim2 = Cim(1221, "Budapest", "Kocsis utca", "32/A")
cim3 = Cim(2324, "Fonyód", "Kossuth utca", "21-22")
szalloda1 = Szalloda("SZAL0001", "üzleti", cim1, 20000, 5, True)
panzio1 = Panzio("PANZ0001", "sport", cim2, 18000, 4, True )
camping1 = Camping("CAMP0001", "egyéb", cim3, False)

print(camping1.ar_szamitasa())

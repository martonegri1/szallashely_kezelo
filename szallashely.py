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
        self.azonosito = azonosito
        self.fajta = fajta
        self.cim = cim

class Epitett_szallashely(Szallashely):
    def __init__(self, azonosito, fajta, cim, ar, ertekeles):
        super().__init__(azonosito, fajta, cim)
        self.ar = ar
        self.ertekeles = ertekeles

class Szalloda(Epitett_szallashely):
    def __init__(self, azonosito, fajta, cim, ar, ertekeles, wellness):
        super().__init__(azonosito, fajta, cim, ar, ertekeles)
        self.wellness = wellness

class Panzio(Epitett_szallashely):
    def __init__(self, azonosito, fajta, cim, ar, ertekeles, reggeli):
        super().__init__(azonosito, fajta, cim, ar, ertekeles)
        self.reggeli = reggeli

class Camping(Szallashely):
    def __init__(self, azonosito, fajta, cim, vizpart):
        super().__init__(azonosito, fajta, cim)
        self.vizpart = vizpart

class Cim():
    def __init__(self, iranyitoszam, telepules, kozterulet_neve, hazszam):
        self.iranyitoszam = iranyitoszam
        self.telepules = telepules
        self.kozterulet_neve = kozterulet_neve
        self.hazszam = hazszam


cim1 = Cim(1014, "Budapest", "Úri utca", 45)
cim2 = Cim(1221, "Budapest", "Kocsis utca", 32)
cim3 = Cim(2324, "Fonyód", "Kossuth utca", 21)
szalloda1 = Szalloda("sz000001", "üzleti", cim1, 18000, 5, True)
panzio1 = Panzio("p0000001", "sport", cim2, 20000, 4, True )
camping1 = Camping("c0000001", "egyéb", cim3, True)


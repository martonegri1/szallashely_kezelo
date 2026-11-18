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

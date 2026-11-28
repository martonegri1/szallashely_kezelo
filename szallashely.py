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

class Szallashelyek(list):
    def __init__(self):
        super().__init__()

    def szallashely_hozzaadasa(self):
        azonosito = input("Azonosító: ")
        for szallashely in self:
            if azonosito == szallashely.azonosito:
                print("A szálláshely már létezik.")
                return

        fajta = input("Fajta: ")
        iranyitoszam = int(input("Irányítószám: "))
        varos = input("Város: ")
        kozterulet_neve = input("Közterület neve: ")
        hazszam = input("Házszám: ")
        uj_cim = Cim(iranyitoszam, varos, kozterulet_neve, hazszam)

        print("1 - Szálloda")
        print("2 - Panzió")
        print("3 - Camping")
        tipus = input("Válaszd ki a szálláshely típusát: ")

        if tipus == "1":
            tipus = "szálloda"
            ar = int(input("Ár: "))
            ertekeles = int(input("Értékelés (1-5): "))
            wellness = input("Wellness (van/nincs): ").lower() == "van"

            uj_szallashely = Szalloda(
                azonosito, fajta, uj_cim, ar, ertekeles, wellness
            )

        elif tipus == "2":
            tipus = "panzió"
            ar = int(input("Ár: "))
            ertekeles = int(input("Értékelés (1-5): "))
            reggeli = input("Reggeli (van/nincs): ").lower() == "van"

            uj_szallashely = Panzio(
                azonosito, fajta, uj_cim, ar, ertekeles, reggeli
            )

        elif tipus == "3":
            tipus = "camping"
            vizpart = input("Vízpart (van/nincs): ").lower() == "van"

            uj_szallashely = Camping(
                azonosito, fajta, uj_cim, vizpart
            )

        else:
            print("Hibás választás!")
            return

        cur.execute("""
            INSERT INTO szallashelyek.szallashelyek
                (azonosito, fajta, tipus)
            VALUES (%s, %s, %s)
        """, (uj_szallashely.azonosito, uj_szallashely.fajta, tipus))

        cur.execute("""
            INSERT INTO szallashelyek.cimek
                (szallashely_id, iranyitoszam, varos, utca, hazszam)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            uj_szallashely.azonosito,
            uj_cim.iranyitoszam,
            uj_cim.telepules,
            uj_cim.kozterulet_neve,
            uj_cim.hazszam
        ))

        if tipus == "szálloda":
            cur.execute("""
                INSERT INTO szallashelyek.epitett_szallashely
                    (szallashely_id, ar, ertekeles)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (
                uj_szallashely.azonosito,
                uj_szallashely.ar,
                uj_szallashely.ertekeles
            ))

            epitett_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO szallashelyek.szalloda
                    (epitett_szallashely_id, wellness)
                VALUES (%s, %s)
            """, (epitett_id, uj_szallashely.wellness))

        elif tipus == "panzió":
            cur.execute("""
                INSERT INTO szallashelyek.epitett_szallashely
                    (szallashely_id, ar, ertekeles)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (
                uj_szallashely.azonosito,
                uj_szallashely.ar,
                uj_szallashely.ertekeles
            ))

            epitett_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO szallashelyek.panzio
                    (epitett_szallashely_id, reggeli)
                VALUES (%s, %s)
            """, (epitett_id, uj_szallashely.reggeli))

        elif tipus == "camping":
            cur.execute("""
                INSERT INTO szallashelyek.camping
                    (szallashely_id, vizpart)
                VALUES (%s, %s)
            """, (uj_szallashely.azonosito, uj_szallashely.vizpart))

        conn.commit()
        self.append(uj_szallashely)
        print("A szálláshely sikeresen hozzáadva!")

    def szallashely_torlese(self):
        azonosito = input("Azonosító: ")

        for szallashely in self:
            if azonosito == szallashely.azonosito:

                if isinstance(szallashely, Szalloda):
                    cur.execute("""
                        SELECT id
                        FROM szallashelyek.epitett_szallashely
                        WHERE szallashely_id = %s
                    """, (azonosito,))

                    epitett_id = cur.fetchone()[0]

                    cur.execute("""
                        DELETE FROM szallashelyek.szalloda
                        WHERE epitett_szallashely_id = %s
                    """, (epitett_id,))

                    cur.execute("""
                        DELETE FROM szallashelyek.epitett_szallashely
                        WHERE id = %s
                    """, (epitett_id,))

                elif isinstance(szallashely, Panzio):
                    cur.execute("""
                        SELECT id
                        FROM szallashelyek.epitett_szallashely
                        WHERE szallashely_id = %s
                    """, (azonosito,))

                    epitett_id = cur.fetchone()[0]

                    cur.execute("""
                        DELETE FROM szallashelyek.panzio
                        WHERE epitett_szallashely_id = %s
                    """, (epitett_id,))

                    cur.execute("""
                        DELETE FROM szallashelyek.epitett_szallashely
                        WHERE id = %s
                    """, (epitett_id,))

                else:
                    cur.execute("""
                        DELETE FROM szallashelyek.camping
                        WHERE szallashely_id = %s
                    """, (azonosito,))

                cur.execute("""
                    DELETE FROM szallashelyek.cimek
                    WHERE szallashely_id = %s
                """, (azonosito,))

                cur.execute("""
                    DELETE FROM szallashelyek.szallashelyek
                    WHERE azonosito = %s
                """, (azonosito,))

                conn.commit()

                self.remove(szallashely)
                print("Szálláshely törölve.")
                return

        else:
            print("Azonosító nem található.")

    def szallashely_listazasa(self, szallashely=None):
        if szallashely is None:
            for szallashely in self:
                print(f"Azonosító: {szallashely.azonosito}")
                print(f"Fajta: {szallashely.fajta}")
                print(f"Cím: {szallashely.cim}")
                if isinstance(szallashely, Szalloda):
                    print(f"Ár: {szallashely.ar}")
                    print(f"Értekeles: {szallashely.ertekeles}")
                    print(f"Wellness: {szallashely.wellness}")
                elif isinstance(szallashely, Panzio):
                    print(f"Ár: {szallashely.ar}")
                    print(f"Értekeles: {szallashely.ertekeles}")
                    print(f"Reggeli: {szallashely.reggeli}")
                elif isinstance(szallashely, Camping):
                    print(f"Vízpart: {szallashely.vizpart}")
                print("-" * 40)

        elif isinstance(szallashely, list):
            for szallashely in szallashely:
                print(f"Azonosító: {szallashely.azonosito}")
                print(f"Fajta: {szallashely.fajta}")
                print(f"Cím: {szallashely.cim}")
                if isinstance(szallashely, Szalloda):
                    print(f"Ár: {szallashely.ar}")
                    print(f"Értekeles: {szallashely.ertekeles}")
                    print(f"Wellness: {szallashely.wellness}")
                elif isinstance(szallashely, Panzio):
                    print(f"Ár: {szallashely.ar}")
                    print(f"Értekeles: {szallashely.ertekeles}")
                    print(f"Reggeli: {szallashely.reggeli}")
                elif isinstance(szallashely, Camping):
                    print(f"Vízpart: {szallashely.vizpart}")
                print("-" * 40)

        else:
            szallashely = [szallashely]
            for szallashely in szallashely:
                print(f"Azonosító: {szallashely.azonosito}")
                print(f"Fajta: {szallashely.fajta}")
                print(f"Cím: {szallashely.cim}")
                if isinstance(szallashely, Szalloda):
                    print(f"Ár: {szallashely.ar}")
                    print(f"Értekeles: {szallashely.ertekeles}")
                    print(f"Wellness: {szallashely.wellness}")
                elif isinstance(szallashely, Panzio):
                    print(f"Ár: {szallashely.ar}")
                    print(f"Értekeles: {szallashely.ertekeles}")
                    print(f"Reggeli: {szallashely.reggeli}")
                elif isinstance(szallashely, Camping):
                    print(f"Vízpart: {szallashely.vizpart}")
                print("-" * 40)

    def szallashely_keresese(self):
        azonosito = input("Azonosito: ")
        for szallashely in self:
            if azonosito == szallashely.azonosito:
                szallashelyek.szallashely_listazasa(szallashely)
                return
        else:
            print("Azonosító nem található.")
        return

    def szallashely_modositasa(self):
        azonosito = input("Azonosító: ")
        for szallashely in self:
            if azonosito == szallashely.azonosito:
                print("1 - Azonosító")
                print("2 - Fajta")
                print("3 - Cím")
                if isinstance(szallashely, Szalloda):
                    print("4 - Ár")
                    print("5 - Értékelés")
                    print("6 - Wellness")
                elif isinstance(szallashely, Panzio):
                    print("4 - Ár")
                    print("5 - Értékelés")
                    print("6 - Reggeli")
                elif isinstance(szallashely, Camping):
                    print("4 - Vízpart")

                modositas = input("Mit szeretnél módosítani?")

                if modositas == "1":
                    uj_azonosito = input("Új azonosító: ")
                    for elem in self:
                        if elem is not szallashely and uj_azonosito == elem.azonosito:
                            print("Az azonosító már használatban van!")
                            return
                    szallashely.azonosito = szallashely.azonosito_beallitasa(uj_azonosito)
                    return

                elif modositas == "2":
                    uj_fajta = input("Új fajta: ")
                    if uj_fajta != szallashely.fajta:
                        szallashely.fajta = szallashely.fajta_beallitasa(uj_fajta)
                        return
                    else:
                        print("Ugyanaz a fajta nem adható meg!")
                        return

                elif modositas == "3":
                    uj_cim = input("Új cim: ")
                    if uj_cim != szallashely.cim:
                        szallashely.cim = uj_cim
                        return
                    else:
                        print("Ugyanaz a cím nem adható meg!")
                        return

                elif modositas == "4":
                    if isinstance(szallashely, Szalloda) or isinstance(szallashely, Panzio):
                        uj_ar = int(input("Új ár: "))
                        if uj_ar != szallashely.ar:
                            szallashely.ar = szallashely.ar_beallitasa(uj_ar)
                            return
                        else:
                            print("Ugyanaz az ár nem adható meg!")
                            return

                    elif isinstance(szallashely, Camping):
                        uj_vizpart = input("Vízpart: ")
                        if uj_vizpart != szallashely.vizpart:
                            if uj_vizpart == "van":
                                uj_vizpart = True
                            elif uj_vizpart == "nincs":
                                uj_vizpart = False
                            else:
                                print("Hibás választás!")
                                return
                            szallashely.vizpart = szallashely.vizpart_beallitasa(uj_vizpart)
                            return
                        else:
                            print("Ugyanaz nem adható meg!")
                            return

                elif modositas == "5":
                    if isinstance(szallashely, Szalloda) or isinstance(szallashely, Panzio):
                        uj_ertekeles = int(input("Új értekeles: "))
                        if uj_ertekeles != szallashely.ertekeles:
                            szallashely.ertekeles = szallashely.ertekeles_beallitasa(uj_ertekeles)
                            return
                        else:
                            print("Ugyanaz az értékelés nem adható meg!")
                            return

                elif modositas == "6":
                    if isinstance(szallashely, Szalloda):
                        uj_wellness = input("Wellness: ")
                        if uj_wellness != szallashely.wellness:
                            if uj_wellness == "van":
                                uj_wellness = True
                            elif uj_wellness == "nincs":
                                uj_wellness = False
                            else:
                                print("Hibás választás!")
                                return
                            szallashely.wellness = szallashely.wellness_beallitasa(uj_wellness)
                            return
                        else:
                            print("Ugyanaz nem adható meg!")
                            return
                    elif isinstance(szallashely, Panzio):
                        uj_reggeli = input("Reggeli: ")
                        if uj_reggeli != szallashely.reggeli:
                            if uj_reggeli == "van":
                                uj_reggeli = True
                            elif uj_reggeli == "nincs":
                                uj_reggeli = False
                            else:
                                print("Hibás választás!")
                                return
                            szallashely.reggeli = szallashely.reggeli_beallitasa(uj_reggeli)
                            return
                        else:
                            print("Ugyanaz nem adható meg!")
                            return
        else:
            print("Azonosító nem található.")

    def szallashelyek_rendezese(self):
        print("1 - Azonosító szerint")
        print("2 - Fajta szerint")
        rendezes = input("Add meg a rendezés szempontját: ")

        if rendezes == "1":
            rendezett_azonosito = sorted(self, key=lambda x:x.azonosito, reverse=False)
            self.szallashely_listazasa(rendezett_azonosito)
        elif rendezes == "2":
            rendezett_fajta = sorted(self, key=lambda x:x.fajta, reverse=False)
            self.szallashely_listazasa(rendezett_fajta)

    def szallashelyek_szurese(self):
        print("1 - Azonosító alapján")
        print("2 - Fajta alapján")
        print("3 - Típus alapján")
        szures = input("Válassz: ")

        if szures == "1":
            azonosito = input("Azonosító: ")
            talalat = False
            for szallashely in self:
                if azonosito == szallashely.azonosito:
                    talalat = True
                    self.szallashely_listazasa(szallashely)
            if not talalat:
                print("A keresett azonosító nem található.")
                return
        elif szures == "2":
            fajta = input("Fajta: ")
            talalat = False
            for szallashely in self:
                if fajta == szallashely.fajta:
                    talalat = True
                    self.szallashely_listazasa(szallashely)
            if not talalat:
                print("A keresett fajta nem található.")
                return
        elif szures == "3":
            tipus = input("Típus: ")
            talalat = False
            for szallashely in self:
                if tipus == "Szalloda" and isinstance(szallashely, Szalloda):
                    talalat = True
                    self.szallashely_listazasa(szallashely)

                elif tipus == "Panzio" and isinstance(szallashely, Panzio):
                    talalat = True
                    self.szallashely_listazasa(szallashely)

                elif tipus == "Camping" and isinstance(szallashely, Camping):
                    talalat = True
                    self.szallashely_listazasa(szallashely)

            if not talalat:
                print("A keresett típus nem található.")
                return

    def szallashelyek_statisztikaja(self):
        szalloda_db = 0
        panzio_db = 0
        camping_db = 0
        for szallashely in self:
            if isinstance(szallashely, Szalloda):
                szalloda_db += 1
            elif isinstance(szallashely, Panzio):
                panzio_db += 1
            elif isinstance(szallashely, Camping):
                camping_db += 1
        print(f"+--------------------+-----------+")
        print(f"| Szálláshely típusa | Darabszám |")
        print(f"+--------------------+-----------+")
        print(f"|Összes szálláshely  |{len(self):>11}|")
        print(f"|Szálloda            |{szalloda_db:>11}|")
        print(f"|Panzió              |{panzio_db:>11}|")
        print(f"|Camping             |{camping_db:>11}|")
        print(f"+--------------------+-----------+")

    def szallashelyek_betoltese(self):
        cur.execute("""
            SELECT *
            FROM szallashelyek.szallashelyek
            INNER JOIN szallashelyek.cimek
            ON szallashelyek.szallashelyek.azonosito = szallashelyek.cimek.szallashely_id
        """)
        adatok = cur.fetchall()
        for adat in adatok:
            cim = Cim((adat[5]), (adat[6]), (adat[7]), (adat[8]))
            if adat[2] == "szálloda":
                cur.execute("""
                    SELECT
                        szallashelyek.szallashelyek.azonosito,
                        szallashelyek.epitett_szallashely.ar,
                        szallashelyek.epitett_szallashely.ertekeles,
                        szallashelyek.szalloda.wellness
                    FROM szallashelyek.epitett_szallashely
                    INNER JOIN szallashelyek.szallashelyek
                        ON szallashelyek.epitett_szallashely.szallashely_id = szallashelyek.szallashelyek.azonosito
                    INNER JOIN szallashelyek.szalloda
                        ON szallashelyek.epitett_szallashely.id = szallashelyek.szalloda.epitett_szallashely_id
                    WHERE szallashelyek.epitett_szallashely.szallashely_id = %s
                """, (adat[0],))
                szalloda = cur.fetchone()
                szalloda = Szalloda((szalloda[0]), (adat[1]), cim, (szalloda[1]), (szalloda[2]), (szalloda[3]))
                self.append(szalloda)
            elif adat[2] == "panzió":
                cur.execute("""
                    SELECT
                        szallashelyek.szallashelyek.azonosito,
                        szallashelyek.epitett_szallashely.ar,
                        szallashelyek.epitett_szallashely.ertekeles,
                        szallashelyek.panzio.reggeli
                    FROM szallashelyek.epitett_szallashely
                    INNER JOIN szallashelyek.szallashelyek
                        ON szallashelyek.epitett_szallashely.szallashely_id = szallashelyek.szallashelyek.azonosito
                    INNER JOIN szallashelyek.panzio
                        ON szallashelyek.epitett_szallashely.id = szallashelyek.panzio.epitett_szallashely_id
                    WHERE szallashelyek.epitett_szallashely.szallashely_id = %s
                """, (adat[0],))
                panzio = cur.fetchone()
                panzio = Panzio((panzio[0]), (adat[1]), cim, (panzio[1]), (panzio[2]), (panzio[3]))
                self.append(panzio)
            elif adat[2] == "camping":
                cur.execute("""
                    SELECT
                        szallashelyek.szallashelyek.azonosito,
                        szallashelyek.camping.vizpart
                    FROM szallashelyek.szallashelyek
                    INNER JOIN szallashelyek.camping
                        ON szallashelyek.szallashelyek.azonosito = szallashelyek.camping.szallashely_id
                    WHERE szallashelyek.szallashelyek.azonosito = %s
                """, (adat[0],))
                camping = cur.fetchone()
                camping = Camping((camping[0]), (adat[1]), cim, (camping[1]))
                self.append(camping)


cim1 = Cim(1014, "Budapest", "Úri utca", "45")
cim2 = Cim(1221, "Budapest", "Kocsis utca", "32/A")
cim3 = Cim(2324, "Fonyód", "Kossuth utca", "21-22")
szalloda1 = Szalloda("SZAL0001", "üzleti", cim1, 20000, 5, True)
panzio1 = Panzio("PANZ0001", "sport", cim2, 18000, 4, True )
camping1 = Camping("CAMP0001", "egyéb", cim3, False)

szallashelyek = Szallashelyek()
szallashelyek.szallashelyek_betoltese()
#szallashelyek.szallashely_hozzaadasa()
#szallashelyek.szallashely_listazasa()
szallashelyek.szallashely_torlese()
#szallashelyek.szallashely_modositasa()
#szallashelyek.szallashelyek_statisztikaja()

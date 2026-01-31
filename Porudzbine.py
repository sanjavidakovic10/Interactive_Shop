import Artikli
import datetime
import os
import ast
import Korisnici  # da bismo prikazali prodavce

putanja_porudzbine = "porudzbine.txt"


def ucitaj_porudzbine():
    porudzbine = []
    if not os.path.exists(putanja_porudzbine):
        return porudzbine

    with open(putanja_porudzbine, "r", encoding="utf-8") as f:
        for linija in f:
            linija = linija.strip()
            if linija == "" or linija.startswith("#"):
                continue
            delovi = linija.split("|")
            if len(delovi) != 7:  # zaštita da se ne sruši
                print(f"⚠ Preskačem neispravnu liniju: {linija}")
                continue
            porudzbina = {
                "id_racuna": int(delovi[0]),
                "id_kupca": int(delovi[1]),
                "id_prodavca": int(delovi[2]),
                "datum": delovi[3],
                "vreme": delovi[4],
                "artikli": ast.literal_eval(delovi[5]),
                "ukupna_cena": float(delovi[6])
            }
            porudzbine.append(porudzbina)
    return porudzbine


def sacuvaj_porudzbine(porudzbine):
    with open(putanja_porudzbine, "w", encoding="utf-8") as f:
        f.write("#id_racuna|id_kupca|id_prodavca|datum|vreme|listaRecnikaArtikala|racunCena\n")
        for p in porudzbine:
            linija = f"{p['id_racuna']}|{p['id_kupca']}|{p['id_prodavca']}|{p['datum']}|{p['vreme']}|{p['artikli']}|{p['ukupna_cena']}\n"
            f.write(linija)


def kupovina(korisnik):
    Artikli.prikazi_artikle()
    artikli = Artikli.ucitaj_artikle()

    # ➕ izbor prodavca od strane kupca
    korisnici = Korisnici.ucitaj_korisnike()
    prodavci = [k for k in korisnici.values() if k["uloga"] == "prodavac"]

    if not prodavci:
        print("⚠ Nema dostupnih prodavaca.")
        return

    print("\n=== Lista prodavaca ===")
    for p in prodavci:
        print(f"{p['id']} - {p['ime']} {p['prezime']} ({p['username']})")

    try:
        id_prodavca = int(input("Unesite ID prodavca kod kog kupujete: ").strip())
    except ValueError:
        print("❌ Neispravan unos!")
        return

    if id_prodavca not in [p["id"] for p in prodavci]:
        print("❌ Ne postoji prodavac sa tim ID-jem!")
        return

    # ➕ unos artikala
    korpa = []
    ukupna_cena = 0

    while True:
        sifra = input("\nUnesite šifru artikla za kupovinu (ili X za kraj): ").strip()
        if sifra.upper() == "X":
            break

        if sifra not in artikli:
            print("❌ Artikal sa tom šifrom ne postoji!")
            continue

        try:
            kolicina = int(input("Unesite količinu: "))
        except ValueError:
            print("❌ Morate uneti broj!")
            continue

        if kolicina <= 0:
            print("❌ Količina mora biti veća od 0.")
            continue

        if artikli[sifra]["stanje"] < kolicina:
            print("❌ Nema dovoljno na stanju!")
            continue

        stavka = {
            "sifra": sifra,
            "naziv": artikli[sifra]["naziv"],
            "cena": artikli[sifra]["cena"],
            "kolicina": kolicina
        }
        korpa.append(stavka)
        ukupna_cena += kolicina * artikli[sifra]["cena"]

        # smanji stanje
        artikli[sifra]["stanje"] -= kolicina
        Artikli.sacuvaj_artikle(artikli)

        print(f"✅ Dodato u korpu: {artikli[sifra]['naziv']} x {kolicina}")

    if not korpa:
        print("🛒 Korpa je prazna. Kupovina otkazana.")
        return

    print("\n=== RAČUN ===")
    for stavka in korpa:
        print(f"{stavka['naziv']} x {stavka['kolicina']} = {stavka['kolicina'] * stavka['cena']:.2f} RSD")
    print(f"Ukupno za plaćanje: {ukupna_cena:.2f} RSD")

    potvrda = input("Potvrdite kupovinu (da/ne): ").strip().lower()
    if potvrda != "da":
        print("❌ Kupovina otkazana.")
        return

    # učitaj sve porudžbine
    porudzbine = ucitaj_porudzbine()
    novi_id = 1 if not porudzbine else max(p["id_racuna"] for p in porudzbine) + 1

    datum = datetime.date.today().isoformat()
    vreme = datetime.datetime.now().strftime("%H:%M")

    nova = {
        "id_racuna": novi_id,
        "id_kupca": korisnik["id"],
        "id_prodavca": id_prodavca,
        "datum": datum,
        "vreme": vreme,
        "artikli": korpa,
        "ukupna_cena": ukupna_cena
    }
    porudzbine.append(nova)
    sacuvaj_porudzbine(porudzbine)

    print(f"✅ Kupovina uspešno završena! Prodavac ID {id_prodavca}.")


def prikazi_porudzbine(korisnik):
    porudzbine = ucitaj_porudzbine()
    moje = [p for p in porudzbine if p["id_prodavca"] == korisnik["id"]]
    if not moje:
        print("⚠ Nema porudžbina.")
        return

    print("\n=== Sve porudžbine ===")
    for p in moje:
        print(f"Račun #{p['id_racuna']} | Kupac ID: {p['id_kupca']} | Prodavac ID: {p['id_prodavca']} | "
              f"{p['datum']} {p['vreme']} | Artikli: {p['artikli']} | Ukupno: {p['ukupna_cena']:.2f} RSD")


def prikazi_porudzbine_kupca(korisnik):
    porudzbine = ucitaj_porudzbine()
    moje = [p for p in porudzbine if p["id_kupca"] == korisnik["id"]]

    if not moje:
        print("\n⚠ Nemate nijednu porudžbinu.")
        return

    print(f"\n=== Porudžbine kupca {korisnik['ime']} {korisnik['prezime']} ===")
    for p in moje:
        print(f"Račun #{p['id_racuna']} | Datum: {p['datum']} {p['vreme']} | "
              f"Prodavac ID: {p['id_prodavca']} | Artikli: {p['artikli']} | Ukupno: {p['ukupna_cena']:.2f} RSD")

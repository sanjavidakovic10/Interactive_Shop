import os

putanja_artikli = "artikli.txt"


def ucitaj_artikle():
    artikli = {}
    if not os.path.exists(putanja_artikli):
        return artikli

    with open(putanja_artikli, "r", encoding="utf-8") as f:
        for linija in f:
            linija = linija.strip()
            if linija == "" or linija.startswith("#"):
                continue
            # format: šifra|naziv|cena|kolikoImaNaStanju
            delovi = linija.split("|")
            artikli[delovi[0]] = {
                "sifra": delovi[0],
                "naziv": delovi[1],
                "cena": float(delovi[2]),
                "stanje": int(delovi[3])
            }
    return artikli


def sacuvaj_artikle(artikli):
    with open(putanja_artikli, "w", encoding="utf-8") as f:
        f.write("#šifra|naziv|cena|kolikoImaNaStanju\n")
        for sifra, a in artikli.items():
            linija = f"{a['sifra']}|{a['naziv']}|{a['cena']}|{a['stanje']}\n"
            f.write(linija)


def prikazi_artikle():
    artikli = ucitaj_artikle()
    if not artikli:
        print("Nema artikala u prodavnici.")
        return
    print("\n=== Lista artikala ===")
    for sifra, a in artikli.items():
        print(f"{a['sifra']} | {a['naziv']} | {a['cena']} RSD | Na stanju: {a['stanje']}")


def dodaj_artikal():
    artikli = ucitaj_artikle()

    sifra = input("Unesite šifru artikla: ").strip()
    if sifra in artikli:
        print("❌ Artikal sa tom šifrom već postoji!")
        return

    naziv = input("Unesite naziv artikla: ").strip()
    try:
        cena = float(input("Unesite cenu artikla: "))
        stanje = int(input("Unesite koliko ima na stanju: "))
    except ValueError:
        print("❌ Cena mora biti broj, stanje ceo broj!")
        return

    artikli[sifra] = {"sifra": sifra, "naziv": naziv, "cena": cena, "stanje": stanje}
    sacuvaj_artikle(artikli)
    print("✅ Artikal uspešno dodat!")


def izmeni_artikal():
    artikli = ucitaj_artikle()
    sifra = input("Unesite šifru artikla koji menjate: ").strip()
    if sifra not in artikli:
        print("❌ Ne postoji artikal sa tom šifrom!")
        return

    print(f"Menjate artikal: {artikli[sifra]['naziv']} "
          f"(trenutno {artikli[sifra]['cena']} RSD, stanje {artikli[sifra]['stanje']})")

    novi_naziv = input("Unesite novi naziv (ENTER za preskok): ").strip()
    nova_cena = input("Unesite novu cenu (ENTER za preskok): ").strip()
    novo_stanje = input("Unesite novo stanje (ENTER za preskok): ").strip()

    if novi_naziv:
        artikli[sifra]["naziv"] = novi_naziv
    if nova_cena:
        try:
            artikli[sifra]["cena"] = float(nova_cena)
        except ValueError:
            print("❌ Cena mora biti broj!")
    if novo_stanje:
        try:
            artikli[sifra]["stanje"] = int(novo_stanje)
        except ValueError:
            print("❌ Stanje mora biti ceo broj!")

    sacuvaj_artikle(artikli)
    print("✅ Artikal uspešno izmenjen!")


def obrisi_artikal():
    artikli = ucitaj_artikle()
    sifra = input("Unesite šifru artikla koji brišete: ").strip()
    if sifra not in artikli:
        print("❌ Ne postoji artikal sa tom šifrom!")
        return

    potvrda = input(f"Da li ste sigurni da želite da obrišete {artikli[sifra]['naziv']}? (da/ne): ").strip().lower()
    if potvrda == "da":
        del artikli[sifra]
        sacuvaj_artikle(artikli)
        print("✅ Artikal uspešno obrisan!")
    else:
        print("❌ Brisanje otkazano.")
        
def str2artikal(line):
    
    parts = [p.strip() for p in line.rstrip('\n').split('|')]

    if len(parts) < 4:
        return None

    return {
        'sifra': parts[0],
        'naziv': parts[1],
        'cena': parts[2],
        'stanje': parts[3] if len(parts) >= 4 else ''  # (opciono)
    }

def Artikal2str(artikal):
    return '|'.join([
        artikal['sifra'],
        artikal['naziv'],
        artikal['cena'],
        artikal['stanje'],
    ])
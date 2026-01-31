import os

putanja_korisnici = "korisnici.txt"


def ucitaj_korisnike():
    korisnici = {}
    if not os.path.exists(putanja_korisnici):
        return korisnici

    with open(putanja_korisnici, "r", encoding="utf-8") as f:
        for linija in f:
            linija = linija.strip()
            if linija == "" or linija.startswith("#"):
                continue
            # format: id|ime|prezime|username|password|uloga
            delovi = linija.split("|")
            korisnici[int(delovi[0])] = {
                "id": int(delovi[0]),
                "ime": delovi[1],
                "prezime": delovi[2],
                "username": delovi[3],
                "password": delovi[4],
                "uloga": delovi[5]
            }
    return korisnici


def sacuvaj_korisnike(korisnici):
    with open(putanja_korisnici, "w", encoding="utf-8") as f:
        f.write("#id|ime|prezime|username|password|uloga\n")
        for kid, k in korisnici.items():
            linija = f"{k['id']}|{k['ime']}|{k['prezime']}|{k['username']}|{k['password']}|{k['uloga']}\n"
            f.write(linija)


def login():
    korisnici = ucitaj_korisnike()
    if not korisnici:
        print("⚠ Nema korisnika u sistemu.")
        return None

    username = input("Unesite korisničko ime: ").strip()
    password = input("Unesite lozinku: ").strip()

    for k in korisnici.values():
        if k["username"] == username and k["password"] == password:
            print(f"✅ Uspešno logovanje kao {k['uloga']} ({k['ime']} {k['prezime']})")
            return k

    print("❌ Pogrešno korisničko ime ili lozinka.")
    return None


def registracija():
    korisnici = ucitaj_korisnike()

    ime = input("Unesite ime: ").strip()
    prezime = input("Unesite prezime: ").strip()
    username = input("Unesite novo korisničko ime: ").strip()

    for k in korisnici.values():
        if k["username"] == username:
            print("❌ Korisničko ime već postoji!")
            return

    password = input("Unesite lozinku: ").strip()

    uloga = input("Unesite ulogu (kupac/prodavac): ").strip().lower()
    if uloga not in ["kupac", "prodavac"]:
        print("❌ Uloga mora biti 'kupac' ili 'prodavac'!")
        return

    novi_id = 1
    if korisnici:
        novi_id = max(korisnici.keys()) + 1

    korisnici[novi_id] = {
        "id": novi_id,
        "ime": ime,
        "prezime": prezime,
        "username": username,
        "password": password,
        "uloga": uloga
    }

    sacuvaj_korisnike(korisnici)
    print(f"✅ Registracija uspešna! ID: {novi_id}, uloga: {uloga}")
    
def StringToKorisnik(linija: str):
    ln = linija.strip()
    if ln == "" or ln.startswith("#"):
        return None
    delovi = [x.strip() for x in ln.split("|")]
    if len(delovi) < 6 or not delovi[0].isdigit():
        return None
    return {
        "id": int(delovi[0]),
        "ime": delovi[1],
        "prezime": delovi[2],
        "username": delovi[3],
        "password": delovi[4],
        "uloga": delovi[5]
    }

def KorisnikToString(k: dict) -> str:
    return f"{int(k['id'])}|{k['ime']}|{k['prezime']}|{k['username']}|{k['password']}|{k['uloga']}"
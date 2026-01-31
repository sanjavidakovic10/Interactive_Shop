kupci = []


def ucitaj_kupce():
    try:
        with open("kupci.txt", "r", encoding="utf-8") as f:
            for linija in f:
                korisnicko_ime, ime, prezime = linija.strip().split("|")
                kupci.append({
                    "korisnicko_ime": korisnicko_ime,
                    "ime": ime,
                    "prezime": prezime
                })
    except FileNotFoundError:
        print("Fajl 'kupci.txt' nije pronađen.")


def prikazi_kupce():
    print("\n--- Lista registrovanih kupaca ---")
    print("Korisničko ime | Ime       | Prezime")
    print("----------------|-----------|-----------")
    for k in kupci:
        print(f"{k['korisnicko_ime']:16}|{k['ime']:10}|{k['prezime']}")

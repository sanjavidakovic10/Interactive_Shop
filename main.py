import Korisnici
import Kupci
import Artikli
import Porudzbine
import matplotlib.pyplot as plt
import datetime

ulogovani_korisnik = None


def meni_prodavac():
    print("\n=== Meni prodavca ===")
    print("1 - Prikaz artikala")
    print("2 - Dodavanje artikla")
    print("3 - Izmena artikla")
    print("4 - Brisanje artikla")
    print("5 - Pregled prodaje")
    print("6 - Generisanje grafikona zarade")
    print("X - Izlaz")
    return input("Izaberite opciju: ").strip()


def meni_kupac():
    print("\n=== Meni kupca ===")
    print("1 - Prikaz artikala")
    print("2 - Kupovina artikala")
    print("3 - Prikaz mojih porudžbina")
    print("X - Izlaz")
    return input("Izaberite opciju: ").strip()


def generisi_grafikon():
    # Učitavamo porudžbine
    porudzbine = Porudzbine.ucitaj_porudzbine()

    if not porudzbine:
        print("Nema podataka o prodaji za grafikon.")
        return

    # grupisanje zarade po danima
    zarada_po_danima = {}
    for p in porudzbine:
        datum = p["datum"]
        iznos = float(p["ukupna_cena"])
        if datum in zarada_po_danima:
            zarada_po_danima[datum] += iznos
        else:
            zarada_po_danima[datum] = iznos

    # crtanje grafikona
    datumi = list(zarada_po_danima.keys())
    vrednosti = list(zarada_po_danima.values())

    plt.figure(figsize=(8, 5))
    plt.bar(datumi, vrednosti, color="skyblue")
    plt.xlabel("Datum")
    plt.ylabel("Ukupna zarada")
    plt.title("Zarada po danima")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("zarada_po_danima.png")
    plt.show()

    print("Grafikon je generisan i sačuvan kao 'zarada_po_danima.png'.")


def main():
    print("\n=== Dobrodošli u aplikaciju PRODAVNICA ===")
    global ulogovani_korisnik
    ulogovani_korisnik = Korisnici.login()

    Artikli.ucitaj_artikle()

    if ulogovani_korisnik is None:
        print("\nNeuspešno logovanje. Pogrešno korisničko ime ili lozinka. Kraj programa.")
        return

    if ulogovani_korisnik["uloga"] == "prodavac":
        while True:
            izbor = meni_prodavac()
            if izbor == "1":
                Artikli.prikazi_artikle()
            elif izbor == "2":
                Artikli.dodaj_artikal()
            elif izbor == "3":
                Artikli.izmeni_artikal()
            elif izbor == "4":
                Artikli.obrisi_artikal()
            elif izbor == "5":
                Porudzbine.prikazi_porudzbine(ulogovani_korisnik)
            elif izbor == "6":
                generisi_grafikon()
            elif izbor.upper() == "X":
                print("Izlaz iz sistema. Doviđenja!")
                break
            else:
                print("Nepoznata opcija.")

    elif ulogovani_korisnik["uloga"] == "kupac":
        while True:
            izbor = meni_kupac()
            if izbor == "1":
                Artikli.prikazi_artikle()
            elif izbor == "2":
                Porudzbine.kupovina(ulogovani_korisnik)
            elif izbor == "3":
                Porudzbine.prikazi_porudzbine_kupca(ulogovani_korisnik)
            elif izbor.upper() == "X":
                print("Izlaz iz sistema. Doviđenja!")
                break
            else:
                print("Nepoznata opcija.")


if __name__ == "__main__":
    main()

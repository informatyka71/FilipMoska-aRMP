# Definiujemy klasę Produkt, która reprezentuje produkt w systemie MRP.
class Produkt:
    def __init__(self, nazwa, czas_realizacji, poczatkowy_stan_magazynowy, minimalne_zapotrzebowanie=0, wielkosc_partii=1):
        # Inicjalizacja atrybutów produktu
        self.nazwa = nazwa
        self.czas_realizacji = czas_realizacji
        self.poczatkowy_stan_magazynowy = poczatkowy_stan_magazynowy
        self.minimalne_zapotrzebowanie = minimalne_zapotrzebowanie
        self.wielkosc_partii = wielkosc_partii
        self.zapotrzebowanie_brutto = []  # Lista zapotrzebowań brutto na produkt
        self.zaplanowane_dostawy = []  # Lista zaplanowanych dostaw produktu
        self.stan_magazynowy = poczatkowy_stan_magazynowy  # Aktualny stan magazynowy produktu
        self.zapotrzebowanie_netto = []  # Lista zapotrzebowań netto na produkt
        self.zaplanowane_zwolnienia_zamowienia = []  # Lista zaplanowanych zwolnień zamówienia
        self.zaplanowane_przyjecia_zamowienia = []  # Lista zaplanowanych przyjęć zamówienia
        self.komponenty = {}  # Słownik komponentów i ich ilości potrzebnych do produkcji produktu

    # Metoda dodająca zapotrzebowanie brutto do listy zapotrzebowań brutto
    def dodaj_zapotrzebowanie_brutto(self, zapotrzebowanie):
        self.zapotrzebowanie_brutto.append(zapotrzebowanie)

    # Metoda dodająca zaplanowaną dostawę do listy zaplanowanych dostaw
    def dodaj_zaplanowana_dostawe(self, dostawa):
        self.zaplanowane_dostawy.append(dostawa)

    # Metoda dodająca komponent do słownika komponentów
    def dodaj_komponent(self, komponent, ilosc):
        self.komponenty[komponent.nazwa] = ilosc

# Definiujemy klasę MRP, która zarządza wszystkimi produktami i obliczeniami MRP.
class MRP:
    def __init__(self):
        self.produkty = {}  # Słownik przechowujący wszystkie produkty

    # Metoda dodająca produkt do słownika produktów
    def dodaj_produkt(self, produkt):
        self.produkty[produkt.nazwa] = produkt

    # Metoda obliczająca MRP dla podanego produktu przez określoną liczbę okresów
    def oblicz_mrp(self, nazwa_produktu, okresy):
        produkt = self.produkty[nazwa_produktu]

        for okres in range(okresy):
            zapotrzebowanie_brutto = produkt.zapotrzebowanie_brutto[okres] if okres < len(produkt.zapotrzebowanie_brutto) else 0
            zaplanowana_dostawa = produkt.zaplanowane_dostawy[okres] if okres < len(produkt.zaplanowane_dostawy) else 0

            if okres == 0:
                stan_magazynowy = produkt.poczatkowy_stan_magazynowy
            else:
                stan_magazynowy = produkt.stan_magazynowy

            zapotrzebowanie_netto = max(0, zapotrzebowanie_brutto - stan_magazynowy - zaplanowana_dostawa + produkt.minimalne_zapotrzebowanie)
            zaplanowane_przyjecie_zamowienia = self.oblicz_zaplanowane_przyjecie_zamowienia(zapotrzebowanie_netto, produkt.wielkosc_partii)

            if okres + produkt.czas_realizacji < okresy:
                produkt.zaplanowane_przyjecia_zamowienia.append(zaplanowane_przyjecie_zamowienia)
                produkt.zaplanowane_zwolnienia_zamowienia.append(zaplanowane_przyjecie_zamowienia)
            else:
                produkt.zaplanowane_przyjecia_zamowienia.append(0)
                produkt.zaplanowane_zwolnienia_zamowienia.append(0)

            produkt.zapotrzebowanie_netto.append(zapotrzebowanie_netto)
            produkt.stan_magazynowy = max(0, stan_magazynowy + zaplanowana_dostawa - zapotrzebowanie_brutto)

            for nazwa_komponentu, ilosc in produkt.komponenty.items():
                self.produkty[nazwa_komponentu].dodaj_zapotrzebowanie_brutto(zaplanowane_przyjecie_zamowienia * ilosc)

    # Metoda obliczająca zaplanowane przyjęcie zamówienia na podstawie zapotrzebowania netto i wielkości partii
    def oblicz_zaplanowane_przyjecie_zamowienia(self, zapotrzebowanie_netto, wielkosc_partii):
        if zapotrzebowanie_netto == 0:
            return 0
        else:
            return ((zapotrzebowanie_netto + wielkosc_partii - 1) // wielkosc_partii) * wielkosc_partii

# Funkcja pobierająca dane produktu od użytkownika
def pobierz_dane_produktu(okresy):
    nazwa = input("Podaj nazwę produktu: ")
    czas_realizacji = int(input(f"Podaj czas realizacji dla produktu {nazwa} (w okresach): "))
    poczatkowy_stan_magazynowy = int(input(f"Podaj początkowy stan magazynowy dla produktu {nazwa}: "))
    minimalne_zapotrzebowanie = input(f"Podaj minimalny poziom zapasów dla produktu {nazwa} (naciśnij Enter, aby pominąć): ")
    minimalne_zapotrzebowanie = int(minimalne_zapotrzebowanie) if minimalne_zapotrzebowanie else 0
    wielkosc_partii = int(input(f"Podaj wielkość partii produkcyjnej dla produktu {nazwa}: "))

    zapotrzebowanie_brutto = []
    for okres in range(okresy):
        zapotrzebowanie = int(input(f"Podaj zapotrzebowanie brutto dla produktu {nazwa} w okresie {okres + 1}: "))
        zapotrzebowanie_brutto.append(zapotrzebowanie)

    liczba_komponentow = int(input(f"Podaj liczbę komponentów dla produktu {nazwa}: "))
    komponenty = {}
    for _ in range(liczba_komponentow):
        nazwa_komponentu = input("Podaj nazwę komponentu: ")
        ilosc = int(input(f"Podaj ilość komponentu {nazwa_komponentu} potrzebną do produkcji {nazwa}: "))
        komponenty[nazwa_komponentu] = ilosc

    return nazwa, czas_realizacji, poczatkowy_stan_magazynowy, minimalne_zapotrzebowanie, wielkosc_partii, zapotrzebowanie_brutto, komponenty

# Główna funkcja programu
def main():
    okresy = 10
    mrp = MRP()

    liczba_produktow = int(input("Podaj liczbę produktów: "))

    for _ in range(liczba_produktow):
        nazwa, czas_realizacji, poczatkowy_stan_magazynowy, minimalne_zapotrzebowanie, wielkosc_partii, zapotrzebowanie_brutto, komponenty = pobierz_dane_produktu(okresy)
        produkt = Produkt(nazwa, czas_realizacji, poczatkowy_stan_magazynowy, minimalne_zapotrzebowanie, wielkosc_partii)
        produkt.zapotrzebowanie_brutto = zapotrzebowanie_brutto
        for nazwa_komponentu, ilosc in komponenty.items():
            komponent = Produkt(nazwa_komponentu, 1, 0)  # Załóżmy czas realizacji i początkowy stan magazynowy dla komponentów
            mrp.dodaj_produkt(komponent)
            produkt.dodaj_komponent(komponent, ilosc)
        mrp.dodaj_produkt(produkt)

    for nazwa_produktu in mrp.produkty:
        mrp.oblicz_mrp(nazwa_produktu, okresy)

    for nazwa_produktu, produkt in mrp.produkty.items():
        print(f"\nProdukt {nazwa_produktu}")
        print("Zapotrzebowanie netto: ", produkt.zapotrzebowanie_netto)
        print("Zaplanowane zwolnienia zamówienia: ", produkt.zaplanowane_zwolnienia_zamowienia)
        print("Zaplanowane przyjęcia zamówienia: ", produkt.zaplanowane_przyjecia_zamowienia)

if __name__ == "__main__":
    main()
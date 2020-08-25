
class Uporabnik:




class Finance:
    def __init__(self):
        self.stanje = 0
        self.stroski = {}
        self.kategorije = []

    def dodaj_kategorijo(self, kategorija):
        if kategorija in self.kategorije:
            raise ValueError(f'Kategorija {kategorija} že obstaja!')
        else:
            self.kategorije.append(kategorija)

    def dodaj_strosek(self, strosek, kolicina=1, cena, kategorija, datum):
        if type(kolicina) != int:
            raise TypeError('Količina mora biti celo število!')
        skupna_cena = kolicina * cena
        self.stroski[strosek] = [skupna_cena, kategorija, datum]

    def nov_priliv(self, priliv):
        if type(priliv) != float:
            raise TypeError('Vrednost mora biti število!')
        if priliv < 0:
            raise ValueError('Vnesi pozitivno število!')
        self.stanje += priliv





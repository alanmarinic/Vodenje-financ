import datetime



#class Uporabnik:




class Finance:
    def __init__(self):
        self.stanje = 0
        self.stroski = {}
        self.kategorije = []
        self.stanje_graf = {}
        self.stroski_graf = {}

    def dodaj_kategorijo(self, kategorija):
        if kategorija in self.kategorije:
            raise ValueError(f'Kategorija {kategorija} že obstaja!')
        else:
            self.kategorije.append(kategorija)

    def dodaj_strosek(self, strosek, kategorija, cena, datum, kolicina=1):
        if type(kolicina) != int:
            raise TypeError('Količina mora biti celo število!')
        skupna_cena = kolicina * cena
        self.stroski[(strosek, kategorija)] = [skupna_cena, datum]
        self.stanje -= skupna_cena
        self._stroski_graf(datum, skupna_cena)
#dodat kategorijo error ce se ne obstaja

    def _stroski_graf(self, datum, vrednost):
        if datum in self.stroski_graf:
            self.stroski_graf[datum] += vrednost
        else:
            self.stroski_graf[datum] = vrednost

    def nov_priliv(self, priliv, datum):
        if type(priliv) != float:
            raise TypeError('Vrednost mora biti število!')
        if priliv < 0:
            raise ValueError('Vnesi pozitivno število!')
        self.stanje += priliv
        self._stanje_graf(datum, priliv)

    def _stanje_graf(self, datum, priliv):
        if datum in self.stanje_graf:
            self.stanje_graf[datum] += priliv
        else:
            self.stanje_graf[datum] = priliv

#    def odstrani_strosek(self, strosek, kategorija):
#        if (storsek, kategorija) not in self.stroski:
#            raise ValueError(f'Strošek {strosek} ne obstaja!')
#        else:
#            skupna_cena = self.stroski[(strosek, kategorija)][0]
#            self.stanje += skupna_cena
#            del self.stroski[(strosek, kategorija)]

 #   def limit_porabe(self, limit):
 #       omeji stroske ki jih lahko porabis na mesec

    def spodnja_meja_stanja(self, spodnja_meja=0):
        if self.stanje <= spodnja_meja:
#            raise ValueError('Presegli ste spodnjo mejo!')
            pass
        else:
            pass


import datetime
#import matplot.libpyplot as plt
import json


class Uporabnik:
    def __init__(self, uporabnisko_ime, zasifrirano_geslo, osebne_finance):
        self.uporabnisko_ime = uporabnisko_ime
        self.zasifrirano_geslo = zasifrirano_geslo
        self.osebne_finance = osebne_finance

    def preveri_geslo(self, zasifrirano_geslo):
        if self.zasifrirano_geslo != zasifrirano_geslo:
            raise ValueError('Geslo je napačno!')

    def shrani_stanje(self, ime_datoteke):
        slovar_stanja = {
            'uporabnisko_ime': self.uporabnisko_ime,
            'zasifrirano_geslo': self.zasifrirano_geslo,
            'osebne_finance': self.osebne_finance.slovar_s_stanjem(),
        }
        with open(ime_datoteke, 'w') as datoteka:
            json.dump(slovar_stanja, datoteka, ensure_ascii=False, indent=4)

    @classmethod
    def nalozi_stanje(cls, ime_datoteke):
        with open(ime_datoteke) as datoteka:
            slovar_stanja = json.load(datoteka)
        uporabnisko_ime = slovar_stanja['uporabnisko_ime']
        zasifrirano_geslo = slovar_stanja['zasifrirano_geslo']
        osebne_finance = Finance.nalozi_iz_slovarja(slovar_stanja['osebne_finance'])
        return cls(uporabnisko_ime, zasifrirano_geslo, osebne_finance)

class Finance:
    def __init__(self):
        self.stanje = 0
        self.kategorije = []
        self.stroski = {}
        self.stanje_graf = {}
        self.prilivi = {}
        self.stroski_graf = {}
        self.posojeno_drugim = {}
        self.posojeno_meni = {}

    def dodaj_kategorijo(self, naziv):
        if naziv in self.kategorije:
            raise ValueError(f'Kategorija {naziv} že obstaja!')
        else:
            self.kategorije.append(naziv)

    def dodaj_strosek(self, strosek, kategorija, cena, datum, kolicina=1):
        if type(kolicina) != int:
            raise TypeError('Količina mora biti celo število!')
        if kategorija not in self.kategorije:
            self.kategorije.append(kategorija)
        skupna_cena = kolicina * cena
        self.stroski[(strosek, kategorija)] = [skupna_cena, datum]
        self.stanje -= skupna_cena
        self._stroski_graf(datum, skupna_cena)

    def _stroski_graf(self, datum, vrednost):
        if datum in self.stroski_graf:
            self.stroski_graf[datum] += vrednost
        else:
            self.stroski_graf[datum] = vrednost

    def nov_priliv(self, priliv, datum, opis):
        if type(priliv) != float or int:
            raise TypeError('Vrednost mora biti število!')
        if priliv < 0:
            raise ValueError('Vnesi pozitivno število!')
        self.prilivi[(priliv, datum)] = opis
        self.stanje += priliv
        self._stanje_graf(datum, priliv)

    def _stanje_graf(self, datum, priliv):
        if datum in self.stanje_graf:
            self.stanje_graf[datum] += priliv
        else:
            self.stanje_graf[datum] = priliv

    def odstrani_strosek(self, strosek, kategorija):
        if (strosek, kategorija) not in self.stroski:
            raise ValueError(f'Strošek {strosek} ne obstaja!')
        else:
            skupna_cena = self.stroski[(strosek, kategorija)][0]
            self.stanje += skupna_cena
            del self.stroski[(strosek, kategorija)]

#   def limit_porabe(self, limit):
#      omeji stroske ki jih lahko porabis na mesec

    def spodnja_meja_stanja(self, spodnja_meja=0):
        if self.stanje <= spodnja_meja:
            raise ValueError('Presegli ste spodnjo mejo!')
        else:
            pass

    def posodi(self, komu, koliko):
        if komu in self.posojeno_drugim:
            self.posojeno_drugim[komu] += koliko
        self.posojeno_drugim[komu] = koliko
        self.stanje -= koliko
    #v botlu - ce ti posods

    def vrnjeno_meni(self, odkoga, koliko):
        if odkoga not in self.posojeno_drugim:
            raise ValueError('Tej osebi nisi posodil denarja')
        else:
            self.posojeno_drugim[odkoga] -= koliko
            self.stanje += koliko
            if self.posojeno_drugim[odkoga] = 0:
                del self.posojeno_drugim[odkoga]
                #z mihcem sta poravnala stroske juhej!

    def dolg(self, komu, koliko):
        if komu in self.posojeno_meni:
            self.posojeno_meni[komu] += koliko
        self.posojeno_meni[komu] = koliko
        self.stanje += koliko
    #v botlu - ce ti posods

    def poravnaj_dolg(self, odkoga, koliko):
        if odkoga not in self.posojeno_meni:
            raise ValueError(f'{odkoga} ti ni posodil denarja')
        else:
            self.posojeno_meni[odkoga] -= koliko
            self.stanje -= koliko
            if self.posojeno_meni[odkoga] = 0:
                del self.posojeno_meni[odkoga]
                #z mihcem sta poravnala stroske juhej!

#funkcije za shranjevanje in nalaganje obstojecih datotek
    def slovar_s_stanjem(self):
        return {
    #        'stanje' : [{
   #             'stanje' : 
  #          }]
            'kategorije' : [{
                'naziv' : kategorija.naziv,
            } for kategorija in self.kategorije],
            'stroski' : [{
                'strosek' : k[0],
                'kategorija' : k[1],
                'skupna cena' : v[0],
                'datum' : str(v[1]),
            } for k, v in self.stroski.items()],
            'prilivi' : [{
                'priliv' : k[0],
                'datum' : str(k[1]),
                'opis' : v,
            } for k, v in self.prilivi.items()],
            'posojeno drugim' : [{
                'komu' : k,
                'koliko' : v,
            } for k, v in self.posojeno_drugim.items()],
            'posojeno meni' : [{
                'komu' : k,
                'koliko' : v,
            } for k, v in self.posojeno_meni.items()],
        }

    @classmethod
    def nalozi_iz_slovarja(cls, slovar_s_stanjem):
        osebne_finance = cls()
        for kategorija in slovar_s_stanjem['kategorije']:
            nova_kategorija = osebne_finance.dodaj_kategorijo(kategorija['naziv'])
        for strosek in slovar_s_stanjem['stroski']:
            osebne_finance.dodaj_strosek(
                strosek['strosek'],
                strosek['kategorija'],
                strosek['skupna cena'],
                strosek['datum']
            )
        for priliv in slovar_s_stanjem['prilivi']:
            osebne_finance.nov_priliv(
                priliv['priliv'],
                priliv['datum'],
                priliv['opis']
            )
        for posojilo in slovar_s_stanjem['posojeno drugim']:
            osebne_finance.posodi(
                posojilo['komu'],
                posojilo['koliko']
            )
        for dolgovi in slovar_s_stanjem['posojeno meni']:
            osebne_finance.dolg(
                dolgovi['komu'],
                dolgovi['koliko']
            )
        return osebne_finance 

    def shrani_stanje(self, ime_datoteke):
        with open(ime_datoteke, 'w') as datoteka:
            json.dump(self.slovar_s_stanjem(), datoteka, ensure_ascii=False, indent=4)

    @classmethod
    def nalozi_stanje(cls, ime_datoteke):
        with open(ime_datoteke) as datoteka:
            slovar_s_stanjem = json.load(datoteka)
        return cls.nalozi_iz_slovarja(slovar_s_stanjem)
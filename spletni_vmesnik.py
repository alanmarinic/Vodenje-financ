import bottle
import os
import hashlib
import random
from model import Finance, Uporabnik

imenik_s_podatki = 'uporabniki'
uporabniki = {}
skrivnost = 'GESLO'

if not os.path.isdir(imenik_s_podatki):
    os.mkdir(imenik_s_podatki)

for ime_datoteke in os.listdir(imenik_s_podatki):
    uporabnik = Uporabnik.nalozi_stanje(os.path.join(imenik_s_podatki, ime_datoteke))
    uporabniki[uporabnik.uporabnisko_ime] = uporabnik

def trenutni_uporabnik():
    uporabnisko_ime = bottle.request.get_cookie('uporabnisko_ime', secret=skrivnost)
    if uporabnisko_ime is None:
        bottle.redirect('/prijava/')
    return uporabniki[uporabnisko_ime]

def finance_uporabnika():
    return trenutni_uporabnik().osebne_finance

def shrani_trenutnega_uporabnika():
    uporabnik = trenutni_uporabnik()
    uporabnik.shrani_stanje(os.path.join('uporabniki', f'{uporabnik.uporabnisko_ime}.json'))

@bottle.get('/')
def zacetna_stran():
    bottle.redirect('/stroski/')

@bottle.get('/stroski/')
def pregled_spg():
    finance = finance_uporabnika()
    return bottle.template('stroski.html', finance=finance, sporocilo=sporocilo, poraba_kat=poraba_kat)

@bottle.get('/posojila/')
def posojila():
    finance = finance_uporabnika()
    return bottle.template('posojila.html', finance=finance)

@bottle.get('/graf/')
def odpri_graf():
    finance = finance_uporabnika()
    finance.izrisi_graf()
    bottle.redirect('/')

@bottle.get('/pomoc/')
def pomoc():
    finance = finance_uporabnika()
    return bottle.template('pomoc.html', finance=finance)

@bottle.get('/prijava/')
def prijava_get():
    return bottle.template('prijava.html')

@bottle.post('/prijava/')
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode('uporabnisko_ime')
    geslo = bottle.request.forms.getunicode('geslo')
    h = hashlib.blake2b()
    h.update(geslo.encode(encoding='utf-8'))
    zasifrirano_geslo = h.hexdigest()
    if 'nove_finance' in bottle.request.forms and uporabnisko_ime not in uporabniki:
        uporabnik = Uporabnik(
            uporabnisko_ime,
            zasifrirano_geslo,
            Finance()
        )
        uporabniki[uporabnisko_ime] = uporabnik
    else:
        uporabnik = uporabniki[uporabnisko_ime]
        uporabnik.preveri_geslo(zasifrirano_geslo)
    bottle.response.set_cookie('uporabnisko_ime', uporabnik.uporabnisko_ime, path='/', secret=skrivnost)
    bottle.redirect('/')

@bottle.post('/odjava/')
def odjava():
    bottle.response.delete_cookie('uporabnisko_ime', path='/')
    bottle.redirect('/')

@bottle.post('/dodaj-strosek/')
def dodaj_strosek():
    finance = finance_uporabnika()
    strosek = bottle.request.forms.getunicode("strosek")
    kategorija = bottle.request.forms.getunicode("kategorija")
    cena = float(bottle.request.forms["cena"])
    kolicina = int(bottle.request.forms["kolicina"])
    datum = bottle.request.forms["datum"]
    finance.dodaj_strosek(strosek, kategorija, cena, datum, kolicina)
    shrani_trenutnega_uporabnika()
    bottle.redirect('/')

@bottle.post('/dodaj-dohodek/')
def dodaj_dohodek():
    finance = finance_uporabnika()
    dohodek = float(bottle.request.forms["dohodek"])
    datum = bottle.request.forms["datum"]
    opis = bottle.request.forms.getunicode("opis")
    finance.nov_priliv(dohodek, datum, opis)
    shrani_trenutnega_uporabnika()
    bottle.redirect('/')

@bottle.post('/poraba-kategorija/')
def poraba_kategorija():
    finance = finance_uporabnika()
    global poraba_kat, sporocilo
    kategorija = bottle.request.forms.getunicode("kategorija")
    poraba_kat = True
    kategorija_st = finance.poraba_na_kategorijo(kategorija)
    sporocilo = "V kategoriji {} ste porabili {} €".format(kategorija, str(round(kategorija_st, 2)))
    bottle.redirect('/stroski/')

@bottle.post('/posodi-denar/')
def posodi():
    finance = finance_uporabnika()
    komu = bottle.request.forms.getunicode("komu")
    datum = bottle.request.forms["datum"]
    koliko = float(bottle.request.forms["koliko"])
    finance.posodi(komu, datum, koliko)
    shrani_trenutnega_uporabnika()
    bottle.redirect('/posojila/')

@bottle.post('/izposodi-denar/')
def izposodi():
    finance = finance_uporabnika()
    odkoga = bottle.request.forms.getunicode("odkoga")
    datum = bottle.request.forms["datum"]
    koliko = float(bottle.request.forms["koliko"])
    finance.dolg(odkoga, datum, koliko)
    shrani_trenutnega_uporabnika()
    bottle.redirect('/posojila/')

@bottle.post('/vrnjeno-meni/')
def vrnjeno_meni():
    finance = finance_uporabnika()
    odkoga = bottle.request.forms.getunicode("odkoga")
    koliko = float(bottle.request.forms["koliko"])
    datum = bottle.request.forms["datum"]
    finance.vrnjeno_meni(odkoga, koliko, datum)
    shrani_trenutnega_uporabnika()
    bottle.redirect('/posojila/')

@bottle.post('/vrnjeno-ostalim/')
def vrnjeno_ostalim():
    finance = finance_uporabnika()
    odkoga = bottle.request.forms.getunicode("odkoga")
    datum = bottle.request.forms["datum"]
    koliko = float(bottle.request.forms["koliko"])
    finance.poravnaj_dolg(odkoga, koliko, datum)
    shrani_trenutnega_uporabnika()
    bottle.redirect('/posojila/')

sporocilo = ""
poraba_kat = False

bottle.run(debug=True, reloader=True)
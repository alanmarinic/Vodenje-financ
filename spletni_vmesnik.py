import bottle
from model import Finance

DATOTEKA_S_STANJEM = 'stanje.json'
try:
    finance = Finance.nalozi_stanje(DATOTEKA_S_STANJEM)
except:
    finance = Finance()

@bottle.get('/')
def zacetna_stran():
    return bottle.template('zacetna_stran.html', finance=finance)

@bottle.get('/odpri-graf/')
def odpri_graf():
    finance.izrisi_graf()
    bottle.redirect('/')

@bottle.post('/dodaj_strosek/')
def dodaj_strosek():
    strosek = bottle.request.forms.getunicode("strosek")
    kategorija = bottle.request.forms.getunicode("kategorija")
    cena = float(bottle.request.forms["cena"])
    kolicina = int(bottle.request.forms["kolicina"])
    datum = bottle.request.forms["datum"]
    finance.dodaj_strosek(strosek, kategorija, cena, datum, kolicina=1)
    bottle.redirect('/')

@bottle.post('/dodaj_dohodek/')
def dodaj_dohodek():
    dohodek = float(bottle.request.forms["dohodek"])
    datum = bottle.request.forms["datum"]
    opis = bottle.request.forms.getunicode("opis")
    finance.nov_priliv(dohodek, datum, opis)
    bottle.redirect('/')

@bottle.post('/posodi_denar/')
def posodi():
    komu = bottle.request.forms.getunicode("komu")
    datum = bottle.request.forms["datum"]
    koliko = float(bottle.request.forms["koliko"])
    finance.posodi(komu, datum, koliko)
    bottle.redirect('/')

@bottle.post('/izposodi_denar/')
def izposodi():
    odkoga = bottle.request.forms.getunicode("odkoga")
    datum = bottle.request.forms["datum"]
    koliko = float(bottle.request.forms["koliko"])
    finance.dolg(odkoga, datum, koliko)
    bottle.redirect('/')

@bottle.post('/vrnjeno_meni/')
def vrnjeno_meni():
    odkoga = bottle.request.forms.getunicode("odkoga")
    datum = bottle.request.forms["datum"]
    koliko = float(bottle.request.forms["koliko"])
    finance.vrnjeno_meni(odkoga, koliko, datum)
    bottle.redirect('/')

@bottle.post('/vrnjeno_ostalim/')
def vrnjeno_ostalim():
    odkoga = bottle.request.forms.getunicode("odkoga")
    datum = bottle.request.forms["datum"]
    koliko = float(bottle.request.forms["koliko"])
    finance.poravnaj_dolg(odkoga, koliko, datum)
    bottle.redirect('/')

bottle.run(debug=True, reloader=True)
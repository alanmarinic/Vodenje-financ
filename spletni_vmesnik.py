import bottle
from model import Finance

DATOTEKA_S_STANJEM = 'stanje.json'
try:
    finance = Finance.nalozi_stanje(DATOTEKA_S_STANJEM)
except:
    finance = Finance()

@bottle.get('/')
def zacetna_stran():
    bottle.redirect('/stroski/')

@bottle.get('/stroski/')
def pregled_spg():
    return bottle.template('stroski.html', finance=finance)

@bottle.get('/posojila/')
def posojila():
    return bottle.template('posojila.html', finance=finance)

@bottle.get('/pomoc/')
def pomoc():
    return bottle.template('pomoc.html')

@bottle.post('/dodaj-strosek/')
def dodaj_strosek():
    strosek = bottle.request.forms.getunicode("strosek")
    kategorija = bottle.request.forms.getunicode("kategorija")
    cena = float(bottle.request.forms["cena"])
    kolicina = int(bottle.request.forms["kolicina"])
    datum = bottle.request.forms["datum"]
    finance.dodaj_strosek(strosek, kategorija, cena, datum, kolicina=1)
    bottle.redirect('/')

@bottle.post('/dodaj-dohodek/')
def dodaj_dohodek():
    dohodek = float(bottle.request.forms["dohodek"])
    datum = bottle.request.forms["datum"]
    opis = bottle.request.forms.getunicode("opis")
    finance.nov_priliv(dohodek, datum, opis)
    bottle.redirect('/')

@bottle.post('/posodi-denar/')
def posodi():
    komu = bottle.request.forms.getunicode("komu")
    datum = bottle.request.forms["datum"]
    koliko = float(bottle.request.forms["koliko"])
    finance.posodi(komu, datum, koliko)
    bottle.redirect('/posojila/')

@bottle.post('/izposodi-denar/')
def izposodi():
    odkoga = bottle.request.forms.getunicode("odkoga")
    datum = bottle.request.forms["datum"]
    koliko = float(bottle.request.forms["koliko"])
    finance.dolg(odkoga, datum, koliko)
    bottle.redirect('/posojila/')

@bottle.post('/vrnjeno-meni/')
def vrnjeno_meni():
    odkoga = bottle.request.forms.getunicode("odkoga")
    datum = bottle.request.forms["datum"]
    koliko = float(bottle.request.forms["koliko"])
    finance.vrnjeno_meni(odkoga, koliko, datum)
    bottle.redirect('/posojila/')

@bottle.post('/vrnjeno-ostalim/')
def vrnjeno_ostalim():
    odkoga = bottle.request.forms.getunicode("odkoga")
    datum = bottle.request.forms["datum"]
    koliko = float(bottle.request.forms["koliko"])
    finance.poravnaj_dolg(odkoga, koliko, datum)
    bottle.redirect('/posojila/')

@bottle.get('/odpri-graf/')
def odpri_graf():
    finance.izrisi_graf()
    bottle.redirect('/')

bottle.run(debug=True, reloader=True)
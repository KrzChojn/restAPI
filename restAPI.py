# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 18:51:44 2021

@author: krzys
"""

import requests as rq
import json
from flask import Flask, request, redirect, url_for, render_template

app = Flask (__name__)

dane = rq.get('https://www.googleapis.com/books/v1/volumes?q=hobbit')
daneText = dane.text
daneTextJSON = json.loads(daneText)

#w tym bloku pozyskuję rok publikacji oraz tytuł dla dane. 
#Dodatkowo robię z tego slownik oraz posortowana po latach liste
iloscPozycji = len (daneTextJSON['items'])
lista_lat = []
lista_tytulow = []
lista_autorow = []
lista_id = []
lista_kategorii = []
lista_srednich_ocen = []
lista_ilosci_ocen = []
lista_thumbnail = []

slownik = {}
slownik_autor_tytul = {}
slownikIdTitle = {}
slownikIdAuthors = {}
slownikIdPublished = {}
slownikIdCategories = {}
slownikIdAvgRat = {}
slownikIdRatCt = {}
slownikIdThumb = {}


#lista tytulow i lista lat+
for i in range (iloscPozycji):
    lista_tytulow.append(daneTextJSON['items'][i]['volumeInfo']['title'])
    lista_lat.append(daneTextJSON['items'][i]['volumeInfo']['publishedDate']\
                     [:4])

#lista tytulow unikalna+
lista_tytulow_unikalna = set(lista_tytulow)

#slownik rok:tytul+
for i in range(iloscPozycji):
    try:
        slownik[lista_lat[i]]
        slownik[lista_lat[i]] = slownik[lista_lat[i]] + ' / ' + lista_tytulow\
            [i]
    except KeyError:
        slownik[lista_lat[i]] = lista_tytulow[i]
        
#lista tytulow posortowana wg dat publikacji+
tytulySorted = sorted(slownik.items())

#lista autorow+
for i in range (iloscPozycji):
    try:
        a = daneTextJSON['items'][i]['volumeInfo']['authors']
        b = str(a)
        b = b.replace('[', '')
        b = b.replace(']', '')
        b = b.replace("'",'"')
        lista_autorow.append(b)
    except KeyError:
        lista_autorow.append("Brak info")
        
#slownik autor:tytul+
for i in range(iloscPozycji):
    try:
        slownik_autor_tytul[str(lista_autorow[i])]
        slownik_autor_tytul[str(lista_autorow[i])] = slownik_autor_tytul\
            [str(lista_autorow[i])] + ' / ' + lista_tytulow[i]
    except KeyError:
        slownik_autor_tytul[str(lista_autorow[i])] = lista_tytulow[i]

#reszta list potrzebna do stworzenia slownikow
for i in range(iloscPozycji):
    lista_id.append(daneTextJSON['items'][i]['id'])
    try:
        lista_kategorii.append(str(daneTextJSON['items'][i]['volumeInfo']\
                               ['categories']))
    except KeyError:
        lista_kategorii.append("Brak info")
    try:
        lista_srednich_ocen.append(str(daneTextJSON['items'][i]['volumeInfo']\
                                   ['averageRating']))
    except KeyError:
        lista_srednich_ocen.append("Brak info")
    try:
        lista_ilosci_ocen.append(str(daneTextJSON['items'][i]['volumeInfo']\
                                 ['ratingsCount']))
    except KeyError:
        lista_ilosci_ocen.append("Brak info")
    try:
        lista_thumbnail.append(daneTextJSON['items'][i]['volumeInfo']\
                               ['imageLinks']['thumbnail'])
    except KeyError:
        lista_thumbnail.append("Brak info")


#slownik id:title+
for i in range(iloscPozycji):
    try:
        slownikIdTitle[lista_id[i]]
        slownikIdTitle[lista_id[i]] = slownikIdTitle[lista_id[i]] +\
            ' / ' + lista_tytulow[i]
    except KeyError:
        slownikIdTitle[lista_id[i]] = lista_tytulow[i]

#slownik id:authors+
for i in range(iloscPozycji):
    try:
        slownikIdAuthors[lista_id[i]]
        slownikIdAuthors[lista_id[i]] = slownikIdAuthors[lista_id[i]] +\
            ' / ' + lista_autorow[i]
    except KeyError:
        slownikIdAuthors[lista_id[i]] = lista_autorow[i]

#slownik id:published+
for i in range(iloscPozycji):
    try:
        slownikIdPublished[lista_id[i]]
        slownikIdPublished[lista_id[i]] = slownikIdPublished[lista_id[i]] + \
            ' / ' + lista_lat\
            [i]
    except KeyError:
        slownikIdPublished[lista_id[i]] = lista_lat[i]

#slownik id:categories+
for i in range(iloscPozycji):
    try:
        slownikIdCategories[lista_id[i]]
        slownikIdCategories[lista_id[i]] = slownikIdCategories[lista_id[i]] + \
            ' / ' + lista_kategorii\
            [i]
    except KeyError:
        slownikIdCategories[lista_id[i]] = lista_kategorii[i]
        
#slownik id:srednia_ocena+
for i in range(iloscPozycji):
    try:
        slownikIdAvgRat[lista_id[i]]
        slownikIdAvgRat[lista_id[i]] = slownikIdAvgRat[lista_id[i]] + \
            ' / ' + lista_srednich_ocen[i]
    except KeyError:
        slownikIdAvgRat[lista_id[i]] = lista_srednich_ocen[i]

#slownik id:ilosc_ocen+
for i in range(iloscPozycji):
    try:
        slownikIdRatCt[lista_id[i]]
        slownikIdRatCt[lista_id[i]] = slownikIdRatCt[lista_id[i]] + \
            ' / ' + lista_ilosci_ocen[i]
    except KeyError:
        slownikIdRatCt[lista_id[i]] = lista_ilosci_ocen[i]

#slownik id:thumbnail+
for i in range(iloscPozycji):
    try:
        slownikIdThumb[lista_id[i]]
        slownikIdThumb[lista_id[i]] = slownikIdThumb[lista_id[i]] + \
            ' / ' + lista_thumbnail[i]
    except KeyError:
        slownikIdThumb[lista_id[i]] = lista_thumbnail[i]

#routingi do wyswietlania danych na bazie wprowadzonego adresu url
@app.route('/')
def wyswietl_metody():
    return render_template("powitalna.html", slownikIdTitle = slownikIdTitle)
                                                                                                        
#dostępne pod adresem:
#http://127.0.0.1:1234/books
@app.route('/books')
def wyswietl_ksiazki():
    return render_template("books.html", lista_tytulow_unikalna=lista_tytulow_unikalna)

#dostępne pod adresem:
#http://127.0.0.1:1234/books/sorted?sort=-published_date
@app.route('/books/sorted')
def wyswietl_sortowanie():
    sortowanie = request.args.get("sort", None)
    if sortowanie == "-published_date":
        return render_template("published_date.html", tytulySorted = tytulySorted)

#dostępne pod adresem:
#http://127.0.0.1:1234/books/year?published_date=1985
@app.route('/books/year')
def wyswietl_po_latach():
    rok_ksiazek = request.args.get("published_date", None)
    try:
        if rok_ksiazek == None:
            return "Nie podano roku, lista wszystkich ksiazek: " + str\
                (lista_tytulow_unikalna)
        else:
            return str(slownik[str(rok_ksiazek)])
    except KeyError:
        return "Nie ma ksiazek wydanych w tym roku"

#dostępne pod adresem:
#http://127.0.0.1:1234/books/author?author="autor"
@app.route('/books/author')
def autor():
    autor = request.args.get("author", None)
    if autor not in lista_autorow:
        return "Brak takiego autora"
    else:
        return slownik_autor_tytul[autor]   

#dostępne pod adresem:
#http://127.0.0.1:1234/books/8ef3-s6fixIC
@app.route('/books/<string:a>')
def dane_id(a):
    return 'title: ' + str(slownikIdTitle[a]) + \
        '<p>authors: ' + str(slownikIdAuthors[a]) + '</p>' \
            '<p>published date: ' + str(slownikIdPublished[a]) + '</p>' \
                '<p>categories: ' + str(slownikIdCategories[a]) + '</p>' \
                    '<p>average rating: ' + str(slownikIdAvgRat[a]) + '</p>' \
                        '<p>ratings_count: ' + str(slownikIdRatCt[a]) + '</p>' \
                            '<p>thumbnail: ' + str(slownikIdThumb[a]) + '</p>'

#metoda POST do wprowadzenia linku, od razu przekierowuje do update'a            
@app.route ('/wgraj', methods = ['POST', 'GET'])
def form_example():
    if request.method == 'POST':
        global link
        link = request.form.get('link')
        return redirect(url_for('update'))
    return '''
    <form method="POST">
        <div><label>Podaj link: <input type="text" name="link"></label></div>
        <input type="submit" value="Submit">
    </form>'''

@app.route('/update')
def update():
    global daneTextJSON2, iloscPozycji2, lista_tytulow_unikalna,tytulySorted,\
        lista_autorow, iloscPozycji3, tytulySorted
    try:
        daneTextJSON2 = json.loads(rq.get(link).text)
    except:
        return "Zły format. Spróbuj jeszcze raz"
    iloscPozycji2 = len (daneTextJSON2['items'])
    for i in range (iloscPozycji2):
        lista_tytulow.append(daneTextJSON2['items'][i]['volumeInfo']['title'])
        lista_lat.append(daneTextJSON2['items'][i]['volumeInfo']['publishedDate']\
                         [:4])
    lista_tytulow_unikalna = set(lista_tytulow)
    for i in range (iloscPozycji2):
        try:
            a = daneTextJSON2['items'][i]['volumeInfo']['authors']
            b = str(a)
            b = b.replace('[', '')
            b = b.replace(']', '')
            b = b.replace("'",'"')
            lista_autorow.append(b)
        except KeyError:
            lista_autorow.append("Brak info")
    for i in range(iloscPozycji2):
        lista_id.append(daneTextJSON2['items'][i]['id'])
        try:
            lista_kategorii.append(str(daneTextJSON2['items'][i]['volumeInfo']\
                                    ['categories']))
        except KeyError:
            lista_kategorii.append("Brak info")
        try:
            lista_srednich_ocen.append(str(daneTextJSON2['items'][i]['volumeInfo']\
                                        ['averageRating']))
        except KeyError:
            lista_srednich_ocen.append("Brak info")
        try:
            lista_ilosci_ocen.append(str(daneTextJSON2['items'][i]['volumeInfo']\
                                      ['ratingsCount']))
        except KeyError:
            lista_ilosci_ocen.append("Brak info")
        try:
            lista_thumbnail.append(daneTextJSON2['items'][i]['volumeInfo']\
                                    ['imageLinks']['thumbnail'])
        except KeyError:
            lista_thumbnail.append("Brak info")
    
    iloscPozycji3 = len (daneTextJSON['items']) + len (daneTextJSON2['items'])

    for i in range(iloscPozycji3):
        try:
            if lista_tytulow[i] in slownik[lista_lat[i]]:
                pass
            else:
                slownik[lista_lat[i]] = slownik[lista_lat[i]] + ' / ' + \
                    lista_tytulow[i]
        except KeyError:
            slownik[lista_lat[i]] = lista_tytulow[i]
    
    tytulySorted = sorted(slownik.items())
    
    for i in range(iloscPozycji3):
        try:
            if slownik_autor_tytul[str(lista_autorow[i])] in lista_tytulow[i]:
                pass
            else:
                slownik_autor_tytul[str(lista_autorow[i])]
                slownik_autor_tytul[str(lista_autorow[i])] = slownik_autor_tytul\
                    [str(lista_autorow[i])] + ' / ' + lista_tytulow[i]
        except KeyError:
            slownik_autor_tytul[str(lista_autorow[i])] = lista_tytulow[i]
            
    #slownik id:title
    for i in range(iloscPozycji3):
        try:
            if slownikIdTitle[lista_id[i]] in lista_tytulow[i]:
                pass
            else:
                slownikIdTitle[lista_id[i]]
                slownikIdTitle[lista_id[i]] = slownikIdTitle[lista_id[i]] +\
                    ' / ' + lista_tytulow[i]
        except KeyError:
            slownikIdTitle[lista_id[i]] = lista_tytulow[i]
    
    #slownik id:authors
    for i in range(iloscPozycji3):
        try:
            if slownikIdAuthors[lista_id[i]] in lista_autorow[i]:
                pass
            else:
                slownikIdAuthors[lista_id[i]]
                slownikIdAuthors[lista_id[i]] = slownikIdAuthors[lista_id[i]] +\
                    ' / ' + lista_autorow[i]
        except KeyError:
            slownikIdAuthors[lista_id[i]] = lista_autorow[i]
    
    #slownik id:published
    for i in range(iloscPozycji3):
        try:
            if slownikIdPublished[lista_id[i]] in lista_lat[i]:
                pass
            else:
                slownikIdPublished[lista_id[i]]
                slownikIdPublished[lista_id[i]] = slownikIdPublished[lista_id[i]] \
                    + ' / ' + lista_lat[i]
        except KeyError:
            slownikIdPublished[lista_id[i]] = lista_lat[i]

    #slownik id:categories    
    for i in range(iloscPozycji3):
        try:
            if slownikIdCategories[lista_id[i]] in lista_kategorii[i]:
                pass
            else:
                slownikIdCategories[lista_id[i]]
                slownikIdCategories[lista_id[i]] = slownikIdCategories[lista_id[i]] \
                    + ' / ' + lista_kategorii[i]
        except KeyError:
            slownikIdCategories[lista_id[i]] = lista_kategorii[i]

    #slownik id:srednia_ocena
    for i in range(iloscPozycji3):
        try:
            if slownikIdAvgRat[lista_id[i]] in lista_srednich_ocen[i]:
                pass
            else:
                slownikIdAvgRat[lista_id[i]]
                slownikIdAvgRat[lista_id[i]] = slownikIdAvgRat[lista_id[i]] + \
                    ' / ' + lista_srednich_ocen[i]
        except KeyError:
            slownikIdAvgRat[lista_id[i]] = lista_srednich_ocen[i]
    
    #slownik id:ilosc_ocen
    for i in range(iloscPozycji3):
        try:
            if slownikIdRatCt[lista_id[i]] in lista_ilosci_ocen[i]:
                pass
            else:
                slownikIdRatCt[lista_id[i]]
                slownikIdRatCt[lista_id[i]] = slownikIdRatCt[lista_id[i]] + \
                    ' / ' + lista_ilosci_ocen[i]
        except KeyError:
            slownikIdRatCt[lista_id[i]] = lista_ilosci_ocen[i]
    
    #slownik id:thumbnail
    for i in range(iloscPozycji3):
        try:
            if slownikIdThumb[lista_id[i]] in lista_thumbnail[i]:
                pass
            else:
                slownikIdThumb[lista_id[i]]
                slownikIdThumb[lista_id[i]] = slownikIdThumb[lista_id[i]] + \
                    ' / ' + lista_thumbnail[i]
        except KeyError:
            slownikIdThumb[lista_id[i]] = lista_thumbnail[i]
        
    return "Dane zostaly zaktualizowane"

if __name__ == "__main__":
    app.run(debug = False, port = 1234)

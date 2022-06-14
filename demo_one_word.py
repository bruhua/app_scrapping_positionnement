import streamlit as st
import os
import re
import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from time import sleep
from urllib.parse import urlparse

# Creation de la fonction pour aller chercher des urls
@st.cache
def Find_url(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)
    return [x[0] for x in url]

def nom_domaine (string):
    domaine = urlparse(string)[1]
    return domaine


def app():
    st.title("Positionnement des concurrents via l'utilisation du webscrapping")
    st.write("")
    st.subheader("Connaitre la position sur Google de la concurrence")

    st.write("Cet outil permet de connaitre le positionnement de vos concurrents. "
             "Entrez un terme de recherche dans le champs ci-dessous : ")

    name = st.text_input("Mot à rechercher :", "")

    if (st.button('Rechercher')) :

        driver = webdriver.Chrome(ChromeDriverManager().install())  # Creation drive
        sleep(1)

        driver.get('https://www.google.com/')  # ouverture google
        driver.find_element_by_id('L2AGLb').click()  # acceptation cookie

        sleep(1)
        barre =driver.find_element_by_name('q')  # Aller chercher la barre de recherche
        barre.clear()
        barre.send_keys(name)    # Entrer le mot qu'on souhaite chercher
        barre.send_keys(Keys.ENTER)  # Cliquer
        info_box = driver.find_element_by_id('tvcap').text    # Aller prendre le texte present dans l'id tvcap (sea)
        info_box2 = driver.find_element_by_id('search').text    # search / seo
        # info_box2= remplace(info_box)
        url = Find_url(info_box)   # Recherche des urls avec la fonction find
        liste_domaine_sea = []
        for element in url:
            domaine_sea = nom_domaine(element)
            liste_domaine_sea.append(domaine_sea)
        url2 = Find_url(info_box2)

        liste_domaine_seo = []
        for element in url2:
            domaine_seo = nom_domaine(element)
            liste_domaine_seo.append(domaine_seo)

        ## Partie resultat


        st.markdown('Les résultats de la recherche pour la partie SEA (annonces Google) :')
        if len(url) ==0 :
            st.write("Pas de concurrent actuellement positionné sur le référencement payant")
        else :
            for element in range(len(liste_domaine_sea)) :
                st.write("Concurrent n°:",element+1 ,liste_domaine_sea[element])

        st.write("")
        st.write("")
        st.markdown('Les résultats de la recherche pour le SEO :')
        if len(url2) ==0 :
            st.write("Pas de concurrent actuellement positionné en SEO")
        else :
            for element in range(len(liste_domaine_seo)) :
                st.write("Concurrent n°:",element+1 ,liste_domaine_seo[element])


        st.write("")
        st.write("")
        st.subheader("Ok et alors ?")
        st.write("")
        st.write("A ce stade, l'outil a été chercher les positions des différentes marques qui sont référencées ou qui paient "
                 "pour être affichées sur le terme de recherche que vous avez choisi.")
        st.write("On aurait très bien pu chercher nous même sur Google les résultats qui s'affichent.")
        st.write("Là où l'outil va se révéler plus efficace c'est si l'on veut connaitre le positionnement des concurrents sur "
                 "plusieurs mots clés. Plutôt que d'entrer chaque mot clé à la main dans la barre de recherche Google, l'outil va le faire "
                 "à notre place.")
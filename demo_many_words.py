import streamlit as st
import os
import re
import pandas as pd
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
    st.title("Mise en application sur plusieurs termes de recherche")

    mot1 = st.text_input("1ere recherche:", "")
    mot2 = st.text_input("2e recherche :", "")
    mot3 = st.text_input("3e recherche :", "")

    liste_mots=[mot1,mot2,mot3]
    # Creation d'un dataframe
    df_sea=pd.DataFrame()
    df_seo=pd.DataFrame()

    if (st.button('Go')) :
        driver = webdriver.Chrome(ChromeDriverManager().install())  # Creation drive
        driver.get('https://www.google.com/')  # ouverture google
        driver.find_element_by_id('L2AGLb').click()  # acceptation cookie

        for element in liste_mots :
            sleep(1)

            df_sea_temp = pd.DataFrame()
            df_seo_temp = pd.DataFrame()

            sleep(1)
            barre =driver.find_element_by_name('q')  # Aller chercher la barre de recherche
            barre.clear()
            barre.send_keys(element)    # Entrer le mot qu'on souhaite chercher
            barre.send_keys(Keys.ENTER)  # Cliquer
            info_box_sea = driver.find_element_by_id('tvcap').text    # Aller prendre le texte present dans l'id tvcap (sea)
            info_box_seo = driver.find_element_by_id('search').text    # search / seo

            url_sea = Find_url(info_box_sea)   # Recherche des urls avec la fonction find
            url_seo = Find_url(info_box_seo)

            liste_domaine_sea = []
            for url_long_sea in url_sea:
                domaine_sea = nom_domaine(url_long_sea)
                liste_domaine_sea.append(domaine_sea)

            liste_domaine_seo = []
            for url_long_seo in url_seo:
                domaine_seo = nom_domaine(url_long_seo)
                liste_domaine_seo.append(domaine_seo)

            df_sea_temp[element]=liste_domaine_sea
            df_seo_temp[element] = liste_domaine_seo

            df_sea = pd.concat([df_sea, df_sea_temp], axis=1)
            df_seo = pd.concat([df_seo, df_seo_temp], axis=1)


        ## Partie resultat
        # SEA
        # Mise en forme du df
        df_sea = df_sea.fillna('Pas de résultat')
        df_sea.insert(0, "Positionnement", range(len(df_sea)), allow_duplicates=True)
        df_sea['Positionnement'] = df_sea['Positionnement'] + 1

        st.write("")
        st.title("Résultats pour la partie SEA")
        st.write("")
        st.write("Voici les résultats obtenus en fonction des termes de recherches utilisés précédemment :")
        st.write(df_sea)

        df_cumul_sea = pd.DataFrame()
        for element in liste_mots:
            df_cumul_sea = pd.concat([df_cumul_sea, df_sea[element]], axis=0)
        df_cumul_sea = df_cumul_sea[df_cumul_sea[0] != 'Pas de résultat']
        st.subheader("TOP 3 des marques les plus positionnées :")
        for element in range(len(df_cumul_sea.value_counts().head(3))):
            st.write("Site ou Marque n° ", element + 1, df_cumul_sea.value_counts().index.tolist()[element])
            st.write("Cette marque est positionnée ", df_cumul_sea.value_counts()[element], "fois.")

        st.write("")
        st.write("")

        # SEO
        # Mise en forme du df
        df_seo = df_seo.fillna('Pas de résultat')
        df_seo.insert(0, "Positionnement", range(len(df_seo)), allow_duplicates=True)
        df_seo['Positionnement'] = df_seo['Positionnement'] + 1

        st.write("")
        st.title("Résultats pour la partie SEO")
        st.write("")
        st.write("Voici les résultats obtenus en fonction des termes de recherches utilisés précédemment :")
        st.write(df_seo)

        df_cumul_seo = pd.DataFrame()
        for element in liste_mots:
            df_cumul_seo = pd.concat([df_cumul_seo, df_seo[element]], axis=0)
        df_cumul_seo = df_cumul_seo[df_cumul_seo[0] != 'Pas de résultat']
        st.subheader("TOP 3 des marques les plus positionnées :")
        for element in range(len(df_cumul_seo.value_counts().head(3))):
            st.write("Site ou Marque n° ", element + 1, df_cumul_seo.value_counts().index.tolist()[element])
            st.write("Cette marque est positionnée ", df_cumul_seo.value_counts()[element], "fois.")
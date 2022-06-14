import streamlit as st
import os
import re
import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from time import sleep

import demo_one_word
import demo_many_words

# Variables globales
PAGES = {
    "Introduction": demo_one_word,
    "Mise en application ": demo_many_words

}


# Variables globales

st.sidebar.title("Application webscrapping - positionnement ")

# Choix de la page
selection = st.sidebar.radio("Menu", (list(PAGES.keys())),  key=range(0,2))
page = PAGES[selection]
page.app()

st.sidebar.markdown("""<hr style="height:2px;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
st.sidebar.markdown("Auteur :")
st.sidebar.markdown("[Bruno Huart](https://www.linkedin.com/in/bruno-huart-051459107/) ")
st.sidebar.markdown("""<hr style="height:2px;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)

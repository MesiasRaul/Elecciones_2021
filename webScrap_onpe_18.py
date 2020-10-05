#!/usr/bin/env python
# coding: utf-8

# In[185]:


# Objetivo 1: Web Scraping a la página de la ONPE #
# Objetivo 2: Obtener información de las elecciones municipales del 2018 #

from selenium import webdriver
import os
import pandas as pd

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


chromedriver = "C:/Users/ASUS/Desktop/PC/2.Estudio/10. Web_Scraping/ChromeDriver_85/chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(executable_path=chromedriver)
url="http://resultadoshistorico.onpe.gob.pe/PRERM2018/Actas/Numero"
driver.get(url)


# Se genera la lista de mesas del distrito correspondiente

lista_mesas = '0236'
part_21 = range(4,18) # el límite extremo es más 1

part_2 = []
for q in range(0,len(part_21)) :
    if len(str(part_21[q])) == 1 :
        a = '0' + str(part_21[q])
        part_2.append(a)
    elif len(str(part_21[q])) == 2 :
        a = str(part_21[q])
        part_2.append(a)

lista_mesas = [lista_mesas + part_2[q] for q in range(0,len(part_2))]

resultado = []

for k in range(0,len(lista_mesas)):

    num_acta = driver.find_element_by_name("numeroActaForm")
    num_acta.clear() # Se limpia, para que que el bucle continúe.
    num_acta.send_keys(lista_mesas[k])

    buscar_btn = driver.find_element_by_class_name("btn_buscar")
    buscar_btn.click()
    time.sleep(4) # necesario para que las tablas aparezcan
    
    municipal_btn = driver.find_element_by_xpath('//*[@id="pdf"]/div[3]/div[1]/ul/li[2]/a')
    municipal_btn.click()
    time.sleep(4) # necesario para que las tablas aparezcan

    tabla = driver.find_element_by_xpath('//*[@id="pdf"]/div[5]/div/div/table')
    filas = tabla.find_elements_by_css_selector("tr")
    
    lista_temp = []
        
    for i in range(1,len(filas)) :
        columnas = filas[i].find_elements_by_css_selector("td")
        columnas = [columnas[q].text for q in range(0,len(columnas))] # No desde 0, porque la primera columna está vacía.
        lista_temp.append(columnas)
    
    lista_temp = pd.DataFrame(lista_temp, columns = ['A','B','C','D'])
    lista_temp["columna_name"] = lista_mesas[k]

    resultado.append(lista_temp)

    
resultado2 = resultado[0]

for j in range(1,len(resultado)):
    resultado2 = resultado2.append(resultado[j])

resultado2.to_excel("C:/Users/ASUS/Desktop/PC/9.Proyectos/1.analitica_elecciones_2021/1.insumos/resultado_2018_distrito.xlsx")

driver.close()


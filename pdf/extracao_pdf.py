#!/usr/bin/python
# -*- coding: UTF-8 -*-
# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252


#------------------------------------------------------------------
#	Recuperação de informações de Normas do CMN e do BC 
#	
#------------------------------------------------------------------


#------------------------------------------------------------------
# Inserir o nome do arquivo aqui!
# Obs: O arquivo deverá estar na mesma pasta da script
file_csv = 'saida_normas_completo_novo.csv'
#------------------------------------------------------------------

#------------------------------------------------------------------
# Bibliotecas
# Manipulação das funções de tempo
import time

# Importando a biblioteca de expressões regulares
import re

# Manipulação dos sites SELENIUM (instalar o firefox no PC)
from selenium import webdriver

# Sistema operacional 
import os

# Trabalhar com datas
from datetime import date

# Gerar csv
import csv

# Manipulação e parsing de html
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

# Manipulação e parsing html usando Beautiful Soup
from bs4 import BeautifulSoup


#-------------------------------------------------------------------------
def ajustaArray(string):
	#string = string.replace("\xba", "")
	string = string.replace("\xc0", "")
        string = string.replace("\xc1", "")
        string = string.replace("\xc2", "")
        string = string.replace("\xc3", "")
        string = string.replace("\xc4", "")
        string = string.replace("\xc7", "C")
        string = string.replace("\xe7", "c")
        string = string.replace("\xc8", "E")
        string = string.replace("\xc9", "E")
        string = string.replace("\xc1", "E")
        string = string.replace("\xc8", "E")
        string = string.replace("\xcc", "I")
        string = string.replace("\xcd", "I")
        string = string.replace("\xce", "I")
        string = string.replace("\xcf", "I")
        string = string.replace("\xd2", "O")
        string = string.replace("\xd3", "O")
        string = string.replace("\xd4", "O")
        string = string.replace("\xd5", "O")
        string = string.replace("\xd6", "O")
        string = string.replace("\xd9", "U")
        string = string.replace("\xda", "U")
        string = string.replace("\xdb", "U")
        string = string.replace("\xdc", "U")
        string = string.replace("\xe0", "a")
        string = string.replace("\xe1", "a")
        string = string.replace("\xe2", "a")
        string = string.replace("\xe3", "a")
        string = string.replace("\xe4", "a")
        string = string.replace("\xe5", "a")
        string = string.replace("\xe8", "e")
        string = string.replace("\xe9", "e")
        string = string.replace("\xea", "e")
        string = string.replace("\xeb", "e")
        string = string.replace("\xec", "i")
        string = string.replace("\xed", "i")
        string = string.replace("\xee", "i")
        string = string.replace("\xef", "i")
        string = string.replace("\xf2", "o")
        string = string.replace("\xf3", "o")
        string = string.replace("\xf4", "o")
        string = string.replace("\xf5", "o")
        string = string.replace("\xf9", "u")
        string = string.replace("\xfa", "u")
        string = string.replace("\xfb", "u")
        string = string.replace("\xfc", "u")
        string = string.replace("\xaa", "un ")
        string = string.replace("\xba", "un ")
        
	string = string.replace("\xa0", "")
	string = string.replace("\xa1", "")
	string = string.replace("\xa2", "")
	string = string.replace("\xa3", "")
	string = string.replace("\xa4", "")
	string = string.replace("\xa5", "")
	string = string.replace("\xa6", "")
	string = string.replace("\xa7", "")
	string = string.replace("\xa8", "")
	string = string.replace("\xa9", "")
	string = string.replace("\xaa", "")
	string = string.replace("\xab", "")
	string = string.replace("\xac", "")
	string = string.replace("\xad", "")
	string = string.replace("\xae", "")
	string = string.replace("\xaf", "")
	string = string.replace("\xb0", "")
	string = string.replace("\xb1", "")
	string = string.replace("\xb2", "")
	string = string.replace("\xb3", "")
	string = string.replace("\xb4", "")
	string = string.replace("\xb5", "")
	string = string.replace("\xb6", "")
	string = string.replace("\xb7", "")
	string = string.replace("\xb8", "")
	string = string.replace("\xb9", "")
	string = string.replace("\xba", "")
	string = string.replace("\xbb", "")
	string = string.replace("\xbc", "")
	string = string.replace("\xbd", "")
	string = string.replace("\xbe", "")
	string = string.replace("\xbf", "")
        
	string = string.replace("/", "_")
        string = string.replace(",", "")
        string = string.replace(" ", "_")
        string = string.replace("__", "_")
	return string


#-------------------------------------------------------------------------
# Abrindo um browser firefox
driver = webdriver.Firefox()

# Esperar abrir o browser
time.sleep(5)

#url='http://www.bcb.gov.br/pre/normativos/busca/normativo.asp?numero=3803&tipo=Circular&data=12/7/2016'

# Lendo o csv dos resultados passados
arquivo = open(file_csv, 'rb')
urls = csv.reader(arquivo, delimiter=';')

urls.next()

for url_csv in urls:
	nome = ajustaArray(str(url_csv[0]))
	nome = nome + '.pdf'
	url = str(url_csv[1])
	
	try:
		# Acessar a página 
		driver.get(url)
		
		# Aguardando o site abrir por completo
		time.sleep(12)		

		# Recuperar o código fonte do html
		html = driver.page_source

		# Expressão regular
		response = re.findall(r'href="/.+\.pdf"', html)

		if response != []:
			response1 = response[0].split('"')[1]
			url_full = 'http://www.bcb.gov.br' + response1

			# Fazer o download
			os.system('wget '+url_full+' -O '+nome)
			
			# Aguardando o download
			time.sleep(15)
	except Exception:
		
		print '****************** PDF que deram errado ***********'
		print url
		print nome
# Fechar navegador
driver.close()





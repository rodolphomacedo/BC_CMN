#!/usr/bin/python
# -*- coding: UTF-8 -*-

#------------------------------------------------------------------
#	Recuperação de informações de Normas do CMN e do BC 
#	
#------------------------------------------------------------------

#------------------------------------------------------------------
# Bibliotecas
# Manipulação das funções de tempo
import time

# Importando a biblioteca de expressões regulares
import re

# Manipulação dos sites SELENIUM (instalar o firefox no PC)
from selenium import webdriver

# Remover os caracter especiais que não estão no padrão UTF-8
from unicodedata import normalize

# Trabalhar com datas
from datetime import date

# Manipulação e parsing de html
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

# Manipulação e parsing html usando Beautiful Soup
from bs4 import BeautifulSoup


#-------------------------------------------------------------------------
def ajustaArray(string):
	string = string.replace("\xba", "")
	string = string.replace("\xc0", "A")
        string = string.replace("\xc1", "A")
        string = string.replace("\xc2", "A")
        string = string.replace("\xc3", "A")
        string = string.replace("\xc4", "A")
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
	return string


#-------------------------------------------------------------------------
# Controle de fluxo das páginas
have_page = True

# Abrindo um browser firefox
driver = webdriver.Firefox()

# Url a ser utilizada
url = 'http://www.bcb.gov.br/pre/normativos/busca/buscaNormativo.asp?tema=&startRow=0&refinadorTipo=&refinadorRevogado=&tipo=P&tipoDocumento=0&numero=&conteudo=&dataInicioBusca=19%2F6%2F2016&dataFimBusca=22%2F6%2F2016'

# Acessar a página 
driver.get(url)

# XXX: Fazer a finalização da última página, esta rodando conforme while 1

while (have_page):
	# Aguardar o carregamento do ajax - 10 segundos para garantir o carregamento total
	time.sleep(10)

	# Recuperar o código fonte do html
	html = driver.page_source

	# ---------------------------------------------------
	# Tratamento do html com BeautifulSoap
	soup = BeautifulSoup(html, 'html.parser')
	
	# Rastreando as tags de lista li's
	lis = soup.find('div',id='wrapper')
	lis = lis.find('div', id="content-container")
	lis = lis.find('div', attrs={'class': 'section group busca margin-b-20 '})
	lis = lis.find('div', attrs={'class': 'encontrados'})
	lis = lis.find('ol').findAll('li')

	for li in lis:
		link = (li.find('a').text)
		titulo = li.find('a').text
		#dataHoraDocts = ajustaArray(str(li.text)).split("<br>")[1]
		#assunto = ajustaArray(str(li.text)).split("<br>")[2]
		#responsavel = ajustaArray(str(li.text)).split("<br>")[3]

		print '--------------------------------------------------'
		print li.text
		print titulo
		print link
		#print dataHoraDocts
		#print assunto
		#print responsavel


	# ---------------------------------------------------

	# Tentar: Encontrar o "botão" link para a pŕoxima no html
	button = driver.find_element_by_link_text('Próxima')

	if button:
		# Acionar onclick do javascript
		button.click()
	else:
		have_page = False

# Fechar navegador
driver.close()

print 'Todas as páginas foram listadas!!!'




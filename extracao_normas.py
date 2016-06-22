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
	# Tratamento do html com beautifulSoap
	print html
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




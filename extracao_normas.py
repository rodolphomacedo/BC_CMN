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
url = 'http://www.bcb.gov.br/pre/normativos/busca/buscaNormativo.asp?tema=&startRow=0&refinadorTipo=&refinadorRevogado=&tipo=P&tipoDocumento=0&numero=&conteudo=&dataInicioBusca=13%2F1%2F2012&dataFimBusca=22%2F6%2F2016'
url = 'http://www.bcb.gov.br/pre/normativos/busca/buscaNormativo.asp?tema=&startRow=0&refinadorTipo=&refinadorRevogado=&tipo=P&tipoDocumento=0&numero=&conteudo=&dataInicioBusca=19%2F6%2F1940&dataFimBusca=11%2F1%2F2012'
url = 'http://www.bcb.gov.br/pre/normativos/busca/buscaNormativo.asp?tema=&startRow=0&refinadorTipo=&refinadorRevogado=&tipo=P&tipoDocumento=0&numero=&conteudo=&dataInicioBusca=19%2F6%2F1940&dataFimBusca=4%2F3%2F2010'
url = 'http://www.bcb.gov.br/pre/normativos/busca/buscaNormativo.asp?tema=&startRow=0&refinadorTipo=&refinadorRevogado=&tipo=P&tipoDocumento=0&numero=&conteudo=&dataInicioBusca=12%2F6%2F2012&dataFimBusca=06%2F7%2F2016'

# Acessar a página 
driver.get(url)

# XXX: Fazer a finalização da última página, esta rodando conforme while 1


# Dia de hoje
now = date.today()

# Criando arquivo csv
print("Título;Link;Data/Hora Documento;Assunto;Responsável;DataInserção")

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
		# Inicializando assunto
		assunto = {}
		dataHoraDocts = {}

		string = (li.text).encode('utf-8')
		link = "http://www.bcb.gov.br"+(li.find('a'))['href']
		titulo = li.find('a').text
		#re.findall('<!--(.*?)-->', string, re.DOTALL)
		
		try:
			dataHoraDocts = re.findall('Documento:(.*?)Assunto:', string, re.DOTALL)
		except Exception:
			'null'
		try:
			if not dataHoraDocts:
				dataHoraDocts = re.findall('Documento:(.*?)Resumo:', string, re.DOTALL)
		except Exception:
			'null'
		
		if not dataHoraDocts:
			dataHoraDocts = {}
			dataHoraDocts[0] = '****** ERROR: VER ESSA ENTRADA *******'


		try:
			assunto = re.findall('Assunto:(.*?)Responsável:', string, re.DOTALL)
		except Exception:
			'null'
		try:
			if not assunto:
				assunto = re.findall('Resumo:(.*?)Responsável:', string, re.DOTALL)
		except Exception:
			'null'
	
		if not assunto:
			assunto = {}
			assunto[0] = '****** ERROR: VER ESSA ENTRADA *******'
		else:
			# Retirar as quebras de linhas 
			assunto[0] = assunto[0].replace(';', '.,')
			assunto[0] = assunto[0].replace('\n', ' ')
			assunto[0] = assunto[0].replace('     ', ' ') # 5 Espaços
			assunto[0] = assunto[0].replace('    ', ' ') # 4 Espaços
			assunto[0] = assunto[0].replace('   ', ' ') # 3 Espaços
			assunto[0] = assunto[0].replace('  ', ' ') # 2 Espaços

		responsavel = re.findall('Responsável:(.*?)$', string, re.DOTALL)

		#print "'"+(li.text).encode('utf-8')+"'",
		#print  ';',
		print ""+titulo.encode('utf-8')+"",
		print  ';',
		print ""+link+"",
		print  ';',
		print ""+dataHoraDocts[0]+"",
		print  ';',
		print  ""+assunto[0].decode('utf-8')+"",
		print  ';',
		print  ""+responsavel[0]+"",
		print  ';',
		print ""+str(now).encode('utf-8')+""

#		csv.writerow([ajustaArray(titulo.decode(encoding='UTF-8',errors='strict')),
#				dataHoraDocts,
#				ajustaArray(assunto.decode(encoding='UTF-8',errors='strict')),
#				responsavel,
#				link,now])
		#csv.writerow(['%d','%d','%d','%d','%d','%d'])%(titulo,dataHoraDocts,assunto,responsável,link,now)

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

print ('Todas as páginas foram listadas!!!')




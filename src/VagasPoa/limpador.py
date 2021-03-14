# script para limpar emails duplicados

import os

# load mailing a ser limpo
mailing = []
file=open('maillist.txt','r', encoding='utf-8')
string = file.read()
mailing = string.replace('\n', '').split(',')
file.close()

# delete file
try:
    os.remove("limpador.txt")
except OSError:
    pass

# workflow
# | a  ^ d | 1
# |    | c | 1
# |    | b
# v    | a
#
# |    ^ 
# | a  | c | 1
# |    | a | 0
# v    | b
#
# |    ^ 
# |    | a
# | a  | a | 0
# v    | c 
#
# or
# ->
# a a
# x y z l k m n o p f
#                  <-
# ->
#   b b
# x y z l k m n o p f
#                  <-
#

# Adiciona dois indexes, um no começo do arquivo e outro no final do arquivo
last_email = ''
begin = 0
print("O processo de limpeza começou.")
print("O tamanho atual do mailing é %s ", len(mailing))
while begin < len(mailing)-1:
	end = len(mailing)-1
	while end >= 0:

		# Verifica se ambas posicoes possuem emails diferentes
		if str(mailing[begin]) != str(mailing[end]):

			# Verifica se o ultimo email manipulado e' diferente do email na posicao atual
			if last_email != str(mailing[begin]):

				# Efetua escrita, e leitura no arquivo, para nao inserir duplicatas
				# Abre o arquivo como escrita (apendar, se nao exite arquivo, cria) 
				# e define escrita como verdadeira
				writer = open("limpador.txt", "a+")
				write = True

				# Abre o arquivo como leitura, carrega a lista ja escrita em memoria, e fecha o arquivo
				reader=open('limpador.txt','r', encoding='utf-8')
				string = reader.read()
				email_list_reader = string.split(',')
				reader.close()

				# Efetua busca no arquivo se o endereco de email ja foi escrito, 
				# se sim, define escrita como falsa
				for address_email in email_list_reader:
					if str(address_email) == str(mailing[begin]):
						write = False

				# Se nao foi escrito, o escritor escreve este endereço 
				# e fecha o arquivo aberto em modo escrita
				if write == True:
					writer.write(mailing[begin] + str(','))
				writer.close()

			# Atuali o ultimo email manipulado
			# /r volta para o começo da linha
			last_email = str(mailing[begin])
			print("Processando " + str(begin) + " de " + str(len(mailing)), end="\r")

		end = end - 1
	begin = begin + 1

print("O processo de limpeza terminou.")
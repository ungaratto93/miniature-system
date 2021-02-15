
# script para limpar emails duplicados

emails = []
mailing = 'maillist.txt'
file=open(mailing,'r', encoding='utf-8')
string = file.read()
emails = string.replace('\n', '').split(',')
file.close()

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


begin = 0
string = ''
while begin < len(emails)-1:
	
	end = len(emails)-1
	while end >= 0:

		if str(emails[begin]) != str(emails[end]):
			if (str(emails[begin]) != str(emails[begin+1])):
				item = str(emails[begin])
				if item not in string:
					string = str(item) + ","
					with open('limpador.txt', 'a+', encoding='utf-8') as logfile:
						print(string)
						logfile.write(string)

		end = end - 1

	begin = begin + 1

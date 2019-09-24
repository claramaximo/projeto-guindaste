from tkinter import *
from functools import partial

from pyfirmata import Arduino, util

Porta = '3';
                                
#Uno = Arduino('COM'+Porta)

janela = Tk()

#Título da janela
janela.title("GUI Projeto Guindaste - Laboratório de Projetos 3")

#Define a geometria da janela
janela.geometry("525x330")

janela["bg"] = "gray";

#CABEÇALHO
cabecalho = Label(janela, text = "Universidade Federal de Minas Gerais\n"
 	"Escola de Engenharia - Departamento de Engenharia Elétrica\n"
 	"[ELE084] Laboratório de Projeto III\n"
	"Prof. Gustavo Medeiros Freitas\n"
	"Grupo A - 2o Semestre de 2019")
cabecalho.pack(side = TOP, fill = BOTH, expand = 1)

#PULA UM ESPAÇO 
espaco = Label(janela, text = "", bg = "gray")
espaco.pack(side = TOP, fill = BOTH, expand =1)

#VARIAVEL PARA TRATAMENTO DE ERRO
erro = 0

#Função relacionada a introdução a eventos
def bt_click():
	if (int(ed2.get()) > 25 or int(ed2.get()) < 0 ):
		status["text"] = f"Altura inválida"
		erro = 1
	else:
		erro = 0
		status["text"] = f"Enviado: Ângulo {ed1.get()} e Altura {ed2.get()}."



def incrementa(botao):
	status["text"] = botao["text"]
'''	if int(botao["text"]) == 0:
		Uno.digital[13].write(0)

	elif int(botao["text"]) == 5:
		Uno.digital[13].write(1)

	elif int(botao["text"]) == 10:
		Uno.digital[13].write(1)

	elif int(botao["text"]) == 15:
		Uno.digital[13].write(1)

	elif int(botao["text"]) == 20:
		Uno.digital[13].write(1)

	else:
		Uno.digital[13].write(1)
'''

#Caixa de texto e label 1
lb1 = Label(janela, text = "Digite o ângulo:", width = 20, bg = "gray")
lb1.pack(side = TOP, expand = 1)

ed1 = Entry(janela, width = 25)
ed1.pack(side = TOP, expand = 1)


#Caixa de texto e label 2
lb2 = Label(janela, text = "Digite a altura:", width = 20, bg = "gray")
lb2.pack(side = TOP, expand = 1)

ed2 = Entry(janela, width = 25)
ed2.pack(side = TOP, expand = 1)


label_esq = Label(janela, text = "", width = 5, bg = "gray")
label_esq.pack(side = LEFT, expand = 1)


bt_menos1cm = Button(janela, width = 5, text = "- 1cm", command = incrementa)
bt_menos1cm.pack(side = LEFT, expand = 1)
bt_menos1cm["command"] = partial(incrementa, bt_menos1cm)

bt_mais1cm = Button(janela, width = 5, text = "+ 1cm", command = incrementa)
bt_mais1cm.pack(side = LEFT, expand = 1)
bt_mais1cm["command"] = partial(incrementa, bt_mais1cm)

label_dir = Label(janela, text = "", width = 5, bg = "gray")
label_dir.pack(side = RIGHT, expand = 1)

bt_mais1grau = Button(janela, width = 5, text = "+ 1º", command = incrementa)
bt_mais1grau.pack(side = RIGHT, expand = 1)
bt_mais1grau["command"] = partial(incrementa, bt_mais1grau)

bt_menos1grau = Button(janela, width = 5, text = "- 1º", command = incrementa)
bt_menos1grau.pack(side = RIGHT, expand = 1)
bt_menos1grau["command"] = partial(incrementa, bt_menos1grau)

#PULA UM ESPAÇO 
instrucao = Label(janela, text = "Altura / Ângulo:", width = 15, bg = "gray")
instrucao.pack(side = TOP, fill = BOTH, expand =1)



#PULA UM ESPAÇO 
status = Label(janela, text = "Aguardando interação", bg = "gray")
status.pack(side = BOTTOM, fill = BOTH, expand =1)

#
bt = Button(janela, width = 20, text = "OK", command = bt_click)
bt.pack(side = BOTTOM, anchor = CENTER, expand = 1)


espaco1 = Label(janela, text = "", bg = "gray")
espaco1.pack(side = BOTTOM, expand = 1)

#Abre a janela
janela.mainloop()
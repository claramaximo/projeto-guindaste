import serial
import time
from string import *
from tkinter import *
from functools import partial
from tkinter import ttk
from PIL import ImageTk,Image

# PARÂMETROS - ARDUINO
PORTA = 'COM3'
Velocidade = 9600
arduinoData = serial.Serial(PORTA, Velocidade)

#PARÂMETROS - TEXTOS NOS BOTÕES
botao_enviar = "Enviar"
botao_mais1cm = "+ 1cm"
botao_menos1cm = "- 1cm"
botao_mais1grau = "+ 1º" 
botao_menos1grau = "- 1º"
botao_ligaEletroima = "Ligado"
botao_desligaEletroima = "Desligado"

#PARÂMETROS - RESTRIÇÕES
angulo_max = 180
angulo_min = -180
altura_max = 25
altura_min = 0


# PARÂMETROS - PROTOCOLO DE COMUNICAÇÃO
sinal_positivo = 0
sinal_negativo = 1

numeroBits_Angulo = 8
numeroBits_Altura = 5
#charEnvio[] = ''

def dec2bin(n):
    b = ''
    if(n == 0):
        b = '0'
    else:
        while n != 0:
            b = b + str(n % 2)
            n = int(n / 2)

    return b[::-1]

def Clicado(botao):

    estado_Eletroima = False

    if(botao["text"] == botao_enviar):
        input_angulo = Entry1.get()
        input_altura = Entry2.get()
        estado_Eletroima = False
        sinal_altura = 0


        time.sleep(1); #Pausa de 1 sec

        #Caso o usuário não insira valor
        if(input_angulo == ''):
            input_angulo = 0;
        elif(input_altura == ''):
            input_altura = 0


        #CAST PARA INT PARA REALIZAR COMPARAÇÕES COM INTEIRO
        input_angulo = int(input_angulo)
        input_altura = int(input_altura)

        b_angulo = dec2bin(input_angulo)
        b_altura = dec2bin(input_altura)

        print("Angulo: ",input_angulo," em binario eh: ", b_angulo,"\n")
        print("Altura: ",input_altura," em binario eh: ", b_altura,"\n")



        flag = tratamento_erros(input_angulo,input_altura)

        #CAST PARA STRING PARA MANDAR DADOS
        input_angulo = str(input_angulo)
        input_altura = str(input_altura)

        #SE NÃO HOUVER ERROS, FAÇA
        if(flag == 0):

            #SIGNIFICA QUE O NÚEMRO É POSITIVO
            if(input_angulo.find('-') == -1):
                sinal_angulo = sinal_positivo;
                protocolo_de_comunicacao(sinal_angulo, input_angulo, sinal_altura, input_altura, estado_Eletroima)
            else:
                sinal_angulo = sinal_negativo;
                print("NEGATIVO")
                protocolo_de_comunicacao(sinal_angulo, input_angulo, sinal_altura, input_altura, estado_Eletroima)
            
            #converte_num2step(input_angulo, input_altura)

    elif(botao["text"] == botao_mais1grau):
        input_angulo = "1"
        input_altura = "0"
        estado_Eletroima = False
        sinal_angulo = sinal_positivo
        sinal_altura = sinal_positivo
        protocolo_de_comunicacao(sinal_angulo, input_angulo, sinal_altura, input_altura, estado_Eletroima)
    elif(botao["text"] == botao_menos1grau):
        input_angulo = "1"
        input_altura = "0"
        estado_Eletroima = False
        sinal_angulo = sinal_negativo
        sinal_altura = sinal_positivo
        protocolo_de_comunicacao(sinal_angulo, input_angulo, sinal_altura, input_altura, estado_Eletroima)
    elif(botao["text"] == botao_mais1cm):
        input_angulo = "0"
        input_altura = "1"
        estado_Eletroima = False
        sinal_angulo = sinal_positivo
        sinal_altura = sinal_positivo
        protocolo_de_comunicacao(sinal_angulo, input_angulo, sinal_altura, input_altura, estado_Eletroima)
    elif(botao["text"] == botao_menos1cm):
        input_angulo = "0"
        input_altura = "1"
        estado_Eletroima = False
        sinal_angulo = sinal_positivo
        sinal_altura = sinal_negativo
        protocolo_de_comunicacao(sinal_angulo, input_angulo, sinal_altura, input_altura, estado_Eletroima)
    elif(botao["text"] == botao_ligaEletroima):
        input_angulo = "0"
        input_altura = "0"
        estado_Eletroima = True
        sinal_angulo = sinal_positivo
        sinal_altura = sinal_positivo
        protocolo_de_comunicacao(sinal_angulo, input_angulo, sinal_altura, input_altura, estado_Eletroima)
    elif(botao["text"] == botao_desligaEletroima):
        input_angulo = "0"
        input_altura = "0"
        estado_Eletroima = False
        sinal_angulo = sinal_positivo
        sinal_altura = sinal_positivo
        protocolo_de_comunicacao(sinal_angulo, input_angulo, sinal_altura, input_altura, estado_Eletroima)
    
    

# Define as restrições dos valores de entrada - Mensagem é mostrada no status
def tratamento_erros(input_angulo, input_altura):
    #Indica se há erro ou não nos dados de entrada - 1 -> ERRO; 0-> SEM ERRO
    flag = 0

    if((input_angulo > angulo_max) or (input_angulo < angulo_min)) or ((input_altura > altura_max) or (input_altura < altura_min)):
        flag = 1;
        if((input_angulo > angulo_max) or (input_angulo < angulo_min)) and ((input_altura > altura_max) or (input_altura < altura_min)):
            Label10["text"] = "Erro: Valores de altura e ângulo fora do range." 
        elif((input_angulo > angulo_max) or (input_angulo < angulo_min)):
            Label10["text"] = "Erro: Valor de ângulo fora do range." 
        elif((input_altura > altura_max) or (input_altura < altura_min)):
            Label10["text"] = "Erro: Valor de altura fora do range." 
    else:

        # NADA ESCRITO -> OK
        Label10["text"] = ""
        flag = 0;

    return flag;


#Converte os dados no protocolo de comunicação estabelecido
def protocolo_de_comunicacao(sinal_angulo, input_angulo, sinal_altura, input_altura, estado_Eletroima):

    charEnvio = ''

    # SINAL DO ANGULO
    if(sinal_angulo == 0): #SINAL POSITIVO
        charEnvio = '0' + charEnvio
    else:  #SINAL NEGATIVO
        charEnvio = '1' + charEnvio

    # ANGULO
    input_angulo = int(input_angulo)
    b_angulo = dec2bin(input_angulo)

    #COMPLETA PARA CHEGAR EM 8 BITS
    while(len(b_angulo) < numeroBits_Angulo):
        b_angulo = '0' + b_angulo

    charEnvio = charEnvio + b_angulo
    

    # SINAL DA ALTURA
    if(sinal_altura == 0): #SINAL POSITIVO
        charEnvio = charEnvio + '0'
    else:  #SINAL NEGATIVO
        charEnvio = charEnvio + '1'


    # ALTURA
    input_altura = int(input_altura)
    b_altura = dec2bin(input_altura)


    #COMPLETA PARA CHEGAR EM 5 BITS
    while(len(b_altura) < numeroBits_Altura):
        b_altura = '0' + b_altura

    charEnvio = charEnvio + b_altura


    # ELETROÍMÃ
    if(estado_Eletroima == False): #DESLIGADO
        charEnvio = charEnvio + '0'
    else:  #LIGADO
        charEnvio = charEnvio + '1'


    # MARCADOR DE FINAL DE STRING
    charEnvio = charEnvio + '\n'

    print(charEnvio)

    envia_dados(charEnvio)
    recebe_dados()

    # CONVERTE PARA STRING E MANDA BYTES
    #converte_strBin2char(charEnvio)


#Converte a string contendo a informação em bits para um char
def converte_strBin2char(charEnvio):
    
    auxiliar_primeiroByte = ''
    auxiliar_segundoByte = ''
    envio_Byte = ''

    # SEPARAÇÃO DA STRING INTEIRA PARA 2 BYTES
    primeiro_Byte = charEnvio[0:8]
    segundo_Byte = charEnvio[8:16]

    #INVERTE PARA FAZER O CÁLCULO
    auxiliar_primeiroByte = primeiro_Byte[::-1]
    auxiliar_segundoByte = segundo_Byte[::-1]
    
    # INICIALIZA AS VARIÁVEIS
    soma_primeiroByte  = 0
    soma_segundoByte  = 0;
    
    for i in range(len(auxiliar_primeiroByte)):
        
        soma_primeiroByte = soma_primeiroByte + ( (2 ** i) * int(auxiliar_primeiroByte[i]))
        soma_segundoByte = soma_segundoByte + ( (2 ** i) * int(auxiliar_segundoByte[i]))

    
    
    #print(len(auxiliar_primeiroByte))
    #print(soma_primeiroByte, "e ", soma_segundoByte)
    print(str(chr(soma_primeiroByte)), "e ", str(chr(soma_segundoByte)) )
    # CONCATENA AS STRINGS PARA ENVIAR
    envio_Byte = envio_Byte + str(chr(soma_primeiroByte)) + str(chr(soma_segundoByte))

    # MARCADOR DE FINAL DE STRING
    envio_Byte = envio_Byte + '\n'
    print(envio_Byte)

    # ENVIA DADOS PROCESSADOS
    envia_dados(envio_Byte)

    # RECEBE CONFIRMAÇÃO DOS DADOS ENVIADOS
    recebe_dados()


# ENVIA OS 2 BYTES PARA O ARDUINO
def envia_dados(envio_Byte):
    
    # ENVIA BYTES PARA ARDUINO
    arduinoData.write(envio_Byte.encode('utf-8'))

# RECEBE DADOS DO ARDUINO PARA EXIBIR NA INTERFACE
def recebe_dados():
    
    # RECEBE RESPOSTA
    resposta = arduinoData.readline();

    # LABEL DE STATUS
    Label10["text"] = resposta ;


# INTERFACE
window  = Tk()
window.title("GUI Projeto Guindaste - Laboratório de Projetos 3")
window.geometry("528x400")


#CABEÇALHO
cabecalho = Label(window, text = "Universidade Federal de Minas Gerais\n"
    "Escola de Engenharia - Departamento de Engenharia Elétrica\n"
    "[ELE084] Laboratório de Projeto III\n"
    "Prof. Gustavo Medeiros Freitas\n"
    "Grupo A - 2o Semestre de 2019")
cabecalho.grid(row = 0, column = 2)


#Espaço em branco - Separação entre cabeçalho e widgets
Label12 = Label(window, text = "******************")
Label12.grid(row = 1, column = 1)

Label11 = Label(window, text = "*****************************************************************")
Label11.grid(row = 1, column = 2)

Label13 = Label(window, text = "******************")
Label13.grid(row = 1, column = 3)



#Imagem
path = "C:/Users/migma/Desktop/ENGENHARIA DE SISTEMAS/LogoEE1.png"
img = Image.open(path)
img = img.resize((70, 70), Image.ANTIALIAS)
img = ImageTk.PhotoImage(img)
panel = Label(window, image=img)
panel.image = img
panel.grid(row=0, column=1)


#   Ângulo
Label1 = Label(window, text = "Digite o ângulo:")
Label1.grid(row = 2, column = 1)

Entry1 = Entry(window)
Entry1.grid(row = 2, column = 2)
numero = Entry1.get()

Label6 = Label(window, text = " º (graus)")
Label6.grid(row = 2, column = 3)

#   Altura
Label2 = Label(window, text = "Digite a altura:")
Label2.grid(row = 3, column = 1)

Entry2 = Entry(window)
Entry2.grid(row = 3, column = 2)

Label7 = Label(window, text = "cm (centímetros)")
Label7.grid(row = 3, column = 3)

#Espaço em branco
Label9 = Label(window, text = "")
Label9.grid(row = 4, column = 2)

#Ajuste fino Ângulo
Label5 = Label(window, text = "Ajuste fino ângulo/altura:")
Label5.grid(row = 6, column = 2)

#ALTURA AJUSTE FINO
Buttom4 = Button(window, text = botao_mais1grau, command = Clicado)
Buttom4.grid(row = 7, column = 1)
Buttom4["command"] = partial(Clicado, Buttom4)

Buttom5 = Button(window, text = botao_menos1grau, command = Clicado)
Buttom5.grid(row = 8, column = 1)
Buttom5["command"] = partial(Clicado, Buttom5)

#ÂNGULO AJUSTE FINO
Buttom6 = Button(window, text = botao_mais1cm, command = Clicado)
Buttom6.grid(row = 7, column = 3)
Buttom6["command"] = partial(Clicado, Buttom6)

Buttom7 = Button(window, text = botao_menos1cm, command = Clicado)
Buttom7.grid(row = 8, column = 3)
Buttom7["command"] = partial(Clicado, Buttom7)


# Botão ENVIAR
Buttom3 = Button(window, text = botao_enviar, command = Clicado)
Buttom3.grid(row = 5, column = 2)
Buttom3["command"] = partial(Clicado, Buttom3)

#   Eletroímã
Label3 = Label(window, text = "Eletroímã:")
Label3.grid(row = 9, column = 2)

Buttom1 = Button(window, text = botao_ligaEletroima, command = Clicado)
Buttom1.grid(row = 10, column = 2)
Buttom1["command"] = partial(Clicado, Buttom1)

Buttom2 = Button(window, text = botao_desligaEletroima, command = Clicado)
Buttom2.grid(row = 11, column = 2)
Buttom2["command"] = partial(Clicado, Buttom2)

# Espaço em branco + Status
Label4 = Label(window, text = "")
Label4.grid(row = 12, column = 2)

Label8 = Label(window, text = "Status:")
Label8.grid(row = 13, column = 2)

# RESULTADO STATUS
Label10 = Label(window, text = "")
Label10.grid(row = 14, column = 2)

#Janela da Interface
window.mainloop()
    

#FECHA CONEXÃO
arduinoData.close()
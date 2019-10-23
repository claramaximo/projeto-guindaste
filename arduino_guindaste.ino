#include <Stepper.h>
#include <String.h>
#define NUM_BITS 8

const byte numChars = 16;

// PARÂMETROS - RECEBIMENTO DE STRING
String inputString = ""; // an array to store the received data
bool stringComplete = false;  // whether the string is complete

// PARÂMETROS - 
int a[NUM_BITS];
int b[NUM_BITS];
String bytes_reconstruidos;

// PARÂMETROS - PROTOCOLO DE COMUNICAÇÃO
int posicao_sinal_angulo = 0;
int posicao_sinal_altura = 9;
int posicao_estadoEletroima = 15;

// PARÂMETROS RECEBIDOS POR COMUNICAÇÃO SERIAL
float angulo = 0;
float altura = 0;
bool estado_Eletroima;


// PARÂMETROS MOTOR DE PASSOS
const int stepsPerRevolution = 500; 
//Inicializa a biblioteca utilizando as portas de 8 a 11 para 
//Ligacao ao motor do angulo 
Stepper Motor_Angulo(stepsPerRevolution, 8,10,9,11);
//Ligacao do motor de altura
Stepper Motor_Altura(stepsPerRevolution, 4,6,5,7);


// PARÂMETROS - PASSOS
float passos_1voltacompleta = 2048;
float num_passo_angulo = passos_1voltacompleta/360;
float num_passo_altura = (2*3.14159*(0.005/2)) * passos_1voltacompleta;
int passos_angulo;
int passos_altura; 



void setup() {
 Serial.begin(9600);
 inputString.reserve(numChars);

 // inicializa o pino digital 13 como uma saída.
  pinMode(13, OUTPUT);    
 
 //Determina a velocidade inicial do motor 
 Motor_Angulo.setSpeed(45);
 Motor_Altura.setSpeed(45);
 
}

void loop() {
 
 if(stringComplete){
    
    //Serial.print(inputString);
    processa_string(inputString);
    converte_int2step();
    move_stepMotors();
    status_eletroima();
    
    // clear the string:
    inputString = "";
    stringComplete = false;
 }
}


void serialEvent(){
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}


void processa_string(String dadosEntrada){

  int primeiro_Byte, segundo_Byte;
  int vetor_primeiroByte[8];
  int vetor_segundoByte[8];
  int i,j, auxiliar;
  


  bytes_reconstruidos = dadosEntrada;
  
  // PARA ÂNGULO
  angulo = 0;
  for(i = 1, j = 7; i <= 8 && j >= 0 ; i++, j--){
    
    int diogo = bytes_reconstruidos[i] - 48;
   
    angulo = angulo + (pow(2,j)*diogo );
    
  }
  
  
  // SINAL ANGULO
  if(bytes_reconstruidos[posicao_sinal_angulo] == '0'){ // ANGULO POSITIVO
    angulo = angulo;
  }
  else{  // ANGULO NEGATIVO
    
    angulo = (-1)*angulo;
  }


  // PARA ALTURA
  altura = 0;
  for(i = 10, j = 4; i <= 14 ; i++, j--){  
    altura = altura +  ( pow(2,j) * int(bytes_reconstruidos[i] - 48));
  }
  
  
  // SINAL ALTURA
  if(bytes_reconstruidos[posicao_sinal_altura] == '0'){ // ANGULO POSITIVO
    altura = (+1)*altura;
  }
  else{  // ANGULO NEGATIVO
    altura = (-1)*altura;
  }


  // PARA ESTADO DO ELETROÍMA
  if(bytes_reconstruidos[posicao_estadoEletroima] == '0'){ // DESLIGADO
    estado_Eletroima = false;
  }
  else{  // LIGADO
    estado_Eletroima = true;
  }
  
}

// CONVERTE OS INTEIROS RECEBIDOS NO PROTOCOLO DE COMUNICAÇÃO EM PASSOS PARA O MOTOR DE PASSOS
void converte_int2step(){

    // CAST DE INT PARA NÃO TER VALOR DECIMAL (COM ARREDONDAMENTO)
    passos_angulo = int( (num_passo_angulo*angulo) + 0.5);
    passos_altura = int( (num_passo_altura*altura) + 0.5);
}

// MOVE OS MOTORES DE PASSO
void move_stepMotors(){
  
    // MOTOR PARA ÂNGULO - BRAÇO DO GUINGASTE
    Motor_Angulo.step(passos_angulo);
    
    Serial.print("Angulo ");
    Serial.print(angulo);
    Serial.print(" -> ");
    Serial.print(passos_angulo);
    Serial.print(" passos. ");
    
    Serial.print("Altura ");
    Serial.print(altura);
    Serial.print(" -> ");
    Serial.print(passos_altura);
    Serial.println(" passos");


    // MOTOR PARA ALTURA - ERGUE/DESCE O ELETROÍMA
    Motor_Altura.step(passos_altura);
}

// LIGA E DESLIGA O ELETROIMA
void status_eletroima(){
  if(estado_Eletroima == true){
    digitalWrite(13, HIGH);       // liga o LED
  }
  else{
    digitalWrite(13, LOW);      // desliga o LED
  }        
}

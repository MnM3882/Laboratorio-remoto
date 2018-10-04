#include <TimerOne.h>

//------------ESTADOS---------------

#define ESPERAR 0
#define MEDIR  1
#define ENVIAR 2
#define MOVER_OBSTACULO 4
#define MOVER_ZAHLROHR_POR_PASOS 5  //Chequear con el demoscope3.py que modo le corresponde
#define ALEJAR_ZAHLROHR 6
#define ACERCAR_ZAHLROHR 7
unsigned int estado=ESPERAR;
unsigned char modo = ENVIAR;

//----------------------------------

//------------PINES-----------------

const int ADC1 = 1;             // Pin del ADC
const int ExtNoria = 2;         // external interrupt, detección de flanco de bajada en el fototransistor
const int eOptico = 4;          // Sensor final de carrera LED NO obstaculo ->0V SI obstaculo 5V
const int eMecanico = 1;        // Sensor final de carrera mecanico NO obstaculo ->0V SI obstaculo 5V
const int M1_VB=12, M1_R=11, M1_V=10, M1_RB=9, M2_VB=8, M2_R=7, M2_V=6, M2_RB=5; //pines de motores
const int Noria=13;				// Sensor fototransistor NO obstaculo ->5V SI obstaculo 0V
const int ExtPulsos=3;          // external interrupt, Deteccion de pulsos


//----------------------------------

//------------VARIABLES-------------
typedef union{
unsigned char u8[2];  // char 1 Byte
unsigned int u16;     // int 2 Bytes
}AMPLITUD;

volatile AMPLITUD iADC1;  // variable to store the value read
unsigned char dTrama[2]={0x00,0x00};
unsigned int distpasos[17] = {0, 39, 78, 117, 156, 195, 234, 273, 312, 351, 390, 429, 468, 507, 546, 585, 624};
volatile bool m1VB=0, m1R=0, m1V=0, m1RB=0, m2VB=0, m2R=0, m2V=0, m2RB=0; //  m1 Noria  m2 Carro Miguel: Anotar aqui la traduccion de los colores, por si acaso
unsigned int obs_arr[9] = {13, 37, 61, 87, 111, 136, 161, 187, 4095};     //Pasos que debe dar el m1 para llegar a cada obstaculo
unsigned int obsid = 4096;    //Numero total de pasos que da la noria
unsigned int npulsos=0;  //Contador de pulsos que llegan desde el detector
unsigned int light=0;    //Cantidad de pasos que da m1 con el fototransistor recibiendo luz constantemente
unsigned int i=0, pasos=4096, j=0, antirebote=0;  //Contadores auxiliares
//----------------------------------


void setup()
{
  pinMode(Noria, INPUT_PULLUP);		//sensor off->HIGH sensor on->  LOW 
  pinMode(ExtNoria, INPUT_PULLUP);  //sensor off->HIGH sensor on->  LOW 
  pinMode(eOptico, INPUT_PULLUP);   //sensor off->HIGH sensor on->  LOW 
  pinMode(eMecanico, INPUT_PULLUP); //sensor off->HIGH sensor on->  LOW
  pinMode(ExtPulsos, INPUT_PULLUP); //sensor off->HIGH sensor on->  LOW
  pinMode(M1_VB, OUTPUT);
  pinMode(M1_R, OUTPUT);
  pinMode(M1_V, OUTPUT);
  pinMode(M1_RB, OUTPUT);
  pinMode(M2_VB, OUTPUT);
  pinMode(M2_R, OUTPUT);
  pinMode(M2_V, OUTPUT);
  pinMode(M2_RB, OUTPUT); 
  Serial.begin(115200);             //Velocidad de transmision
  Timer1.initialize(1000);          //Interrupcion cada 1ms
  Timer1.attachInterrupt(Timer_int);//Funcion de interrupcion temporal
  attachInterrupt(digitalPinToInterrupt(ExtNoria), blink_Noria, FALLING);  //Funcion de interrupcion EXTERNA
  attachInterrupt(digitalPinToInterrupt(ExtPulsos), Contador_pulsos, FALLING); //Funcion de interrupcion EXTERNA
}

void Timer_int(void)
{
  if (estado==ESPERAR){
      estado=MEDIR;
    }
}

void blink_Noria(void) {
  light = 0;
}

void Contador_pulsos(void) {
  npulsos++;
}

void loop()
{
  switch(estado)
  {
    case ESPERAR:      
      break;
    case MEDIR:
      iADC1.u16 = analogRead(ADC1);               // Lectura de ADC
      if (Serial.available() > 0)   // Si hay datos en el buffer
      {
        //modo = Serial.read();
	      Serial.readBytes(&modo, 1);
        Serial.write(modo);         
      }
      estado = modo & 0x07;   //0x07=0000 0111
      break;
    case ENVIAR:
    //Trama 1_0_d1_d2_d3_x_x_x   0_x_x_x_x_x_x_x
    //x son bits de lectura ADC
    //di son bits destinados a los sensores digitales

      digitalWrite(M2_VB, LOW);
      digitalWrite(M2_R, LOW);
      digitalWrite(M2_V, LOW);
      digitalWrite(M2_RB, LOW);

      digitalWrite(M1_VB, LOW);
      digitalWrite(M1_R, LOW);
      digitalWrite(M1_V, LOW);
      digitalWrite(M1_RB, LOW);
    
      if((modo >> 4) == 0)
      {
        iADC1.u16 = npulsos;      
      }

      npulsos = 0;
    //Se ensambla la trama que se enviara por serial
    //iADC.u8[1] almacena el byte mas significativo de la lectura del ADC
      dTrama[0] = (iADC1.u8[1] & 0x03) << 1;      //  0x03=0000 0011
      dTrama[0] += ((iADC1.u8[0] & 0x80) >> 7);   //  0x80=1000 0000
      dTrama[0] += 0x80; //0x80=1000 0000
    //iADC.u8[0] almacena el byte menos significativo de la lectura del ADC
      dTrama[1] = (iADC1.u8[0] & 0x7F);           //  0x7F=0111 1111
    //Lectura de los sensores digitales
      if(!digitalRead(eOptico))
      {
        dTrama[0]+=0x20;                            //0x20=0010 0000                            
      }
      if(!digitalRead(eMecanico))
      {
        dTrama[0]+=0x10;                            //0x20=0001 0000                            
      }
      for (int i = 0; i < 2; i++)
      {
        Serial.write(dTrama,2);
      }
      
      estado=ESPERAR;

    break;
      
    case MOVER_ZAHLROHR_POR_PASOS:

      if(i==0)
        {
          //Avanza hacia atras
          if( (pasos) < distpasos[modo >> 4] && digitalRead(eMecanico))  
          // si el numero de pasos avanzados en menor que el necesario y no se ha llegado al extremo lejano, continua avanzando  
          {
            if(m2VB)
            {
              m2VB = 0;
              m2R = 0;
              m2V = 0;
              m2RB = 1;                 
            }
            else if(m2R)
            {
              m2VB = 1;
              m2R = 0;
              m2V = 0;
              m2RB = 0;                 
            }
            else if(m2V)
            {
              m2VB = 0;
              m2R = 1;
              m2V = 0;
              m2RB = 0;                 
            }
            else if(m2RB)
            {
              m2VB = 0;
              m2R = 0;
              m2V = 1;
              m2RB = 0;                 
            }
            else
            {
              m2VB = 0;
              m2R = 0;
              m2V = 0;
              m2RB = 1;                 
            }
            
            pasos++;
           }
          //  Avanza hacia adelante
          else if( (pasos) > distpasos[modo >> 4] && digitalRead(eOptico))
          // si el numero de pasos avanzados en menor que el necesario y no se ha llegado al extremo cercano, continua avanzando
          {
            if(m2VB)
            {
              m2VB = 0;
              m2R = 1;
              m2V = 0;
              m2RB = 0;             
            }
            else if(m2R)
            {
              m2VB = 0;
              m2R = 0;
              m2V = 1;
              m2RB = 0;             
            }
            else if(m2V)
            {
              m2VB = 0;
              m2R = 0;
              m2V = 0;
              m2RB = 1;             
            }
            else if(m2RB)
            {
              m2VB = 1;
              m2R = 0;
              m2V = 0;
              m2RB = 0;             
            }
            else
            {
              m2VB = 1;
              m2R = 0;
              m2V = 0;
              m2RB = 0;             
            }               
            pasos--;
          }
          else
	      {
	      modo = ENVIAR;
	      }

       }

      if(!digitalRead(eOptico)) // Si estás en el extrema cercano 
      {
        pasos = 0;
      }
      
      i = (i+1)%50;
      
      digitalWrite(M2_VB, m2VB);
      digitalWrite(M2_R, m2R);
      digitalWrite(M2_V, m2V);
      digitalWrite(M2_RB, m2RB);

      estado = ESPERAR;
      
      break;

    case MOVER_OBSTACULO:
                            
      if(obsid != obs_arr[modo >> 4])
        // Si aun no se han dado los pasos necesarios para llegar al obstaculo deseado
      {
                
        if(i==0)
        { 
          if(!digitalRead(Noria))
          {
            light++;
          }
          
          if(m1VB)
          {
            m1VB = 0;
            m1R = 0;
            m1V = 0;
            m1RB = 1;                 
          }
          else if(m1R)
          {
            m1VB = 1;
            m1R = 0;
            m1V = 0;
            m1RB = 0;                 
          }
          else if(m1V)
          {
            m1VB = 0;
            m1R = 1;
            m1V = 0;
            m1RB = 0;                 
          }
          else if(m1RB)
          {
            m1VB = 0;
            m1R = 0;
            m1V = 1;
            m1RB = 0;                 
          }
          else
          {
            m1VB = 0;
            m1R = 0;
            m1V = 0;
            m1RB = 1;                 
          }
          obsid++;
      
          if(light > 6)
          {
            obsid = 0;
          }
        }
            
        i = (i+1)%70;
        
        digitalWrite(M1_VB, m1VB);
        digitalWrite(M1_R, m1R);
        digitalWrite(M1_V, m1V);
        digitalWrite(M1_RB, m1RB);
        
      }             
              
      else
      {
      modo = ENVIAR;
      }
                    
      estado = ESPERAR;
              
      break;
  }
 }

/* ###################################################################
**     Filename    : main.c
**     Project     : Proyectos2
**     Processor   : MC9S08QE128CLK
**     Version     : Driver 01.12
**     Compiler    : CodeWarrior HCS08 C Compiler
**     Date/Time   : 2018-02-14, 14:56, # CodeGen: 0
**     Abstract    :
**         Main module.
**         This module contains user's application code.
**     Settings    :
**     Contents    :
**         No public methods
**
** ###################################################################*/
/*!
** @file main.c
** @version 01.12
** @brief
**         Main module.
**         This module contains user's application code.
*/         
/*!
**  @addtogroup main_module main module documentation
**  @{
*/         
/* MODULE main */


/* Including needed modules to compile this module/procedure */
#include "Cpu.h"
#include "Events.h"
#include "TI1.h"
#include "Bit1.h"
#include "Bit2.h"
#include "Bit3.h"
#include "Bit4.h"
#include "Bit5.h"
#include "AS1.h"
#include "AD1.h"
#include "Bit6.h"
#include "EInt1.h"
#include "Bit7.h"
#include "Bit8.h"
#include "Bit9.h"
#include "Bit10.h"
#include "Bit11.h"
#include "EInt2.h"
/* Include shared modules, which are used for whole project */
#include "PE_Types.h"
#include "PE_Error.h"
#include "PE_Const.h"
#include "IO_Map.h"

/* User includes (#include below this line is not maintained by Processor Expert) */
unsigned char estado = ESPERAR;
unsigned int npulsos=0; //Contador de pulsos que llegan desde el detector
unsigned int light=0;

unsigned char CodError;
unsigned int Enviados = 4;		// Esta variable no aporta nada más sino el número de elementos del arreglo a enviar.

typedef union{
unsigned char u8[2];
unsigned int u16;
}AMPLITUD;

volatile AMPLITUD iADC1, iADC2;
volatile bool d1=0, d2=1, d3=1, m1VB=0, m1R=0, m1V=0, m1RB=0, m2VB=0, m2R=0, m2V=0, m2RB=0;
unsigned char dTrama[4]={0x00,0x00,0x00,0x00};
unsigned int i=0, pasos=4096, j=0, antirebote=0;
unsigned char modo = ENVIAR;
unsigned int distancias[16][2] = {{1947,1952},{1685,1690},{1501,1506},{1352,1356},{1223,1229},{1113,1118},{1036,1042},{965,970},{907,913},{846,851},{802,807},{759,764},{726,732},{687,692},{657,663},{629,634}};
unsigned int distpasos[17] = {0, 39, 78, 117, 156, 195, 234, 273, 312, 351, 390, 429, 468, 507, 546, 585, 624};
unsigned int obs_arr[9] = {13, 37, 61, 87, 111, 136, 161, 187, 4095};
unsigned int obsid = 4096, avdist = 4096;

void main(void)
{
  /* Write your local variable definition here */

  /*** Processor Expert internal initialization. DON'T REMOVE THIS CODE!!! ***/
  PE_low_level_init();
  /*** End of Processor Expert internal initialization.                    ***/

  /* Write your code here */
  /* For example: for(;;) { } */
  
  Bit3_PutVal(m1VB);
  Bit4_PutVal(m1R);
  Bit5_PutVal(m1V);
  Bit6_PutVal(m1RB);
  
  Bit7_PutVal(m2VB);
  Bit8_PutVal(m2R);
  Bit9_PutVal(m2V);
  Bit10_PutVal(m2RB);

  for(;;) { 
  	  
  	  switch (estado){
  	    		
  	    		case ESPERAR:
  	    			break;
  	    			
  	    		case MEDIR:
  	    			CodError = AD1_Measure(TRUE);
  	    			CodError = AD1_GetChanValue16(0,&iADC1.u16);	// Galvanometro
  					CodError = AD1_GetChanValue16(1,&iADC2.u16);	// Sharp
  	    			d1=Bit1_GetVal();								// Noria
  	    			d2=Bit2_GetVal();								// Extremo optico
  	    			d3=Bit11_GetVal();								// Extremo mecanico
 	    			if(AS1_GetCharsInRxBuf()>0)
  	    			{
  	    				CodError = AS1_RecvChar(&modo);
  	    				CodError = AS1_ClearRxBuf();
  	    			}
  	    			estado = modo & 0x07;
 	    			
  	    			break;
  	    	
  	    		case ENVIAR:
  	    			
  	    			Bit3_PutVal(0);
  	    			Bit4_PutVal(0);
  	    			Bit5_PutVal(0);
  	    			Bit6_PutVal(0);
  	    			
  	    			Bit7_PutVal(0);
  	    			Bit8_PutVal(0);
  	    			Bit9_PutVal(0);
  	    			Bit10_PutVal(0);
  	    			
  	    			if((modo >> 4) == 0)
  	    			{
  	    				iADC2.u16 = npulsos<<4;  	    				
  	    			}
  	    			else if((modo >> 4) == 2)
  	    			{
  	    				iADC1.u16 = pasos<<4;
  	    			}

  	    			npulsos = 0;
  	    			
  	    			dTrama[0] = (iADC1.u8[0] & 0xF8) >> 3;	// 0xF8=1111 1000
  	    			dTrama[1] = (iADC1.u8[0] & 0x07) << 4;	//0x07=0000 0111
  	    			dTrama[1] += iADC1.u8[1] >> 4;
  	    			
  					dTrama[2] = (iADC2.u8[0] & 0xF8) >> 3;
  	    			dTrama[3] = (iADC2.u8[0] & 0x07) << 4;
  	    			dTrama[3] += iADC2.u8[1] >> 4;
  	    			
  	    			
  	    			if(d2)
  	    			{
  	    				dTrama[0] += 0x20;	//0x20=0010 0000
  	    			}
  	    			
  	    			if(d3)
  	    			{
  	    				dTrama[2] += 0x20;	//0x20=0010 0000
  	    			}
  	    			
  					
  	    			
  	    			dTrama[0] += 0x80;	////0x80=1000 0000
  	    			CodError = AS1_SendBlock(dTrama,4,&Enviados); //El arreglo con la medición está en iADC.u8 (notar que es un apuntador)
  	    			estado = ESPERAR;
  	    			
  	    			break;
  	    			
  	    		case MOVER_ZAHLROHR:
  	    			
  	    			/* 
  	    			 * 4 bits para seleccion de distancias
  	    			 * 4 bits para seleccion de modo
  	    			 * Modos:
  	    			 * 			- Medir
  	    			 * 			- Mover Zahlrohr
  	    			 * 			- Mover disco de obstaculos
  	    			 * 			- ...
  	    			 * 
  	    			 * Trama recibida: d1 d2 d3 d4 m1 m2 m3 m4
  	    			 * 
  	    			 */
  	    			
  	    			if(i==0)
  	    			{
  	    				if(avdist == 4096)
  	    				{
  	    					avdist = iADC2.u16 >> 4;
  	    				}
  	    				
						if( avdist > distancias[modo >> 4][1] && !d3)
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
						
						else if( avdist < distancias[modo >> 4][0] && !d2)
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
						
						avdist = iADC2.u16 >> 4;
					
  	    			}
  	    			
  	    			avdist = (avdist+(iADC2.u16 >> 4))/2;
  	    			
  	    			if(d2)
  	    			{
  	    				pasos = 0;
  	    			}
  	    			
  	    			i = (i+1)%50;
  	    			
  	    			
  	    			Bit3_PutVal(m2VB);
  	    			Bit4_PutVal(m2R);
  	    			Bit5_PutVal(m2V);
  	    			Bit6_PutVal(m2RB);
  	    			
  	    			estado = ESPERAR;
  	    			
  	    			break;

  	    		case MOVER_OBSTACULO:
  	    			  	    			
  	    			if(obsid != obs_arr[modo >> 4])
  	    			{
  	    				
						if(i==0)
						{	
	  	    				if(d1)
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
	  	    			
						Bit7_PutVal(m1VB);
						Bit8_PutVal(m1R);
						Bit9_PutVal(m1V);
						Bit10_PutVal(m1RB);
  	    			} 	    			
  	    			
  	    			else
  	    			{
  						modo = ENVIAR;
  	    			}
										
					estado = ESPERAR;
  	    			
  	    			break;
  	    			
  	    		case MOVER_ZAHLROHR_POR_PASOS:
  	    			
  	    			if(i==0)
  	    			{
  	    				
  	    			
						if( (pasos) < distpasos[modo >> 4] && !d3)
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
						
						else if( (pasos) > distpasos[modo >> 4] && !d2)
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
  	    			
  	    			if(d2)
  	    			{
  	    				pasos = 0;
  	    			}
  	    			
  	    			i = (i+1)%50;
  	    			
  	    			
  	    			Bit3_PutVal(m2VB);
  	    			Bit4_PutVal(m2R);
  	    			Bit5_PutVal(m2V);
  	    			Bit6_PutVal(m2RB);
  	    			
  	    			estado = ESPERAR;
  	    			
  	    			break;

  	    		default:
  	    			break;
  	    	
  	    	}
    }
  
  /*** Don't write any code pass this line, or it will be deleted during code generation. ***/
  /*** RTOS startup code. Macro PEX_RTOS_START is defined by the RTOS component. DON'T MODIFY THIS CODE!!! ***/
  #ifdef PEX_RTOS_START
    PEX_RTOS_START();                  /* Startup of the selected RTOS. Macro is defined by the RTOS component. */
  #endif
  /*** End of RTOS startup code.  ***/
  /*** Processor Expert end of main routine. DON'T MODIFY THIS CODE!!! ***/
  for(;;){}
  /*** Processor Expert end of main routine. DON'T WRITE CODE BELOW!!! ***/
} /*** End of main routine. DO NOT MODIFY THIS TEXT!!! ***/

/* END main */
/*!
** @}
*/
/*
** ###################################################################
**
**     This file was created by Processor Expert 10.3 [05.09]
**     for the Freescale HCS08 series of microcontrollers.
**
** ###################################################################
*/

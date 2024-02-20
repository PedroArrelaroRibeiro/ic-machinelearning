# Python para o Radiuino over Arduino
import serial
import math
import time
import struct
import socket
from time import localtime, strftime
import os

def calc_rssi(byte):
   rssi =0
   if byte > 128:
      rssi = ((byte-256)/2.0)-81
   else:
      rssi = (byte/2.0)-81
   return rssi

# Configura a serial
### para COM# o número que se coloca é n-1 no primeiro parâmetrso. Ex COM9  valor 8
n_serial = input("Digite o número da serial = ") #seta a serial
n_serial1 = int(n_serial) - 1
ser = serial.Serial("COM"+str(n_serial), 9600, timeout=0.5,parity=serial.PARITY_NONE) # serial Windows
#ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1) # serial Linux

Tempo_entre_rotas = 1.2

'''#====ARQUIVOS GERADOS
Cada arquivo terá duas RSSI. Uma de ida e outra de volta

ROTA 1
Bytes em que está as RSSI na sequência de subida e descida 
Rota1_B1.txt  -> RSSIs B-1 e 1-B bytes 20 e 25
Rota1_12.txt  -> RSSIs 1-2 e 2-1 bytes 21 e 24
Rota1_23.txt  -> RSSIs 2-3 e 3-2 bytes 22 e 23

ROTA 2
Bytes em que está as RSSI na sequência de subida e descida 
Rota2_B3.txt  -> RSSIs B-2 e 2-B bytes 20 e 25
Rota2_31.txt  -> RSSIs 2-1 e 1-2 bytes 21 e 24
Rota2_12.txt  -> RSSIs 1-3 e 3-1 bytes 22 e 23


ROTA 3
Bytes em que está as RSSI na sequência de subida e descida 
Rota3_B2.txt  -> RSSIs B-3 e 3-B bytes 20 e 25
Rota3_21.txt  -> RSSIs 3-1 e 1-3 bytes 21 e 24
Rota3_13.txt  -> RSSIs 1-2 e 2-1 bytes 22 e 23


'''

#apaga os arquivos que são usados somente para gerar o gráfico na tela. A cada rodada de medidas eles devem ser apacados
#arquivos de exibição Rota 1
if os.path.exists("Rota1_B1.txt"): # esse arquivo é apagado a cada rodada
   os.remove("Rota1_B1.txt")

if os.path.exists("Rota1_12.txt"): # esse arquivo é apagado a cada rodada
   os.remove("Rota1_12.txt")

if os.path.exists("Rota1_23.txt"): # esse arquivo é apagado a cada rodada
   os.remove("Rota1_23.txt")



#arquivos de exibição Rota 2
if os.path.exists("Rota2_B3.txt"): # esse arquivo é apagado a cada rodada
   os.remove("Rota2_B3.txt")

if os.path.exists("Rota2_31.txt"): # esse arquivo é apagado a cada rodada
   os.remove("Rota2_31.txt")

if os.path.exists("Rota2_31.txt"): # esse arquivo é apagado a cada rodada
   os.remove("Rota2_31.txt")



#arquivos de exibição Rota 3
if os.path.exists("Rota3_B2.txt"): # esse arquivo é apagado a cada rodada
   os.remove("Rota3_B2.txt")

if os.path.exists("Rota3_21.txt"): # esse arquivo é apagado a cada rodada
   os.remove("Rota3_21.txt")

if os.path.exists("Rota3_12.txt"): # esse arquivo é apagado a cada rodada
   os.remove("Rota3_12.txt")



#arquivos de exibição Rota 4
if os.path.exists("Rota4_B4.txt"): # esse arquivo é apagado a cada rodada
   os.remove("Rota4_B4.txt")

if os.path.exists("Rota4_42.txt"): # esse arquivo é apagado a cada rodada
   os.remove("Rota4_42.txt")

if os.path.exists("Rota4_23.txt"): # esse arquivo é apagado a cada rodada
   os.remove("Rota4_23.txt")

if os.path.exists("Rota4_31.txt"): # esse arquivo é apagado a cada rodada
   os.remove("Rota4_31.txt")
   
#CRIA NOME DOS ARQUIVOS E ABRI O ARQUIVO DE LOG PARA ESCREVER
#======ARQUIVOS ROTA 1
filename1 = strftime("LOG_Rota1_B1_%Y_%m_%d_%H-%M-%S.txt") # esse arquivo é salvo a cada rodada de medidas
filename2 = "Rota1_B1.txt" # esse arquivo será apagado a cada nova rodada de medidas
Log_Rota1_B1 = open(filename1, 'w') #abre o arquivo para escrever

filename3 = strftime("LOG_Rota1_12_%Y_%m_%d_%H-%M-%S.txt") # esse arquivo é salvo a cada rodada de medidas
filename4 = "Rota1_12.txt" # esse arquivo será apagado a cada nova rodada de medidas
Log_Rota1_12 = open(filename3, 'w')

filename5 = strftime("LOG_Rota1_23_%Y_%m_%d_%H-%M-%S.txt") # esse arquivo é salvo a cada rodada de medidas
filename6 = "Rota1_23.txt" # esse arquivo será apagado a cada nova rodada de medidas
Log_Rota1_23 = open(filename5, 'w')

filename7 = strftime("LOG_Rota1_34_%Y_%m_%d_%H-%M-%S.txt") # esse arquivo é salvo a cada rodada de medidas
filename8 = "Rota1_34.txt" # esse arquivo será apagado a cada nova rodada de medidas
Log_Rota1_34 = open(filename7, 'w')

#=======ARQUIVOS ROTA 2
filename9 = strftime("LOG_Rota2_B3_%Y_%m_%d_%H-%M-%S.txt") # esse arquivo é salvo a cada rodada de medidas
filename10 = "Rota2_B3.txt" # esse arquivo será apagado a cada nova rodada de medidas
Log_Rota2_B3 = open(filename9, 'w') #abre o arquivo para escrever

filename11 = strftime("LOG_Rota2_31_%Y_%m_%d_%H-%M-%S.txt") # esse arquivo é salvo a cada rodada de medidas
filename12 = "Rota2_31.txt" # esse arquivo será apagado a cada nova rodada de medidas
Log_Rota2_31 = open(filename11, 'w')

filename13 = strftime("LOG_Rota2_12_%Y_%m_%d_%H-%M-%S.txt") # esse arquivo é salvo a cada rodada de medidas
filename14 = "Rota2_12.txt" # esse arquivo será apagado a cada nova rodada de medidas
Log_Rota2_12 = open(filename13, 'w')

filename15 = strftime("LOG_Rota2_13_%Y_%m_%d_%H-%M-%S.txt") # esse arquivo é salvo a cada rodada de medidas
filename16 = "Rota2_13.txt" # esse arquivo será apagado a cada nova rodada de medidas
Log_Rota2_13 = open(filename15, 'w')

#=======ARQUIVOS ROTA 3
filename17 = strftime("LOG_Rota3_B2_%Y_%m_%d_%H-%M-%S.txt") # esse arquivo é salvo a cada rodada de medidas
filename18 = "Rota3_B2.txt" # esse arquivo será apagado a cada nova rodada de medidas
Log_Rota3_B2 = open(filename17, 'w') #abre o arquivo para escrever

filename19 = strftime("LOG_Rota3_21_%Y_%m_%d_%H-%M-%S.txt") # esse arquivo é salvo a cada rodada de medidas
filename20 = "Rota3_21.txt" # esse arquivo será apagado a cada nova rodada de medidas
Log_Rota3_21 = open(filename19, 'w')

filename21 = strftime("LOG_Rota3_13_%Y_%m_%d_%H-%M-%S.txt") # esse arquivo é salvo a cada rodada de medidas
filename22 = "Rota3_13.txt" # esse arquivo será apagado a cada nova rodada de medidas
Log_Rota3_13 = open(filename21, 'w')

filename23 = strftime("LOG_Rota3_42_%Y_%m_%d_%H-%M-%S.txt") # esse arquivo é salvo a cada rodada de medidas
filename24 = "Rota3_42.txt" # esse arquivo será apagado a cada nova rodada de medidas
Log_Rota3_42 = open(filename23, 'w')

#=======ARQUIVOS ROTA 4
filename25 = strftime("LOG_Rota4_B4_%Y_%m_%d_%H-%M-%S.txt") # esse arquivo é salvo a cada rodada de medidas
filename26 = "Rota4_B4.txt" # esse arquivo será apagado a cada nova rodada de medidas
Log_Rota4_B4 = open(filename25, 'w') #abre o arquivo para escrever

filename27 = strftime("LOG_Rota4_42_%Y_%m_%d_%H-%M-%S.txt") # esse arquivo é salvo a cada rodada de medidas
filename28 = "Rota4_42.txt" # esse arquivo será apagado a cada nova rodada de medidas
Log_Rota4_42 = open(filename27, 'w')

filename29 = strftime("LOG_Rota4_23_%Y_%m_%d_%H-%M-%S.txt") # esse arquivo é salvo a cada rodada de medidas
filename30 = "Rota4_23.txt" # esse arquivo será apagado a cada nova rodada de medidas
Log_Rota4_23 = open(filename29, 'w')

filename31 = strftime("LOG_Rota4_31_%Y_%m_%d_%H-%M-%S.txt") # esse arquivo é salvo a cada rodada de medidas
filename32 = "Rota4_31.txt" # esse arquivo será apagado a cada nova rodada de medidas
Log_Rota4_31 = open(filename31, 'w')

# Entra com quantas medidas vai realizar
#num_medidas = input('Entre com o número de medidas = ')
num_medidas = 1000000

# Cria o vetor Pacote
Pacote_TX =[0]*52
Pacote_RX=[0]*52

# Cria Pacote de 52 bytes com valor zero em todas as posições
for i in range(52): # faz um array com 52 bytes
   Pacote_TX[i] = 0
   Pacote_RX[i] = 0

#inicializa variáveis auxiliares
w = int(num_medidas)+1
perda_PK_RX =0
i = 0
contador = 0
PKT_down = 0

try:
   # ============ Camada Física - Transmite o pacote        
   for j in range(1,w):
   
      # ==== Camada de Transporte contagem de pacotes de descida
      PKT_down = PKT_down + 1
      if PKT_down == 256:
         PKT_down = 0
      Pacote_TX[12] = PKT_down

   # ============= ROTA 1
      arquivo = open('1_ROTA1.txt', 'r') # leitura do arquivo comandos_oficina.txt que estão nas linhas
      Pacote_TX[8] = int(arquivo.readline())
      Pacote_TX[9] = int(arquivo.readline())
      Pacote_TX[10] = int(arquivo.readline())
      Pacote_TX[11] = int(arquivo.readline())
      Pacote_TX[16] = int(arquivo.readline())
      Pacote_TX[17] = int(arquivo.readline())
      Pacote_TX[18] = int(arquivo.readline())
      Pacote_TX[19] = int(arquivo.readline())
      Pacote_TX[20] = int(arquivo.readline())      
      arquivo.close()
      
                  
      for k in range(52): # transmite pacote
         TXbyte = chr(Pacote_TX[k])
         ser.write(TXbyte.encode('latin1'))
         #print ('TX PACOTE')
               
      # Aguarda a resposta do sensor
      time.sleep(Tempo_entre_rotas)
      
   # ============= Camada Física - Recebe o pacote
      Pacote_RX = ser.read(52) # faz a leitura de 52 bytes do buffer que rec

      if len(Pacote_RX) == 52:
         #print ('RX pacote ROTA 1')

         RSSI_B_1 = calc_rssi(Pacote_RX[20])
         RSSI_1_2 = calc_rssi(Pacote_RX[21])
         RSSI_2_3 = calc_rssi(Pacote_RX[22])
         RSSI_3_2 = calc_rssi(Pacote_RX[23])
         RSSI_2_1 = calc_rssi(Pacote_RX[24])
         RSSI_1_B = calc_rssi(Pacote_RX[25])       
             
   
         print ('ROTA 1 Cont=',j,'| B-1=',RSSI_B_1,'| 1-B=',RSSI_1_B,'| 1-2 =',RSSI_1_2,'| 2-1 =',RSSI_2_1,'| 2-3=',RSSI_2_3,'| 3-2=',RSSI_3_2,'| 3-4 =',0,'| 4-3 =',0)

         # Salva no arquivo de log e arquivo de visualização
         print (time.asctime(),';',j,';',RSSI_B_1,';',RSSI_1_B,file=Log_Rota1_B1)
         Medidas_rssi_B_1 = open(filename2, 'a+')
         print (j,';',RSSI_B_1,';',RSSI_1_B,file=Medidas_rssi_B_1)
         Medidas_rssi_B_1.close()
         
         print (time.asctime(),';',j,';',RSSI_1_2,';',RSSI_2_1,file=Log_Rota1_12)
         Medidas_rssi_1_2 = open(filename4, 'a+')
         print (j,';',RSSI_1_2,';',RSSI_2_1,file=Medidas_rssi_1_2)
         Medidas_rssi_1_2.close()

         print (time.asctime(),';',j,';',RSSI_2_3,';',RSSI_3_2,file=Log_Rota1_23)
         Medidas_rssi_2_3 = open(filename6, 'a+')
         print (j,';',RSSI_2_3,';',RSSI_2_3,file=Medidas_rssi_2_3)
         Medidas_rssi_2_3.close()
            
            
      else: #Caso de erro de recepção
         perda_PK_RX = perda_PK_RX+1
         print ('Cont = ', j,' PERDEU PACOTE ROTA 1')
         
         # Salva no arquivo de log
         print (time.asctime(),';',j,';;',file=Log_Rota1_B1)
         Medidas_B_1 = open(filename2, 'a+')
         print (j,';;',perda_PK_RX,file=Medidas_B_1)
         Medidas_B_1.close()

         print (time.asctime(),';',j,';;',file=Log_Rota1_12)
         Medidas_1_2 = open(filename4, 'a+')
         print (j,';;',perda_PK_RX,file=Medidas_1_2)
         Medidas_1_2.close()

         print (time.asctime(),';',j,';;',file=Log_Rota1_23)
         Medidas_2_3 = open(filename6, 'a+')
         print (j,';;',perda_PK_RX,file=Medidas_2_3)
         Medidas_2_3.close()
         


   # ============= ROTA 2

      arquivo = open('2_ROTA2.txt', 'r') # leitura do arquivo comandos_oficina.txt que estão nas linhas
      Pacote_TX[8] = int(arquivo.readline())
      Pacote_TX[9] = int(arquivo.readline())
      Pacote_TX[10] = int(arquivo.readline())
      Pacote_TX[11] = int(arquivo.readline())
      Pacote_TX[16] = int(arquivo.readline())
      Pacote_TX[17] = int(arquivo.readline())
      Pacote_TX[18] = int(arquivo.readline())
      Pacote_TX[19] = int(arquivo.readline())
      Pacote_TX[20] = int(arquivo.readline())      
      arquivo.close()

      for k in range(52): # transmite pacote
         TXbyte = chr(Pacote_TX[k])
         ser.write(TXbyte.encode('latin1'))
         #print ('TX PACOTE')
               
      # Aguarda a resposta do sensor
      time.sleep(Tempo_entre_rotas)         

      Pacote_RX = ser.read(52) # faz a leitura de 52 bytes do buffer que rec
      if len(Pacote_RX) == 52:
         #print ('RX pacote ROTA 2')
 
         RSSI_B_3 = calc_rssi(Pacote_RX[20])  
         RSSI_3_1 = calc_rssi(Pacote_RX[21])   
         RSSI_1_2 = calc_rssi(Pacote_RX[22])
         RSSI_2_1 = calc_rssi(Pacote_RX[23])
         RSSI_1_3 = calc_rssi(Pacote_RX[24])
         RSSI_3_B = calc_rssi(Pacote_RX[25])            
 
         print ('ROTA 2 Cont=',j,'| B-3=',RSSI_B_3,'| 3-B=',RSSI_3_B,'| 3-1 =',RSSI_3_1,'| 1-3 =',RSSI_1_3,'| 1-2=',RSSI_1_2,'| 2-1=',RSSI_2_1,'| 1-3 =',0,'| 3-1 =',0)
         
         # Salva no arquivo de log e arquivo de visualização
         print (time.asctime(),';',j,';',RSSI_B_3,';',RSSI_3_B,file=Log_Rota2_B3)
         Medidas_rssi_B_3 = open(filename10, 'a+')
         print (j,';',RSSI_B_3,';',RSSI_3_B,file=Medidas_rssi_B_3)
         Medidas_rssi_B_3.close()
         
         print (time.asctime(),';',j,';',RSSI_3_1,';',RSSI_1_3,file=Log_Rota2_31)
         Medidas_rssi_3_1 = open(filename12, 'a+')
         print (j,';',RSSI_3_1,';',RSSI_1_3,file=Medidas_rssi_3_1)
         Medidas_rssi_3_1.close()

         print (time.asctime(),';',j,';',RSSI_1_2,';',RSSI_2_1,file=Log_Rota2_12)
         Medidas_rssi_1_2 = open(filename14, 'a+')
         print (j,';',RSSI_1_2,';',RSSI_2_1,file=Medidas_rssi_1_2)
         Medidas_rssi_1_2.close()
                 
      else: #Caso de erro de recepção
         perda_PK_RX = perda_PK_RX+1
         print ('Cont = ', j,' PERDEU PACOTE ROTA 2')
         
         # Salva no arquivo de log
         print (time.asctime(),';',j,';;',file=Log_Rota2_B3)
         Medidas_B_3 = open(filename10, 'a+')
         print (j,';;',perda_PK_RX,file=Medidas_B_3)
         Medidas_B_3.close()

         print (time.asctime(),';',j,';;',file=Log_Rota2_31)
         Medidas_3_1 = open(filename12, 'a+')
         print (j,';;',perda_PK_RX,file=Medidas_3_1)
         Medidas_3_1.close()

         print (time.asctime(),';',j,';;',file=Log_Rota2_12)
         Medidas_1_2 = open(filename14, 'a+')
         print (j,';;',perda_PK_RX,file=Medidas_1_2)
         Medidas_1_2.close()
         


   # ============= ROTA 3

      arquivo = open('3_ROTA3.txt', 'r') # leitura do arquivo comandos_oficina.txt que estão nas linhas
      Pacote_TX[8] = int(arquivo.readline())
      Pacote_TX[9] = int(arquivo.readline())
      Pacote_TX[10] = int(arquivo.readline())
      Pacote_TX[11] = int(arquivo.readline())
      Pacote_TX[16] = int(arquivo.readline())
      Pacote_TX[17] = int(arquivo.readline())
      Pacote_TX[18] = int(arquivo.readline())
      Pacote_TX[19] = int(arquivo.readline())
      Pacote_TX[20] = int(arquivo.readline())      
      arquivo.close()

      for k in range(52): # transmite pacote
         TXbyte = chr(Pacote_TX[k])
         ser.write(TXbyte.encode('latin1'))
         #print ('TX PACOTE')
               
      # Aguarda a resposta do sensor
      time.sleep(Tempo_entre_rotas)         

      Pacote_RX = ser.read(52) # faz a leitura de 52 bytes do buffer que rec
      if len(Pacote_RX) == 52:
         #print ('RX pacote ROTA 2')
 
         RSSI_B_2 = calc_rssi(Pacote_RX[20])  
         RSSI_2_1 = calc_rssi(Pacote_RX[21])   
         RSSI_1_3 = calc_rssi(Pacote_RX[22])
         RSSI_3_1 = calc_rssi(Pacote_RX[23])
         RSSI_1_2 = calc_rssi(Pacote_RX[24])
         RSSI_2_B = calc_rssi(Pacote_RX[25]) 

         print ('ROTA 3 Cont=',j,'| B-3=',RSSI_B_2,'| 3-B=',RSSI_2_B,'| 3-1 =',RSSI_3_1,'| 1-3 =',RSSI_1_3,'| 1-4=',0,'| 4-1=',0,'| 4-2 =',0,'| 2-4 =',0)
         
         # Salva no arquivo de log e arquivo de visualização
         print (time.asctime(),';',j,';',RSSI_B_2,';',RSSI_2_B,file=Log_Rota3_B2)
         Medidas_rssi_B_2 = open(filename18, 'a+')
         print (j,';',RSSI_B_2,';',RSSI_2_B,file=Medidas_rssi_B_2)
         Medidas_rssi_B_2.close()
         
         print (time.asctime(),';',j,';',RSSI_2_1,';',RSSI_2_1,file=Log_Rota3_21)
         Medidas_rssi_2_1 = open(filename20, 'a+')
         print (j,';',RSSI_2_1,';',RSSI_2_1,file=Medidas_rssi_2_1)
         Medidas_rssi_2_1.close()

         print (time.asctime(),';',j,';',RSSI_1_3,';',RSSI_3_1,file=Log_Rota3_13)
         Medidas_rssi_1_3 = open(filename22, 'a+')
         print (j,';',RSSI_1_3,';',RSSI_3_1,file=Medidas_rssi_1_3)
         Medidas_rssi_1_3.close()
                 
      else: #Caso de erro de recepção
         perda_PK_RX = perda_PK_RX+1
         print ('Cont = ', j,' PERDEU PACOTE ROTA 3')
         
         # Salva no arquivo de log
         print (time.asctime(),';',j,';;',file=Log_Rota3_B2)
         Medidas_B_3 = open(filename18, 'a+')
         print (j,';;',perda_PK_RX,file=Medidas_B_3)
         Medidas_B_3.close()

         print (time.asctime(),';',j,';;',file=Log_Rota3_21)
         Medidas_3_1 = open(filename20, 'a+')
         print (j,';;',perda_PK_RX,file=Medidas_3_1)
         Medidas_3_1.close()

         print (time.asctime(),';',j,';;',file=Log_Rota3_13)
         Medidas_1_4 = open(filename22, 'a+')
         print (j,';;',perda_PK_RX,file=Medidas_1_4)
         Medidas_1_4.close()

   # ============= ROTA 4




   print ('Pacotes enviados = ',j,' Pacotes perdidos = ',perda_PK_RX)
   Log_Rota1_B1.close()
   Log_Rota1_12.close()
   Log_Rota1_23.close()
   Log_Rota1_34.close()
   Log_Rota2_B3.close()
   Log_Rota2_31.close()
   Log_Rota2_12.close()
   Log_Rota2_13.close()
   Log_Rota3_B2.close()
   Log_Rota3_21.close()
   Log_Rota3_13.close()
   Log_Rota3_42.close()
   Log_Rota4_B4.close()
   Log_Rota4_42.close()
   Log_Rota4_23.close()
   Log_Rota4_31.close()   
   ser.close()
   print ('Fim da Execução')  # escreve na tela
   

except KeyboardInterrupt:
   ser.close()
   Log_Rota1_B1.close()
   Log_Rota1_12.close()
   Log_Rota1_23.close()
   Log_Rota1_34.close()
   Log_Rota2_B3.close()
   Log_Rota2_31.close()
   Log_Rota2_12.close()
   Log_Rota2_13.close()
   Log_Rota3_B2.close()
   Log_Rota3_21.close()
   Log_Rota3_13.close()
   Log_Rota3_42.close()
   Log_Rota4_B4.close()
   Log_Rota4_42.close()
   Log_Rota4_23.close()
   Log_Rota4_31.close()   

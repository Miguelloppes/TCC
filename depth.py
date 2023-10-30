'''
Algoritmo para retirar os valores capturado pelos sensores com um auxilio de um arduino

@author: Miguel Lopes de Moraes
@Version: 1.1
'''
import serial 

def depth_arduino_ultra(dist_floor,port):
    '''
    Esta função  retorna o valor capturado pelo sensor ultrassonico
    '''

    arduino = serial.Serial(port, 115200) #Numero serial de comunicao do arduino 

    line_monitor_serial = str(arduino.readline()) #Lendo os valores encontrados
    print(line_monitor_serial)
    #Retorna o valor que o sensor capturou
    dist_ultrasson = int(line_monitor_serial[6:-5])
    dist_ultrasson = float(dist_floor - dist_ultrasson)/10
    return float(dist_ultrasson)

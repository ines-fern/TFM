# Para reconocer los puertos 
import serial
#from serial import tools
import serial.tools.list_ports
# Crear subprocesos o hilos
from threading import Thread, Event
from tkinter import StringVar

class Comunicacion():
    # Metodo constructor
    def __init__(self, *args):
        super().__init__(*args)
        self.datos_flujo = StringVar()
        self.datos_temp = StringVar()
        self.dato_motor = StringVar()
        
        # Creo el objeto para la comunicacion serie con la placa
        # Puerto al que esta conectado, velocidad de comunicacion en baudios y 
        # tiempo de espera para poder realizar la conexion
        self.micro = serial.Serial()
        self.micro.timeout= 0.5

        # Listas de la velocidad en baudios que asignaremos a combobox
        self.baudrates= ["1200", "2400", "4800", "9600", "19200", "38400", "115200"]
        self.puertos= []

        # Inicializamos la senal de evento y de hilo
        #self.senal= Event()
        #self.hilo= None
        # Creamos el hilo de leer los sensores
        # indicamos que es un hilo que se esta corriendo siempre
        self.hilo1 = Thread(target= self.leer_datos, daemon=False)
        # Variable para matar el hilo
        self.isRun=True

    def puertos_disponibles(self):
        # Vemos los puertos disponibles
        self.puertos= [port.device for port in serial.tools.list_ports.comports()]

    def conexion_serial(self):
        # Excepcion si hay algun error al abrir la conexion con la placa
        try:
            self.micro.open()
        except:
            pass
        if(self.micro.is_open):
            self.iniciar_hilo()
            print("Conectado")

    def iniciar_hilo(self):
        print("llego al start")
        # Inicializamos e   l hiloe
        self.hilo1.start()

    def enviar_datos(self):
        try:
            if(self.micro.is_open):
                # Si la conexion esta abierta
                # # Escribir salto de linea y codificar
                dato = self.dato_motor.get()
                int_dato = int(dato)
                print(f"Esribo {dato}")
                print(f"INT {dato}")
                if int_dato < 10:
                    str_dato = '00'+dato
                elif int_dato < 100:
                    str_dato = '0'+dato
                else:
                    str_dato = dato
                print(f"STR {str_dato}")
                self.micro.write(str_dato.encode())
        except TypeError:
            pass

    def leer_datos(self):
        try:
            while (self.isRun and self.micro.is_open):
                # Leemos la cadena que manda la placa
                # decodificamos y quitamos todos los espacios en blanco
                data = self.micro.readline().decode("utf-8").strip()
                # Comprobamos que la cadena no este vacia
                if data:
                    print(f'Datos: {data}')
                    # Comprobamos si el dato es de temperatura (T) o de flujo (F)
                    if (data[0] == 'F'):
                        self.datos_flujo.set(data[1:])
                        print(f'Datos flujo: {self.datos_flujo.get()}')

                        # Regulamos el relé
                        valor_flujo= float(data[1:])
                        print(valor_flujo)

                        if(valor_flujo <= 0.7):
                            print('Envio 255')
                            #self.dato_motor.set('255')
                            #self.enviar_datos()
                        elif(valor_flujo >= 2.5):
                            print('Envio 000')
                            #self.dato_motor.set('000')
                            #self.enviar_datos()
             
                    elif(data[0] == 'T'):
                        self.datos_temp.set(data[1:])
                        print(f'Datos temp: {self.datos_temp.get()}')
                    else:
                         pass
                    self.isRun=False
                    while not self.isRun:
                        ...
        except TypeError:
            pass

    def desconectar(self):
        print("Llego a desconectar")
        # Detenemos el bucle del hilo
        self.isRun=False
        # Detenemos la comunicacion serie
        self.micro.close()

        # Detenemos el hilo uniendolo al principal
        #self.hilo1.join()
        print("Finalizando...")
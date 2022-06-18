#from comunicacion import Comunicacion
# Paquete utilizado para crear interfaces graficas
from tkinter import *
from tkinter import ttk
# Libreria para dibujar la gráfica dinámica
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk 
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import collections
# Libreria para crear los arrays de nuestra futura gráfica
import numpy as np


class VentanaHija(Frame): 
    def __init__(self, master=None): 
        # Asigno tamano y titulo a la ventana de base que no se ve
        self.master = master
        self.master.geometry("50x50+500+350")
        # Esconde la ventana sin destruirla
        self.master.withdraw() 

        # Crear las variables antes de llamar a create_widgets()
        self.value_motor = StringVar()
        self.flujo = IntVar()
        self.temp = IntVar()
        self.is_on = False

        # Creamos una ventana hija y le aplicamos un titulo 
        # Asigno tamaño (inamovible) y título a la ventana principal
        self.hija = Toplevel()
        self.hija.geometry('1024x725+0+0')
        self.hija.title("Control software") 
        # Color de fondo
        self.hija.config(bg="snow3")
        self.hija.resizable(0,0) 
        
        #Añadimos pestañas 
        self.notebook = ttk.Notebook(self.hija)
        # Las pestañas se pueden expandir en horizontal y vertical
        self.notebook.pack(fill="both", expand='yes')
        self.pes0 = ttk.Frame(self.notebook,height=600,width=1024)
        self.pes1 = ttk.Frame(self.notebook,height=600,width=1024)
        self.notebook.add(self.pes0,text='Visualisation')
        self.notebook.add(self.pes1,text='Control')

        # Objeto de la clase Comunicacion, pudiendo asi acceder a todos sus metodos
        self.datos_micro = None
        # self.datos_micro = Comunicacion()
        # Cuando cerramos la ventana se llama a un metodo para matar los hilos
        self.hija.protocol("WM_DELETE_WINDOW", self.cerrar)
        
        #Texto y Cuadros de Coordenadas de posición
        Button(self.hija, text="Exit", font="Helvetica", bg="#FF7779", command = self.cerrar).place(x=920, y=650) 

        # Invoca al constructor del master
        Frame.__init__(self, self.hija)

        # Funciones para crear las pestañas 
        self.pestana0(self.pes0,self.hija)
        self.pestana1(self.pes1,self.hija)

    def pestana0(self,pestania, coordenadas): 
        '''funcion que crea los elementos de la pestaña1''' 
        # Self sirve para utilizarlo en diferentes metodos
        # Creo la base de las dos grásficas
        self.figure1, self.ax1 = plt.subplots(figsize=(5,4))
        plt.title("Flow (LPM)", family="Arial")
        self.ax1.set_xlabel("Time")
        self.ax1.set_ylabel("Amplitude")
        self.ax1.set_xlim(0, 100)
        self.ax1.set_ylim(0, 7)
        self.figure1Canvas = FigureCanvasTkAgg(self.figure1, master=pestania )
        
        self.figure2, self.ax2 = plt.subplots(figsize=(5,4))
        plt.title("Temperature (ºC)", family="Arial")
        self.ax2.set_xlabel("Time")
        self.ax2.set_ylabel("Amplitude")
        self.ax2.set_xlim(0, 100)
        self.ax2.set_ylim(25, 45)
        self.figure2Canvas = FigureCanvasTkAgg(self.figure2, master=pestania)

        # Creamos las lineas donde iran los datos, una para cada sensor
        # Tiene dos listas de datos que estan vacias por ahora
        self.line1 = self.ax1.plot([], [], color='#80FF00')[0]
        self.line2 = self.ax2.plot([], [], color='#80FF00')[0]

        # Creamos las coleciones de 100 datos
        self.datos1 = collections.deque([0]*100, maxlen=100)
        self.datos2 = collections.deque([0]*100, maxlen=100)

        # Las colocamos en las ventana
        self.figure1Canvas.get_tk_widget().grid(row=0, column=0, padx=(10, 40), pady=(10, 30))
        self.figure2Canvas.get_tk_widget().grid(row=0, column=1, padx=(10, 40), pady=(10, 30))

        # Disenamos los botones
        self.bt_iniciar= Button(pestania, text="Start", font="Helvetica", bg="#D1F3C5", command=self.iniciar_animacion)
        self.bt_iniciar.grid(row=1, column=0, padx=(10, 40), pady=(10, 30))

        self.bt_pausar= Button(pestania, state="disabled", text="Stop", font="Helvetica", bg="#4169E1", command=self.pausar_animacion)
        self.bt_pausar.grid(row=1, column=1, padx=(10, 40), pady=(10, 30))
    
        #Creo los cuadros gráficos 
        LabelFrame(pestania, text="Current values", font= "Helvetica").place(height=100, width=1000, x=20, y=500) 
        # Etiquetas de de los valores actuales
        # Obtenemos los puertos y la velocidad de comunicacion del fichero Comunicacion
        Label(pestania, text="Flow:", font= "Helvetica").place(x=200,y=550)
        #Label(pestania, width=6, textvariable= self.datos_micro.datos_flujo.get()).place(x=45,y=550)
        Label(pestania,  font= "Helvetica", textvariable= self.flujo).place(x=250,y=550)

        Label(pestania, text="Temperature:", font= "Helvetica").place(x=700,y=550)
        #Label(pestania, width=6, textvariable= self.datos_micro.datos_temp.get()).place(x=545,y=550)
        Label(pestania, font= "Helvetica", textvariable= self.temp).place(x=800,y=550)


    def pestana1(self, pestania, coordenadas):
        '''Se crean los elementos de la segunda pestaña''' 
        # Activar o desactivar el motor con la varable global boolean
        # Al clickar se llama a la funcion enviar
        #motorOnOff= Checkbutton(pestania, text="Encender/Apagar Motor", variable=self.value_motor, onvalue=1, offvalue=0, command= self.enviar)
        #motorOnOff.pack(ipadx=30, ipady=90)

        # Texto
        texto= Label(pestania, bg="snow3",font= "Helvetica", text="The engine regulates itself according to the measured value of the flow meter. \nIf manual operation is required, the following controls are available to operate the engine:") 
        texto.pack(ipady=45)

        # Marco
        LabelFrame(pestania,text="Manual engine control", font= "Helvetica").place(height=450, width=1000, x=20, y=160) 
 
        # Create Label
        self.my_label = Label(pestania, text = "The engine is off",  fg = "grey", font = "Helvetica")
        self.my_label.place(x= 700, y= 300)
        
        # Define Our Images
        self.on = PhotoImage(file = "imagenes/on.png")
        self.off = PhotoImage(file = "imagenes/off.png")
        
        # Create A Button
        self.on_button = Button(pestania, image = self.off, bd = 0, command = self.switch)
        self.on_button.place(x= 710, y= 350)

        # Etiqueta y barra de estado del motor con un boton de enviar
        Label(pestania, text= "Speed").place(x= 80, y= 370)
        Button(pestania, text="Send", command=self.enviar).place(x=490,y=365)
        # Creamos un objeto de la clase escala
        Scale(pestania, from_=0, to=999, orient="horizontal", tickinterval=100,
        length=350, variable= self.value_motor).place(x=130,y=350)

    def cerrar(self):
        # Llamo a desconectar
        self.datos_micro.desconectar()
    
        # Finalizamos la ejecución y destruimos la ventana
        self.hija.quit()
        self.hija.destroy()

    
    def enviar(self):
        # Envía a la placa el valor del checkbutton (1 o 0)
        self.datos_micro.dato_motor.set(self.value_motor.get())
        print("Velocidad"+ self.value_motor.get())
        self.datos_micro.enviar_datos()
    
    

    def switch(self):
        # Determina si es on o off
        if self.is_on:
            self.on_button.config(image = self.off)
            # Envía a la placa el valor del checkbutton (1 o 0)
            self.datos_micro.dato_motor.set('000')
            self.datos_micro.enviar_datos()
            self.my_label.config(text = "The engine is off", fg = "grey")
            self.is_on = False
        else:
            self.on_button.config(image = self.on)
            # Envía a la placa el valor del checkbutton (1 o 0)
            self.datos_micro.dato_motor.set('999')
            self.datos_micro.enviar_datos()
            self.my_label.config(text = "The engine is on", fg = "green")
            self.is_on = True

    # Se ejecuta cuando vayamos a graficar
    def iniciar_animacion(self):
        # Llamamos a la funcion de graficar
        self.ani1= animation.FuncAnimation(self.figure1, self.animar, interval=5)
        self.ani2= animation.FuncAnimation(self.figure1, self.animar, interval=5)
       # Deshabilitamos graficar y habilitamos pausar
        self .bt_iniciar.config(state="disabled")
        self.bt_pausar.config(state="normal")
        self.figure1Canvas.draw()
        self.figure2Canvas.draw()

    # Animamos
    def animar(self, i):
        # Desde el objeto creado en la ventana madre de la clase Comunicacion (datos_micro)
        # podemos acceder a sus variables (datos_flujo y datos_temp)
        # Los ponemos a 0 en cada interacción
        dato1, dato2 = self.datos_micro.datos_flujo.get(), self.datos_micro.datos_temp.get()
        if len(dato1) > 0:
            #print(f'GRAFICO flujo: {dato1}')
            dato1= float(dato1)
            # Una vez separados los datos de los sensores los vamos añadiendo a sus colecciones
            self.datos1.append(dato1)
            self.line1.set_data(range(0, 100), self.datos1)
            self.flujo.set(dato1)
            self.datos_micro.datos_flujo.set('')
        elif len(dato2) > 0:
            #print(f'GRAFICO temp: {dato2}')
            dato2= float(dato2)
            self.datos2.append(dato2)
            self.line2.set_data(range(0, 100), self.datos2)
            self.temp.set(dato2)
            self.datos_micro.datos_temp.set('')
        self.datos_micro.isRun = True
        
    # Metodo pausar y reanuar, configuramos los botones
    def pausar_animacion(self):
        self.ani1.event_source.stop()
        self.ani2.event_source.stop()
        # Deshabilitamos pausar y habilitamos graficar
        self .bt_iniciar.config(state="normal")
        self.bt_pausar.config(state="disabled")
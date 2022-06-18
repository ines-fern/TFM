from comunicacion import Comunicacion
from ventanaHija import VentanaHija
# Paquete utilizado para crear interfaces graficas
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

## ## ## VENTANA PRINCIPAL ## ## ## ## 
class VentanaMadre(Frame): 
    # Constructor para el marco y todo lo que hereden las ventanas hijas
    def __init__(self, master=None): 
        #Asigno tamano y titulo a la ventana de base que no se ve
        self.master = master
        self.master.geometry("50x50+500+350")
        # esconde la ventana sin destruirla
        self.master.withdraw() 
        #self.pack()
        
        #Asigno tamano y titulo a la ventana menu
        # Toplevel funcionan como ventanas gestionadas por el master
        self.root = Toplevel()
        self.root.title("Home window")
        self.root.geometry("650x700+200+0")
        # Color de fondo
        self.root.config(bg="snow3")

        # Objeto de la clase Comunicacion, pudiendo asi acceder a todos sus metodos
        self.datos_micro = Comunicacion()
        self.actualizar_puertos()

        # Cuando cerramos la ventana se llama a un metodo para matar los hilos
        #self.master.protocol("WM_DELETE_WINDOW", self.datos_micro.desconectar())
        
        # Invoca al constructor del master
        Frame.__init__(self, self.root)
        self.crea_widgets()

    def crea_widgets(self): 
        """Crea los widgets en el frame correspondiente al objeto""" 
        titulo = Label(self.root, bg="snow3",font= ("Helvetica", 16),  fg = "blue", text="Welcome: \nPerfusion device monitoring programme in normothermia ") 
        # En lugar de declarar la ubicación precisa de un widget, el método pack() declara la posición de los widgets
        # en relación con los demás. ipady, que rellena internamente a lo largo del eje y.
        titulo.pack(ipady=25)

        # Ponemos la imagen en el frame3

        #Load an image in the script
        self.img= (Image.open("imagenes/logo7.jpg"))

        #Resize the Image using resize method
        self.resized_image= self.img.resize((300,300), Image.ANTIALIAS)
        self.new_image= ImageTk.PhotoImage(self.resized_image)
        
        # Create A Button
        portada = Label(self.root, image = self.new_image, bd = 0)
        portada.pack(pady = 50)

        # Obtenemos los puertos y la velocidad de comunicacion del fichero Comunicacion
        port= self.datos_micro.puertos
        baud= self.datos_micro.baudrates

        Label(self.root, bg="snow3", font= "Helvetica", text='Select a connection port:').pack()
        self.combobox_port= ttk.Combobox(self.root, values=port, justify="center", width=12, font="Helvetica")
        self.combobox_port.pack()

        Label(self.root, bg="snow3", font= "Helvetica", text='Select a connection speed:').pack()
        self.combobox_baud= ttk.Combobox(self.root, values=baud, justify="center", width=12, font="Helvetica")
        self.combobox_baud.pack()
        self.combobox_baud.current(3)

        # Disenamos los botones del frame1
        self.bt_conectar= Button(self.root, bg="snow3", font= "Helvetica", text='Connect', command= self.conectar_serial).pack()

        self.bt_actualizar= Button(self.root, bg="snow3", font= "Helvetica", text='Update', command= self.actualizar_puertos).pack()
        

    # CORREGIR ESTOOO
    def conectar_serial(self):
        # Asignamos lo que seleccionamos en el combobox a las variables del otro fichero
        self.datos_micro.micro.port= self.combobox_port.get()
        self.datos_micro.micro.baudrate= self.combobox_baud.get()
        #VentanaHija(Tk())
        self.datos_micro.conexion_serial()
        self.ventana_hija = VentanaHija(Tk())
        self.ventana_hija.datos_micro = self.datos_micro
        self.root.destroy()
    


    # Al pulsar el boton Actualizar
    def actualizar_puertos(self):
        self.datos_micro.puertos_disponibles()
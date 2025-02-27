import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw

class Meter(ttk.Label):
    def __init__(self, parent, indicatorcolor='#FF0000', **kwargs):
        self.font = 'helvetica 12 bold'
        self.foreground = '#FFFFFF'
        self.background = '#000000'
        self.im = Image.new('RGBA',(1000,1000))
        self.hollowcolor = '#e0e0e0'
        self.size  = 200

        self.textvariable = tk.StringVar()
        self.arcvariable = tk.IntVar(value='text')
        self.arc = None
        self.indicatorcolor = indicatorcolor
        self.arcvariable.trace_add('write',self.update_arcvariable)

        self.setup()

        super().__init__(parent,image=self.arc,compound='center',style='Meter.TLabel',
                         textvariable=self.textvariable,**kwargs)
        
    def setup(self):
        style = ttk.Style()
        style.configure('Meter.TLabel',font=self.font,foreground=self.foreground)
        if self.background:
            style.configure('Meter.TLabel',background=self.background) 
        draw = ImageDraw.Draw(self.im)
        draw.arc((0,0,990,990),0,360,self.hollowcolor,100) 

        self.arc = ImageTk.PhotoImage(self.im.resize((self.size,self.size),Image.LANCZOS))   

    def update_arcvariable(self,*args):
        angle= int(float(self.arcvariable.get())) + 90
        self.im = Image.new('RGBA',(1000,1000))
        draw = ImageDraw.Draw(self.im)
        draw.arc((0,0,990,990),0,360,self.hollowcolor,100)
        draw.arc((0,0,990,990),90,angle,self.indicatorcolor,100)
        self.arc = ImageTk.PhotoImage(self.im.resize((self.size,self.size), Image.LANCZOS))
        self.configure(image=self.arc)

def update_meters1():
    with open('VALORES/Irradiancia.txt', 'r') as f:
        valor = float(f.read().strip())
    meter1.arcvariable.set(float(valor)/3)
    meter1.textvariable.set(float(valor))
    root.after(1000, update_meters1)

def update_meters2():
    with open('VALORES/Temperatura.txt', 'r') as f:
        valor = f.read().strip()
    meter2.arcvariable.set(float(valor)*5)
    meter2.textvariable.set(float(valor))
    root.after(1000, update_meters2)

def update_meters3():
    with open('VALORES/VoltajeIN.txt', 'r') as f:
        valor = f.read().strip()
    meter3.arcvariable.set(float(valor)*6)
    meter3.textvariable.set(float(valor))
    root.after(1000, update_meters3)

def update_meters4():
    with open('VALORES/CorrienteIN.txt', 'r') as f:
        valor = f.read().strip()
    meter4.arcvariable.set(float(valor)*10)
    meter4.textvariable.set(float(valor))
    root.after(1000, update_meters4)

def update_meters5():
    with open('VALORES/PotenciaIN.txt', 'r') as f:
        valor = f.read().strip()
    meter5.arcvariable.set(float(valor))
    meter5.textvariable.set(float(valor))
    root.after(1000, update_meters5)


def update_meters6():
    with open('VALORES/VoltajeOUT.txt', 'r') as f:
        valor = f.read().strip()
    meter6.arcvariable.set(float(valor)*6)
    meter6.textvariable.set(float(valor))
    root.after(1000, update_meters6)

def update_meters7():
    with open('VALORES/CorrienteOUT.txt', 'r') as f:
        valor = f.read().strip()
    meter7.arcvariable.set(float(valor)*10)
    meter7.textvariable.set(float(valor))
    root.after(1000, update_meters7)

def update_meters8():
    with open('VALORES/PotenciaOUT.txt', 'r') as f:
        valor = f.read().strip()
    meter8.arcvariable.set(float(valor)*10)
    meter8.textvariable.set(float(valor))
    root.after(1000, update_meters8)

def update_meters9():
    with open('VALORES/Ciclodetrabajo.txt', 'r') as f:
        valor = f.read().strip()
    meter9.arcvariable.set(float(valor))
    meter9.textvariable.set(float(valor))
    root.after(1000, update_meters9)

def update_meters10():
    with open('VALORES/Contador.txt', 'r') as f:
        valor = f.read().strip()
    meter10.arcvariable.set(float(valor))
    meter10.textvariable.set(float(valor))
    root.after(1000, update_meters10)

if __name__=='__main__':
    root = tk.Tk()
    root.resizable(False,False)
    title_frame = ttk.Frame(root)
    title_frame.pack(fill=tk.X)
    # División de la ventana en tres filas
    frame1 = ttk.Frame(root)
    frame1.pack(fill=tk.X)

    title_frame1 = ttk.Frame(root)
    title_frame1.pack(fill=tk.X)

    frame2 = ttk.Frame(root)
    frame2.pack(fill=tk.X)


    
    title_bar1 = ttk.Label(title_frame, text="Irradiancia", font="helvetica 16 italic", background='#000000', foreground='#FF0000', width=20 )
    title_bar1.pack(side=tk.LEFT, padx=0)

    title_bar2 = ttk.Label(title_frame, text="Temperatura", font="helvetica 16 bold", background='#000000', foreground='#00FF00', width=20)
    title_bar2.pack(side=tk.LEFT, padx=0)

    title_bar3 = ttk.Label(title_frame, text="Voltaje IN", font="helvetica 16 bold", background='#000000', foreground='#0000FF', width=20)
    title_bar3.pack(side=tk.LEFT, padx=0)

    title_bar4 = ttk.Label(title_frame, text="Corriente IN", font="helvetica 16 bold", background='#000000', foreground='#FFFF00', width=20)
    title_bar4.pack(side=tk.LEFT, padx=0)

    title_bar5 = ttk.Label(title_frame, text="Potencia IN", font="helvetica 16 bold", background='#000000', foreground='#00FFFF', width=20)
    title_bar5.pack(side=tk.LEFT, padx=0)

    title_bar6 = ttk.Label(title_frame1, text="Voltaje OUT", font="helvetica 16 italic", background='#000000', foreground='#FF00FF', width=20 )
    title_bar6.pack(side=tk.LEFT, padx=0)

    title_bar7 = ttk.Label(title_frame1, text="Corriente OUT", font="helvetica 16 bold", background='#000000', foreground='#FFA500', width=20)
    title_bar7.pack(side=tk.LEFT, padx=0)

    title_bar8 = ttk.Label(title_frame1, text="Potencia OUT", font="helvetica 16 bold", background='#000000', foreground='#FFC0CB', width=20)
    title_bar8.pack(side=tk.LEFT, padx=0)

    title_bar9 = ttk.Label(title_frame1, text="Ciclo de trabajo", font="helvetica 16 bold", background='#000000', foreground='#A52A2A', width=20)
    title_bar9.pack(side=tk.LEFT, padx=0)

    title_bar10 = ttk.Label(title_frame1, text="Contador", font="helvetica 16 bold", background='#000000', foreground='#808080', width=20)
    title_bar10.pack(side=tk.LEFT, padx=0)

    # Creación de los medidores
    meter1 = Meter(frame1, padding=20, indicatorcolor='#FF0000')  # Cambiando el color del medidor a rojo
    meter1.pack(side=tk.LEFT)

    meter2 = Meter(frame1, padding=20, indicatorcolor='#00FF00')  # Cambiando el color del medidor a verde
    meter2.pack(side=tk.LEFT)

    meter3 = Meter(frame1, padding=20, indicatorcolor='#0000FF')  # Cambiando el color del medidor a azul
    meter3.pack(side=tk.LEFT)

    meter4 = Meter(frame1, padding=20, indicatorcolor='#FFFF00')  # Cambiando el color del medidor a amarillo
    meter4.pack(side=tk.LEFT) 

    meter5 = Meter(frame1, padding=20, indicatorcolor='#00FFFF')  # Cambiando el color del medidor a amarillo
    meter5.pack(side=tk.LEFT) 

    meter6 = Meter(frame2, padding=20, indicatorcolor='#FF00FF')  # Cambiando el color del medidor a amarillo
    meter6.pack(side=tk.LEFT) 

    meter7 = Meter(frame2, padding=20, indicatorcolor='#FFA500')  # Cambiando el color del medidor a amarillo
    meter7.pack(side=tk.LEFT) 

    meter8 = Meter(frame2, padding=20, indicatorcolor='#FFC0CB')  # Cambiando el color del medidor a amarillo
    meter8.pack(side=tk.LEFT) 

    meter9 = Meter(frame2, padding=20, indicatorcolor='#A52A2A')  # Cambiando el color del medidor a amarillo
    meter9.pack(side=tk.LEFT)

    meter10 = Meter(frame2, padding=20, indicatorcolor='#808080')  # Cambiando el color del medidor a amarillo
    meter10.pack(side=tk.LEFT)

    update_meters1()
    update_meters2()
    update_meters3()
    update_meters4()
    update_meters5() 
    update_meters6() 
    update_meters7()
    update_meters8()   
    update_meters9()
    update_meters10()    

    root.mainloop()

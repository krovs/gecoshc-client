from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class WelcomeHC:

    def __init__(self):

        root = Tk()

        root.title("Preconfiguración de Helpchannel")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.nombre = StringVar()
        nombre_entry = ttk.Entry(mainframe, width=18, textvariable=self.nombre)
        nombre_entry.grid(column=2, row=2, sticky=(W, E))

        self.ip = StringVar()
        ip_entry = ttk.Entry(mainframe, width=7, textvariable=self.ip)
        ip_entry.grid(column=2, row=3, sticky=(W, E))

        ttk.Button(mainframe, text="Conectar", command=self.validate).grid(column=2, row=5, sticky=E)

        ttk.Label(mainframe, text="Datos de conexión").grid(column=1, row=1, sticky=W)
        ttk.Label(mainframe, text="Nombre").grid(column=1, row=2, sticky=W)
        ttk.Label(mainframe, text="Servidor").grid(column=1, row=3, sticky=W)

        for child in mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        nombre_entry.focus()
        root.bind("<Return>", self.validate)

        root.eval('tk::PlaceWindow . center')
        
        root.mainloop()

    def validate(self, *args):
        
        if str(self.nombre.get()) == '':
            messagebox.showerror(title='Error', message='El nombre de usuario no puede estar vacío.')

        if str(self.ip.get()) == '':
            messagebox.showerror(title='Error', message='La IP/nombre del host no puede estar vacío.')

        
    
if __name__ == "__main__":

    app = WelcomeHC()
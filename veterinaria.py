import tkinter as tk
from tkinter import ttk
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Time, Numeric, TIMESTAMP
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# Configuración de la base de datos
DATABASE_URL = "postgresql://postgres:root@localhost/VeterinariaProyecto"

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelos de la base de datos
class AuditoriaCitas(Base):
    __tablename__ = 'auditoriacitas'
    auditoriaid = Column(Integer, primary_key=True, autoincrement=True)
    citaid = Column(Integer)
    fecha = Column(Date)
    hora = Column(Time)
    mascotaid = Column(Integer)
    veterinarioid = Column(Integer)
    descripcion = Column(String(200))
    fecharegistro = Column(TIMESTAMP, default="CURRENT_TIMESTAMP")

class Citas(Base):
    __tablename__ = 'citas'
    citaid = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date)
    hora = Column(Time)
    mascotaid = Column(Integer, ForeignKey('mascotas.mascotaid'))
    veterinarioid = Column(Integer, ForeignKey('veterinarios.veterinarioid'))
    descripcion = Column(String(200))

class Clientes(Base):
    __tablename__ = 'clientes'
    clienteid = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nombre = Column(String(50), index=True)
    apellido = Column(String(50), index=True)
    direccion = Column(String(100))
    telefono = Column(String(20))
    email = Column(String(100), unique=True, index=True)

class DetalleVenta(Base):
    __tablename__ = 'detalleventa'
    ventaid = Column(Integer, ForeignKey('ventas.ventaid'), primary_key=True)
    productoid = Column(Integer, ForeignKey('productos.productoid'), primary_key=True)
    cantidad = Column(Integer)
    preciounitario = Column(Numeric(10, 2))

class Mascotas(Base):
    __tablename__ = 'mascotas'
    mascotaid = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), index=True)
    especie = Column(String(50))
    raza = Column(String(50))
    fechanacimiento = Column(Date)
    clienteid = Column(Integer, ForeignKey('clientes.clienteid'))

class Productos(Base):
    __tablename__ = 'productos'
    productoid = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), index=True)
    descripcion = Column(String(200))
    precio = Column(Numeric(10, 2))

class Tratamientos(Base):
    __tablename__ = 'tratamientos'
    tratamientoid = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), index=True)
    descripcion = Column(String(200))

class TratamientosPorCita(Base):
    __tablename__ = 'tratamientosporcita'
    citaid = Column(Integer, ForeignKey('citas.citaid'), primary_key=True)
    tratamientoid = Column(Integer, ForeignKey('tratamientos.tratamientoid'), primary_key=True)
    dosis = Column(String(50))
    duracion = Column(Integer)

class Ventas(Base):
    __tablename__ = 'ventas'
    ventaid = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date)
    clienteid = Column(Integer, ForeignKey('clientes.clienteid'))
    total = Column(Numeric(10, 2))

class Veterinarios(Base):
    __tablename__ = 'veterinarios'
    veterinarioid = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), index=True)
    apellido = Column(String(50), index=True)
    especialidad = Column(String(100))
    telefono = Column(String(20))
    email = Column(String(100), unique=True, index=True)

# Crear las tablas en la base de datos (si no existen)
Base.metadata.create_all(bind=engine)

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Clase de la aplicación de Tkinter
class VeterinariaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Veterinaria Proyecto")
        
        self.create_widgets()
        
    def create_widgets(self):
        self.tabControl = ttk.Notebook(self.root)
        
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        
        self.tabControl.add(self.tab1, text ='Clientes')
        self.tabControl.add(self.tab2, text ='Mascotas')
        
        self.tabControl.pack(expand = 1, fill ="both")
        
        self.create_client_tab()
        self.create_mascota_tab()
    
    def create_client_tab(self):
        self.client_tree = ttk.Treeview(self.tab1, columns=('nombre', 'apellido', 'direccion', 'telefono', 'email'), show='headings')
        self.client_tree.heading('nombre', text='Nombre')
        self.client_tree.heading('apellido', text='Apellido')
        self.client_tree.heading('direccion', text='Direccion')
        self.client_tree.heading('telefono', text='Telefono')
        self.client_tree.heading('email', text='Email')
        self.client_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.client_form = tk.Frame(self.tab1)
        self.client_form.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.client_name_label = tk.Label(self.client_form, text="Nombre:")
        self.client_name_label.grid(row=0, column=0)
        self.client_name_entry = tk.Entry(self.client_form)
        self.client_name_entry.grid(row=0, column=1)
        
        self.client_apellido_label = tk.Label(self.client_form, text="Apellido:")
        self.client_apellido_label.grid(row=1, column=0)
        self.client_apellido_entry = tk.Entry(self.client_form)
        self.client_apellido_entry.grid(row=1, column=1)
        
        self.client_direccion_label = tk.Label(self.client_form, text="Direccion:")
        self.client_direccion_label.grid(row=2, column=0)
        self.client_direccion_entry = tk.Entry(self.client_form)
        self.client_direccion_entry.grid(row=2, column=1)
        
        self.client_telefono_label = tk.Label(self.client_form, text="Telefono:")
        self.client_telefono_label.grid(row=3, column=0)
        self.client_telefono_entry = tk.Entry(self.client_form)
        self.client_telefono_entry.grid(row=3, column=1)
        
        self.client_email_label = tk.Label(self.client_form, text="Email:")
        self.client_email_label.grid(row=4, column=0)
        self.client_email_entry = tk.Entry(self.client_form)
        self.client_email_entry.grid(row=4, column=1)
        
        self.client_add_button = tk.Button(self.client_form, text="Agregar", command=self.add_client)
        self.client_add_button.grid(row=5, column=0, columnspan=2)
        
    def add_client(self):
        db = next(get_db())
        new_client = Clientes(
            nombre=self.client_name_entry.get(),
            apellido=self.client_apellido_entry.get(),
            direccion=self.client_direccion_entry.get(),
            telefono=self.client_telefono_entry.get(),
            email=self.client_email_entry.get()
        )
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
        db.close()
        self.refresh_clients()

    def refresh_clients(self):
        for item in self.client_tree.get_children():
            self.client_tree.delete(item)
        
        db = next(get_db())
        clients = db.query(Clientes).all()
        for client in clients:
            self.client_tree.insert('', 'end', values=(client.nombre, client.apellido, client.direccion, client.telefono, client.email))
        db.close()
    
    def create_mascota_tab(self):
        # Implementa la pestaña para gestionar mascotas aquí
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = VeterinariaApp(root)
    root.mainloop()









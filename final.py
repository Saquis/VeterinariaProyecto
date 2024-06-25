import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttkb
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Time, Numeric, TIMESTAMP
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# Configuración de la base de datos
DATABASE_URL = "postgresql://postgres:root@localhost/VeterinariaProyecto"

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelos de la base de datos
class Clientes(Base):
    __tablename__ = 'clientes'
    clienteid = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), index=True)
    apellido = Column(String(50), index=True)
    direccion = Column(String(100))
    telefono = Column(String(20))
    email = Column(String(100), unique=True, index=True)

class Mascotas(Base):
    __tablename__ = 'mascotas'
    mascotaid = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), index=True)
    especie = Column(String(50))
    raza = Column(String(50))
    fechanacimiento = Column(Date)
    clienteid = Column(Integer, ForeignKey('clientes.clienteid'))

class Veterinarios(Base):
    __tablename__ = 'veterinarios'
    veterinarioid = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), index=True)
    apellido = Column(String(50), index=True)
    especialidad = Column(String(100))
    telefono = Column(String(20))
    email = Column(String(100), unique=True, index=True)

class Citas(Base):
    __tablename__ = 'citas'
    citaid = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    mascotaid = Column(Integer, ForeignKey('mascotas.mascotaid'), nullable=False)
    veterinarioid = Column(Integer, ForeignKey('veterinarios.veterinarioid'), nullable=False)
    descripcion = Column(String(200))

# Crear las tablas en la base de datos (si no existen)
Base.metadata.create_all(bind=engine)

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class VeterinariaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Veterinaria")
        self.style = ttkb.Style()
        self.style.theme_use('flatly')

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        self.clients_frame = ttk.Frame(self.notebook)
        self.pets_frame = ttk.Frame(self.notebook)
        self.appointments_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.clients_frame, text='Clientes')
        self.notebook.add(self.pets_frame, text='Mascotas')
        self.notebook.add(self.appointments_frame, text='Citas')

        self.setup_clients_ui()
        self.setup_pets_ui()
        self.setup_appointments_ui()

    def setup_clients_ui(self):
        clients_label_frame = ttk.LabelFrame(self.clients_frame, text='Clientes')
        clients_label_frame.pack(fill='both', expand=True, padx=20, pady=10)

        self.client_tree = ttk.Treeview(clients_label_frame, columns=('Nombre', 'Apellido', 'Direccion', 'Telefono', 'Email'), show='headings')
        self.client_tree.heading('Nombre', text='Nombre')
        self.client_tree.heading('Apellido', text='Apellido')
        self.client_tree.heading('Direccion', text='Direccion')
        self.client_tree.heading('Telefono', text='Telefono')
        self.client_tree.heading('Email', text='Email')
        self.client_tree.pack(fill='both', expand=True)

        form_frame = ttk.Frame(clients_label_frame)
        form_frame.pack(fill='x', padx=20, pady=10)

        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.client_name_entry = ttk.Entry(form_frame)
        self.client_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Apellido:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.client_lastname_entry = ttk.Entry(form_frame)
        self.client_lastname_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Direccion:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.client_address_entry = ttk.Entry(form_frame)
        self.client_address_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Telefono:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.client_phone_entry = ttk.Entry(form_frame)
        self.client_phone_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Email:").grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.client_email_entry = ttk.Entry(form_frame)
        self.client_email_entry.grid(row=4, column=1, padx=5, pady=5)

        add_client_button = ttkb.Button(form_frame, text="Agregar Cliente", style="success.TButton", command=self.add_client)
        add_client_button.grid(row=5, column=0, columnspan=2, pady=10)
        
        delete_client_button = ttkb.Button(form_frame, text="Eliminar Cliente", style="danger.TButton", command=self.delete_client)
        delete_client_button.grid(row=6, column=0, columnspan=2, pady=10)

        

        self.refresh_clients()

    def setup_pets_ui(self):
        pets_label_frame = ttk.LabelFrame(self.pets_frame, text='Mascotas')
        pets_label_frame.pack(fill='both', expand=True, padx=20, pady=10)

        self.pet_tree = ttk.Treeview(pets_label_frame, columns=('Nombre', 'Especie', 'Raza', 'Fecha de Nacimiento', 'Cliente ID'), show='headings')
        self.pet_tree.heading('Nombre', text='Nombre')
        self.pet_tree.heading('Especie', text='Especie')
        self.pet_tree.heading('Raza', text='Raza')
        self.pet_tree.heading('Fecha de Nacimiento', text='Fecha de Nacimiento')
        self.pet_tree.heading('Cliente ID', text='Cliente ID')
        self.pet_tree.pack(fill='both', expand=True)

        form_frame = ttk.Frame(pets_label_frame)
        form_frame.pack(fill='x', padx=20, pady=10)

        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.pet_name_entry = ttk.Entry(form_frame)
        self.pet_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Especie:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.pet_species_entry = ttk.Entry(form_frame)
        self.pet_species_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Raza:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.pet_breed_entry = ttk.Entry(form_frame)
        self.pet_breed_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Fecha de Nacimiento:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.pet_birthdate_entry = ttk.Entry(form_frame)
        self.pet_birthdate_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Cliente ID:").grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.pet_client_id_entry = ttk.Entry(form_frame)
        self.pet_client_id_entry.grid(row=4, column=1, padx=5, pady=5)

        add_pet_button = ttkb.Button(form_frame, text="Agregar Mascota", style="success.TButton", command=self.add_pet)
        add_pet_button.grid(row=5, column=0, columnspan=2, pady=10)

        delete_pet_button = ttkb.Button(form_frame, text="Eliminar Mascota", style="danger.TButton", command=self.delete_pet)
        delete_pet_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.refresh_pets()

    def setup_appointments_ui(self):
        appointments_label_frame = ttk.LabelFrame(self.appointments_frame, text='Citas')
        appointments_label_frame.pack(fill='both', expand=True, padx=20, pady=10)

        self.appointment_tree = ttk.Treeview(appointments_label_frame, columns=('Fecha', 'Hora', 'Mascota ID', 'Veterinario ID', 'Descripcion'), show='headings')
        self.appointment_tree.heading('Fecha', text='Fecha')
        self.appointment_tree.heading('Hora', text='Hora')
        self.appointment_tree.heading('Mascota ID', text='Mascota ID')
        self.appointment_tree.heading('Veterinario ID', text='Veterinario ID')
        self.appointment_tree.heading('Descripcion', text='Descripcion')
        self.appointment_tree.pack(fill='both', expand=True)

        form_frame = ttk.Frame(appointments_label_frame)
        form_frame.pack(fill='x', padx=20, pady=10)

        ttk.Label(form_frame, text="Fecha (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.appointment_date_entry = ttk.Entry(form_frame)
        self.appointment_date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Hora (HH:MM):").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.appointment_time_entry = ttk.Entry(form_frame)
        self.appointment_time_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Mascota ID:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.appointment_pet_id_entry = ttk.Entry(form_frame)
        self.appointment_pet_id_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Veterinario ID:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.appointment_vet_id_entry = ttk.Entry(form_frame)
        self.appointment_vet_id_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Descripcion:").grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.appointment_description_entry = ttk.Entry(form_frame)
        self.appointment_description_entry.grid(row=4, column=1, padx=5, pady=5)

        add_appointment_button = ttkb.Button(form_frame, text="Agregar Cita", style="success.TButton", command=self.add_appointment)
        add_appointment_button.grid(row=5, column=0, columnspan=2, pady=10)

        delete_appointment_button = ttkb.Button(form_frame, text="Eliminar Cita", style="danger.TButton", command=self.delete_appointment)
        delete_appointment_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.refresh_appointments()

    def add_client(self):
        db = next(get_db())
        new_client = Clientes(
            nombre=self.client_name_entry.get(),
            apellido=self.client_lastname_entry.get(),
            direccion=self.client_address_entry.get(),
            telefono=self.client_phone_entry.get(),
            email=self.client_email_entry.get()
        )
        db.add(new_client)
        db.commit()
        db.close()
        self.refresh_clients()

    def add_pet(self):
        db = next(get_db())
        new_pet = Mascotas(
            nombre=self.pet_name_entry.get(),
            especie=self.pet_species_entry.get(),
            raza=self.pet_breed_entry.get(),
            fechanacimiento=self.pet_birthdate_entry.get(),
            clienteid=self.pet_client_id_entry.get()
        )
        db.add(new_pet)
        db.commit()
        db.close()
        self.refresh_pets()

    def add_appointment(self):
        db = next(get_db())
        new_appointment = Citas(
            fecha=self.appointment_date_entry.get(),
            hora=self.appointment_time_entry.get(),
            mascotaid=self.appointment_pet_id_entry.get(),
            veterinarioid=self.appointment_vet_id_entry.get(),
            descripcion=self.appointment_description_entry.get()
        )
        db.add(new_appointment)
        db.commit()
        db.close()
        self.refresh_appointments()

    def delete_client(self):
        selected_item = self.client_tree.selection()
        if selected_item:
            item = self.client_tree.item(selected_item)
            client_email = item['values'][4]
            db = next(get_db())
            client = db.query(Clientes).filter_by(email=client_email).first()
            db.delete(client)
            db.commit()
            db.close()
            self.refresh_clients()

    def delete_pet(self):
        selected_item = self.pet_tree.selection()
        if selected_item:
            item = self.pet_tree.item(selected_item)
            pet_id = item['values'][4]
            db = next(get_db())
            pet = db.query(Mascotas).filter_by(mascotaid=pet_id).first()
            db.delete(pet)
            db.commit()
            db.close()
            self.refresh_pets()

    def delete_appointment(self):
        selected_item = self.appointment_tree.selection()
        if selected_item:
            item = self.appointment_tree.item(selected_item)
            appointment_id = item['values'][0]
            db = next(get_db())
            appointment = db.query(Citas).filter_by(citaid=appointment_id).first()
            db.delete(appointment)
            db.commit()
            db.close()
            self.refresh_appointments()

    def refresh_clients(self):
        for item in self.client_tree.get_children():
            self.client_tree.delete(item)
        
        db = next(get_db())
        clients = db.query(Clientes).all()
        for client in clients:
            self.client_tree.insert('', 'end', values=(client.nombre, client.apellido, client.direccion, client.telefono, client.email))
        db.close()

    def refresh_pets(self):
        for item in self.pet_tree.get_children():
            self.pet_tree.delete(item)
        
        db = next(get_db())
        pets = db.query(Mascotas).all()
        for pet in pets:
            self.pet_tree.insert('', 'end', values=(pet.nombre, pet.especie, pet.raza, pet.fechanacimiento, pet.clienteid))
        db.close()

    def refresh_appointments(self):
        for item in self.appointment_tree.get_children():
            self.appointment_tree.delete(item)
        
        db = next(get_db())
        appointments = db.query(Citas).all()
        for appointment in appointments:
            self.appointment_tree.insert('', 'end', values=(appointment.fecha, appointment.hora, appointment.mascotaid, appointment.veterinarioid, appointment.descripcion))
        db.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = VeterinariaApp(root)
    root.mainloop()

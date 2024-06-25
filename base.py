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




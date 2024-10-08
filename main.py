import flet as ft
from pymongo import MongoClient
from bson.objectid import ObjectId

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["alumnos"]
collection = db["datos"]

# Función para insertar un nuevo estudiante en MongoDB
def crear_estudiante(nombre, telefono, sexo, clase, edad):
    estudiante = {
        "Nombre": nombre,
        "Telefono": int(telefono),
        "Sexo": sexo,
        "Clase": clase,
        "Edad": int(edad)
    }
    collection.insert_one(estudiante)

# Función para leer todos los estudiantes
def leer_estudiantes():
    return list(collection.find())

# Función para actualizar un estudiante por su ObjectId
def actualizar_estudiante(id, nuevos_datos):
    collection.update_one({"_id": ObjectId(id)}, {"$set": nuevos_datos})

# Función para eliminar un estudiante por su ObjectId
def eliminar_estudiante(id):
    collection.delete_one({"_id": ObjectId(id)})

# Interfaz con Flet
def main(page: ft.Page):

    # Agregar un título a la ventana
    page.title = "CRUD de Estudiantes"

    # Campos de entrada
    id_field = ft.TextField(label="ID (solo para actualización/eliminación)")
    nombre = ft.TextField(label="Nombre")
    telefono = ft.TextField(label="Teléfono")
    sexo = ft.TextField(label="Sexo")
    clase = ft.TextField(label="Clase")
    edad = ft.TextField(label="Edad")

    # Lista para mostrar los registros de estudiantes
    lista_estudiantes = ft.ListView(expand=1, spacing=10)

    def cargar_estudiantes():
        lista_estudiantes.controls.clear()  # Limpiar la lista antes de cargar los nuevos datos
        estudiantes = leer_estudiantes()
        for estudiante in estudiantes:
            lista_estudiantes.controls.append(
                ft.Text(f"{str(estudiante['_id'])}: {estudiante['Nombre']} - {estudiante['Telefono']} - {estudiante['Sexo']} - {estudiante['Clase']} - {estudiante['Edad']}")
            )
        page.update()

    # Función para agregar un nuevo estudiante
    def agregar_estudiante(e):
        crear_estudiante(nombre.value, telefono.value, sexo.value, clase.value, edad.value)
        cargar_estudiantes()

    # Función para actualizar un estudiante por ID
    def actualizar_estudiante_registro(e):
        nuevos_datos = {
            "Nombre": nombre.value,
            "Telefono": int(telefono.value),
            "Sexo": sexo.value,
            "Clase": clase.value,
            "Edad": int(edad.value)
        }
        actualizar_estudiante(id_field.value, nuevos_datos)
        cargar_estudiantes()

    # Función para eliminar un estudiante por ID
    def eliminar_estudiante_registro(e):
        eliminar_estudiante(id_field.value)
        cargar_estudiantes()

    # Botones para realizar las operaciones de CRUD
    agregar_btn = ft.ElevatedButton("Agregar Estudiante", on_click=agregar_estudiante)
    actualizar_btn = ft.ElevatedButton("Actualizar Estudiante", on_click=actualizar_estudiante_registro)
    eliminar_btn = ft.ElevatedButton("Eliminar Estudiante", on_click=eliminar_estudiante_registro)

    # Layout de la aplicación
    page.add(
        id_field,
        nombre,
        telefono,
        sexo,
        clase,
        edad,
        ft.Row([agregar_btn, actualizar_btn, eliminar_btn]),
        lista_estudiantes
    )

    cargar_estudiantes()  # Cargar la lista inicial de estudiantes

# Ejecutar la app Flet
ft.app(target=main)

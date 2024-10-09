import flet as ft
from pymongo import MongoClient
from bson.objectid import ObjectId
import re  # Importamos re para usar expresiones regulares

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["alumnos"]  # Base de datos "alumnos"
collection = db["datos"]  # Colección "datos"

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

# Función para buscar un estudiante por su ObjectId
def buscar_estudiante(id):
    return collection.find_one({"_id": ObjectId(id)})

# Interfaz con Flet
def main(page: ft.Page):

    # Agregar un título a la ventana
    page.title = "CRUD de Estudiantes"

    # Validación del nombre para permitir solo letras del alfabeto español
    def validar_nombre():
        nombre_valor = nombre.value
        # Expresión regular para validar solo letras, incluyendo acentos y ñ
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", nombre_valor):
            nombre_error.value = "El nombre solo puede contener letras y espacios."
        else:
            nombre_error.value = ""  # Limpiar el mensaje de error si es válido
        
        validar_botones()  # Revalidar los botones
        page.update()

    # Validación del teléfono para que sea un número entero de 10 dígitos
    def validar_telefono():
        telefono_valor = telefono.value
        # Expresión regular para validar un número entero de 10 dígitos
        if not re.match(r"^\d{10}$", telefono_valor):
            telefono_error.value = "El teléfono debe tener exactamente 10 dígitos."
        else:
            telefono_error.value = ""  # Limpiar el mensaje de error si es válido
        
        validar_botones()  # Revalidar los botones
        page.update()

    # Campos de entrada
    id_field = ft.TextField(label="ID (solo para actualización/eliminación)", on_change=lambda e: validar_botones())
    nombre = ft.TextField(label="Nombre", on_change=lambda e: validar_nombre())  # Validación en tiempo real
    telefono = ft.TextField(label="Teléfono", on_change=lambda e: validar_telefono())  # Validación en tiempo real
    edad = ft.TextField(label="Edad", on_change=lambda e: validar_edad())
    
    # RadioGroup para seleccionar el sexo
    sexo_seleccionado = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="Masculino", label="Masculino"),  # Primero "Masculino"
        ft.Radio(value="Femenino", label="Femenino")  # Luego "Femenino"
    ]), value="Masculino")  # Valor por defecto "Masculino"
    
    # Dropdown para seleccionar la clase
    clase_seleccionada = ft.Dropdown(
        label="Clase",
        options=[
            ft.dropdown.Option("Sistemas"),
            ft.dropdown.Option("Industrial"),
            ft.dropdown.Option("Ciencias")
        ],
        value="Sistemas"  # Valor por defecto
    )
    
    # Mensaje de error para la validación de nombre, teléfono y edad
    nombre_error = ft.Text(value="", color="red")
    telefono_error = ft.Text(value="", color="red")
    edad_error = ft.Text(value="", color="red")
    id_error = ft.Text(value="", color="red")  # Mensaje de error para el campo ID
    agregar_error = ft.Text(value="", color="red")  # Mensaje de error para agregar estudiante

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
        # Validar que los campos no estén vacíos
        if not nombre.value.strip() or not telefono.value.strip() or not edad.value.strip():
            agregar_error.value = "Todos los campos deben estar llenos para agregar un estudiante."
            return
        
        agregar_error.value = ""  # Limpiar el mensaje de error
        crear_estudiante(nombre.value, telefono.value, sexo_seleccionado.value, clase_seleccionada.value, edad.value)

        # Limpiar los campos
        id_field.value = ""
        nombre.value = ""
        telefono.value = ""
        edad.value = ""

        cargar_estudiantes()

    # Función para actualizar un estudiante por ID
    def actualizar_estudiante_registro(e):
        nuevos_datos = {
            "Nombre": nombre.value,
            "Telefono": int(telefono.value),
            "Sexo": sexo_seleccionado.value,
            "Clase": clase_seleccionada.value,
            "Edad": int(edad.value)
        }
        actualizar_estudiante(id_field.value, nuevos_datos)

        # Limpiar los campos
        id_field.value = ""
        nombre.value = ""
        telefono.value = ""
        edad.value = ""

        cargar_estudiantes()

    # Función para eliminar un estudiante por ID
    def eliminar_estudiante_registro(e):
        eliminar_estudiante(id_field.value)
        cargar_estudiantes()

    # Función para buscar un estudiante por ID
    def buscar_estudiante_por_id(e):
        if id_field.value.strip() == "":  # Validar que el campo ID no esté vacío
            id_error.value = "El campo ID no puede estar vacío."
            nombre.value = ""
            telefono.value = ""
            sexo_seleccionado.value = "Masculino"
            clase_seleccionada.value = "Sistemas"
            edad.value = ""
            #return
        elif not re.match(r"^[0-9a-fA-F]{24}$", id_field.value.strip()): # Validar que el ID sea un string hexadecimal de 24 caracteres
            id_error.value = "El ID debe ser un string hexadecimal de 24 caracteres."
            nombre.value = ""
            telefono.value = ""
            sexo_seleccionado.value = "Masculino"
            clase_seleccionada.value = "Sistemas"
            edad.value = ""
            #return
        else:
            id_error.value = ""  # Limpiar el mensaje de error si se ingresa un ID válido
            estudiante = buscar_estudiante(id_field.value)
            if estudiante:
                nombre.value = estudiante['Nombre']
                telefono.value = str(estudiante['Telefono'])
                sexo_seleccionado.value = estudiante['Sexo']
                clase_seleccionada.value = estudiante['Clase']
                edad.value = str(estudiante['Edad'])
                nombre_error.value = ""
                telefono_error.value = ""
            else:
                nombre.value = ""
                telefono.value = ""
                sexo_seleccionado.value = "Masculino"
                clase_seleccionada.value = "Sistemas"
                edad.value = ""
                id_error.value = "Estudiante no encontrado."
                nombre_error.value = ""
                telefono_error.value = ""
        
        validar_botones()  # Revalidar los botones después de la búsqueda
        page.update()

    # Validar los botones en función del contenido del campo ID
    def validar_botones():
        id_valor = id_field.value.strip()
        nombre_valor = nombre.value.strip()
        telefono_valor = telefono.value.strip()
        edad_valor = 0
        
        if edad.value.strip() and not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", edad.value):
            edad_valor = int(edad.value)

        id_flag = bool(re.match(r"^[0-9a-fA-F]{24}$", id_valor))
        nombre_flag = bool(re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", nombre_valor))
        telefono_flag = bool(re.match(r"^\d{10}$", telefono_valor))
        edad_flag = bool(edad_valor > 0)

        if id_flag and nombre_flag and telefono_flag and edad_flag: # Si hay contenido en id, nombre, telefono y edad
            actualizar_btn.disabled = False
        else: # Si no hay contenido en id, nombre, telefono y edad
            actualizar_btn.disabled = True

        if nombre_flag and telefono_flag and edad_flag: # Si hay contenido en nombre, telefono y edad
            agregar_btn.disabled = False
        else:
            agregar_btn.disabled = True # Si no hay contenido en nombre, telefono y edad
            
        if id_flag:  # Si hay contenido en el campo ID
            eliminar_btn.disabled = False
            buscar_btn.disabled = False
        else:  # Si no hay contenido en el campo ID
            eliminar_btn.disabled = True
            buscar_btn.disabled = True
        page.update()  # Actualizar la interfaz

    # Validar que el campo edad solo acepte enteros mayores a 0
    def validar_edad():
        try:
            # Convertir la edad a un número entero
            edad_valor = int(edad.value)
            if edad_valor <= 0:  # Verificar si es mayor a 0
                edad_error.value = "La edad debe ser un número mayor que 0."
            else:
                edad_error.value = ""  # Limpiar el mensaje de error
            
            validar_botones()  # Revalidar botones si la edad es válida
        except ValueError:
            # Si no es un número válido, mostrar el error
            edad_error.value = "La edad debe ser un número entero válido."
        page.update()

    # Botones para realizar las operaciones de CRUD
    agregar_btn = ft.ElevatedButton("Agregar Estudiante", on_click=agregar_estudiante, disabled=True)
    actualizar_btn = ft.ElevatedButton("Actualizar Estudiante", on_click=actualizar_estudiante_registro, disabled=True)
    eliminar_btn = ft.ElevatedButton("Eliminar Estudiante", on_click=eliminar_estudiante_registro, disabled=True)
    buscar_btn = ft.ElevatedButton("Buscar Estudiante", on_click=buscar_estudiante_por_id, disabled=True)

    # Layout de la aplicación
    page.add(
        id_field,
        id_error,  # Mensaje de error para el campo ID
        nombre,
        nombre_error,  # Mensaje de error para el campo de nombre
        telefono,
        telefono_error,  # Mensaje de error para el campo de teléfono
        sexo_seleccionado,  # Reemplazamos el TextField con el RadioGroup
        clase_seleccionada,  # Reemplazamos el TextField de clase con el Dropdown
        edad,
        edad_error,  # Mensaje de error para el campo de edad
        agregar_error,  # Mensaje de error para agregar estudiante
        ft.Row([agregar_btn, actualizar_btn, eliminar_btn, buscar_btn]),  # Incluimos el botón de búsqueda
        lista_estudiantes
    )

    cargar_estudiantes()  # Cargar la lista inicial de estudiantes

# Ejecutar la app Flet
ft.app(target=main)

from flask import Flask, render_template
from flask import request, redirect, url_for
import requests
from db_utils import ini_db
from blueprints.productos import productos_db
from blueprints.usuarios import usuarios_bp


servidor = Flask(__name__)

#Iniciamos la BD
ini_db()

#Registrar los blueprint
servidor.register_blueprint(productos_db)
servidor.register_blueprint(usuarios_bp, url_prefix='/api')

#cambiamos url backend usuarios
backend_url_usuarios = 'http://127.0.0.1:5000/api/usuarios'

#Defino la función para el index
@servidor.route('/')
def home():
    return render_template('index.html')

#Función para leer todos los usuarios
@servidor.route('/usuarios')
def listar_usuarios():
    response = requests.get(backend_url_usuarios)
    usuarios = response.json() if response.status_code == 200 else []
    return render_template("usuarios.html", usuarios=usuarios)

#Función para leer un solo usuario
@servidor.route("/usuarios/<int:id>")
def usuario_detalle(id):
    response = requests.get(f"{backend_url_usuarios}/{id}")
    if response.status_code == 200:
        usuario = response.json()
        return render_template("editar_usuario.html", usuario=usuario)
    else:
        return redirect(url_for("listar_usuarios"))
    
@servidor.route("/crear_usuario", methods= ["GET", "POST"])
def crear_usuario():
    if request.method == "POST":
        usuario = {
            "nombre": request.form["nombre"],
            "apellido": request.form["apellido"],
            "telefono": request.form["telefono"],
            "direccion": request.form["direccion"]
        }
        response = requests.post(backend_url_usuarios, json=usuario)
        if response.status_code == 201:
            return redirect(url_for("listar_usuarios"))
    return render_template("crear_usuario.html")

#Editar un usuario
@servidor.route("/editar_usuario/<int:id>", methods=["GET", "POST"])
def editar_usuario(id):
    if request.method == "POST":
        usuario = {
            "nombre": request.form["nombre"],
            "apellido": request.form["apellido"],
            "telefono": request.form["telefono"],
            "direccion": request.form["direccion"]
        }
        response = requests.put(f"{backend_url_usuarios}/{id}", json=usuario)
        if response.status_code == 200:
            return redirect(url_for("listar_usuarios"))
        else:
            return "Error al actualizar el usuario: ", response.status_code
    #Para llenar el formulario con la información del usuario
    response = requests.get(f"{backend_url_usuarios}/{id}")
    try:
        usuario = response.json()
        return render_template("editar_usuario.html", usuario=usuario)
    except:
        #En caso de error no se cierre el servidor
        return redirect(url_for("listar_usuarios")), 404
    
#Eliminar usuario
@servidor.route("/eliminar_usuario/<int:id>", methods=["POST"])
def eliminar_usuario(id):
    response = requests.delete(f"{backend_url_usuarios}/{id}")
    print(response)
    return redirect(url_for("listar_usuarios"))


#Ejecutar el server
if __name__ == "__main__":
    servidor.run(debug=True)
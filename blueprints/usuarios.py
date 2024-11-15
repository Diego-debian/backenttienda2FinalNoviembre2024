from flask import Flask, Blueprint, jsonify, request
from db_utils import get_db_connection

usuarios_bp = Blueprint('usuarios', __name__)

#Función para crear un nuevo usuario
@usuarios_bp.route("/usuarios", methods=['POST'])
def create_usuario():
    data = request.get_json()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Usuarios (nombre, apellido, telefono, direccion) VALUES (?,?,?,?)", (data['nombre'], data['apellido'], data.get('telefono'), data.get('direccion')))
        conn.commit()
        return jsonify({"message": "Usuario creado exitosamente"}), 201


#Función para obtener todos los usuarios
@usuarios_bp.route('/usuarios', methods=['GET'])
def get_usuarios():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Usuarios')
        usuarios = cursor.fetchall()
        return jsonify([dict(usuario) for usuario in usuarios]), 200

#Función para obtener un solo usuario
@usuarios_bp.route('/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Usuarios WHERE idUsuario=?', (id,))
        usuario = cursor.fetchone()
        return jsonify(dict(usuario)) if usuario else jsonify({"mensaje":"Usuario no encontrado"}), 404

#Función para editar un usuario
@usuarios_bp.route('/usuarios/<int:id>',methods=['PUT'])
def update_usuario(id):
    data = request.get_json()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE Usuarios SET nombre=?, apellido=?, telefono=?, direccion=? WHERE idUsuario=?', (data['nombre'], data['apellido'], data.get('telefono'), data.get('direccion'), id))
        conn.commit()
        return jsonify({"message": "Usuario actualizado exitosamente"}), 200

#Función para eliminar un usuario
@usuarios_bp.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Usuarios WHERE idUsuario=?', (id,))
        conn.commit()
        return jsonify({"message": "Usuario eliminado exitosamente"}), 200
     
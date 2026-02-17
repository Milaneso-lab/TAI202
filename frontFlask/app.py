from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import json

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Necesaria para flash messages

# URL base de la API FastAPI (ajusta si es necesario)
API_BASE_URL = "http://localhost:5000"

@app.route('/')
def index():
    """Página principal que muestra la tabla de usuarios y formularios"""
    try:
        # Obtener usuarios desde la API FastAPI
        response = requests.get(f"{API_BASE_URL}/v1/usuarios/")
        if response.status_code == 200:
            data = response.json()
            usuarios = data.get('usuarios', [])
            return render_template('index.html', usuarios=usuarios)
        else:
            flash('Error al obtener usuarios de la API', 'error')
            return render_template('index.html', usuarios=[])
    except requests.exceptions.ConnectionError:
        flash('No se pudo conectar a la API. Asegúrate de que esté corriendo en el puerto 5000.', 'error')
        return render_template('index.html', usuarios=[])
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return render_template('index.html', usuarios=[])

@app.route('/agregar', methods=['POST'])
def agregar_usuario():
    """Agregar un nuevo usuario usando POST"""
    try:
        id_usuario = int(request.form.get('id'))
        nombre = request.form.get('nombre')
        edad = int(request.form.get('edad'))
        
        usuario = {
            "id": id_usuario,
            "nombre": nombre,
            "edad": edad
        }
        
        response = requests.post(
            f"{API_BASE_URL}/v1/usuarios/",
            json=usuario,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            flash('Usuario agregado correctamente', 'success')
        else:
            error_data = response.json()
            flash(f'Error: {error_data.get("detail", "Error desconocido")}', 'error')
    except ValueError:
        flash('Error: ID y Edad deben ser números válidos', 'error')
    except requests.exceptions.ConnectionError:
        flash('No se pudo conectar a la API', 'error')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    """Eliminar un usuario usando DELETE"""
    try:
        response = requests.delete(f"{API_BASE_URL}/v1/usuarios/{id}")
        
        if response.status_code == 200:
            flash('Usuario eliminado correctamente', 'success')
        else:
            error_data = response.json()
            flash(f'Error: {error_data.get("detail", "Usuario no encontrado")}', 'error')
    except requests.exceptions.ConnectionError:
        flash('No se pudo conectar a la API', 'error')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5010, host='0.0.0.0')

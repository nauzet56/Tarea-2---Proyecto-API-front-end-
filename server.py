from flask import Flask, request, jsonify
from flask_cors import CORS 
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

app = Flask(__name__)
CORS(app) 

DB_CONFIG = {
    'host': 'localhost',
    'database': 'API',         
    'user': 'nauzetbetancor',    
    'password': '',              
    'port': 5432
}

def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn


@app.route('/formularios', methods=['POST'])
def crear_formulario():
    try:
        datos = request.get_json()
        
        if not datos.get('nombre') or not datos.get('email') or not datos.get('asunto') or not datos.get('mensaje'):
            return jsonify({'error': 'Faltan campos obligatorios'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO formularios (nombre, email, asunto, mensaje)
            VALUES (%s, %s, %s, %s)
            RETURNING id, nombre, email, asunto, mensaje, fecha_creacion;
        """, (datos['nombre'], datos['email'], datos['asunto'], datos['mensaje']))
        
        resultado = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            'mensaje': 'Formulario enviado correctamente',
            'id': resultado[0],
            'nombre': resultado[1],
            'email': resultado[2],
            'asunto': resultado[3],
            'mensaje': resultado[4],
            'fecha_creacion': resultado[5].isoformat()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/formularios', methods=['GET'])
def obtener_formularios():
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("SELECT * FROM formularios ORDER BY fecha_creacion DESC;")
        formularios = cur.fetchall()
        
        cur.close()
        conn.close()
        
        for form in formularios:
            if isinstance(form['fecha_creacion'], datetime):
                form['fecha_creacion'] = form['fecha_creacion'].isoformat()
            if isinstance(form.get('fecha_actualizacion'), datetime):
                form['fecha_actualizacion'] = form['fecha_actualizacion'].isoformat()
        
        return jsonify(formularios), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/formularios/<int:id>', methods=['GET'])
def obtener_formulario(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("SELECT * FROM formularios WHERE id = %s;", (id,))
        formulario = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if not formulario:
            return jsonify({'error': 'Formulario no encontrado'}), 404
        
        if isinstance(formulario['fecha_creacion'], datetime):
            formulario['fecha_creacion'] = formulario['fecha_creacion'].isoformat()
        if isinstance(formulario.get('fecha_actualizacion'), datetime):
            formulario['fecha_actualizacion'] = formulario['fecha_actualizacion'].isoformat()
        
        return jsonify(formulario), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
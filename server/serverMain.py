from flask import Flask, request, jsonify
import json

app = Flask(__name__)

PORT_BASE = 50052  # Puerto base para asignar a los peers
PORT_RANGE = 5      # Rango de puertos a utilizar
PEER_FILE = 'C:\\Users\\dalva\\Desktop\\telematica2\\server\\peer.json'

def load_peer_data():
    with open(PEER_FILE, 'r') as f:
        return json.load(f)

def save_peer_data(data):
    with open(PEER_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def initialize_peers():
    peer_data = load_peer_data()
    for peer in peer_data['peers']:
        peer['connected'] = 0 # Establecer la conexion en 0 al inicio
        peer['port'] = 0  # Establecer todos los puertos en 0 al inicio
        
    save_peer_data(peer_data)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    global username 
    username = data['username']
    password = data['password']
    
    peer_data = load_peer_data()
    initialize_peers()  # Inicializar peers antes de asignar puertos
    
    for peer in peer_data['peers']:
        if peer['username'] == username:
            if peer['connected'] == 1: # Si el usuario ya se encuentra logeado no permitir el acceso
                return jsonify({"message": "User already connected"}), 403
            elif peer['password'] == password:
                # Obtener la IP y puerto asignados
                assigned_ip = '127.0.0.1'
                assigned_port = find_available_port(peer_data)
                
                if assigned_port is None:
                    return jsonify({"message": "No available ports"}), 500
                
                peer['connected'] = 1
                peer['port'] = assigned_port
                
                save_peer_data(peer_data)
                return jsonify({"message": "Login successful", "peer_data": peer, "ip": assigned_ip, "port": assigned_port})
            else:
                return jsonify({"message": "Invalid credentials"}), 401
    
    return jsonify({"message": "User not found"}), 404 #Usuario no encontrado en la base de datos

def find_available_port(peer_data):
    # Buscar el primer puerto disponible en el rango especificado
    for port_offset in range(PORT_RANGE):
        port = PORT_BASE + port_offset
        if not any(peer['port'] == port for peer in peer_data['peers']):
            return port
    return None

@app.route('/logout', methods=['POST'])
def logout():
    global username
        
    peer_data = load_peer_data()
    for peer in peer_data['peers']:
        if peer['username'] == username:
            peer['connected'] = 0 # Establecer la conexion en 0 al cerrar sesión
            peer['port'] = 0  # Establecer el puerto en 0 al cerrar sesión
            save_peer_data(peer_data)
            return jsonify({"message": "Logout successful"})

    return jsonify({"message": "Peer not found"}), 404

@app.route('/index', methods=['GET'])
def index():
    peer_data = load_peer_data()
    connected_users = []
    for peer in peer_data['peers']:
        if peer['connected'] == 1:
            connected_users.append({"nombre": peer['username'], "ip_port": f"127.0.0.1:{peer['port']}"})
    return jsonify({"Usuarios Conectados": connected_users})



@app.route('/search/<username>', methods=['GET'])
def search(username):
    peer_data = load_peer_data()
    for peer in peer_data['peers']:
        if peer['username'] == username:
            if peer['connected'] == 0:
                return jsonify({"message": "Peer not connected"}), 404
            else:
                return jsonify({"peer_files": peer['files']})
    return jsonify({"message": "Peer not found"}), 404

# Inicializar todos los peers como desconectados al iniciar el servidor
initialize_peers()

if __name__ == '__main__':
    app.run(debug=True)

import grpc
import requests
import p2p_pb2
import p2p_pb2_grpc

def login(username, password):
    url = 'http://localhost:5000/login'
    data = {'username': username, 'password': password}
    response = requests.post(url, json=data)
    login_response = response.json()
    if 'message' in login_response and login_response['message'] == 'Login successful':
        peer_data = login_response.get('peer_data', {})
        ip = login_response.get('ip')
        port = login_response.get('port')
        return {'message': 'Login successful', 'peer_data': peer_data, 'ip': ip, 'port': port}
    else:
        return login_response


def logout():
    url = 'http://localhost:5000/logout'
    response = requests.post(url)
    if response.status_code == 200:  # Si la solicitud fue exitosa
        print("Cierre de sesión exitoso.")
    else:
        print("Error al cerrar sesión.")
    return response

def index():
    url = 'http://localhost:5000/index'
    response = requests.get(url)
    return response.json()

def search(username):
    url = f'http://localhost:5000/search/{username}'
    response = requests.get(url)
    return response.json()

def get_file_from_peer(filename, peer_username):
    channel = grpc.insecure_channel('localhost:50051')
    stub = p2p_pb2_grpc.P2PServerStub(channel)
    try:
        response = stub.GetFile(p2p_pb2.GetFileRequest(filename=filename, peer_username=peer_username))
        return response
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.PERMISSION_DENIED:
            return p2p_pb2.GetFileResponse(message=f"El peer '{peer_username}' no está conectado.")
        elif e.code() == grpc.StatusCode.NOT_FOUND:
            return p2p_pb2.GetFileResponse(message=f"El archivo '{filename}' no se encuentra en el peer '{peer_username}'.")
        else:
            raise e

def menu():
    while True:
        print("1. Iniciar sesión")
        print("2. Salir")
        choice = input("Selecciona una opción: ")

        if choice == '1':
            username = input("Introduce tu nombre de usuario: ")
            password = input("Introduce tu contraseña: ")
            login_response = login(username, password)
            if 'message' in login_response:
                if login_response['message'] == 'Login successful':
                    print(f"Inicio de sesión exitoso. Usuario: {login_response['peer_data']['username']}\nIP: {login_response['ip']}\nPuerto: {login_response['port']}")
                    while True:
                        print("1. Obtener lista de usuarios")
                        print("2. Buscar archivos de un usuario")
                        print("3. Descargar archivo de un peer")
                        print("4. Cerrar sesión")
                        print("5. Salir")
                        choice = input("Selecciona una opción: ")

                        if choice == '1':
                            print(index())
                        elif choice == '2':
                            username = input("Introduce el nombre de usuario para buscar archivos: ")
                            print(search(username))
                        elif choice == '3':
                            peer_username = input("Introduce el nombre de usuario del peer del que deseas descargar el archivo: ")
                            filename = input("Introduce el nombre del archivo que deseas descargar: ")
                            response = get_file_from_peer(filename, peer_username)
                            if response.message.startswith('Descarga completa'):
                                print(response.message)
                            else:
                                print("Error:", response.message)
                        elif choice == '4':
                            logout()
                            break
                        elif choice == '5':
                            print("Adiós.")
                            return
                        else:
                            print("Opción no válida. Inténtalo de nuevo.")
                elif login_response['message'] == 'User already connected':
                    print("El usuario ya está conectado.")
                else:
                    print("Credenciales incorrectas. Inténtalo de nuevo.")
        elif choice == '2':
            print("Adiós.")
            return
        else:
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == '__main__':
    menu()
# server.py

from concurrent.futures import ThreadPoolExecutor
import grpc
import p2p_pb2
import p2p_pb2_grpc
import json

class P2PServer(p2p_pb2_grpc.P2PServerServicer):
    def load_peer_data(self):
        with open('C:\\Users\\dalva\\Desktop\\telematica2\\server\\peer.json', 'r') as f:
            return json.load(f)

    def GetFile(self, request, context):
        filename = request.filename
        peer_username = request.peer_username
        peer_data = self.load_peer_data()  # Load the peer data from the file

        # Verificar si el peer está conectado
        peer_found = False  # Bandera para indicar si se encontró el peer
        for peer in peer_data['peers']:
            if peer['username'] == peer_username:
                peer_found = True  # Se encontró el peer en la lista
                if peer['connected'] == 1:  # Peer is connected
                    if filename in peer['files']:
                        return p2p_pb2.GetFileResponse(message=f"Descarga completa: {filename}")
                    else:
                        context.set_code(grpc.StatusCode.NOT_FOUND)
                        context.set_details(f"El archivo '{filename}' no se encuentra en el peer.")
                        return p2p_pb2.GetFileResponse(message=f"No se encontró el archivo '{filename}'.")
                else:  # Peer is not connected
                    context.set_code(grpc.StatusCode.PERMISSION_DENIED)
                    context.set_details(f"El peer '{peer_username}' no está conectado.")
                    return p2p_pb2.GetFileResponse(message=f"El peer '{peer_username}' no está conectado.")
        
        # Si el peer no se encuentra en la lista
        if not peer_found:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"El peer '{peer_username}' no se encuentra en la lista.")
            return p2p_pb2.GetFileResponse(message=f"El peer '{peer_username}' no se encuentra en la lista.")

def serve():
    server = grpc.server(ThreadPoolExecutor())
    p2p_pb2_grpc.add_P2PServerServicer_to_server(P2PServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor P2P iniciado. Escuchando en el puerto 50051.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

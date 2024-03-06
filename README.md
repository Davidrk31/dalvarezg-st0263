# dalvarezg-st0263
# Info de la materia: ST0263 Topicos especiales en Telematica.

## Estudiante(s):
- **David Alvarez Grisales** 
- **dalvarezg@eafit.edu.co** 

## Profesor:
- **Nombre:** Alvaro Enrique Ospina Sanjuan
- **Correo Electrónico:** aeospinas@eafit.edu.co

## Reto 1 y 2.

## 1. Breve descripción de la actividad.

1.1  Se ha desarrollado un sistema P2P donde cada nodo o peer contiene varios microservicios que soportan un sistema de compartición de archivos distribuido y descentralizado, Se ha utilizado el middleware gRPC para la comunicación entre los diferentes nodos o peers, para esto se creo un servidor el cual seria el principal donde cada cliente peer se conecta a este, alli se realizan los metodos API REST como el login, logout, index y search, el servidor prinicipal cuenta con una base de datos simulada la cual va en un .json, en esta se encuentra la informacion de cada peer, su usuario, su contraseña y los archivos que este contiene, luego se simulo la descarga de los archivos con la conexion gRPC entre los peers, esto mediante el server peer.

1.2 No se desplego el proyecto en otra cosa que no fuera el sistema local y hace faltar cambiar las partes simuladas por archivos reales para posteriores versiones del proyecto.

# 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

- Se uso gRPC para el sistema P2P implementando un cliente y un server peer.

- La arquitectura del sistema se basa en un sistema P2P no estructurado donde no hay un control centralizado por parte de un solo peer. Cada nodo es igual y puede actuar como cliente y servidor. La comunicación entre los nodos se realiza a través de middleware gRPC, que proporciona una comunicación eficiente y escalable. Además, se utiliza un enfoque de microservicios para modularizar las diferentes funcionalidades del sistema.

- Se utiliza API REST para la comunicación entre el cliente y el servidor HTTP y gRPC para la comunicación entre los nodos en la red P2P. Esto permite una comunicación eficiente y flexible entre los componentes del sistema, implementando los dos middleware.

![image](https://github.com/Davidrk31/dalvarezg-st0263/assets/89051979/a51934d0-4db6-46af-b5ce-cf1182a795e7)



# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

- IDE: Visual Studio Code
- Lenguaje de Programación: Python v3.11.5
- Middleware:
  * Api Rest
  * gRPC
- Librerías: 
  * grpcio v1.62.0 
  * grpcio-tools v1.62.0
  * Flask v3.0.0
  * requests v2.31.0

Para ejecutar y compilar en el entorno de desarrollo:

Instalamos las librerias correspondientes mencionadas anteriormente 

 Luego generar el archivo .proto:
    'python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. peerServidor.proto'

Corremos el servidor central de la forma: 

    'python serverMain.py'

Luego correr los archivos de los peers:

    'python server.py'
    'python client.py'



Los puertos de los peers, se configuran segun su orden de llegada, cuando un peer se conecta se le asigna un puerto, luego al desconectarse este puerto queda libre otra vez


En los metodos, cuando se realiza la simulacion de la descarga de un archivo el sistema comprueba si el peer esta conectado y luego si el archivo existe, si este existe dira descarga exitosa y se devolvera el nombre del archivo y si no dependiendo del caso, indicara que el peer no existe/no esta conectado o que el archivo no se encuentra en ese peer.

La ip usada fue la local de la maquina: "127.0.0.1"


Archivos:


![image](https://github.com/Davidrk31/dalvarezg-st0263/assets/89051979/8e535cf3-db5c-430b-b16c-a03543c88eb0)


# 4 Ambiente de ejecucion:
Para este reto 1 y 2 todo se hizo de manera local 


# Referencias:

* https://youtu.be/WB37L7PjI5k 

* https://putukusuma.medium.com/creating-simple-cryptocurrency-part-5-peer-to-peer-p2p-with-grpc-f96913ddd7dd

* https://blog.hubspot.com/website/what-is-rest-api#:~:text=A%20REST%20API%20(also%20called,resource%20in%20a%20standardized%20representation.

* https://github.com/cpurta/p2p-grpc

* https://grpc.io/docs/languages/python/basics/



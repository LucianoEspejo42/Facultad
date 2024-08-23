import socket
import threading

"""
El cliente envia un mensaje al servidor, y este devuelve el mensaje cifrado

Paso:
    Servidor:
        1) Escucha las conexiones de los cliente
        2) Recibe mensaje del cliente
        3) El mensaje se cifra (usando alguna especie de algoritmo)
        4) Devuelve el mensaje cifrado
    Cliente:
        1) Se conecta al servidor
        2) Envia un mensaje al servidor
        3) Recibe y se muestra el mensaje cifrado

    [Cliente] ----Envia el mensaje al servidor---> [Servidor]
    [Servidor] ----Le envia el mensaje cifrado---> [Cliente]
"""
host = "0.0.0.0"
port = 5555
max_connect = 2

#creamos nuestro socket
servidor = new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Pasamos los datos de conexion a nuestro servidor
servidor.bind((host,port))
servidor.listen(max_connect)

print(f"Server running on {host}:{port}")

"""
Función para cifrar un mensaje, lo que realiza es desplazar cada caracter en 3 (o lo q venga en el 
parametro 'desplazamiento', por defecto 3), por ejemplo: para el caracter 'a' se cifra al caracter 'd', el 
caracter 'b' se cifra a 'e' y asi sucesivamente.
Por lo tanto el mensaje 'Kawavonwa' se cifra como 'Ndzdyrqzd'"""

def cifrado_de_mensaje(mensaje, desplazamiento):
    resultado = ""
    for char in mensaje:
        if char.isalpha():  # Solo cifrar letras
            ascii_offset = 65 if char.isupper() else 97
            resultado += chr((ord(char) - ascii_offset + desplazamiento) % 26 + ascii_offset)
        else:
            resultado += char  # No modificar caracteres no alfabéticos
    return resultado

def manejo_cliente (cli, addr):
    try:
        print(f"Connection established with {addr}")
        desp = 3
        while True:
            #Recibir el mensaje a cifrar
            recv = cli.recv(1024).decode()

            if not recv:
                break

            texto_cifrado = cifrado_de_mensaje(recv,desp)

            #Devolver el mensaje al cliente
            cli.send(texto_cifrado.encode())
    except ConnectionResetError:
        print("Cliente desconectado")
        cli.close()


def receive_connection ():
    while True:
        client, address = servidor.accept()

        #Crear un hilo para manejar al cliente
        thread_client = threading.Thread(target=manejo_cliente,args=(client,address))
        thread_client.start()

receive_connection()

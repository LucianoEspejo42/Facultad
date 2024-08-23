import socket
import threading


servidor = "127.0.0.1"
puerto = 5555
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Conecto al cliente con el servidor
cliente.connect((servidor,puerto))

print(f"Connect to server {servidor}:{puerto}")

def receive_message ():
    while True:
        try:
            input_text = input("Ingrese mensaje a cifrar (o salir para terminar): ")

            if input_text.lower() == 'salir':
                break
            #Envia el mensaje al servidor
            cliente.send(input_text.encode())

            #Recibe el mensaje del servidor
            mensaje = cliente.recv(1024).decode()

            #Mostrar el mensaje cifrado
            print(f"El texto cifrado es {mensaje}")

        except:
            print("Ha ocurrido un error..")
            cliente.close()

receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

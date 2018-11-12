from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def aceptar_conexion():

    while True:
        cliente, dir_cliente = SERVER.accept()
        print("%s:%s se ha conectado." % dir_cliente)
        cliente.send(bytes("Saludos y bienvenido al chat. Ingresa tu nombre y presiona Enter!", "utf8"))
        direcciones[cliente] = dir_cliente
        Thread(target=conf_cliente, args=(cliente,)).start()


def conf_cliente(cliente):
    nombre = cliente.recv(BUFSIZ).decode("utf8")
    saludos='Saludos %s! Si deseas salir, escribe {salir} para hacerlo' % nombre
    cliente.send(bytes(saludos, "utf8"))
    mensaje = "%s se ha unido al chat!" % nombre
    broadcast(bytes(mensaje, "utf8"))
    clientes[cliente] = nombre

    while True:
        mensaje = cliente.recv(BUFSIZ)
        if mensaje != bytes("{salir}", "utf8"):
            broadcast(mensaje, nombre+": ")
        else:
            cliente.send(bytes("{quit}", "utf8"))
            cliente.close()
            del clientes[cliente]
            broadcast(bytes("%s ha dejado el chat." % nombre, "utf8"))
            break

def broadcast(mensaje, prefijo=""):
    for sock in clientes:
        sock.send(bytes(prefijo, "utf8"))

clientes = {}
direcciones = {}

HOST = '0.0.0.0'
PORT = 42424
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(1)
    print("Esperando conexion...")
    ACCEPT_THREAD = Thread(target=aceptar_conexion())
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()









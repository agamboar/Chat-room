from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread   #permite multioperaciones en el codigo, mediante la creacion de hilos
import tkinter #permite la creacion de la interfaz para el chat


HOST = input('Ingrese el host...')
PORT = input('Ingrese el puerto...')
if not PORT:
    PORT = 42424   #numero random
else:
    PORT = int(PORT)
BUFSIZ = 1024
ADDR = (HOST, PORT)

cliente_socket = socket(AF_INET, SOCK_STREAM)
cliente_socket.connect(ADDR)

def recibir():
    while True:
        try:
            mensaje = cliente_socket.recv(BUFSIZ).decode("utf8")
            lista_mensajes.insert(tkinter.END, mensaje)

        except OSError:             #probablemente, el cliente dejo el chat
            break

def enviar(event=None):
    mensaje = mi_mensaje.get()
    mi_mensaje.set("")
    cliente_socket.send(bytes(mensaje, "utf8"))
    if mensaje == "{quit}":
        cliente_socket.close()
        top.quit()

def cerrando(event=None):
    mi_mensaje.set("{quit}")
    enviar()

top = tkinter.Tk()
top.title("Chat")

cuadro_conversacion = tkinter.Frame(top)
mi_mensaje = tkinter.StringVar()
mi_mensaje.set("Escribe aqui tu mensaje...")
barra_des = tkinter.Scrollbar(cuadro_conversacion)
lista_mensajes = tkinter.Listbox(cuadro_conversacion, height=15, width=50, yscrollcommand=barra_des.set)
barra_des.pack(side=tkinter.RIGHT, fill=tkinter.Y)
lista_mensajes.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
lista_mensajes.pack()
cuadro_conversacion.pack()

campo_entrada = tkinter.Entry(top, textvariable=mi_mensaje)
campo_entrada.bind("<Return>", enviar())
campo_entrada.pack()
boton_envio = tkinter.Button(top, text="Enviar", command=enviar())
boton_envio.pack()

top.protocol("WM_DELETE_WINDOW", cerrando())


hilo_recibido = Thread(target=recibir())
hilo_recibido.start()
tkinter.mainloop()


















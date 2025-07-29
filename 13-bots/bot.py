import socket 

if __name__ == "__main__":
    print("[+] Conectando con el servidor")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("192.168.100.62", 8085))
    run_bot = True
    while run_bot:
        communicate_bot = True
        while  communicate_bot:
            msg = s.recv(1024)
            msg = msg.decode()
            print("El centro de comandos dijo: ", msg)
            if msg == "exit":
                communicate_bot = False
        ans = "conectado"
        if ans == "no":
            status = "desconectado"
            s.send(status.encode())
            run_bot = False
        else:
            status = "conectado".encode()
            s.send(status)
    s.close()

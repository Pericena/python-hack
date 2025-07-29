import subprocess

if __name__ == "__main__":
    interfaz = "eth0"
    nueva_mac = "22:11:22:33:44:57"

    print("Apagando la interfaz")
    subprocess.run(["ifconfig", "eth0", "down"])

    print("Cambiando la dirección HW de la interfaz", interfaz, "a", nueva_mac)
    subprocess.run(["ifconfig", interfaz, "hw", "ether", nueva_mac])
    
    print("Dirección MAC cambiada a", nueva_mac)
    subprocess.run(["ifconfig", interfaz, "up"])
    
    print("Interfaz de red encendida")

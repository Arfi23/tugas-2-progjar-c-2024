import socket

def main():
    host = '172.16.16.101' # IP mesin1 jupyter notebook  
    port = 45000        

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        while True:
            command = input("Tuliskan perintah request (TIME/QUIT): ").strip().upper()
            
            if command == "TIME":
                s.sendall("TIME\r\n".encode('utf-8'))
                data = s.recv(1024).decode('utf-8')
                print(f"Respon dari server: {data}")

            elif command == "QUIT":
                s.sendall("QUIT\r\n".encode('utf-8'))
                data = s.recv(1024).decode('utf-8')
                print(f"Respon dari server: {data}")
                break

            else:
                print("Perintah tidak dikenali. Server hanya menerima perintah TIME atau QUIT.")

if __name__ == "__main__":
    main()

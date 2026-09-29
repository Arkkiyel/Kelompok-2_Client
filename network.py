import socket
import json

def connect_to_server(ip, port):
    """
    Membuka koneksi TCP ke server
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(10.0) 
    
    try:
        client_socket.connect((ip, port))
        print(f"[+] Connected to server {ip}:{port}")
    
        client_socket.settimeout(None) 
        return client_socket
        
    except ConnectionRefusedError:
        print("[-] Failed to connect: Server declined the request. Make sure the server is already running")
        return None
    except socket.timeout:
        print("[-] Failed to connect: Server Timeout.")
        return None
    except Exception as e:
        print(f"[-] Network Error: {e}")
        return None

def send_and_request(client_socket, pesan_dict):
    """
    Mengirim data dari dictionary Python, diubah ke JSON, dikirim ke server.
    Lalu menerima balasan dari server, diparse dari JSON kembali menjadi dictionary.
    """
    try:
        pesan_json = json.dumps(pesan_dict)
        client_socket.sendall(pesan_json.encode('utf-8'))
        respons_byte = client_socket.recv(4096)
        if not respons_byte:
            print("[-] Connection is closed by server.")
            return None
        respons_string = respons_byte.decode('utf-8')
        respons_dict = json.loads(respons_string)
        
        return respons_dict
        
    except ConnectionResetError:
        print("[-] Error: Connection is suddenly closed by server.")
        return None
    except json.JSONDecodeError:
        print("[-] Error: Response isn't JSON.")
        return None
    except Exception as e:
        print(f"[-] Error: {e}")
        return None

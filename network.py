import socket
import json

def connect_to_server(ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(10.0) 
    
    try:
        client_socket.connect((ip, port))
        print(f"[+] Successfully connected to server {ip}:{port}")
        client_socket.settimeout(None) 
        return client_socket
        
    except ConnectionRefusedError:
        print("[-] Connection failed: Connection refused (Server might not be running).")
        return None
    except socket.timeout:
        print("[-] Connection failed: Connection timed out.")
        return None
    except Exception as e:
        print(f"[-] A network error occurred: {e}")
        return None

def send_and_receive(client_socket, message_dict):
    try:
        message_json = json.dumps(message_dict)
        client_socket.sendall(message_json.encode('utf-8'))
        
        response_bytes = client_socket.recv(4096)
        
        if not response_bytes:
            print("[-] Connection closed by the server.")
            return None
            
        return json.loads(response_bytes.decode('utf-8'))
        
    except ConnectionResetError:
        print("[-] Error: Connection was forcibly closed by the server.")
        return None
    except json.JSONDecodeError:
        print("[-] Error: Received invalid JSON format from the server.")
        return None
    except Exception as e:
        print(f"[-] A communication error occurred: {e}")
        return None

def close_connection(client_socket):
    try:
        if client_socket:
            client_socket.close()
            print("[!] Connection closed safely.")
    except Exception as e:
        print(f"[-] Error while closing the connection: {e}")

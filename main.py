import argparse
import json
import uuid

from network import close_connection, connect_to_server
from validator import inputValidation, verify_result


SERVICES = {
    "1": ("CHAR_COUNT", "Hitung karakter"),
    "2": ("WORD_COUNT", "Hitung kata"),
    "3": ("REVERSE_STRING", "Balik teks"),
    "4": ("REMOVE_VOWELS", "Hapus huruf vokal"),
    "5": ("MATRIX_3X3", "Determinan dan invers matriks 3x3"),
}


def read_input(service):
    if service != "MATRIX_3X3":
        return inputValidation.ivString(input("Masukkan teks: "))

    matrix = []
    print("Masukkan tiga baris matriks, masing-masing berisi tiga angka dipisah spasi.")
    for index in range(3):
        values = input(f"Baris {index + 1}: ").split()
        if len(values) != 3:
            raise ValueError("Setiap baris harus berisi tepat tiga angka.")
        try:
            matrix.append([float(value) for value in values])
        except ValueError as error:
            raise ValueError("Elemen matriks harus berupa angka.") from error
    return inputValidation.ivMatrix(matrix)


def exchange(client_socket, reader, message, expected_type):
    client_socket.sendall((json.dumps(message, ensure_ascii=False) + "\n").encode("utf-8"))
    line = reader.readline()
    if not line:
        raise ConnectionError("Server menutup koneksi.")
    try:
        response = json.loads(line)
    except json.JSONDecodeError as error:
        raise ValueError("Respons server bukan JSON yang valid.") from error
    if not isinstance(response, dict):
        raise ValueError("Respons server harus berupa objek JSON.")
    if response.get("type") == "ERROR":
        raise ValueError(response.get("message", "Server menolak pesan."))
    if response.get("type") != expected_type:
        raise ValueError(f"Tipe respons tidak sesuai: {response.get('type')!r}.")
    if response.get("request_id") != message["request_id"] or response.get("service") != message["service"]:
        raise ValueError("ID permintaan atau layanan pada respons tidak sesuai.")
    return response


def run_client(client_socket):
    active_services = {service for service, _ in SERVICES.values()}
    client_socket.settimeout(10)
    with client_socket.makefile("r", encoding="utf-8") as reader:
        while active_services:
            print("\nLayanan tersedia:")
            for choice, (service, label) in SERVICES.items():
                if service in active_services:
                    print(f"  {choice}. {label} ({service})")
            print("  q. Keluar")
            choice = input("Pilih layanan: ").strip().lower()
            if choice == "q":
                return
            if choice not in SERVICES:
                print("Pilihan tidak tersedia.")
                continue

            service = SERVICES[choice][0]
            if service not in active_services:
                print("Layanan ini sudah dinonaktifkan.")
                continue
            try:
                data = read_input(service)
            except ValueError as error:
                print(f"Input tidak valid: {error}")
                continue

            request_id = uuid.uuid4().hex
            payload = {"matrix": data} if service == "MATRIX_3X3" else {"text": data}
            response = exchange(
                client_socket,
                reader,
                {"type": "REQUEST", "request_id": request_id, "service": service, "payload": payload},
                "RESPONSE",
            )
            status = response.get("status")
            if status == "DISABLED":
                active_services.discard(service)
                print(response.get("message", "Layanan sudah dinonaktifkan."))
                continue
            if status != "SUCCESS":
                print(response.get("message", f"Permintaan gagal dengan status {status}."))
                continue

            result = response.get("result")
            correct = verify_result(service, data, result)
            ack_status = "CORRECT" if correct else "INCORRECT"
            print(f"Hasil server: {json.dumps(result, ensure_ascii=False)}")
            print(f"Verifikasi lokal: {ack_status}")

            confirmation = exchange(
                client_socket,
                reader,
                {"type": "ACK", "request_id": request_id, "service": service, "status": ack_status},
                "ACK_CONFIRM",
            )
            active_list = confirmation.get("active_services")
            if not isinstance(active_list, list):
                raise ValueError("Daftar layanan aktif dalam ACK_CONFIRM tidak valid.")
            active_services = set(active_list)
            print(f"Tindakan server: {confirmation.get('action', 'tidak diketahui')}")
            if confirmation.get("server_status") == "TERMINATING":
                print("Semua layanan nonaktif. Server sedang berhenti.")
                return

    print("Semua layanan sudah nonaktif.")


def main():
    parser = argparse.ArgumentParser(description="Klien TCP untuk server Jarkom Kelompok 7")
    parser.add_argument("--host", default="127.0.0.1", help="Alamat server (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=65432, help="Port server (default: 65432)")
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("Port harus berada di antara 1 dan 65535.")

    client_socket = connect_to_server(args.host, args.port)
    if client_socket is None:
        return
    try:
        run_client(client_socket)
    except (ConnectionError, OSError, TimeoutError, ValueError) as error:
        print(f"Komunikasi terhenti: {error}")
    except (EOFError, KeyboardInterrupt):
        print("\nKlien dihentikan.")
    finally:
        close_connection(client_socket)


if __name__ == "__main__":
    main()

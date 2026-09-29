# Klien Jaringan Komputer Kelompok 2

Klien terminal untuk [server TCP Kelompok 7](https://github.com/kentarotaro/kelompok-07-jarkom-server). Klien mengirim permintaan layanan, memeriksa hasil dengan perhitungan lokal, lalu mengirim ACK `CORRECT` atau `INCORRECT`. Server dapat menyisipkan hasil yang salah sesuai `--fault-rate`; ACK `INCORRECT` membuat server menonaktifkan layanan tersebut.

## Persiapan

- Python 3.8 atau lebih baru
- `numpy` untuk verifikasi determinan dan invers matriks
- Server Kelompok 7 yang dapat dijangkau melalui TCP

Pasang dependensi klien:

```sh
python -m pip install numpy
```

Jalankan server dari direktori repo server:

```sh
python main.py --host 0.0.0.0 --port 65432
```

Di direktori repo klien, jalankan:

```sh
python main.py
```

Untuk server di komputer lain:

```sh
python main.py --host ALAMAT_SERVER --port 65432
```

Alamat bawaan klien adalah `127.0.0.1:65432`. Pastikan port server dapat diakses dari komputer klien.

## Menggunakan klien

Pilih angka layanan pada menu, lalu masukkan teks atau tiga baris matriks. Setiap baris matriks berisi tiga angka yang dipisahkan spasi. Ketik `q` pada menu untuk keluar.

| Pilihan | Layanan | Input | Hasil |
| --- | --- | --- | --- |
| 1 | `CHAR_COUNT` | Teks | Jumlah karakter, termasuk spasi |
| 2 | `WORD_COUNT` | Teks | Jumlah kata |
| 3 | `REVERSE_STRING` | Teks | Teks dengan urutan karakter terbalik |
| 4 | `REMOVE_VOWELS` | Teks | Teks tanpa huruf vokal `a`, `i`, `u`, `e`, `o` |
| 5 | `MATRIX_3X3` | Tiga baris, masing-masing tiga angka | Determinan dan invers; invers bernilai `null` jika matriks singular |

Contoh masukan matriks:

```text
Baris 1: 1 2 3
Baris 2: 0 1 4
Baris 3: 5 6 0
```

Setelah respons berstatus `SUCCESS`, klien menampilkan hasil server dan keputusan verifikasi lokal. Klien lalu mengirim ACK untuk permintaan yang sama dan memperbarui menu dari daftar layanan aktif pada `ACK_CONFIRM`. Respons `DISABLED` ditampilkan tanpa mengirim ACK. Ketika semua layanan dinonaktifkan, server mengirim status `TERMINATING` dan klien berhenti.

## Protokol

Setiap pesan adalah objek JSON UTF-8 yang diakhiri newline (`\n`). Satu koneksi TCP dapat memuat beberapa pasangan permintaan dan ACK. Contoh pertukaran untuk layanan karakter:

```json
{"type":"REQUEST","request_id":"req-101","service":"CHAR_COUNT","payload":{"text":"Halo"}}
{"type":"RESPONSE","request_id":"req-101","service":"CHAR_COUNT","status":"SUCCESS","result":4}
{"type":"ACK","request_id":"req-101","service":"CHAR_COUNT","status":"CORRECT"}
{"type":"ACK_CONFIRM","request_id":"req-101","service":"CHAR_COUNT","action":"MAINTAINED","active_services":["CHAR_COUNT","WORD_COUNT","REVERSE_STRING","REMOVE_VOWELS","MATRIX_3X3"],"server_status":"RUNNING"}
```

Urutan di atas bergantian antara pesan klien dan server. `request_id` dibuat unik untuk setiap permintaan. Jika server mengembalikan `ERROR`, `NOT_FOUND`, atau `DISABLED`, klien menampilkan pesan kegagalan. Rincian status dan format layanan ada di [README server](https://github.com/kentarotaro/kelompok-07-jarkom-server#spesifikasi-protokol-komunikasi).

## Berkas

- `main.py`: menu terminal, pembingkaian pesan JSON per baris, alur REQUEST dan ACK.
- `network.py`: pembukaan dan penutupan koneksi TCP.
- `validator.py`: validasi input dan verifikasi hasil layanan.
- `test_validator.py`: pengujian fungsi validasi yang sudah ada di repo.

Server memproses satu koneksi klien pada satu waktu. Jika respons tidak datang, klien menghentikan pembacaan setelah 10 detik dan menutup koneksi.

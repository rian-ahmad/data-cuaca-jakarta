# data-cuaca-jakarta
🚀📊💡 Data pipeline Python untuk mengambil dan memproses data prakiraan cuaca Jakarta dari Public API BMKG (Badan Meteorologi, Klimatologi, dan Geofisika).

## Fitur Utama
- **Integrasi API**: Mengambil data prakiraan cuaca dari API publik BMKG.
- **Ketahanan (Resilience)**: Menggunakan mekanisme _retry_ otomatis untuk menangani kegagalan jaringan atau batasan laju panggilan (rate-limiting) dari API.
- **Modularitas**: Konfigurasi dipisahkan ke dalam file `config.py` untuk kemudahan pemeliharaan dan penyesuaian.
- **Pencatatan (Logging)**: Merekam setiap langkah alur kerja ke dalam konsol dan file log, memudahkan pemantauan dan `debugging`.
- **Pembersihan Data**: Memproses dan menormalisasi data mentah dari JSON ke dalam format tabel yang bersih menggunakan `pandas`.
- **RAG Ready**: Data yang dihasilkan disimpan dalam format yang ideal untuk aplikasi **Retrieval-Augmented Generation (RAG)**, siap untuk diintegrasikan dengan model bahasa besar (LLM).

## Struktur Proyek
├── requirement.txt              # Daftar library yang diperulukan
├── processing_cuaca_jakarta.py  # Skrip utama untuk menjalankan pipeline
├── config.py                    # File konfigurasi
├── pipeline.log                 # Log hasil eksekusi (dihasilkan setelah dijalankan)
└── README.md                    # File yang sedang Anda baca

## Persyaratan (Requirements)
Pastikan Anda telah menginstal Python (disarankan versi 3.8 atau lebih tinggi).
Instal semua pustaka yang diperlukan dengan menjalankan perintah berikut:
```bash
pip install -r requirements.txt
```
## Cara Menjalankan
Jalankan skrip Python dari terminal:
```bash
python processing_cuaca_jakarta.py
```
Setelah skrip selesai, data prakiraan cuaca akan disimpan dalam file data_cuaca_jkt.json di direktori yang sama.

## Sumber Data
### **Data Cuaca**: BMKG (Badan Meteorologi, Klimatologi, dan Geofisika)
**URL**: https://data.bmkg.go.id/prakiraan-cuaca/
### Kode Wilayah: Permendagri (Kementerian Dalam Negeri Republik Indonesia)
URL: https://kodewilayah.id/

## Lisensi
Proyek ini dilisensikan di bawah MIT License 
- lihat file LICENSE untuk detail selengkapnya.

# data-cuaca-jakarta
🚀📊💡 Proyek ini adalah data pipeline otomatis yang dirancang untuk mengambil, membersihkan, dan menyimpan data prakiraan cuaca dari BMKG (Badan Meteorologi, Klimatologi, dan Geofisika). Menggunakan pandas untuk pemrosesan data, requests dengan mekanisme retry untuk ketahanan terhadap kegagalan jaringan, dan logging untuk pemantauan alur kerja. Data disimpan dalam format JSON untuk kemudahan konsumsi oleh aplikasi hilir (downstream applications).  



## ⭐Fitur Utama
- 🔌**Integrasi API**: Mengambil data prakiraan cuaca dari API publik BMKG.
- 🛡️**Ketahanan (Resilience)**: Menggunakan mekanisme _retry_ otomatis untuk menangani kegagalan jaringan atau batasan laju panggilan (rate-limiting) dari API.
- 🧩**Modularitas**: Konfigurasi dipisahkan ke dalam file `config.py` untuk kemudahan pemeliharaan dan penyesuaian.
- 📝**Pencatatan (Logging)**: Merekam setiap langkah alur kerja ke dalam konsol dan file log, memudahkan pemantauan dan `debugging`.
- ✨**Pembersihan Data**: Memproses dan menormalisasi data mentah dari JSON ke dalam format tabel yang bersih menggunakan `pandas`.
- 🤖**RAG Ready**: Data yang dihasilkan disimpan dalam format yang ideal untuk aplikasi **Retrieval-Augmented Generation (RAG)**, siap untuk diintegrasikan dengan model bahasa besar (LLM).  



## 📂Struktur Proyek
```
├── requirement.txt              # Daftar library yang diperlukan
├── processing_cuaca_jakarta.py  # Skrip utama untuk menjalankan pipeline
├── config.py                    # File konfigurasi
├── pipeline.log                 # Log hasil eksekusi (dihasilkan setelah dijalankan)
└── README.md                    # File yang sedang Anda baca
```  



## 🛠️Persyaratan (Requirements)
Pastikan Anda telah menginstal Python (disarankan versi 3.12 atau lebih tinggi).
Instal semua pustaka yang diperlukan dengan menjalankan perintah berikut:
```bash
pip install -r requirements.txt
```  



## 🚀Cara Menjalankan
Jalankan skrip Python dari terminal:
```bash
python processing_cuaca_jakarta.py
```
💾 Setelah skrip selesai, data prakiraan cuaca akan disimpan dalam file data_cuaca_jkt.json di direktori yang sama.  


  
## 📜Contoh Output JSON
```json
[
  {
    "id": "31.01.01.1001_2025-09-05_17:00:00",
    "text": "Cuaca di desa Pulau Panggang (kode 31.01.01.1001) pada 2025-09-05 17:00:00 adalah Cerah dengan suhu 28°C, kelembapan 74%, dan kecepatan angin 7.0 km/jam.",
    "metadata": {
      "Provinsi": "DKI Jakarta",
      "Kota/Kabupaten": "Administrasi Kepulauan Seribu",
      "Kecamatan": "Kepulauan Seribu Utara",
      "Desa": "Pulau Panggang",
      "Kode adm4": "31.01.01.1001",
      "Waktu Lokal": "2025-09-05 17:00:00",
      "Suhu Udara (c)": 28,
      "Kelembapan": 74,
      "Kondisi Cuaca": "Cerah",
      "Kecepatan Angin (Km/Jam)": 7.0,
      "Jarak Pandang (m)": 7094
    }
  }
]
```


  
## ℹ️Sumber Data
### ☁️**Data Cuaca**: BMKG (Badan Meteorologi, Klimatologi, dan Geofisika)
**URL**: https://data.bmkg.go.id/prakiraan-cuaca/
### 🗺️Kode Wilayah: Permendagri (Kementerian Dalam Negeri Republik Indonesia)
URL: https://kodewilayah.id/  



## ⚖️Lisensi
Proyek ini dilisensikan di bawah MIT License 
- lihat file LICENSE untuk detail selengkapnya.

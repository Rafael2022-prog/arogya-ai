# Quick Start - AI Kesehatan Maluku Tenggara

## Langkah Cepat dengan Data Profil Kesehatan 2013 & 2024

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Import Data Profil Kesehatan
```bash
python data/import_profil_kesehatan.py
```

Tool ini akan memandu Anda:
- Input path file Excel profil kesehatan 2013
- Input path file Excel profil kesehatan 2024
- Pilih sheet yang berisi data penyakit
- Mapping kolom secara interaktif
- Otomatis gabungkan data dari kedua tahun

**Contoh path file:**
```
data/profil_kesehatan_2013.xlsx
data/profil_kesehatan_2024.xlsx
```

### 3. Training Model
Setelah data berhasil diimport:
```bash
python models/train.py
```

Model akan:
- Membaca data dari `data/health_data.csv`
- Training dengan Random Forest
- Menyimpan model ke `models/saved/`
- Menampilkan akurasi model

### 4. Jalankan API Server
```bash
python api/app.py
```

API akan berjalan di: http://localhost:5000

### 5. Buka Dashboard
Buka terminal baru:
```bash
cd dashboard
python -m http.server 8080
```

Akses dashboard di browser: http://localhost:8080

---

## Tips Import Data

### Jika Data Penyakit di Satu Kolom
```
Kecamatan | Penyakit | Jumlah Kasus
Kei Kecil | DBD      | 15
Kei Kecil | ISPA     | 45
```
Pilih opsi 1 saat mapping

### Jika Data Penyakit di Beberapa Kolom
```
Kecamatan | DBD | ISPA | Malaria
Kei Kecil | 15  | 45   | 8
```
Pilih opsi 2 saat mapping, lalu input:
```
2:DBD,3:ISPA,4:Malaria
```

---

## Struktur Data yang Dihasilkan

File `data/health_data.csv` akan berisi:
```csv
bulan,tahun,kecamatan,penyakit,jumlah_kasus,jumlah_penduduk,fasilitas_kesehatan
12,2013,Kei Kecil,DBD,15,12000,2
12,2013,Kei Kecil,ISPA,45,12000,2
12,2024,Kei Besar,DBD,22,15000,3
```

---

## Troubleshooting

**Q: File Excel tidak terbaca**
```bash
pip install --upgrade openpyxl
```

**Q: Error saat training model**
Pastikan file `data/health_data.csv` ada dan berisi minimal 10 baris data

**Q: Ingin update data demografis**
Edit fungsi `add_demographic_data()` di `data/import_profil_kesehatan.py`

**Q: Ingin menambah data tahun lain**
Jalankan lagi `python data/import_profil_kesehatan.py` dan pilih 'y' untuk gabung dengan data existing

---

## Contoh Penggunaan API

### Prediksi Kasus
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "bulan": 3,
    "kecamatan": "Kei Kecil",
    "penyakit": "DBD",
    "jumlah_penduduk": 12000,
    "fasilitas_kesehatan": 2
  }'
```

Response:
```json
{
  "prediksi_kasus": 18,
  "rekomendasi": [
    "Lakukan monitoring rutin",
    "Edukasi masyarakat tentang gejala awal"
  ]
}
```

---

## Next Steps

1. ✅ Import data profil kesehatan
2. ✅ Training model
3. ✅ Test prediksi via dashboard
4. 🔄 Evaluasi akurasi model
5. 🔄 Tambah fitur visualisasi
6. 🔄 Deploy ke server production

---

## Kontak

Untuk bantuan implementasi di Dinas Kesehatan Kabupaten Maluku Tenggara,
silakan hubungi tim IT atau developer yang bertanggung jawab.

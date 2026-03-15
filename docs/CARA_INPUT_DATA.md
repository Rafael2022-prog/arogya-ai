# Cara Input Data dari PDF

## Metode 1: Ekstraksi Otomatis dari PDF

### Langkah 1: Install dependencies
```bash
pip install PyPDF2 pandas openpyxl tabula-py
```

### Langkah 2: Ekstrak teks dari PDF
```bash
python data/pdf_extractor.py data/laporan_kesehatan.pdf
```

Ini akan menghasilkan file `data/extracted_text.txt` yang berisi teks dari PDF.

### Langkah 3: Review hasil ekstraksi
Buka file `data/extracted_text.txt` dan lihat strukturnya.

---

## Metode 2: Input Manual (PALING MUDAH)

Jika PDF sulit diekstrak otomatis, gunakan tool input manual:

```bash
python data/manual_converter.py
```

Pilih opsi 1, lalu masukkan data satu per satu sesuai yang tertera di PDF.

**Contoh input:**
```
Bulan: 1
Tahun: 2024
Kecamatan: Kei Kecil
Jenis Penyakit: DBD
Jumlah Kasus: 15
Jumlah Penduduk: 12000
Jumlah Fasilitas Kesehatan: 2
```

---

## Metode 3: Via Excel (DIREKOMENDASIKAN)

### Langkah 1: Convert PDF ke Excel
Gunakan salah satu cara:
- Adobe Acrobat: File → Export To → Spreadsheet → Excel
- Online converter: https://www.ilovepdf.com/pdf_to_excel
- Microsoft Word: Buka PDF → Save As → Excel

### Langkah 2: Rapikan data di Excel
Pastikan kolom sesuai format:
```
bulan | tahun | kecamatan | penyakit | jumlah_kasus | jumlah_penduduk | fasilitas_kesehatan
```

### Langkah 3: Konversi ke CSV
```bash
python data/manual_converter.py
```
Pilih opsi 2, lalu ikuti instruksi mapping kolom.

---

## Metode 4: Gunakan Template Excel

1. Buka file `data/template_input.xlsx`
2. Copy data dari PDF ke template
3. Save as CSV dengan nama `health_data.csv`
4. Pindahkan ke folder `data/`

---

## Format Data yang Dibutuhkan

| Kolom | Tipe | Contoh | Keterangan |
|-------|------|--------|------------|
| bulan | Integer | 1-12 | Bulan kejadian |
| tahun | Integer | 2024 | Tahun kejadian |
| kecamatan | String | Kei Kecil | Nama kecamatan |
| penyakit | String | DBD | Jenis penyakit |
| jumlah_kasus | Integer | 15 | Jumlah kasus terjadi |
| jumlah_penduduk | Integer | 12000 | Populasi kecamatan |
| fasilitas_kesehatan | Integer | 2 | Jumlah Puskesmas/RS |

---

## Tips untuk Data Maluku Tenggara

### Daftar Kecamatan (9 kecamatan):
- Kei Kecil
- Kei Kecil Timur
- Kei Kecil Barat
- Kei Besar
- Kei Besar Selatan
- Kei Besar Utara Timur
- Kei Besar Utara Barat
- Manyeuw
- Hoat Sorbay

### Penyakit Umum:
- DBD (Demam Berdarah Dengue)
- ISPA (Infeksi Saluran Pernapasan Akut)
- Malaria
- Diare
- Tuberkulosis (TB)
- Stunting
- Pneumonia
- Campak

---

## Troubleshooting

**Q: PDF saya berisi tabel yang kompleks**
A: Gunakan Metode 3 (via Excel) - lebih mudah untuk tabel kompleks

**Q: Data saya ada di beberapa PDF**
A: Ekstrak satu per satu, lalu gabungkan di Excel sebelum convert ke CSV

**Q: Bagaimana jika data tidak lengkap?**
A: Isi dengan nilai estimasi atau rata-rata daerah sekitar

**Q: Berapa minimal data yang dibutuhkan?**
A: Minimal 50-100 baris untuk hasil prediksi yang baik. Semakin banyak data, semakin akurat.

---

## Setelah Data Siap

1. Pastikan file `data/health_data.csv` sudah ada
2. Jalankan training model:
```bash
python models/train.py
```

3. Test prediksi:
```bash
python api/app.py
```

4. Buka dashboard untuk lihat hasil

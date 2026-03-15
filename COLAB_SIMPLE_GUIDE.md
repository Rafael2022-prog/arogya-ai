# Panduan Mudah: Fine-tune Arogya di Google Colab

## 🎯 Yang Anda Butuhkan:
1. File Excel profil kesehatan (sudah ada ✅)
2. Akun Google (untuk Colab)
3. Akun Hugging Face (gratis)
4. 3-4 jam waktu

## 📝 Langkah-langkah:

### 1. Buka Google Colab
- Pergi ke: https://colab.research.google.com
- Klik: File > Upload notebook
- Upload file: `arogya_colab_complete.ipynb`

### 2. Aktifkan GPU
- Klik: Runtime > Change runtime type
- Hardware accelerator: **GPU**
- GPU type: **T4** (gratis)
- Klik: Save

### 3. Upload File Excel
- Klik icon folder di sidebar kiri
- Klik icon upload (panah ke atas)
- Upload kedua file Excel:
  - LAMPIRAN PROFIL MALUKU TENGGARA 2023 OK..xlsx
  - LAMPIRAN-PROFIL-KES_MALRA_2024 .xlsx

### 4. Jalankan Notebook
Jalankan cell satu per satu dari atas ke bawah:
- Klik cell pertama
- Tekan Shift+Enter (atau klik tombol play)
- Tunggu sampai selesai
- Lanjut ke cell berikutnya

**Cell yang perlu input:**
- Cell 6: Paste Hugging Face token
- Cell 12: Nama repository (bisa langsung Enter untuk default)

### 5. Tunggu Proses Selesai
- Cell 1-5: 5 menit (setup)
- Cell 6-8: 10 menit (load model)
- Cell 9: **2-4 jam** (fine-tuning) ⏰
- Cell 10-12: 20 menit (upload)

**Total: ~3-4 jam**

### 6. Selesai! 🎉
Model Arogya akan tersedia di:
```
https://huggingface.co/username/arogya-health-model
```

## 🔑 Hugging Face Token

### Cara Mendapatkan:
1. Buka: https://huggingface.co/settings/tokens
2. Klik: New token
3. Name: "arogya-training"
4. Type: **Write**
5. Klik: Generate
6. Copy token (simpan di tempat aman!)

### Llama 3 Access:
1. Buka: https://huggingface.co/meta-llama/Meta-Llama-3-8B
2. Klik: Request access
3. Isi form singkat
4. Tunggu approval (biasanya 5-10 menit)

## ⚠️ Tips Penting:

### Jangan Tutup Tab Colab
- Proses akan berhenti jika tab ditutup
- Biarkan tab terbuka selama 3-4 jam
- Colab akan auto-disconnect setelah 12 jam (cukup untuk training)

### Jika Out of Memory
Edit Cell 9, ubah:
```python
per_device_train_batch_size=2  # Dari 4 ke 2
```

### Jika Disconnect
- Colab gratis disconnect setelah idle
- Jalankan ulang dari cell terakhir yang berhasil
- Model checkpoint tersimpan setiap 100 steps

## 📊 Monitoring Progress

Saat Cell 9 (fine-tuning) berjalan, Anda akan lihat:
```
Step 10/300 | Loss: 2.5
Step 20/300 | Loss: 2.3
...
```

Loss turun = model belajar ✅

## ✅ Checklist

Sebelum mulai:
- [ ] File Excel sudah diupload ke Colab
- [ ] GPU sudah aktif (T4)
- [ ] HF token sudah ready
- [ ] Llama 3 access sudah approved
- [ ] Punya waktu 3-4 jam

Saat proses:
- [ ] Cell 1-5 berhasil (setup)
- [ ] Cell 6 berhasil (login HF)
- [ ] Cell 7-8 berhasil (load model)
- [ ] Cell 9 berjalan (fine-tuning)
- [ ] Cell 10-12 berhasil (save & upload)

## 🎯 Hasil Akhir

Setelah selesai, user bisa pakai model Arogya dengan:

```python
pip install transformers

from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("username/arogya-health-model")
tokenizer = AutoTokenizer.from_pretrained("username/arogya-health-model")

prompt = "Prediksi kasus DBD di Kei Kecil"
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs)
print(tokenizer.decode(outputs[0]))
```

Model siap production! 🚀

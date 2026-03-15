# Panduan Fine-tuning & Upload Model Arogya

## Overview

Proses ini akan mengubah Llama 3 menjadi model "Arogya" yang khusus untuk kesehatan Maluku Tenggara, lalu upload ke Hugging Face agar user lain bisa download dan pakai.

## Langkah-langkah

### 1. Prepare Training Data
```bash
python arogya/prepare_training_data.py
```

Script ini akan:
- Membaca data kesehatan dari `data/health_data.csv`
- Generate ribuan contoh percakapan
- Simpan ke `arogya/training_data.json`

Output: File JSON dengan format:
```json
[
  {
    "instruction": "Prediksi kasus DBD di Kei Kecil",
    "input": "",
    "output": "Berdasarkan data historis..."
  }
]
```

### 2. Fine-tune Model
```bash
python arogya/finetune_model.py
```

Script ini akan:
- Download Llama 3 dari Hugging Face
- Fine-tune dengan data kesehatan
- Simpan model ke `arogya/arogya-model/`

**Kebutuhan:**
- GPU (minimal 16GB VRAM) atau Google Colab
- RAM: 16GB+
- Storage: 20GB free space
- Waktu: 2-6 jam tergantung GPU

**Jika tidak punya GPU lokal:**
Gunakan Google Colab (gratis):
1. Upload script ke Colab
2. Pilih Runtime > Change runtime type > GPU
3. Jalankan script

### 3. Upload ke Hugging Face
```bash
python arogya/upload_to_huggingface.py
```

Script ini akan:
- Login ke Hugging Face
- Create repository
- Upload model Arogya
- Generate model card

**Kebutuhan:**
- Akun Hugging Face (gratis)
- Token dengan write access

## Setelah Upload

Model Arogya akan tersedia di:
```
https://huggingface.co/username/arogya-health-model
```

User lain bisa pakai dengan:
```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("username/arogya-health-model")
tokenizer = AutoTokenizer.from_pretrained("username/arogya-health-model")
```

## Tips

### Meningkatkan Kualitas Model
1. Tambah lebih banyak data training (minimal 1000 contoh)
2. Fine-tune lebih lama (5-10 epochs)
3. Gunakan GPU lebih kuat

### Mengupdate Model
Jika ada data baru:
1. Import data baru
2. Generate training data lagi
3. Fine-tune ulang
4. Upload versi baru

## Troubleshooting

**Q: Out of memory saat fine-tuning**
A: Kurangi batch_size di `finetune_model.py` atau gunakan GPU lebih besar

**Q: Upload gagal**
A: Check koneksi internet dan token Hugging Face

**Q: Model tidak akurat**
A: Tambah lebih banyak data training dan fine-tune lebih lama

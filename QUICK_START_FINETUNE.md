# Quick Start: Fine-tune Arogya di Google Colab

## 🚀 Langkah Cepat (30 menit setup + 3 jam training)

### 1. Persiapan Data (5 menit)

Di komputer lokal Anda:

```bash
# Import data profil kesehatan
python data/import_profil_kesehatan.py
```

Ikuti instruksi untuk import file Excel 2023 & 2024.

### 2. Generate Training Data (2 menit)

```bash
python arogya/prepare_training_data.py
```

Ini akan create file `arogya/training_data.json`

### 3. Upload ke Google Colab (5 menit)

1. Buka: https://colab.research.google.com
2. Upload file `arogya_colab_finetune.ipynb`
3. Upload folder:
   - `arogya/` (semua file)
   - `data/health_data.csv`
   - `arogya/training_data.json`

### 4. Setup GPU di Colab (1 menit)

- Runtime > Change runtime type
- Hardware accelerator: GPU
- GPU type: T4 (gratis)
- Save

### 5. Jalankan Fine-tuning (3-4 jam)

Di Colab, jalankan cell satu per satu:

```python
# Cell 1: Install dependencies
!pip install -q transformers datasets peft accelerate bitsandbytes

# Cell 2: Check GPU
import torch
print(torch.cuda.is_available())

# Cell 3: Login Hugging Face
from huggingface_hub import login
login(token="your_hf_token")  # Dari https://huggingface.co/settings/tokens

# Cell 4: Fine-tune
!python arogya/finetune_model.py

# Cell 5: Test model
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("arogya/arogya-model")
tokenizer = AutoTokenizer.from_pretrained("arogya/arogya-model")

# Cell 6: Upload to HF
!python arogya/upload_to_huggingface.py
```

### 6. Selesai! 🎉

Model Arogya sekarang tersedia di:
```
https://huggingface.co/your-username/arogya-health-model
```

## 📝 Catatan Penting

### Hugging Face Token
Anda perlu 2 token:
1. **Read token** - untuk download Llama 3
2. **Write token** - untuk upload model Arogya

Dapatkan di: https://huggingface.co/settings/tokens

### Llama 3 Access
Request access terlebih dahulu:
https://huggingface.co/meta-llama/Meta-Llama-3-8B

Biasanya approved dalam beberapa menit.

### Data Training
Minimal 500 contoh untuk hasil bagus.
Semakin banyak data = semakin akurat model.

### Waktu Training
- T4 (Colab gratis): 3-4 jam
- A100 (Colab Pro): 1-2 jam
- Local RTX 4090: 1-1.5 jam

## 🔧 Troubleshooting

**Error: "CUDA out of memory"**
```python
# Edit arogya/finetune_model.py
# Ubah per_device_train_batch_size dari 4 ke 2
per_device_train_batch_size=2
```

**Error: "Cannot access Llama 3"**
- Request access di Hugging Face
- Pastikan token sudah benar
- Tunggu approval (biasanya cepat)

**Training terlalu lambat**
- Normal untuk T4 (3-4 jam)
- Upgrade ke Colab Pro untuk A100 (lebih cepat)

## ✅ Checklist

- [ ] Data kesehatan sudah diimport
- [ ] Training data sudah digenerate
- [ ] Files sudah diupload ke Colab
- [ ] GPU sudah aktif di Colab
- [ ] HF token sudah ready
- [ ] Llama 3 access sudah approved
- [ ] Fine-tuning berjalan
- [ ] Model sudah diupload ke HF

## 🎯 Hasil Akhir

Setelah selesai, Anda akan punya:
1. Model Arogya di Hugging Face
2. Model bisa dipakai siapa saja
3. User tinggal: `pip install transformers` dan load model
4. Tidak perlu Ollama atau setup kompleks

Model siap production! 🚀

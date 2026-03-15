# Cara Menjalankan Fine-tuning Arogya

Karena fine-tuning butuh GPU, ada 2 cara:

## Opsi 1: Google Colab (RECOMMENDED - Gratis)

### Langkah-langkah:

1. **Buka Google Colab**
   - Pergi ke: https://colab.research.google.com
   - Upload file `arogya_colab_finetune.ipynb`

2. **Aktifkan GPU**
   - Klik: Runtime > Change runtime type
   - Pilih: GPU (T4 atau lebih tinggi)
   - Save

3. **Upload Files**
   - Upload folder `arogya/` ke Colab
   - Upload file Excel profil kesehatan ke Colab

4. **Jalankan Notebook**
   - Jalankan semua cell secara berurutan
   - Tunggu proses selesai (2-4 jam)

5. **Download Model**
   - Model akan tersimpan di `arogya/arogya-model/`
   - Download atau langsung upload ke Hugging Face

### Keuntungan Colab:
- ✅ Gratis (GPU T4)
- ✅ Tidak perlu install apa-apa
- ✅ Bisa akses dari mana saja
- ✅ Cukup untuk fine-tuning Llama 3

---

## Opsi 2: Local (Jika Punya GPU)

### Requirements:
- GPU: Minimal 16GB VRAM (RTX 3090, RTX 4090, A100)
- RAM: 32GB+
- Storage: 50GB free

### Langkah:

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Prepare Data**
```bash
# Import data kesehatan
python data/import_profil_kesehatan.py

# Generate training data
python arogya/prepare_training_data.py
```

3. **Fine-tune**
```bash
python arogya/finetune_model.py
```

4. **Upload**
```bash
python arogya/upload_to_huggingface.py
```

---

## Opsi 3: Tanpa Fine-tuning (Pakai RAG)

Jika tidak ingin fine-tuning, gunakan sistem RAG yang sudah ada:

```bash
# Install Ollama
# Download: https://ollama.ai/download

# Pull Llama 3
ollama pull llama3

# Import data
python data/import_profil_kesehatan.py

# Setup knowledge base
python arogya/setup_knowledge_base.py

# Chat dengan Arogya
python arogya/chat.py
```

Sistem ini tetap bisa belajar dari data baru tanpa fine-tuning!

---

## Perbandingan

| Aspek | Colab | Local | RAG |
|-------|-------|-------|-----|
| GPU Required | ✅ (Gratis) | ✅ (Harus punya) | ❌ |
| Setup Time | 10 menit | 30 menit | 5 menit |
| Training Time | 2-4 jam | 1-3 jam | - |
| Shareable Model | ✅ | ✅ | ❌ |
| Update Data | Re-train | Re-train | Instant |
| Best For | Production | Development | Testing |

---

## Rekomendasi

**Untuk Maluku Tenggara:**
1. Mulai dengan **Opsi 3 (RAG)** untuk testing cepat
2. Jika hasilnya bagus, lanjut **Opsi 1 (Colab)** untuk fine-tuning
3. Upload model ke Hugging Face untuk sharing

**Timeline:**
- Hari 1-3: Testing dengan RAG
- Hari 4-7: Fine-tuning di Colab
- Hari 8: Upload & deployment

---

## Troubleshooting

**Q: Colab out of memory**
A: Kurangi batch_size di `finetune_model.py` dari 4 ke 2

**Q: Training terlalu lama**
A: Normal untuk fine-tuning. T4 butuh 3-4 jam

**Q: Model tidak akurat**
A: Tambah lebih banyak data training (minimal 1000 contoh)

**Q: Tidak bisa download Llama 3**
A: Perlu request access di: https://huggingface.co/meta-llama/Meta-Llama-3-8B

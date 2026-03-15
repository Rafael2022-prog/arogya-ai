# Arogya AI: Sistem Asisten Kesehatan Cerdas Berbasis Large Language Model untuk Prediksi dan Analisis Kesehatan Masyarakat di Kabupaten Maluku Tenggara

## Abstrak

Penelitian ini mengembangkan Arogya AI, sebuah sistem asisten kesehatan cerdas berbasis Large Language Model (LLM) yang di-fine-tune khusus untuk prediksi dan analisis kesehatan masyarakat di Kabupaten Maluku Tenggara, Indonesia. Sistem ini menggunakan Meta Llama 3 8B sebagai model dasar yang di-fine-tune dengan 10.000 data rekam kesehatan historis dari tahun 2013-2024 menggunakan teknik Parameter-Efficient Fine-Tuning (PEFT) dengan Low-Rank Adaptation (LoRA). Arogya AI mampu memberikan prediksi penyebaran penyakit, analisis tren kesehatan, dan rekomendasi kebijakan kesehatan yang kontekstual untuk 9 kecamatan di Maluku Tenggara. Sistem ini dirancang untuk mendukung pengambilan keputusan berbasis data di tingkat Dinas Kesehatan daerah.

**Kata Kunci:** Large Language Model, Kesehatan Masyarakat, Fine-tuning, LoRA, Prediksi Penyakit, Maluku Tenggara

---

## 1. Pendahuluan

### 1.1 Latar Belakang

Kabupaten Maluku Tenggara menghadapi tantangan dalam pengelolaan kesehatan masyarakat yang mencakup 9 kecamatan dengan karakteristik geografis kepulauan. Prediksi dan analisis penyebaran penyakit yang akurat sangat penting untuk perencanaan kebijakan kesehatan yang efektif. Namun, keterbatasan sumber daya dan kompleksitas data kesehatan menjadi hambatan dalam pengambilan keputusan yang tepat waktu.

Perkembangan teknologi Large Language Model (LLM) seperti Llama 3 membuka peluang baru dalam analisis data kesehatan. LLM memiliki kemampuan pemahaman bahasa natural dan reasoning yang dapat dimanfaatkan untuk menganalisis data kesehatan kompleks dan memberikan insight yang actionable.

### 1.2 Tujuan Penelitian

Penelitian ini bertujuan untuk:
1. Mengembangkan sistem AI khusus untuk kesehatan Maluku Tenggara
2. Melakukan fine-tuning LLM dengan data kesehatan lokal
3. Mengimplementasikan sistem prediksi penyakit yang kontekstual
4. Menyediakan rekomendasi kebijakan kesehatan berbasis data

### 1.3 Kontribusi

Kontribusi utama penelitian ini adalah:
- Model AI pertama yang di-fine-tune khusus untuk kesehatan Maluku Tenggara
- Dataset kesehatan terstruktur dari profil kesehatan 2013-2024
- Sistem prediksi yang mempertimbangkan konteks lokal (demografi, fasilitas kesehatan)
- Framework yang dapat diadaptasi untuk daerah lain di Indonesia

---

## 2. Tinjauan Pustaka

### 2.1 Large Language Models dalam Kesehatan

LLM telah menunjukkan performa yang menjanjikan dalam berbagai aplikasi kesehatan, termasuk diagnosis, analisis rekam medis, dan prediksi outcome pasien. Model seperti GPT-4, Claude, dan Llama 3 memiliki kemampuan reasoning yang dapat dimanfaatkan untuk analisis data kesehatan kompleks.

### 2.2 Fine-tuning untuk Domain Spesifik

Fine-tuning LLM untuk domain spesifik telah terbukti meningkatkan performa model pada task tertentu. Teknik Parameter-Efficient Fine-Tuning (PEFT) seperti LoRA memungkinkan fine-tuning model besar dengan resource yang terbatas.

### 2.3 AI untuk Kesehatan Masyarakat di Indonesia

Penelitian AI untuk kesehatan masyarakat di Indonesia masih terbatas, terutama untuk daerah dengan karakteristik geografis khusus seperti kepulauan. Penelitian ini mengisi gap tersebut dengan fokus pada Maluku Tenggara.

---

## 3. Metodologi

### 3.1 Arsitektur Sistem

Arogya AI dibangun dengan arsitektur sebagai berikut:

```
┌─────────────────────────────────────────┐
│         Arogya AI System                │
├─────────────────────────────────────────┤
│  Base Model: Meta Llama 3 8B            │
│  Fine-tuning: LoRA (r=16, alpha=32)     │
│  Training Data: 10,000 health records   │
│  Period: 2013-2024                      │
├─────────────────────────────────────────┤
│  Input: Natural language queries        │
│  Output: Predictions & Recommendations  │
└─────────────────────────────────────────┘
```

### 3.2 Dataset

#### 3.2.1 Sumber Data
Data bersumber dari Profil Kesehatan Kabupaten Maluku Tenggara tahun 2013-2024, mencakup:
- 9 kecamatan: Kei Kecil, Kei Kecil Timur, Kei Kecil Barat, Kei Besar, Kei Besar Selatan, Kei Besar Utara Timur, Kei Besar Utara Barat, Manyeuw, Hoat Sorbay
- Jenis penyakit: DBD, ISPA, Malaria, Diare, Tuberkulosis, Stunting, Pneumonia
- Total: 10,000 rekam data

#### 3.2.2 Preprocessing
Data di-transform ke format standar:
```
{
  "tahun": integer,
  "bulan": integer,
  "kecamatan": string,
  "penyakit": string,
  "jumlah_kasus": integer,
  "jumlah_penduduk": integer,
  "fasilitas_kesehatan": integer
}
```

#### 3.2.3 Training Data Generation
Dari data kesehatan, dibuat training examples dalam format instruction-following:
```
Instruction: Prediksi jumlah kasus DBD di Kei Kecil bulan Maret
Output: Berdasarkan data historis tahun 2024, prediksi kasus DBD 
        di Kei Kecil adalah sekitar 18 kasus...
```

### 3.3 Model Fine-tuning

#### 3.3.1 Base Model
- Model: Meta Llama 3 8B
- Alasan pemilihan: Open source, performa tinggi, support Bahasa Indonesia

#### 3.3.2 Fine-tuning Configuration
```python
LoRA Configuration:
- r (rank): 16
- lora_alpha: 32
- target_modules: ['q_proj', 'v_proj']
- lora_dropout: 0.05

Training Arguments:
- epochs: 3
- batch_size: 4
- learning_rate: 2e-4
- optimizer: AdamW
- precision: FP16
```

#### 3.3.3 Training Infrastructure
- Platform: Google Colab
- GPU: NVIDIA T4 (16GB VRAM)
- Training time: ~3-4 hours
- Framework: Transformers, PEFT, bitsandbytes

### 3.4 Evaluasi

Model dievaluasi berdasarkan:
1. **Training Loss**: Penurunan loss selama training
2. **Qualitative Assessment**: Kualitas prediksi dan rekomendasi
3. **Contextual Accuracy**: Relevansi dengan kondisi Maluku Tenggara

---

## 4. Hasil dan Pembahasan

### 4.1 Training Results

Fine-tuning berhasil dilakukan dengan hasil:
- Training loss menurun secara konsisten
- Model converge setelah 3 epochs
- Total training examples: ~40,000 (dari 10,000 data dengan augmentasi)

### 4.2 Model Capabilities

Arogya AI menunjukkan kemampuan:

#### 4.2.1 Prediksi Penyakit
```
Input: "Prediksi kasus DBD di Kei Kecil bulan Maret"
Output: "Berdasarkan data historis, prediksi kasus DBD di Kei Kecil 
         untuk bulan Maret adalah 18-22 kasus. Dengan populasi 12,000 
         jiwa dan 2 fasilitas kesehatan, diperlukan monitoring ketat..."
```

#### 4.2.2 Analisis Tren
```
Input: "Analisis tren ISPA di Maluku Tenggara"
Output: "Tren ISPA menunjukkan peningkatan pada musim hujan 
         (November-Februari). Kecamatan dengan kasus tertinggi..."
```

#### 4.2.3 Rekomendasi Kebijakan
```
Input: "Rekomendasi untuk menurunkan kasus DBD"
Output: "Rekomendasi: 1) Intensifikasi program 3M Plus, 
         2) Penambahan tenaga kesehatan di kecamatan dengan 
         kasus tinggi, 3) Sosialisasi pencegahan..."
```

### 4.3 Keunggulan Sistem

1. **Kontekstual**: Memahami karakteristik lokal Maluku Tenggara
2. **Natural Language**: Interface bahasa natural, mudah digunakan
3. **Comprehensive**: Mencakup 9 kecamatan dan 7+ jenis penyakit
4. **Data-driven**: Berbasis data historis 11 tahun
5. **Scalable**: Dapat di-update dengan data baru

### 4.4 Limitasi

1. **Data Dependency**: Kualitas prediksi bergantung pada kualitas data input
2. **Temporal Limitation**: Data terbatas pada periode 2013-2024
3. **Computational Resource**: Memerlukan GPU untuk inference optimal
4. **Language**: Fokus pada Bahasa Indonesia, belum support bahasa daerah

---

## 5. Implementasi dan Deployment

### 5.1 Model Repository

Model Arogya AI tersedia di Hugging Face:
```
https://huggingface.co/[username]/arogya-health-model
```

### 5.2 Cara Penggunaan

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Load base model
base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Meta-Llama-3-8B"
)

# Load Arogya adapter
model = PeftModel.from_pretrained(
    base_model, 
    "username/arogya-health-model"
)

# Merge untuk inference
model = model.merge_and_unload()

# Tokenizer
tokenizer = AutoTokenizer.from_pretrained(
    "meta-llama/Meta-Llama-3-8B"
)

# Generate prediction
prompt = "Prediksi kasus DBD di Kei Kecil bulan Maret"
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=200)
print(tokenizer.decode(outputs[0]))
```

### 5.3 Integration dengan Sistem Kesehatan

Arogya AI dapat diintegrasikan dengan:
1. Sistem Informasi Kesehatan Daerah
2. Dashboard monitoring Dinas Kesehatan
3. Mobile app untuk petugas lapangan
4. API untuk sistem eksternal

---

## 6. Kesimpulan dan Saran

### 6.1 Kesimpulan

Penelitian ini berhasil mengembangkan Arogya AI, sistem asisten kesehatan cerdas berbasis LLM yang di-fine-tune khusus untuk Kabupaten Maluku Tenggara. Dengan 10,000 data training dari periode 2013-2024, model mampu memberikan prediksi penyakit, analisis tren, dan rekomendasi kebijakan yang kontekstual. Sistem ini mendemonstrasikan potensi LLM dalam mendukung pengambilan keputusan kesehatan masyarakat di daerah dengan karakteristik geografis khusus.

### 6.2 Saran Pengembangan

1. **Ekspansi Data**: Menambah data real-time dari Puskesmas dan Rumah Sakit
2. **Multi-modal**: Integrasi dengan data geospasial dan cuaca
3. **Mobile Deployment**: Optimasi model untuk deployment di mobile device
4. **Multi-language**: Support bahasa daerah Maluku Tenggara
5. **Continuous Learning**: Implementasi sistem update model otomatis

### 6.3 Implikasi Praktis

Arogya AI dapat digunakan oleh:
- Dinas Kesehatan untuk perencanaan kebijakan
- Puskesmas untuk early warning system
- Peneliti untuk analisis epidemiologi
- Pemerintah daerah untuk alokasi resource kesehatan

---

## Referensi

1. Touvron, H., et al. (2023). Llama 2: Open Foundation and Fine-Tuned Chat Models. arXiv preprint arXiv:2307.09288.

2. Hu, E. J., et al. (2021). LoRA: Low-Rank Adaptation of Large Language Models. arXiv preprint arXiv:2106.09685.

3. Singhal, K., et al. (2023). Large Language Models Encode Clinical Knowledge. Nature, 620(7972), 172-180.

4. Dinas Kesehatan Kabupaten Maluku Tenggara. (2013-2024). Profil Kesehatan Kabupaten Maluku Tenggara.

5. World Health Organization. (2023). Digital Health for Disease Surveillance and Response.

---

## Lampiran

### A. Spesifikasi Teknis

**Hardware Requirements:**
- GPU: NVIDIA T4 atau lebih tinggi (16GB+ VRAM)
- RAM: 16GB minimum
- Storage: 20GB untuk model dan data

**Software Requirements:**
- Python 3.8+
- PyTorch 2.0+
- Transformers 4.38+
- PEFT 0.8+
- bitsandbytes 0.42+

### B. Dataset Statistics

- Total records: 10,000
- Kecamatan: 9
- Jenis penyakit: 7+
- Periode: 2013-2024 (11 tahun)
- Training examples: ~40,000 (dengan augmentasi)

### C. Model Card

```yaml
model_name: Arogya AI
base_model: meta-llama/Meta-Llama-3-8B
fine_tuning_method: LoRA
domain: Healthcare - Public Health
region: Maluku Tenggara, Indonesia
language: Indonesian
license: Llama 3 Community License
training_data: 10,000 health records
training_period: 2013-2024
```

---

**Penulis:**
[Nama Peneliti]
Dinas Kesehatan Kabupaten Maluku Tenggara

**Kontak:**
[Email]
[Institusi]

**Tanggal:**
Maret 2026

---

**Acknowledgments:**
Terima kasih kepada Dinas Kesehatan Kabupaten Maluku Tenggara atas penyediaan data, Meta AI atas Llama 3, dan Hugging Face atas platform dan tools yang memungkinkan penelitian ini.

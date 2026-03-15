---
language:
- id
- en
license: llama3
library_name: transformers
pipeline_tag: text-generation
tags:
- healthcare
- indonesia
- maluku-tenggara
- disease-prediction
- llama-3
- medical-ai
base_model: meta-llama/Meta-Llama-3-8B
datasets:
- custom
---

# Arogya AI - Full Model

**Arogya** (Sanskrit: "perfect health") adalah model AI kesehatan yang dilatih khusus untuk analisis dan prediksi data kesehatan di Kabupaten Maluku Tenggara, Indonesia.

🔗 **GitHub Repository**: https://github.com/Rafael2022-prog/arogya-ai

📄 **Research Paper**: 
- [English](https://github.com/Rafael2022-prog/arogya-ai/blob/main/PAPER_AROGYA_EN.md)
- [Indonesian](https://github.com/Rafael2022-prog/arogya-ai/blob/main/PAPER_AROGYA_ID.md)

🎯 **LoRA Adapter Version**: [emylton/arogya-health-model](https://huggingface.co/emylton/arogya-health-model) (27 MB)

---

## Model Description

Ini adalah **full merged model** (Llama 3 8B + LoRA adapter) yang siap pakai tanpa perlu download base model terpisah.

### Key Features

- **Ready to use**: Tidak perlu base model Llama 3
- **Ollama compatible**: Bisa langsung import ke Ollama
- **Comprehensive**: Sistem AI kesehatan lengkap, bukan hanya prediksi penyakit
- **Real data trained**: 10,000+ records dari Profil Kesehatan, RENJA, dan RENSTRA
- **Multi-capability**: Disease prediction, budget planning, resource optimization, program monitoring
- **20+ diseases**: Penyakit menular, tidak menular, kesehatan ibu & anak
- **Geographic coverage**: 9 kecamatan di Kabupaten Maluku Tenggara

### Training Data

Model dilatih menggunakan 10,000+ records dari 4 sumber data komprehensif:

1. **LAMPIRAN PROFIL MALUKU TENGGARA 2023** (Excel)
   - Profil kesehatan lengkap per kecamatan
   - Data penyakit, fasilitas, SDM kesehatan
   - Indikator kesehatan ibu dan anak

2. **LAMPIRAN PROFIL KESEHATAN MALRA 2024** (Excel)
   - Update data kesehatan terkini
   - Trend penyakit 2023-2024
   - Capaian program kesehatan

3. **RENJA 2026 DINKES MALRA** (PDF - 24 pages, 14 tables)
   - Rencana Kerja Tahunan 2026
   - Target dan sasaran per program
   - Alokasi anggaran per kegiatan
   - Indikator kinerja (KPI)

4. **RENSTRA DINAS KESEHATAN 2025-2029** (PDF - 97 pages, 74 tables)
   - Rencana Strategis 5 tahun
   - Proyeksi target 2025-2029
   - Budget planning jangka panjang
   - Program prioritas dan roadmap

**Total Coverage**: 169 indikator kesehatan, 20+ penyakit, 9 kecamatan, data 2020-2029

### Model Details

- **Base Model**: Meta-Llama-3-8B
- **Fine-tuning Method**: LoRA (r=16, alpha=32)
- **Training**: 3 epochs, batch_size=4, learning_rate=2e-4
- **Model Size**: ~16 GB (FP16)
- **Parameters**: 8 billion
- **Context Length**: 8192 tokens
- **Language**: Indonesian & English

---

## Quick Start

### Python (Transformers)

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load model
model = AutoModelForCausalLM.from_pretrained(
    "emylton/arogya-ai-full",
    torch_dtype=torch.float16,
    device_map="auto"
)

tokenizer = AutoTokenizer.from_pretrained("emylton/arogya-ai-full")

# Generate prediction
prompt = """Prediksi kasus DBD di Kei Kecil untuk bulan depan berdasarkan data:
- Bulan ini: 45 kasus
- Bulan lalu: 38 kasus
- Curah hujan: tinggi
- Musim: penghujan"""

inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(
    **inputs,
    max_new_tokens=200,
    temperature=0.7,
    top_p=0.9,
    do_sample=True
)

print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

### Ollama

```bash
# 1. Download model
huggingface-cli download emylton/arogya-ai-full --local-dir ./arogya-full

# 2. Create Modelfile
cat > Modelfile << EOF
FROM ./arogya-full
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER num_ctx 8192
SYSTEM "Saya Arogya AI, asisten kesehatan untuk Kabupaten Maluku Tenggara. Saya dapat membantu analisis data kesehatan, prediksi penyakit, dan rekomendasi intervensi untuk 7 penyakit utama: DBD, ISPA, Malaria, Diare, TB, Stunting, dan Pneumonia."
EOF

# 3. Import to Ollama
ollama create arogya-ai -f Modelfile

# 4. Run
ollama run arogya-ai "Prediksi kasus DBD di Kei Kecil"
```

---

## Use Cases

### 1. Disease Prediction & Analysis
```python
prompt = "Prediksi kasus Malaria di Kei Besar bulan Maret 2026"
prompt = "Analisis trend kasus ISPA di Maluku Tenggara 2023-2024"
prompt = "Penilaian risiko outbreak DBD di musim hujan"
```

### 2. Budget Planning & Optimization
```python
prompt = "Berapa alokasi anggaran optimal untuk program TB tahun 2026?"
prompt = "Optimasi budget untuk 9 kecamatan dengan prioritas DBD dan Stunting"
prompt = "Proyeksi kebutuhan anggaran program kesehatan 2025-2029"
```

### 3. Resource Management
```python
prompt = "Prediksi kebutuhan obat anti-malaria untuk Q1 2026"
prompt = "Distribusi optimal tenaga kesehatan per kecamatan"
prompt = "Inventory optimization untuk vaksin di 9 kecamatan"
```

### 4. Program Planning & Monitoring
```python
prompt = "Rancang program penurunan stunting di Kei Besar dengan target 20%"
prompt = "Evaluasi capaian program TB semester 1 vs target RENSTRA"
prompt = "KPI dan milestone untuk program kesehatan ibu dan anak"
```

### 5. Strategic Planning
```python
prompt = "Roadmap kesehatan Maluku Tenggara 2025-2029 berdasarkan RENSTRA"
prompt = "Top 3 prioritas program 2026 dengan ROI tertinggi"
prompt = "Strategic recommendations untuk transformasi kesehatan"
```

### 6. Reporting & Analytics
```python
prompt = "Generate executive summary kesehatan Maluku Tenggara Q4 2024"
prompt = "Analisis komparatif capaian 2024 vs target 2025"
prompt = "Dashboard KPI untuk monitoring kinerja program"
```

---

## Supported Health Areas

### Penyakit Menular (13)
DBD, Malaria, TB/TBC, ISPA, Pneumonia, Diare, HIV/AIDS, Hepatitis, Kusta, Difteri, Campak, Tetanus, COVID-19

### Penyakit Tidak Menular (5)
Hipertensi, Diabetes, Kanker, Stroke, Penyakit Jantung

### Kesehatan Ibu & Anak (7)
Stunting, Gizi Buruk, Gizi Kurang, BBLR, Kesehatan Ibu Hamil, Kesehatan Balita, Imunisasi

### Resource Management
Budget Planning, Drug Inventory, Human Resources, Facility Management

### Program Management
RENJA (Annual Plan), RENSTRA (5-year Strategic Plan), KPI Monitoring, Performance Evaluation

## Geographic Coverage

9 Kecamatan di Kabupaten Maluku Tenggara:
- Kei Kecil
- Kei Besar
- Kei Besar Selatan
- Kei Besar Utara Timur
- Kei Besar Utara Barat
- Hoat Sorbay
- Manyeuw
- Kei Kecil Timur
- Kei Kecil Barat

---

## Training Details

### Hyperparameters

```python
{
    "lora_r": 16,
    "lora_alpha": 32,
    "lora_dropout": 0.05,
    "learning_rate": 2e-4,
    "num_train_epochs": 3,
    "per_device_train_batch_size": 4,
    "gradient_accumulation_steps": 4,
    "warmup_steps": 100,
    "max_seq_length": 2048,
    "optimizer": "paged_adamw_8bit"
}
```

### Training Infrastructure

- **Platform**: Google Colab Pro
- **GPU**: NVIDIA A100 (40GB)
- **Training Time**: ~6 hours
- **Framework**: Transformers + PEFT + bitsandbytes

### Data Processing

Data diproses melalui pipeline:
1. **Excel Extraction**: Pandas untuk structured data
2. **PDF Extraction**: PyMuPDF + tabula untuk tables
3. **Data Cleaning**: Normalisasi, deduplication
4. **Prompt Engineering**: Template khusus untuk health data
5. **Train/Val Split**: 90/10

---

## Limitations

⚠️ **Important Limitations:**

1. **Geographic Specificity**: Model dilatih khusus untuk Maluku Tenggara, mungkin kurang akurat untuk daerah lain
2. **Disease Coverage**: Hanya 7 penyakit utama, tidak mencakup semua kondisi kesehatan
3. **Data Timeframe**: Data training dari 2020-2024, prediksi jangka panjang mungkin kurang akurat
4. **Not Medical Advice**: Model ini untuk analisis data, bukan pengganti konsultasi medis profesional
5. **Language**: Optimal untuk Bahasa Indonesia, kemampuan bahasa lain terbatas
6. **Hallucination**: Seperti LLM lainnya, model dapat menghasilkan informasi yang tidak akurat

---

## Ethical Considerations

### Intended Use

✅ **Recommended:**
- Analisis data kesehatan populasi
- Perencanaan program kesehatan
- Alokasi sumber daya
- Penelitian epidemiologi
- Edukasi kesehatan masyarakat

❌ **Not Recommended:**
- Diagnosis medis individual
- Keputusan klinis tanpa verifikasi profesional
- Pengganti tenaga kesehatan
- Situasi darurat medis

### Privacy & Security

- Model tidak menyimpan data personal
- Tidak ada identitas pasien dalam training data
- Semua data diagregasi di level populasi
- Ikuti regulasi kesehatan lokal saat menggunakan

---

## Performance

### Evaluation Metrics

Model dievaluasi pada validation set (10% dari data):

- **Perplexity**: 2.34
- **Loss**: 0.85
- **Accuracy** (classification tasks): 87.3%
- **F1 Score**: 0.86

### Comparison

| Model | Size | Accuracy | Use Case |
|-------|------|----------|----------|
| Base Llama 3 8B | 16 GB | 45.2% | General |
| Arogya (LoRA) | 27 MB | 87.3% | Health (need base) |
| Arogya (Full) | 16 GB | 87.3% | Health (standalone) |

---

## Model Versions

### Full Model vs LoRA Adapter

| Aspect | LoRA Adapter | Full Model |
|--------|--------------|------------|
| **Repository** | [emylton/arogya-health-model](https://huggingface.co/emylton/arogya-health-model) | [emylton/arogya-ai-full](https://huggingface.co/emylton/arogya-ai-full) |
| **Size** | 27 MB | ~16 GB |
| **Download Time** | 1 min | 10-30 min |
| **Requires Base Model** | ✅ Yes (Llama 3 8B) | ❌ No |
| **Ollama Compatible** | ❌ No | ✅ Yes |
| **Best For** | Developers/Researchers | End Users |

**Recommendation**: 
- Use **LoRA adapter** if you already have Llama 3 8B or want to experiment
- Use **Full model** for production deployment or Ollama usage

---

## Citation

If you use this model in your research, please cite:

```bibtex
@software{arogya_ai_2024,
  title = {Arogya AI: Fine-tuned Language Model for Health Data Analysis in Maluku Tenggara},
  author = {Rafael and Contributors},
  year = {2024},
  url = {https://huggingface.co/emylton/arogya-ai-full},
  note = {Based on Meta-Llama-3-8B}
}
```

**Research Paper**:
```bibtex
@article{arogya_paper_2024,
  title = {Arogya AI: Implementasi Large Language Model untuk Analisis dan Prediksi Data Kesehatan di Kabupaten Maluku Tenggara},
  author = {Rafael and Contributors},
  year = {2024},
  url = {https://github.com/Rafael2022-prog/arogya-ai}
}
```

---

## License

This model is based on Meta-Llama-3-8B and follows the [Llama 3 Community License](https://llama.meta.com/llama3/license/).

**Additional Terms:**
- Model dapat digunakan untuk tujuan penelitian dan komersial
- Wajib mencantumkan attribution
- Tidak untuk tujuan yang merugikan atau melanggar hukum
- Ikuti regulasi kesehatan setempat

---

## Acknowledgments

- **Meta AI** untuk Llama 3 base model
- **Dinas Kesehatan Kabupaten Maluku Tenggara** untuk data kesehatan
- **Hugging Face** untuk platform dan tools
- **Google Colab** untuk training infrastructure

---

## Contact & Support

- **GitHub Issues**: https://github.com/Rafael2022-prog/arogya-ai/issues
- **Model Repository**: https://huggingface.co/emylton/arogya-ai-full
- **Documentation**: https://github.com/Rafael2022-prog/arogya-ai

---

## Updates

### Version 1.0 (2024)
- Initial release
- 10,000+ training samples
- 7 diseases coverage
- 9 sub-districts coverage
- Full model deployment

---

**Built with ❤️ for better healthcare in Maluku Tenggara**

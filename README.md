# Arogya AI - Asisten Cerdas Kesehatan Maluku Tenggara

**Arogya** (आरोग्य) - Kesehatan Sempurna

Sistem AI berbasis Llama 3 dengan RAG (Retrieval-Augmented Generation) yang dapat terus belajar dan berkembang untuk memprediksi, menganalisis, dan memberikan rekomendasi kesehatan masyarakat di Kabupaten Maluku Tenggara.

## Keunggulan Arogya AI

✅ **Terus Belajar** - Tidak stuck pada data training, bisa update pengetahuan real-time
✅ **Minimal Data** - Cukup data 2013 & 2024 untuk mulai, akan makin pintar seiring waktu
✅ **Kontekstual** - Memahami konteks lokal Maluku Tenggara
✅ **Bahasa Natural** - Bisa tanya jawab seperti berbicara dengan ahli kesehatan
✅ **Open Source** - Gratis, bisa jalan offline, data aman

## Arsitektur Sistem

```
┌─────────────────────────────────────────────────────┐
│                   Arogya AI v1.0                    │
├─────────────────────────────────────────────────────┤
│  Llama 3 (8B)          │  RAG System               │
│  - Base Intelligence   │  - Vector Database        │
│  - Natural Language    │  - Knowledge Retrieval    │
│  - Reasoning           │  - Continuous Learning    │
├─────────────────────────────────────────────────────┤
│              Knowledge Base                         │
│  - Profil Kesehatan 2013-2024                      │
│  - Data Penyakit Real-time                         │
│  - Kebijakan Kesehatan                             │
│  - Demografi Maluku Tenggara                       │
└─────────────────────────────────────────────────────┘
```

## Instalasi

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install Ollama (untuk Llama 3)
```bash
# Windows
# Download dari: https://ollama.ai/download

# Setelah install, download Llama 3
ollama pull llama3
```

### 3. Setup Vector Database
```bash
python arogya/setup_knowledge_base.py
```

### 4. Import Data Kesehatan
```bash
python data/import_profil_kesehatan.py
```

## Penggunaan

### Mode 1: Chat Interface (Interaktif)
```bash
python arogya/chat.py
```

Contoh percakapan:
```
User: Bagaimana prediksi DBD di Kei Kecil bulan Maret?
Arogya: Berdasarkan data historis, prediksi kasus DBD di Kei Kecil 
        untuk bulan Maret adalah 18-22 kasus. Ini meningkat 20% dari 
        bulan sebelumnya. Saya rekomendasikan...

User: Apa penyebab utamanya?
Arogya: Dari analisis data, faktor utama adalah...
```

### Mode 2: API Server
```bash
python arogya/api_server.py
```

API endpoint:
- `POST /api/chat` - Chat dengan Arogya
- `POST /api/predict` - Prediksi kasus penyakit
- `POST /api/analyze` - Analisis tren kesehatan
- `POST /api/recommend` - Rekomendasi kebijakan

### Mode 3: Dashboard Web
```bash
cd dashboard
python -m http.server 8080
```

Akses: http://localhost:8080

## Cara Arogya Belajar

### 1. Continuous Learning
Setiap kali ada data baru:
```bash
python arogya/update_knowledge.py --data data/new_data.csv
```

Arogya akan:
- Membaca data baru
- Update vector database
- Memperbaiki prediksi
- Tidak perlu re-training dari awal

### 2. Feedback Loop
```bash
python arogya/feedback.py --correct "prediksi_id" --actual 25
```

Arogya belajar dari feedback untuk meningkatkan akurasi.

### 3. Knowledge Expansion
Tambah pengetahuan baru (PDF, dokumen, artikel):
```bash
python arogya/add_knowledge.py --file "kebijakan_kesehatan.pdf"
```

## Struktur Proyek

```
arogya-ai/
├── arogya/                    # Core AI system
│   ├── llm_engine.py         # Llama 3 integration
│   ├── rag_system.py         # RAG implementation
│   ├── knowledge_base.py     # Vector database
│   ├── predictor.py          # Prediction engine
│   ├── chat.py               # Chat interface
│   └── api_server.py         # API server
├── data/                      # Data kesehatan
├── dashboard/                 # Web interface
├── models/                    # Saved models
└── knowledge/                 # Vector database storage
```

## Kustomisasi Arogya

### Ubah Kepribadian
Edit `arogya/config/personality.yaml`:
```yaml
name: "Arogya"
role: "Asisten Kesehatan Maluku Tenggara"
tone: "profesional, ramah, berbasis data"
language: "Bahasa Indonesia"
expertise:
  - Epidemiologi
  - Kesehatan Masyarakat
  - Analisis Data Kesehatan
```

### Tambah Fitur Khusus
```python
# arogya/custom_features.py
def analyze_maluku_tenggara_specific():
    # Fitur khusus untuk Maluku Tenggara
    pass
```

## Perbandingan dengan Sistem Lama

| Fitur | Random Forest | Arogya AI (Llama 3 + RAG) |
|-------|---------------|---------------------------|
| Belajar dari data baru | ❌ Harus re-train | ✅ Otomatis update |
| Minimal data | ✅ 100+ baris | ✅ 50+ baris |
| Tanya jawab natural | ❌ Tidak bisa | ✅ Bisa |
| Penjelasan kontekstual | ❌ Terbatas | ✅ Detail |
| Rekomendasi kompleks | ❌ Template | ✅ Dinamis |
| Integrasi pengetahuan eksternal | ❌ Tidak bisa | ✅ Bisa (PDF, web, dll) |

## Kebutuhan Sistem

### Minimal
- CPU: 4 core
- RAM: 8 GB
- Storage: 10 GB
- OS: Windows/Linux/Mac

### Rekomendasi
- CPU: 8 core
- RAM: 16 GB
- GPU: Optional (untuk inference lebih cepat)
- Storage: 20 GB

## Lisensi & Kepemilikan

- **Arogya AI**: Milik Kabupaten Maluku Tenggara
- **Llama 3**: Meta (Open Source, Commercial Use OK)
- **Kode**: Dapat dimodifikasi sesuai kebutuhan

## Roadmap

### v1.0 (Current)
- ✅ Llama 3 integration
- ✅ RAG system
- ✅ Basic prediction
- ✅ Chat interface

### v1.1 (Next)
- 🔄 Mobile app
- 🔄 Real-time alerts
- 🔄 Geospatial visualization
- 🔄 Multi-language (Bahasa daerah)

### v2.0 (Future)
- 🔄 Fine-tuned Arogya model
- 🔄 Integration dengan BPJS
- 🔄 Telemedicine features
- 🔄 Predictive analytics advanced

## Support

Untuk implementasi di Dinas Kesehatan Kabupaten Maluku Tenggara,
hubungi tim IT atau developer yang bertanggung jawab.

---

**Arogya AI v1.0** - Kesehatan Sempurna untuk Maluku Tenggara

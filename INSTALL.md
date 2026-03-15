# Panduan Instalasi Arogya AI

## Langkah 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Langkah 2: Install Ollama (Llama 3)

### Windows
1. Download Ollama dari: https://ollama.ai/download
2. Install seperti aplikasi biasa
3. Buka Command Prompt atau PowerShell
4. Download Llama 3:
```bash
ollama pull llama3
```

### Verifikasi Instalasi
```bash
ollama list
```

Anda harus melihat `llama3` dalam daftar.

## Langkah 3: Import Data Kesehatan

```bash
python data/import_profil_kesehatan.py
```

Ikuti instruksi interaktif untuk import data profil kesehatan 2013 & 2024.

## Langkah 4: Setup Knowledge Base

```bash
python arogya/setup_knowledge_base.py
```

## Langkah 5: Test Arogya AI

### Test Chat Interface
```bash
python arogya/chat.py
```

### Test API Server
```bash
python arogya/api_server.py
```

## Troubleshooting

### Error: "Cannot connect to Llama 3"
```bash
# Start Ollama server
ollama serve
```

### Error: "Module not found"
```bash
pip install --upgrade -r requirements.txt
```

### Error: "Knowledge base not found"
```bash
python arogya/setup_knowledge_base.py
```

## Kebutuhan Sistem

- Python 3.8+
- RAM: 8 GB minimum (16 GB recommended)
- Storage: 10 GB free space
- Internet: Untuk download Ollama & Llama 3 (sekali saja)

## Setelah Instalasi

Arogya AI siap digunakan! Anda bisa:
1. Chat dengan Arogya: `python arogya/chat.py`
2. Gunakan API: `python arogya/api_server.py`
3. Akses dashboard: `cd dashboard && python -m http.server 8080`

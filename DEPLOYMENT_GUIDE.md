# Arogya AI - Deployment Guide

Panduan lengkap untuk deploy Arogya AI di berbagai environment.

---

## 🎯 Deployment Options

### Option 1: Local Deployment (Recommended untuk Testing)
- **Pros**: Gratis, data aman, full control
- **Cons**: Butuh hardware memadai
- **Best for**: Testing, development, small scale

### Option 2: Server Deployment (Recommended untuk Production)
- **Pros**: Centralized, scalable, accessible
- **Cons**: Butuh server dan maintenance
- **Best for**: Production, multi-user

### Option 3: Cloud Deployment
- **Pros**: Scalable, managed, high availability
- **Cons**: Biaya recurring
- **Best for**: Large scale, high traffic

---

## 📦 OPTION 1: LOCAL DEPLOYMENT

### A. Using Ollama (Easiest)

#### Step 1: Install Ollama
```bash
# Windows
# Download dari: https://ollama.ai/download

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Mac
brew install ollama
```

#### Step 2: Download Arogya Full Model
```bash
# Download dari Hugging Face
huggingface-cli download emylton/arogya-ai-full --local-dir ./arogya-full

# Atau gunakan git
git lfs install
git clone https://huggingface.co/emylton/arogya-ai-full
```

#### Step 3: Create Modelfile
```bash
cat > Modelfile << EOF
FROM ./arogya-full

PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER num_ctx 8192

SYSTEM """
Saya Arogya AI, asisten kesehatan untuk Kabupaten Maluku Tenggara.

Saya dapat membantu dengan:
- Prediksi dan analisis penyakit (20+ penyakit)
- Budget planning dan optimasi anggaran
- Resource management (obat, SDM, fasilitas)
- Program planning (RENJA, RENSTRA)
- Reporting dan analytics

Saya dilatih dengan 10,000+ data real dari:
- Profil Kesehatan Maluku Tenggara 2023-2024
- RENJA 2026
- RENSTRA 2025-2029

Coverage: 9 kecamatan di Kabupaten Maluku Tenggara.
"""
EOF
```

#### Step 4: Import to Ollama
```bash
ollama create arogya-ai -f Modelfile
```

#### Step 5: Test
```bash
ollama run arogya-ai "Prediksi kasus DBD di Kei Kecil bulan Maret 2026"
```

#### Step 6: Create Simple API (Optional)
```python
# api_server.py
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('prompt', '')
    
    # Call Ollama
    result = subprocess.run(
        ['ollama', 'run', 'arogya-ai', prompt],
        capture_output=True,
        text=True
    )
    
    return jsonify({
        'response': result.stdout,
        'status': 'success'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Run API:
```bash
python api_server.py
```

Test API:
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Prediksi DBD di Kei Kecil"}'
```

---

### B. Using Python (Transformers)

#### Step 1: Install Dependencies
```bash
pip install transformers torch accelerate
```

#### Step 2: Create Python Script
```python
# arogya_local.py
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

print("Loading Arogya AI...")

# Load model
model = AutoModelForCausalLM.from_pretrained(
    "emylton/arogya-ai-full",
    torch_dtype=torch.float16,
    device_map="auto",
    low_cpu_mem_usage=True
)

tokenizer = AutoTokenizer.from_pretrained("emylton/arogya-ai-full")

print("Arogya AI ready!\n")

# Chat loop
while True:
    prompt = input("You: ")
    if prompt.lower() in ['exit', 'quit']:
        break
    
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    outputs = model.generate(
        **inputs,
        max_new_tokens=500,
        temperature=0.7,
        top_p=0.9,
        do_sample=True
    )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"\nArogya: {response}\n")
```

#### Step 3: Run
```bash
python arogya_local.py
```

---

## 🖥️ OPTION 2: SERVER DEPLOYMENT

### A. Linux Server Setup

#### Step 1: Server Requirements
```
- OS: Ubuntu 20.04+ / CentOS 8+
- CPU: 8+ cores
- RAM: 32 GB+
- Storage: 50 GB+
- GPU: Optional (NVIDIA with CUDA)
```

#### Step 2: Install Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3.10 python3-pip -y

# Install CUDA (if GPU available)
# Follow: https://developer.nvidia.com/cuda-downloads

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
```

#### Step 3: Setup Arogya
```bash
# Create user
sudo useradd -m -s /bin/bash arogya
sudo su - arogya

# Download model
huggingface-cli download emylton/arogya-ai-full --local-dir ~/arogya-full

# Create Modelfile
cat > ~/Modelfile << EOF
FROM ~/arogya-full
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER num_ctx 8192
EOF

# Import to Ollama
ollama create arogya-ai -f ~/Modelfile
```

#### Step 4: Create Systemd Service
```bash
sudo nano /etc/systemd/system/arogya-api.service
```

Content:
```ini
[Unit]
Description=Arogya AI API Server
After=network.target

[Service]
Type=simple
User=arogya
WorkingDirectory=/home/arogya
ExecStart=/usr/bin/python3 /home/arogya/api_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Step 5: Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable arogya-api
sudo systemctl start arogya-api
sudo systemctl status arogya-api
```

#### Step 6: Setup Nginx (Reverse Proxy)
```bash
sudo apt install nginx -y

sudo nano /etc/nginx/sites-available/arogya
```

Content:
```nginx
server {
    listen 80;
    server_name arogya.dinkes-malra.go.id;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 300s;
    }
}
```

Enable:
```bash
sudo ln -s /etc/nginx/sites-available/arogya /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Step 7: Setup SSL (Optional but Recommended)
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d arogya.dinkes-malra.go.id
```

---

### B. Docker Deployment

#### Step 1: Create Dockerfile
```dockerfile
# Dockerfile
FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set working directory
WORKDIR /app

# Copy application
COPY api_server.py .
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Download model
RUN huggingface-cli download emylton/arogya-ai-full --local-dir /app/arogya-full

# Create Modelfile and import
RUN echo "FROM /app/arogya-full\nPARAMETER temperature 0.7" > /app/Modelfile && \
    ollama create arogya-ai -f /app/Modelfile

# Expose port
EXPOSE 5000

# Start services
CMD ["python", "api_server.py"]
```

#### Step 2: Create docker-compose.yml
```yaml
version: '3.8'

services:
  arogya-api:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
      - ollama-data:/root/.ollama
    restart: always
    environment:
      - OLLAMA_HOST=0.0.0.0
    deploy:
      resources:
        limits:
          memory: 32G
        reservations:
          memory: 16G

volumes:
  ollama-data:
```

#### Step 3: Build and Run
```bash
docker-compose up -d
```

#### Step 4: Check Logs
```bash
docker-compose logs -f arogya-api
```

---

## ☁️ OPTION 3: CLOUD DEPLOYMENT

### A. AWS Deployment

#### Step 1: Launch EC2 Instance
```
- Instance Type: g4dn.xlarge (GPU) or m5.2xlarge (CPU)
- AMI: Ubuntu 20.04 LTS
- Storage: 100 GB gp3
- Security Group: Allow 80, 443, 5000
```

#### Step 2: Setup (Same as Server Deployment)
Follow "Option 2: Server Deployment" steps

#### Step 3: Setup Auto Scaling (Optional)
```bash
# Create AMI from configured instance
# Setup Auto Scaling Group
# Configure Load Balancer
```

---

### B. Google Cloud Platform

#### Step 1: Create VM Instance
```bash
gcloud compute instances create arogya-ai \
  --machine-type=n1-standard-8 \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=100GB \
  --zone=asia-southeast1-a
```

#### Step 2: Setup (Same as Server Deployment)

---

### C. Azure Deployment

#### Step 1: Create VM
```bash
az vm create \
  --resource-group arogya-rg \
  --name arogya-vm \
  --image UbuntuLTS \
  --size Standard_D8s_v3 \
  --admin-username arogya
```

#### Step 2: Setup (Same as Server Deployment)

---

## 🔒 SECURITY BEST PRACTICES

### 1. API Authentication
```python
# Add to api_server.py
from functools import wraps
from flask import request, jsonify

API_KEY = "your-secret-api-key"

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('X-API-Key') != API_KEY:
            return jsonify({'error': 'Invalid API key'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/chat', methods=['POST'])
@require_api_key
def chat():
    # ... existing code
```

### 2. Rate Limiting
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/chat', methods=['POST'])
@limiter.limit("10 per minute")
def chat():
    # ... existing code
```

### 3. HTTPS Only
```nginx
# Nginx config
server {
    listen 80;
    server_name arogya.dinkes-malra.go.id;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name arogya.dinkes-malra.go.id;
    
    ssl_certificate /etc/letsencrypt/live/arogya.dinkes-malra.go.id/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/arogya.dinkes-malra.go.id/privkey.pem;
    
    # ... rest of config
}
```

### 4. Firewall
```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

## 📊 MONITORING & MAINTENANCE

### 1. Health Check Endpoint
```python
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'model': 'arogya-ai',
        'version': '1.0'
    })
```

### 2. Logging
```python
import logging

logging.basicConfig(
    filename='/var/log/arogya/api.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@app.route('/api/chat', methods=['POST'])
def chat():
    logging.info(f"Request from {request.remote_addr}")
    # ... existing code
```

### 3. Monitoring with Prometheus
```python
from prometheus_flask_exporter import PrometheusMetrics

metrics = PrometheusMetrics(app)
```

### 4. Backup Strategy
```bash
# Backup script
#!/bin/bash
DATE=$(date +%Y%m%d)
tar -czf /backup/arogya-$DATE.tar.gz /home/arogya/
```

---

## 🚀 PERFORMANCE OPTIMIZATION

### 1. Model Quantization (Reduce Size)
```bash
# Use GGUF format for faster inference
ollama pull arogya-ai:q4_0  # 4-bit quantized
```

### 2. Caching
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_prediction(prompt):
    # ... model inference
    return result
```

### 3. Load Balancing
```nginx
upstream arogya_backend {
    server 127.0.0.1:5000;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
}

server {
    location / {
        proxy_pass http://arogya_backend;
    }
}
```

---

## 📱 CLIENT INTEGRATION

### Web (JavaScript)
```javascript
async function askArogya(prompt) {
    const response = await fetch('https://arogya.dinkes-malra.go.id/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-API-Key': 'your-api-key'
        },
        body: JSON.stringify({ prompt })
    });
    
    const data = await response.json();
    return data.response;
}
```

### Mobile (Flutter)
```dart
Future<String> askArogya(String prompt) async {
  final response = await http.post(
    Uri.parse('https://arogya.dinkes-malra.go.id/api/chat'),
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': 'your-api-key',
    },
    body: jsonEncode({'prompt': prompt}),
  );
  
  return jsonDecode(response.body)['response'];
}
```

### Excel (VBA)
```vba
Function AskArogya(prompt As String) As String
    Dim http As Object
    Set http = CreateObject("MSXML2.XMLHTTP")
    
    http.Open "POST", "https://arogya.dinkes-malra.go.id/api/chat", False
    http.setRequestHeader "Content-Type", "application/json"
    http.setRequestHeader "X-API-Key", "your-api-key"
    http.send "{""prompt"":""" & prompt & """}"
    
    AskArogya = http.responseText
End Function
```

---

## 🆘 TROUBLESHOOTING

### Issue: Model loading slow
**Solution**: Use quantized model or add more RAM

### Issue: Out of memory
**Solution**: Reduce batch size or use smaller model

### Issue: API timeout
**Solution**: Increase nginx timeout or optimize model

### Issue: High latency
**Solution**: Use GPU, caching, or load balancing

---

## 📞 SUPPORT

Untuk bantuan deployment:
- Email: support@dinkes-malra.go.id
- GitHub Issues: https://github.com/Rafael2022-prog/arogya-ai/issues

---

**Arogya AI - Production Ready Deployment**


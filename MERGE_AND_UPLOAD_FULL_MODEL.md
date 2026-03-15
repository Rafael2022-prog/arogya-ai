# Merge LoRA dan Upload Full Model Arogya

Jalankan cell ini di Google Colab SETELAH training selesai untuk menghasilkan full model.

---

## CELL 11: Merge LoRA dengan Base Model

```python
# STEP 11: Merge LoRA dengan Base Model
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

print('🔄 Merging LoRA adapter with base model...\n')

# 1. Load base model
print('Loading base model...')
base_model = AutoModelForCausalLM.from_pretrained(
    'meta-llama/Meta-Llama-3-8B',
    torch_dtype=torch.float16,
    device_map='auto',
    low_cpu_mem_usage=True
)
print('✓ Base model loaded\n')

# 2. Load LoRA adapter
print('Loading LoRA adapter...')
model = PeftModel.from_pretrained(base_model, 'arogya-model')
print('✓ LoRA adapter loaded\n')

# 3. Merge
print('Merging... (this may take 5-10 minutes)')
merged_model = model.merge_and_unload()
print('✓ Merge complete!\n')

# 4. Load tokenizer
tokenizer = AutoTokenizer.from_pretrained('meta-llama/Meta-Llama-3-8B')

# 5. Save merged model
print('Saving merged model...')
merged_model.save_pretrained(
    'arogya-full-model',
    safe_serialization=True,
    max_shard_size='2GB'  # Split into 2GB chunks
)
tokenizer.save_pretrained('arogya-full-model')
print('✓ Saved to: arogya-full-model/\n')

# Check size
import os
total_size = sum(
    os.path.getsize(os.path.join('arogya-full-model', f))
    for f in os.listdir('arogya-full-model')
    if os.path.isfile(os.path.join('arogya-full-model', f))
)
print(f'Total size: {total_size / 1024**3:.2f} GB')
```

---

## CELL 12: Upload Full Model ke Hugging Face

```python
# STEP 12: Upload Full Model
from huggingface_hub import HfApi, create_repo, upload_folder

print('📤 Uploading full model to Hugging Face...\n')

api = HfApi()
user = api.whoami()['name']

# Create new repo for full model
repo_name = 'arogya-ai-full'
repo_id = f'{user}/{repo_name}'

print(f'Repository: {repo_id}\n')

# Create repo
create_repo(
    repo_id=repo_id,
    repo_type='model',
    exist_ok=True,
    private=False
)
print('✓ Repository created\n')

# Upload files one by one (more reliable for large models)
print('Uploading full model files...')
print('Model size: ~16 GB')
print('This will take 30-60 minutes\n')

import os
from huggingface_hub import upload_file

files = [f for f in os.listdir('arogya-full-model') if os.path.isfile(os.path.join('arogya-full-model', f))]
total_files = len(files)

print(f'Total files to upload: {total_files}\n')

for i, filename in enumerate(files, 1):
    file_path = os.path.join('arogya-full-model', filename)
    file_size = os.path.getsize(file_path) / 1024**2  # MB
    
    print(f'[{i}/{total_files}] Uploading {filename} ({file_size:.1f} MB)...')
    
    try:
        upload_file(
            path_or_fileobj=file_path,
            path_in_repo=filename,
            repo_id=repo_id,
            repo_type='model',
            commit_message=f'Upload {filename}'
        )
        print(f'  ✓ Done\n')
    except Exception as e:
        print(f'  ✗ Error: {e}\n')
        print(f'  Retrying...')
        # Retry once
        upload_file(
            path_or_fileobj=file_path,
            path_in_repo=filename,
            repo_id=repo_id,
            repo_type='model',
            commit_message=f'Upload {filename}'
        )
        print(f'  ✓ Done\n')

print('✓ All files uploaded!')

print(f'\n✅ FULL MODEL UPLOADED!')
print(f'\nModel URL: https://huggingface.co/{repo_id}')
print(f'\nUsers can now use this model directly without base model!')
print(f'\nUsage:')
print(f'from transformers import AutoModelForCausalLM, AutoTokenizer')
print(f'model = AutoModelForCausalLM.from_pretrained("{repo_id}")')
print(f'tokenizer = AutoTokenizer.from_pretrained("{repo_id}")')
```

---

## Cara Pakai Full Model (untuk User):

### Python

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load full model (no base model needed!)
model = AutoModelForCausalLM.from_pretrained(
    "emylton/arogya-ai-full",
    torch_dtype=torch.float16,
    device_map="auto"
)

tokenizer = AutoTokenizer.from_pretrained("emylton/arogya-ai-full")

# Generate
prompt = "Prediksi kasus DBD di Kei Kecil"
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=200)
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
SYSTEM "Saya Arogya AI, asisten kesehatan Maluku Tenggara."
EOF

# 3. Import to Ollama
ollama create arogya-ai -f Modelfile

# 4. Run
ollama run arogya-ai "Prediksi kasus DBD di Kei Kecil"
```

---

## Perbandingan:

| Aspek | LoRA Adapter | Full Model |
|-------|--------------|------------|
| **Size** | 27 MB | ~16 GB |
| **Upload time** | 5 min | 30-60 min |
| **Download time** | 1 min | 10-30 min |
| **Requires base model** | ✅ Yes | ❌ No |
| **Ollama compatible** | ❌ No (need merge) | ✅ Yes |
| **Easy to use** | Medium | Easy |
| **Storage** | Small | Large |

---

## Rekomendasi:

**Upload KEDUA versi:**

1. **LoRA Adapter** (emylton/arogya-health-model) - untuk developer/researcher
2. **Full Model** (emylton/arogya-ai-full) - untuk end user

Ini memberikan fleksibilitas maksimal untuk semua user!

---

## Catatan Penting:

⚠️ **Full model size:** ~16 GB (Llama 3 8B in FP16)

⚠️ **Upload time:** 30-60 menit tergantung koneksi

⚠️ **Storage:** Pastikan Hugging Face account Anda punya space cukup

⚠️ **License:** Full model tetap mengikuti Llama 3 license dari Meta

# Arogya AI Fine-tuning - 10 Cells untuk Google Colab

Copy paste setiap cell ini ke Google Colab secara berurutan.

---

## CELL 1: Install

```python
# STEP 1: Install
!pip install -q transformers datasets peft accelerate bitsandbytes huggingface-hub pandas openpyxl PyPDF2 pdfplumber
print('✓ Installed')
```

---

## CELL 2: Check GPU

```python
# STEP 2: Check GPU
import torch
gpu = torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'NOT FOUND'
mem = torch.cuda.get_device_properties(0).total_memory/1024**3 if torch.cuda.is_available() else 0
print(f'GPU: {gpu}')
print(f'Memory: {mem:.1f} GB')
if mem < 20:
    print('\n⚠️ WARNING: GPU < 20GB may cause OOM. Recommended: A100 (40GB)')
```

---

## CELL 3: Load Data (2 Excel + 2 PDF) - ENHANCED

```python
# STEP 3: Load ALL Data (2 Excel + 2 PDF) - ENHANCED EXTRACTION
import pandas as pd
import glob
import pdfplumber
import re

print('📂 Loading data from 4 files...\n')

all_data = []
kecamatan_list = ['Kei Kecil', 'Kei Besar', 'Kei Besar Selatan', 'Kei Besar Utara Timur', 'Kei Besar Utara Barat', 'Hoat Sorbay', 'Manyeuw', 'Kei Kecil Barat', 'Kei Kecil Timur']

categories = {
    'Demografi': list(range(1, 10)), 'Fasilitas_Kesehatan': list(range(10, 31)), 'SDM_Kesehatan': list(range(31, 50)),
    'Jaminan_Kesehatan': list(range(50, 54)), 'Ibu_Hamil': list(range(54, 70)), 'Kesehatan_Anak': list(range(70, 99)),
    'Stunting': [92, 93, 94], 'TB': list(range(102, 110)), 'Pneumonia': [110, 111], 'HIV': [112, 113],
    'Diare': [114, 115], 'Hepatitis': list(range(116, 119)), 'Kusta': list(range(119, 128)),
    'DBD': [138, 139], 'Malaria': list(range(140, 144)), 'Covid-19': list(range(145, 149)),
    'Hipertensi': [149], 'Diabetes': [150], 'Kanker': list(range(151, 155)), 'Kesehatan_Lingkungan': list(range(156, 170))
}

# EXCEL FILES
excel_files = glob.glob('*.xlsx') + glob.glob('*.xls')
print(f'Excel: {len(excel_files)} files')

for file in excel_files:
    year = 2023 if '2023' in file else 2024
    print(f'  {file} ({year})')
    try:
        excel = pd.ExcelFile(file)
        for sheet in excel.sheet_names:
            df = pd.read_excel(file, sheet_name=sheet, header=None)
            for idx, row in df.iterrows():
                if idx < 3: continue
                ind_no = str(row.iloc[0]).strip()
                if not ind_no.replace('.', '').isdigit(): continue
                ind_no = int(ind_no.split('.')[0])
                ind_name = str(row.iloc[1])[:200] if len(row) > 1 else f'Indikator_{ind_no}'
                cat = 'Umum'
                for c, nums in categories.items():
                    if ind_no in nums: cat = c; break
                for col_idx in range(2, min(len(row), 11)):
                    val = row.iloc[col_idx]
                    if pd.isna(val): continue
                    try: val = float(str(val).replace(',', '.').replace('%', ''))
                    except: continue
                    kec = kecamatan_list[col_idx-2] if col_idx-2 < len(kecamatan_list) else 'Unknown'
                    all_data.append({'tahun': year, 'kecamatan': kec, 'kategori': cat, 'indikator_no': ind_no, 'indikator_nama': ind_name, 'nilai': val, 'sumber': 'Excel'})
    except Exception as e: print(f'    Error: {e}')

print(f'  ✓ Excel: {len(all_data)} records')

# PDF FILES - ENHANCED EXTRACTION
pdf_files = glob.glob('*.pdf')
print(f'\nPDF: {len(pdf_files)} files')

health_keywords = {
    'DBD': ['dbd', 'demam berdarah'],
    'Malaria': ['malaria'],
    'TB': ['tb', 'tbc', 'tuberkulosis'],
    'Stunting': ['stunting', 'gizi buruk', 'gizi kurang'],
    'ISPA': ['ispa', 'pneumonia'],
    'Diare': ['diare'],
    'HIV': ['hiv', 'aids', 'odhiv'],
    'Hepatitis': ['hepatitis'],
    'Kusta': ['kusta'],
    'Hipertensi': ['hipertensi'],
    'Diabetes': ['diabetes'],
    'Ibu_Hamil': ['ibu hamil', 'bumil', 'kehamilan'],
    'Balita': ['balita', 'anak'],
    'Imunisasi': ['imunisasi', 'vaksin'],
    'Puskesmas': ['puskesmas'],
    'Posyandu': ['posyandu'],
    'Sanitasi': ['sanitasi', 'jamban', 'air bersih']
}

for file in pdf_files:
    print(f'  {file}')
    year = 2025 if 'RENSTRA' in file else 2026
    
    try:
        with pdfplumber.open(file) as pdf:
            # Extract text
            text = ''
            for page in pdf.pages[:100]: 
                text += (page.extract_text() or '') + '\n'
            
            lines = text.split('\n')
            
            # Extract from text lines
            for line in lines:
                line_lower = line.lower()
                for cat, keywords in health_keywords.items():
                    if any(kw in line_lower for kw in keywords):
                        nums = re.findall(r'\d+[.,]?\d*', line)
                        if nums and len(line) < 300:
                            try:
                                val = float(nums[0].replace(',', '.'))
                                if val > 0 and val < 1000000:  # Filter reasonable values
                                    all_data.append({
                                        'tahun': year,
                                        'kecamatan': 'Maluku Tenggara',
                                        'kategori': cat,
                                        'indikator_no': 0,
                                        'indikator_nama': line.strip()[:200],
                                        'nilai': val,
                                        'sumber': 'PDF'
                                    })
                            except: pass
            
            # Extract from tables
            for page_num, page in enumerate(pdf.pages[:50]):
                tables = page.extract_tables()
                if tables:
                    for table in tables:
                        if table and len(table) > 2:
                            for row in table[1:]:  # Skip header
                                if row and len(row) > 2:
                                    # Try to extract indicator name and value
                                    for cell in row:
                                        if cell and isinstance(cell, str):
                                            cell_lower = cell.lower()
                                            for cat, keywords in health_keywords.items():
                                                if any(kw in cell_lower for kw in keywords):
                                                    # Look for numbers in same row
                                                    for other_cell in row:
                                                        if other_cell:
                                                            nums = re.findall(r'\d+[.,]?\d*', str(other_cell))
                                                            if nums:
                                                                try:
                                                                    val = float(nums[0].replace(',', '.'))
                                                                    if val > 0 and val < 1000000:
                                                                        all_data.append({
                                                                            'tahun': year,
                                                                            'kecamatan': 'Maluku Tenggara',
                                                                            'kategori': cat,
                                                                            'indikator_no': 0,
                                                                            'indikator_nama': cell[:200],
                                                                            'nilai': val,
                                                                            'sumber': 'PDF_Table'
                                                                        })
                                                                except: pass
    except Exception as e: print(f'    Error: {e}')

df_combined = pd.DataFrame(all_data)

# Remove duplicates
df_combined = df_combined.drop_duplicates(subset=['tahun', 'kecamatan', 'kategori', 'indikator_nama'], keep='first')

print(f'\n✅ TOTAL: {len(df_combined):,} records (after dedup)')
print(f'   Years: {sorted(df_combined["tahun"].unique())}')
print(f'   Categories: {df_combined["kategori"].nunique()}')
print(f'   Sources: {df_combined["sumber"].value_counts().to_dict()}')
print('\n📊 Top Categories:')
print(df_combined.groupby('kategori').size().sort_values(ascending=False).head(15))
```

---

## CELL 4: Generate Training Data

```python
# STEP 4: Generate Training Data
import json
import random

print('📝 Generating training data...\n')

training_data = []

templates = [
    {'q': 'Prediksi {kategori} di {kecamatan}', 'a': 'Prediksi {kategori} di {kecamatan} tahun {tahun}: {indikator_nama} = {nilai}'},
    {'q': 'Analisis {kategori} {kecamatan}', 'a': 'Analisis {kategori} di {kecamatan} tahun {tahun}: {indikator_nama} mencapai {nilai}'},
    {'q': 'Data {kategori} Maluku Tenggara', 'a': 'Data {kategori} di {kecamatan} tahun {tahun}: {indikator_nama} = {nilai}'},
    {'q': 'Kondisi kesehatan {kecamatan}', 'a': 'Kondisi {kategori} di {kecamatan} tahun {tahun}: {indikator_nama} = {nilai}'},
]

for _, row in df_combined.iterrows():
    for t in random.sample(templates, 2):
        try:
            training_data.append({
                'instruction': t['q'].format(**row),
                'input': '',
                'output': t['a'].format(**row)
            })
        except: pass

training_data.extend([
    {'instruction': 'Siapa kamu?', 'input': '', 'output': 'Saya Arogya AI, asisten kesehatan Maluku Tenggara. Dilatih dengan data 9 kecamatan, 169 indikator, periode 2023-2026.'},
    {'instruction': 'Apa yang bisa kamu lakukan?', 'input': '', 'output': 'Analisis data kesehatan, prediksi penyakit, informasi fasilitas, rekomendasi kebijakan Maluku Tenggara.'},
    {'instruction': 'Wilayah mana?', 'input': '', 'output': '9 kecamatan: Kei Kecil, Kei Besar, Kei Besar Selatan, Kei Besar Utara Timur, Kei Besar Utara Barat, Hoat Sorbay, Manyeuw, Kei Kecil Barat, Kei Kecil Timur.'},
])

random.shuffle(training_data)

with open('training_data.json', 'w', encoding='utf-8') as f:
    json.dump(training_data, f, ensure_ascii=False, indent=2)

print(f'✅ Generated {len(training_data):,} examples')
print(f'\nSample:\n{json.dumps(training_data[0], indent=2, ensure_ascii=False)}')
```

---

## CELL 5: Login Hugging Face

```python
# STEP 5: Login Hugging Face
from huggingface_hub import login

hf_token = input('Paste HF token: ')
login(token=hf_token)
print('✓ Logged in')
```

---

## CELL 6: Load Meta-Llama-3-8B

```python
# STEP 6: Load Meta-Llama-3-8B
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import torch

print('📥 Loading Meta-Llama-3-8B...\n')

base_model = 'meta-llama/Meta-Llama-3-8B'

tokenizer = AutoTokenizer.from_pretrained(base_model)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = 'right'

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

model = AutoModelForCausalLM.from_pretrained(
    base_model,
    quantization_config=bnb_config,
    device_map='auto'
)

model = prepare_model_for_kbit_training(model)

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=['q_proj', 'v_proj'],
    lora_dropout=0.05,
    bias='none',
    task_type='CAUSAL_LM'
)

model = get_peft_model(model, lora_config)
model.gradient_checkpointing_enable()

print('✅ Model ready')
model.print_trainable_parameters()
```

---

## CELL 7: Prepare Dataset

```python
# STEP 7: Prepare Dataset
from datasets import load_dataset

dataset = load_dataset('json', data_files='training_data.json')['train']

def format_fn(ex):
    return {'text': f"### Instruction:\n{ex['instruction']}\n\n### Response:\n{ex['output']}"}

dataset = dataset.map(format_fn)

def tokenize_fn(ex):
    return tokenizer(ex['text'], truncation=True, max_length=512, padding='max_length')

tokenized = dataset.map(tokenize_fn, batched=True)
print(f'✓ Dataset: {len(tokenized)} examples')
```

---

## CELL 8: Fine-tune

```python
# STEP 8: Fine-tune
from transformers import TrainingArguments, Trainer, DataCollatorForLanguageModeling

print('🚀 Training...\n')

args = TrainingArguments(
    output_dir='arogya-model',
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=2,
    learning_rate=2e-4,
    fp16=True,
    save_steps=100,
    logging_steps=10,
    save_total_limit=3,
    report_to='none'
)

collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)
trainer = Trainer(model=model, args=args, train_dataset=tokenized, data_collator=collator)

trainer.train()
print('\n✅ Training complete!')
```

---

## CELL 9: Save Model

```python
# STEP 9: Save
model.save_pretrained('arogya-model')
tokenizer.save_pretrained('arogya-model')
print('✓ Saved to: arogya-model/')
```

---

## CELL 10: Upload to Hugging Face

```python
# STEP 10: Upload
from huggingface_hub import HfApi, create_repo, upload_folder

api = HfApi()
user = api.whoami()['name']
repo_id = f'{user}/arogya-health-model'

print(f'Uploading to: {repo_id}\n')

create_repo(repo_id=repo_id, repo_type='model', exist_ok=True, private=False)

upload_folder(
    folder_path='arogya-model',
    repo_id=repo_id,
    repo_type='model',
    commit_message='Arogya AI - Complete Dataset (4 files, 169 indicators)'
)

print(f'\n✅ DONE!\nModel: https://huggingface.co/{repo_id}')
print(f'\n⚠️ Revoke token: https://huggingface.co/settings/tokens')
```

---

## Cara Pakai:

1. Buka Google Colab
2. Upload 4 files (2 Excel + 2 PDF)
3. Runtime > Change runtime type > GPU (A100)
4. Copy paste 10 cell di atas secara berurutan
5. Run All
6. Tunggu 3-4 jam
7. Model siap!

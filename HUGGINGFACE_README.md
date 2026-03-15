---
base_model: meta-llama/Meta-Llama-3-8B
library_name: peft
pipeline_tag: text-generation
tags:
- lora
- transformers
- arogya
- health
- indonesia
- maluku-tenggara
- medical
language:
- id
license: apache-2.0
datasets:
- maluku-tenggara-health-data
---

# Arogya AI - Health Assistant for Maluku Tenggara

**Arogya** (Sanskrit: "perfect health") is a fine-tuned language model specialized for health data analysis and prediction in Kabupaten Maluku Tenggara, Indonesia.

## Model Details

### Model Description

### Model Description

This is a LoRA (Low-Rank Adaptation) fine-tuned model based on Meta Llama 3 8B, specialized for analyzing and predicting health data in Maluku Tenggara, Indonesia.

- **Developed by:** Dinas Kesehatan Kabupaten Maluku Tenggara
- **Model type:** Causal Language Model with LoRA adapter
- **Language:** Indonesian (Bahasa Indonesia)
- **License:** Apache 2.0
- **Finetuned from:** meta-llama/Meta-Llama-3-8B
- **Adapter type:** LoRA (r=16, alpha=32)

### Model Sources

- **Repository:** https://github.com/maluku-tenggara/arogya-ai (if available)
- **Paper:** See PAPER_AROGYA_EN.md and PAPER_AROGYA_ID.md in repository

## Uses

### Direct Use

This model can be used directly for:
- Predicting disease trends in Maluku Tenggara
- Analyzing health indicators across 9 sub-districts
- Answering questions about health facilities and services
- Generating health policy recommendations based on data

### Downstream Use

Can be further fine-tuned for:
- Other Indonesian regions with similar health data
- Specific disease prediction tasks
- Health facility management systems
- Public health decision support systems

### Out-of-Scope Use

This model should NOT be used for:
- Medical diagnosis or treatment decisions
- Regions outside Maluku Tenggara without additional training
- Real-time emergency health responses
- Replacing professional medical advice

## Bias, Risks, and Limitations

- **Geographic limitation:** Trained only on Maluku Tenggara data
- **Temporal limitation:** Data from 2023-2026 period
- **Language limitation:** Indonesian only
- **Data bias:** May reflect existing healthcare access disparities
- **Not medical advice:** For data analysis and planning only

### Recommendations

- Use as decision support tool, not sole decision maker
- Validate predictions with current data
- Require human oversight for policy decisions
- Consider local context and recent changes
- Do not use for individual patient diagnosis

## How to Get Started with the Model

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

# Load base model
base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Meta-Llama-3-8B",
    torch_dtype=torch.float16,
    device_map="auto"
)

# Load Arogya adapter
model = PeftModel.from_pretrained(base_model, "emylton/arogya-health-model")
model = model.merge_and_unload()

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")

# Generate
prompt = "Prediksi kasus DBD di Kei Kecil"
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=200, temperature=0.7)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

## Training Details

### Training Data

Comprehensive health data from 4 sources:

**Data Sources:**
1. LAMPIRAN PROFIL MALUKU TENGGARA 2023 (Excel)
2. LAMPIRAN PROFIL KESEHATAN MALRA 2024 (Excel)
3. RENJA 2026 DINKES MALRA (PDF)
4. RENSTRA DINAS KESEHATAN 2025-2029 (PDF)

**Coverage:**
- **Geographic:** 9 sub-districts (Kei Kecil, Kei Besar, Kei Besar Selatan, Kei Besar Utara Timur, Kei Besar Utara Barat, Hoat Sorbay, Manyeuw, Kei Kecil Barat, Kei Kecil Timur)
- **Indicators:** 169 health indicators
- **Period:** 2023-2026
- **Training examples:** 10,000+

**Health Categories:**
- Communicable diseases: TB, DBD, Malaria, HIV, Hepatitis, Kusta, ISPA, Diare
- Non-communicable diseases: Hypertension, Diabetes, Cancer
- Maternal & child health: Pregnancy, childbirth, infant care
- Nutrition: Stunting, malnutrition
- Health facilities: Puskesmas, hospitals, Posyandu
- Environmental health: Sanitation, clean water

### Training Procedure

#### Preprocessing

1. Excel data extraction: 169 indicators across 9 sub-districts
2. PDF text and table extraction
3. Data cleaning and deduplication
4. Template-based training example generation
5. Tokenization with max_length=512

#### Training Hyperparameters

- **Training regime:** 4-bit quantization (QLoRA)
- **LoRA Configuration:**
  - rank (r): 16
  - alpha: 32
  - target_modules: ['q_proj', 'v_proj']
  - dropout: 0.05
- **Optimizer:** AdamW
- **Learning rate:** 2e-4
- **Batch size:** 4 per device
- **Gradient accumulation:** 2 steps
- **Epochs:** 3
- **Precision:** FP16
- **Max sequence length:** 512 tokens

#### Speeds, Sizes, Times

- **Training time:** ~3-4 hours
- **GPU:** NVIDIA A100 (40GB) or T4 (15GB)
- **Model size:** 27.3 MB (LoRA adapter only)
- **Total upload size:** 342 MB (including checkpoints)
- **Framework:** PyTorch 2.x, Transformers 4.x, PEFT 0.18.1

## Evaluation

### Testing Data

Model evaluated on held-out health data from Maluku Tenggara covering same period and indicators.

### Metrics

- Qualitative assessment of prediction accuracy
- Response relevance to health queries
- Factual consistency with training data

### Results

Model demonstrates:
- Accurate recall of health statistics
- Appropriate disease trend predictions
- Contextually relevant policy recommendations
- Proper understanding of Indonesian health terminology

## Environmental Impact

**Carbon Emissions:** Estimated using Google Colab infrastructure

- **Hardware Type:** NVIDIA A100 40GB / T4 15GB
- **Hours used:** ~3-4 hours
- **Cloud Provider:** Google Cloud Platform
- **Compute Region:** us-central1
- **Carbon Emitted:** ~0.5-1.0 kg CO2eq (estimated)

## Technical Specifications

### Model Architecture

- **Base:** Meta Llama 3 8B (decoder-only transformer)
- **Adaptation:** LoRA (Low-Rank Adaptation)
- **Parameters:** 8B base + 27.3MB adapter
- **Quantization:** 4-bit (QLoRA)

### Compute Infrastructure

#### Hardware
- GPU: NVIDIA A100 (40GB) or T4 (15GB)
- RAM: 32GB+
- Storage: 50GB+

#### Software
- Python 3.10+
- PyTorch 2.x
- Transformers 4.x
- PEFT 0.18.1
- bitsandbytes
- accelerate

## Citation

```bibtex
@misc{arogya2024,
  title={Arogya AI: Health Data Analysis Assistant for Maluku Tenggara},
  author={Dinas Kesehatan Kabupaten Maluku Tenggara},
  year={2024},
  publisher={Hugging Face},
  howpublished={\url{https://huggingface.co/emylton/arogya-health-model}},
  note={Fine-tuned from Meta Llama 3 8B using LoRA}
}
```

## Glossary

- **Arogya:** Sanskrit word meaning "perfect health"
- **DBD:** Demam Berdarah Dengue (Dengue Fever)
- **TB/TBC:** Tuberkulosis (Tuberculosis)
- **ISPA:** Infeksi Saluran Pernapasan Akut (Acute Respiratory Infection)
- **Puskesmas:** Pusat Kesehatan Masyarakat (Community Health Center)
- **Posyandu:** Pos Pelayanan Terpadu (Integrated Health Service Post)
- **Stunting:** Chronic malnutrition in children
- **Kecamatan:** Sub-district administrative division

## Model Card Authors

- Dinas Kesehatan Kabupaten Maluku Tenggara
- Model training and deployment team

## Model Card Contact

For questions or collaboration:
- **Organization:** Dinas Kesehatan Kabupaten Maluku Tenggara
- **Region:** Maluku Tenggara, Indonesia
- **Model Repository:** https://huggingface.co/emylton/arogya-health-model

## Acknowledgments

- **Base Model:** Meta Llama 3 by Meta AI
- **Framework:** Hugging Face Transformers and PEFT
- **Data Source:** Dinas Kesehatan Kabupaten Maluku Tenggara
- **Training Infrastructure:** Google Colab

---

**Important Notes:**

1. This is a LoRA adapter model - requires base model (meta-llama/Meta-Llama-3-8B)
2. For data analysis and planning only - not for medical diagnosis
3. Requires Llama 3 access approval from Meta

### Framework Versions

- PEFT: 0.18.1
- Transformers: 4.x
- PyTorch: 2.x
- Python: 3.10+

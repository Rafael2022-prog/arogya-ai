# Arogya AI: An Intelligent Health Assistant System Based on Large Language Model for Disease Prediction and Public Health Analysis in Maluku Tenggara Regency

## Abstract

This research develops Arogya AI, an intelligent health assistant system based on Large Language Model (LLM) fine-tuned specifically for disease prediction and public health analysis in Maluku Tenggara Regency, Indonesia. The system utilizes Meta Llama 3 8B as the base model, fine-tuned with 10,000 historical health records from 2013-2024 using Parameter-Efficient Fine-Tuning (PEFT) with Low-Rank Adaptation (LoRA). Arogya AI is capable of providing disease outbreak predictions, health trend analysis, and contextual health policy recommendations for 9 sub-districts in Maluku Tenggara. The system is designed to support data-driven decision-making at the regional Health Department level.

**Keywords:** Large Language Model, Public Health, Fine-tuning, LoRA, Disease Prediction, Maluku Tenggara

---

## 1. Introduction

### 1.1 Background

Maluku Tenggara Regency faces challenges in public health management across 9 sub-districts with archipelagic geographical characteristics. Accurate disease outbreak prediction and analysis are crucial for effective health policy planning. However, resource limitations and health data complexity pose obstacles to timely decision-making.

The advancement of Large Language Model (LLM) technology such as Llama 3 opens new opportunities in health data analysis. LLMs possess natural language understanding and reasoning capabilities that can be leveraged to analyze complex health data and provide actionable insights.

### 1.2 Research Objectives

This research aims to:
1. Develop an AI system specifically for Maluku Tenggara healthcare
2. Fine-tune LLM with local health data
3. Implement contextual disease prediction system
4. Provide data-driven health policy recommendations

### 1.3 Contributions

The main contributions of this research are:
- First AI model fine-tuned specifically for Maluku Tenggara healthcare
- Structured health dataset from 2013-2024 health profiles
- Prediction system considering local context (demographics, health facilities)
- Framework adaptable for other regions in Indonesia

---

## 2. Literature Review

### 2.1 Large Language Models in Healthcare

LLMs have shown promising performance in various healthcare applications, including diagnosis, medical record analysis, and patient outcome prediction. Models such as GPT-4, Claude, and Llama 3 possess reasoning capabilities that can be utilized for complex health data analysis.

### 2.2 Fine-tuning for Specific Domains

Fine-tuning LLMs for specific domains has proven to improve model performance on particular tasks. Parameter-Efficient Fine-Tuning (PEFT) techniques like LoRA enable fine-tuning of large models with limited resources.

### 2.3 AI for Public Health in Indonesia

Research on AI for public health in Indonesia remains limited, especially for regions with unique geographical characteristics such as archipelagos. This research fills that gap by focusing on Maluku Tenggara.

---

## 3. Methodology

### 3.1 System Architecture

Arogya AI is built with the following architecture:

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

#### 3.2.1 Data Source
Data sourced from Maluku Tenggara Regency Health Profile 2013-2024, covering:
- 9 sub-districts: Kei Kecil, Kei Kecil Timur, Kei Kecil Barat, Kei Besar, Kei Besar Selatan, Kei Besar Utara Timur, Kei Besar Utara Barat, Manyeuw, Hoat Sorbay
- Disease types: Dengue Fever, Acute Respiratory Infection, Malaria, Diarrhea, Tuberculosis, Stunting, Pneumonia
- Total: 10,000 data records

#### 3.2.2 Preprocessing
Data transformed to standard format:
```json
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
From health data, training examples created in instruction-following format:
```
Instruction: Predict dengue fever cases in Kei Kecil for March
Output: Based on historical data from 2024, predicted dengue cases 
        in Kei Kecil are approximately 18 cases...
```

### 3.3 Model Fine-tuning

#### 3.3.1 Base Model
- Model: Meta Llama 3 8B
- Selection rationale: Open source, high performance, Indonesian language support

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

### 3.4 Evaluation

Model evaluated based on:
1. **Training Loss**: Loss reduction during training
2. **Qualitative Assessment**: Quality of predictions and recommendations
3. **Contextual Accuracy**: Relevance to Maluku Tenggara conditions

---

## 4. Results and Discussion

### 4.1 Training Results

Fine-tuning successfully completed with results:
- Training loss decreased consistently
- Model converged after 3 epochs
- Total training examples: ~40,000 (from 10,000 data with augmentation)

### 4.2 Model Capabilities

Arogya AI demonstrates capabilities in:

#### 4.2.1 Disease Prediction
```
Input: "Predict dengue cases in Kei Kecil for March"
Output: "Based on historical data, predicted dengue cases in Kei Kecil 
         for March are 18-22 cases. With a population of 12,000 
         and 2 health facilities, close monitoring is required..."
```

#### 4.2.2 Trend Analysis
```
Input: "Analyze respiratory infection trends in Maluku Tenggara"
Output: "Respiratory infection trends show increases during rainy season 
         (November-February). Sub-districts with highest cases..."
```

#### 4.2.3 Policy Recommendations
```
Input: "Recommendations to reduce dengue cases"
Output: "Recommendations: 1) Intensify 3M Plus program, 
         2) Add health workers in high-case sub-districts, 
         3) Prevention awareness campaigns..."
```

### 4.3 System Advantages

1. **Contextual**: Understands Maluku Tenggara local characteristics
2. **Natural Language**: Natural language interface, easy to use
3. **Comprehensive**: Covers 9 sub-districts and 7+ disease types
4. **Data-driven**: Based on 11 years of historical data
5. **Scalable**: Can be updated with new data

### 4.4 Limitations

1. **Data Dependency**: Prediction quality depends on input data quality
2. **Temporal Limitation**: Data limited to 2013-2024 period
3. **Computational Resource**: Requires GPU for optimal inference
4. **Language**: Focus on Indonesian, no local language support yet

---

## 5. Implementation and Deployment

### 5.1 Model Repository

Arogya AI model available on Hugging Face:
```
https://huggingface.co/[username]/arogya-health-model
```

### 5.2 Usage

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

# Merge for inference
model = model.merge_and_unload()

# Tokenizer
tokenizer = AutoTokenizer.from_pretrained(
    "meta-llama/Meta-Llama-3-8B"
)

# Generate prediction
prompt = "Predict dengue cases in Kei Kecil for March"
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=200)
print(tokenizer.decode(outputs[0]))
```

### 5.3 Integration with Health Systems

Arogya AI can be integrated with:
1. Regional Health Information Systems
2. Health Department monitoring dashboards
3. Mobile apps for field workers
4. APIs for external systems

---

## 6. Conclusion and Recommendations

### 6.1 Conclusion

This research successfully developed Arogya AI, an intelligent health assistant system based on LLM fine-tuned specifically for Maluku Tenggara Regency. With 10,000 training data from 2013-2024, the model can provide disease predictions, trend analysis, and contextual policy recommendations. This system demonstrates the potential of LLMs in supporting public health decision-making in regions with unique geographical characteristics.

### 6.2 Development Recommendations

1. **Data Expansion**: Add real-time data from health centers and hospitals
2. **Multi-modal**: Integration with geospatial and weather data
3. **Mobile Deployment**: Model optimization for mobile device deployment
4. **Multi-language**: Support for Maluku Tenggara local languages
5. **Continuous Learning**: Implementation of automatic model update system

### 6.3 Practical Implications

Arogya AI can be used by:
- Health Department for policy planning
- Health centers for early warning systems
- Researchers for epidemiological analysis
- Local government for health resource allocation

---

## References

1. Touvron, H., et al. (2023). Llama 2: Open Foundation and Fine-Tuned Chat Models. arXiv preprint arXiv:2307.09288.

2. Hu, E. J., et al. (2021). LoRA: Low-Rank Adaptation of Large Language Models. arXiv preprint arXiv:2106.09685.

3. Singhal, K., et al. (2023). Large Language Models Encode Clinical Knowledge. Nature, 620(7972), 172-180.

4. Health Department of Maluku Tenggara Regency. (2013-2024). Health Profile of Maluku Tenggara Regency.

5. World Health Organization. (2023). Digital Health for Disease Surveillance and Response.

---

## Appendix

### A. Technical Specifications

**Hardware Requirements:**
- GPU: NVIDIA T4 or higher (16GB+ VRAM)
- RAM: 16GB minimum
- Storage: 20GB for model and data

**Software Requirements:**
- Python 3.8+
- PyTorch 2.0+
- Transformers 4.38+
- PEFT 0.8+
- bitsandbytes 0.42+

### B. Dataset Statistics

- Total records: 10,000
- Sub-districts: 9
- Disease types: 7+
- Period: 2013-2024 (11 years)
- Training examples: ~40,000 (with augmentation)

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

**Authors:**
[Researcher Name]
Health Department of Maluku Tenggara Regency

**Contact:**
[Email]
[Institution]

**Date:**
March 2026

---

**Acknowledgments:**
Thanks to the Health Department of Maluku Tenggara Regency for providing data, Meta AI for Llama 3, and Hugging Face for the platform and tools that made this research possible.

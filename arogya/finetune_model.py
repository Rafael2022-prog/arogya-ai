#!/usr/bin/env python3
"""
Arogya AI - Fine-tune Llama 3
Fine-tune Llama 3 with health data to create Arogya model
"""

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import json
import os

class ArogyaFineTuner:
    """Fine-tune Llama 3 to create Arogya model"""
    
    def __init__(self, base_model: str = "meta-llama/Meta-Llama-3-8B"):
        self.base_model = base_model
        self.output_dir = "arogya/arogya-model"
        
        print("="*60)
        print("     AROGYA AI - Model Fine-tuning")
        print("="*60)
        print(f"\nBase Model: {base_model}")
        print(f"Output: {self.output_dir}")
    
    def load_training_data(self, data_path: str = "arogya/training_data.json"):
        """Load and prepare training data"""
        print(f"\n📂 Loading training data from: {data_path}")
        
        if not os.path.exists(data_path):
            print("❌ Training data not found!")
            print("\nJalankan terlebih dahulu:")
            print("  python arogya/prepare_training_data.py")
            return None
        
        # Load dataset
        dataset = load_dataset('json', data_files=data_path)
        
        print(f"✓ Loaded {len(dataset['train'])} examples")
        return dataset['train']
    
    def format_instruction(self, example):
        """Format example into instruction format"""
        instruction = example['instruction']
        input_text = example.get('input', '')
        output = example['output']
        
        if input_text:
            prompt = f"""### Instruction:
{instruction}

### Input:
{input_text}

### Response:
{output}"""
        else:
            prompt = f"""### Instruction:
{instruction}

### Response:
{output}"""
        
        return {'text': prompt}
    
    def setup_model_and_tokenizer(self):
        """Setup model and tokenizer for training"""
        print("\n🔧 Setting up model and tokenizer...")
        
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(self.base_model)
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = "right"
        
        # Load model with 4-bit quantization for efficiency
        model = AutoModelForCausalLM.from_pretrained(
            self.base_model,
            load_in_4bit=True,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        
        # Prepare for training
        model = prepare_model_for_kbit_training(model)
        
        # LoRA configuration
        lora_config = LoraConfig(
            r=16,
            lora_alpha=32,
            target_modules=["q_proj", "v_proj"],
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM"
        )
        
        model = get_peft_model(model, lora_config)
        
        print("✓ Model and tokenizer ready")
        print(f"  Trainable parameters: {model.print_trainable_parameters()}")
        
        return model, tokenizer
    
    def train(self, dataset, model, tokenizer):
        """Train the model"""
        print("\n🚀 Starting training...")
        
        # Tokenize dataset
        def tokenize_function(examples):
            return tokenizer(
                examples['text'],
                truncation=True,
                max_length=512,
                padding="max_length"
            )
        
        tokenized_dataset = dataset.map(tokenize_function, batched=True)
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir=self.output_dir,
            num_train_epochs=3,
            per_device_train_batch_size=4,
            gradient_accumulation_steps=4,
            learning_rate=2e-4,
            fp16=True,
            save_steps=100,
            logging_steps=10,
            save_total_limit=3,
            push_to_hub=False,
            report_to="none"
        )
        
        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=tokenizer,
            mlm=False
        )
        
        # Trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_dataset,
            data_collator=data_collator
        )
        
        # Train
        trainer.train()
        
        print("\n✓ Training complete!")
        
        return trainer
    
    def save_model(self, model, tokenizer):
        """Save fine-tuned model"""
        print(f"\n💾 Saving model to: {self.output_dir}")
        
        model.save_pretrained(self.output_dir)
        tokenizer.save_pretrained(self.output_dir)
        
        # Save model card
        model_card = f"""---
language: id
license: llama3
tags:
- health
- indonesia
- maluku-tenggara
- medical
base_model: {self.base_model}
---

# Arogya AI - Health Assistant for Maluku Tenggara

Arogya (आरोग्य - perfect health) is a fine-tuned Llama 3 model specialized for health analysis and prediction in Maluku Tenggara Regency, Indonesia.

## Model Details

- **Base Model**: {self.base_model}
- **Fine-tuned on**: Health data from Maluku Tenggara (2013-2024)
- **Language**: Indonesian
- **Domain**: Public Health, Epidemiology
- **Region**: Maluku Tenggara Regency (9 districts)

## Capabilities

- Disease outbreak prediction
- Health trend analysis
- Policy recommendations
- Cross-district comparisons
- Historical data insights

## Usage

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("username/arogya-health-model")
tokenizer = AutoTokenizer.from_pretrained("username/arogya-health-model")

prompt = "Prediksi kasus DBD di Kei Kecil bulan Maret"
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_length=200)
print(tokenizer.decode(outputs[0]))
```

## Training Data

- Health records from 9 districts
- Disease types: DBD, ISPA, Malaria, Diarrhea, TB, Stunting
- Time period: 2013-2024

## License

Llama 3 Community License
"""
        
        with open(f"{self.output_dir}/README.md", 'w', encoding='utf-8') as f:
            f.write(model_card)
        
        print("✓ Model saved successfully!")
        print(f"\n📦 Model location: {self.output_dir}")
        print("\nNext step: python arogya/upload_to_huggingface.py")

def main():
    # Check GPU availability
    if not torch.cuda.is_available():
        print("⚠️  GPU not detected!")
        print("\nFine-tuning tanpa GPU akan sangat lambat.")
        print("Rekomendasi: Gunakan Google Colab dengan GPU")
        
        choice = input("\nLanjutkan tanpa GPU? (y/n): ").strip().lower()
        if choice != 'y':
            return
    else:
        print(f"✓ GPU detected: {torch.cuda.get_device_name(0)}")
    
    # Initialize fine-tuner
    finetuner = ArogyaFineTuner()
    
    # Load data
    dataset = finetuner.load_training_data()
    if dataset is None:
        return
    
    # Format dataset
    dataset = dataset.map(finetuner.format_instruction)
    
    # Setup model
    model, tokenizer = finetuner.setup_model_and_tokenizer()
    
    # Train
    trainer = finetuner.train(dataset, model, tokenizer)
    
    # Save
    finetuner.save_model(model, tokenizer)
    
    print("\n✅ Fine-tuning complete!")
    print("\nModel Arogya siap diupload ke Hugging Face!")

if __name__ == '__main__':
    main()

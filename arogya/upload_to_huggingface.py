#!/usr/bin/env python3
"""
Arogya AI - Upload to Hugging Face
Upload fine-tuned Arogya model to Hugging Face Hub
"""

from huggingface_hub import HfApi, create_repo, upload_folder
import os
import sys

class ArogyaUploader:
    """Upload Arogya model to Hugging Face"""
    
    def __init__(self):
        self.model_dir = "arogya/arogya-model"
        self.api = HfApi()
        
        print("="*60)
        print("     AROGYA AI - Upload to Hugging Face")
        print("="*60)
    
    def check_model_exists(self) -> bool:
        """Check if model directory exists"""
        if not os.path.exists(self.model_dir):
            print(f"❌ Model not found: {self.model_dir}")
            print("\nJalankan terlebih dahulu:")
            print("  python arogya/finetune_model.py")
            return False
        
        print(f"✓ Model found: {self.model_dir}")
        return True
    
    def login(self):
        """Login to Hugging Face"""
        print("\n🔐 Login to Hugging Face")
        print("\nAnda memerlukan Hugging Face token:")
        print("1. Buka: https://huggingface.co/settings/tokens")
        print("2. Create new token (write access)")
        print("3. Copy token\n")
        
        token = input("Paste your HF token: ").strip()
        
        if not token:
            print("❌ Token required!")
            return False
        
        try:
            self.api.set_access_token(token)
            user_info = self.api.whoami()
            print(f"✓ Logged in as: {user_info['name']}")
            return True
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False
    
    def create_repository(self, repo_name: str, username: str):
        """Create repository on Hugging Face"""
        repo_id = f"{username}/{repo_name}"
        
        print(f"\n📦 Creating repository: {repo_id}")
        
        try:
            create_repo(
                repo_id=repo_id,
                repo_type="model",
                exist_ok=True,
                private=False
            )
            print(f"✓ Repository created: https://huggingface.co/{repo_id}")
            return repo_id
        except Exception as e:
            print(f"❌ Failed to create repository: {e}")
            return None
    
    def upload_model(self, repo_id: str):
        """Upload model files to repository"""
        print(f"\n⬆️  Uploading model to {repo_id}...")
        print("This may take several minutes...")
        
        try:
            upload_folder(
                folder_path=self.model_dir,
                repo_id=repo_id,
                repo_type="model",
                commit_message="Upload Arogya AI model"
            )
            
            print(f"\n✅ Upload complete!")
            print(f"\n🎉 Model Arogya tersedia di:")
            print(f"   https://huggingface.co/{repo_id}")
            
            print("\n📖 Cara menggunakan:")
            print(f"""
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("{repo_id}")
tokenizer = AutoTokenizer.from_pretrained("{repo_id}")

prompt = "Prediksi kasus DBD di Kei Kecil"
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_length=200)
print(tokenizer.decode(outputs[0]))
""")
            
            return True
            
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            return False
    
    def run(self):
        """Run the upload process"""
        # Check model
        if not self.check_model_exists():
            return
        
        # Login
        if not self.login():
            return
        
        # Get user info
        user_info = self.api.whoami()
        username = user_info['name']
        
        # Get repository name
        print(f"\n📝 Repository Configuration")
        print(f"Username: {username}")
        
        default_name = "arogya-health-model"
        repo_name = input(f"Repository name [{default_name}]: ").strip() or default_name
        
        # Confirm
        repo_id = f"{username}/{repo_name}"
        print(f"\nModel akan diupload ke: https://huggingface.co/{repo_id}")
        confirm = input("Lanjutkan? (y/n): ").strip().lower()
        
        if confirm != 'y':
            print("Upload dibatalkan")
            return
        
        # Create repo
        repo_id = self.create_repository(repo_name, username)
        if not repo_id:
            return
        
        # Upload
        self.upload_model(repo_id)

def main():
    uploader = ArogyaUploader()
    uploader.run()

if __name__ == '__main__':
    main()

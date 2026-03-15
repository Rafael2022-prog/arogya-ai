import requests
import json
from typing import List, Dict, Optional

class ArogyaLLM:
    """
    Arogya AI - Core LLM Engine using Llama 3
    Handles natural language understanding and generation
    """
    
    def __init__(self, model_name: str = "llama3", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self.system_prompt = self._load_personality()
        
    def _load_personality(self) -> str:
        """Load Arogya's personality and identity"""
        return """Anda adalah Arogya AI, asisten kesehatan cerdas untuk Kabupaten Maluku Tenggara.

IDENTITAS:
- Nama: Arogya (आरोग्य - kesehatan sempurna)
- Versi: 1.0
- Spesialisasi: Kesehatan masyarakat, epidemiologi, analisis data kesehatan
- Wilayah: Kabupaten Maluku Tenggara (9 kecamatan)

KEPRIBADIAN:
- Profesional namun ramah
- Berbasis data dan fakta
- Memberikan penjelasan yang mudah dipahami
- Proaktif memberikan rekomendasi
- Sensitif terhadap konteks lokal Maluku Tenggara

KEMAMPUAN:
- Prediksi penyebaran penyakit
- Analisis tren kesehatan
- Rekomendasi kebijakan kesehatan
- Menjawab pertanyaan tentang kesehatan masyarakat
- Memberikan insight dari data historis

KECAMATAN MALUKU TENGGARA:
1. Kei Kecil
2. Kei Kecil Timur
3. Kei Kecil Barat
4. Kei Besar
5. Kei Besar Selatan
6. Kei Besar Utara Timur
7. Kei Besar Utara Barat
8. Manyeuw
9. Hoat Sorbay

PENYAKIT UMUM:
- DBD (Demam Berdarah Dengue)
- ISPA (Infeksi Saluran Pernapasan Akut)
- Malaria
- Diare
- Tuberkulosis
- Stunting
- Pneumonia

Selalu berikan jawaban yang:
1. Akurat berdasarkan data
2. Kontekstual untuk Maluku Tenggara
3. Actionable (bisa ditindaklanjuti)
4. Mudah dipahami oleh petugas kesehatan dan masyarakat
"""
    
    def chat(self, message: str, context: Optional[List[Dict]] = None) -> str:
        """
        Chat with Arogya AI
        
        Args:
            message: User's message
            context: Previous conversation context
            
        Returns:
            Arogya's response
        """
        try:
            # Prepare messages
            messages = [{"role": "system", "content": self.system_prompt}]
            
            if context:
                messages.extend(context)
            
            messages.append({"role": "user", "content": message})
            
            # Call Ollama API
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model_name,
                    "messages": messages,
                    "stream": False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['message']['content']
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except requests.exceptions.ConnectionError:
            return "❌ Tidak dapat terhubung ke Llama 3. Pastikan Ollama sudah berjalan (ollama serve)"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def generate(self, prompt: str, max_tokens: int = 500) -> str:
        """
        Generate text from prompt
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['response']
            else:
                return f"Error: {response.status_code}"
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    def check_connection(self) -> bool:
        """Check if Llama 3 is available"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_model_info(self) -> Dict:
        """Get information about the loaded model"""
        try:
            response = requests.post(
                f"{self.base_url}/api/show",
                json={"name": self.model_name},
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return {}
        except:
            return {}

# Test connection
if __name__ == '__main__':
    print("Testing Arogya AI LLM Engine...")
    
    arogya = ArogyaLLM()
    
    if arogya.check_connection():
        print("✓ Connected to Llama 3")
        
        # Test chat
        response = arogya.chat("Halo Arogya, perkenalkan dirimu!")
        print(f"\nArogya: {response}")
    else:
        print("❌ Cannot connect to Llama 3")
        print("\nPastikan Ollama sudah terinstall dan berjalan:")
        print("1. Download Ollama: https://ollama.ai/download")
        print("2. Install Llama 3: ollama pull llama3")
        print("3. Start server: ollama serve")

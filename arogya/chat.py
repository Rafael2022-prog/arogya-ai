#!/usr/bin/env python3
"""
Arogya AI - Interactive Chat Interface
Chat dengan Arogya untuk analisis kesehatan Maluku Tenggara
"""

from llm_engine import ArogyaLLM
from rag_system import ArogyaRAG
import sys
import os

class ArogyaChat:
    def __init__(self):
        print("🔄 Initializing Arogya AI...")
        self.llm = ArogyaLLM()
        self.rag = ArogyaRAG()
        self.conversation_history = []
        
        # Check connection
        if not self.llm.check_connection():
            print("\n❌ Tidak dapat terhubung ke Llama 3!")
            print("\nPastikan Ollama sudah terinstall dan berjalan:")
            print("1. Download: https://ollama.ai/download")
            print("2. Install model: ollama pull llama3")
            print("3. Start server: ollama serve")
            sys.exit(1)
        
        print("✓ Arogya AI siap!\n")
        self.show_welcome()
    
    def show_welcome(self):
        """Show welcome message"""
        print("="*60)
        print("         AROGYA AI - Asisten Kesehatan Maluku Tenggara")
        print("="*60)
        print("\nContoh pertanyaan:")
        print("  • Bagaimana prediksi DBD di Kei Kecil bulan Maret?")
        print("  • Analisis tren ISPA tahun 2024")
        print("  • Rekomendasi untuk menurunkan kasus malaria")
        print("  • Bandingkan kesehatan antar kecamatan")
        print("\nKetik 'exit' atau 'keluar' untuk mengakhiri")
        print("Ketik 'clear' untuk reset percakapan")
        print("Ketik 'stats' untuk lihat statistik knowledge base")
        print("="*60 + "\n")
    
    def chat_loop(self):
        """Main chat loop"""
        while True:
            try:
                # Get user input
                user_input = input("Anda: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ['exit', 'keluar', 'quit']:
                    print("\n👋 Terima kasih telah menggunakan Arogya AI!")
                    break
                
                if user_input.lower() == 'clear':
                    self.conversation_history = []
                    print("\n✓ Percakapan direset\n")
                    continue
                
                if user_input.lower() == 'stats':
                    stats = self.rag.get_statistics()
                    print(f"\n📊 Knowledge Base Statistics:")
                    print(f"  Health Records: {stats['health_records']}")
                    print(f"  Policies: {stats['policies']}")
                    print(f"  Insights: {stats['insights']}")
                    print(f"  Total: {stats['total']}\n")
                    continue
                
                # Get relevant context from RAG
                context = self.rag.get_context_for_query(user_input)
                
                # Prepare enhanced message with context
                if context:
                    enhanced_message = f"""Berdasarkan data yang tersedia:

{context}

Pertanyaan: {user_input}

Berikan jawaban yang akurat berdasarkan data di atas. Jika data tidak cukup, jelaskan keterbatasannya."""
                else:
                    enhanced_message = user_input
                
                # Get response from LLM
                print("\nArogya: ", end="", flush=True)
                response = self.llm.chat(enhanced_message, self.conversation_history)
                print(response + "\n")
                
                # Update conversation history
                self.conversation_history.append({
                    "role": "user",
                    "content": user_input
                })
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response
                })
                
                # Keep only last 10 exchanges to manage context size
                if len(self.conversation_history) > 20:
                    self.conversation_history = self.conversation_history[-20:]
                
            except KeyboardInterrupt:
                print("\n\n👋 Terima kasih telah menggunakan Arogya AI!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}\n")

def main():
    # Check if knowledge base exists
    if not os.path.exists('knowledge'):
        print("⚠️  Knowledge base belum disetup!")
        print("\nJalankan terlebih dahulu:")
        print("  python arogya/setup_knowledge_base.py")
        print("\nAtau import data kesehatan:")
        print("  python data/import_profil_kesehatan.py")
        print()
        
        choice = input("Lanjutkan tanpa knowledge base? (y/n): ").strip().lower()
        if choice != 'y':
            sys.exit(0)
    
    chat = ArogyaChat()
    chat.chat_loop()

if __name__ == '__main__':
    main()

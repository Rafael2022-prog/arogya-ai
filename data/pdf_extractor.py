import PyPDF2
import pandas as pd
import re
import json

class PDFHealthDataExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.text = ""
        
    def extract_text(self):
        """Ekstrak teks dari PDF"""
        print(f"Membaca PDF: {self.pdf_path}")
        with open(self.pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                self.text += page.extract_text() + "\n"
        
        print(f"Berhasil ekstrak {len(self.text)} karakter")
        return self.text
    
    def save_raw_text(self, output_path='data/extracted_text.txt'):
        """Simpan teks mentah untuk review manual"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(self.text)
        print(f"Teks mentah disimpan di: {output_path}")
    
    def parse_to_dataframe(self):
        """Parse teks ke DataFrame (perlu disesuaikan dengan format PDF Anda)"""
        # Template parsing - sesuaikan dengan format PDF Anda
        data = []
        
        # Contoh pattern untuk tabel kesehatan
        # Format: Bulan | Kecamatan | Penyakit | Jumlah Kasus
        lines = self.text.split('\n')
        
        for line in lines:
            # Skip baris kosong atau header
            if not line.strip() or 'LAPORAN' in line.upper():
                continue
            
            # Coba ekstrak data dengan berbagai pattern
            # Pattern 1: Data terpisah spasi/tab
            parts = re.split(r'\s{2,}|\t', line.strip())
            
            if len(parts) >= 4:
                try:
                    # Coba identifikasi kolom
                    row = {
                        'raw_line': line,
                        'parts': parts
                    }
                    data.append(row)
                except:
                    continue
        
        df = pd.DataFrame(data)
        return df
    
    def interactive_mapping(self):
        """Mode interaktif untuk mapping kolom"""
        print("\n=== MODE INTERAKTIF ===")
        print("Saya akan menampilkan beberapa baris pertama dari PDF.")
        print("Anda perlu memberitahu saya struktur datanya.\n")
        
        lines = [l for l in self.text.split('\n') if l.strip()][:20]
        
        for i, line in enumerate(lines, 1):
            print(f"{i}. {line}")
        
        print("\n" + "="*50)
        print("Contoh struktur yang diharapkan:")
        print("bulan,tahun,kecamatan,penyakit,jumlah_kasus,jumlah_penduduk,fasilitas_kesehatan")
        print("\nSilakan buat file 'data/mapping_config.json' dengan struktur:")
        print(json.dumps({
            "start_row": 5,
            "columns": {
                "0": "bulan",
                "1": "kecamatan", 
                "2": "penyakit",
                "3": "jumlah_kasus"
            },
            "separator": "\\s{2,}",
            "defaults": {
                "tahun": 2024,
                "jumlah_penduduk": 12000,
                "fasilitas_kesehatan": 2
            }
        }, indent=2))

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Penggunaan: python pdf_extractor.py <path_to_pdf>")
        print("\nContoh:")
        print("  python data/pdf_extractor.py data/laporan_kesehatan.pdf")
        return
    
    pdf_path = sys.argv[1]
    
    # Ekstrak PDF
    extractor = PDFHealthDataExtractor(pdf_path)
    extractor.extract_text()
    
    # Simpan teks mentah
    extractor.save_raw_text()
    
    # Mode interaktif
    extractor.interactive_mapping()
    
    print("\n✓ Langkah selanjutnya:")
    print("1. Buka file 'data/extracted_text.txt' untuk melihat hasil ekstraksi")
    print("2. Identifikasi struktur data (kolom apa saja, mulai baris berapa)")
    print("3. Jalankan: python data/manual_converter.py untuk konversi manual")

if __name__ == '__main__':
    main()

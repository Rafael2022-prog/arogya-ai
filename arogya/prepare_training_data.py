#!/usr/bin/env python3
"""
Arogya AI - Prepare Training Dataset
Convert health data to conversational format for fine-tuning
"""

import pandas as pd
import json
import random
from typing import List, Dict

class ArogyaDatasetGenerator:
    """Generate training dataset from health data"""
    
    def __init__(self):
        self.templates = self._load_templates()
        self.dataset = []
    
    def _load_templates(self) -> Dict:
        """Load conversation templates"""
        return {
            'prediction': [
                {
                    'instruction': 'Prediksi jumlah kasus {penyakit} di {kecamatan} bulan {bulan}',
                    'response': 'Berdasarkan data historis, prediksi kasus {penyakit} di {kecamatan} untuk bulan {bulan} adalah sekitar {jumlah_kasus} kasus. Dengan populasi {jumlah_penduduk} jiwa dan {fasilitas_kesehatan} fasilitas kesehatan.'
                },
                {
                    'instruction': 'Berapa estimasi kasus {penyakit} di {kecamatan}?',
                    'response': 'Estimasi kasus {penyakit} di {kecamatan} adalah {jumlah_kasus} kasus berdasarkan data tahun {tahun}. Area ini memiliki {fasilitas_kesehatan} fasilitas kesehatan untuk melayani {jumlah_penduduk} penduduk.'
                }
            ],
            'analysis': [
                {
                    'instruction': 'Analisis situasi {penyakit} di {kecamatan}',
                    'response': 'Situasi {penyakit} di {kecamatan}: Tercatat {jumlah_kasus} kasus pada bulan {bulan} tahun {tahun}. Dengan rasio kasus per 1000 penduduk adalah {rasio}. Diperlukan monitoring ketat mengingat kapasitas {fasilitas_kesehatan} fasilitas kesehatan.'
                }
            ],
            'comparison': [
                {
                    'instruction': 'Bandingkan kasus {penyakit} antar kecamatan',
                    'response': 'Perbandingan kasus {penyakit}: {kecamatan} memiliki {jumlah_kasus} kasus dengan populasi {jumlah_penduduk} jiwa.'
                }
            ],
            'recommendation': [
                {
                    'instruction': 'Rekomendasi untuk menangani {penyakit} di {kecamatan}',
                    'response': 'Rekomendasi untuk {kecamatan} dengan {jumlah_kasus} kasus {penyakit}: 1) Tingkatkan sosialisasi pencegahan, 2) Optimalkan {fasilitas_kesehatan} fasilitas kesehatan yang ada, 3) Monitoring rutin mengingat populasi {jumlah_penduduk} jiwa.'
                }
            ]
        }
    
    def generate_from_health_data(self, df: pd.DataFrame) -> List[Dict]:
        """Generate training examples from health data"""
        print(f"📊 Generating training data from {len(df)} health records...")
        
        examples = []
        
        for _, row in df.iterrows():
            # Calculate ratio
            rasio = round((row['jumlah_kasus'] / row['jumlah_penduduk']) * 1000, 2)
            
            # Fill template variables
            variables = {
                'tahun': row['tahun'],
                'bulan': self._get_month_name(row['bulan']),
                'kecamatan': row['kecamatan'],
                'penyakit': row['penyakit'],
                'jumlah_kasus': row['jumlah_kasus'],
                'jumlah_penduduk': row['jumlah_penduduk'],
                'fasilitas_kesehatan': row['fasilitas_kesehatan'],
                'rasio': rasio
            }
            
            # Generate examples for each template type
            for template_type, templates in self.templates.items():
                for template in templates:
                    example = {
                        'instruction': template['instruction'].format(**variables),
                        'input': '',
                        'output': template['response'].format(**variables),
                        'metadata': {
                            'type': template_type,
                            'source': 'health_data',
                            'kecamatan': row['kecamatan'],
                            'penyakit': row['penyakit']
                        }
                    }
                    examples.append(example)
        
        print(f"✓ Generated {len(examples)} training examples")
        return examples
    
    def generate_system_knowledge(self) -> List[Dict]:
        """Generate examples about Arogya's identity and capabilities"""
        print("🤖 Generating system knowledge examples...")
        
        examples = [
            {
                'instruction': 'Siapa kamu?',
                'input': '',
                'output': 'Saya adalah Arogya AI, asisten kesehatan cerdas untuk Kabupaten Maluku Tenggara. Nama saya berasal dari bahasa Sansekerta yang berarti "kesehatan sempurna". Saya dilatih khusus untuk membantu analisis dan prediksi kesehatan masyarakat di 9 kecamatan Maluku Tenggara.'
            },
            {
                'instruction': 'Apa yang bisa kamu lakukan?',
                'input': '',
                'output': 'Saya dapat membantu: 1) Memprediksi penyebaran penyakit, 2) Menganalisis tren kesehatan, 3) Memberikan rekomendasi kebijakan kesehatan, 4) Membandingkan data antar kecamatan, 5) Memberikan insight dari data historis kesehatan Maluku Tenggara.'
            },
            {
                'instruction': 'Kecamatan apa saja yang kamu cover?',
                'input': '',
                'output': 'Saya melayani 9 kecamatan di Kabupaten Maluku Tenggara: Kei Kecil, Kei Kecil Timur, Kei Kecil Barat, Kei Besar, Kei Besar Selatan, Kei Besar Utara Timur, Kei Besar Utara Barat, Manyeuw, dan Hoat Sorbay.'
            },
            {
                'instruction': 'Penyakit apa yang sering terjadi di Maluku Tenggara?',
                'input': '',
                'output': 'Penyakit yang umum di Maluku Tenggara meliputi: DBD (Demam Berdarah Dengue), ISPA (Infeksi Saluran Pernapasan Akut), Malaria, Diare, Tuberkulosis, Stunting, dan Pneumonia. Saya dapat membantu analisis dan prediksi untuk semua penyakit ini.'
            }
        ]
        
        print(f"✓ Generated {len(examples)} system knowledge examples")
        return examples
    
    def _get_month_name(self, month: int) -> str:
        """Convert month number to Indonesian name"""
        months = {
            1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April',
            5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Agustus',
            9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'
        }
        return months.get(month, str(month))
    
    def save_dataset(self, examples: List[Dict], output_path: str):
        """Save dataset in JSON format"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(examples, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Dataset saved to: {output_path}")
        print(f"  Total examples: {len(examples)}")
    
    def create_full_dataset(self, health_data_path: str, output_path: str = 'arogya/training_data.json'):
        """Create complete training dataset"""
        print("="*60)
        print("     AROGYA AI - Training Dataset Preparation")
        print("="*60)
        
        all_examples = []
        
        # Load health data
        if pd.io.common.file_exists(health_data_path):
            df = pd.read_csv(health_data_path)
            health_examples = self.generate_from_health_data(df)
            all_examples.extend(health_examples)
        else:
            print(f"⚠️  Health data not found: {health_data_path}")
        
        # Add system knowledge
        system_examples = self.generate_system_knowledge()
        all_examples.extend(system_examples)
        
        # Shuffle
        random.shuffle(all_examples)
        
        # Save
        self.save_dataset(all_examples, output_path)
        
        # Statistics
        print("\n📊 Dataset Statistics:")
        types = {}
        for ex in all_examples:
            t = ex.get('metadata', {}).get('type', 'system')
            types[t] = types.get(t, 0) + 1
        
        for t, count in types.items():
            print(f"  {t}: {count} examples")
        
        print("\n✅ Dataset preparation complete!")
        print(f"\nNext step: python arogya/finetune_model.py")
        
        return all_examples

def main():
    import sys
    
    # Check for health data
    health_data_path = 'data/health_data.csv'
    
    if not pd.io.common.file_exists(health_data_path):
        print("⚠️  Health data not found!")
        print("\nJalankan terlebih dahulu:")
        print("  python data/import_profil_kesehatan.py")
        sys.exit(1)
    
    # Generate dataset
    generator = ArogyaDatasetGenerator()
    generator.create_full_dataset(health_data_path)

if __name__ == '__main__':
    main()

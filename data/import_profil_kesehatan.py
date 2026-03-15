import pandas as pd
import os
import json

class ProfilKesehatanImporter:
    """Tool untuk import data profil kesehatan Maluku Tenggara"""
    
    def __init__(self):
        self.data_2013 = None
        self.data_2024 = None
        self.combined_data = None
    
    def load_excel(self, file_path, year):
        """Load data dari Excel profil kesehatan"""
        print(f"\n📂 Membaca file: {file_path}")
        
        try:
            # Coba baca semua sheets
            excel_file = pd.ExcelFile(file_path)
            print(f"✓ Ditemukan {len(excel_file.sheet_names)} sheets:")
            for i, sheet in enumerate(excel_file.sheet_names, 1):
                print(f"   {i}. {sheet}")
            
            # Simpan info untuk processing
            return {
                'file': excel_file,
                'year': year,
                'sheets': excel_file.sheet_names
            }
        except Exception as e:
            print(f"❌ Error membaca file: {e}")
            return None
    
    def extract_penyakit_data(self, excel_info, sheet_name=None):
        """Ekstrak data penyakit dari sheet tertentu"""
        excel_file = excel_info['file']
        year = excel_info['year']
        
        if sheet_name is None:
            print("\nPilih sheet yang berisi data penyakit:")
            for i, sheet in enumerate(excel_info['sheets'], 1):
                print(f"{i}. {sheet}")
            choice = int(input("Nomor sheet: ")) - 1
            sheet_name = excel_info['sheets'][choice]
        
        print(f"\n📊 Membaca sheet: {sheet_name}")
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        
        print(f"✓ Ditemukan {len(df)} baris, {len(df.columns)} kolom")
        print("\nPreview data:")
        print(df.head())
        
        return df
    
    def interactive_mapping(self, df, year):
        """Mapping interaktif kolom ke format standar"""
        print("\n" + "="*60)
        print("MAPPING KOLOM KE FORMAT STANDAR")
        print("="*60)
        
        print("\nKolom yang tersedia:")
        for i, col in enumerate(df.columns, 1):
            print(f"{i}. {col}")
        
        print("\nFormat standar yang dibutuhkan:")
        print("- kecamatan: Nama kecamatan")
        print("- penyakit: Jenis penyakit")
        print("- jumlah_kasus: Total kasus")
        print("- bulan (opsional): Bulan kejadian")
        
        mapping = {}
        
        # Mapping kecamatan
        print("\n--- Mapping Kecamatan ---")
        kec_col = input("Nomor/nama kolom untuk KECAMATAN (atau 'skip'): ").strip()
        if kec_col.lower() != 'skip':
            try:
                mapping['kecamatan'] = df.columns[int(kec_col) - 1]
            except:
                mapping['kecamatan'] = kec_col
        
        # Mapping penyakit
        print("\n--- Mapping Penyakit ---")
        print("Apakah data penyakit ada di:")
        print("1. Satu kolom (contoh: kolom 'Jenis Penyakit')")
        print("2. Beberapa kolom (contoh: kolom 'DBD', 'ISPA', 'Malaria')")
        penyakit_type = input("Pilihan (1/2): ").strip()
        
        if penyakit_type == '1':
            penyakit_col = input("Nomor/nama kolom untuk PENYAKIT: ").strip()
            try:
                mapping['penyakit'] = df.columns[int(penyakit_col) - 1]
            except:
                mapping['penyakit'] = penyakit_col
            
            kasus_col = input("Nomor/nama kolom untuk JUMLAH KASUS: ").strip()
            try:
                mapping['jumlah_kasus'] = df.columns[int(kasus_col) - 1]
            except:
                mapping['jumlah_kasus'] = kasus_col
        else:
            # Multiple columns untuk berbagai penyakit
            print("\nMasukkan nomor kolom untuk setiap penyakit (pisahkan dengan koma)")
            print("Format: nomor_kolom:nama_penyakit")
            print("Contoh: 3:DBD,4:ISPA,5:Malaria")
            penyakit_cols = input("Input: ").strip()
            mapping['penyakit_columns'] = penyakit_cols
        
        # Mapping bulan (opsional)
        print("\n--- Mapping Bulan (Opsional) ---")
        bulan_col = input("Nomor/nama kolom untuk BULAN (atau 'skip'): ").strip()
        if bulan_col.lower() != 'skip':
            try:
                mapping['bulan'] = df.columns[int(bulan_col) - 1]
            except:
                mapping['bulan'] = bulan_col
        
        return mapping
    
    def transform_data(self, df, mapping, year):
        """Transform data ke format standar"""
        print("\n🔄 Transforming data...")
        
        result_data = []
        
        # Jika penyakit di multiple columns
        if 'penyakit_columns' in mapping:
            penyakit_cols = mapping['penyakit_columns'].split(',')
            
            for _, row in df.iterrows():
                kecamatan = row[mapping.get('kecamatan', df.columns[0])]
                
                for col_info in penyakit_cols:
                    try:
                        col_num, penyakit_name = col_info.split(':')
                        col_idx = int(col_num) - 1
                        jumlah_kasus = row[df.columns[col_idx]]
                        
                        if pd.notna(jumlah_kasus) and jumlah_kasus > 0:
                            result_data.append({
                                'tahun': year,
                                'bulan': row.get(mapping.get('bulan'), 12),  # Default bulan 12 jika tidak ada
                                'kecamatan': kecamatan,
                                'penyakit': penyakit_name.strip(),
                                'jumlah_kasus': int(jumlah_kasus)
                            })
                    except Exception as e:
                        continue
        else:
            # Penyakit di satu kolom
            for _, row in df.iterrows():
                try:
                    result_data.append({
                        'tahun': year,
                        'bulan': row.get(mapping.get('bulan'), 12),
                        'kecamatan': row[mapping['kecamatan']],
                        'penyakit': row[mapping['penyakit']],
                        'jumlah_kasus': int(row[mapping['jumlah_kasus']])
                    })
                except:
                    continue
        
        result_df = pd.DataFrame(result_data)
        print(f"✓ Berhasil transform {len(result_df)} baris data")
        
        return result_df
    
    def add_demographic_data(self, df):
        """Tambahkan data demografis (populasi dan fasilitas kesehatan)"""
        print("\n📍 Menambahkan data demografis...")
        
        # Data demografis Maluku Tenggara per kecamatan (estimasi)
        # Anda bisa update dengan data real
        demographic_data = {
            'Kei Kecil': {'populasi': 12000, 'faskes': 2},
            'Kei Kecil Timur': {'populasi': 8000, 'faskes': 1},
            'Kei Kecil Barat': {'populasi': 7000, 'faskes': 1},
            'Kei Besar': {'populasi': 15000, 'faskes': 3},
            'Kei Besar Selatan': {'populasi': 10000, 'faskes': 2},
            'Kei Besar Utara Timur': {'populasi': 9000, 'faskes': 2},
            'Kei Besar Utara Barat': {'populasi': 8500, 'faskes': 1},
            'Manyeuw': {'populasi': 6000, 'faskes': 1},
            'Hoat Sorbay': {'populasi': 5500, 'faskes': 1}
        }
        
        print("\nGunakan data demografis default? (y/n)")
        print("Default: populasi dan jumlah faskes per kecamatan")
        use_default = input("Pilihan: ").strip().lower()
        
        if use_default != 'y':
            print("\nInput data demografis manual:")
            for kecamatan in df['kecamatan'].unique():
                print(f"\n{kecamatan}:")
                pop = input(f"  Jumlah penduduk: ").strip()
                faskes = input(f"  Jumlah fasilitas kesehatan: ").strip()
                demographic_data[kecamatan] = {
                    'populasi': int(pop) if pop else 10000,
                    'faskes': int(faskes) if faskes else 2
                }
        
        # Apply demographic data
        df['jumlah_penduduk'] = df['kecamatan'].map(
            lambda x: demographic_data.get(x, {'populasi': 10000})['populasi']
        )
        df['fasilitas_kesehatan'] = df['kecamatan'].map(
            lambda x: demographic_data.get(x, {'faskes': 2})['faskes']
        )
        
        return df
    
    def save_data(self, df, output_path='data/health_data.csv'):
        """Simpan data ke CSV"""
        # Gabung dengan data existing jika ada
        if os.path.exists(output_path):
            print(f"\n⚠ File {output_path} sudah ada")
            choice = input("Gabung dengan data existing? (y/n): ").strip().lower()
            if choice == 'y':
                existing_df = pd.read_csv(output_path)
                df = pd.concat([existing_df, df], ignore_index=True)
                df = df.drop_duplicates()
        
        df.to_csv(output_path, index=False)
        print(f"\n✅ Data berhasil disimpan ke: {output_path}")
        print(f"Total: {len(df)} baris data")
        
        # Statistik
        print("\n📊 Statistik Data:")
        print(f"Periode: {df['tahun'].min()} - {df['tahun'].max()}")
        print(f"Jumlah kecamatan: {df['kecamatan'].nunique()}")
        print(f"Jenis penyakit: {df['penyakit'].nunique()}")
        print(f"\nKecamatan: {', '.join(df['kecamatan'].unique())}")
        print(f"\nPenyakit: {', '.join(df['penyakit'].unique())}")
        
        return df

def main():
    print("="*60)
    print("IMPORT DATA PROFIL KESEHATAN MALUKU TENGGARA")
    print("="*60)
    
    importer = ProfilKesehatanImporter()
    
    all_data = []
    
    # Import data 2013
    print("\n--- DATA TAHUN 2013 ---")
    file_2013 = input("Path file profil kesehatan 2013 (atau 'skip'): ").strip()
    if file_2013.lower() != 'skip' and os.path.exists(file_2013):
        excel_info = importer.load_excel(file_2013, 2013)
        if excel_info:
            df_raw = importer.extract_penyakit_data(excel_info)
            mapping = importer.interactive_mapping(df_raw, 2013)
            df_2013 = importer.transform_data(df_raw, mapping, 2013)
            df_2013 = importer.add_demographic_data(df_2013)
            all_data.append(df_2013)
    
    # Import data 2024
    print("\n--- DATA TAHUN 2024 ---")
    file_2024 = input("Path file profil kesehatan 2024 (atau 'skip'): ").strip()
    if file_2024.lower() != 'skip' and os.path.exists(file_2024):
        excel_info = importer.load_excel(file_2024, 2024)
        if excel_info:
            df_raw = importer.extract_penyakit_data(excel_info)
            mapping = importer.interactive_mapping(df_raw, 2024)
            df_2024 = importer.transform_data(df_raw, mapping, 2024)
            df_2024 = importer.add_demographic_data(df_2024)
            all_data.append(df_2024)
    
    # Gabungkan semua data
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        importer.save_data(combined_df)
        
        print("\n✅ SELESAI!")
        print("\nLangkah selanjutnya:")
        print("1. Review file 'data/health_data.csv'")
        print("2. Jalankan training model: python models/train.py")
        print("3. Test prediksi: python api/app.py")
    else:
        print("\n⚠ Tidak ada data yang diimport")

if __name__ == '__main__':
    main()

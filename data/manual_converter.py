import pandas as pd
import json
import os

def manual_data_entry():
    """Tool untuk input data manual dari PDF"""
    print("="*60)
    print("TOOL INPUT DATA MANUAL - Kesehatan Maluku Tenggara")
    print("="*60)
    
    data = []
    
    print("\nPetunjuk:")
    print("- Masukkan data sesuai yang tertera di PDF")
    print("- Ketik 'selesai' pada kolom bulan untuk mengakhiri")
    print("- Data akan disimpan ke 'data/health_data.csv'\n")
    
    while True:
        print("\n--- Entry Data Baru ---")
        
        bulan = input("Bulan (1-12) atau 'selesai': ").strip()
        if bulan.lower() == 'selesai':
            break
        
        try:
            bulan = int(bulan)
            if bulan < 1 or bulan > 12:
                print("❌ Bulan harus 1-12")
                continue
        except:
            print("❌ Bulan harus angka")
            continue
        
        tahun = input("Tahun (contoh: 2024): ").strip()
        kecamatan = input("Kecamatan: ").strip()
        penyakit = input("Jenis Penyakit: ").strip()
        jumlah_kasus = input("Jumlah Kasus: ").strip()
        jumlah_penduduk = input("Jumlah Penduduk: ").strip()
        fasilitas_kesehatan = input("Jumlah Fasilitas Kesehatan: ").strip()
        
        try:
            row = {
                'bulan': int(bulan),
                'tahun': int(tahun),
                'kecamatan': kecamatan,
                'penyakit': penyakit,
                'jumlah_kasus': int(jumlah_kasus),
                'jumlah_penduduk': int(jumlah_penduduk),
                'fasilitas_kesehatan': int(fasilitas_kesehatan)
            }
            data.append(row)
            print(f"✓ Data tersimpan ({len(data)} baris)")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    if data:
        df = pd.DataFrame(data)
        
        # Gabung dengan data existing jika ada
        if os.path.exists('data/health_data.csv'):
            existing_df = pd.read_csv('data/health_data.csv')
            df = pd.concat([existing_df, df], ignore_index=True)
        
        df.to_csv('data/health_data.csv', index=False)
        print(f"\n✓ Berhasil menyimpan {len(df)} baris data ke 'data/health_data.csv'")
        print("\nPreview data:")
        print(df.tail())
    else:
        print("\n⚠ Tidak ada data yang diinput")

def load_from_excel():
    """Konversi dari Excel jika PDF sudah diconvert ke Excel"""
    print("\n=== KONVERSI DARI EXCEL ===")
    excel_path = input("Path file Excel: ").strip()
    
    if not os.path.exists(excel_path):
        print(f"❌ File tidak ditemukan: {excel_path}")
        return
    
    try:
        df = pd.read_excel(excel_path)
        print("\nKolom yang ditemukan:")
        for i, col in enumerate(df.columns):
            print(f"{i}. {col}")
        
        print("\nMapping kolom ke format yang dibutuhkan:")
        print("Format: bulan,tahun,kecamatan,penyakit,jumlah_kasus,jumlah_penduduk,fasilitas_kesehatan")
        
        mapping = {}
        for target in ['bulan', 'tahun', 'kecamatan', 'penyakit', 'jumlah_kasus', 
                       'jumlah_penduduk', 'fasilitas_kesehatan']:
            source = input(f"Kolom untuk '{target}' (nomor atau nama, kosongkan jika tidak ada): ").strip()
            if source:
                try:
                    source = int(source)
                    mapping[target] = df.columns[source]
                except:
                    mapping[target] = source
        
        # Buat DataFrame baru dengan mapping
        new_df = pd.DataFrame()
        for target, source in mapping.items():
            if source in df.columns:
                new_df[target] = df[source]
        
        # Isi nilai default untuk kolom yang kosong
        for col in ['bulan', 'tahun', 'kecamatan', 'penyakit', 'jumlah_kasus', 
                    'jumlah_penduduk', 'fasilitas_kesehatan']:
            if col not in new_df.columns:
                default = input(f"Nilai default untuk '{col}': ").strip()
                new_df[col] = default
        
        new_df.to_csv('data/health_data.csv', index=False)
        print(f"\n✓ Berhasil konversi {len(new_df)} baris")
        print("\nPreview:")
        print(new_df.head())
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("\nPilih metode input data:")
    print("1. Input manual dari PDF")
    print("2. Konversi dari Excel")
    print("3. Keluar")
    
    choice = input("\nPilihan (1-3): ").strip()
    
    if choice == '1':
        manual_data_entry()
    elif choice == '2':
        load_from_excel()
    else:
        print("Keluar...")

if __name__ == '__main__':
    main()

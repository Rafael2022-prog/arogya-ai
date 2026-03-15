import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os

def load_data():
    """Memuat data kesehatan"""
    # Coba load data real, fallback ke sample
    if os.path.exists('data/health_data.csv'):
        print("Menggunakan data real: data/health_data.csv")
        df = pd.read_csv('data/health_data.csv')
    else:
        print("Menggunakan sample data: data/sample_data.csv")
        df = pd.read_csv('data/sample_data.csv')
    
    print(f"Total data: {len(df)} baris")
    print(f"Periode: {df['tahun'].min()} - {df['tahun'].max()}")
    return df

def prepare_features(df):
    """Menyiapkan fitur untuk model"""
    # Encoding kategorikal
    df['kecamatan_encoded'] = pd.Categorical(df['kecamatan']).codes
    df['penyakit_encoded'] = pd.Categorical(df['penyakit']).codes
    
    # Fitur tambahan
    df['rasio_kasus'] = df['jumlah_kasus'] / df['jumlah_penduduk'] * 1000
    df['rasio_faskes'] = df['jumlah_penduduk'] / df['fasilitas_kesehatan']
    
    return df

def train_model():
    """Training model prediksi"""
    print("Memuat data...")
    df = load_data()
    df = prepare_features(df)
    
    # Fitur dan target
    features = ['bulan', 'kecamatan_encoded', 'penyakit_encoded', 
                'jumlah_penduduk', 'fasilitas_kesehatan']
    X = df[features]
    y = df['jumlah_kasus']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Training
    print("Training model...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluasi
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"MAE: {mae:.2f}")
    print(f"R2 Score: {r2:.2f}")
    
    # Simpan model
    os.makedirs('models/saved', exist_ok=True)
    joblib.dump(model, 'models/saved/health_model.pkl')
    
    # Simpan mapping
    mapping = {
        'kecamatan': dict(enumerate(df['kecamatan'].unique())),
        'penyakit': dict(enumerate(df['penyakit'].unique()))
    }
    joblib.dump(mapping, 'models/saved/mapping.pkl')
    
    print("Model berhasil disimpan!")
    return model

if __name__ == '__main__':
    train_model()

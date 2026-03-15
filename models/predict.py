import joblib
import numpy as np

class HealthPredictor:
    def __init__(self):
        self.model = joblib.load('models/saved/health_model.pkl')
        self.mapping = joblib.load('models/saved/mapping.pkl')
    
    def predict(self, bulan, kecamatan, penyakit, jumlah_penduduk, fasilitas_kesehatan):
        """Prediksi jumlah kasus"""
        # Encoding
        kecamatan_map = {v: k for k, v in self.mapping['kecamatan'].items()}
        penyakit_map = {v: k for k, v in self.mapping['penyakit'].items()}
        
        kecamatan_encoded = kecamatan_map.get(kecamatan, 0)
        penyakit_encoded = penyakit_map.get(penyakit, 0)
        
        # Prediksi
        features = np.array([[bulan, kecamatan_encoded, penyakit_encoded, 
                             jumlah_penduduk, fasilitas_kesehatan]])
        prediction = self.model.predict(features)[0]
        
        return max(0, int(prediction))
    
    def get_recommendations(self, prediction, kecamatan):
        """Rekomendasi berdasarkan prediksi"""
        recommendations = []
        
        if prediction > 30:
            recommendations.append(f"PERINGATAN: Prediksi kasus tinggi di {kecamatan}")
            recommendations.append("Tingkatkan sosialisasi pencegahan")
            recommendations.append("Siapkan stok obat dan tenaga medis")
        elif prediction > 15:
            recommendations.append("Lakukan monitoring rutin")
            recommendations.append("Edukasi masyarakat tentang gejala awal")
        else:
            recommendations.append("Kondisi terkendali")
            recommendations.append("Lanjutkan program pencegahan rutin")
        
        return recommendations

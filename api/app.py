from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
sys.path.append('..')
from models.predict import HealthPredictor

app = Flask(__name__)
CORS(app)

predictor = None

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'API Kesehatan Maluku Tenggara'})

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        prediction = predictor.predict(
            bulan=data['bulan'],
            kecamatan=data['kecamatan'],
            penyakit=data['penyakit'],
            jumlah_penduduk=data['jumlah_penduduk'],
            fasilitas_kesehatan=data['fasilitas_kesehatan']
        )
        
        recommendations = predictor.get_recommendations(
            prediction, data['kecamatan']
        )
        
        return jsonify({
            'prediksi_kasus': prediction,
            'rekomendasi': recommendations
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/kecamatan', methods=['GET'])
def get_kecamatan():
    kecamatan_list = list(predictor.mapping['kecamatan'].values())
    return jsonify({'kecamatan': kecamatan_list})

@app.route('/api/penyakit', methods=['GET'])
def get_penyakit():
    penyakit_list = list(predictor.mapping['penyakit'].values())
    return jsonify({'penyakit': penyakit_list})

if __name__ == '__main__':
    print("Memuat model...")
    predictor = HealthPredictor()
    print("Server siap!")
    app.run(host='0.0.0.0', port=5000, debug=True)

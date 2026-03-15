#!/usr/bin/env python3
"""
Arogya AI - API Server
REST API for integration with other systems
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from llm_engine import ArogyaLLM
from rag_system import ArogyaRAG

app = Flask(__name__)
CORS(app)

llm = ArogyaLLM()
rag = ArogyaRAG()

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'service': 'Arogya AI',
        'version': '1.0',
        'model': 'Llama 3 + RAG'
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    context = data.get('context', [])
    
    if not message:
        return jsonify({'error': 'Message required'}), 400
    
    # Get relevant context from RAG
    rag_context = rag.get_context_for_query(message)
    
    # Enhance message with context
    if rag_context:
        enhanced_message = f"Data: {rag_context}\n\nPertanyaan: {message}"
    else:
        enhanced_message = message
    
    # Get response from LLM
    response = llm.chat(enhanced_message, context)
    
    return jsonify({
        'response': response,
        'has_context': bool(rag_context)
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    stats = rag.get_statistics()
    return jsonify(stats)

if __name__ == '__main__':
    print("🚀 Starting Arogya AI API Server...")
    print("📍 API: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)

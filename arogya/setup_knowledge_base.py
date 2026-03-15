#!/usr/bin/env python3
"""
Setup Knowledge Base for Arogya AI
Load initial data into RAG system
"""

import os
import sys
import pandas as pd
from rag_system import ArogyaRAG

def setup_knowledge_base():
    print("="*60)
    print("     AROGYA AI - Knowledge Base Setup")
    print("="*60)
    
    rag = ArogyaRAG()
    
    # Check for health data
    data_path = 'data/health_data.csv'
    
    if os.path.exists(data_path):
        print(f"\n📂 Loading data from: {data_path}")
        df = pd.read_csv(data_path)
        rag.add_health_data(df)
    else:
        print(f"\n⚠️  File tidak ditemukan: {data_path}")
        print("\nJalankan terlebih dahulu:")
        print("  python data/import_profil_kesehatan.py")
        return
    
    # Add default policies
    print("\n📋 Adding default health policies...")
    rag.add_policy(
        title="Pencegahan DBD",
        content="Program 3M Plus: Menguras, Menutup, Mengubur, plus menghindari gigitan nyamuk"
    )
    
    print("\n✅ Knowledge base setup complete!")
    stats = rag.get_statistics()
    print(f"\n📊 Statistics:")
    print(f"  Health Records: {stats['health_records']}")
    print(f"  Policies: {stats['policies']}")
    print(f"  Total: {stats['total']}")

if __name__ == '__main__':
    setup_knowledge_base()

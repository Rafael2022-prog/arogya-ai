import chromadb
from chromadb.config import Settings
import pandas as pd
from typing import List, Dict, Optional
import json
from datetime import datetime

class ArogyaRAG:
    """
    Arogya AI - RAG (Retrieval-Augmented Generation) System
    Enables continuous learning without retraining
    """
    
    def __init__(self, persist_directory: str = "knowledge"):
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        
        # Collections for different types of knowledge
        self.health_data_collection = self._get_or_create_collection("health_data")
        self.policies_collection = self._get_or_create_collection("policies")
        self.insights_collection = self._get_or_create_collection("insights")
        
    def _get_or_create_collection(self, name: str):
        """Get or create a collection"""
        try:
            return self.client.get_collection(name)
        except:
            return self.client.create_collection(name)
    
    def add_health_data(self, df: pd.DataFrame):
        """
        Add health data to knowledge base
        Data will be automatically indexed for retrieval
        """
        print(f"📚 Adding {len(df)} health records to knowledge base...")
        
        documents = []
        metadatas = []
        ids = []
        
        for idx, row in df.iterrows():
            # Create searchable document
            doc = f"""
            Tahun: {row['tahun']}
            Bulan: {row['bulan']}
            Kecamatan: {row['kecamatan']}
            Penyakit: {row['penyakit']}
            Jumlah Kasus: {row['jumlah_kasus']}
            Populasi: {row.get('jumlah_penduduk', 'N/A')}
            Fasilitas Kesehatan: {row.get('fasilitas_kesehatan', 'N/A')}
            """
            
            documents.append(doc.strip())
            metadatas.append({
                'type': 'health_record',
                'tahun': str(row['tahun']),
                'bulan': str(row['bulan']),
                'kecamatan': row['kecamatan'],
                'penyakit': row['penyakit'],
                'jumlah_kasus': str(row['jumlah_kasus']),
                'timestamp': datetime.now().isoformat()
            })
            ids.append(f"health_{idx}_{datetime.now().timestamp()}")
        
        # Add to collection in batches
        batch_size = 100
        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i:i+batch_size]
            batch_meta = metadatas[i:i+batch_size]
            batch_ids = ids[i:i+batch_size]
            
            self.health_data_collection.add(
                documents=batch_docs,
                metadatas=batch_meta,
                ids=batch_ids
            )
        
        print(f"✓ Successfully added {len(documents)} records")
    
    def search_health_data(self, query: str, n_results: int = 5) -> List[Dict]:
        """
        Search relevant health data based on query
        
        Args:
            query: Natural language query
            n_results: Number of results to return
            
        Returns:
            List of relevant health records
        """
        results = self.health_data_collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        if not results['documents'][0]:
            return []
        
        # Format results
        formatted_results = []
        for i, doc in enumerate(results['documents'][0]):
            formatted_results.append({
                'document': doc,
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i] if 'distances' in results else None
            })
        
        return formatted_results
    
    def add_policy(self, title: str, content: str, metadata: Optional[Dict] = None):
        """Add health policy or guideline to knowledge base"""
        doc_id = f"policy_{datetime.now().timestamp()}"
        
        meta = metadata or {}
        meta.update({
            'type': 'policy',
            'title': title,
            'timestamp': datetime.now().isoformat()
        })
        
        self.policies_collection.add(
            documents=[content],
            metadatas=[meta],
            ids=[doc_id]
        )
        
        print(f"✓ Added policy: {title}")
    
    def add_insight(self, insight: str, source: str, metadata: Optional[Dict] = None):
        """Add analytical insight to knowledge base"""
        doc_id = f"insight_{datetime.now().timestamp()}"
        
        meta = metadata or {}
        meta.update({
            'type': 'insight',
            'source': source,
            'timestamp': datetime.now().isoformat()
        })
        
        self.insights_collection.add(
            documents=[insight],
            metadatas=[meta],
            ids=[doc_id]
        )
        
        print(f"✓ Added insight from: {source}")
    
    def get_context_for_query(self, query: str, max_results: int = 5) -> str:
        """
        Get relevant context for a query from all knowledge sources
        This context will be fed to the LLM
        """
        context_parts = []
        
        # Search health data
        health_results = self.search_health_data(query, n_results=max_results)
        if health_results:
            context_parts.append("=== DATA KESEHATAN RELEVAN ===")
            for result in health_results:
                context_parts.append(result['document'])
        
        # Search policies
        policy_results = self.policies_collection.query(
            query_texts=[query],
            n_results=3
        )
        if policy_results['documents'][0]:
            context_parts.append("\n=== KEBIJAKAN TERKAIT ===")
            for doc in policy_results['documents'][0]:
                context_parts.append(doc)
        
        # Search insights
        insight_results = self.insights_collection.query(
            query_texts=[query],
            n_results=3
        )
        if insight_results['documents'][0]:
            context_parts.append("\n=== INSIGHT ANALITIS ===")
            for doc in insight_results['documents'][0]:
                context_parts.append(doc)
        
        return "\n\n".join(context_parts)
    
    def get_statistics(self) -> Dict:
        """Get knowledge base statistics"""
        return {
            'health_records': self.health_data_collection.count(),
            'policies': self.policies_collection.count(),
            'insights': self.insights_collection.count(),
            'total': (self.health_data_collection.count() + 
                     self.policies_collection.count() + 
                     self.insights_collection.count())
        }

# Test
if __name__ == '__main__':
    print("Testing Arogya RAG System...")
    
    rag = ArogyaRAG()
    
    # Test with sample data
    sample_data = pd.DataFrame([
        {
            'tahun': 2024,
            'bulan': 3,
            'kecamatan': 'Kei Kecil',
            'penyakit': 'DBD',
            'jumlah_kasus': 18,
            'jumlah_penduduk': 12000,
            'fasilitas_kesehatan': 2
        }
    ])
    
    rag.add_health_data(sample_data)
    
    # Test search
    results = rag.search_health_data("DBD di Kei Kecil")
    print(f"\n✓ Found {len(results)} relevant records")
    
    # Statistics
    stats = rag.get_statistics()
    print(f"\n📊 Knowledge Base Statistics:")
    print(json.dumps(stats, indent=2))

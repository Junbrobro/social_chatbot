"""
검색 모델 초기화 모듈 (STEP 5)
- ChromaDB 또는 FAISS를 사용하여 벡터 검색 수행
- NumPy 폴백 지원
- 검색 인덱스 설정 및 top-k 검색 함수 정의
"""

import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# 프로젝트 루트 경로 설정
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
VECTOR_DB_DIR = DATA_DIR / "vector_db"
CHUNKS_DIR = DATA_DIR / "chunks"


class SearchModel:
    """
    벡터 검색 모델 클래스
    ChromaDB, FAISS, NumPy 중 사용 가능한 것을 자동 선택합니다.
    """
    
    def __init__(self, collection_name: str = "social_culture", backend: str = "auto"):
        """
        검색 모델을 초기화합니다.
        
        Args:
            collection_name: ChromaDB 컬렉션 이름
            backend: "chroma", "faiss", "numpy", "auto"
        """
        self.collection_name = collection_name
        self.backend = backend
        self.embedding_model = None
        
        # 백엔드별 리소스
        self.chroma_client = None
        self.chroma_collection = None
        self.faiss_index = None
        self.numpy_embeddings = None
        self.chunks = None
        
        self._initialize()
    
    def _initialize(self):
        """
        검색 백엔드를 초기화합니다.
        """
        from sentence_transformers import SentenceTransformer
        
        # 임베딩 모델 로드
        print(f"🤖 임베딩 모델 로드 중...")
        self.embedding_model = SentenceTransformer("jhgan/ko-sroberta-multitask")
        
        # 청크 데이터 로드
        self._load_chunks()
        
        # 백엔드 초기화
        if self.backend == "auto":
            # ChromaDB 시도 → FAISS 시도 → NumPy 폴백
            if self._init_chroma():
                self.backend = "chroma"
            elif self._init_faiss():
                self.backend = "faiss"
            else:
                self._init_numpy()
                self.backend = "numpy"
        elif self.backend == "chroma":
            if not self._init_chroma():
                print("⚠️ ChromaDB 초기화 실패, NumPy로 폴백")
                self._init_numpy()
                self.backend = "numpy"
        elif self.backend == "faiss":
            if not self._init_faiss():
                print("⚠️ FAISS 초기화 실패, NumPy로 폴백")
                self._init_numpy()
                self.backend = "numpy"
        else:
            self._init_numpy()
            self.backend = "numpy"
        
        print(f"   - 사용 백엔드: {self.backend.upper()}")
        print(f"   - 모델: jhgan/ko-sroberta-multitask")
    
    def _load_chunks(self):
        """청크 데이터를 로드합니다."""
        # combined_all_chunks.json 우선 로드
        combined_file = CHUNKS_DIR / "combined_all_chunks.json"
        if combined_file.exists():
            with open(combined_file, 'r', encoding='utf-8') as f:
                chunks_data = json.load(f)
                self.chunks = chunks_data.get('chunks', [])
            print(f"📖 {len(self.chunks)}개 청크 로드 완료 (통합 파일)")
        else:
            chunks_files = list(CHUNKS_DIR.glob("*_chunks.json"))
            if chunks_files:
                with open(chunks_files[0], 'r', encoding='utf-8') as f:
                    chunks_data = json.load(f)
                    self.chunks = chunks_data.get('chunks', [])
                print(f"📖 {len(self.chunks)}개 청크 로드 완료")
    
    def _init_chroma(self) -> bool:
        """ChromaDB를 초기화합니다."""
        try:
            import chromadb
            from chromadb.config import Settings
            
            chroma_path = str(VECTOR_DB_DIR / "chroma_db")
            print(f"📦 ChromaDB 로드 중: {chroma_path}")
            
            settings = Settings(anonymized_telemetry=False)
            self.chroma_client = chromadb.PersistentClient(path=chroma_path, settings=settings)
            self.chroma_collection = self.chroma_client.get_collection(name=self.collection_name)
            
            print(f"   - 컬렉션: {self.collection_name}")
            print(f"   - 문서 수: {self.chroma_collection.count()}")
            return True
        except Exception as e:
            print(f"⚠️ ChromaDB 초기화 실패: {e}")
            return False
    
    def _init_faiss(self) -> bool:
        """FAISS 인덱스를 로드합니다."""
        try:
            import faiss
            
            index_path = str(VECTOR_DB_DIR / "faiss_index.bin")
            print(f"📦 FAISS 로드 중: {index_path}")
            
            self.faiss_index = faiss.read_index(index_path)
            print(f"   - 벡터 수: {self.faiss_index.ntotal}")
            return True
        except Exception as e:
            print(f"⚠️ FAISS 초기화 실패: {e}")
            return False
    
    def _init_numpy(self) -> bool:
        """NumPy 임베딩을 로드합니다."""
        try:
            embeddings_path = VECTOR_DB_DIR / "embeddings.npy"
            print(f"📦 NumPy 임베딩 로드 중: {embeddings_path}")
            
            self.numpy_embeddings = np.load(str(embeddings_path))
            print(f"   - 벡터 수: {len(self.numpy_embeddings)}")
            print(f"   - 차원: {self.numpy_embeddings.shape[1]}")
            return True
        except Exception as e:
            print(f"⚠️ NumPy 초기화 실패: {e}")
            return False
    
    def embed_query(self, query: str) -> np.ndarray:
        """쿼리를 임베딩 벡터로 변환합니다."""
        return self.embedding_model.encode(query)
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        include_distances: bool = True
    ) -> List[Dict]:
        """쿼리와 유사한 문서를 검색합니다."""
        
        if self.backend == "chroma":
            return self._search_chroma(query, top_k)
        elif self.backend == "faiss":
            return self._search_faiss(query, top_k)
        else:
            return self._search_numpy(query, top_k)
    
    def _search_chroma(self, query: str, top_k: int) -> List[Dict]:
        """ChromaDB로 검색합니다."""
        query_embedding = self.embed_query(query).tolist()
        
        results = self.chroma_collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )
        
        search_results = []
        if results and results['documents']:
            documents = results['documents'][0]
            metadatas = results['metadatas'][0] if results['metadatas'] else [{}] * len(documents)
            distances = results['distances'][0] if results['distances'] else [0] * len(documents)
            ids = results['ids'][0] if results['ids'] else [''] * len(documents)
            
            for i, (doc, meta, dist, doc_id) in enumerate(zip(documents, metadatas, distances, ids)):
                # source_file이 metadata에 없으면 chunks에서 찾기
                if 'source_file' not in meta and self.chunks:
                    try:
                        # global_chunk_id 사용 (metadata에 있으면 우선 사용)
                        global_chunk_id = meta.get('global_chunk_id')
                        if global_chunk_id is None:
                            # doc_id에서 인덱스 추출 (예: "chunk_123" -> 123)
                            if '_' in doc_id:
                                global_chunk_id = int(doc_id.split('_')[-1])
                        
                        if global_chunk_id is not None and global_chunk_id < len(self.chunks):
                            chunk = self.chunks[global_chunk_id]
                            if 'source_file' in chunk:
                                meta['source_file'] = chunk['source_file']
                    except Exception as e:
                        pass
                
                result = {
                    "rank": i + 1,
                    "id": doc_id,
                    "text": doc,
                    "metadata": meta,
                    "distance": dist,
                    "similarity": 1 - dist
                }
                search_results.append(result)
        
        return search_results
    
    def _search_faiss(self, query: str, top_k: int) -> List[Dict]:
        """FAISS로 검색합니다."""
        query_embedding = self.embed_query(query).reshape(1, -1).astype('float32')
        
        distances, indices = self.faiss_index.search(query_embedding, top_k)
        
        search_results = []
        for rank, (idx, dist) in enumerate(zip(indices[0], distances[0])):
            if idx < 0:
                continue
            
            chunk = self.chunks[idx] if self.chunks and idx < len(self.chunks) else {}
            
            result = {
                "rank": rank + 1,
                "id": f"chunk_{idx}",
                "text": chunk.get('text', ''),
                "metadata": {
                    "page_number": chunk.get('page_number', 0),
                    "chunk_id": chunk.get('chunk_id', idx),
                    "char_count": chunk.get('char_count', 0),
                    "source_file": chunk.get('source_file', '')  # PDF 파일 이름 추가
                },
                "distance": float(dist),
                "similarity": 1 / (1 + float(dist))  # L2 거리를 유사도로 변환
            }
            search_results.append(result)
        
        return search_results
    
    def _search_numpy(self, query: str, top_k: int) -> List[Dict]:
        """NumPy로 검색합니다."""
        query_embedding = self.embed_query(query)
        
        # 코사인 유사도 계산
        query_norm = query_embedding / np.linalg.norm(query_embedding)
        embeddings_norm = self.numpy_embeddings / np.linalg.norm(self.numpy_embeddings, axis=1, keepdims=True)
        similarities = np.dot(embeddings_norm, query_norm)
        
        # top-k 인덱스
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        search_results = []
        for rank, idx in enumerate(top_indices):
            chunk = self.chunks[idx] if self.chunks and idx < len(self.chunks) else {}
            
            result = {
                "rank": rank + 1,
                "id": f"chunk_{idx}",
                "text": chunk.get('text', ''),
                "metadata": {
                    "page_number": chunk.get('page_number', 0),
                    "chunk_id": chunk.get('chunk_id', idx),
                    "char_count": chunk.get('char_count', 0),
                    "source_file": chunk.get('source_file', '')  # PDF 파일 이름 추가
                },
                "distance": 1 - similarities[idx],
                "similarity": float(similarities[idx])
            }
            search_results.append(result)
        
        return search_results
    
    def search_with_filter(
        self,
        query: str,
        top_k: int = 5,
        page_filter: Optional[Tuple[int, int]] = None
    ) -> List[Dict]:
        """필터를 적용하여 검색합니다."""
        all_results = self.search(query, top_k=top_k * 3)
        
        if page_filter:
            start_page, end_page = page_filter
            filtered = [
                r for r in all_results
                if start_page <= r['metadata'].get('page_number', 0) <= end_page
            ]
            for i, r in enumerate(filtered[:top_k]):
                r['rank'] = i + 1
            return filtered[:top_k]
        
        return all_results[:top_k]


def get_search_model(collection_name: str = "social_culture", backend: str = "auto") -> SearchModel:
    """검색 모델 인스턴스를 반환합니다."""
    return SearchModel(collection_name=collection_name, backend=backend)


def format_search_results(results: List[Dict], show_text: bool = True) -> str:
    """검색 결과를 포맷팅합니다."""
    output = []
    
    for result in results:
        output.append(f"\n[{result['rank']}위] 유사도: {result['similarity']:.4f}")
        output.append(f"   페이지: {result['metadata'].get('page_number', 'N/A')}")
        
        if show_text:
            text = result['text']
            if len(text) > 200:
                text = text[:200] + "..."
            output.append(f"   내용: {text}")
    
    return "\n".join(output)


# 테스트 코드
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🔍 검색 모델 테스트")
    print("="*60)
    
    # 검색 모델 초기화 (자동 백엔드 선택)
    search_model = get_search_model()
    
    # 테스트 쿼리
    test_queries = [
        "사회화란 무엇인가?",
        "문화의 특성에 대해 설명해줘"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"🔎 쿼리: {query}")
        print("="*60)
        
        results = search_model.search(query, top_k=3)
        print(format_search_results(results))
    
    print("\n" + "="*60)
    print("✅ 검색 모델 테스트 완료!")
    print("="*60 + "\n")

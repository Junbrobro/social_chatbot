"""
임베딩 및 벡터DB 생성 모듈 (STEP 3)
- sentence-transformers를 사용하여 청크 임베딩
- ChromaDB와 FAISS를 사용하여 벡터 DB 생성
- output: data/vector_db/ 에 embedding index 저장
"""

import os
import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional
import sys
import tempfile
import shutil

# 프로젝트 루트 경로 설정
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CHUNKS_DIR = DATA_DIR / "chunks"
VECTOR_DB_DIR = DATA_DIR / "vector_db"

# 임베딩 모델 설정 (한국어 지원 무료 모델)
EMBEDDING_MODEL = "jhgan/ko-sroberta-multitask"


def load_chunks(chunks_path: str) -> List[Dict]:
    """
    청크 JSON 파일을 로드합니다.
    """
    with open(chunks_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('chunks', [])


def create_embeddings(texts: List[str], model_name: str = EMBEDDING_MODEL) -> np.ndarray:
    """
    텍스트 리스트를 임베딩 벡터로 변환합니다.
    """
    from sentence_transformers import SentenceTransformer
    
    print(f"🤖 임베딩 모델 로드 중: {model_name}")
    model = SentenceTransformer(model_name)
    
    print(f"🔄 {len(texts)}개 텍스트 임베딩 중...")
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True
    )
    
    print(f"✅ 임베딩 완료! 차원: {embeddings.shape}")
    return embeddings


def build_chroma_db(
    chunks: List[Dict],
    embeddings: np.ndarray,
    collection_name: str = "social_culture",
    persist_directory: str = None
) -> bool:
    """
    ChromaDB를 사용하여 벡터 데이터베이스를 생성합니다.
    """
    try:
        import chromadb
        from chromadb.config import Settings
        
        if persist_directory is None:
            persist_directory = str(VECTOR_DB_DIR / "chroma_db")
        
        # 기존 폴더 삭제
        chroma_path = Path(persist_directory)
        if chroma_path.exists():
            shutil.rmtree(str(chroma_path))
            print(f"   기존 ChromaDB 삭제 완료")
        
        print(f"📦 ChromaDB 생성 중: {persist_directory}")
        
        # ChromaDB 클라이언트 생성 (새 설정)
        settings = Settings(
            anonymized_telemetry=False,
            allow_reset=True
        )
        client = chromadb.PersistentClient(path=persist_directory, settings=settings)
        
        # 기존 컬렉션 삭제 후 재생성
        try:
            client.delete_collection(name=collection_name)
        except:
            pass
        
        collection = client.create_collection(
            name=collection_name,
            metadata={"description": "사회문화 교과서 벡터 DB"}
        )
        
        # 데이터 준비
        ids = [f"chunk_{chunk['global_chunk_id']}" for chunk in chunks]
        documents = [chunk['text'] for chunk in chunks]
        metadatas = [
            {
                "chunk_id": int(chunk.get('chunk_id', 0)),
                "global_chunk_id": int(chunk.get('global_chunk_id', 0)),
                "page_number": int(chunk.get('page_number', 0)),
                "char_count": int(chunk.get('char_count', 0))
            }
            for chunk in chunks
        ]
        
        # 배치로 추가
        batch_size = 100
        for i in range(0, len(ids), batch_size):
            end_idx = min(i + batch_size, len(ids))
            collection.add(
                ids=ids[i:end_idx],
                embeddings=embeddings[i:end_idx].tolist(),
                documents=documents[i:end_idx],
                metadatas=metadatas[i:end_idx]
            )
            if (i + batch_size) % 500 == 0:
                print(f"   ⏳ {end_idx}/{len(ids)} 청크 추가 완료")
        
        print(f"✅ ChromaDB 저장 완료!")
        print(f"   - 컬렉션: {collection_name}")
        print(f"   - 총 문서 수: {collection.count()}")
        return True
        
    except Exception as e:
        print(f"⚠️ ChromaDB 생성 실패: {e}")
        return False


def build_faiss_index(
    embeddings: np.ndarray,
    index_path: str = None
) -> bool:
    """
    FAISS를 사용하여 벡터 인덱스를 생성합니다.
    한글 경로 문제를 우회하기 위해 임시 폴더 사용
    """
    try:
        import faiss
        
        if index_path is None:
            index_path = str(VECTOR_DB_DIR / "faiss_index.bin")
        
        print(f"📦 FAISS 인덱스 생성 중...")
        
        # 벡터 차원
        dimension = embeddings.shape[1]
        
        # L2 거리 기반 인덱스 생성
        index = faiss.IndexFlatL2(dimension)
        
        # 벡터 추가
        index.add(embeddings.astype('float32'))
        
        # 한글 경로 문제 우회: 임시 파일에 저장 후 복사
        try:
            # 직접 저장 시도
            faiss.write_index(index, index_path)
            print(f"✅ FAISS 인덱스 저장 완료!")
        except:
            # 임시 폴더 사용
            with tempfile.NamedTemporaryFile(delete=False, suffix='.bin') as tmp:
                tmp_path = tmp.name
            
            faiss.write_index(index, tmp_path)
            shutil.copy(tmp_path, index_path)
            os.remove(tmp_path)
            print(f"✅ FAISS 인덱스 저장 완료! (임시 경로 사용)")
        
        print(f"   - 경로: {index_path}")
        print(f"   - 벡터 수: {index.ntotal}")
        print(f"   - 차원: {dimension}")
        return True
        
    except Exception as e:
        print(f"⚠️ FAISS 인덱스 생성 실패: {e}")
        return False


def save_embeddings_numpy(
    embeddings: np.ndarray,
    chunks: List[Dict],
    output_dir: str = None
) -> None:
    """
    임베딩과 메타데이터를 NumPy/JSON 형식으로 저장합니다.
    """
    if output_dir is None:
        output_dir = str(VECTOR_DB_DIR)
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 임베딩 저장
    embeddings_path = output_path / "embeddings.npy"
    np.save(str(embeddings_path), embeddings)
    print(f"💾 임베딩 저장: {embeddings_path}")
    
    # 메타데이터 저장
    metadata = {
        "total_chunks": len(chunks),
        "embedding_dim": embeddings.shape[1],
        "embedding_model": EMBEDDING_MODEL,
        "chunks_info": [
            {
                "id": i,
                "global_chunk_id": chunk.get('global_chunk_id', i),
                "page_number": chunk.get('page_number', 0),
                "char_count": chunk.get('char_count', 0),
                "text_preview": chunk['text'][:100] + "..." if len(chunk['text']) > 100 else chunk['text']
            }
            for i, chunk in enumerate(chunks)
        ]
    }
    
    metadata_path = output_path / "embeddings_metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    print(f"💾 메타데이터 저장: {metadata_path}")


def process_chunks_file(chunks_path: str, use_faiss: bool = True, use_chroma: bool = True) -> None:
    """
    청크 파일을 처리하여 임베딩 및 벡터 DB를 생성합니다.
    """
    chunks_file = Path(chunks_path)
    
    if not chunks_file.exists():
        print(f"❌ 파일을 찾을 수 없습니다: {chunks_path}")
        return
    
    print(f"\n{'='*60}")
    print(f"📄 처리 중: {chunks_file.name}")
    print(f"{'='*60}")
    
    # 청크 로드
    chunks = load_chunks(str(chunks_file))
    print(f"📖 {len(chunks)}개 청크 로드 완료")
    
    # 텍스트 추출
    texts = [chunk['text'] for chunk in chunks]
    
    # 임베딩 생성
    embeddings = create_embeddings(texts)
    
    # 출력 디렉토리 생성
    VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)
    
    # NumPy 형식으로 저장 (항상)
    save_embeddings_numpy(embeddings, chunks)
    
    # ChromaDB 생성
    chroma_success = False
    if use_chroma:
        chroma_success = build_chroma_db(chunks, embeddings)
    
    # FAISS 인덱스 생성
    faiss_success = False
    if use_faiss:
        faiss_success = build_faiss_index(embeddings)
    
    print(f"\n✅ {chunks_file.name} 임베딩 완료!")
    print(f"   - NumPy: ✅")
    print(f"   - ChromaDB: {'✅' if chroma_success else '❌'}")
    print(f"   - FAISS: {'✅' if faiss_success else '❌'}")


def process_all_chunks() -> None:
    """
    data/chunks/ 디렉토리의 모든 청크 파일을 처리합니다.
    """
    chunks_files = list(CHUNKS_DIR.glob("*_chunks.json"))
    
    if not chunks_files:
        print("⚠️ 처리할 청크 파일이 없습니다.")
        print(f"   먼저 chunking.py를 실행하여 텍스트를 청킹하세요.")
        return
    
    print(f"\n🔍 발견된 청크 파일: {len(chunks_files)}개")
    for f in chunks_files:
        print(f"   - {f.name}")
    
    for chunks_file in chunks_files:
        process_chunks_file(str(chunks_file))
    
    print(f"\n✅ 모든 파일 임베딩 완료!")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 임베딩 및 벡터DB 생성 시작")
    print(f"   - 임베딩 모델: {EMBEDDING_MODEL}")
    print("="*60)
    
    if len(sys.argv) > 1:
        # 특정 파일 처리
        chunks_path = sys.argv[1]
        process_chunks_file(chunks_path)
    else:
        # 모든 청크 파일 처리
        process_all_chunks()
    
    print("\n" + "="*60)
    print("🎉 임베딩 및 벡터DB 생성 완료!")
    print(f"📁 결과 저장 위치: {VECTOR_DB_DIR}")
    print("="*60 + "\n")

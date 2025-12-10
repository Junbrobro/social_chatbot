"""본문 + 해설 청크를 합쳐서 벡터DB 빌드"""
import sys
sys.path.insert(0, 'src')

import json
import numpy as np
from pathlib import Path

DATA_DIR = Path("data")
CHUNKS_DIR = DATA_DIR / "chunks"
VECTOR_DB_DIR = DATA_DIR / "vector_db"

print("="*60)
print("🔄 본문 + 해설 통합 벡터DB 빌드")
print("="*60)

# 1. 모든 청크 로드 및 합치기
all_chunks = []
chunk_files = list(CHUNKS_DIR.glob("*_chunks.json"))

print(f"\n📖 청크 파일 로드 중...")
for chunk_file in chunk_files:
    print(f"   - {chunk_file.name}")
    with open(chunk_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    chunks = data.get('chunks', [])
    
    # 소스 파일 정보 추가
    source = chunk_file.stem.replace('_chunks', '')
    for chunk in chunks:
        chunk['source_file'] = source
    
    all_chunks.extend(chunks)

print(f"\n✅ 총 {len(all_chunks)}개 청크 로드 완료!")

# 2. global_chunk_id 재할당
for i, chunk in enumerate(all_chunks):
    chunk['global_chunk_id'] = i

# 3. 임베딩 생성
print(f"\n🤖 임베딩 생성 중...")
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("jhgan/ko-sroberta-multitask")
texts = [chunk['text'] for chunk in all_chunks]
embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

print(f"✅ 임베딩 완료! shape: {embeddings.shape}")

# 4. NumPy 저장
VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)
np.save(str(VECTOR_DB_DIR / "embeddings.npy"), embeddings)
print(f"💾 NumPy 임베딩 저장 완료")

# 5. 메타데이터 저장
metadata = {
    "total_chunks": len(all_chunks),
    "embedding_dim": embeddings.shape[1],
    "model": "jhgan/ko-sroberta-multitask",
    "chunks": all_chunks
}
with open(VECTOR_DB_DIR / "embeddings_metadata.json", 'w', encoding='utf-8') as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)
print(f"💾 메타데이터 저장 완료")

# 6. FAISS 인덱스 생성
print(f"\n📦 FAISS 인덱스 생성 중...")
import faiss

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings.astype('float32'))
faiss.write_index(index, str(VECTOR_DB_DIR / "faiss_index.bin"))

print(f"✅ FAISS 인덱스 저장 완료!")
print(f"   - 벡터 수: {index.ntotal}")
print(f"   - 차원: {dimension}")

# 7. 통합 청크 파일 저장
combined_chunks_path = CHUNKS_DIR / "combined_all_chunks.json"
combined_data = {
    "metadata": {
        "sources": [f.stem for f in chunk_files],
        "total_chunks": len(all_chunks)
    },
    "chunks": all_chunks
}
with open(combined_chunks_path, 'w', encoding='utf-8') as f:
    json.dump(combined_data, f, ensure_ascii=False, indent=2)
print(f"💾 통합 청크 파일 저장: {combined_chunks_path}")

print("\n" + "="*60)
print("🎉 통합 벡터DB 빌드 완료!")
print(f"   - 총 청크: {len(all_chunks)}개")
print(f"   - 본문: 1,130개 + 해설: 349개 = {len(all_chunks)}개")
print("="*60)






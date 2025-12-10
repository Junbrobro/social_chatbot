"""
쿼리 임베딩 생성 모듈
- user query → embedding vector 형태로 변환
"""

from sentence_transformers import SentenceTransformer
from typing import List, Union
import numpy as np

# 임베딩 모델 (싱글톤)
_embedding_model = None
EMBEDDING_MODEL_NAME = "jhgan/ko-sroberta-multitask"


def get_embedding_model() -> SentenceTransformer:
    """
    임베딩 모델 싱글톤 인스턴스를 반환합니다.
    """
    global _embedding_model
    
    if _embedding_model is None:
        print(f"🤖 임베딩 모델 로드 중: {EMBEDDING_MODEL_NAME}")
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    
    return _embedding_model


def embed_text(text: str) -> np.ndarray:
    """
    단일 텍스트를 임베딩합니다.
    
    Args:
        text: 임베딩할 텍스트
        
    Returns:
        임베딩 벡터 (numpy array)
    """
    model = get_embedding_model()
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding


def embed_texts(texts: List[str], show_progress: bool = False) -> np.ndarray:
    """
    여러 텍스트를 임베딩합니다.
    
    Args:
        texts: 임베딩할 텍스트 리스트
        show_progress: 진행률 표시 여부
        
    Returns:
        임베딩 벡터 배열 (N x embedding_dim)
    """
    model = get_embedding_model()
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=show_progress
    )
    return embeddings


def embed_query(query: str) -> List[float]:
    """
    쿼리를 임베딩하고 리스트로 반환합니다.
    (ChromaDB 호환용)
    
    Args:
        query: 검색 쿼리
        
    Returns:
        임베딩 벡터 (list)
    """
    embedding = embed_text(query)
    return embedding.tolist()


def compute_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    """
    두 임베딩 간의 코사인 유사도를 계산합니다.
    
    Args:
        embedding1: 첫 번째 임베딩
        embedding2: 두 번째 임베딩
        
    Returns:
        코사인 유사도 (0~1)
    """
    dot_product = np.dot(embedding1, embedding2)
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return dot_product / (norm1 * norm2)


if __name__ == "__main__":
    # 테스트
    print("\n" + "="*60)
    print("🔤 임베딩 모듈 테스트")
    print("="*60)
    
    test_texts = [
        "사회화는 개인이 사회 구성원으로서 필요한 가치와 규범을 학습하는 과정이다.",
        "문화는 한 사회의 구성원들이 공유하는 생활 양식의 총체이다."
    ]
    
    for text in test_texts:
        embedding = embed_text(text)
        print(f"\n📝 텍스트: {text[:30]}...")
        print(f"   임베딩 shape: {embedding.shape}")
        print(f"   임베딩 샘플: {embedding[:5]}...")
    
    # 유사도 계산
    emb1 = embed_text(test_texts[0])
    emb2 = embed_text(test_texts[1])
    similarity = compute_similarity(emb1, emb2)
    print(f"\n🔗 두 텍스트 간 유사도: {similarity:.4f}")
    
    print("\n✅ 임베딩 모듈 테스트 완료!")



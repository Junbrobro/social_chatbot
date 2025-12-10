"""
최종 검색 파이프라인
- Query → embedding → 벡터 검색 → 문서 반환
- Coarse 검색 + Fine 재랭킹 지원
"""

from typing import List, Dict, Optional, Tuple
from pathlib import Path
import sys

# 프로젝트 경로 추가
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from search_model_setup import SearchModel, get_search_model
from embedding import embed_text, compute_similarity
import numpy as np


class Retriever:
    """
    RAG 검색 파이프라인 클래스
    """
    
    def __init__(self, collection_name: str = "social_culture"):
        """
        검색기를 초기화합니다.
        """
        self.search_model = get_search_model(collection_name)
    
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        rerank: bool = False
    ) -> List[Dict]:
        """
        쿼리에 대해 관련 문서를 검색합니다.
        
        Args:
            query: 검색 쿼리
            top_k: 반환할 문서 수
            rerank: 재랭킹 적용 여부
            
        Returns:
            검색 결과 리스트
        """
        # 1차 검색 (Coarse retrieval)
        if rerank:
            # 재랭킹 시 더 많은 후보 검색
            initial_results = self.search_model.search(query, top_k=top_k * 3)
            # 2차 재랭킹 (Fine reranking)
            results = self._rerank(query, initial_results, top_k)
        else:
            results = self.search_model.search(query, top_k=top_k)
        
        return results
    
    def _rerank(
        self,
        query: str,
        candidates: List[Dict],
        top_k: int
    ) -> List[Dict]:
        """
        검색 결과를 재랭킹합니다.
        쿼리와 문서 간의 코사인 유사도를 직접 계산하여 순위를 조정합니다.
        """
        query_embedding = embed_text(query)
        
        for candidate in candidates:
            doc_embedding = embed_text(candidate['text'])
            candidate['rerank_score'] = compute_similarity(query_embedding, doc_embedding)
        
        # 재랭킹 점수로 정렬
        reranked = sorted(candidates, key=lambda x: x['rerank_score'], reverse=True)
        
        # 순위 재설정
        for i, result in enumerate(reranked[:top_k]):
            result['rank'] = i + 1
        
        return reranked[:top_k]
    
    def retrieve_with_context(
        self,
        query: str,
        top_k: int = 5,
        context_window: int = 0
    ) -> Tuple[List[Dict], str]:
        """
        검색 결과와 함께 컨텍스트 문자열을 반환합니다.
        
        Args:
            query: 검색 쿼리
            top_k: 반환할 문서 수
            context_window: 앞뒤 문맥 포함 범위 (현재 미사용)
            
        Returns:
            (검색 결과 리스트, 컨텍스트 문자열)
        """
        results = self.retrieve(query, top_k=top_k)
        
        # 컨텍스트 문자열 생성
        context_parts = []
        for i, result in enumerate(results):
            page = result['metadata'].get('page_number', 'N/A')
            text = result['text']
            context_parts.append(f"[문서 {i+1}] (페이지 {page})\n{text}")
        
        context = "\n\n---\n\n".join(context_parts)
        
        return results, context


def get_retriever(collection_name: str = "social_culture") -> Retriever:
    """
    검색기 인스턴스를 반환합니다.
    """
    return Retriever(collection_name=collection_name)


def retrieve_documents(
    query: str,
    top_k: int = 5,
    rerank: bool = False
) -> List[Dict]:
    """
    간편하게 문서를 검색하는 함수
    """
    retriever = get_retriever()
    return retriever.retrieve(query, top_k=top_k, rerank=rerank)


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🔍 검색 파이프라인 테스트")
    print("="*60)
    
    retriever = get_retriever()
    
    test_queries = [
        "사회화의 정의와 유형",
        "문화 상대주의란?"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"🔎 쿼리: {query}")
        print("="*60)
        
        results, context = retriever.retrieve_with_context(query, top_k=3)
        
        print(f"\n📚 검색 결과 ({len(results)}개):")
        for result in results:
            print(f"\n[{result['rank']}위] 유사도: {result['similarity']:.4f}")
            print(f"   페이지: {result['metadata'].get('page_number', 'N/A')}")
            text_preview = result['text'][:100] + "..." if len(result['text']) > 100 else result['text']
            print(f"   내용: {text_preview}")
    
    print("\n" + "="*60)
    print("✅ 검색 파이프라인 테스트 완료!")
    print("="*60 + "\n")



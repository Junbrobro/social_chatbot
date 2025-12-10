"""
챗봇 메인 로직 (STEP 6-2)
- 검색 + LLM 답변까지 전체 파이프라인 연결
- CLI 및 API 인터페이스 제공
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional

# 프로젝트 경로 추가
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from retrieval import Retriever, get_retriever
from prompt import create_rag_prompt, create_context_from_results, create_chat_messages, format_answer
from llmmodel import get_llm, BaseLLM


class SocialCultureChatbot:
    """
    사회문화 교과서 기반 RAG 챗봇
    """
    
    def __init__(
        self,
        llm_provider: str = "simple",
        collection_name: str = "social_culture",
        top_k: int = 5,
        **llm_kwargs
    ):
        """
        챗봇을 초기화합니다.
        
        Args:
            llm_provider: LLM 제공자 ("simple", "ollama", "openai", "huggingface")
            collection_name: 벡터 DB 컬렉션 이름
            top_k: 검색할 문서 수
            **llm_kwargs: LLM 추가 설정
        """
        print("\n" + "="*60)
        print("🤖 사회문화 챗봇 초기화 중...")
        print("="*60)
        
        # 검색기 초기화
        print("\n📚 검색 모델 로드 중...")
        self.retriever = get_retriever(collection_name)
        self.top_k = top_k
        
        # LLM 초기화
        print(f"\n🧠 LLM 로드 중 (provider: {llm_provider})...")
        self.llm = get_llm(llm_provider, **llm_kwargs)
        
        # 대화 기록
        self.chat_history: List[Dict] = []
        
        print("\n✅ 챗봇 초기화 완료!")
        print("="*60 + "\n")
    
    def ask(
        self,
        question: str,
        use_history: bool = True,
        show_sources: bool = True
    ) -> str:
        """
        질문에 답변합니다.
        
        Args:
            question: 사용자 질문
            use_history: 대화 기록 사용 여부
            show_sources: 출처 표시 여부
            
        Returns:
            챗봇 답변
        """
        # 1. 관련 문서 검색
        results, context = self.retriever.retrieve_with_context(
            question, 
            top_k=self.top_k
        )
        
        # 2. 프롬프트 생성
        if use_history and self.chat_history:
            messages = create_chat_messages(
                question, 
                context, 
                self.chat_history
            )
            answer = self.llm.chat(messages)
        else:
            prompt = create_rag_prompt(question, context)
            answer = self.llm.generate(prompt)
        
        # 3. 대화 기록 업데이트
        self.chat_history.append({"role": "user", "content": question})
        self.chat_history.append({"role": "assistant", "content": answer})
        
        # 최근 10개 메시지만 유지
        if len(self.chat_history) > 10:
            self.chat_history = self.chat_history[-10:]
        
        # 4. 답변 포맷팅
        if show_sources:
            answer = format_answer(answer, results)
        
        return answer
    
    def search_only(self, query: str, top_k: int = None) -> List[Dict]:
        """
        검색만 수행합니다.
        
        Args:
            query: 검색 쿼리
            top_k: 반환할 문서 수
            
        Returns:
            검색 결과 리스트
        """
        k = top_k or self.top_k
        return self.retriever.retrieve(query, top_k=k)
    
    def clear_history(self):
        """대화 기록을 초기화합니다."""
        self.chat_history = []
        print("🗑️ 대화 기록이 초기화되었습니다.")
    
    def get_history(self) -> List[Dict]:
        """대화 기록을 반환합니다."""
        return self.chat_history


def run_cli_chatbot(llm_provider: str = "simple"):
    """
    CLI 기반 챗봇을 실행합니다.
    """
    print("\n" + "="*60)
    print("📚 사회문화 교과서 RAG 챗봇")
    print("="*60)
    print("\n명령어:")
    print("  /quit, /exit  - 종료")
    print("  /clear        - 대화 기록 초기화")
    print("  /search <쿼리> - 검색만 수행")
    print("  /help         - 도움말")
    print("\n" + "-"*60)
    
    # 챗봇 초기화
    chatbot = SocialCultureChatbot(llm_provider=llm_provider)
    
    while True:
        try:
            # 사용자 입력
            user_input = input("\n👤 질문: ").strip()
            
            if not user_input:
                continue
            
            # 명령어 처리
            if user_input.lower() in ["/quit", "/exit", "종료", "exit", "quit"]:
                print("\n👋 챗봇을 종료합니다. 안녕히 가세요!")
                break
            
            elif user_input.lower() == "/clear":
                chatbot.clear_history()
                continue
            
            elif user_input.lower() == "/help":
                print("\n📖 사용 방법:")
                print("  - 사회문화 관련 질문을 입력하세요")
                print("  - 예: '사회화란 무엇인가요?'")
                print("  - 예: '문화의 특성을 설명해주세요'")
                continue
            
            elif user_input.lower().startswith("/search "):
                query = user_input[8:].strip()
                if query:
                    print("\n🔍 검색 결과:")
                    results = chatbot.search_only(query, top_k=3)
                    for r in results:
                        print(f"\n[{r['rank']}위] 유사도: {r['similarity']:.4f}")
                        print(f"   페이지: {r['metadata'].get('page_number', 'N/A')}")
                        text = r['text'][:150] + "..." if len(r['text']) > 150 else r['text']
                        print(f"   내용: {text}")
                continue
            
            # 질문 처리
            print("\n🤖 답변 생성 중...")
            answer = chatbot.ask(user_input)
            print(f"\n🤖 답변:\n{answer}")
            
        except KeyboardInterrupt:
            print("\n\n👋 챗봇을 종료합니다.")
            break
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")


def get_chatbot(
    llm_provider: str = "simple",
    **kwargs
) -> SocialCultureChatbot:
    """
    챗봇 인스턴스를 반환합니다.
    """
    return SocialCultureChatbot(llm_provider=llm_provider, **kwargs)


if __name__ == "__main__":
    # CLI 모드로 실행
    import argparse
    
    parser = argparse.ArgumentParser(description="사회문화 교과서 RAG 챗봇")
    parser.add_argument(
        "--llm",
        type=str,
        default="simple",
        choices=["simple", "ollama", "openai", "huggingface"],
        help="LLM 제공자 선택"
    )
    
    args = parser.parse_args()
    
    run_cli_chatbot(llm_provider=args.llm)



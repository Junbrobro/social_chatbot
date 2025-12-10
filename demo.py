"""
사회문화 RAG 챗봇 데모 테스트
간단한 테스트용 스크립트
"""
import sys
sys.path.insert(0, 'src')

from chatbot import get_chatbot

def main():
    print("\n" + "="*60)
    print("📚 사회문화 RAG 챗봇 데모 테스트")
    print("="*60)
    
    # 챗봇 초기화
    print("\n🤖 챗봇 초기화 중...")
    chatbot = get_chatbot(llm_provider='groq')
    print("✅ 챗봇 준비 완료!\n")
    
    # 테스트 질문들
    test_questions = [
        "사회화란 무엇인가요?",
        "문화의 특성을 설명해주세요",
        "사회 계층화 현상이란?"
    ]
    
    print("="*60)
    print("💬 테스트 질문 시작")
    print("="*60 + "\n")
    
    for i, question in enumerate(test_questions, 1):
        print(f"[질문 {i}] {question}")
        print("-" * 60)
        
        # 답변 생성
        answer = chatbot.ask(question, show_sources=True)
        print(f"답변:\n{answer}")
        print("\n" + "="*60 + "\n")
    
    print("✅ 데모 테스트 완료!")

if __name__ == "__main__":
    main()

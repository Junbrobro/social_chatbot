"""
사회문화 RAG 챗봇 웹 데모
Gradio 6.x 완전 호환
"""
import sys
sys.path.insert(0, 'src')

import gradio as gr
import threading
from chatbot import get_chatbot

# 전역 챗봇 인스턴스
chatbot_instance = None
initialization_lock = threading.Lock()
initialization_started = False

def initialize_chatbot():
    """챗봇 초기화 (스레드 안전)"""
    global chatbot_instance, initialization_started
    
    if chatbot_instance is not None:
        return chatbot_instance
    
    with initialization_lock:
        # 이중 체크 (다른 스레드가 이미 초기화했을 수 있음)
        if chatbot_instance is not None:
            return chatbot_instance
        
        if not initialization_started:
            initialization_started = True
            print("🤖 챗봇 초기화 시작...")
            chatbot_instance = get_chatbot(llm_provider='groq')
            print("✅ 챗봇 준비 완료!")
        else:
            # 다른 스레드가 초기화 중이면 대기
            while chatbot_instance is None:
                import time
                time.sleep(0.1)
    
    return chatbot_instance

def preload_chatbot():
    """백그라운드에서 챗봇 미리 로드"""
    try:
        initialize_chatbot()
    except Exception as e:
        print(f"⚠️ 백그라운드 초기화 실패: {e}")

def respond(message, history):
    """채팅 응답 함수"""
    if not message.strip():
        return ""
    
    bot = initialize_chatbot()
    response = bot.ask(message, show_sources=True)  # 출처 정보 포함
    return response

def search_documents(query):
    """문서 검색"""
    if not query.strip():
        return "검색어를 입력해주세요."
    
    bot = initialize_chatbot()
    results = bot.search_only(query, top_k=5)
    
    output = f"### 🔍 '{query}' 검색 결과\n\n"
    for r in results:
        page = r['metadata'].get('page_number', 'N/A')
        similarity = r.get('similarity', 0)
        text = r['text'][:200] + "..." if len(r['text']) > 200 else r['text']
        output += f"---\n**[{r['rank']}위]** 페이지 {page} | 유사도: {similarity:.3f}\n\n{text}\n\n"
    
    return output

# 메인 채팅 인터페이스
demo = gr.ChatInterface(
    fn=respond,
    title="📚 사회문화 RAG 챗봇",
    description="**2026학년도 수능특강 사회문화** 교재 기반 질문-답변 시스템\n\n💡 사회문화 관련 질문을 입력하면 교재 내용을 바탕으로 답변합니다.\n\n🛠️ 임베딩: ko-sroberta | LLM: Ollama gemma3:4b | 청크: 1,479개",
    examples=[
        "사회화란 무엇인가요?",
        "문화의 특성을 설명해주세요",
        "사회 계층화 현상이란?",
        "일탈 행동의 원인은 무엇인가요?",
        "문화 상대주의란 무엇인가요?"
    ]
)

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 사회문화 RAG 챗봇 웹 데모 시작")
    print("="*50)
    print("\n브라우저에서 http://localhost:7860 접속하세요!\n")
    
    # 백그라운드에서 챗봇 미리 로드 시작
    print("⏳ 백그라운드에서 챗봇 초기화 시작 중...")
    init_thread = threading.Thread(target=preload_chatbot, daemon=True)
    init_thread.start()
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True  # 공개 URL 생성 (72시간 유효)
    )

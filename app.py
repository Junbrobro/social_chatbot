"""
Hugging Face Spaces 배포용 앱
web_demo.py와 동일하지만 Spaces 환경에 맞게 최적화
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
        if chatbot_instance is not None:
            return chatbot_instance
        
        if not initialization_started:
            initialization_started = True
            print("🤖 챗봇 초기화 시작...")
            chatbot_instance = get_chatbot(llm_provider='groq')
            print("✅ 챗봇 준비 완료!")
        else:
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
    response = bot.ask(message, show_sources=True)
    return response

# 메인 채팅 인터페이스
demo = gr.ChatInterface(
    fn=respond,
    title="📚 사회문화 RAG 챗봇",
    description="**2026학년도 수능특강 사회문화** 교재 기반 질문-답변 시스템\n\n💡 사회문화 관련 질문을 입력하면 교재 내용을 바탕으로 답변합니다.\n\n🛠️ 임베딩: ko-sroberta | LLM: Groq (llama-3.1-8b) | 청크: 1,479개",
    examples=[
        "사회화란 무엇인가요?",
        "문화의 특성을 설명해주세요",
        "사회 계층화 현상이란?",
        "일탈 행동의 원인은 무엇인가요?",
        "문화 상대주의란 무엇인가요?"
    ]
)

# 백그라운드에서 챗봇 미리 로드 시작
print("⏳ 백그라운드에서 챗봇 초기화 시작 중...")
init_thread = threading.Thread(target=preload_chatbot, daemon=True)
init_thread.start()

# Hugging Face Spaces는 자동으로 app을 실행
if __name__ == "__main__":
    demo.launch()





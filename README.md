# 📚 사회문화 RAG 챗봇

2026학년도 수능특강 사회문화 교재 기반 질문-답변 시스템

## 🎯 프로젝트 소개

이 프로젝트는 RAG (Retrieval-Augmented Generation) 기술을 활용하여 사회문화 교과서 내용을 기반으로 질문에 답변하는 챗봇입니다.

### 주요 기능
- 📖 PDF 교재 텍스트 추출 및 청킹
- 🔍 벡터 검색 기반 문서 검색
- 💬 LLM을 활용한 자연어 답변 생성
- 📄 출처 정보 제공 (문서명, 페이지 번호)

## 🛠️ 기술 스택

- **임베딩 모델**: `jhgan/ko-sroberta-multitask`
- **벡터 DB**: FAISS, ChromaDB
- **LLM**: Groq (llama-3.1-8b-instant), Ollama, OpenAI, Gemini 등 지원
- **웹 인터페이스**: Gradio

## 📦 설치 방법

### 1. 저장소 클론
```bash
git clone https://github.com/[사용자명]/social_chatbot.git
cd social_chatbot
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정
```bash
# Windows (PowerShell)
$env:GROQ_API_KEY="your-api-key"

# Linux/Mac
export GROQ_API_KEY="your-api-key"
```

## 🚀 사용 방법

### 방법 1: Hugging Face Spaces (가장 간단! 추천!) ⭐

**배포 후 URL만 공유하면 끝!** 별도 설정 불필요

1. 배포 완료 후 Space URL 접속
2. 질문 입력
3. 답변 확인

📖 배포 방법: [SIMPLE_DEPLOY.md](SIMPLE_DEPLOY.md)

### 방법 2: GitHub Codespaces (개발/테스트용) 🌟

**가장 쉬운 방법!** GitHub에서 바로 실행할 수 있습니다.

1. **Codespace 생성**
   - 저장소 페이지에서 **"Code"** 버튼 클릭
   - **"Codespaces"** 탭 선택
   - **"Create codespace on main"** 클릭
   - Codespace가 자동으로 생성되고 의존성이 설치됩니다

2. **환경 변수 설정**
   ```bash
   export GROQ_API_KEY="your-api-key-here"
   ```

3. **웹 데모 실행**
   ```bash
   python web_demo.py
   ```

4. **접속**
   - Codespace가 자동으로 포트를 포워딩합니다
   - 포트 탭에서 "Open in Browser" 클릭하거나
   - 터미널에 표시된 URL 클릭

### 방법 2: 로컬 실행
```bash
python web_demo.py
```

브라우저에서 `http://localhost:7860` 접속

### 방법 3: 데모 테스트
```bash
python demo.py
```

## 📁 프로젝트 구조

```
social_chatbot/
├── src/                    # 소스 코드
│   ├── chatbot.py         # 챗봇 메인 로직
│   ├── llmmodel.py        # LLM 모델 클래스
│   ├── search_model_setup.py  # 벡터 검색 모델
│   ├── prompt.py          # 프롬프트 관리
│   └── ...
├── data/                   # 데이터 파일
│   ├── chunks/            # 텍스트 청크
│   └── vector_db/         # 벡터 데이터베이스
├── web_demo.py            # 웹 데모 (Gradio)
├── app.py                 # Hugging Face Spaces 배포용
└── requirements.txt       # 의존성 목록
```

## 🌐 배포 및 공유 (가장 간단한 방법!)

### ⭐ Hugging Face Spaces (추천! 가장 쉬움!)

**3단계로 끝!** 클릭 몇 번으로 배포 완료

1. **Space 생성**: https://huggingface.co/spaces → "New Space"
2. **GitHub 연결**: 저장소 연결 (`Junbrobro/social_chatbot`)
3. **API 키 설정**: Settings → Secrets → `GROQ_API_KEY` 추가

**완료!** URL만 공유하면 누구나 바로 사용 가능!

📖 **자세한 가이드**: [SIMPLE_DEPLOY.md](SIMPLE_DEPLOY.md) (5분 완성!)

### GitHub Codespaces (개발/테스트용)
- 저장소를 클론할 필요 없이 브라우저에서 바로 실행
- 무료 플랜: 월 60시간 제공
- 자세한 방법은 위의 "사용 방법" 참고

## 📝 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.

## 🤝 기여

이슈 및 풀 리퀘스트 환영합니다!




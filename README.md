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

### 방법 : 로컬 실행
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
├── src/                           # 소스 코드
│   ├── chatbot.py                 # 챗봇 메인 로직
│   ├── llmmodel.py                # LLM 모델 클래스 (Groq, OpenAI, Gemini 등)
│   ├── search_model_setup.py      # 벡터 검색 모델 (FAISS, ChromaDB)
│   ├── prompt.py                  # 프롬프트 관리 및 답변 포맷팅
│   ├── chunking.py                # 텍스트 청킹
│   ├── embedding.py               # 임베딩 생성
│   ├── pdf_extracting.py          # PDF 텍스트 추출
│   ├── retrieval.py               # 검색 로직
│   ├── build_embeddings.py        # 벡터DB 빌드
│   └── utils/                     # 부가 유틸 함수 모음
├── data/                          # 데이터 파일
│   ├── chunks/                   # 텍스트 청크 JSON 파일
│   │   ├── 2026학년도_수능특강_사회문화_본문_chunks.json
│   │   ├── 2026학년도_수능특강_사회문화_해설_chunks.json
│   │   └── combined_all_chunks.json
│   ├── original/                 # (옵션) 원본/중간 데이터 저장
│   ├── text/                     # 추출된 텍스트/JSON
│   │   ├── 2026학년도_수능특강_사회문화_본문.json
│   │   ├── 2026학년도_수능특강_사회문화_본문.txt
│   │   ├── 2026학년도_수능특강_사회문화_해설.json
│   │   └── 2026학년도_수능특강_사회문화_해설.txt
│   ├── vector_db/                # 벡터 데이터베이스
│   │   ├── embeddings.npy        # 임베딩 벡터
│   │   ├── embeddings_metadata.json
│   │   ├── faiss_index.bin      # FAISS 인덱스
│   │   └── chroma_db/           # ChromaDB 데이터
│   │       ├── chroma.sqlite3
│   │       └── 2df0cbbe-.../    # Chroma 내부 인덱스 파일들
│   └── viz/                     # 임베딩 시각화 결과
│       ├── embeddings_pca_2d.png
│       ├── embeddings_pca_3d.png
│       ├── embeddings_3d_pca.html
│       └── reduced_embeddings_pca_3d.npy
├── web_demo.py                   # 로컬 웹 데모 실행 (Gradio, share=True)
├── app.py                        # Hugging Face Spaces 배포용
├── demo.py                       # 간단한 데모 테스트 (CLI)
├── build_combined.py             # 본문+해설 청크 통합 및 벡터DB 빌드
├── visualize_embeddings.py       # 임베딩 벡터 시각화 스크립트
├── notion_upload.py              # 노션 업로드 유틸 스크립트
├── NOTION_UPLOAD_GUIDE.md        # 노션 업로드 사용 가이드
├── requirements.txt              # Python 의존성 목록
├── env.example                   # 환경 변수 예시
├── 2026학년도_수능특강_사회문화_본문.pdf
├── 2026학년도_수능특강_사회문화_해설.pdf
├── 사회문화_교학사_교사용 교과서.pdf
├── 사회문화_미래엔_교사용 교과서.pdf
└── README.md                     # 프로젝트 설명서
```

### 🔎 요약 버전 (GitHub README용)

```text
social_chatbot/
├── src/                # 챗봇/RAG 핵심 로직
│   ├── chatbot.py
│   ├── llmmodel.py
│   ├── search_model_setup.py
│   ├── prompt.py
│   ├── chunking.py
│   ├── embedding.py
│   ├── pdf_extracting.py
│   ├── retrieval.py
│   └── build_embeddings.py
├── data/
│   ├── chunks/         # 청크된 본문·해설
│   ├── text/           # 추출 텍스트/JSON
│   ├── vector_db/      # FAISS/Chroma 벡터 DB
│   └── viz/            # 임베딩 시각화 결과
├── web_demo.py         # Gradio 웹 데모
├── app.py              # Hugging Face Spaces용
├── demo.py             # CLI 데모
├── build_combined.py   # 본문+해설 통합/임베딩
├── visualize_embeddings.py  # 임베딩 시각화
└── requirements.txt
```





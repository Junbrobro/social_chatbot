# 사회문화 챗봇 프로젝트 진행 상황

## 📁 프로젝트 정보
- **경로**: `C:\Projects\social_chatbot`
- **Python 환경**: `C:\Users\82103\anaconda3\python.exe`

## ✅ 완료된 작업

### STEP 1: PDF 텍스트 추출
- ✅ 2026학년도_수능특강_사회문화_본문.pdf
- ✅ 2026학년도_수능특강_사회문화_해설.pdf

### STEP 2: 청킹
- ✅ 본문: 1,130개 청크
- ✅ 해설: 349개 청크
- ✅ **총 1,479개 청크**

### STEP 3: 임베딩 + 벡터DB
- ✅ 통합 임베딩 완료 (1,479개, 768차원)
- ✅ FAISS 인덱스 저장 완료
- ✅ 통합 청크 파일: `data/chunks/combined_all_chunks.json`

### STEP 4: 3D 시각화
- ✅ `data/viz/embeddings_3d_pca.html`

### STEP 5: 검색 모델
- ✅ `src/search_model_setup.py` 준비됨
- ✅ FAISS 백엔드 사용

### STEP 6: LLM
- ✅ `src/llmmodel.py` - Ollama, OpenAI, Gemini, HuggingFace 지원
- ⏳ **Ollama llama3.2 모델 다운로드 필요**

## 🔜 다음 작업

### 1. Ollama 모델 다운로드
```powershell
ollama pull llama3.2
```
- Ollama 앱이 실행된 상태에서
- PowerShell 또는 명령 프롬프트에서 위 명령어 실행
- 안 되면 컴퓨터 재시작 후 다시 시도

### 2. 챗봇 테스트
```powershell
& "C:\Users\82103\anaconda3\python.exe" test_ollama.py
```

### 3. 웹 데모 제작
- Gradio 또는 Streamlit으로 웹 UI 제작

### 4. README.md 작성

## 💻 유용한 명령어

```powershell
# 챗봇 테스트 (Ollama)
& "C:\Users\82103\anaconda3\python.exe" test_ollama.py

# 전체 테스트
& "C:\Users\82103\anaconda3\python.exe" run_test.py

# Ollama 모델 목록 확인
ollama list

# Ollama 모델 다운로드
ollama pull llama3.2
```

## 📂 프로젝트 구조
```
social_chatbot/
├── data/
│   ├── text/           # 추출된 텍스트
│   ├── chunks/         # 청킹된 데이터 (1,479개)
│   ├── vector_db/      # FAISS 인덱스
│   └── viz/            # 3D 시각화
├── src/
│   ├── chatbot.py      # 챗봇 메인 로직
│   ├── llmmodel.py     # LLM 모듈
│   ├── retrieval.py    # 검색 파이프라인
│   └── ...
├── test_ollama.py      # Ollama 테스트
├── run_test.py         # 전체 테스트
└── build_combined.py   # 통합 빌드 스크립트
```

## ⚠️ 참고 사항
- ChromaDB는 오류 발생 → FAISS 사용 중
- Gemini API는 할당량 초과 오류 발생

---
마지막 업데이트: 2025-12-09

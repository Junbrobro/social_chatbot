# 🔍 Hugging Face Spaces - 탭 찾기 가이드

## "Files" 탭을 찾을 수 없을 때

### 방법 1: 상단 탭 메뉴 확인

Space 페이지 상단에 이런 탭들이 있습니다:
```
[App] [Files] [Settings] [Community]
```

- **"Files"** 탭 클릭
- 또는 **"Files and versions"** 탭 클릭

### 방법 2: 우측 상단 버튼

1. Space 페이지 우측 상단을 확인
2. **"+"** 또는 **"Add file"** 버튼 클릭
3. **"Connect repository"** 선택

### 방법 3: Settings에서 연결

1. **"Settings"** 탭 클릭
2. 좌측 메뉴 또는 페이지에서 **"Repository"** 섹션 찾기
3. **"Connect repository"** 또는 **"Sync from GitHub"** 클릭

### 방법 4: 직접 URL 접속

Space URL에 `/files` 추가:
```
https://huggingface.co/spaces/Junbrobro/social-culture-chatbot/files
```

---

## GitHub 연결이 안 될 때

### 대안: 파일 직접 업로드

GitHub 연결이 어렵다면 파일을 직접 업로드하세요:

1. **"Add file"** → **"Upload files"** 클릭
2. 다음 파일들을 드래그 앤 드롭:

**필수 파일:**
- `app.py`
- `requirements.txt`
- `README.md` (또는 `README_HF.md` 내용 복사)

**src 폴더:**
- `src/chatbot.py`
- `src/llmmodel.py`
- `src/search_model_setup.py`
- `src/prompt.py`
- `src/chunking.py`
- `src/embedding.py`
- `src/pdf_extracting.py`
- `src/retrieval.py`
- `src/build_embeddings.py`

**데이터 파일:**
- `data/chunks/combined_all_chunks.json`
- `data/vector_db/embeddings_metadata.json`
- `data/vector_db/embeddings.npy` (직접 업로드)
- `data/vector_db/faiss_index.bin` (직접 업로드)

---

## 여전히 안 되면?

1. **Space를 새로 만들기**
   - 기존 Space 삭제 후 다시 생성
   - Space 이름을 다르게 시도

2. **브라우저 확인**
   - 다른 브라우저로 시도
   - 캐시 삭제 후 다시 시도

3. **상세 가이드 참고**
   - `HF_DEPLOY_STEP_BY_STEP.md` 파일 확인


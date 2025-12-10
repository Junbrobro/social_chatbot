# 🚀 배포 가이드 (GitHub + Hugging Face Spaces)

## 1단계: GitHub에 업로드

### 1.1 GitHub 저장소 생성
1. https://github.com 접속
2. 우측 상단 "+" → "New repository" 클릭
3. 저장소 이름: `social_chatbot` (또는 원하는 이름)
4. Public 선택
5. "Create repository" 클릭

### 1.2 로컬에서 Git 초기화 및 업로드

```bash
# Git 초기화 (아직 안 했다면)
git init

# 원격 저장소 추가 (본인의 GitHub 저장소 URL로 변경)
git remote add origin https://github.com/[사용자명]/social_chatbot.git

# 파일 추가
git add .

# 커밋
git commit -m "Initial commit: Social Culture RAG Chatbot"

# 메인 브랜치로 푸시
git branch -M main
git push -u origin main
```

**중요**: `.gitignore` 파일이 있어서 큰 파일들(PDF, 벡터DB 등)은 업로드되지 않습니다.

---

## 2단계: Hugging Face Spaces에 배포

### 2.1 Hugging Face 계정 및 Space 생성
1. https://huggingface.co 접속 및 로그인 (또는 회원가입)
2. 우측 상단 프로필 → "New Space" 클릭
3. 설정:
   - **Space name**: `social-culture-chatbot` (또는 원하는 이름)
   - **SDK**: `Gradio` 선택
   - **Visibility**: `Public` 선택
4. "Create Space" 클릭

### 2.2 GitHub 저장소 연결 (방법 1 - 추천)

1. Space 페이지에서 "Files and versions" 탭 클릭
2. "Add file" → "Connect repository" 클릭
3. GitHub 계정 연결 (처음이면)
4. 저장소 선택: `[사용자명]/social_chatbot`
5. "Connect" 클릭
6. 자동으로 파일들이 업로드됩니다!

### 2.3 수동 업로드 (방법 2)

필요한 파일들을 직접 업로드:

**필수 파일:**
- `app.py` (메인 앱 파일)
- `requirements.txt` (의존성)
- `src/` 폴더 전체
- `data/chunks/combined_all_chunks.json` (청크 데이터)
- `data/vector_db/embeddings.npy` (임베딩 벡터)
- `data/vector_db/embeddings_metadata.json` (메타데이터)
- `data/vector_db/faiss_index.bin` (FAISS 인덱스)
- `README.md` 또는 `README_HF.md` (Space 설명)

**업로드 방법:**
1. Space 페이지에서 "Files and versions" 탭
2. "Add file" → "Upload files" 클릭
3. 파일 드래그 앤 드롭 또는 선택
4. 커밋 메시지 입력 후 "Upload files" 클릭

### 2.4 Secrets 설정 (API 키)

1. Space 페이지에서 "Settings" 탭 클릭
2. 좌측 메뉴에서 "Secrets" 클릭
3. "New secret" 클릭
4. 설정:
   - **Key**: `GROQ_API_KEY`
   - **Value**: 본인의 Groq API 키
5. "Add secret" 클릭

### 2.5 배포 확인

1. Space 페이지에서 "App" 탭 클릭
2. 빌드 로그 확인 (처음에는 5-10분 소요)
3. 빌드 완료 후 챗봇 사용 가능!

**접속 URL:**
```
https://huggingface.co/spaces/[사용자명]/social-culture-chatbot
```

---

## 3단계: 데이터 파일 업로드 (중요!)

### 문제: Git에 큰 파일 업로드 안 됨

`.gitignore`로 인해 벡터DB 파일들이 GitHub에 업로드되지 않습니다.

### 해결 방법:

#### 방법 1: Hugging Face Datasets 사용 (추천)

1. https://huggingface.co/datasets 접속
2. "New dataset" 클릭
3. 이름: `social-culture-vector-db`
4. 파일 업로드:
   - `data/vector_db/embeddings.npy`
   - `data/vector_db/embeddings_metadata.json`
   - `data/vector_db/faiss_index.bin`
   - `data/chunks/combined_all_chunks.json`

5. `app.py` 수정하여 Datasets에서 로드하도록 변경

#### 방법 2: Spaces에 직접 업로드

1. Space의 "Files and versions"에서 직접 업로드
2. `data/` 폴더 구조 유지

#### 방법 3: Git LFS 사용

```bash
# Git LFS 설치 (https://git-lfs.github.com)
git lfs install

# 큰 파일 추적
git lfs track "*.npy"
git lfs track "*.bin"
git lfs track "data/chunks/combined_all_chunks.json"

# 커밋 및 푸시
git add .gitattributes
git add data/
git commit -m "Add vector DB files with LFS"
git push
```

---

## 4단계: 업데이트 방법

### GitHub 업데이트 후 Spaces 자동 동기화

GitHub 저장소를 연결했다면:
1. 로컬에서 코드 수정
2. Git 커밋 및 푸시
3. Spaces가 자동으로 업데이트됨 (몇 분 소요)

### 수동 업데이트

1. Space의 "Files and versions"에서 파일 수정
2. 또는 "Add file" → "Upload files"로 새 파일 업로드

---

## ⚠️ 주의사항

1. **API 키 보안**: 절대 코드에 API 키를 하드코딩하지 마세요!
2. **파일 크기**: Hugging Face Spaces는 무료 플랜에서 50GB 제한
3. **빌드 시간**: 첫 배포는 10-15분 소요될 수 있습니다
4. **메모리**: 무료 플랜은 16GB RAM 제한

---

## 🐛 트러블슈팅

### 빌드 실패
- 로그 확인: Space 페이지 → "Logs" 탭
- `requirements.txt` 확인
- Python 버전 확인 (3.8 이상 필요)

### API 키 오류
- Secrets에 올바르게 설정되었는지 확인
- 환경 변수 이름 확인 (`GROQ_API_KEY`)

### 파일을 찾을 수 없음
- 파일 경로 확인
- `data/` 폴더 구조 확인

---

## ✅ 체크리스트

배포 전 확인:

- [ ] GitHub 저장소 생성 및 코드 업로드
- [ ] Hugging Face Space 생성
- [ ] `app.py` 파일 존재
- [ ] `requirements.txt` 파일 존재
- [ ] `src/` 폴더 전체 업로드
- [ ] 벡터DB 데이터 파일 업로드
- [ ] Secrets에 `GROQ_API_KEY` 설정
- [ ] README 파일 작성
- [ ] 빌드 성공 확인
- [ ] 챗봇 테스트 완료

---

## 🎉 완료!

배포가 완료되면 다른 사람들도 사용할 수 있습니다!

**공유 URL:**
```
https://huggingface.co/spaces/[사용자명]/social-culture-chatbot
```




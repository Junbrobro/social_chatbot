# 🚀 Hugging Face Spaces 배포 단계별 가이드

## ✅ 준비 완료된 항목
- ✅ GitHub 저장소 업로드 완료
- ✅ `app.py` 파일 준비 완료
- ✅ `requirements.txt` 준비 완료
- ✅ API 키 보호 처리 완료

## 📋 배포 단계

### 1단계: Hugging Face Space 생성

1. **Hugging Face 접속**
   - https://huggingface.co/spaces 접속
   - 로그인 (또는 회원가입)

2. **새 Space 생성**
   - 우측 상단 **"New Space"** 클릭
   - 설정 입력:
     - **Space name**: `social-culture-chatbot`
     - **SDK**: `Gradio` 선택
     - **Visibility**: `Public` 선택
   - **"Create Space"** 클릭

---

### 2단계: GitHub 저장소 연결

1. **Space 페이지에서**
   - **"Files and versions"** 탭 클릭

2. **저장소 연결**
   - **"Add file"** → **"Connect repository"** 클릭
   - GitHub 계정 연결 (처음이면 인증 필요)
   - 저장소 선택: `Junbrobro/social_chatbot`
   - **"Connect"** 클릭

3. **자동 동기화**
   - GitHub 저장소의 파일들이 자동으로 업로드됩니다
   - 몇 분 소요될 수 있습니다

---

### 3단계: README 파일 설정 (선택)

Hugging Face Spaces는 루트의 `README.md`를 자동으로 인식합니다.

**옵션 1: Space에서 직접 수정**
1. Space의 "Files and versions"에서 `README.md` 클릭
2. "Edit" 클릭
3. `README_HF.md`의 내용을 복사하여 붙여넣기
4. 저장

**옵션 2: GitHub에서 수정 후 동기화**
- GitHub 저장소에서 `README.md`를 `README_HF.md` 내용으로 업데이트
- Space가 자동으로 동기화됩니다

---

### 4단계: Secrets 설정 (필수!)

**API 키를 안전하게 설정합니다.**

1. **Space 설정으로 이동**
   - Space 페이지에서 **"Settings"** 탭 클릭
   - 좌측 메뉴에서 **"Secrets"** 클릭

2. **API 키 추가**
   - **"New secret"** 클릭
   - 설정:
     - **Key**: `GROQ_API_KEY`
     - **Value**: 본인의 Groq API 키 입력
   - **"Add secret"** 클릭

⚠️ **중요**: API 키는 절대 코드에 하드코딩하지 마세요!

---

### 5단계: 데이터 파일 확인

GitHub에 업로드된 데이터 파일:
- ✅ `data/chunks/combined_all_chunks.json` (청크 데이터)
- ✅ `data/vector_db/embeddings_metadata.json` (메타데이터)

**추가로 필요한 파일들** (용량이 커서 Git에 없을 수 있음):
- `data/vector_db/embeddings.npy` (임베딩 벡터)
- `data/vector_db/faiss_index.bin` (FAISS 인덱스)

**해결 방법**:
1. Space의 "Files and versions"에서 직접 업로드
2. 또는 Hugging Face Datasets 사용 (권장)

---

### 6단계: 빌드 확인

1. **Space 페이지에서**
   - **"App"** 탭 클릭
   - 빌드 로그 확인 (처음에는 5-10분 소요)

2. **빌드 완료 후**
   - 챗봇 인터페이스가 표시됩니다
   - 질문을 입력하여 테스트!

---

## 🔗 접속 URL

배포 완료 후 접속 URL:
```
https://huggingface.co/spaces/Junbrobro/social-culture-chatbot
```

(사용자명과 Space 이름에 따라 다를 수 있습니다)

---

## ⚠️ 트러블슈팅

### 빌드 실패
- **로그 확인**: Space → "Logs" 탭
- **원인 확인**: 
  - `requirements.txt` 의존성 문제
  - Python 버전 문제
  - 파일 경로 문제

### API 키 오류
- **Secrets 확인**: Settings → Secrets
- **환경 변수 이름**: `GROQ_API_KEY` (정확히 일치해야 함)

### 파일을 찾을 수 없음
- **경로 확인**: `data/` 폴더 구조 확인
- **파일 업로드**: 필요한 파일이 Space에 있는지 확인

### 메모리 부족
- Hugging Face Spaces 무료 플랜: 16GB RAM
- 임베딩 모델 로드 시 메모리 사용량 확인

---

## ✅ 체크리스트

배포 전 확인:
- [ ] Hugging Face Space 생성 완료
- [ ] GitHub 저장소 연결 완료
- [ ] Secrets에 `GROQ_API_KEY` 설정 완료
- [ ] 데이터 파일 업로드 확인
- [ ] 빌드 성공 확인
- [ ] 챗봇 테스트 완료

---

## 🎉 완료!

배포가 완료되면 다른 사람들도 사용할 수 있습니다!

**공유 URL을 다른 사람들에게 알려주세요!**


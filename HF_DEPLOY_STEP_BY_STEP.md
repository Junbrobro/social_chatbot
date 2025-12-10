# 🚀 Hugging Face Spaces 배포 - 단계별 상세 가이드

## 📍 1단계: Space 생성

### 1-1. Hugging Face 접속
1. 브라우저에서 https://huggingface.co 접속
2. 로그인 (또는 회원가입)

### 1-2. Spaces 페이지로 이동
1. 상단 메뉴에서 **"Spaces"** 클릭
   - 또는 직접 https://huggingface.co/spaces 접속

### 1-3. 새 Space 생성
1. 우측 상단의 **"New Space"** 버튼 클릭 (큰 파란색 버튼)
2. 다음 정보 입력:
   - **Space name**: `social-culture-chatbot`
   - **SDK**: 드롭다운에서 **"Gradio"** 선택
   - **Visibility**: **"Public"** 선택
3. **"Create Space"** 버튼 클릭

### 1-4. Space 생성 완료
- Space가 생성되면 자동으로 Space 페이지로 이동합니다
- URL 예시: `https://huggingface.co/spaces/Junbrobro/social-culture-chatbot`

---

## 📍 2단계: GitHub 저장소 연결

### 2-1. Space 페이지에서 파일 업로드 방법 찾기

**방법 A: 상단 탭 메뉴 사용**
1. Space 페이지 상단에 여러 탭이 있습니다:
   - **"App"** (기본)
   - **"Files"** 또는 **"Files and versions"** ← 여기!
   - **"Settings"**
   - **"Community"**
2. **"Files"** 또는 **"Files and versions"** 탭 클릭

**방법 B: 직접 찾기**
- Space 페이지에서 파일 목록이 보이는 곳을 찾습니다
- 또는 우측 상단의 **"+"** 버튼 클릭

### 2-2. GitHub 저장소 연결

**옵션 1: Connect repository (추천)**
1. **"Add file"** 버튼 클릭 (우측 상단 또는 파일 목록 위)
2. 드롭다운 메뉴에서 **"Connect repository"** 선택
3. GitHub 계정 연결:
   - 처음이면 "Connect GitHub" 클릭
   - GitHub 인증 진행
4. 저장소 선택:
   - `Junbrobro/social_chatbot` 선택
5. **"Connect"** 또는 **"Sync"** 클릭

**옵션 2: 파일 직접 업로드**
1. **"Add file"** → **"Upload files"** 클릭
2. 로컬 파일들을 드래그 앤 드롭
3. 필요한 파일들:
   - `app.py`
   - `requirements.txt`
   - `src/` 폴더 전체
   - `data/chunks/combined_all_chunks.json`
   - `data/vector_db/embeddings_metadata.json`

### 2-3. 연결 확인
- GitHub 저장소의 파일들이 Space에 나타나면 성공!
- 몇 분 소요될 수 있습니다

---

## 📍 3단계: API 키 설정 (Secrets)

### 3-1. Settings 페이지로 이동
1. Space 페이지 상단 탭에서 **"Settings"** 클릭
   - 또는 URL에 `/settings` 추가:
   - `https://huggingface.co/spaces/Junbrobro/social-culture-chatbot/settings`

### 3-2. Secrets 섹션 찾기
1. Settings 페이지에서 좌측 메뉴 또는 스크롤
2. **"Secrets"** 또는 **"Repository secrets"** 섹션 찾기
   - 보통 중간 부분에 있습니다

### 3-3. API 키 추가
1. **"New secret"** 또는 **"Add secret"** 버튼 클릭
2. 입력:
   - **Key**: `GROQ_API_KEY` (정확히 이대로!)
   - **Value**: 본인의 Groq API 키 입력
3. **"Add secret"** 또는 **"Save"** 클릭

---

## 📍 4단계: 데이터 파일 업로드 (중요!)

### 4-1. Files 탭으로 이동
- Space 페이지 → **"Files"** 탭

### 4-2. data 폴더 구조 만들기
1. **"Add file"** → **"Create a new file"** 클릭
2. 파일 경로 입력: `data/chunks/.gitkeep` (임시)
3. 저장 후 삭제해도 됩니다 (폴더 구조 생성용)

### 4-3. 데이터 파일 업로드
1. **"Add file"** → **"Upload files"** 클릭
2. 다음 파일들을 업로드:

**필수 파일:**
- `data/vector_db/embeddings.npy` (큰 파일, 시간 소요)
- `data/vector_db/faiss_index.bin` (큰 파일)
- `data/vector_db/embeddings_metadata.json` (이미 GitHub에 있으면 생략 가능)
- `data/chunks/combined_all_chunks.json` (이미 GitHub에 있으면 생략 가능)

**파일 위치:**
- 로컬: `C:\Projects\social_chatbot\data\vector_db\`

### 4-4. 업로드 확인
- Files 탭에서 파일들이 보이면 성공!

---

## 📍 5단계: 빌드 확인

### 5-1. App 탭으로 이동
1. Space 페이지 → **"App"** 탭 클릭
2. 빌드 로그 확인:
   - "Building..." 또는 진행 상황 표시
   - 처음 빌드는 5-10분 소요

### 5-2. 빌드 완료 확인
- "Running" 또는 챗봇 인터페이스가 보이면 성공!

### 5-3. 테스트
1. 질문 입력: "사회화란 무엇인가요?"
2. 답변 확인
3. 출처 정보 확인

---

## 🆘 문제 해결

### "Files" 탭이 안 보여요
- Space가 아직 생성 중일 수 있습니다
- 페이지를 새로고침해보세요
- Space 생성이 완료되었는지 확인

### GitHub 연결이 안 돼요
- GitHub 인증이 완료되었는지 확인
- 저장소 이름이 정확한지 확인: `Junbrobro/social_chatbot`
- 저장소가 Public인지 확인

### Secrets를 찾을 수 없어요
- Settings 페이지에서 스크롤해보세요
- 또는 검색창에 "secrets" 입력
- Space 타입이 올바른지 확인 (Gradio)

### 빌드가 실패해요
- **"Logs"** 탭에서 오류 메시지 확인
- `requirements.txt` 파일이 있는지 확인
- `app.py` 파일이 있는지 확인

---

## ✅ 완료 체크리스트

- [ ] Space 생성 완료
- [ ] GitHub 저장소 연결 완료
- [ ] Secrets에 `GROQ_API_KEY` 설정 완료
- [ ] 데이터 파일 업로드 완료
- [ ] 빌드 성공 확인
- [ ] 챗봇 테스트 완료

---

## 🎉 완료!

이제 Space URL을 공유하면 누구나 사용할 수 있습니다!

**공유 URL:**
```
https://huggingface.co/spaces/Junbrobro/social-culture-chatbot
```


# 🚀 초간단 배포 가이드 (5분 완성!)

## Hugging Face Spaces가 가장 간단합니다! ⭐

**왜 Hugging Face Spaces?**
- ✅ 클릭 몇 번으로 배포 완료
- ✅ URL만 공유하면 바로 사용 가능
- ✅ 환경 설정 불필요
- ✅ API 키만 설정하면 끝

---

## 📋 3단계로 끝내기

### 1단계: Space 생성 (1분)

1. https://huggingface.co/spaces 접속
2. **"New Space"** 클릭
3. 설정:
   - **Space name**: `social-culture-chatbot`
   - **SDK**: `Gradio` 선택
   - **Visibility**: `Public` 선택
4. **"Create Space"** 클릭

### 2단계: GitHub 연결 (2분)

**Space 페이지에서:**

1. **상단 탭 메뉴 확인**
   - **"Files"** 또는 **"Files and versions"** 탭 클릭
   - 또는 우측 상단의 **"+"** 버튼 클릭

2. **GitHub 연결**
   - **"Add file"** 버튼 클릭
   - 드롭다운에서 **"Connect repository"** 선택
   - GitHub 계정 연결 (처음이면 인증 필요)
   - 저장소 선택: `Junbrobro/social_chatbot`
   - **"Connect"** 클릭

**참고:** 
- "Files" 탭이 안 보이면 페이지를 새로고침하거나 Space 생성이 완료되었는지 확인하세요
- 또는 **"Settings"** 탭에서 **"Repository"** 섹션을 찾아보세요

### 3단계: API 키 설정 (1분)

1. Space 페이지에서 **"Settings"** 탭
2. 좌측 **"Secrets"** 클릭
3. **"New secret"** 클릭
4. 설정:
   - **Key**: `GROQ_API_KEY`
   - **Value**: 본인의 Groq API 키
5. **"Add secret"** 클릭

---

## 🎉 완료!

이제 자동으로 빌드가 시작됩니다 (5-10분 소요)

빌드 완료 후:
- Space URL이 생성됩니다
- 이 URL을 다른 사람에게 공유하면 끝!
- 별도 설정 없이 바로 사용 가능

**접속 URL 예시:**
```
https://huggingface.co/spaces/Junbrobro/social-culture-chatbot
```

---

## 📝 데이터 파일 업로드 (중요!)

빌드 후 챗봇이 작동하려면 데이터 파일이 필요합니다:

1. Space 페이지 → **"Files and versions"** 탭
2. **"Add file"** → **"Upload files"** 클릭
3. 다음 파일들 업로드:
   - `data/vector_db/embeddings.npy`
   - `data/vector_db/faiss_index.bin`
   - `data/vector_db/embeddings_metadata.json` (이미 GitHub에 있음)
   - `data/chunks/combined_all_chunks.json` (이미 GitHub에 있음)

**파일 위치:**
- 로컬: `C:\Projects\social_chatbot\data\vector_db\`

---

## ✅ 체크리스트

- [ ] Hugging Face Space 생성 완료
- [ ] GitHub 저장소 연결 완료
- [ ] Secrets에 `GROQ_API_KEY` 설정 완료
- [ ] 데이터 파일 업로드 완료
- [ ] 빌드 완료 확인
- [ ] 챗봇 테스트 완료

---

## 🎯 이제 이렇게 공유하세요!

```
안녕하세요! 사회문화 RAG 챗봇입니다.

아래 링크에서 바로 사용하실 수 있습니다:
https://huggingface.co/spaces/Junbrobro/social-culture-chatbot

질문을 입력하면 교재 내용을 바탕으로 답변해드립니다!
```

**끝!** 이제 누구나 클릭 한 번으로 사용할 수 있습니다! 🎉


# 📝 Notion에 프로젝트 업로드 가이드

## 방법 1: Notion Import 기능 사용 (가장 간단!)

### 1단계: Notion 페이지 준비
1. Notion 접속: https://www.notion.so
2. 새 페이지 생성 또는 기존 페이지 선택

### 2단계: Markdown 파일 Import
1. 페이지에서 **"..."** (더보기) 클릭
2. **"Import"** 선택
3. **"Markdown"** 선택
4. `README.md` 파일 업로드
5. Import 완료!

### 3단계: 추가 파일 Import (선택)
- 다른 마크다운 파일들도 같은 방식으로 Import 가능
- 여러 파일을 하나의 페이지에 추가 가능

---

## 방법 2: 수동 복사/붙여넣기

### 1단계: README.md 내용 복사
1. `README.md` 파일 열기
2. 전체 내용 선택 (Ctrl+A)
3. 복사 (Ctrl+C)

### 2단계: Notion에 붙여넣기
1. Notion 페이지 열기
2. **"/markdown"** 입력 후 Enter
3. 복사한 내용 붙여넣기 (Ctrl+V)
4. 자동으로 포맷팅됩니다!

---

## 방법 3: Notion API 사용 (자동화)

### 준비
1. Notion Integration 생성
   - https://www.notion.so/my-integrations 접속
   - "New integration" 클릭
   - 이름 입력 후 생성
   - Internal Integration Token 복사

2. 페이지에 Integration 연결
   - Notion 페이지에서 "..." → "Connections" → Integration 추가

### Python 스크립트로 자동 업로드
```python
# notion_upload.py (아래에 제공)
```

---

## 방법 4: 전체 프로젝트 문서화

### 추천 구조:
```
📚 사회문화 RAG 챗봇 프로젝트
├── 📖 프로젝트 개요 (README.md 내용)
├── 🏗️ 프로젝트 구조
├── 🚀 사용 방법
├── 📁 소스 코드 설명
│   ├── chatbot.py
│   ├── llmmodel.py
│   └── ...
└── 📊 진행 상황
```

---

## 빠른 시작 (추천!)

1. **README.md 파일 열기**
2. **전체 내용 복사** (Ctrl+A, Ctrl+C)
3. **Notion 페이지 열기**
4. **"/markdown"** 입력 후 Enter
5. **붙여넣기** (Ctrl+V)
6. **완료!** 🎉

---

## 추가 팁

### 코드 블록 포맷팅
- Notion은 자동으로 코드 블록을 인식합니다
- 필요시 **"/code"** 입력하여 코드 블록 생성

### 이미지 추가
- 스크린샷이나 다이어그램 추가 가능
- 드래그 앤 드롭으로 이미지 추가

### 데이터베이스로 관리
- 프로젝트를 데이터베이스로 만들어 체계적으로 관리
- 태그, 상태, 날짜 등으로 필터링 가능







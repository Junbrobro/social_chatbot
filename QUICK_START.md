# ⚡ 빠른 시작 가이드

## 🎯 GitHub Codespaces로 5분 안에 실행하기

### 1단계: Codespace 생성 (1분)

1. GitHub 저장소 페이지로 이동
   ```
   https://github.com/Junbrobro/social_chatbot
   ```

2. **"Code"** 버튼 클릭 → **"Codespaces"** 탭

3. **"Create codespace on main"** 클릭

4. Codespace가 자동으로 생성됩니다 (1-2분 소요)

### 2단계: 환경 변수 설정 (30초)

터미널에서 실행:
```bash
export GROQ_API_KEY="your-groq-api-key-here"
```

> 💡 **Groq API 키가 없나요?**
> - https://console.groq.com 접속
> - 무료 계정 생성
> - API 키 발급

### 3단계: 웹 데모 실행 (30초)

```bash
python web_demo.py
```

### 4단계: 접속 (즉시!)

- Codespace가 자동으로 포트를 포워딩합니다
- 포트 탭에서 **"Open in Browser"** 클릭
- 또는 터미널에 표시된 URL 클릭

**완료!** 🎉 이제 챗봇을 사용할 수 있습니다!

---

## 🔄 다른 사람과 공유하기

### 방법 1: GitHub 저장소 링크 공유
```
https://github.com/Junbrobro/social_chatbot
```
- 다른 사람도 Codespaces로 실행 가능
- 각자 API 키만 설정하면 됩니다

### 방법 2: README에 사용 방법 안내
- README.md에 위의 빠른 시작 가이드 포함
- 누구나 쉽게 따라할 수 있습니다

---

## ⚠️ 주의사항

1. **API 키 보안**
   - API 키는 절대 코드에 하드코딩하지 마세요
   - 환경 변수로만 사용하세요

2. **Codespaces 제한**
   - 무료 플랜: 월 60시간
   - Codespace는 30분 비활성 시 자동 종료

3. **데이터 파일**
   - 첫 실행 시 임베딩 모델 다운로드 (시간 소요)
   - 이후에는 캐시되어 빠릅니다

---

## 🐛 문제 해결

### Codespace가 생성되지 않아요
- GitHub 계정이 Codespaces를 지원하는지 확인
- 저장소가 Public이거나 접근 권한이 있는지 확인

### API 키 오류가 나요
- 환경 변수가 제대로 설정되었는지 확인
- `echo $GROQ_API_KEY`로 확인

### 포트가 열리지 않아요
- Codespace 포트 탭에서 수동으로 포워딩 설정
- 포트 7860을 Public으로 설정

---

## 📚 더 알아보기

- [전체 README](README.md)
- [배포 가이드](DEPLOYMENT.md)
- [프로젝트 상태](PROJECT_STATUS.md)


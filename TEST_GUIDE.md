# 🧪 테스트 가이드

## GitHub Codespaces로 테스트하기

### 1단계: Codespace 생성

1. **GitHub 저장소 페이지 접속**
   ```
   https://github.com/Junbrobro/social_chatbot
   ```

2. **"Code" 버튼 클릭** (초록색 버튼)

3. **"Codespaces" 탭 선택**

4. **"Create codespace on main" 클릭**
   - 또는 "+" 버튼 클릭

5. **Codespace 생성 대기** (1-2분)
   - 새 브라우저 탭이 열립니다
   - 자동으로 의존성이 설치됩니다

### 2단계: 환경 변수 설정

Codespace 터미널에서 실행:

```bash
export GROQ_API_KEY="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"
```

> ⚠️ **주의**: 실제 API 키를 사용하세요. 위는 예시입니다.

### 3단계: 웹 데모 실행

```bash
python web_demo.py
```

### 4단계: 접속

1. **포트 탭 확인**
   - Codespace 하단의 "PORTS" 탭 클릭
   - 포트 7860이 자동으로 포워딩됩니다

2. **브라우저에서 열기**
   - 포트 7860 옆의 "Open in Browser" 클릭
   - 또는 터미널에 표시된 URL 클릭

3. **챗봇 테스트**
   - 질문 입력: "사회화란 무엇인가요?"
   - 답변 확인
   - 출처 정보 확인

---

## 로컬에서 테스트하기

### 1단계: 저장소 클론

```bash
git clone https://github.com/Junbrobro/social_chatbot.git
cd social_chatbot
```

### 2단계: 의존성 설치

```bash
pip install -r requirements.txt
```

### 3단계: 환경 변수 설정

**Windows (PowerShell):**
```powershell
$env:GROQ_API_KEY="your-api-key"
```

**Linux/Mac:**
```bash
export GROQ_API_KEY="your-api-key"
```

### 4단계: 실행

```bash
python web_demo.py
```

브라우저에서 `http://localhost:7860` 접속

---

## 간단한 데모 테스트

터미널에서 바로 테스트:

```bash
python demo.py
```

대화형으로 질문하고 답변을 확인할 수 있습니다.

---

## 테스트 체크리스트

- [ ] Codespace 생성 성공
- [ ] 환경 변수 설정 완료
- [ ] 웹 데모 실행 성공
- [ ] 브라우저에서 접속 가능
- [ ] 질문 입력 및 답변 확인
- [ ] 출처 정보 표시 확인

---

## 문제 해결

### Codespace가 생성되지 않아요
- GitHub 계정이 Codespaces를 지원하는지 확인
- 저장소가 Public이거나 접근 권한이 있는지 확인

### API 키 오류
```bash
# 환경 변수 확인
echo $GROQ_API_KEY
```

### 포트가 열리지 않아요
- Codespace 포트 탭에서 수동으로 설정
- 포트 7860을 Public으로 변경

### 의존성 설치 오류
```bash
# 수동으로 재설치
pip install -r requirements.txt --upgrade
```


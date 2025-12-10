# 🚀 배포 가이드

## 방법 1: Gradio Share 링크 (가장 빠름! ⚡)

### 사용 방법:
1. `web_demo.py` 실행:
   ```bash
   python web_demo.py
   ```

2. 터미널에 나타나는 공개 URL 복사:
   ```
   * Running on public URL: https://xxxxx.gradio.live
   ```

3. 이 URL을 다른 사람에게 공유!

### 특징:
- ✅ 즉시 사용 가능
- ✅ 별도 설정 불필요
- ⚠️ 72시간 후 만료 (재시작하면 새 URL 생성)

---

## 방법 2: Hugging Face Spaces (무료, 영구) 🌟

### 준비:
1. Hugging Face 계정 생성: https://huggingface.co
2. 새 Space 생성:
   - https://huggingface.co/spaces 에서 "New Space" 클릭
   - 이름: `social-culture-chatbot`
   - SDK: `Gradio`
   - Visibility: `Public`

### 배포:
1. GitHub에 코드 업로드 (또는 Spaces에서 직접 업로드)

2. Spaces에 다음 파일들이 있는지 확인:
   - `app.py` (메인 앱 파일)
   - `requirements.txt` (의존성)
   - `src/` 폴더 (전체 소스 코드)
   - `data/` 폴더 (벡터DB 데이터)

3. Secrets 설정 (Spaces 설정에서):
   - `GROQ_API_KEY`: Groq API 키

4. 자동 배포 완료! 🎉

### 접속 URL:
```
https://huggingface.co/spaces/[사용자명]/social-culture-chatbot
```

---

## 방법 3: 클라우드 서버 배포

### Railway (추천)
1. https://railway.app 가입
2. GitHub 저장소 연결
3. 환경 변수 설정:
   - `GROQ_API_KEY`
4. 자동 배포!

### Render
1. https://render.com 가입
2. 새 Web Service 생성
3. GitHub 저장소 연결
4. 환경 변수 설정
5. 배포!

### Fly.io
1. https://fly.io 가입
2. `flyctl` 설치
3. `fly launch` 실행
4. 배포!

---

## 방법 4: VPS/서버 배포

### 준비:
1. 서버 준비 (AWS EC2, GCP, Azure 등)
2. 도메인 연결 (선택)

### 배포:
```bash
# 서버에 접속
ssh user@your-server.com

# 프로젝트 클론
git clone [your-repo-url]
cd social_chatbot

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
export GROQ_API_KEY="your-api-key"

# 서버 실행 (백그라운드)
nohup python web_demo.py > server.log 2>&1 &

# 또는 systemd 서비스로 등록
```

### Nginx 리버스 프록시 (선택):
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:7860;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 환경 변수 설정

### 필수:
- `GROQ_API_KEY`: Groq API 키

### 설정 방법:
```bash
# Linux/Mac
export GROQ_API_KEY="your-api-key"

# Windows (PowerShell)
$env:GROQ_API_KEY="your-api-key"

# .env 파일 사용
echo "GROQ_API_KEY=your-api-key" > .env
```

---

## 트러블슈팅

### 포트 충돌:
```bash
# 다른 포트 사용
python web_demo.py --port 8080
```

### 메모리 부족:
- 더 작은 모델 사용
- 청크 수 줄이기
- 서버 업그레이드

### API 키 오류:
- 환경 변수 확인
- API 키 유효성 확인
- 할당량 확인

---

## 추천 배포 방법

| 방법 | 난이도 | 비용 | 영구성 | 추천도 |
|------|--------|------|--------|--------|
| Gradio Share | ⭐ | 무료 | 72시간 | ⭐⭐⭐ |
| Hugging Face | ⭐⭐ | 무료 | 영구 | ⭐⭐⭐⭐⭐ |
| Railway | ⭐⭐⭐ | $5/월 | 영구 | ⭐⭐⭐⭐ |
| VPS | ⭐⭐⭐⭐ | $5-20/월 | 영구 | ⭐⭐⭐ |

**가장 추천: Hugging Face Spaces** (무료 + 영구 + 쉬움!)





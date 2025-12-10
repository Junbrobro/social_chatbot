# 🚀 GitHub Codespaces로 실행하기

이 프로젝트는 GitHub Codespaces에서 바로 실행할 수 있습니다!

## 사용 방법

1. **Codespace 생성**
   - GitHub 저장소 페이지에서 **"Code"** 버튼 클릭
   - **"Codespaces"** 탭 선택
   - **"Create codespace on main"** 클릭

2. **자동 설정**
   - Codespace가 생성되면 자동으로 의존성이 설치됩니다
   - 터미널에서 진행 상황을 확인할 수 있습니다

3. **환경 변수 설정**
   ```bash
   export GROQ_API_KEY="your-api-key-here"
   ```

4. **웹 데모 실행**
   ```bash
   python web_demo.py
   ```

5. **포트 포워딩**
   - Codespace가 자동으로 포트 7860을 포워딩합니다
   - 포트 탭에서 "Open in Browser" 클릭하거나
   - 터미널에 표시된 URL 클릭

## 주의사항

- Codespaces는 무료 플랜에서 월 60시간 제공
- 환경 변수는 Codespace 세션마다 다시 설정해야 합니다
- 데이터 파일이 크면 로드 시간이 걸릴 수 있습니다


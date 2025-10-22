
# Streamlit ChatGPT (Minimal)

간단한 Streamlit 챗봇 예제입니다. OpenAI Chat Completions API를 사용하며, 스트리밍 응답을 지원합니다.

## 배포 방법 (Streamlit Community Cloud)

1. 이 두 파일을 저장합니다.
   - `app.py`
   - `requirements.txt`
2. GitHub 저장소에 푸시합니다.
3. [streamlit.io](https://streamlit.io) → Community Cloud에서 새 앱을 생성하고 해당 저장소를 연결합니다.
4. **Secrets**에 아래처럼 API 키를 등록합니다.
   ```toml
   # Streamlit → Settings → Secrets
   OPENAI_API_KEY = "sk-..."
   ```
   (또는 환경변수 `OPENAI_API_KEY` 로 설정해도 됩니다.)
5. 앱을 실행하면 바로 대화할 수 있습니다.

## 로컬 실행
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 주요 기능
- 사이드바에서 모델, temperature, 시스템 프롬프트 설정
- 세션 상태에 대화 히스토리 저장
- 실시간 스트리밍 출력

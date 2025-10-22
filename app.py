
import os
import streamlit as st
from openai import OpenAI

# ---- Page setup ----
st.set_page_config(page_title="ChatGPT on Streamlit", page_icon="💬", layout="centered")
st.title("💬 ChatGPT on Streamlit")
st.caption("A minimal, stream-enabled chatbot powered by OpenAI")

# ---- API key handling ----
# Prefer Streamlit Cloud secrets, fallback to environment variable
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("🔑 OPENAI_API_KEY가 설정되어 있지 않습니다. Streamlit Secrets 또는 환경변수로 설정해 주세요.")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)

# ---- Sidebar ----
with st.sidebar:
    st.subheader("⚙️ 설정")
    model = st.selectbox(
        "모델",
        options=[
            "gpt-4o-mini",
            "gpt-4o",
            "gpt-4.1-mini"
        ],
        index=0,
        help="가볍게 테스트는 gpt-4o-mini, 더 높은 품질은 gpt-4o 계열을 선택하세요."
    )
    temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.1)
    system_prompt = st.text_area(
        "시스템 프롬프트 (선택)",
        value="You are a helpful, concise assistant.",
        height=100
    )
    if st.button("대화 초기화"):
        st.session_state.messages = [{"role": "system", "content": system_prompt}]

# ---- Session state init ----
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# Keep system prompt in sync when user edits it
if st.session_state.messages and st.session_state.messages[0]["role"] == "system":
    st.session_state.messages[0]["content"] = system_prompt

# ---- Render chat history (excluding system) ----
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---- Chat input ----
user_input = st.chat_input("메시지를 입력하세요...")
if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # ---- Get assistant response (streaming) ----
    with st.chat_message("assistant"):
        placeholder = st.empty()
        stream_text = ""
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    m for m in st.session_state.messages
                    if m["role"] in ("system", "user", "assistant")
                ],
                temperature=temperature,
                stream=True,
            )
            for chunk in response:
                delta = chunk.choices[0].delta
                if hasattr(delta, "content") and delta.content:
                    stream_text += delta.content
                    placeholder.markdown(stream_text)
        except Exception as e:
            st.error(f"API 호출 중 오류가 발생했습니다: {e}")
            st.stop()

        # Save and render final assistant message
        st.session_state.messages.append({"role": "assistant", "content": stream_text})
        placeholder.markdown(stream_text)

# ---- Footer ----
st.markdown("---")
st.caption("Tip: 사이드바에서 모델과 톤(temperature)을 바꿔보세요.")

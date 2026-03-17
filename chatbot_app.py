import streamlit as st
import anthropic

# 페이지 설정
st.set_page_config(
    page_title="상업교과 학습 챗봇",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 타이틀 및 설명
st.title("📚 고등학교 상업교과 학습 가이드 챗봇")
st.markdown("고등학교 2학년 상업교과 교사가 여러분의 학습을 도와드립니다.")

# 사이드바: API 키 입력
with st.sidebar:
    st.header("⚙️ 설정")
    api_key = st.text_input(
        "Claude API 키를 입력하세요",
        type="password",
        help="https://console.anthropic.com에서 API 키를 발급받으세요"
    )
    
    st.divider()
    
    st.markdown("### 💡 학습 팁")
    st.markdown("""
    - 구체적인 질문을 할수록 더 도움이 됩니다
    - 경제, 경영, 회계 등 다양한 주제 질문 가능
    - 개념 설명, 문제 풀이, 학습 전략 등을 물어보세요
    """)
    
    # 대화 초기화 버튼
    if st.button("🔄 대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.success("대화가 초기화되었습니다!")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 채팅 이력 표시
st.markdown("### 💬 대화")
chat_container = st.container()

with chat_container:
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            st.chat_message("user").write(content)
        else:
            st.chat_message("assistant").write(content)

# 사용자 입력
user_input = st.chat_input("질문을 입력하세요...")

if user_input:
    # API 키 확인
    if not api_key:
        st.error("❌ Claude API 키를 입력해주세요.")
        st.stop()
    
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)
    
    # Claude 호출
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        system_prompt = """당신은 고등학교 2학년 상업교과 교사입니다.
        
학생들의 학습을 돕기 위해 다음과 같이 행동하세요:
1. 항상 한국어로 친절하고 명확하게 설명합니다.
2. 경제, 경영, 회계, 마케팅 등 상업 관련 주제를 다룹니다.
3. 복잡한 개념은 구체적인 예시와 함께 설명합니다.
4. 학생의 수준에 맞게 쉽게 이해할 수 있도록 설명합니다.
5. 필요시 학습 팁이나 공부 방법을 제시합니다.
6. 문제 풀이를 요청받으면 단계별로 설명합니다."""
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # 스트리밍 응답
            with client.messages.stream(
                model="claude-haiku-4-5-20251001",
                max_tokens=1024,
                system=system_prompt,
                messages=[
                    {"role": msg["role"], "content": msg["content"]}
                    for msg in st.session_state.messages
                ]
            ) as stream:
                for text in stream.text_stream:
                    full_response += text
                    message_placeholder.markdown(full_response)
            
            # 어시스턴트 메시지 저장
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response
            })
    
    except anthropic.APIError as e:
        st.error(f"❌ API 오류: {str(e)}")
    except anthropic.AuthenticationError:
        st.error("❌ API 키가 유효하지 않습니다. 다시 확인해주세요.")
    except Exception as e:
        st.error(f"❌ 오류 발생: {str(e)}")

# 푸터
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 0.9em;'>
    고등학교 상업교과 학습 가이드 챗봇 | Powered by Claude Haiku
</div>
""", unsafe_allow_html=True)
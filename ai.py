import streamlit as st
import anthropic
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="물리 에너지 튜터",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
    <style>
    .teacher-message {
        background-color: #E3F2FD;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #1976D2;
        margin: 10px 0;
    }
    .student-message {
        background-color: #F5F5F5;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #757575;
        margin: 10px 0;
    }
    .info-box {
        background-color: #FFF3E0;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #F57C00;
        margin: 15px 0;
    }
    </style>
""", unsafe_allow_html=True)

# 제목 및 설명
st.title("⚡ 중학교 물리 - 에너지 전환 튜터")
st.markdown("**운동에너지와 위치에너지의 전환에 대해 배워봅시다!**")

# 사이드바 - API 키 및 설정
with st.sidebar:
    st.header("⚙️ 설정")
    
    api_key = st.text_input(
        "Anthropic API 키 입력:",
        type="password",
        help="https://console.anthropic.com 에서 발급받으세요"
    )
    
    st.divider()
    
    st.subheader("📚 학습 자료")
    st.markdown("""
    **이 튜터는 다음을 다룹니다:**
    - 운동에너지 (Kinetic Energy)
    - 위치에너지 (Potential Energy)
    - 에너지 전환 원리
    - 실생활 예시
    - 문제 풀이
    
    **사용 모델:** Claude Haiku 4.5
    """)
    
    if st.button("💬 대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.session_state.conversation_count = 0
        st.success("대화가 초기화되었습니다!")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_count" not in st.session_state:
    st.session_state.conversation_count = 0

# 시스템 프롬프트
SYSTEM_PROMPT = """당신은 경험 많은 중학교 물리 교사입니다.

전문 분야:
- 운동에너지(KE = 1/2 × m × v²)와 위치에너지(PE = m × g × h) 설명
- 에너지 전환 원리 (운동에너지 ↔ 위치에너지)
- 에너지 보존 법칙
- 실생활 예시를 통한 설명

지도 원칙:
1. 학생 수준에 맞춘 쉬운 설명
2. 구체적인 예시 제시 (롤러코스터, 자유낙하, 공 던지기 등)
3. 단계별 계산 방법 안내
4. 자주 묻는 질문에 친절한 답변
5. 격려와 긍정적 피드백

형식:
- 수식은 LaTeX 형식으로: $수식$
- 중요한 개념은 **굵게** 표시
- 단계별 설명은 숫자 목록으로 정렬
- 질문을 권장하고 이해도 확인"""

# 메시지 표시 함수
def display_message(message, is_teacher=True):
    if is_teacher:
        st.markdown(f'<div class="teacher-message">{message}</div>', 
                   unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="student-message">{message}</div>', 
                   unsafe_allow_html=True)

# 대화 기록 표시
for message in st.session_state.messages:
    is_teacher = message["role"] == "assistant"
    display_message(message["content"], is_teacher=is_teacher)

# 입력창
st.divider()
col1, col2 = st.columns([0.9, 0.1])

with col1:
    user_input = st.chat_input(
        "운동에너지와 위치에너지에 대해 질문해주세요... 예: 롤러코스터에서 에너지는 어떻게 변할까요?",
        key="user_input"
    )

# 메시지 처리 및 응답 생성
if user_input:
    if not api_key:
        st.error("❌ Anthropic API 키를 먼저 입력해주세요.")
    else:
        # 사용자 메시지 추가 및 표시
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        display_message(user_input, is_teacher=False)
        st.session_state.conversation_count += 1
        
        # Claude API 호출
        try:
            client = anthropic.Anthropic(api_key=api_key)
            
            # 스트리밍 응답 처리
            with st.chat_message("assistant", avatar="👨‍🏫"):
                message_placeholder = st.empty()
                full_response = ""
                
                with client.messages.stream(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=1024,
                    system=SYSTEM_PROMPT,
                    messages=[
                        {
                            "role": msg["role"],
                            "content": msg["content"]
                        }
                        for msg in st.session_state.messages
                    ]
                ) as stream:
                    for text in stream.text_stream:
                        full_response += text
                        message_placeholder.markdown(full_response)
                
                # 응답 저장
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": full_response
                })
        
        except anthropic.APIError as e:
            st.error(f"❌ API 오류: {str(e)}")
            # 오류 메시지 제거
            st.session_state.messages.pop()
        except Exception as e:
            st.error(f"❌ 예상치 못한 오류: {str(e)}")
            st.session_state.messages.pop()

# 하단 정보
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("대화 횟수", st.session_state.conversation_count)

with col2:
    st.metric("메시지 수", len(st.session_state.messages))

with col3:
    if api_key:
        st.success("✅ API 연결됨")
    else:
        st.warning("⚠️ API 키 필요")

st.markdown("""
---
**💡 팁:** 다양한 질문을 해보세요!
- "운동에너지를 줄이려면 어떻게 해야 할까?"
- "높은 곳에서 떨어지는 공의 에너지는?"
- "에너지 전환의 실생활 예시를 들어줄래?"
""")

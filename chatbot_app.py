import streamlit as st
import anthropic
import json
import random

# ─────────────────────────────────────────────
# 페이지 설정
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="상업교과 학습 챗봇 🏫",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# 커스텀 CSS (학생 친화적 디자인)
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* 전체 배경 */
    .stApp {
        background: linear-gradient(135deg, #667eea22 0%, #764ba222 100%);
    }

    /* 메인 타이틀 */
    .main-title {
        text-align: center;
        font-size: 2.4rem;
        font-weight: 900;
        background: linear-gradient(90deg, #667eea, #764ba2, #f64f59);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
        letter-spacing: -1px;
    }
    .sub-title {
        text-align: center;
        font-size: 1rem;
        color: #888;
        margin-bottom: 1.5rem;
    }

    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f0f2f6;
        border-radius: 16px;
        padding: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 8px 20px;
        font-weight: 600;
        font-size: 0.95rem;
        color: #555;
        transition: all 0.2s;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
    }

    /* 채팅 메시지 */
    .stChatMessage {
        border-radius: 18px !important;
        margin-bottom: 8px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07) !important;
    }

    /* 카드 컴포넌트 */
    .info-card {
        background: white;
        border-radius: 20px;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 4px 15px rgba(102,126,234,0.12);
        margin-bottom: 1rem;
        border-left: 5px solid #667eea;
        transition: transform 0.2s;
    }
    .info-card:hover {
        transform: translateY(-2px);
    }
    .info-card h4 {
        margin: 0 0 0.4rem 0;
        color: #667eea;
        font-size: 1rem;
    }
    .info-card p {
        margin: 0;
        color: #555;
        font-size: 0.9rem;
    }

    /* 퀴즈 카드 */
    .quiz-card {
        background: linear-gradient(135deg, #fff9c4, #fff3e0);
        border-radius: 20px;
        padding: 1.5rem 2rem;
        box-shadow: 0 4px 20px rgba(255,193,7,0.2);
        border-left: 6px solid #ffc107;
        margin: 1rem 0;
    }
    .quiz-question {
        font-size: 1.15rem;
        font-weight: 700;
        color: #333;
        margin-bottom: 1rem;
        line-height: 1.6;
    }

    /* 결과 박스 */
    .result-correct {
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        border-radius: 16px;
        padding: 1rem 1.5rem;
        border-left: 5px solid #28a745;
        font-weight: 600;
        color: #155724;
        font-size: 1rem;
    }
    .result-wrong {
        background: linear-gradient(135deg, #f8d7da, #f5c6cb);
        border-radius: 16px;
        padding: 1rem 1.5rem;
        border-left: 5px solid #dc3545;
        font-weight: 600;
        color: #721c24;
        font-size: 1rem;
    }

    /* 점수 뱃지 */
    .score-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border-radius: 50px;
        padding: 0.4rem 1.2rem;
        font-weight: 700;
        font-size: 1rem;
        box-shadow: 0 3px 10px rgba(102,126,234,0.35);
    }

    /* 사이드바 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    [data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }
    [data-testid="stSidebar"] .stButton button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.3s !important;
    }
    [data-testid="stSidebar"] .stButton button:hover {
        opacity: 0.85 !important;
        transform: translateY(-1px) !important;
    }

    /* 입력창 */
    .stChatInputContainer {
        border-radius: 20px !important;
        border: 2px solid #667eea44 !important;
        box-shadow: 0 4px 12px rgba(102,126,234,0.1) !important;
    }

    /* 통계 박스 */
    .stat-box {
        background: white;
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
    }
    .stat-num {
        font-size: 2rem;
        font-weight: 900;
        color: #667eea;
    }
    .stat-label {
        font-size: 0.8rem;
        color: #888;
        font-weight: 600;
    }

    /* 주제 버튼 */
    div[data-testid="column"] .stButton button {
        border-radius: 14px;
        font-size: 0.88rem;
        padding: 0.5rem 0.3rem;
        font-weight: 600;
        border: 2px solid #667eea44;
        background: white;
        color: #444;
        transition: all 0.2s;
        width: 100%;
    }
    div[data-testid="column"] .stButton button:hover {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border-color: transparent;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102,126,234,0.3);
    }

    /* 진행바 */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
        border-radius: 10px !important;
    }

    /* 구분선 */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, #667eea33, #764ba233);
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# 세션 상태 초기화
# ─────────────────────────────────────────────
def init_session():
    defaults = {
        "messages": [],
        "quiz_question": None,
        "quiz_answer": None,
        "quiz_explanation": None,
        "quiz_choices": None,
        "quiz_submitted": False,
        "quiz_correct": None,
        "quiz_score": 0,
        "quiz_total": 0,
        "quiz_topic": "전체",
        "chat_count": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()


# ─────────────────────────────────────────────
# Claude 클라이언트 생성
# ─────────────────────────────────────────────
def get_client(api_key: str):
    return anthropic.Anthropic(api_key=api_key)


# ─────────────────────────────────────────────
# 시스템 프롬프트
# ─────────────────────────────────────────────
SYSTEM_PROMPT = """당신은 고등학교 2학년 상업교과 담당 교사입니다.

✅ 역할 및 행동 지침:
- 학생들에게 친절하고 따뜻하게, 존댓말을 사용해 답변합니다.
- 경제, 경영, 회계, 마케팅, 무역, 금융 등 상업 관련 주제를 전문으로 다룹니다.
- 어려운 개념은 쉬운 예시와 비유를 들어 설명합니다.
- 답변은 명확하게 핵심을 먼저 말하고, 필요시 단계별로 설명합니다.
- 학생이 틀린 개념을 갖고 있으면 부드럽게 교정해줍니다.
- 마크다운(볼드, 글머리 기호, 표 등)을 적극 활용하여 가독성을 높입니다.
- 답변 말미에 관련 심화 질문을 1~2개 제안하여 학습 동기를 높입니다.
- 모든 답변은 반드시 한국어로 합니다."""

QUIZ_SYSTEM_PROMPT = """당신은 고등학교 2학년 상업교과 퀴즈 출제 AI입니다.
다음 JSON 형식으로만 응답하세요. 다른 텍스트는 절대 포함하지 마세요.

{
  "question": "문제 내용",
  "choices": ["① 선택지1", "② 선택지2", "③ 선택지3", "④ 선택지4"],
  "answer": "① 선택지1",
  "explanation": "정답 해설 (2~3문장, 핵심 개념 포함)"
}

규칙:
- 고2 상업교과 수준의 4지선다 문제를 출제합니다.
- 선택지는 반드시 4개, ①②③④ 기호를 붙입니다.
- answer는 choices 중 정확히 하나와 일치해야 합니다.
- explanation은 왜 정답인지 명확히 설명합니다.
- 반드시 유효한 JSON만 반환합니다."""


# ─────────────────────────────────────────────
# 퀴즈 생성 함수
# ─────────────────────────────────────────────
def generate_quiz(api_key: str, topic: str):
    client = get_client(api_key)
    topic_map = {
        "전체": "경제, 경영, 회계, 마케팅, 무역 중 랜덤 주제",
        "경제": "경제 기초 (수요/공급, GDP, 인플레이션 등)",
        "경영": "경영 전략, 조직 관리, 기업 형태 등",
        "회계": "재무제표, 분개, 손익계산 등",
        "마케팅": "마케팅 믹스, 시장 조사, 브랜드 전략 등",
        "무역": "무역 기초, 인코텀즈, 무역 서류 등",
        "금융": "금융 상품, 이자, 환율, 주식 기초 등",
    }
    prompt = f"{topic_map.get(topic, topic)} 주제로 고등학교 2학년 수준의 4지선다 퀴즈 1문제를 출제해주세요."

    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=600,
            system=QUIZ_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = response.content[0].text.strip()
        # JSON 파싱
        data = json.loads(raw)
        return data
    except json.JSONDecodeError:
        # JSON 블록 추출 시도
        try:
            start = raw.index("{")
            end   = raw.rindex("}") + 1
            data  = json.loads(raw[start:end])
            return data
        except Exception:
            return None
    except Exception:
        return None


# ─────────────────────────────────────────────
# 사이드바
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎓 상업교과 챗봇")
    st.markdown("---")

    # API 키
    st.markdown("### 🔑 API 설정")
    api_key = st.text_input(
        "Claude API 키",
        type="password",
        placeholder="sk-ant-...",
        help="https://console.anthropic.com 에서 발급"
    )
    if api_key:
        st.success("✅ API 키 입력 완료!")
    else:
        st.warning("⚠️ API 키를 입력하세요")

    st.markdown("---")

    # 학습 통계
    st.markdown("### 📊 내 학습 현황")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class='stat-box'>
            <div class='stat-num'>{st.session_state.chat_count}</div>
            <div class='stat-label'>💬 질문 수</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='stat-box'>
            <div class='stat-num'>{st.session_state.quiz_score}</div>
            <div class='stat-label'>🏆 퀴즈 점수</div>
        </div>""", unsafe_allow_html=True)

    # 퀴즈 정답률
    if st.session_state.quiz_total > 0:
        rate = int(st.session_state.quiz_score / st.session_state.quiz_total * 100)
        st.markdown(f"**퀴즈 정답률:** {rate}% ({st.session_state.quiz_score}/{st.session_state.quiz_total})")
        st.progress(rate / 100)

    st.markdown("---")

    # 추천 질문
    st.markdown("### 💡 추천 질문 주제")
    topics = ["수요와 공급 법칙", "재무제표 읽기", "마케팅 4P 전략",
              "환율의 영향", "주식과 채권 차이", "GDP란 무엇인가"]
    for topic in topics:
        st.markdown(f"• {topic}")

    st.markdown("---")

    # 초기화 버튼
    if st.button("🔄 대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_count = 0
        st.rerun()

    if st.button("🗑️ 퀴즈 기록 초기화", use_container_width=True):
        for k in ["quiz_question","quiz_answer","quiz_explanation",
                  "quiz_choices","quiz_submitted","quiz_correct",
                  "quiz_score","quiz_total"]:
            st.session_state[k] = 0 if "score" in k or "total" in k else None
        st.session_state.quiz_submitted = False
        st.rerun()


# ─────────────────────────────────────────────
# 메인 타이틀
# ─────────────────────────────────────────────
st.markdown("<div class='main-title'>📚 상업교과 학습 도우미</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>고2 상업교과 | AI 선생님이 24시간 함께합니다 🙌</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 탭 구성
# ─────────────────────────────────────────────
tab_chat, tab_quiz, tab_guide = st.tabs(["💬 학습 챗봇", "🧩 퀴즈 풀기", "📖 학습 가이드"])


# ════════════════════════════════════════════
# 탭 1: 학습 챗봇
# ════════════════════════════════════════════
with tab_chat:
    st.markdown("#### 무엇이든 물어보세요! 선생님이 친절하게 설명해 드립니다 😊")

    # 빠른 질문 버튼
    st.markdown("**⚡ 빠른 질문 선택:**")
    qcols = st.columns(4)
    quick_questions = [
        ("📈 수요·공급", "수요와 공급의 법칙을 쉽게 설명해주세요."),
        ("💰 회계 기초", "재무제표의 종류와 각각의 역할을 알려주세요."),
        ("🎯 마케팅", "마케팅 믹스(4P)란 무엇인가요?"),
        ("🌍 환율", "환율이 오르면 어떤 영향이 있나요?"),
    ]
    for i, (label, question) in enumerate(quick_questions):
        with qcols[i]:
            if st.button(label, key=f"quick_{i}", use_container_width=True):
                st.session_state["quick_input"] = question

    st.markdown("---")

    # 채팅 메시지 출력
    chat_box = st.container(height=430, border=False)
    with chat_box:
        if not st.session_state.messages:
            st.markdown("""
            <div class='info-card'>
                <h4>👋 안녕하세요! 상업교과 AI 선생님입니다.</h4>
                <p>경제, 경영, 회계, 마케팅 등 상업교과 관련 질문을 자유롭게 해주세요.<br>
                위 빠른 질문 버튼을 클릭하거나 직접 입력해도 됩니다!</p>
            </div>
            """, unsafe_allow_html=True)

        for msg in st.session_state.messages:
            avatar = "🧑‍🎓" if msg["role"] == "user" else "👨‍🏫"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

    # 사용자 입력 처리
    user_input = st.chat_input("질문을 입력하세요... (예: 복식부기란 무엇인가요?)")

    # 빠른 질문 자동 채움
    if "quick_input" in st.session_state and st.session_state["quick_input"]:
        user_input = st.session_state.pop("quick_input")

    if user_input:
        if not api_key:
            st.error("❌ 왼쪽 사이드바에서 API 키를 먼저 입력해주세요!")
            st.stop()

        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.chat_count += 1

        with chat_box:
            with st.chat_message("user", avatar="🧑‍🎓"):
                st.markdown(user_input)

            with st.chat_message("assistant", avatar="👨‍🏫"):
                placeholder = st.empty()
                full_response = ""
                try:
                    client = get_client(api_key)
                    with client.messages.stream(
                        model="claude-haiku-4-5-20251001",
                        max_tokens=1200,
                        system=SYSTEM_PROMPT,
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ]
                    ) as stream:
                        for text in stream.text_stream:
                            full_response += text
                            placeholder.markdown(full_response + "▌")
                    placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                except anthropic.AuthenticationError:
                    st.error("❌ API 키가 유효하지 않습니다.")
                except anthropic.APIError as e:
                    st.error(f"❌ API 오류: {e}")
                except Exception as e:
                    st.error(f"❌ 오류 발생: {e}")

        st.rerun()


# ════════════════════════════════════════════
# 탭 2: 퀴즈 풀기
# ════════════════════════════════════════════
with tab_quiz:
    st.markdown("#### 🧩 상업교과 실력을 테스트해보세요!")

    # 점수 현황
    score_col1, score_col2, score_col3 = st.columns(3)
    with score_col1:
        st.markdown(f"""
        <div class='stat-box'>
            <div class='stat-num' style='color:#28a745'>{st.session_state.quiz_score}</div>
            <div class='stat-label'>✅ 맞은 문제</div>
        </div>""", unsafe_allow_html=True)
    with score_col2:
        wrong = st.session_state.quiz_total - st.session_state.quiz_score
        st.markdown(f"""
        <div class='stat-box'>
            <div class='stat-num' style='color:#dc3545'>{wrong}</div>
            <div class='stat-label'>❌ 틀린 문제</div>
        </div>""", unsafe_allow_html=True)
    with score_col3:
        rate = int(st.session_state.quiz_score / st.session_state.quiz_total * 100) \
               if st.session_state.quiz_total > 0 else 0
        st.markdown(f"""
        <div class='stat-box'>
            <div class='stat-num' style='color:#764ba2'>{rate}%</div>
            <div class='stat-label'>🎯 정답률</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # 주제 선택
    st.markdown("**📌 퀴즈 주제 선택:**")
    topic_cols = st.columns(7)
    topics_list = ["전체", "경제", "경영", "회계", "마케팅", "무역", "금융"]
    topic_icons = ["🎲", "📈", "🏢", "📊", "🎯", "🌍", "💰"]

    for i, (t, icon) in enumerate(zip(topics_list, topic_icons)):
        with topic_cols[i]:
            is_selected = st.session_state.quiz_topic == t
            btn_label = f"{icon} {t}" + (" ✓" if is_selected else "")
            if st.button(btn_label, key=f"topic_{t}", use_container_width=True):
                st.session_state.quiz_topic = t
                st.rerun()

    st.markdown(f"**선택된 주제:** `{st.session_state.quiz_topic}` 🏷️")
    st.markdown("---")

    # 퀴즈 생성 버튼
    gen_col, _ = st.columns([1, 3])
    with gen_col:
        gen_btn = st.button("🎲 새 문제 생성하기", type="primary", use_container_width=True)

    if gen_btn:
        if not api_key:
            st.error("❌ API 키를 먼저 입력해주세요!")
        else:
            with st.spinner("✨ 선생님이 문제를 출제 중입니다..."):
                data = generate_quiz(api_key, st.session_state.quiz_topic)
            if data:
                st.session_state.quiz_question    = data.get("question")
                st.session_state.quiz_choices     = data.get("choices", [])
                st.session_state.quiz_answer      = data.get("answer")
                st.session_state.quiz_explanation = data.get("explanation")
                st.session_state.quiz_submitted   = False
                st.session_state.quiz_correct     = None
                st.rerun()
            else:
                st.error("❌ 문제 생성에 실패했습니다. 다시 시도해주세요.")

    # 퀴즈 표시
    if st.session_state.quiz_question:
        st.markdown(f"""
        <div class='quiz-card'>
            <div style='font-size:0.85rem; color:#888; margin-bottom:0.5rem;'>
                📌 주제: {st.session_state.quiz_topic} &nbsp;|&nbsp; 총 {st.session_state.quiz_total}문제 풀이
            </div>
            <div class='quiz-question'>❓ {st.session_state.quiz_question}</div>
        </div>
        """, unsafe_allow_html=True)

        choices = st.session_state.quiz_choices or []

        if not st.session_state.quiz_submitted:
            # 라디오 버튼으로 선택
            selected = st.radio(
                "정답을 선택하세요:",
                options=choices,
                index=None,
                key="quiz_radio"
            )

            submit_col, _ = st.columns([1, 4])
            with submit_col:
                if st.button("✅ 정답 제출", type="primary", use_container_width=True,
                             disabled=(selected is None)):
                    st.session_state.quiz_submitted = True
                    st.session_state.quiz_correct   = (selected == st.session_state.quiz_answer)
                    st.session_state.quiz_total    += 1
                    if st.session_state.quiz_correct:
                        st.session_state.quiz_score += 1
                    st.rerun()
        else:
            # 결과 표시
            for ch in choices:
                if ch == st.session_state.quiz_answer:
                    st.success(f"✅ {ch}  ← 정답")
                elif ch == st.session_state.get("quiz_radio"):
                    st.error(f"❌ {ch}  ← 내 선택")
                else:
                    st.markdown(f"　　{ch}")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.session_state.quiz_correct:
                st.markdown("""
                <div class='result-correct'>
                    🎉 정답입니다! 훌륭해요!
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='result-wrong'>
                    😅 아쉽네요! 정답은 <b>{st.session_state.quiz_answer}</b>입니다.
                </div>""", unsafe_allow_html=True)

            # 해설
            if st.session_state.quiz_explanation:
                with st.expander("📖 해설 보기", expanded=True):
                    st.info(f"💡 {st.session_state.quiz_explanation}")

            # 다음 문제 버튼
            next_col, _ = st.columns([1, 3])
            with next_col:
                if st.button("➡️ 다음 문제", type="primary", use_container_width=True):
                    if not api_key:
                        st.error("API 키를 입력하세요.")
                    else:
                        with st.spinner("다음 문제 출제 중..."):
                            data = generate_quiz(api_key, st.session_state.quiz_topic)
                        if data:
                            st.session_state.quiz_question    = data.get("question")
                            st.session_state.quiz_choices     = data.get("choices", [])
                            st.session_state.quiz_answer      = data.get("answer")
                            st.session_state.quiz_explanation = data.get("explanation")
                            st.session_state.quiz_submitted   = False
                            st.session_state.quiz_correct     = None
                            st.rerun()
                        else:
                            st.error("문제 생성 실패. 다시 시도해주세요.")


# ════════════════════════════════════════════
# 탭 3: 학습 가이드
# ════════════════════════════════════════════
with tab_guide:
    st.markdown("#### 📖 상업교과 학습 가이드")
    st.markdown("고등학교 2학년 상업교과의 핵심 단원과 학습 방법을 안내합니다.")

    # 단원별 정리
    guide_data = {
        "📈 경제 기초": {
            "color": "#667eea",
            "topics": ["수요·공급 법칙", "탄력성", "시장 균형", "GDP·물가", "경제 성장"],
            "tip": "그래프와 함께 개념을 이해하면 시험에 유리합니다.",
        },
        "🏢 경영학 기초": {
            "color": "#764ba2",
            "topics": ["기업의 형태", "경영 전략", "조직 관리", "인사관리", "재무관리"],
            "tip": "실제 기업 사례와 연결지어 학습하면 이해가 쉽습니다.",
        },
        "📊 회계 원리": {
            "color": "#f64f59",
            "topics": ["복식부기", "분개·전기", "재무제표", "손익계산", "원가계산"],
            "tip": "분개 연습을 반복하는 것이 회계 학습의 핵심입니다.",
        },
        "🎯 마케팅": {
            "color": "#11998e",
            "topics": ["마케팅 믹스(4P)", "시장 세분화", "소비자 행동", "브랜드 관리", "디지털 마케팅"],
            "tip": "주변 광고·브랜드를 분석하며 개념을 적용해보세요.",
        },
        "🌍 무역 기초": {
            "color": "#f7971e",
            "topics": ["무역 원리", "인코텀즈", "무역 서류", "환율·외환", "수출입 절차"],
            "tip": "환율 뉴스를 매일 확인하며 실전 감각을 키우세요.",
        },
        "💰 금융과 투자": {
            "color": "#56ab2f",
            "topics": ["금융 시장", "주식·채권", "펀드·ETF", "이자·복리", "리스크 관리"],
            "tip": "복리 계산 공식은 시험에 자주 나오니 꼭 암기하세요.",
        },
    }

    g_cols = st.columns(2)
    for i, (unit, info) in enumerate(guide_data.items()):
        with g_cols[i % 2]:
            topics_str = " · ".join(info["topics"])
            st.markdown(f"""
            <div class='info-card' style='border-left-color:{info["color"]}'>
                <h4 style='color:{info["color"]}'>{unit}</h4>
                <p style='color:#666; font-size:0.85rem;'>📌 {topics_str}</p>
                <p style='color:#888; font-size:0.82rem; margin-top:0.5rem;'>
                    💡 <em>{info["tip"]}</em>
                </p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # 시험 대비 전략
    st.markdown("### 🏆 시험 대비 전략")
    strat_cols = st.columns(3)
    strategies = [
        ("📅 계획 수립", "시험 2주 전부터 단원별 학습 계획을 세우고, 매일 복습 시간을 확보하세요."),
        ("📝 오답 노트", "틀린 문제는 반드시 오답 노트에 정리하고, 시험 전날 집중적으로 복습하세요."),
        ("🤝 AI 활용", "챗봇 선생님에게 모르는 개념을 질문하고, 퀴즈로 자기 실력을 점검하세요."),
    ]
    for col, (title, desc) in zip(strat_cols, strategies):
        with col:
            st.markdown(f"""
            <div class='info-card'>
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='text-align:center; color:#aaa; font-size:0.85rem; padding: 1rem 0;'>
        📚 상업교과 학습 가이드 챗봇 | Powered by Claude Haiku 4.5 | Made with ❤️ for Students
    </div>
    """, unsafe_allow_html=True)

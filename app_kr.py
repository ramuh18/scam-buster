import streamlit as st
from openai import OpenAI
import base64

# 1. 페이지 설정
st.set_page_config(
    page_title="ScamBuster AI",
    page_icon="🛡️",
    layout="wide"
)

# --- [가독성 극대화 전용 CSS] ---
st.markdown(
    """
    <style>
    /* 기본 폰트 크기 상향 */
    html, body, [class*="st-"] {
        font-size: 18px !important; /* 전체적으로 크게 */
        line-height: 1.6;
    }
    
    /* 제목(Title) 가독성 */
    h1 {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        padding-bottom: 1rem;
    }
    
    /* 탭 메뉴 글씨 크게 */
    .stTabs [data-baseweb="tab"] {
        font-size: 20px !important;
        font-weight: bold !important;
    }

    /* 입력창 텍스트 크기 */
    .stTextArea textarea {
        font-size: 18px !important;
    }

    /* 버튼 글씨 및 크기 (시원시원하게) */
    .stButton button {
        font-size: 22px !important;
        font-weight: bold !important;
        height: 4rem !important;
        border-radius: 15px !important;
    }

    /* 분석 결과창 폰트 강조 */
    .result-text {
        font-size: 20px !important;
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 8px solid #ff4b4b;
        color: #1f2937;
    }

    /* 모바일 환경 최적화 */
    @media (max-width: 768px) {
        h1 { font-size: 2rem !important; }
        .stButton button { font-size: 20px !important; }
        .banner-text { font-size: 14px !important; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. 비밀 금고 연동
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = st.sidebar.text_input("🔑 관리자 키", type="password")

# --- [사이드바] ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=100)
    st.title("🛡️ 보안 센터")
    st.success("✅ 시스템 정상 가동")
    st.divider()
    st.markdown("### 💡 안전 수칙")
    st.warning("**1. 링크 클릭 절대 금지**")
    st.warning("**2. 개인정보 요구 주의**")
    st.divider()
    st.write("최신 AI가 사기 패턴을 분석합니다.")

# --- [메인 화면] ---
st.title("🕵️‍♂️ ScamBuster AI")
st.markdown("### \"사기인지 불안하시죠? 제가 봐드릴게요.\"")

st.divider()

# 탭 메뉴 (가독성 위해 큼직하게)
tab1, tab2 = st.tabs(["📝 문자 내용 복사", "📸 스크린샷 올리기"])

user_input = ""
uploaded_file = None

with tab1:
    user_input = st.text_area("의심스러운 내용을 아래에 붙여넣으세요:", height=200, placeholder="내용을 여기에 입력하세요...")

with tab2:
    uploaded_file = st.file_uploader("이미지 파일을 선택하세요", type=["jpg", "png", "jpeg"])

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# 분석 버튼 (가장 크게 강조)
if st.button("🚨 지금 즉시 사기 여부 분석", type="primary", use_container_width=True):
    if not api_key:
        st.error("API 키를 확인해 주세요.")
    elif not user_input and not uploaded_file:
        st.warning("⚠️ 분석할 내용이 없습니다!")
    else:
        client = OpenAI(api_key=api_key)
        system_prompt = "당신은 냉철한 보안 전문가입니다. RISK_LEVEL, REASON, ROAST 형식으로 한국어로 답변하세요. 아주 쉽고 명확하게 설명하세요."
        
        with st.spinner("🕵️‍♂️ 보안 전문가가 분석 중..."):
            try:
                if uploaded_file:
                    base_4_img = encode_image(uploaded_file)
                    messages = [{"role": "system", "content": system_prompt},
                                {"role": "user", "content": [{"type": "text", "text": user_input},
                                                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base_4_img}"}}]}]
                else:
                    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}]

                response = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
                
                # 결과 출력부 (CSS 적용)
                st.success("✅ 분석이 완료되었습니다!")
                st.markdown(f'<div class="result-text">{response.choices[0].message.content}</div>', unsafe_allow_html=True)
                st.balloons()
            except Exception as e:
                st.error(f"오류: {e}")

# --- [하단 쿠팡 배너: 가독성 보강] ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()
st.markdown("### 🛒 사기 예방 추천 아이템")

st.markdown(
    """
    <div style="display: flex; gap: 15px; justify-content: space-between; align-items: center;">
        <a href="https://www.coupang.com/np/search?component=&q=%ED%9A%A8%EB%8F%84%ED%8F%B0&channel=user" target="_blank" style="text-decoration: none; flex: 1;">
            <div class="banner-text" style="background-color: #E60012; color: white; padding: 20px 10px; border-radius: 12px; text-align: center; font-weight: bold; height: 80px; display: flex; align-items: center; justify-content: center; line-height: 1.2; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
                📱 사기예방<br>보안 효도폰
            </div>
        </a>
        <a href="https://www.coupang.com/np/search?component=&q=%EC%82%AC%EC%83%9D%ED%99%9C%EB%B3%B4%ED%98%B8%ED%95%84%EB%A6%84&channel=user" target="_blank" style="text-decoration: none; flex: 1;">
            <div class="banner-text" style="background-color: #0050FF; color: white; padding: 20px 10px; border-radius: 12px; text-align: center; font-weight: bold; height: 80px; display: flex; align-items: center; justify-content: center; line-height: 1.2; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
                👀 해킹방지<br>보호필름
            </div>
        </a>
    </div>
    <p style="font-size: 12px; color: gray; text-align: center; margin-top: 15px;">이 포스팅은 쿠팡 파트너스 활동의 일환으로 수수료를 제공받을 수 있습니다.</p>
    """, unsafe_allow_html=True
)

st.caption("© 2026 ScamBuster AI. All rights reserved.")

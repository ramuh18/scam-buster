import streamlit as st
from openai import OpenAI
import base64

# 1. 페이지 설정
st.set_page_config(
    page_title="ScamBuster AI",
    page_icon="🛡️",
    layout="wide"
)

# --- [반응형 디자인 CSS 추가] ---
# 모바일과 PC 환경에 따라 글씨 크기를 자동으로 맞춥니다.
st.markdown(
    """
    <style>
    /* 전체 텍스트 크기 조절 */
    html, body, [class*="st-"] {
        font-size: 16px;
    }
    
    /* 모바일 환경 (화면 너비가 768px 이하일 때) */
    @media (max-width: 768px) {
        h1 { font-size: 1.8rem !important; }
        h3 { font-size: 1.2rem !important; }
        .stTextArea textarea { font-size: 14px !important; }
        .stButton button { font-size: 15px !important; height: 3.5rem !important; }
        .banner-text { font-size: 12px !important; }
    }
    
    /* PC 환경 */
    @media (min-width: 769px) {
        h1 { font-size: 3rem !important; }
        h3 { font-size: 1.8rem !important; }
        .banner-text { font-size: 16px !important; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. 비밀 금고에서 열쇠 꺼내기
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = st.sidebar.text_input("🔑 관리자 키 입력", type="password")

# --- [사이드바] ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=80)
    st.title("🛡️ 보안 관제 센터")
    st.success("✅ AI 엔진 정상")
    st.divider()
    st.markdown("### 💡 보안 수칙")
    st.warning("• 출처 불명 링크 클릭 금지")
    st.warning("• 앱 설치 요구 시 즉시 차단")
    st.divider()
    st.write("본 AI는 최신 피싱 패턴을 분석합니다.")

# --- [메인 화면] ---
st.title("🕵️‍♂️ ScamBuster AI")
st.markdown("### \"사기 문자인지 3초 만에 판독\"")
st.write("문자 내용이나 스크린샷을 업로드해 보세요.")

st.divider()

# 분석 기능 (탭 메뉴)
tab1, tab2 = st.tabs(["📝 텍스트 입력", "📸 스크린샷 업로드"])

user_input = ""
uploaded_file = None

with tab1:
    user_input = st.text_area("의심스러운 내용을 입력하세요:", height=150, placeholder="내용을 여기에 붙여넣으세요...")

with tab2:
    uploaded_file = st.file_uploader("이미지 업로드", type=["jpg", "png", "jpeg"])

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# 분석 버튼
if st.button("🚨 사기 패턴 정밀 분석 시작", type="primary", use_container_width=True):
    if not api_key:
        st.error("API 키를 확인해 주세요.")
    elif not user_input and not uploaded_file:
        st.warning("⚠️ 분석할 내용이 없습니다.")
    else:
        client = OpenAI(api_key=api_key)
        system_prompt = "당신은 냉철한 보안 전문가입니다. RISK_LEVEL, REASON, ROAST 형식으로 한국어로 답변하세요."
        
        with st.spinner("🕵️‍♂️ 분석 중..."):
            try:
                if uploaded_file:
                    base_4_img = encode_image(uploaded_file)
                    messages = [{"role": "system", "content": system_prompt},
                                {"role": "user", "content": [{"type": "text", "text": user_input},
                                                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base_4_img}"}}]}]
                else:
                    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}]

                response = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
                st.success("✅ 분석 완료!")
                st.write(response.choices[0].message.content)
                st.balloons()
            except Exception as e:
                st.error(f"오류: {e}")

# --- [하단 쿠팡 배너: 모바일 최적화 글씨 크기] ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()
st.markdown("### 🛒 보안 전문가 추천 방어 아이템")

st.markdown(
    """
    <div style="display: flex; gap: 10px; justify-content: space-between; align-items: center;">
        <a href="https://www.coupang.com/np/search?component=&q=%ED%9A%A8%EB%8F%84%ED%8F%B0&channel=user" target="_blank" style="text-decoration: none; flex: 1;">
            <div class="banner-text" style="background-color: #E60012; color: white; padding: 15px 5px; border-radius: 10px; text-align: center; font-weight: bold; height: 65px; display: flex; align-items: center; justify-content: center; line-height: 1.2; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                📱 사기예방<br>보안 효도폰
            </div>
        </a>
        <a href="https://www.coupang.com/np/search?component=&q=%EC%82%AC%EC%83%9D%ED%99%9C%EB%B3%B4%ED%98%B8%ED%95%84%EB%A6%84&channel=user" target="_blank" style="text-decoration: none; flex: 1;">
            <div class="banner-text" style="background-color: #0050FF; color: white; padding: 15px 5px; border-radius: 10px; text-align: center; font-weight: bold; height: 65px; display: flex; align-items: center; justify-content: center; line-height: 1.2; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                👀 해킹방지<br>보호필름
            </div>
        </a>
    </div>
    <p style="font-size: 11px; color: gray; text-align: center; margin-top: 10px;">이 포스팅은 쿠팡 파트너스 활동의 일환으로, 일정액의 수수료를 제공받습니다.</p>
    """, unsafe_allow_html=True
)

st.caption("© 2026 ScamBuster AI. All rights reserved.")

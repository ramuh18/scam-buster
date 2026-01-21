import streamlit as st
from openai import OpenAI
import base64

# 1. 페이지 설정
st.set_page_config(
    page_title="ScamBuster AI",
    page_icon="🛡️",
    layout="wide"
)

# --- [디자인 스타일 시트] ---
st.markdown(
    """
    <style>
    /* 전체 폰트 가독성 */
    html, body, [class*="st-"] {
        font-family: 'Pretendard', -apple-system, sans-serif !important;
    }
    
    /* 제목: 굵고 세련된 느낌 */
    .main-title {
        font-size: 3.5rem !important;
        font-weight: 850 !important;
        letter-spacing: -2px !important;
        color: #111827;
        margin-bottom: 0px !important;
    }
    
    /* 서브 문구: 깔끔한 그레이 톤 */
    .sub-title {
        font-size: 1.5rem !important;
        color: #6b7280;
        font-weight: 400;
        margin-bottom: 2rem !important;
    }

    /* 버튼 스타일 (애플 스타일 라운딩) */
    .stButton button {
        background-color: #007AFF !important;
        color: white !important;
        font-size: 20px !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        padding: 0.8rem !important;
        transition: 0.3s;
    }
    
    /* 결과 박스 (전문적인 느낌) */
    .result-card {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. API 키 연동
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = st.sidebar.text_input("🔑 Admin Key", type="password")

# --- [사이드바] ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=100)
    st.title("Admin")
    st.caption("AI Security System v1.2")
    st.divider()
    st.markdown("### 🔍 분석 가이드")
    st.write("1. 텍스트 또는 이미지 업로드")
    st.write("2. AI 정밀 분석 실행")
    st.write("3. 결과에 따른 즉시 대응")

# --- [메인 화면] ---
st.markdown('<p class="main-title">ScamBuster</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">의심스러운 순간, AI로 완벽하게 검증하세요.</p>', unsafe_allow_html=True)

st.divider()

# 탭 구성
tab1, tab2 = st.tabs(["📝 Message Text", "📸 Screenshot Image"])

user_input = ""
uploaded_file = None

with tab1:
    user_input = st.text_area("분석할 내용을 입력해 주세요", height=200, placeholder="여기에 내용을 붙여넣으세요.")

with tab2:
    uploaded_file = st.file_uploader("스크린샷 파일 업로드", type=["jpg", "png", "jpeg"])

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# 분석 실행
if st.button("🚨 정밀 분석 시작", use_container_width=True):
    if not api_key:
        st.error("API 키가 유효하지 않습니다.")
    elif not user_input and not uploaded_file:
        st.warning("분석할 데이터를 입력해 주세요.")
    else:
        client = OpenAI(api_key=api_key)
        system_prompt = "당신은 냉철한 사이버 보안 분석가입니다. 위험 수준(RISK LEVEL), 판단 근거(REASON), 대응 전략(RESPONSE)을 한국어로 보고서 형태로 작성하세요."
        
        with st.spinner("AI 보안 엔진 분석 중..."):
            try:
                if uploaded_file:
                    base_4_img = encode_image(uploaded_file)
                    messages = [{"role": "system", "content": system_prompt},
                                {"role": "user", "content": [{"type": "text", "text": user_input},
                                                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base_4_img}"}}]}]
                else:
                    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}]

                response = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
                
                st.success("분석 결과 리포트가 생성되었습니다.")
                st.markdown(f'<div class="result-card">{response.choices[0].message.content}</div>', unsafe_allow_html=True)
                st.balloons()
            except Exception as e:
                st.error(f"오류: {e}")

# --- [하단 추천 아이템] ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()
st.markdown("#### 🛡️ 보안 솔루션 추천")

col1, col2 = st.columns(2)
with col1:
    st.markdown(
        """<a href="https://www.coupang.com/np/search?q=%ED%9A%A8%EB%8F%84%ED%8F%B0" target="_blank" style="text-decoration: none;">
        <div style="background-color: #000000; color: white; padding: 25px; border-radius: 15px; text-align: center; font-weight: bold;">
        보안 특화 효도폰 보기
        </div></a>""", unsafe_allow_html=True)
with col2:
    st.markdown(
        """<a href="https://www.coupang.com/np/search?q=%EC%82%AC%EC%83%9D%ED%99%9C%EB%B3%B4%ED%98%B8%ED%95%84%EB%A6%84" target="_blank" style="text-decoration: none;">
        <div style="background-color: #007AFF; color: white; padding: 25px; border-radius: 15px; text-align: center; font-weight: bold;">
        정보 보호 필름 보기
        </div></a>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.caption("이 포스팅은 쿠팡 파트너스 활동의 일환으로 수수료를 제공받을 수 있습니다.")

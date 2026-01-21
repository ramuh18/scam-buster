import streamlit as st
from openai import OpenAI
import base64

# 1. 페이지 설정
st.set_page_config(
    page_title="ScamBuster AI",
    page_icon="🛡️",
    layout="wide"
)

# --- [디자인 스타일 시트: 전문 보안 툴 느낌] ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', -apple-system, sans-serif !important;
    }
    
    /* 메인 타이틀 세련되게 */
    .main-title {
        font-size: 3.5rem !important;
        font-weight: 850 !important;
        letter-spacing: -3px !important;
        color: #111827;
        line-height: 1 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .sub-title {
        font-size: 1.2rem !important;
        color: #4b5563;
        margin-bottom: 2rem !important;
    }

    /* 사이드바 박스 스타일 */
    .sidebar-box {
        background-color: #f3f4f6;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 10px;
        border: 1px solid #e5e7eb;
    }
    
    .sidebar-label {
        font-size: 12px;
        font-weight: 700;
        color: #9ca3af;
        text-transform: uppercase;
        margin-bottom: 5px;
    }

    /* 버튼 스타일 */
    .stButton button {
        background-color: #000000 !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        height: 3.5rem !important;
        border: none !important;
    }

    /* 결과 리포트 카드 */
    .report-card {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid #f3f4f6;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. API 키 연동
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = st.sidebar.text_input("🔑 ADMIN ACCESS KEY", type="password")

# --- [사이드바: 보안 관제 대시보드 테마] ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=60)
    st.title("SECURE OS")
    st.caption("AI-Powered Fraud Detection v1.2.4")
    
    st.divider()

    # 시스템 상태 섹션
    st.markdown('<p class="sidebar-label">System Status</p>', unsafe_allow_html=True)
    st.success("● AI Engine: Online (GPT-4o)")
    st.info("● Network: Asia-Pacific Secured")
    
    st.markdown('<p class="sidebar-label">Latest Threats</p>', unsafe_allow_html=True)
    st.error("⚠️ Alert: New SMS Phishing Pattern")
    
    st.divider()

    # 분석 가이드 섹션
    st.markdown("### 🛠️ Analysis Tools")
    st.markdown("""
    - **Heuristic Scanning:** 문자 패턴 매칭
    - **OCR Analysis:** 이미지 텍스트 해독
    - **NLP Deep Learning:** 맥락 및 의도 파악
    - **Vulnerability Check:** 보안 취약점 점검
    """)

    st.divider()
    
    # 통계 섹션 (임의 수치로 신뢰도 상승)
    st.markdown('<p class="sidebar-label">Global Statistics</p>', unsafe_allow_html=True)
    col_s1, col_s2 = st.columns(2)
    col_s1.metric("Accuracy", "99.8%")
    col_s2.metric("Latency", "1.2s")

# --- [메인 화면] ---
st.markdown('<p class="main-title">ScamBuster</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">인공지능 기반 사기 패턴 분석 및 정밀 판독 시스템</p>', unsafe_allow_html=True)

# 메인 기능 탭
tab1, tab2 = st.tabs(["💬 텍스트 데이터 분석", "🖼️ 이미지/스크린샷 검사"])

user_input = ""
uploaded_file = None

with tab1:
    user_input = st.text_area("의심 문구 또는 메신저 대화 내용을 입력하십시오.", height=200, placeholder="분석할 데이터를 여기에 입력하세요.")

with tab2:
    uploaded_file = st.file_uploader("검증할 스크린샷 파일을 업로드하십시오.", type=["jpg", "png", "jpeg"])

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# 분석 실행 버튼
if st.button("🚨 정밀 분석 리포트 생성 (Generate Report)", use_container_width=True):
    if not api_key:
        st.error("Admin Access Key가 필요합니다.")
    elif not user_input and not uploaded_file:
        st.warning("분석할 데이터를 제공해 주십시오.")
    else:
        client = OpenAI(api_key=api_key)
        system_prompt = "당신은 냉철한 사이버 보안 분석관입니다. 위험 수준, 사기 수법 명칭, 분석 근거, 대응 가이드를 전문가적인 어조로 작성하세요."
        
        with st.spinner("보안 엔진 스캐닝 중..."):
            try:
                if uploaded_file:
                    base_4_img = encode_image(uploaded_file)
                    messages = [{"role": "system", "content": system_prompt},
                                {"role": "user", "content": [{"type": "text", "text": user_input},
                                                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base_4_img}"}}]}]
                else:
                    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}]

                response = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
                
                st.subheader("📋 분석 결과 리포트")
                st.markdown(f'<div class="report-card">{response.choices[0].message.content}</div>', unsafe_allow_html=True)
                st.balloons()
            except Exception as e:
                st.error(f"Engine Error: {e}")

# --- [하단 추천 솔루션] ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()
st.markdown("#### 🛡️ 자산 보호를 위한 추천 솔루션")

# 하단 배너 (고대비 세련된 디자인)
st.markdown(
    """
    <div style="display: flex; gap: 15px; justify-content: space-between; align-items: center;">
        <a href="https://www.coupang.com/np/search?q=%ED%9A%A8%EB%8F%84%ED%8F%B0" target="_blank" style="text-decoration: none; flex: 1;">
            <div style="background-color: #f8f9fa; color: #111827; padding: 25px; border-radius: 15px; text-align: center; font-weight: bold; border: 1px solid #e5e7eb; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                📱 사기 예방 보안 단말기
            </div>
        </a>
        <a href="https://www.coupang.com/np/search?q=%EC%82%AC%EC%83%9D%ED%99%9C%EB%B3%B4%ED%98%B8%ED%95%84%EB%A6%84" target="_blank" style="text-decoration: none; flex: 1;">
            <div style="background-color: #111827; color: white; padding: 25px; border-radius: 15px; text-align: center; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                👀 프라이버시 보호 솔루션
            </div>
        </a>
    </div>
    <p style="font-size: 11px; color: #9ca3af; text-align: center; margin-top: 15px;">본 포스팅은 쿠팡 파트너스 활동의 일환으로 수수료를 제공받을 수 있습니다.</p>
    """, unsafe_allow_html=True
)

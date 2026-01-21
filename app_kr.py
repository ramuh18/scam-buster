import streamlit as st
from openai import OpenAI
import base64

# 1. 페이지 설정
st.set_page_config(
    page_title="ScamBuster AI",
    page_icon="🛡️",
    layout="wide"
)

# 2. 비밀 금고에서 열쇠 꺼내기
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = st.sidebar.text_input("🔑 관리자 키 입력", type="password")

# --- [사이드바] 모바일 최적화 배너 버전 ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=80) 
    st.title("🛡️ ScamBuster")
    st.markdown("**대한민국 사기 방지 시스템**")
    
    st.divider()
    
    # 1. 사용법 안내
    st.markdown("### 📖 사용법")
    st.info(
        """
        1. 스크린샷 **업로드** 📸
        2. 또는 내용 **붙여넣기** 📝
        3. **분석 시작** 클릭 🚨
        """
    )
    
    st.divider()

    # 2. 실시간 카운터
    st.markdown("### 📊 Scams Blocked")
    st.markdown(
        "[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fscam-buster-kbxdvib6ghejadljolbgsb.streamlit.app&count_bg=%23FF4B4B&title_bg=%23555555&icon=shield.svg&icon_color=%23E7E7E7&title=Total+Blocked&edge_flat=false)](https://hits.seeyoufarm.com)"
    )
    
    st.divider()

    # 3. 프로젝트 후원 & 쿠팡 파트너스 (모바일 나란히 배치)
    st.markdown("### 💖 프로젝트 후원")
    
    # 모바일에서도 무조건 나란히 보이게 하는 HTML/CSS
    st.markdown(
        """
        <div style="display: flex; gap: 10px; justify-content: space-between; align-items: center;">
            <a href="https://www.coupang.com/np/search?component=&q=%ED%9A%A8%EB%8F%84%ED%8F%B0&channel=user" target="_blank" style="text-decoration: none; flex: 1;">
                <div style="background-color: #E60012; color: white; padding: 10px 5px; border-radius: 8px; text-align: center; font-size: 11px; font-weight: bold; height: 55px; display: flex; align-items: center; justify-content: center; line-height: 1.2;">
                    📱 보안<br>효도폰
                </div>
            </a>
            <a href="https://www.coupang.com/np/search?component=&q=%EC%82%AC%EC%83%9D%ED%99%9C%EB%B3%B4%ED%98%B8%ED%95%84%EB%A6%84&channel=user" target="_blank" style="text-decoration: none; flex: 1;">
                <div style="background-color: #0050FF; color: white; padding: 10px 5px; border-radius: 8px; text-align: center; font-size: 11px; font-weight: bold; height: 55px; display: flex; align-items: center; justify-content: center; line-height: 1.2;">
                    👀 사생활<br>보호필름
                </div>
            </a>
        </div>
        """, unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.")

# --- [메인 화면] ---
col_main_1, col_main_2 = st.columns([2, 1])

with col_main_1:
    st.title("🕵️‍♂️ ScamBuster AI")
    st.markdown("### \"이거 사기 아닐까?\"")
    st.markdown("AI가 문자와 이미지를 분석하여 위험을 찾아내고, 사이다 답장을 써드립니다.")

with col_main_2:
    st.warning("⚠️ **최신 트렌드:** '토스 사기계좌 조회' 수법을 주의하세요!")

st.markdown("---")

# 탭 메뉴
tab1, tab2 = st.tabs(["📝 텍스트 분석", "📸 스크린샷 분석"])

user_input = ""
uploaded_file = None

with tab1:
    st.markdown("의심스러운 내용을 입력하세요:")
    user_input = st.text_area("내용:", height=150, placeholder="여기에 붙여넣으세요...")

with tab2:
    st.markdown("스크린샷을 업로드하세요:")
    uploaded_file = st.file_uploader("이미지 업로드", type=["jpg", "png", "jpeg"])

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

if st.button("🚨 분석 및 팩트폭격 시작", type="primary", use_container_width=True):
    if not api_key:
        st.error("API 키가 없습니다.")
    elif not user_input and not uploaded_file:
        st.warning("⚠️ 내용을 입력해주세요!")
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

st.markdown("---")
st.caption("© 2026 ScamBuster AI. 이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.")

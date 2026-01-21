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

# --- [메인 상단: 모바일 최적화 영역] ---
# 모바일에서 바로 보이도록 메인 화면 최상단에 배치
st.title("🕵️‍♂️ ScamBuster AI")

# 방문자 카운터 (오늘 방문자 / 전체 방문자)
# 사장님 주소 기반으로 오늘(Today) 수치도 나오게 설정했습니다.
st.markdown(
    """
    <div style="display: flex; gap: 5px; margin-bottom: 10px;">
        <img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fscam-buster-kbxdvib6ghejadljolbgsb.streamlit.app&count_bg=%23FF4B4B&title_bg=%23555555&icon=shield.svg&icon_color=%23E7E7E7&title=Total+Blocked&edge_flat=false"/>
        <img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fscam-buster-kbxdvib6ghejadljolbgsb.streamlit.app&count_bg=%23238636&title_bg=%23555555&icon=check.svg&icon_color=%23E7E7E7&title=Today&edge_flat=false"/>
    </div>
    """, unsafe_allow_html=True
)

# 모바일에서도 무조건 나란히 보이는 빨간색 효도폰 배너 세트
st.markdown(
    """
    <div style="display: flex; gap: 10px; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <a href="https://www.coupang.com/np/search?component=&q=%ED%9A%A8%EB%8F%84%ED%8F%B0&channel=user" target="_blank" style="text-decoration: none; flex: 1;">
            <div style="background-color: #E60012; color: white; padding: 10px 5px; border-radius: 8px; text-align: center; font-size: 11px; font-weight: bold; height: 55px; display: flex; align-items: center; justify-content: center; line-height: 1.2; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
                📱 보안<br>효도폰
            </div>
        </a>
        <a href="https://www.coupang.com/np/search?component=&q=%EC%82%AC%EC%83%9D%ED%99%9C%EB%B3%B4%ED%98%B8%ED%95%84%EB%A6%84&channel=user" target="_blank" style="text-decoration: none; flex: 1;">
            <div style="background-color: #0050FF; color: white; padding: 10px 5px; border-radius: 8px; text-align: center; font-size: 11px; font-weight: bold; height: 55px; display: flex; align-items: center; justify-content: center; line-height: 1.2; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
                👀 사생활<br>보호필름
            </div>
        </a>
    </div>
    <p style="font-size: 10px; color: gray; margin-top: -10px;">이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.</p>
    """, unsafe_allow_html=True
)

st.markdown("### \"이거 사기 아닐까?\"")
st.write("AI가 문자와 이미지를 분석하여 위험을 찾아내고, 사이다 답장을 써드립니다.")

# --- [사이드바] ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=60)
    st.title("🛡️ ScamBuster")
    st.info("사기 문자를 분석하고 대응하세요.")

st.divider()

# --- [메인 기능: 탭 메뉴] ---
tab1, tab2 = st.tabs(["📝 텍스트 분석", "📸 스크린샷 분석"])

user_input = ""
uploaded_file = None

with tab1:
    user_input = st.text_area("의심스러운 내용을 입력하세요:", height=150)

with tab2:
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

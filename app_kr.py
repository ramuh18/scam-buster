import streamlit as st
from openai import OpenAI
import base64

# --- [1] 디자인 마법 걸기 (CSS 주입) ---
st.set_page_config(
    page_title="스팸버스터 AI",
    page_icon="🛡️",
    layout="centered"
)

# 커스텀 CSS 적용 (부드러운 디자인)
st.markdown(
    """
    <style>
    /* 전체 배경을 은은한 블루 그라데이션으로 */
    .stApp {
        background: linear-gradient(to bottom right, #f0f2f6, #e2eafc);
    }
    /* 메인 컨테이너를 카드처럼 둥글게 */
    .main .block-container {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    /* 제목 스타일 */
    h1 {
        color: #1a237e;
        font-weight: 800;
    }
    /* 서브 제목 스타일 */
    h3 {
        color: #283593;
    }
    /* 버튼 스타일 (스트림릿 기본 버튼도 둥글게) */
    .stButton>button {
        border-radius: 20px;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- [2] 비밀 열쇠 연동 ---
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = st.sidebar.text_input("🔑 관리자 키 입력", type="password")

# --- [3] 헤더 & 카운터 배지 ---
# 딱딱한 텍스트 대신 이모지와 함께 부드럽게 배치
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("🛡️ 스팸버스터 AI")
    st.caption("대한민국 No.1 사기 문자/피싱 판별 솔루션")
with col_h2:
    # 배지 오른쪽 정렬 및 디자인
    st.markdown(
        """
        <div style="text-align: right; padding-top: 20px;">
            <img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fscam-buster-kbxdvib6ghejadljolbgsb.streamlit.app&count_bg=%234c6ef5&title_bg=%23343a40&icon=shield.svg&icon_color=%23ffffff&title=분석+완료&edge_flat=false" style="border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.2);"/>
        </div>
        """, unsafe_allow_html=True
    )

st.markdown("---")

# --- [4] 입력 섹션 (부드러운 안내) ---
st.info("👋 안녕하세요! 의심스러운 문자, 카톡 캡처, 전화번호가 있나요? 아래에 입력해주시면 AI가 즉시 분석합니다.")

# 입력창들을 담는 깔끔한 컨테이너
with st.container():
    col1, col2 = st.columns([1, 1.5], gap="medium")
    with col1:
        st.markdown("##### 📸 이미지로 넣기")
        uploaded_file = st.file_uploader("캡처 화면 업로드", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
    with col2:
        st.markdown("##### 📝 텍스트로 넣기")
        user_input = st.text_area("내용을 붙여넣으세요", height=130, placeholder="예: [국외발신] 결제가 완료되었습니다... (전화번호 포함 가능)")

# 이미지 변환 함수
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# --- [5] 분석 버튼 (강조) ---
st.markdown("<br>", unsafe_allow_html=True) # 간격 띄우기
# 버튼을 중앙에 크고 예쁘게 배치
if st.button("🚀 AI 무료 정밀 분석 시작하기", type="primary", use_container_width=True):
    if not api_key:
        st.error("⚠️ 서버 연결 오류: 관리자에게 문의하세요.")
    elif not user_input and not uploaded_file:
        st.warning("⚠️ 분석할 내용이나 이미지를 먼저 입력해주세요!")
    else:
        client = OpenAI(api_key=api_key)
        
        # 페르소나 설정
        system_prompt = """
        당신은 대한민국 최고의 사이버 보안 전문가이자 유머러스한 '팩트 폭격기'입니다.
        사용자가 입력한 텍스트나 이미지가 스팸/사기인지 정밀 분석하세요.
        
        [분석 리포트 형식]
        1. 🚨 **위험 등급**: (안전 ✅ / 주의 ⚠️ / 위험 🚫 / 매우 치명적 💀) 중에서 선택.
        2. 🔍 **팩트 체크**: 왜 이것이 사기인지(또는 아닌지) 초등학생도 이해하게 1문장으로 요약.
        3. 🤬 **사이다 대응**: 사기꾼에게 보낼 수 있는 아주 웃기고 신랄한 답장 또는 현실적인 대처법.
        """
        
        with st.spinner("🕵️‍♂️ AI가 데이터를 분석 중입니다... 잠시만 기다려주세요."):
            try:
                if uploaded_file:
                    base64_image = encode_image(uploaded_file)
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": [
                            {"type": "text", "text": f"이 이미지와 텍스트를 분석해줘: {user_input}"},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]}
                    ]
                else:
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ]

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    max_tokens=800
                )
                result = response.choices[0].message.content
                
                st.success("✅ 분석이 완료되었습니다!")
                # 결과를 예쁜 박스에 담아서 보여줌
                st.markdown(
                    f"""
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #4c6ef5;">
                        {result}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.balloons()
                
            except Exception as e:
                st.error(f"분석 중 오류가 발생했습니다: {e}")

# --- [6] 하단 배너 (앱 스타일 버튼 적용) ---
st.markdown("---")
st.subheader("🛡️ 보안 전문가 추천 필수템")
st.caption("사기 예방을 위한 가장 확실한 투자입니다.")

col_a, col_b = st.columns(2, gap="medium")

# 쿠팡 링크는 사장님 걸로 꼭 바꾸세요!
coupang_link_1 = "https://www.coupang.com/np/search?component=&q=%ED%9A%A8%EB%8F%84%ED%8F%B0&channel=user"
coupang_link_2 = "https://www.coupang.com/np/search?component=&q=%EC%82%AC%EC%83%9D%ED%99%9C%EB%B3%B4%ED%98%B8%ED%95%84%EB%A6%84&channel=user"

with col_a:
    st.markdown(
        f"""
        <a href="{coupang_link_1}" target="_blank" style="text-decoration: none;">
            <div style="background: linear-gradient(45deg, #ff6b6b, #f06595); padding: 15px; border-radius: 15px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: 0.3s;">
                <div style="font-size: 24px;">📱</div>
                <div style="font-weight: bold; margin-top: 5px;">부모님 효도폰 보기</div>
                <div style="font-size: 12px; opacity: 0.8;">해킹 방지 최신폰</div>
            </div>
        </a>
        """, unsafe_allow_html=True
    )

with col_b:
    st.markdown(
        f"""
        <a href="{coupang_link_2}" target="_blank" style="text-decoration: none;">
            <div style="background: linear-gradient(45deg, #339af0, #5c7cfa); padding: 15px; border-radius: 15px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: 0.3s;">
                <div style="font-size: 24px;">👀</div>
                <div style="font-weight: bold; margin-top: 5px;">사생활 보호 필름</div>
                <div style="font-size: 12px; opacity: 0.8;">옆에서 안 보여요</div>
            </div>
        </a>
        """, unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)
st.caption("© 2026 ScamBuster AI. | 이 서비스는 쿠팡 파트너스 활동의 일환으로 수수료를 제공받을 수 있습니다.")

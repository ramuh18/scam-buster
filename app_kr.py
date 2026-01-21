import streamlit as st
from openai import OpenAI
import base64

# --- [1] 페이지 기본 설정 ---
st.set_page_config(
    page_title="스팸버스터 AI - 사기 문자 판독기",
    page_icon="🛡️",
    layout="centered"
)

# --- [2] 디자인: '다크 사이버 테마' (사장님 Pick!) ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0f1116;
    }
    .main .block-container {
        background-color: #1c1f26;
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid #2d333b;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    h1 {
        color: #00ff41 !important;
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 10px rgba(0,255,65,0.3);
    }
    p, .stMarkdown, h3, h5, div, span {
        color: #e6edf3 !important;
    }
    .stTextArea textarea {
        background-color: #0d1117;
        color: white;
        border: 1px solid #30363d;
    }
    .stButton>button {
        background-color: #238636;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        height: 3em;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #2ea043;
        border: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- [3] 비밀 열쇠 연동 ---
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = st.sidebar.text_input("🔑 관리자 키 입력", type="password")

# --- [4] 헤더 및 카운터 배지 ---
st.title("🛡️ SCAM BUSTER")
st.markdown("### 🇰🇷 대한민국 사기 문자 AI 판독기")

# 방문자 카운터 (사장님 확정 주소 연동)
st.markdown(
    """
    <a href="https://hits.seeyoufarm.com">
        <img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fscam-buster-kbxdvib6ghejadljolbgsb.streamlit.app&count_bg=%23238636&title_bg=%230d1117&icon=shield.svg&icon_color=%23ffffff&title=VISITS&edge_flat=false"/>
    </a>
    """,
    unsafe_allow_html=True
)
st.markdown("---")

# --- [5] 입력 섹션 ---
st.info("💡 의심스러운 문자 텍스트를 복사해서 넣거나 스크린샷을 올려주세요.")

col1, col2 = st.columns([1, 1.5], gap="medium")
with col1:
    st.markdown("##### 📸 스크린샷")
    uploaded_file = st.file_uploader("이미지 업로드", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
with col2:
    st.markdown("##### 📝 문자 내용")
    user_input = st.text_area("내용 입력", height=130, placeholder="예: [국외발신] 결제 완료 문의 006-...")

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# --- [6] 분석 버튼 및 로직 ---
if st.button("🚀 사기 여부 정밀 분석 시작"):
    if not api_key:
        st.error("⚠️ 관리자 키가 설정되지 않았습니다.")
    elif not user_input and not uploaded_file:
        st.warning("⚠️ 분석할 내용을 입력해주세요!")
    else:
        client = OpenAI(api_key=api_key)
        
        system_prompt = """
        당신은 대한민국 최고의 사이버 보안 전문가입니다. 
        냉철하고 정확하게 사기 패턴을 분석하세요.
        말투는 전문가답고 단호하게 하되, 사기꾼에게는 따끔한 일침(Roast)을 가하세요.
        
        [분석 리포트]
        1. 🚨 위험 등급: (안전 / 주의 / 위험 / 치명적)
        2. 🔍 팩트 체크: 왜 이것이 사기인지 전문가의 시선으로 1문장 요약.
        3. 🛡️ 대응 가이드: 지금 즉시 해야 할 행동 요령.
        4. 🔥 한줄 팩폭: 사기꾼에게 날리는 시원한 한마디.
        """
        
        with st.spinner("AI가 사기 수법을 정밀 해독 중입니다..."):
            try:
                if uploaded_file:
                    base64_image = encode_image(uploaded_file)
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": [
                            {"type": "text", "text": f"이 내용을 분석해줘: {user_input}"},
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
                
                st.success("✅ 분석 완료!")
                st.markdown(f"""<div style="background-color: #21262d; padding: 20px; border-radius: 10px; border: 1px solid #30363d;">{result}</div>""", unsafe_allow_html=True)
                st.balloons()
                
            except Exception as e:
                st.error(f"오류 발생: {e}")

# --- [7] 하단 섹션: 쿠팡 파트너스 (수익 모델) ---
st.markdown("---")
st.subheader("🛡️ 보안 전문가 추천 아이템")

c1, c2 = st.columns(2)
with c1:
    # 효도폰 링크
    st.markdown(
        """
        <a href="https://www.coupang.com/np/search?component=&q=%ED%9A%A8%EB%8F%84%ED%8F%B0&channel=user" target="_blank" style="text-decoration: none;">
            <div style="background-color: #d32f2f; padding: 15px; border-radius: 10px; color: white; text-align: center;">
                <div style="font-size: 18px; font-weight: bold;">📱 해킹방지 효도폰</div>
                <div style="font-size: 12px;">부모님 사기 예방 필수</div>
            </div>
        </a>
        """, unsafe_allow_html=True
    )
with c2:
    # 보호필름 링크
    st.markdown(
        """
        <a href="https://www.coupang.com/np/search?component=&q=%EC%82%AC%EC%83%9D%ED%99%9C%EB%B3%B4%ED%98%B8%ED%95%84%EB%A6%84&channel=user" target="_blank" style="text-decoration: none;">
            <div style="background-color: #1976d2; padding: 15px; border-radius: 10px; color: white; text-align: center;">
                <div style="font-size: 18px; font-weight: bold;">👀 사생활 보호필름</div>
                <div style="font-size: 12px;">옆사람 엿보기 차단</div>
            </div>
        </a>
        """, unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)
st.caption("© 2026 ScamBuster AI. (이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다)")

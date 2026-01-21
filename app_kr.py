import streamlit as st
from openai import OpenAI
import base64

# --- [1] 디자인: '다크 사이버 테마' (가독성 최우선) ---
st.set_page_config(
    page_title="스팸버스터 AI",
    page_icon="🛡️",
    layout="centered"
)

# 다크 모드 CSS (검은 배경 + 흰 글씨 + 네온 포인트)
st.markdown(
    """
    <style>
    /* 전체 배경: 아주 진한 남색 (눈이 편안함) */
    .stApp {
        background-color: #0f1116;
    }
    /* 메인 카드: 조금 더 밝은 검은색 */
    .main .block-container {
        background-color: #1c1f26;
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid #2d333b;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    /* 제목: 형광 연두색 (사이버 보안 느낌) */
    h1 {
        color: #00ff41 !important;
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 10px rgba(0,255,65,0.3);
    }
    /* 설명 글씨: 밝은 흰색 */
    p, .stMarkdown, h3, h5, div {
        color: #e6edf3 !important;
    }
    /* 입력창 배경 */
    .stTextArea textarea {
        background-color: #0d1117;
        color: white;
        border: 1px solid #30363d;
    }
    /* 버튼 스타일 */
    .stButton>button {
        background-color: #238636;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #2ea043;
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
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("🛡️ SCAM BUSTER")
    st.markdown("### 🇰🇷 대한민국 사기 문자 판독기")
with col_h2:
    st.markdown(
        """
        <div style="text-align: right; padding-top: 20px;">
            <img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fscam-buster-kbxdvib6ghejadljolbgsb.streamlit.app&count_bg=%23238636&title_bg=%230d1117&icon=shield.svg&icon_color=%23ffffff&title=BLOCK&edge_flat=true"/>
        </div>
        """, unsafe_allow_html=True
    )

st.markdown("---")

# --- [4] 입력 섹션 ---
st.info("💡 팁: 어두운 곳에서도 잘 보이는 '다크 모드'입니다. 텍스트나 이미지를 넣어주세요.")

with st.container():
    col1, col2 = st.columns([1, 1.5], gap="medium")
    with col1:
        st.markdown("##### 📸 이미지 (캡처)")
        uploaded_file = st.file_uploader("이미지 업로드", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
    with col2:
        st.markdown("##### 📝 텍스트 (문자)")
        user_input = st.text_area("내용 입력", height=130, placeholder="예: [국외발신] 006-1234... (번호나 내용 붙여넣기)")

# 이미지 변환 함수
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# --- [5] 분석 버튼 ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 분석 시작 (ANALYZE)", type="primary", use_container_width=True):
    if not api_key:
        st.error("⚠️ 관리자 키가 필요합니다.")
    elif not user_input and not uploaded_file:
        st.warning("⚠️ 내용을 입력해주세요!")
    else:
        client = OpenAI(api_key=api_key)
        
        system_prompt = """
        당신은 대한민국 최고의 사이버 보안 전문가입니다.
        사용자가 입력한 텍스트나 이미지가 스팸/사기인지 정밀 분석하세요.
        말투는 전문가답고 단호하게 하세요.
        
        [분석 리포트]
        1. 🚨 **위험 등급**: (안전 / 주의 / 위험 / 치명적)
        2. 🔍 **팩트 체크**: 왜 이것이 사기인지 1문장 요약.
        3. 🛡️ **대응 가이드**: 현실적인 대처법 및 답장 가이드.
        """
        
        with st.spinner("데이터 해독 중... (Decoding)"):
            try:
                if uploaded_file:
                    base64_image = encode_image(uploaded_file)
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": [
                            {"type": "text", "text": f"분석해줘: {user_input}"},
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
                
                st.success("✅ 분석 완료 (COMPLETE)")
                # 결과창 디자인 (어두운 배경에 밝은 글씨)
                st.markdown(
                    f"""
                    <div style="background-color: #21262d; padding: 20px; border-radius: 10px; border: 1px solid #30363d;">
                        <span style="color: #e6edf3;">{result}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
            except Exception as e:
                st.error(f"오류 발생: {e}")

# --- [6] 하단 배너 (쿠팡 파트너스) ---
st.markdown("---")
st.subheader("🛡️ 보안 추천 (SECURITY)")

col_a, col_b = st.columns(2, gap="medium")

# 사장님 쿠팡 링크로 변경 필요!
coupang_link_1 = "https://link.coupang.com/a/dwKVLj"
coupang_link_2 = "https://link.coupang.com/a/dwKH4v"

with col_a:
    st.markdown(
        f"""
        <a href="{coupang_link_1}" target="_blank" style="text-decoration: none;">
            <div style="background-color: #d32f2f; padding: 15px; border-radius: 10px; color: white; text-align: center; border: 1px solid #f44336;">
                <div style="font-size: 20px; font-weight: bold;">📱 해킹 방지 효도폰</div>
                <div style="font-size: 12px; opacity: 0.9;">부모님 필수품</div>
            </div>
        </a>
        """, unsafe_allow_html=True
    )

with col_b:
    st.markdown(
        f"""
        <a href="{coupang_link_2}" target="_blank" style="text-decoration: none;">
            <div style="background-color: #1976d2; padding: 15px; border-radius: 10px; color: white; text-align: center; border: 1px solid #2196f3;">
                <div style="font-size: 20px; font-weight: bold;">👀 사생활 보호 필름</div>
                <div style="font-size: 12px; opacity: 0.9;">엿보기 방지</div>
            </div>
        </a>
        """, unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)
st.caption("© 2026 ScamBuster AI. (이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.)")

import streamlit as st
from openai import OpenAI
import base64

# --- [1] 페이지 기본 설정 ---
st.set_page_config(
    page_title="스팸버스터 AI",
    page_icon="🛡️",
    layout="centered"
)

# --- [2] 디자인: '글로벌 화이트 테마' (깔끔하고 전문적인 느낌) ---
st.markdown(
    """
    <style>
    /* 전체 배경: 아주 연한 회색 (눈이 편안함) */
    .stApp {
        background-color: #f8f9fa;
    }
    /* 메인 카드: 깨끗한 흰색 + 부드러운 그림자 */
    .main .block-container {
        background-color: #ffffff;
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.05);
    }
    /* 제목 스타일: 진한 남색 (신뢰감) */
    h1 {
        color: #111827 !important;
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0px;
    }
    /* 본문 텍스트: 진한 회색 */
    p, .stMarkdown, h3, h5, div, li, span {
        color: #374151 !important;
        line-height: 1.6;
    }
    /* 입력창 스타일 */
    .stTextArea textarea {
        background-color: #f9fafb;
        color: #111827;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
    }
    .stTextArea textarea:focus {
        border: 1px solid #2563eb;
        box-shadow: 0 0 0 2px rgba(37,99,235,0.1);
    }
    /* 분석 버튼: 신뢰의 '로얄 블루' */
    .stButton>button {
        background-color: #2563eb;
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 16px;
        box-shadow: 0 4px 6px rgba(37,99,235,0.2);
        transition: 0.2s;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
        transform: translateY(-2px);
    }
    /* 결과 박스 및 정보창 */
    .stAlert {
        background-color: #eff6ff;
        border: 1px solid #bfdbfe;
        color: #1e40af;
        border-radius: 10px;
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

# --- [4] 헤더 & 심플 카운터 ---
st.title("ScamBuster AI")
st.caption("🇰🇷 대한민국 사기 문자/스미싱 판독기")

# 카운터 배지: 깔끔한 블루 스타일 (사장님 주소 적용)
st.markdown("[![Visits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fscam-buster-kbxdvib6ghejadljolbgsb.streamlit.app&count_bg=%232563EB&title_bg=%231F2937&icon=&icon_color=%23E7E7E7&title=Users&edge_flat=true)](https://hits.seeyoufarm.com)")

st.markdown("---")

# --- [5] 입력 섹션 ---
st.info("👋 안녕하세요! 006 국제발신, 택배 문자, 카톡 등 의심되는 내용을 넣어주세요.")

with st.container():
    col1, col2 = st.columns([1, 2], gap="medium")
    with col1:
        st.markdown("##### 📸 이미지 (캡처)")
        uploaded_file = st.file_uploader("이미지 업로드", type=["jpg", "png", "jpeg"], label_visibility="collapsed")
    with col2:
        st.markdown("##### 📝 텍스트 (문자)")
        user_input = st.text_area("내용 입력", height=130, placeholder="여기에 내용을 붙여넣으세요 (예: [국외발신] 98만원 결제...)")

# 이미지 변환 함수
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# --- [6] 분석 버튼 ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 사기 여부 무료 분석하기", type="primary", use_container_width=True):
    if not api_key:
        st.error("⚠️ 관리자 키가 필요합니다.")
    elif not user_input and not uploaded_file:
        st.warning("⚠️ 분석할 내용을 입력해주세요!")
    else:
        client = OpenAI(api_key=api_key)
        
        system_prompt = """
        당신은 대한민국 최고의 사이버 보안 전문가입니다.
        사용자가 입력한 텍스트나 이미지가 스팸/사기인지 정밀 분석하세요.
        
        [분석 리포트 형식]
        1. 🛡️ **판결**: (안전 / 주의 / 위험 / 치명적)
        2. 📝 **팩트체크**: 왜 이것이 사기인지 전문가 관점에서 1문장 요약.
        3. 💬 **대처법**: 사용자에게 추천하는 행동 (차단, 무시, 신고 등).
        """
        
        with st.spinner("AI가 데이터를 분석 중입니다..."):
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
                
                st.success("분석이 완료되었습니다!")
                # 결과창: 깔끔한 그레이 박스 + 파란색 포인트
                st.markdown(
                    f"""
                    <div style="background-color: #f3f4f6; padding: 25px; border-radius: 12px; border-left: 5px solid #2563eb; color: #1f2937;">
                        {result}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
            except Exception as e:
                st.error(f"오류 발생: {e}")

# --- [7] 하단 추천 (쿠팡 파트너스 - 깔끔한 디자인 적용) ---
st.markdown("---")
st.subheader("🔒 보안 전문가 추천 아이템")

col_a, col_b = st.columns(2, gap="medium")

# ★ 사장님 쿠팡 링크 ★
coupang_link_1 = "https://www.coupang.com/np/search?component=&q=%ED%9A%A8%EB%8F%84%ED%8F%B0&channel=user"
coupang_link_2 = "https://www.coupang.com/np/search?component=&q=%EC%82%AC%EC%83%9D%ED%99%9C%EB%B3%B4%ED%98%B8%ED%95%84%EB%A6%84&channel=user"

with col_a:
    st.markdown(
        f"""
        <a href="{coupang_link_1}" target="_blank" style="text-decoration: none;">
            <div style="background-color: #111827; padding: 20px; border-radius: 12px; color: white; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.1); transition: 0.3s;">
                <div style="font-size: 20px;">📱</div>
                <div style="font-weight: 600; margin-top:5px;">해킹 방지 효도폰</div>
                <div style="font-size: 12px; color: #9ca3af;">부모님 필수품</div>
            </div>
        </a>
        """, unsafe_allow_html=True
    )

with col_b:
    st.markdown(
        f"""
        <a href="{coupang_link_2}" target="_blank" style="text-decoration: none;">
            <div style="background-color: #ffffff; border: 1px solid #e5e7eb; padding: 20px; border-radius: 12px; color: #111827; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.05); transition: 0.3s;">
                <div style="font-size: 20px;">👀</div>
                <div style="font-weight: 600; margin-top:5px;">사생활 보호 필름</div>
                <div style="font-size: 12px; color: #6b7280;">옆사람 엿보기 방지</div>
            </div>
        </a>
        """, unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)
st.caption("© 2026 ScamBuster AI. 이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.")

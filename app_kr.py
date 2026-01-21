import streamlit as st
from openai import OpenAI
import base64

# --- [1] 페이지 기본 설정 ---
st.set_page_config(
    page_title="스팸버스터 AI",
    page_icon="🕵️‍♂️",
    layout="centered"
)

# --- [2] 디자인: '글로벌 화이트 테마' (깔끔하고 신뢰감 있는 스타일) ---
st.markdown(
    """
    <style>
    /* 전체 배경: 아주 연한 회색 */
    .stApp {
        background-color: #f8f9fa;
    }
    /* 메인 컨테이너 */
    .main .block-container {
        background-color: #ffffff;
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.05);
    }
    /* 제목 스타일 */
    h1 {
        color: #111827 !important;
        font-family: -apple-system, sans-serif;
        font-weight: 800;
        margin-bottom: 0px;
    }
    /* 텍스트 색상 */
    p, .stMarkdown, h3, h5, div, span, li {
        color: #374151 !important;
        line-height: 1.6;
    }
    /* 입력창 커스텀 */
    .stTextArea textarea {
        background-color: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
    }
    /* 버튼 스타일 (파란색) */
    .stButton>button {
        background-color: #2563eb;
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 12px;
        font-weight: 600;
        transition: 0.2s;
    }
    .stButton>button:hover {
        background-color: #1d4ed8;
        transform: translateY(-2px);
    }
    /* 결과 박스 스타일 */
    .result-box {
        background-color: #eff6ff;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2563eb;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- [3] 비밀 열쇠 연동 ---
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = st.sidebar.text_input("🔑 관리자 키 입력 (API Key)", type="password")

# --- [4] 메인 헤더 ---
st.title("🕵️‍♂️ 스팸버스터 AI")
st.caption("🇰🇷 대한민국 사기 문자/스미싱 판독기")

# 방문자 카운터 (사장님 주소 연동)
st.markdown(
    """
    <a href="https://hits.seeyoufarm.com">
        <img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fscam-buster-kbxdvib6ghejadljolbgsb.streamlit.app&count_bg=%232563EB&title_bg=%231F2937&icon=shield.svg&icon_color=%23ffffff&title=Users&edge_flat=true"/>
    </a>
    """,
    unsafe_allow_html=True
)
st.markdown("---")

st.info("👋 이 문자 사기일까요? 캡처한 이미지나 텍스트를 넣어보세요.")

# --- [5] 입력 섹션 ---
# 1. 이미지 업로드
uploaded_file = st.file_uploader("📸 스크린샷 업로드 (선택사항)", type=["jpg", "png", "jpeg"])

# 2. 텍스트 입력창
user_input = st.text_area("📩 또는 내용을 여기에 붙여넣으세요:", height=100, placeholder="예시: [국외발신] 980,000원 결제 완료...")

# 이미지 변환 함수
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# --- [6] 분석 버튼 및 로직 ---
if st.button("🚨 사기 여부 무료 분석하기"):
    if not api_key:
        st.error("시스템 오류: 관리자 키가 없습니다.")
    elif not user_input and not uploaded_file:
        st.warning("⚠️ 분석할 이미지나 텍스트를 입력해주세요!")
    else:
        client = OpenAI(api_key=api_key)
        
        # AI 지령 (한국어 버전으로 수정)
        system_prompt = """
        당신은 유머러스하지만 냉철한 대한민국의 보안 전문가입니다.
        사용자가 입력한 텍스트나 이미지가 스팸/사기인지 분석하세요.
        
        [분석 결과 형식]
        1. 🚨 **위험도**: (안전 / 주의 / 치명적 위험)
        2. 💡 **진실**: 왜 이것이 사기인지 1문장으로 팩트 체크.
        3. 🤣 **사이다 답장**: 사기꾼에게 보낼 짧고 웃긴 답장 추천.
        """
        
        # 이미지 vs 텍스트 분기 처리
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

        with st.spinner("AI가 사기꾼의 수법을 분석 중입니다... 🕵️‍♂️"):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    max_tokens=800
                )
                result = response.choices[0].message.content
                
                # 결과 출력
                st.success("분석 완료!")
                st.markdown(f'<div class="result-box">{result}</div>', unsafe_allow_html=True)
                st.balloons() # 사장님이 좋아하시던 풍선 효과 유지!
                
            except Exception as e:
                st.error(f"오류 발생: {e}")

# --- [7] 하단 섹션: 왼쪽 하단 쿠팡 파트너스 ---
st.markdown("---")

# 화면을 반으로 나눠서 왼쪽에 쿠팡 링크 배치
col_left, col_right = st.columns([1, 1])

with col_left:
    # [왼쪽 하단] 쿠팡 파트너스 배너
    coupang_link = "https://www.coupang.com/np/search?component=&q=%ED%9A%A8%EB%8F%84%ED%8F%B0&channel=user"
    st.markdown(
        f"""
        <a href="{coupang_link}" target="_blank" style="text-decoration: none;">
            <div style="background-color: #d32f2f; padding: 15px; border-radius: 10px; color: white; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <div style="font-size: 18px; font-weight: bold;">📱 해킹 방지 효도폰</div>
                <div style="font-size: 12px;">최저가 보기 (쿠팡)</div>
            </div>
        </a>
        """, 
        unsafe_allow_html=True
    )

with col_right:
    # [오른쪽] 안전 팁
    st.info("💡 팁: 송금 인증샷은 절대 믿지 마세요! 이미지는 포토샵으로 조작이 가능합니다.")

st.markdown("<br>", unsafe_allow_html=True)
st.caption("© 2026 ScamBuster AI. (쿠팡 파트너스 활동 수수료 포함)")

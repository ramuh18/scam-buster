import streamlit as st
from openai import OpenAI
import base64

# --- [1] 페이지 설정 (글로벌 버전 그대로) ---
st.set_page_config(page_title="ScamBuster AI", page_icon="🕵️‍♂️")

# --- [2] 비밀 열쇠 연동 ---
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = st.sidebar.text_input("API Key (Owner Only)", type="password")

# --- [3] 메인 타이틀 (한국어 패치) ---
st.title("🕵️‍♂️ ScamBuster AI")
st.subheader("AI 사기 탐지기 & 팩트 폭격기 🔥")

# --- [4] 실시간 카운터 배지 ---
st.markdown(
    """
    <a href="https://github.com/scambuster">
        <img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fscam-buster-kbxdvib6ghejadljolbgsb.streamlit.app&count_bg=%23FF4B4B&title_bg=%23555555&icon=shield.svg&icon_color=%23E7E7E7&title=Scams+Blocked&edge_flat=false"/>
    </a>
    """,
    unsafe_allow_html=True
)
st.markdown("---")

st.markdown("이 문자가 사기인지 헷갈리시나요? 캡처나 텍스트를 넣어보세요. (AI가 팩폭 날려드립니다)")

# 1. 이미지 업로드 (글로벌 버전 UI)
uploaded_file = st.file_uploader("📸 스크린샷 업로드 (선택)", type=["jpg", "png", "jpeg"])

# 2. 텍스트 입력창 (글로벌 버전 UI)
user_input = st.text_area("📩 또는 내용을 여기에 붙여넣으세요:", height=100, placeholder="예시: [국외발신] 결제 완료 문의 006-...")

# 이미지를 변환하는 마법 함수
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# --- [5] 분석 버튼 (글로벌 로직 유지 + 한국어) ---
if st.button("🚨 사기 분석 & 팩폭 듣기 (Analyze)"):
    if not api_key:
        st.error("시스템 오류: API 키가 없습니다.")
    elif not user_input and not uploaded_file:
        st.warning("분석할 이미지나 텍스트를 넣어주세요!")
    else:
        client = OpenAI(api_key=api_key)
        
        # AI 지령 (글로벌 버전의 'Sarcastic/Roast' 성격을 한국어로 이식)
        system_prompt = """
        You are a world-class security expert with a sarcastic sense of humor (Korean context).
        Analyze the provided image or text for scam patterns.
        Answer in KOREAN.
        
        Output Format:
        1. 🚨 **위험도 (RISK LEVEL)**: (안전 / 주의 / 치명적 위험)
        2. 💡 **진실 (THE TRUTH)**: 왜 이게 사기인지 1문장으로 뼈 때리는 팩트 체크.
        3. 🤣 **사이다 답장 (SAVAGE REPLY)**: 사기꾼에게 보낼 짧고 웃긴(비꼬는) 답장 추천.
        """
        
        # 이미지 vs 텍스트 분기 처리
        if uploaded_file:
            base64_image = encode_image(uploaded_file)
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": [
                    {"type": "text", "text": f"Analyze this image and text in Korean: {user_input}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]}
            ]
            st.info("🧠 AI가 스크린샷을 째려보는 중...")
        else:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze this text in Korean: {user_input}"}
            ]
            st.info("🧠 AI가 텍스트를 분석 중...")

        with st.spinner("사기꾼 패턴 분석 중... 🕵️‍♂️"):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    max_tokens=500
                )
                result = response.choices[0].message.content
                
                # 결과 출력
                st.success("분석 완료! (Analysis Complete)")
                st.markdown(result)
                st.balloons() # ★ 사장님이 좋아하신 풍선 효과 유지! ★
                
            except Exception as e:
                st.error(f"Error: {e}")

# --- [6] 하단: 왼쪽 하단 쿠팡 파트너스 (요청사항 적용) ---
st.markdown("---")

col1, col2 = st.columns([1, 1]) # 화면을 반으로 나눔

with col1:
    # [왼쪽] 쿠팡 파트너스 배너
    coupang_link = "https://www.coupang.com/np/search?component=&q=%ED%9A%A8%EB%8F%84%ED%8F%B0&channel=user"
    st.markdown(
        f"""
        <a href="{coupang_link}" target="_blank" style="text-decoration: none;">
            <div style="
                background-color: #d32f2f; 
                color: white; 
                padding: 10px; 
                border-radius: 8px; 
                text-align: center; 
                font-weight: bold;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
                📱 해킹 방지 효도폰 (최저가)
            </div>
        </a>
        """, 
        unsafe_allow_html=True
    )

with col2:
    # [오른쪽] 팁 메시지
    st.info("💡 팁: 송금 인증샷은 조작될 수 있습니다. 절대 믿지 마세요!")

st.caption("© 2026 ScamBuster AI. 이 포스팅은 쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.")

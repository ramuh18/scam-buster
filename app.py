import streamlit as st
from openai import OpenAI
import base64

# 1. 페이지 설정 (탭 이름과 아이콘)
st.set_page_config(
    page_title="ScamBuster AI",
    page_icon="🛡️",
    layout="centered"
)

# 2. 비밀 금고에서 열쇠 꺼내기
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = st.sidebar.text_input("API Key (Owner Only)", type="password")

# --- [사이드바] 메뉴 & 돈통 & 카운터 ---
with st.sidebar:
    st.header("🛡️ ScamBuster AI")
    st.markdown("Your personal AI security guard.")
    st.markdown("---")
    
    # 카운터 배지 (왼쪽 메뉴로 이동)
    st.markdown(
        """
        <div style="text-align: center;">
            <a href="#">
                <img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fscam-buster-kbxdvib6ghejadljolbgsb.streamlit.app&count_bg=%23FF4B4B&title_bg=%23555555&icon=shield.svg&icon_color=%23E7E7E7&title=Scams+Blocked&edge_flat=false"/>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")
    
    # 후원 버튼 (강조)
    st.info("💖 Did I save your wallet?")
    st.markdown(
        """
        <a href="https://buymeacoffee.com/ramuh4969c" target="_blank">
            <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 50px !important;width: 180px !important;" >
        </a>
        """,
        unsafe_allow_html=True
    )
    st.caption("Server costs are real! Thanks for your support.")

# --- [메인 화면] ---
st.title("🕵️‍♂️ ScamBuster AI")
st.markdown("### Is this message a SCAM? Let's check. 🚨")
st.markdown("Upload a screenshot or paste the text below. AI will analyze the hidden risks.")

# 3. 입력 구역 (탭으로 분리해서 깔끔하게)
tab1, tab2 = st.tabs(["📝 Text Analysis", "📸 Screenshot Analysis"])

user_input = ""
uploaded_file = None

with tab1:
    # 예시 버튼 (손님들이 쉽게 써보게)
    if st.button("🎲 Try Example (Elon Musk Scam)"):
        user_input = "Hi, I am Elon Musk. Send me 1 Bitcoin and I will send you 2 Bitcoin back. Limited time offer!"
    else:
        user_input = st.text_area("Paste the suspicious text here:", value=user_input, height=150, placeholder="Example: Hi, I am Elon Musk...")

with tab2:
    uploaded_file = st.file_uploader("Upload a screenshot (JPG/PNG)", type=["jpg", "png", "jpeg"])

# 이미지 변환 함수
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# 4. 분석 버튼 & 결과 화면 (대시보드 스타일)
if st.button("🚨 Analyze Risk Now", type="primary", use_container_width=True):
    if not api_key:
        st.error("System Error: API Key is missing.")
    elif not user_input and not uploaded_file:
        st.warning("⚠️ Please enter text or upload an image first!")
    else:
        client = OpenAI(api_key=api_key)
        
        # AI 페르소나 설정
        system_prompt = """
        You are a sarcastic but highly professional security expert.
        Analyze the input for scam patterns.
        
        Output Format (STRICTLY FOLLOW THIS):
        RISK_LEVEL: (Low / Medium / High / EXTREME)
        REASON: (1 short sentence explaining why)
        ROAST: (A funny, sarcastic reply to the scammer)
        """
        
        # 메시지 구성
        messages = []
        if uploaded_file:
            base64_image = encode_image(uploaded_file)
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": [
                    {"type": "text", "text": f"Analyze this image and text: {user_input}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]}
            ]
        else:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]

        with st.spinner("🕵️‍♂️ AI is tracking the scammer..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    max_tokens=500
                )
                result_text = response.choices[0].message.content
                
                # 결과 파싱 (AI가 준 글을 예쁘게 자르기)
                # 만약 형식이 안 맞으면 통째로 보여줌
                risk = "HIGH"
                reason = "Suspicious pattern detected."
                roast = result_text

                if "RISK_LEVEL:" in result_text:
                    parts = result_text.split("\n")
                    for part in parts:
                        if "RISK_LEVEL:" in part:
                            risk = part.replace("RISK_LEVEL:", "").strip().replace("*", "")
                        elif "REASON:" in part:
                            reason = part.replace("REASON:", "").strip()
                        elif "ROAST:" in part:
                            roast = part.replace("ROAST:", "").strip()

                # --- [결과 대시보드 UI] ---
                st.markdown("---")
                
                # 1. 계기판 (Metric)
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.metric(label="🚨 RISK LEVEL", value=risk, delta="Danger" if "High" in risk or "EXTREME" in risk else "Safe")
                with col2:
                    st.info(f"💡 **Analysis:** {reason}")
                
                # 2. 팩폭 메시지
                st.success(f"🤣 **Best Reply:** \n\n\"{roast}\"")
                st.balloons()
                
            except Exception as e:
                st.error(f"Error: {e}")

# 5. 하단: 보안 꿀팁 (접었다 폈다 기능)
with st.expander("🛡️ How to stay safe from scams? (Click to read)"):
    st.markdown("""
    1. **Never trust 'Urgent' messages.** (Scammers want you to panic.)
    2. **Don't click strange links.** (Banks never send bit.ly links.)
    3. **Verify the number.** (Call the official bank number, not the one in the text.)
    4. **Use ScamBuster AI.** (You are doing great!)
    """)

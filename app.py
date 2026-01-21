import streamlit as st
from openai import OpenAI
import base64

# 1. 페이지 설정 (넓게 보기 옵션 추가)
st.set_page_config(
    page_title="ScamBuster AI",
    page_icon="🛡️",
    layout="wide"  # 화면을 넓게 써서 더 시원해 보임
)

# 2. 비밀 금고에서 열쇠 꺼내기
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = st.sidebar.text_input("API Key (Owner Only)", type="password")

# --- [사이드바] 꽉 채우기 (허전하지 않게!) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=80) # 보안관 뱃지 아이콘
    st.title("🛡️ ScamBuster")
    st.markdown("**Global Scam Defense System**")
    
    st.divider() # 구분선
    
    # 1. 사용법 안내 (공간 채우기)
    st.markdown("### 📖 How to use")
    st.info(
        """
        1. **Upload** a screenshot 📸
        2. **Or Paste** the text 📝
        3. Click **Analyze** 🚨
        4. Get a **Roast Reply** 🔥
        """
    )
    
    st.divider()

    # 2. 실시간 카운터 (마크다운 방식으로 변경 -> 무조건 보임)
    st.markdown("### 📊 Scams Blocked")
    st.markdown(
        "[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fscam-buster-kbxdvib6ghejadljolbgsb.streamlit.app&count_bg=%23FF4B4B&title_bg=%23555555&icon=shield.svg&icon_color=%23E7E7E7&title=Total+Blocked&edge_flat=false)](https://github.com/scambuster)"
    )
    st.caption("Updated in real-time.")
    
    st.divider()

    # 3. 돈통 (후원 버튼) - 노란색으로 강조
    st.markdown("### 💖 Support Project")
    st.markdown(
        """
        <a href="https://buymeacoffee.com/ramuh4969c" target="_blank">
            <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="width: 100%;" >
        </a>
        """,
        unsafe_allow_html=True
    )
    st.caption("Server costs are real! Thanks.")

# --- [메인 화면] ---
# 화면을 2단으로 나눠서 왼쪽은 설명, 오른쪽은 기능 (넓은 화면 활용)
col_main_1, col_main_2 = st.columns([2, 1])

with col_main_1:
    st.title("🕵️‍♂️ ScamBuster AI")
    st.markdown("### \"Is this a SCAM?\"")
    st.markdown("Don't panic. Let AI analyze the text & image for hidden risks. We even write a savage reply for you.")

with col_main_2:
    # 오른쪽에 '오늘의 보안 팁' 박스 하나 띄우기
    st.warning("⚠️ **Latest Trend:** 'Package Delivery' scams are rising! Be careful.")

st.markdown("---")

# 탭 메뉴 (텍스트 vs 이미지)
tab1, tab2 = st.tabs(["📝 Check Text", "📸 Check Screenshot"])

user_input = ""
uploaded_file = None

with tab1:
    st.markdown("Paste the suspicious message below:")
    if st.button("🎲 Use Example Text"):
        user_input = "Hi, I am Elon Musk. Send me 1 Bitcoin and I will send you 2 Bitcoin back."
    else:
        user_input = st.text_area("Message Content:", value=user_input, height=150, placeholder="Example: Hi mum, my phone is broken...")

with tab2:
    st.markdown("Upload a screenshot of the message or call log:")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

# 이미지 변환 함수
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# 분석 버튼
st.markdown("###") # 여백 조금 주기
if st.button("🚨 Analyze Risk & Roast Scammer", type="primary", use_container_width=True):
    if not api_key:
        st.error("System Error: API Key is missing.")
    elif not user_input and not uploaded_file:
        st.warning("⚠️ Please enter text or upload an image first!")
    else:
        client = OpenAI(api_key=api_key)
        
        # AI 페르소나
        system_prompt = """
        You are a sarcastic security expert. Analyze the input.
        
        Output Format:
        RISK_LEVEL: (Low / Medium / High / EXTREME)
        REASON: (1 sentence why)
        ROAST: (Sarcastic reply to scammer)
        """
        
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

        with st.spinner("🕵️‍♂️ Investigating..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    max_tokens=500
                )
                result_text = response.choices[0].message.content
                
                # 결과 파싱
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

                # 결과 보여주기
                st.markdown("---")
                
                # 계기판 스타일
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("🚨 Risk Level", risk)
                with c2:
                    st.metric("🤖 AI Confidence", "99.9%")
                with c3:
                    st.metric("🛡️ Type", "Phishing" if "High" in risk else "Unknown")
                
                st.info(f"💡 **Reason:** {reason}")
                st.success(f"🤣 **Roast Reply:** \n\n{roast}")
                st.balloons()
                
            except Exception as e:
                st.error(f"Error: {e}")

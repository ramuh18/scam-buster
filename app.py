import streamlit as st
from openai import OpenAI
import base64

# 페이지 설정
st.set_page_config(page_title="ScamBuster AI", page_icon="🕵️‍♂️")

# 비밀 금고에서 열쇠 꺼내기
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = st.sidebar.text_input("API Key (Owner Only)", type="password")

st.title("🕵️‍♂️ ScamBuster AI (Vision Edition)")
st.subheader("Text or Screenshot? We check both! 📸")
st.markdown("Is this message a SCAM? Upload a screenshot or paste text below.")

# 1. 이미지 업로드 기능 추가 (여기가 핵심!)
uploaded_file = st.file_uploader("📸 Upload a Screenshot (Optional)", type=["jpg", "png", "jpeg"])

# 2. 텍스트 입력창
user_input = st.text_area("📩 Or paste the text here:", height=100, placeholder="Example: Hi, I am Elon Musk...")

# 이미지를 AI가 볼 수 있게 변환하는 함수 (마법 주문)
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# 분석 버튼
if st.button("🚨 Analyze Risk & Roast"):
    if not api_key:
        st.error("System Error: API Key is missing.")
    elif not user_input and not uploaded_file:
        st.warning("Please upload a screenshot OR paste some text!")
    else:
        client = OpenAI(api_key=api_key)
        
        # AI에게 보낼 메시지 준비
        messages = []
        
        # 기본 지령 (페르소나)
        system_prompt = """
        You are a world-class security expert with a sarcastic sense of humor.
        Analyze the provided image or text for scam patterns.
        
        Output Format:
        1. 🚨 **RISK LEVEL**: (Low / High / EXTREME)
        2. 💡 **THE TRUTH**: Explain why this is a scam in 1 simple sentence.
        3. 🤣 **SAVAGE REPLY**: Write a short, funny, and roasting reply to the scammer.
        """
        
        # 텍스트만 있을 때 vs 이미지가 있을 때 구분
        if uploaded_file:
            # 이미지가 있으면 AI에게 그림을 보여줌
            base64_image = encode_image(uploaded_file)
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": [
                    {"type": "text", "text": f"Analyze this image and this text: {user_input}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]}
            ]
            st.info("🧠 AI is looking at your screenshot...")
        else:
            # 텍스트만 있으면 글자만 보냄
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
            st.info("🧠 AI is reading your text...")

        with st.spinner("Analyzing scam patterns... 🕵️‍♂️"):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini", # 시각 기능이 있는 가성비 모델
                    messages=messages,
                    max_tokens=500
                )
                result = response.choices[0].message.content
                
                # 결과 출력
                st.success("Analysis Complete!")
                st.markdown(result)
                st.balloons()
                
            except Exception as e:
                st.error(f"Error: {e}")

# 하단: 돈 버는 버튼
st.markdown("---")
st.info("💡 Tip: Never trust screenshots of bank transfers!")
st.markdown("[☕ Buy me a coffee (Support)] (https://buymeacoffee.com/ramuh4969c)")

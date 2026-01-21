import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(page_title="ScamBuster AI", page_icon="🕵️‍♂️")

# 비밀 금고에서 열쇠 꺼내기
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    # 만약 비밀키가 없으면 사이드바에서 입력받음 (사장님 테스트용)
    api_key = st.sidebar.text_input("API Key (Owner Only)", type="password")

st.title("🕵️‍♂️ ScamBuster AI")
st.subheader("Global Scam Detector & Roaster 🔥")
st.markdown("Is this message a SCAM? Paste it below. Our AI will expose the truth.")

# 메인 입력창
user_input = st.text_area("📩 Paste the suspicious text here:", height=150, placeholder="Example: Hi, I am Elon Musk...")

# 분석 버튼
if st.button("🚨 Analyze Risk & Roast"):
    if not api_key:
        st.error("System Error: API Key is missing. Please set it in Streamlit Secrets.")
    elif not user_input:
        st.warning("Please paste the text first!")
    else:
        # AI 분석 시작
        client = OpenAI(api_key=api_key)
        
        # 강력한 글로벌 페르소나 부여
        prompt = f"""
        You are a world-class security expert with a sarcastic sense of humor.
        Analyze the text below.
        
        Output Format:
        1. 🚨 **RISK LEVEL**: (Low / High / EXTREME)
        2. 💡 **THE TRUTH**: Explain why this is a scam in 1 simple sentence.
        3. 🤣 **SAVAGE REPLY**: Write a short, funny, and roasting reply to the scammer.
        
        [Text]: {user_input}
        """
        
        with st.spinner("Analyzing scam patterns... 🕵️‍♂️"):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.choices[0].message.content
                
                # 결과 출력
                st.success("Analysis Complete!")
                st.markdown(result)
                st.balloons()
                
            except Exception as e:
                st.error(f"Error: {e}")

# 하단: 돈 버는 버튼 (예시)
st.markdown("---")
st.info("💡 Tip: Never click links from strangers!")
# 나중에 여기에 광고나 후원 링크를 넣으면 됩니다.
st.markdown("[☕ Buy me a coffee (Support)] (#)")

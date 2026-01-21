import streamlit as st
from openai import OpenAI

# 페이지 기본 설정 (제목, 아이콘)
st.set_page_config(page_title="ScamBuster AI", page_icon="🕵️‍♂️")

# 1. 사이트 제목과 설명
st.title("🕵️‍♂️ ScamBuster AI")
st.subheader("Is this message a SCAM? Let's roast them! 🔥")
st.write("Paste the suspicious text below. AI will analyze if it's a scam and write a funny reply.")

# 2. 사이드바 (왼쪽 메뉴 - 광고나 후원 링크 넣는 곳)
with st.sidebar:
    st.header("⚙️ Settings")
    # 사장님의 API 키를 입력받는 곳 (배포 후에는 숨길 수 있음)
    api_key = st.text_input("Enter OpenAI API Key", type="password")
    st.markdown("---")
    st.markdown("### ☕ Support This Project")
    st.write("If this saved you money, buy me a coffee!")
    # 나중에 여기에 사장님의 후원 링크나 광고를 넣으면 됩니다.
    st.button("Donate $1 (Link Placeholder)") 

# 3. 메인 입력창
user_input = st.text_area("📩 Paste the text here (English recommended):", height=150)

# 4. 분석 버튼
if st.button("🚨 Analyze Risk & Roast"):
    if not api_key:
        st.warning("Please enter your API Key in the sidebar first! 👈")
    elif not user_input:
        st.warning("Please paste the text first!")
    else:
        # AI 분석 시작
        client = OpenAI(api_key=api_key)
        
        # AI에게 내리는 지령 (영어 버전)
        prompt = f"""
        You are a sarcastic security expert. Analyze the text below.
        
        Output Format:
        1. 🚨 **RISK LEVEL**: (Low / Medium / High / EXTREME)
        2. 💡 **WHY**: Explain why it is a scam in 1 simple sentence.
        3. 🤣 **ROAST REPLY**: Write a short, savage, and funny reply to send back to the scammer.
        
        [Text]: {user_input}
        """
        
        with st.spinner("Scanning for scams... 🕵️‍♂️"):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )
                result = response.choices[0].message.content
                
                # 결과 보여주기
                st.success("Analysis Complete!")
                st.markdown(result) # 결과 텍스트 출력
                st.balloons() # 풍선 효과 펑펑!
                
            except Exception as e:
                st.error(f"Error: {e}")

# 5. 저작권 표시
st.markdown("---")
st.caption("© 2026 ScamBuster. Powered by OpenAI.")
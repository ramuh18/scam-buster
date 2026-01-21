import streamlit as st
from openai import OpenAI
import base64

# 페이지 설정
st.set_page_config(page_title="스팸버스터 AI", page_icon="🕵️‍♂️")

# 비밀 금고에서 열쇠 꺼내기
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = st.sidebar.text_input("관리자용 키 입력 (API Key)", type="password")

# --- [주인장 전용] 비밀 마케팅 도구 ---
with st.sidebar:
    st.header("🔧 주인장 도구")
    show_marketing = st.checkbox("마케팅 비서 부르기")
    
    if show_marketing:
        st.markdown("---")
        st.subheader("🚀 홍보 문구 자동 생성기")
        platform = st.selectbox("어디에 올릴까요?", ["네이버 블로그/카페", "인스타그램/쓰레드", "트위터(X)"])
        tone = st.selectbox("분위기 선택", ["유머러스하게 🤣", "진지한 경고 🚨", "감성 스토리 😢"])
        
        if st.button("글짓기 시작"):
            if not api_key:
                st.error("키가 없습니다!")
            else:
                client = OpenAI(api_key=api_key)
                prompt = f"""
                당신은 SNS 마케팅 전문가입니다. '스팸버스터 AI'를 홍보할 매력적인 글을 작성하세요.
                - 플랫폼: {platform}
                - 말투: {tone}
                - 목표: 사람들이 이 링크를 클릭하게 만드세요: https://scam-buster-kbxdvib6ghejadljolbgsb.streamlit.app/
                - 필수: 이모지를 적절히 사용하고, 한국 네티즌이 좋아하는 스타일로 쓰세요.
                """
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.code(response.choices[0].message.content)

# 메인 화면
st.title("🕵️‍♂️ 스팸버스터 AI")
st.subheader("이거 사기일까? AI가 3초 만에 판별해드립니다. 🔥")

# 방문자 카운터 (마케팅용)
st.markdown(
    """
    <a href="https://github.com/scambuster">
        <img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fscam-buster-kbxdvib6ghejadljolbgsb.streamlit.app&count_bg=%2303C75A&title_bg=%23555555&icon=shield.svg&icon_color=%23E7E7E7&title=%EC%82%AC%EA%B8%B0%EB%B0%A9%EC%A7%80+%EC%84%B1%EA%B3%B5&edge_flat=false"/>
    </a>
    """,
    unsafe_allow_html=True
)
st.markdown("---")
st.success("💡 팁: 전화번호, 계좌번호, 카톡 내용, 캡처 사진 뭐든지 물어보세요!")

# 1. 이미지 업로드
uploaded_file = st.file_uploader("📸 캡처한 이미지 올리기 (선택)", type=["jpg", "png", "jpeg"])

# 2. 텍스트 입력창
user_input = st.text_area("📩 또는 문자를 여기에 붙여넣으세요:", height=100, placeholder="예: 엄마 나 폰 고장 났어, 검찰청입니다 등등...")

# 이미지 변환 함수
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# 분석 버튼
if st.button("🚨 AI 분석 시작 (무료)"):
    if not api_key:
        st.error("시스템 오류: 관리자 키가 설정되지 않았습니다.")
    elif not user_input and not uploaded_file:
        st.warning("내용을 입력하거나 사진을 올려주세요!")
    else:
        client = OpenAI(api_key=api_key)
        
        # 한국형 스팸 잡는 탐정 페르소나
        system_prompt = """
        당신은 한국 최고의 보안 전문가이자 '팩트 폭격기'입니다.
        사용자가 입력한 텍스트나 이미지가 스팸/사기인지 분석하세요.
        
        [출력 형식]
        1. 🚨 **위험도**: (안전 / 의심 / 매우 위험)
        2. 🔍 **팩트 체크**: 왜 이것이 사기인지(또는 아닌지) 초등학생도 알기 쉽게 1문장으로 설명.
        3. 🤬 **사이다 일침**: 사기꾼에게 보낼 수 있는 아주 웃기고 신랄한 비꼬는 답장(한국 유행어 사용 가능).
        """
        
        if uploaded_file:
            base64_image = encode_image(uploaded_file)
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": [
                    {"type": "text", "text": f"이 이미지와 텍스트를 분석해줘: {user_input}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]}
            ]
            st.info("🧠 AI가 이미지를 분석하는 중입니다...")
        else:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
            st.info("🧠 AI가 텍스트를 읽고 있습니다...")

        with st.spinner("사기꾼 냄새 맡는 중... 🐕"):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    max_tokens=800
                )
                result = response.choices[0].message.content
                
                st.success("분석 완료!")
                st.markdown(result)
                st.balloons()
            except Exception as e:
                st.error(f"에러 발생: {e}")

# 하단: 후원 버튼
st.markdown("---")
st.info("☕ 이 서비스는 여러분의 후원으로 운영됩니다.")
st.markdown("[👉 개발자에게 커피 한 잔 사주기 (후원)] (https://buymeacoffee.com/ramuh4969c)")

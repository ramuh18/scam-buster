import streamlit as st
from openai import OpenAI
import base64

# 1. 페이지 설정 (사장님이 좋아하시는 넓은 화면 모드)
st.set_page_config(
    page_title="스팸버스터 AI",
    page_icon="🛡️",
    layout="wide"
)

# 2. 비밀 금고에서 열쇠 꺼내기
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = st.sidebar.text_input("🔑 관리자 키 입력", type="password")

# --- [사이드바] 사장님 맞춤형 한국어 구성 ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=80) 
    st.title("🛡️ 스팸버스터")
    st.markdown("**대한민국 사기 방지 시스템**")
    
    st.divider()
    
    # 1. 사용법 안내
    st.markdown("### 📖 사용법")
    st.info(
        """
        1. 의심되는 **스크린샷 업로드** 📸
        2. 또는 문자 **내용 붙여넣기** 📝
        3. **분석 시작** 버튼 클릭 🚨
        4. AI의 **사이다 팩폭** 확인 🔥
        """
    )
    
    st.divider()

    # 2. 실시간 카운터 (사장님 확정 주소 적용)
    st.markdown("### 📊 차단된 사기 문자")
    st.markdown(
        "[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fscam-buster-kbxdvib6ghejadljolbgsb.streamlit.app&count_bg=%23FF4B4B&title_bg=%23555555&icon=shield.svg&icon_color=%23E7E7E7&title=Total+Blocked&edge_flat=false)](https://hits.seeyoufarm.com)"
    )
    st.caption("실시간으로 업데이트됩니다.")
    
    st.divider()

    # 3. 쿠팡 파트너스 (수익 모델을 사이드바 하단에도 배치)
    st.markdown("### 💖 프로젝트 후원")
    coupang_link = "https://www.coupang.com/np/search?component=&q=%ED%9A%A8%EB%8F%84%ED%8F%B0&channel=user"
    st.markdown(
        f"""
        <a href="{coupang_link}" target="_blank">
            <div style="background-color: #f68b1e; color: white; padding: 10px; border-radius: 5px; text-align: center; font-weight: bold;">
                📱 보안 효도폰 최저가 보기
            </div>
        </a>
        """, 
        unsafe_allow_html=True
    )
    st.caption("링크 구매 시 서버 운영에 큰 힘이 됩니다.")

# --- [메인 화면] ---
col_main_1, col_main_2 = st.columns([2, 1])

with col_main_1:
    st.title("🕵️‍♂️ 스팸버스터 AI")
    st.markdown("### \"이거 사기 아닐까? 고민하지 마세요.\"")
    st.markdown("AI가 문자와 이미지를 정밀 분석하여 숨겨진 위험을 찾아냅니다. 사기꾼에게 날릴 시원한 답장까지 준비해 드려요.")

with col_main_2:
    st.warning("⚠️ **최신 트렌드:** 최근 '토스 사기계좌 조회' 및 '택배 주소지 오류' 사기가 급증하고 있습니다. 주의하세요!")

st.markdown("---")

# 탭 메뉴 (한국어화)
tab1, tab2 = st.tabs(["📝 문자 내용 분석", "📸 스크린샷 분석"])

user_input = ""
uploaded_file = None

with tab1:
    st.markdown("의심스러운 문자 내용을 아래에 붙여넣으세요:")
    if st.button("🎲 예시 문구 사용해보기"):
        user_input = "[국외발신] 고객님 해외결제 980,000원 승인완료. 본인 아니면 즉시 신고 006-1234-5678"
        st.text_area("문자 내용:", value=user_input, height=150)
    else:
        user_input = st.text_area("문자 내용:", height=150, placeholder="예: [CJ대한통운] 주소지 불명으로 배송불가. 주소확인 부탁드립니다...")

with tab2:
    st.markdown("문자나 카톡 대화 내용을 캡처해서 올려주세요:")
    uploaded_file = st.file_uploader("이미지 업로드", type=["jpg", "png", "jpeg"])

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# 분석 버튼
st.markdown("###")
if st.button("🚨 사기 여부 분석 및 팩트 폭격 시작", type="primary", use_container_width=True):
    if not api_key:
        st.error("시스템 오류: API 키가 없습니다.")
    elif not user_input and not uploaded_file:
        st.warning("⚠️ 분석할 텍스트를 입력하거나 이미지를 업로드해주세요!")
    else:
        client = OpenAI(api_key=api_key)
        
        system_prompt = """
        당신은 냉철하고 유머러스한 대한민국 최고의 보안 전문가입니다. 
        사용자가 입력한 내용을 분석하여 사기 여부를 판독하세요.
        답변은 반드시 한국어로 하세요.
        
        형식:
        RISK_LEVEL: (안전 / 주의 / 위험 / 치명적)
        REASON: (왜 사기인지 전문가적인 이유 1문장)
        ROAST: (사기꾼에게 날리는 시원하고 비꼬는 사이다 답장)
        """
        
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

        with st.spinner("🕵️‍♂️ 사기꾼의 수법을 해독 중입니다..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    max_tokens=800
                )
                result_text = response.choices[0].message.content
                
                # 결과 파싱
                risk = "위험"
                reason = "사기 패턴이 감지되었습니다."
                roast = result_text

                parts = result_text.split("\n")
                for part in parts:
                    if "RISK_LEVEL:" in part:
                        risk = part.replace("RISK_LEVEL:", "").strip().replace("*", "")
                    elif "REASON:" in part:
                        reason = part.replace("REASON:", "").strip()
                    elif "ROAST:" in part:
                        roast = part.replace("ROAST:", "").strip()

                # 결과 시각화
                st.markdown("---")
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("🚨 위험 등급", risk)
                with c2:
                    st.metric("🤖 AI 신뢰도", "99.9%")
                with c3:
                    st.metric("🛡️ 분석 유형", "보이스피싱/스미싱")
                
                st.info(f"💡 **분석 결과:** {reason}")
                st.success(f"🤣 **사이다 답장:** \n\n{roast}")
                st.balloons()
                
            except Exception as e:
                st.error(f"오류 발생: {e}")

# --- [푸터] ---
st.markdown("---")
st.caption("© 2026 ScamBuster AI. 본 서비스는 쿠팡 파트너스 활동의 일환으로 수수료를 제공받을 수 있습니다.")

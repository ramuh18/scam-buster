import streamlit as st
from openai import OpenAI
import base64

# --- [1] 페이지 기본 설정 (기업 공식 홈페이지 느낌) ---
st.set_page_config(
    page_title="스팸버스터 AI - 대한민국 사기 방지 솔루션",
    page_icon="🛡️",
    layout="centered"
)

# --- [2] 비밀 열쇠 (API Key) 연동 ---
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    # 관리자 테스트용 입력창 (일반 손님에게는 안 보임)
    api_key = st.sidebar.text_input("관리자 키 입력", type="password")

# --- [3] 메인 헤더 & 방문자 카운터 ---
st.title("🛡️ 스팸버스터 AI")
st.subheader("대한민국 No.1 사기 문자/피싱 판별 솔루션")

# 실시간 방문자 카운터 (전문적인 느낌의 '배지' 부착)
st.markdown(
    """
    <div style="display: flex; align-items: center; gap: 10px;">
        <span style="font-weight: bold; color: gray;">누적 분석 건수:</span>
        <img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fscam-buster-kbxdvib6ghejadljolbgsb.streamlit.app&count_bg=%230055FF&title_bg=%23555555&icon=shield.svg&icon_color=%23E7E7E7&title=Scams+Blocked&edge_flat=false"/>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("---")

# --- [4] 입력 섹션 (직관적인 UI) ---
st.info("💡 팁: 의심스러운 문자 내용, 카톡 캡처, 전화번호 등 무엇이든 물어보세요.")

col1, col2 = st.columns([1, 2])
with col1:
    # 이미지 업로드
    uploaded_file = st.file_uploader("📸 캡처 이미지 (선택)", type=["jpg", "png", "jpeg"])
with col2:
    # 텍스트 입력
    user_input = st.text_area("📩 텍스트 입력", height=100, placeholder="예: 엄마 나 폰 고장 났어, 검찰청입니다, 010-XXXX-XXXX 등")

# --- [5] 핵심 기능: 이미지 변환 & AI 분석 ---
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

# 분석 버튼 (가운데 정렬 느낌)
if st.button("🚀 AI 무료 정밀 분석 시작", use_container_width=True):
    if not api_key:
        st.error("⚠️ 시스템 오류: 서버 연결 상태를 확인해주세요. (API Key Missing)")
    elif not user_input and not uploaded_file:
        st.warning("⚠️ 분석할 내용이나 이미지를 입력해주세요.")
    else:
        client = OpenAI(api_key=api_key)
        
        # 한국 최적화 페르소나 (신뢰감 + 팩트 폭격)
        system_prompt = """
        당신은 대한민국 최고의 사이버 보안 전문가이자 '팩트 폭격기'입니다.
        사용자가 입력한 텍스트나 이미지가 스팸/사기인지 정밀 분석하세요.
        
        [분석 리포트 형식]
        1. 🚨 **위험 등급**: (안전 ✅ / 주의 ⚠️ / 위험 🚫 / 매우 치명적 💀)
        2. 🔍 **팩트 체크**: 이 메시지가 왜 사기인지(또는 안전한지) 초등학생도 이해하게 1문장으로 요약.
        3. 🤬 **대응 가이드(사이다)**: 사기꾼에게 보낼 수 있는 아주 웃기고 신랄한 답장 또는 대처법.
        """
        
        # 로딩 애니메이션
        with st.spinner("🕵️‍♂️ AI가 데이터베이스와 패턴을 분석 중입니다..."):
            try:
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

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    max_tokens=800
                )
                result = response.choices[0].message.content
                
                # 결과 출력
                st.success("✅ 분석이 완료되었습니다.")
                st.markdown(result)
                st.balloons()
                
            except Exception as e:
                st.error(f"분석 중 오류가 발생했습니다: {e}")

# --- [6] 하단 수익화 배너 (광고 같지 않게 '보안 추천' 처럼 배치) ---
st.markdown("---")
st.header("🛡️ 보안 전문가 추천 필수품")

col_a, col_b = st.columns(2)

with col_a:
    # 쿠팡 파트너스 1: 효도폰 (보안 강한 폰) - 링크 수정 필요!
    st.markdown(
        """
        <a href="https://www.coupang.com/np/search?component=&q=%ED%9A%A8%EB%8F%84%ED%8F%B0&channel=user" target="_blank">
            <button style="width:100%; padding:15px; background-color:#C32424; color:white; border:none; border-radius:8px; font-weight:bold; cursor:pointer;">
                📱 부모님용 해킹 방지 '효도폰' 보기
            </button>
        </a>
        """, unsafe_allow_html=True
    )

with col_b:
    # 쿠팡 파트너스 2: 사생활 보호 필름 - 링크 수정 필요!
    st.markdown(
        """
        <a href="https://www.coupang.com/np/search?component=&q=%EC%82%AC%EC%83%9D%ED%99%9C%EB%B3%B4%ED%98%B8%ED%95%84%EB%A6%84&channel=user" target="_blank">
            <button style="width:100%; padding:15px; background-color:#333; color:white; border:none; border-radius:8px; font-weight:bold; cursor:pointer;">
                👀 엿보기 방지 '보호 필름' 보기
            </button>
        </a>
        """, unsafe_allow_html=True
    )

# 하단 저작권 및 안내
st.markdown("---")
st.caption("© 2026 ScamBuster AI. All rights reserved. | 이 서비스는 쿠팡 파트너스 활동의 일환으로 수수료를 제공받을 수 있습니다.")

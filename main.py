import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------
# 페이지 기본 설정
# -----------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.write(
    "1년간 박스오피스 10위권에 든 영화 가운데 "
    "이 기간에 개봉한 영화들의 데이터를 살펴봅니다."
)

# -----------------------------------
# 데이터 불러오기
# -----------------------------------
DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 개봉일을 날짜 형식으로 변환
    df["openDt"] = pd.to_datetime(
        df["openDt"].astype(str),
        format="%Y%m%d",
        errors="coerce"
    )

    # 장르가 여러 개라면 첫 번째 장르만 사용
    df["genre"] = (
        df["genre"]
        .fillna("기타")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
    )

    # 빈 장르는 기타로 처리
    df.loc[df["genre"] == "", "genre"] = "기타"

    return df


df = load_data()

# -----------------------------------
# 데이터 확인
# -----------------------------------
st.subheader("📊 데이터 개요")

col1, col2 = st.columns(2)

with col1:
    st.metric("영화 수", f"{len(df):,}편")

with col2:
    st.metric("장르 수", f"{df['genre'].nunique():,}개")


# -----------------------------------
# 그래프 1. 장르별 영화 편수
# -----------------------------------
st.divider()
st.header("1. 장르별 영화 편수")

genre_count = (
    df["genre"]
    .value_counts()
    .reset_index()
)

genre_count.columns = ["장르", "영화 편수"]

fig = px.pie(
    genre_count,
    names="장르",
    values="영화 편수",
    hole=0.45,
    title="장르별 영화 편수"
)

fig.update_traces(
    textinfo="label+percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}<extra></extra>"
    )
)

fig.update_layout(
    height=550,
    legend_title_text="장르"
)

st.plotly_chart(fig, use_container_width=True)

st.info("💡 이 그래프로 알 수 있는 것:"  "영화 장르 중 어떤 장르가 가장 많은 비중을 차지하고, "
    "어떤 장르가 적은 비중을 차지하는지 알 수 있습니다.")

# -----------------------------------
# 원본 데이터 일부 확인
# -----------------------------------
st.divider()
st.subheader("📋 원본 데이터 미리보기")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)
# -----------------------------------
# 그래프 2. 장르별 영화 트리맵
# -----------------------------------
st.divider()
st.header("2. 장르 안에 들어 있는 영화")

# 총 관객 수를 숫자로 변환
df["total_audi"] = pd.to_numeric(
    df["total_audi"],
    errors="coerce"
).fillna(0)

fig2 = px.treemap(
    df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르별 영화의 총 관객 규모"
)

fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,.0f}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    height=650
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.info(
    "💡 이 그래프로 알 수 있는 것: "
    "각 장르 안에서 어떤 영화가 많은 관객을 모았는지와 "
    "영화별 총 관객 규모의 차이를 비교할 수 있습니다."
)

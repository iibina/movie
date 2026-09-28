import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import StringIO


# ============================================================
# 데이터 불러오기
# ============================================================

@st.cache_data
def load_data():

    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

    try:
        response = requests.get(
            url,
            timeout=30
        )

        response.raise_for_status()

        df = pd.read_csv(
            StringIO(response.text)
        )

    except Exception as e:
        st.error("영화 데이터를 인터넷에서 불러오지 못했습니다.")
        st.write("데이터 주소:", url)
        st.write("오류 내용:", e)
        st.stop()

    # --------------------------------------------------------
    # 데이터 정리
    # --------------------------------------------------------

    # 개봉일을 날짜 형식으로 변환
    df["openDt"] = pd.to_datetime(
        df["openDt"].astype(str),
        format="%Y%m%d"
    )

    # 장르가 여러 개이면 첫 번째 장르만 사용
    df["genre"] = (
        df["genre"]
        .fillna("알 수 없음")
        .astype(str)
        .apply(lambda x: x.split("|")[0])
    )

    # 제작 국가가 여러 개이면 첫 번째 국가만 사용
    df["nation"] = (
        df["nation"]
        .fillna("알 수 없음")
        .astype(str)
        .apply(lambda x: x.split("|")[0])
    )

    return df


df = load_data()


# ============================================================
# 제목
# ============================================================

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

st.write(
    "영화의 장르, 관객 수, 스크린 수, 제작 국가 등의 데이터를 "
    "다양한 그래프로 살펴봅니다."
)


# ============================================================
# 그래프 1
# 장르별 영화 편수 도넛 차트
# ============================================================

st.header("1. 장르별 영화 편수")

genre_count = (
    df["genre"]
    .value_counts()
    .reset_index()
)

genre_count.columns = ["genre", "count"]

fig1 = px.pie(
    genre_count,
    names="genre",
    values="count",
    hole=0.45,
    title="장르별 영화 편수"
)

fig1.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}"
        "<extra></extra>"
    )
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.write("**이 그래프로 알 수 있는 것**")
st.write(
    "어떤 장르의 영화가 많이 포함되어 있는지 알 수 있습니다."
)


# ============================================================
# 그래프 2
# 장르 → 영화 트리맵
# ============================================================

st.header("2. 장르별 영화 관객 수")

treemap_df = (
    df.groupby(
        ["genre", "movieNm"],
        as_index=False
    )["total_audi"]
    .sum()
)

fig2 = px.treemap(
    treemap_df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르 → 영화별 총 관객 수"
)

fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,}명"
        "<extra></extra>"
    )
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.write("**이 그래프로 알 수 있는 것**")
st.write(
    "각 장르에서 어떤 영화가 많은 관객을 모았는지 알 수 있습니다."
)


# ============================================================
# 그래프 3
# 총 관객 수 히스토그램
# ============================================================

st.header("3. 영화별 총 관객 수 분포")

fig3 = px.histogram(
    df,
    x="total_audi",
    nbins=20,
    title="영화별 총 관객 수 분포",
    labels={
        "total_audi": "총 관객 수",
        "count": "영화 편수"
    }
)

fig3.update_traces(
    hovertemplate=(
        "관객 수 구간: %{x}<br>"
        "영화 편수: %{y}편"
        "<extra></extra>"
    )
)

st.plotly_chart(
    fig3,
    use_container_width=True
)


# 가장 많은 영화가 포함된 관객 수 구간
counts, bins = pd.cut(
    df["total_audi"],
    bins=20,
    retbins=True
)

most_bin = counts.value_counts().idxmax()

low = int(most_bin.left)
high = int(most_bin.right)


# 총 관객 수가 가장 많은 영화
max_index = df["total_audi"].idxmax()

max_movie = df.loc[
    max_index,
    "movieNm"
]

max_audi = int(
    df.loc[
        max_index,
        "total_audi"
    ]
)

st.write(
    f"가장 많은 영화가 포함된 관객 수 구간은 "
    f"**{low:,}명 ~ {high:,}명**입니다."
)

st.write(
    f"총 관객 수가 가장 많은 영화는 "
    f"**{max_movie}**로, "
    f"**{max_audi:,}명**입니다."
)

st.write("**이 그래프로 알 수 있는 것**")
st.write(
    "영화들의 총 관객 수가 어느 구간에 가장 많이 분포하는지 알 수 있습니다."
)


# ============================================================
# 그래프 4
# 개봉일 스크린 수 vs 총 관객 수
# ============================================================

st.header("4. 개봉일 스크린 수와 총 관객의 관계")

fig4 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    hover_data={
        "first_scrn": ":,",
        "total_audi": ":,",
        "genre": True
    },
    labels={
        "first_scrn": "개봉일 스크린 수",
        "total_audi": "총 관객 수",
        "genre": "장르"
    },
    title="개봉일 스크린 수와 총 관객의 관계"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

st.write("**이 그래프로 알 수 있는 것**")
st.write(
    "개봉일에 많은 스크린을 확보한 영화가 "
    "총 관객 수와 어떤 관계가 있는지 살펴볼 수 있습니다."
)


# ============================================================
# 그래프 5
# 장르별 총 관객 수 박스플롯
# 10편 이상인 장르만 사용
# ============================================================

st.header("5. 장르별 총 관객 수 분포")

genre_counts = df["genre"].value_counts()

valid_genres = genre_counts[
    genre_counts >= 10
].index

box_df = df[
    df["genre"].isin(valid_genres)
].copy()

fig5 = px.box(
    box_df,
    x="genre",
    y="total_audi",
    color="genre",
    points="outliers",
    hover_name="movieNm",
    hover_data={
        "total_audi": ":,",
        "genre": True
    },
    labels={
        "genre": "장르",
        "total_audi": "총 관객 수"
    },
    title="장르별 총 관객 수 분포 (10편 이상인 장르)"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

st.write("**이 그래프로 알 수 있는 것**")
st.write(
    "장르별 총 관객 수의 분포와 "
    "유난히 관객이 많거나 적은 영화를 살펴볼 수 있습니다."
)


# ============================================================
# 그래프 6
# 버블 차트
# ============================================================

st.header("6. 개봉일 스크린 수와 관객 수 관계")

fig6 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    hover_data={
        "genre": True,
        "first_scrn": ":,",
        "total_audi": ":,",
        "first_week_audi": ":,"
    },
    labels={
        "first_scrn": "개봉일 스크린 수",
        "total_audi": "총 관객 수",
        "first_week_audi": "첫 주 관객 수",
        "genre": "장르"
    },
    title="개봉일 스크린 수 · 총 관객 · 첫 주 관객"
)

st.plotly_chart(
    fig6,
    use_container_width=True
)

st.write("**이 그래프로 알 수 있는 것**")
st.write(
    "개봉일 스크린 수와 총 관객 수의 관계를 살펴보고, "
    "첫 주 관객이 많은 영화도 함께 비교할 수 있습니다."
)


# ============================================================
# 그래프 7
# 제작 국가 → 장르 선버스트
# 크기 = 영화 편수
# ============================================================

st.header("7. 제작 국가와 장르별 영화 분포")

sunburst_df = (
    df.groupby(
        ["nation", "genre"]
    )
    .size()
    .reset_index(
        name="movie_count"
    )
)

fig7 = px.sunburst(
    sunburst_df,
    path=["nation", "genre"],
    values="movie_count",
    title="제작 국가 → 장르별 영화 편수"
)

fig7.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편"
        "<extra></extra>"
    )
)

st.plotly_chart(
    fig7,
    use_container_width=True
)

st.write("**이 그래프로 알 수 있는 것**")
st.write(
    "어떤 나라의 영화가 많이 포함되어 있으며, "
    "그 나라의 영화가 어떤 장르로 구성되어 있는지 알 수 있습니다."
)

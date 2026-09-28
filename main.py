import streamlit as st
import pandas as pd
import plotly.express as px


# ==========================================
# 기본 설정
# ==========================================
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.markdown(
    "1년간 박스오피스 10위권에 든 영화 가운데 "
    "이 기간에 개봉한 영화 216편의 데이터를 살펴봅니다."
)


# ==========================================
# 데이터 불러오기
# ==========================================
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

    df = pd.read_csv(url)

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

st.success(f"총 {len(df)}편의 영화 데이터를 불러왔습니다.")

st.divider()


# ==========================================
# 그래프 1. 장르별 영화 편수
# ==========================================
st.subheader("① 장르별 영화 편수")

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
    hole=0.55,
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

fig1.update_layout(
    margin=dict(t=50, l=20, r=20, b=20)
)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것**")
st.info("여기에 이 그래프를 보고 알 수 있는 내용을 한 문장으로 작성합니다.")

st.divider()


# ==========================================
# 그래프 2. 장르 → 영화 트리맵
# ==========================================
st.subheader("② 장르별 영화 흥행 규모 트리맵")

fig2 = px.treemap(
    df,
    path=["genre", "movieNm"],
    values="total_audi",
    color="genre",
    title="장르별 영화의 총 관객 규모"
)

fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    margin=dict(t=50, l=10, r=10, b=10)
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것**")
st.info("여기에 이 그래프를 보고 알 수 있는 내용을 한 문장으로 작성합니다.")

st.divider()


# ==========================================
# 그래프 3. 총 관객 히스토그램
# ==========================================
st.subheader("③ 총 관객 분포 히스토그램")

fig3 = px.histogram(
    df,
    x="total_audi",
    nbins=20,
    labels={
        "total_audi": "총 관객 수",
        "count": "영화 편수"
    },
    title="영화별 총 관객 수 분포"
)

fig3.update_traces(
    hovertemplate=(
        "총 관객 구간: %{x:,}명<br>"
        "영화 편수: %{y}편"
        "<extra></extra>"
    )
)

fig3.update_layout(
    xaxis_title="총 관객 수",
    yaxis_title="영화 편수",
    bargap=0.05
)

st.plotly_chart(fig3, use_container_width=True)


# 가장 많은 영화가 몰린 구간 계산
counts, bins = pd.cut(
    df["total_audi"],
    bins=20,
    retbins=True
)

bin_counts = counts.value_counts()

most_bin = bin_counts.idxmax()

low = int(most_bin.left)
high = int(most_bin.right)
movie_count = int(bin_counts.max())

# 총 관객이 가장 많은 영화
top_movie = df.loc[df["total_audi"].idxmax()]
top_name = top_movie["movieNm"]
top_audi = int(top_movie["total_audi"])

st.markdown("**이 그래프로 알 수 있는 것**")

st.info(
    f"대부분의 영화는 **{low:,}명 ~ {high:,}명** 구간에 "
    f"몰려 있으며, 이 구간에는 **{movie_count}편**의 영화가 있습니다."
)

st.info(
    f"총 관객이 가장 많은 영화는 **{top_name}**이며, "
    f"총 **{top_audi:,}명**의 관객을 기록했습니다."
)

st.divider()


# ==========================================
# 그래프 4. 개봉일 스크린수와 총 관객의 관계
# ==========================================
st.subheader("④ 개봉일 스크린수와 총 관객의 관계")

fig4 = px.scatter(
    df,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    hover_data={
        "genre": True,
        "first_scrn": ":,",
        "total_audi": ":,"
    },
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객 수",
        "genre": "장르"
    },
    title="개봉일 스크린수와 총 관객의 관계"
)

fig4.update_traces(
    marker=dict(
        size=10,
        opacity=0.8
    ),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "장르: %{customdata[0]}<br>"
        "개봉일 스크린수: %{x:,}개<br>"
        "총 관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig4.update_layout(
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객 수",
    legend_title="장르",
    margin=dict(t=50, l=20, r=20, b=20)
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것**")
st.info("여기에 이 그래프를 보고 알 수 있는 내용을 한 문장으로 작성합니다.")

st.divider()


# ==========================================
# 그래프 5. 장르별 총 관객 박스플롯
# ==========================================
st.subheader("⑤ 장르별 총 관객 분포")

# 영화가 10편 이상인 장르만 선택
genre_counts = df["genre"].value_counts()

major_genres = genre_counts[
    genre_counts >= 10
].index

box_df = df[
    df["genre"].isin(major_genres)
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
        "genre": False
    },
    labels={
        "genre": "장르",
        "total_audi": "총 관객 수"
    },
    title="영화가 10편 이상인 장르의 총 관객 분포"
)

fig5.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "총 관객: %{y:,}명"
        "<extra></extra>"
    ),
    marker=dict(
        size=8,
        opacity=0.8
    )
)

fig5.update_layout(
    xaxis_title="장르",
    yaxis_title="총 관객 수",
    showlegend=False,
    margin=dict(t=50, l=20, r=20, b=20)
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것**")
st.info("여기에 이 그래프를 보고 알 수 있는 내용을 한 문장으로 작성합니다.")

st.divider()


# ==========================================
# 그래프 6. 버블 그래프
# ==========================================
st.subheader("⑥ 개봉일 스크린수와 총 관객의 관계 - 버블 그래프")

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
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객 수",
        "first_week_audi": "첫 주 관객",
        "genre": "장르"
    },
    title="개봉일 스크린수와 총 관객의 관계"
)

fig6.update_traces(
    marker=dict(
        opacity=0.7
    ),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "장르: %{customdata[0]}<br>"
        "개봉일 스크린수: %{x:,}개<br>"
        "총 관객: %{y:,}명<br>"
        "첫 주 관객: %{customdata[3]:,}명"
        "<extra></extra>"
    )
)

fig6.update_layout(
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객 수",
    legend_title="장르",
    margin=dict(t=50, l=20, r=20, b=20)
)

st.plotly_chart(fig6, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것**")
st.info("여기에 이 그래프를 보고 알 수 있는 내용을 한 문장으로 작성합니다.")

st.divider()


# ==========================================
# 그래프 7. 제작 국가 → 장르 선버스트
# ==========================================
st.subheader("⑦ 제작 국가와 장르별 영화 분포")

# 국가와 장르별 영화 편수를 먼저 계산
sunburst_df = (
    df.groupby(["nation", "genre"])
    .size()
    .reset_index(name="movie_count")
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

fig7.update_layout(
    margin=dict(t=50, l=10, r=10, b=10)
)

st.plotly_chart(fig7, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것**")
st.info("여기에 이 그래프를 보고 알 수 있는 내용을 한 문장으로 작성합니다.")

st.divider()

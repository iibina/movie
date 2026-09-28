# ----------------------------------
# 그래프 7. 제작 국가 → 장르 선버스트
# ----------------------------------
st.subheader("⑦ 제작 국가와 장르별 영화 분포")

# 제작 국가가 여러 개인 경우 첫 번째 국가만 사용
sunburst_df = df.copy()
sunburst_df["nation"] = (
    sunburst_df["nation"]
    .fillna("알 수 없음")
    .astype(str)
    .apply(lambda x: x.split("|")[0])
)

fig7 = px.sunburst(
    sunburst_df,
    path=["nation", "genre"],
    values=None,
    title="제작 국가 → 장르별 영화 편수"
)

# 영화 편수를 기준으로 칸 크기가 결정되도록 설정
fig7.update_traces(
    counts="value",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편"
        "<extra></extra>"
    )
)

fig7.update_layout(
    margin=dict(t=40, l=10, r=10, b=10)
)

st.plotly_chart(fig7, use_container_width=True)

# ----------------------------------
# 그래프 아래 설명 자리
# ----------------------------------
st.markdown("**이 그래프로 알 수 있는 것**")
st.info("여기에 이 그래프를 보고 알 수 있는 내용을 한 문장으로 작성합니다.")

st.divider()

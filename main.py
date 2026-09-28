# ----------------------------------
# 그래프 8. 10위권 체류 기간과 총 관객의 관계
# ----------------------------------
st.subheader("⑧ 10위권에 오래 머문 영화는 총 관객도 많은가")

fig8 = px.scatter(
    df,
    x="days_in_top10",
    y="total_audi",
    hover_name="movieNm",
    hover_data={
        "days_in_top10": True,
        "total_audi": ":,"
    },
    labels={
        "days_in_top10": "10위권에 머문 날수",
        "total_audi": "총 관객 수"
    },
    title="10위권에 오래 머문 영화는 총 관객도 많은가"
)

fig8.update_traces(
    marker=dict(
        size=10,
        opacity=0.75
    ),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "10위권에 머문 날수: %{x}일<br>"
        "총 관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig8.update_layout(
    xaxis_title="10위권에 머문 날수",
    yaxis_title="총 관객 수",
    margin=dict(t=40, l=20, r=20, b=20)
)

st.plotly_chart(fig8, use_container_width=True)

# ----------------------------------
# 그래프 아래 설명 자리
# ----------------------------------
st.markdown("**이 그래프로 알 수 있는 것**")
st.info("여기에 이 그래프를 보고 알 수 있는 내용을 한 문장으로 작성합니다.")

st.divider()

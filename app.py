# '최근 12개월 운동 현황' 제목 부분
st.markdown("<p style='font-size:1.1rem; font-weight:900; color:#0F172A; margin-bottom:4px;'>📈 최근 12개월 운동 현황</p>", unsafe_allow_html=True)

fig_all_months = px.bar(
    monthly_summary_12m,
    x="Month_Label",
    y="Total_Distance"
)

fig_all_months.update_traces(
    marker_color=monthly_summary_12m["Color"],
    cliponaxis=False,
    hoverinfo="none"
)

fig_all_months.add_hline(
    y=GOAL_KM, 
    line_dash="dot", 
    line_color="#64748B", 
    line_width=1.5
)

annotations_list = []
for idx, row in monthly_summary_12m.iterrows():
    val_str = f"{row['Total_Distance']:.1f}"
    annotations_list.append(dict(
        x=row["Month_Label"],
        y=row["Total_Distance"],
        text=val_str,
        showarrow=False,
        xanchor="center",
        yanchor="bottom",
        yshift=2,
        font=dict(size=9, color="#0F172A", family="Pretendard")
    ))

fig_all_months.update_layout(
    annotations=annotations_list,
    margin=dict(l=10, r=10, t=10, b=0),  # 👈 기존 t=40 에서 t=10으로 변경하여 간격을 좁힙니다.
    height=220,
    xaxis_title=None,
    yaxis_title=None,
    showlegend=False,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(fixedrange=True, showgrid=False, tickfont=dict(size=8, color="#64748B")),
    yaxis=dict(
        fixedrange=True, 
        showgrid=True, 
        gridcolor="#E2E8F0", 
        tickfont=dict(size=10, color="#64748B"), 
        rangemode="tozero"
    ),
    font=dict(size=10, color="#475569")
)
st.plotly_chart(fig_all_months, use_container_width=True, key="chart_all_months", config={'displayModeBar': False, 'scrollZoom': False, 'staticPlot': True})

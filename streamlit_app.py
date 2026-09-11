import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="YerForex | XAU/USD", page_icon="📊", layout="wide")
st.markdown("""
<style>
.stApp {background:#07131d;color:#eef5fb}
.block-container {padding-top:1.3rem;max-width:1500px}
[data-testid="stMetric"] {background:#0d1d29;border:1px solid #284154;padding:14px;border-radius:14px}
.yf-card {background:#0d1d29;border:1px solid #284154;border-radius:14px;padding:16px;margin:8px 0 16px}
.fact {border-left:5px solid #2da8ff}
.proj {border-left:5px solid #f2a900}
.small {color:#9eb0bf;font-size:.92rem}
h1,h2,h3 {color:#f5f8fb}
</style>
""", unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def load_ohlc():
    rows = [
        ["2026-08-10","Mon",4342.50,4396.71,4312.45,4388.96],
        ["2026-08-11","Tue",4389.82,4435.47,4356.49,4368.46],
        ["2026-08-12","Wed",4368.48,4441.26,4360.82,4408.70],
        ["2026-08-13","Thu",4409.88,4450.23,4343.76,4351.34],
        ["2026-08-14","Fri",4351.28,4397.25,4310.73,4376.60],
        ["2026-08-17","Mon",4381.12,4429.26,4367.24,4416.82],
        ["2026-08-18","Tue",4417.55,4436.39,4328.86,4334.52],
        ["2026-08-19","Wed",4334.68,4524.70,4324.49,4522.80],
        ["2026-08-20","Thu",4522.28,4541.49,4450.52,4519.08],
        ["2026-08-21","Fri",4519.09,4632.61,4508.83,4603.56],
        ["2026-08-24","Mon",4618.79,4681.40,4594.68,4651.87],
        ["2026-08-25","Tue",4654.11,4697.66,4605.17,4658.59],
        ["2026-08-26","Wed",4655.20,4674.20,4582.82,4593.68],
        ["2026-08-27","Thu",4596.75,4643.35,4566.17,4601.25],
        ["2026-08-28","Fri",4601.84,4630.25,4445.39,4455.15],
        ["2026-08-31","Mon",4453.21,4472.10,4396.48,4448.92],
        ["2026-09-01","Tue",4449.90,4465.55,4322.37,4329.50],
        ["2026-09-02","Wed",4330.70,4397.53,4282.71,4387.40],
        ["2026-09-03","Thu",4388.38,4511.00,4381.01,4474.06],
        ["2026-09-04","Fri",4481.02,4492.50,4365.59,4430.25],
    ]
    df = pd.DataFrame(rows, columns=["Date","Day","Open","High","Low","Close"])
    df["Date"] = pd.to_datetime(df["Date"])
    df["Change"] = df["Close"] - df["Open"]
    df["Direction"] = df["Change"].apply(lambda x: "Buy" if x > 0 else "Sell" if x < 0 else "Neutral")
    df["Range"] = df["High"] - df["Low"]
    return df

@st.cache_data(show_spinner=False)
def pattern_table(df):
    order = ["Mon","Tue","Wed","Thu","Fri"]
    out=[]
    for day in order:
        x=df[df["Day"]==day]
        bulls=int((x["Change"]>0).sum()); bears=int((x["Change"]<0).sum())
        out.append([day,bulls,bears,round(100*bulls/len(x)),round(x["Change"].mean(),2)])
    return pd.DataFrame(out,columns=["Day","Buy closes","Sell closes","% buy","Average Open→Close change"])

@st.cache_data(show_spinner=False)
def projection(df):
    med_change = df.groupby("Day")["Change"].median().to_dict()
    med_range = df.groupby("Day")["Range"].median().to_dict()
    # Conservative scenario: 25% of the historical median Open→Close change.
    # Daily band: projected Open/Close extremes +/- 25% of that weekday's median D1 range.
    last_close=float(df.iloc[-1]["Close"])
    labels=["Sun/Mon 14","Tue 15","Wed 16","Thu 17","Fri 18"]
    keys=["Mon","Tue","Wed","Thu","Fri"]
    rows=[]
    projected_open=last_close
    for label,key in zip(labels,keys):
        projected_close=projected_open + med_change[key]*0.25
        pad=med_range[key]*0.25
        low=min(projected_open,projected_close)-pad
        high=max(projected_open,projected_close)+pad
        rows.append([label,key,round(projected_open,2),round(projected_close,2),round(low,2),round(high,2)])
        projected_open=projected_close
    return pd.DataFrame(rows,columns=["Session","Day","Projected Open","Projected Close","Range Low","Range High"])

df=load_ohlc()
patterns=pattern_table(df)

st.title("YERFOREX — XAU/USD")
st.caption("D1 quantitative report | 4 complete weeks: Aug 10–Sep 04, 2026 | Validated historical data")

c1,c2,c3,c4=st.columns(4)
c1.metric("Sep 04 Close",f"${df.iloc[-1]['Close']:,.2f}")
c2.metric("20D High",f"${df['High'].max():,.2f}")
c3.metric("20D Low",f"${df['Low'].min():,.2f}")
c4.metric("Average D1 Range",f"${df['Range'].mean():,.2f}")
ret=(df.iloc[-1]['Close']/df.iloc[0]['Close']-1)*100
st.markdown(f"<div class='yf-card fact'><b>FACTS.</b> 20 complete D1 sessions. Initial close ${df.iloc[0]['Close']:,.2f} → final close ${df.iloc[-1]['Close']:,.2f} ({ret:+.2f}%). High ${df['High'].max():,.2f}; low ${df['Low'].min():,.2f}. OHLC source: Investing.com XAU/USD historical data.</div>",unsafe_allow_html=True)

st.header("1. The 4 weeks, one by one")
week_starts=["2026-08-10","2026-08-17","2026-08-24","2026-08-31"]
week_names=["Week Aug 10–14","Week Aug 17–21","Week Aug 24–28","Week Aug 31–Sep 04"]
for ws,name in zip(week_starts,week_names):
    start=pd.Timestamp(ws); w=df[(df.Date>=start)&(df.Date<=start+pd.Timedelta(days=4))]
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=w["Day"],y=w["Open"],mode="lines+markers+text",name="Open",text=[f"${v:,.0f}" for v in w.Open],textposition="bottom center"))
    fig.add_trace(go.Scatter(x=w["Day"],y=w["Close"],mode="lines+markers+text",name="Close",text=[f"${v:,.0f}" for v in w.Close],textposition="top center"))
    fig.update_layout(title=name,height=380,margin=dict(l=20,r=20,t=55,b=20),legend=dict(orientation="h"),xaxis_title="D1 Session",yaxis_title="USD/oz",template="plotly_dark")
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

st.header("2. What repeats across the 4 weeks?")
st.dataframe(patterns,use_container_width=True,hide_index=True)
mon=patterns.iloc[0]; tue=patterns.iloc[1]; wed=patterns.iloc[2]; fri=patterns.iloc[4]
st.markdown(f"""
<div class='yf-card fact'>
<b>Easy read:</b><br>
• <b>Monday:</b> {int(mon['Buy closes'])} of 4 finished above their open. It is the start of the week with the most consistent bullish bias in the sample.<br>
• <b>Tuesday:</b> {int(tue['Sell closes'])} of 4 finished lower; it was the most repeated bearish day, with an average change of {tue['Average Open→Close change']:+.2f} USD.<br>
• <b>Wednesday:</b> {int(wed['Buy closes'])} of 4 finished higher and recorded the largest positive average change ({wed['Average Open→Close change']:+.2f} USD). In this sample, Wednesday tended to recover/rebound after Tuesday weakness.<br>
• <b>Thursday:</b> 2 buys / 2 sells: there is not enough repetitive direction.<br>
• <b>Friday:</b> 2 buys / 2 sells, but the average was {fri['Average Open→Close change']:+.2f} USD because of the sharp Aug 28 decline. There is no stable directional signal.<br><br>
<b>Conclusion:</b> the clearest repetition across these four weeks is <b>weak Tuesday → Wednesday with a higher historical recovery frequency</b>. There are only 4 observations per weekday, so this is a sample pattern, not a guarantee.
</div>
""",unsafe_allow_html=True)

st.header("3. OHLC Table — 20 sessions")
show=df.copy(); show["Date"]=show["Date"].dt.strftime("%d %b %Y")
for c in ["Open","High","Low","Close","Change","Range"]: show[c]=show[c].map(lambda x:f"{x:,.2f}")
st.dataframe(show[["Date","Day","Open","High","Low","Close","Direction","Change","Range"]],use_container_width=True,hide_index=True)

st.header("4. Reaction / rebound levels")
levels=pd.DataFrame([
    ["4,365–4,381","Nearby support","Bullish rebound if price recovers and closes D1 above the zone","Sustained D1 close below 4,365","Sep 04 and Sep 03 lows; recent reaction zone"],
    ["4,310–4,329","Support","Bullish rebound","Loss of 4,310","Clusters Aug 10/14/18 and Sep 01 lows"],
    ["4,282.71","Extreme 20D support","Reaction only if the level is defended","New D1 low below 4,282.71","Absolute low of the 20-session sample"],
    ["4,492–4,525","Nearby resistance","Rejection/selling if price fails to consolidate above","Firm D1 close above 4,525","Sep 04, Sep 03 and Aug 19 highs"],
    ["4,630–4,698","Major resistance","Potential profit-taking/rejection","Breakout and D1 close above 4,698","Top of the 20-session sample"],
],columns=["USD Zone","Type","Reaction to watch","Invalidation","Rationale"])
st.dataframe(levels,use_container_width=True,hide_index=True)
st.caption("Levels are zones derived from the sample OHLC. They are not orders or execution guarantees.")

st.header("5. News and catalysts")
news=pd.DataFrame([
    ["Sep 10, 2026 08:30 ET","U.S. August PPI","STRONG","Released: +0.4% MoM; inflation pressure and higher rate-hike expectations","Bearish for gold through USD/yields, although geopolitics may offset it","BLS / Reuters"],
    ["Sep 11, 2026 08:30 ET","U.S. August CPI","VERY STRONG","Scheduled; not yet released when this report was generated","Potentially high XAU/USD volatility","BLS"],
    ["Sep 15–16, 2026","FOMC","VERY STRONG","Scheduled meeting; decision Sep 16 at 14:00 ET and press conference at 14:30 ET","Primary catalyst for USD, yields and gold","Federal Reserve"],
],columns=["Date/time","Event","Strength","Status","XAU/USD read","Source"])
st.dataframe(news,use_container_width=True,hide_index=True)
st.caption("Strength = qualitative estimate of potential XAU/USD volatility; it does not predict market direction.")
st.info("Current context: on Sep 10 Reuters reported a gold decline after firm PPI, a stronger dollar and higher yields. Sep 11 CPI and the Sep 15–16 FOMC are the next high-impact catalysts.")

st.header("6. Sunday–Friday Forecast — statistical scenario")
proj=projection(df)
fig=go.Figure()
# Shaded projected daily range band.
fig.add_trace(go.Scatter(x=proj["Session"],y=proj["Range High"],mode="lines+markers",name="Range High",line=dict(dash="dash"),hovertemplate="Range High: $%{y:,.2f}<extra></extra>"))
fig.add_trace(go.Scatter(x=proj["Session"],y=proj["Range Low"],mode="lines+markers",name="Range Low",line=dict(dash="dash"),fill="tonexty",fillcolor="rgba(120,150,190,0.20)",hovertemplate="Range Low: $%{y:,.2f}<extra></extra>"))
fig.add_trace(go.Scatter(x=proj["Session"],y=proj["Projected Open"],mode="lines+markers+text",name="Projected Open",text=[f"${v:,.0f}" for v in proj["Projected Open"]],textposition="bottom center",hovertemplate="Projected Open: $%{y:,.2f}<extra></extra>"))
fig.add_trace(go.Scatter(x=proj["Session"],y=proj["Projected Close"],mode="lines+markers+text",name="Projected Close",text=[f"${v:,.0f}" for v in proj["Projected Close"]],textposition="top center",hovertemplate="Projected Close: $%{y:,.2f}<extra></extra>"))
for _,r in proj.iterrows():
    fig.add_annotation(x=r["Session"],y=r["Range High"],text=f"Range ${r['Range Low']:,.0f}–${r['Range High']:,.0f}",showarrow=False,yshift=15,font=dict(size=11))
fig.add_hrect(y0=4365,y1=4381,opacity=.10,line_width=0,annotation_text="Nearby support")
fig.add_hrect(y0=4492,y1=4525,opacity=.10,line_width=0,annotation_text="Nearby resistance")
fig.update_layout(title="PROJECTION — Sep 14 to 18, 2026",height=520,template="plotly_dark",yaxis_title="USD/oz",xaxis_title="Session",margin=dict(l=20,r=20,t=60,b=20),legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="left",x=0))
st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
st.dataframe(proj[["Session","Projected Open","Projected Close","Range Low","Range High"]].style.format({"Projected Open":"${:,.2f}","Projected Close":"${:,.2f}","Range Low":"${:,.2f}","Range High":"${:,.2f}"}),use_container_width=True,hide_index=True)
st.markdown("<div class='yf-card proj'><b>PROJECTION, not fact.</b> The Open line starts from the last complete close and then links to the previous projected Close. The Close uses 25% of each weekday's historical median Open→Close change. The daily shading represents a statistical range built with 25% of that weekday's median D1 range around the projected Open/Close. The pattern favors relative strength on Monday/Wednesday and relative weakness on Tuesday.<br><br>CPI and FOMC can quickly invalidate this 4-week seasonality. For practical reading: watch 4,365–4,381 as support and 4,492–4,525 as resistance; a D1 breakout changes the scenario.</div>",unsafe_allow_html=True)

with st.expander("Methodology and sources"):
    st.write("OHLC: Investing.com XAU/USD Historical Data, Aug 10–Sep 04, 2026. News/calendar: U.S. Bureau of Labor Statistics, Federal Reserve and Reuters, verified Sep 10, 2026. The four weeks use only complete sessions; later partial data are not mixed into the statistical sample. The projection is descriptive/educational and does not replace risk management or constitute market certainty.")
st.caption(f"YerForex | generated/updated: {datetime.now().strftime('%d %b %Y')} | Code without polling or downloads on rerun; data and calculations cached.")

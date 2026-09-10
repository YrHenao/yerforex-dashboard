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
        ["2026-08-10","Lun",4342.50,4396.71,4312.45,4388.96],
        ["2026-08-11","Mar",4389.82,4435.47,4356.49,4368.46],
        ["2026-08-12","Mié",4368.48,4441.26,4360.82,4408.70],
        ["2026-08-13","Jue",4409.88,4450.23,4343.76,4351.34],
        ["2026-08-14","Vie",4351.28,4397.25,4310.73,4376.60],
        ["2026-08-17","Lun",4381.12,4429.26,4367.24,4416.82],
        ["2026-08-18","Mar",4417.55,4436.39,4328.86,4334.52],
        ["2026-08-19","Mié",4334.68,4524.70,4324.49,4522.80],
        ["2026-08-20","Jue",4522.28,4541.49,4450.52,4519.08],
        ["2026-08-21","Vie",4519.09,4632.61,4508.83,4603.56],
        ["2026-08-24","Lun",4618.79,4681.40,4594.68,4651.87],
        ["2026-08-25","Mar",4654.11,4697.66,4605.17,4658.59],
        ["2026-08-26","Mié",4655.20,4674.20,4582.82,4593.68],
        ["2026-08-27","Jue",4596.75,4643.35,4566.17,4601.25],
        ["2026-08-28","Vie",4601.84,4630.25,4445.39,4455.15],
        ["2026-08-31","Lun",4453.21,4472.10,4396.48,4448.92],
        ["2026-09-01","Mar",4449.90,4465.55,4322.37,4329.50],
        ["2026-09-02","Mié",4330.70,4397.53,4282.71,4387.40],
        ["2026-09-03","Jue",4388.38,4511.00,4381.01,4474.06],
        ["2026-09-04","Vie",4481.02,4492.50,4365.59,4430.25],
    ]
    df = pd.DataFrame(rows, columns=["Fecha","Día","Open","High","Low","Close"])
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    df["Cambio"] = df["Close"] - df["Open"]
    df["Dirección"] = df["Cambio"].apply(lambda x: "Compra" if x > 0 else "Venta" if x < 0 else "Neutro")
    df["Rango"] = df["High"] - df["Low"]
    return df

@st.cache_data(show_spinner=False)
def pattern_table(df):
    order = ["Lun","Mar","Mié","Jue","Vie"]
    out=[]
    for day in order:
        x=df[df["Día"]==day]
        bulls=int((x["Cambio"]>0).sum()); bears=int((x["Cambio"]<0).sum())
        out.append([day,bulls,bears,round(100*bulls/len(x)),round(x["Cambio"].mean(),2)])
    return pd.DataFrame(out,columns=["Día","Cierres compra","Cierres venta","% compra","Cambio medio Open→Close"])

@st.cache_data(show_spinner=False)
def projection(df):
    med = df.groupby("Día")["Cambio"].median().to_dict()
    # Escenario estadístico: se aplica 25% de la mediana histórica para no extrapolar movimientos extremos.
    start=float(df.iloc[-1]["Close"])
    days=["Dom/Lun 14","Mar 15","Mié 16","Jue 17","Vie 18"]
    keys=["Lun","Mar","Mié","Jue","Vie"]
    vals=[]; p=start
    for label,key in zip(days,keys):
        p += med[key]*0.25
        vals.append([label,round(p,2)])
    return pd.DataFrame(vals,columns=["Sesión","Escenario central"])

df=load_ohlc()
patterns=pattern_table(df)

st.title("YERFOREX — XAU/USD")
st.caption("Reporte cuantitativo D1 | 4 semanas completas: 10 Ago–04 Sep 2026 | Datos históricos validados")

c1,c2,c3,c4=st.columns(4)
c1.metric("Cierre 04 Sep",f"${df.iloc[-1]['Close']:,.2f}")
c2.metric("Máximo 20D",f"${df['High'].max():,.2f}")
c3.metric("Mínimo 20D",f"${df['Low'].min():,.2f}")
c4.metric("Rango D1 promedio",f"${df['Rango'].mean():,.2f}")

ret=(df.iloc[-1]['Close']/df.iloc[0]['Close']-1)*100
st.markdown(f"<div class='yf-card fact'><b>HECHOS.</b> 20 sesiones D1 completas. Cierre inicial ${df.iloc[0]['Close']:,.2f} → cierre final ${df.iloc[-1]['Close']:,.2f} ({ret:+.2f}%). Máximo ${df['High'].max():,.2f}; mínimo ${df['Low'].min():,.2f}. Fuente OHLC: Investing.com XAU/USD histórico.</div>",unsafe_allow_html=True)

st.header("1. Las 4 semanas, una por una")
week_starts=["2026-08-10","2026-08-17","2026-08-24","2026-08-31"]
week_names=["Semana 10–14 Ago","Semana 17–21 Ago","Semana 24–28 Ago","Semana 31 Ago–04 Sep"]
for ws,name in zip(week_starts,week_names):
    start=pd.Timestamp(ws); w=df[(df.Fecha>=start)&(df.Fecha<=start+pd.Timedelta(days=4))]
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=w["Día"],y=w["Open"],mode="lines+markers+text",name="Open",text=[f"${v:,.0f}" for v in w.Open],textposition="bottom center"))
    fig.add_trace(go.Scatter(x=w["Día"],y=w["Close"],mode="lines+markers+text",name="Close",text=[f"${v:,.0f}" for v in w.Close],textposition="top center"))
    fig.update_layout(title=name,height=380,margin=dict(l=20,r=20,t=55,b=20),legend=dict(orientation="h"),xaxis_title="Sesión D1",yaxis_title="USD/oz",template="plotly_dark")
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

st.header("2. ¿Qué se repite en las 4 semanas?")
st.dataframe(patterns,use_container_width=True,hide_index=True)
mon=patterns.iloc[0]; tue=patterns.iloc[1]; wed=patterns.iloc[2]; thu=patterns.iloc[3]; fri=patterns.iloc[4]
st.markdown(f"""
<div class='yf-card fact'>
<b>Lectura fácil:</b><br>
• <b>Lunes:</b> {int(mon['Cierres compra'])} de 4 terminaron por encima de su apertura. Es el inicio de semana con sesgo comprador más consistente de la muestra.<br>
• <b>Martes:</b> {int(tue['Cierres venta'])} de 4 terminaron en venta; fue el día bajista más repetido, con cambio medio de {tue['Cambio medio Open→Close']:+.2f} USD.<br>
• <b>Miércoles:</b> {int(wed['Cierres compra'])} de 4 terminaron en compra y registraron el mayor cambio medio positivo ({wed['Cambio medio Open→Close']:+.2f} USD). En esta muestra el miércoles tendió a recuperar/rebotar después de la debilidad del martes.<br>
• <b>Jueves:</b> 2 compras / 2 ventas: no hay dirección repetitiva suficiente.<br>
• <b>Viernes:</b> 2 compras / 2 ventas, pero el promedio fue {fri['Cambio medio Open→Close']:+.2f} USD por la caída fuerte del 28 Ago. No hay señal direccional estable.<br><br>
<b>Conclusión:</b> la repetición más clara de estas cuatro semanas es <b>martes débil → miércoles con mayor probabilidad histórica de recuperación</b>. Son 4 observaciones por día, por lo que es una pauta de muestra, no una garantía.
</div>
""",unsafe_allow_html=True)

st.header("3. Tabla OHLC — 20 sesiones")
show=df.copy(); show["Fecha"]=show["Fecha"].dt.strftime("%d %b %Y")
for c in ["Open","High","Low","Close","Cambio","Rango"]: show[c]=show[c].map(lambda x:f"{x:,.2f}")
st.dataframe(show[["Fecha","Día","Open","High","Low","Close","Dirección","Cambio","Rango"]],use_container_width=True,hide_index=True)

st.header("4. Niveles de reacción / rebote")
levels=pd.DataFrame([
    ["4,365–4,381","Soporte cercano","Rebote comprador si recupera y cierra D1 sobre la zona","Cierre D1 sostenido bajo 4,365","Mínimos del 04 Sep y 03 Sep; zona de reacción reciente"],
    ["4,310–4,329","Soporte","Rebote comprador","Pérdida de 4,310","Agrupa mínimos 10/14/18 Ago y 01 Sep"],
    ["4,282.71","Soporte extremo 20D","Reacción solo si el nivel se defiende","Nuevo mínimo D1 bajo 4,282.71","Mínimo absoluto de las 20 sesiones"],
    ["4,492–4,525","Resistencia cercana","Rechazo/venta si no consolida arriba","Cierre D1 firme sobre 4,525","Máximos 04 Sep, 03 Sep y 19 Ago"],
    ["4,630–4,698","Resistencia mayor","Toma de beneficio/rechazo potencial","Ruptura y cierre D1 sobre 4,698","Techo de la muestra de 20 sesiones"],
],columns=["Zona USD","Tipo","Reacción a vigilar","Invalidación","Fundamento"])
st.dataframe(levels,use_container_width=True,hide_index=True)
st.caption("Los niveles son zonas derivadas del OHLC de la muestra. No son órdenes ni garantías de ejecución.")

st.header("5. Noticias y catalizadores")
news=pd.DataFrame([
    ["10 Sep 2026 08:30 ET","PPI EE. UU. agosto","Publicado: +0.4% mensual; presión inflacionaria y mayores expectativas de subida de tipos","Bajista para oro vía USD/rendimientos, aunque la geopolítica puede compensar","BLS / Reuters"],
    ["11 Sep 2026 08:30 ET","CPI EE. UU. agosto","Programado; aún no publicado al generar este reporte","Alta volatilidad potencial en XAU/USD","BLS"],
    ["15–16 Sep 2026","FOMC","Reunión programada; decisión 16 Sep 14:00 ET y rueda de prensa 14:30 ET","Catalizador principal para USD, yields y oro","Federal Reserve"],
],columns=["Fecha/hora","Evento","Estado","Lectura para XAU/USD","Fuente"])
st.dataframe(news,use_container_width=True,hide_index=True)
st.info("Contexto actual: el 10 Sep Reuters informó caída del oro tras PPI firme, dólar más fuerte y mayores rendimientos. El CPI del 11 Sep y el FOMC del 15–16 Sep son los próximos catalizadores de alto impacto.")

st.header("6. Pronóstico Domingo–Viernes — escenario estadístico")
proj=projection(df)
fig=go.Figure(go.Scatter(x=proj["Sesión"],y=proj["Escenario central"],mode="lines+markers+text",text=[f"${v:,.0f}" for v in proj["Escenario central"]],textposition="top center",name="Proyección"))
fig.add_hrect(y0=4365,y1=4381,opacity=.15,line_width=0,annotation_text="Soporte cercano")
fig.add_hrect(y0=4492,y1=4525,opacity=.15,line_width=0,annotation_text="Resistencia cercana")
fig.update_layout(title="PROYECCIÓN — 14 al 18 Sep 2026",height=430,template="plotly_dark",yaxis_title="USD/oz",xaxis_title="Sesión",margin=dict(l=20,r=20,t=60,b=20))
st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
st.markdown("<div class='yf-card proj'><b>PROYECCIÓN, no hecho.</b> El escenario central parte del último cierre completo de la muestra (04 Sep: $4,430.25) y usa solo una fracción conservadora de la mediana Open→Close observada para cada día de la semana. La pauta favorece fortaleza relativa lunes/miércoles y debilidad relativa martes. El CPI del 11 Sep y, sobre todo, el FOMC del 15–16 Sep pueden invalidar rápidamente esa estacionalidad de 4 semanas. Para lectura práctica: primero observar 4,365–4,381 como soporte y 4,492–4,525 como resistencia; una ruptura D1 cambia el escenario.</div>",unsafe_allow_html=True)

with st.expander("Metodología y fuentes"):
    st.write("OHLC: Investing.com XAU/USD Historical Data, 10 Ago–04 Sep 2026. Noticias/calendario: U.S. Bureau of Labor Statistics, Federal Reserve y Reuters, verificados el 10 Sep 2026. Las cuatro semanas usan únicamente sesiones completas; los datos parciales posteriores no se mezclan con la muestra estadística. La proyección es descriptiva/educativa y no sustituye gestión de riesgo ni constituye una certeza de mercado.")

st.caption(f"YerForex | generado/actualizado: {datetime.now().strftime('%d %b %Y')} | Código sin polling ni descargas en rerun; datos y cálculos cacheados.")

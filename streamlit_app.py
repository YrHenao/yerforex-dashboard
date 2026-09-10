import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="YerForex | XAUUSD D1", page_icon="🥇", layout="wide")

DATA = [('2026-08-10', 4342.5, 4396.71, 4312.45, 4388.96), ('2026-08-11', 4389.82, 4435.47, 4356.49, 4368.46), ('2026-08-12', 4368.48, 4441.26, 4360.82, 4408.7), ('2026-08-13', 4409.88, 4450.23, 4343.76, 4351.34), ('2026-08-14', 4351.28, 4397.25, 4310.73, 4376.6), ('2026-08-17', 4381.12, 4429.26, 4367.24, 4416.82), ('2026-08-18', 4417.55, 4436.39, 4328.86, 4334.52), ('2026-08-19', 4334.68, 4524.7, 4324.49, 4522.8), ('2026-08-20', 4522.28, 4541.49, 4450.52, 4519.08), ('2026-08-21', 4519.09, 4632.61, 4508.83, 4603.56), ('2026-08-24', 4618.79, 4681.4, 4594.68, 4651.87), ('2026-08-25', 4654.11, 4697.66, 4605.17, 4658.59), ('2026-08-26', 4655.2, 4674.2, 4582.82, 4593.68), ('2026-08-27', 4596.75, 4643.35, 4566.17, 4601.25), ('2026-08-28', 4601.84, 4630.25, 4445.39, 4455.15), ('2026-08-31', 4453.21, 4472.1, 4396.48, 4448.92), ('2026-09-01', 4449.9, 4465.55, 4322.37, 4329.5), ('2026-09-02', 4330.7, 4397.53, 4282.71, 4387.4), ('2026-09-03', 4388.38, 4511.0, 4381.01, 4474.06), ('2026-09-04', 4481.02, 4492.5, 4365.59, 4430.25)]
CONTEXT = [('2026-09-07', 4427.79, 4436.03, 4381.08, 4405.07), ('2026-09-08', 4406.55, 4443.1, 4346.07, 4355.65), ('2026-09-09', 4360.4, 4434.18, 4341.44, 4394.22)]

df = pd.DataFrame(DATA, columns=["Fecha","Apertura","Máximo","Mínimo","Cierre"])
df["Fecha"] = pd.to_datetime(df["Fecha"])
ctx = pd.DataFrame(CONTEXT, columns=["Fecha","Apertura","Máximo","Mínimo","Cierre"])
ctx["Fecha"] = pd.to_datetime(ctx["Fecha"])

df["Rango"] = df["Máximo"]-df["Mínimo"]
prev = df["Cierre"].shift(1)
df["TR"] = np.maximum(df["Máximo"]-df["Mínimo"], np.maximum((df["Máximo"]-prev).abs(), (df["Mínimo"]-prev).abs()))
atr14 = df["TR"].rolling(14).mean().iloc[-1]
sma5 = df["Cierre"].rolling(5).mean().iloc[-1]
sma10 = df["Cierre"].rolling(10).mean().iloc[-1]
sma20 = df["Cierre"].mean()
delta = df["Cierre"].diff()
g = delta.clip(lower=0).rolling(14).mean()
l = (-delta.clip(upper=0)).rolling(14).mean()
rsi14 = (100 - 100/(1+g/l)).iloc[-1]

weekly = (df.assign(Semana=df["Fecha"].dt.to_period("W-FRI").astype(str))
          .groupby("Semana", as_index=False)
          .agg(Apertura=("Apertura","first"),Máximo=("Máximo","max"),Mínimo=("Mínimo","min"),Cierre=("Cierre","last")))
weekly["Variación %"]=(weekly["Cierre"]/weekly["Apertura"]-1)*100

projection = pd.DataFrame([
["Dom 13-sep",4394.22,4415.00,4368.00,"Neutral / apertura"],
["Lun 14-sep",4410.00,4455.00,4355.00,"Alcista moderado"],
["Mar 15-sep",4435.00,4490.00,4380.00,"Alcista"],
["Mié 16-sep",4450.00,4510.00,4395.00,"Alcista con resistencia"],
["Jue 17-sep",4438.00,4495.00,4375.00,"Consolidación"],
["Vie 18-sep",4425.00,4480.00,4350.00,"Neutral / volátil"],
], columns=["Sesión","Centro","Banda alta","Banda baja","Sesgo"])

st.title("XAUUSD · Reporte cuantitativo D1")
st.caption("YerForex Trading · Datos históricos validados · 10-sep-2026")
st.info("**HECHOS** = datos cerrados observados. **PROYECCIÓN** = escenario cuantitativo, no precio observado ni garantía.")

st.header("1. HECHOS — 4 semanas completas (20 sesiones)")
a,b,c,d,e=st.columns(5)
a.metric("Cierre 04-sep",f"{df['Cierre'].iloc[-1]:,.2f}")
b.metric("Variación 20 sesiones",f"{(df['Cierre'].iloc[-1]/df['Cierre'].iloc[0]-1)*100:+.2f}%")
c.metric("Máximo",f"{df['Máximo'].max():,.2f}")
d.metric("Mínimo",f"{df['Mínimo'].min():,.2f}")
e.metric("ATR(14)",f"{atr14:,.2f}")
st.caption(f"Rango medio: {df['Rango'].mean():,.2f} · SMA5: {sma5:,.2f} · SMA10: {sma10:,.2f} · SMA20: {sma20:,.2f} · RSI14: {rsi14:.1f}")

fig=go.Figure([go.Candlestick(x=df["Fecha"],open=df["Apertura"],high=df["Máximo"],low=df["Mínimo"],close=df["Cierre"],name="XAUUSD D1")])
fig.add_trace(go.Scatter(x=df["Fecha"],y=df["Cierre"].rolling(5).mean(),mode="lines",name="SMA 5"))
fig.add_trace(go.Scatter(x=df["Fecha"],y=df["Cierre"].rolling(10).mean(),mode="lines",name="SMA 10"))
fig.update_layout(title="XAUUSD D1 — histórico validado",height=560,xaxis_rangeslider_visible=False,yaxis_title="USD/oz",legend_orientation="h")
st.plotly_chart(fig,use_container_width=True)

st.subheader("Tabla de 20 días")
t=df[["Fecha","Apertura","Máximo","Mínimo","Cierre","Rango"]].copy()
t["Fecha"]=t["Fecha"].dt.strftime("%d-%m-%Y")
st.dataframe(t.style.format({"Apertura":"{:,.2f}","Máximo":"{:,.2f}","Mínimo":"{:,.2f}","Cierre":"{:,.2f}","Rango":"{:,.2f}"}),use_container_width=True,hide_index=True)

st.subheader("Resumen semanal")
st.dataframe(weekly.style.format({"Apertura":"{:,.2f}","Máximo":"{:,.2f}","Mínimo":"{:,.2f}","Cierre":"{:,.2f}","Variación %":"{:+.2f}%"}),use_container_width=True,hide_index=True)

st.subheader("Patrones observados")
st.markdown("""
- **10–14 ago:** avance semanal moderado.
- **17–21 ago:** expansión alcista fuerte; 19-ago fue la vela de mayor impulso del tramo.
- **24–28 ago:** máximo de cuatro semanas en **4,697.66** y reversión marcada hacia el viernes.
- **31-ago–4-sep:** barrido del mínimo de cuatro semanas en **4,282.71**, seguido de recuperación parcial.
- **Balance:** el primer a último cierre subió aproximadamente **0.94%**, pero SMA5 terminó debajo de SMA10 y SMA20, señal de menor impulso al final de la muestra.
""")

st.subheader("Contexto posterior ya cerrado: 7–9 sep")
ct=ctx.copy(); ct["Fecha"]=ct["Fecha"].dt.strftime("%d-%m-%Y")
st.dataframe(ct.style.format({"Apertura":"{:,.2f}","Máximo":"{:,.2f}","Mínimo":"{:,.2f}","Cierre":"{:,.2f}"}),use_container_width=True,hide_index=True)
st.caption("El 10-sep se excluye: la sesión estaba abierta durante la preparación del reporte y los snapshots intradía no eran estables.")

st.header("2. PROYECCIÓN — domingo 13 a viernes 18 sep")
st.warning("Escenario estadístico educativo. Las bandas no son OHLC reales ni una recomendación de compra/venta.")
st.dataframe(projection.style.format({"Centro":"{:,.2f}","Banda alta":"{:,.2f}","Banda baja":"{:,.2f}"}),use_container_width=True,hide_index=True)

fp=go.Figure()
fp.add_trace(go.Scatter(x=projection["Sesión"],y=projection["Banda alta"],mode="lines",name="Banda alta"))
fp.add_trace(go.Scatter(x=projection["Sesión"],y=projection["Banda baja"],mode="lines",name="Banda baja",fill="tonexty"))
fp.add_trace(go.Scatter(x=projection["Sesión"],y=projection["Centro"],mode="lines+markers",name="Escenario central"))
for y,label in [(4341.44,"S1"),(4322.37,"S2"),(4434.18,"R1"),(4492.50,"R2"),(4511.00,"R3")]:
    fp.add_hline(y=y,line_dash="dot",annotation_text=f"{label} {y:,.2f}")
fp.update_layout(title="PROYECCIÓN XAUUSD",height=520,yaxis_title="USD/oz",legend_orientation="h")
st.plotly_chart(fp,use_container_width=True)

st.markdown("""
**Lectura del escenario:** recuperación moderada mientras 4,341–4,322 se mantenga. Una recuperación sostenida sobre 4,434 vuelve relevantes 4,492–4,511. Una ruptura de 4,322 deteriora el escenario y devuelve foco a 4,282.71. Son condiciones analíticas, no instrucciones de ejecución.
""")

st.header("3. Metodología y fuentes")
st.markdown("""
**Muestra:** exactamente 20 sesiones D1 de cuatro semanas completas, 10-ago-2026 a 04-sep-2026.

**Validación:** OHLC cotejados entre las tablas históricas XAU/USD de Investing.com ES, CA y UK. El contexto 7–9 sep se mantiene separado de la muestra principal. El 10-sep no se trata como vela cerrada.

**Indicadores:** ATR(14) con True Range medio simple; SMA(5/10/20); RSI(14) con medias simples de ganancias y pérdidas. La proyección se construye con volatilidad reciente y niveles observados, sin mezclar datos proyectados con el histórico.

**Fuentes:** Investing.com XAU/USD Historical Data (ES, CA, UK), consultadas el 10-sep-2026.
""")
st.caption("YerForex Trading · D1 · Hechos y proyecciones separados")

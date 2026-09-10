import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title='YerForex | XAUUSD D1', page_icon='🥇', layout='wide')

st.markdown('''
<style>
.stApp {background:#071018;color:#eaf2f8}
.block-container {padding-top:1.5rem;max-width:1450px}
[data-testid="stMetric"] {background:#0d1924;border:1px solid #243746;border-radius:12px;padding:14px}
h1,h2,h3 {color:#f5c451}
.small {color:#9fb3c8;font-size:.88rem}
.fact {background:#0d1924;border-left:4px solid #4da3ff;padding:12px;border-radius:8px}
.proj {background:#171b22;border-left:4px solid #f5c451;padding:12px;border-radius:8px}
</style>
''', unsafe_allow_html=True)

hist = pd.DataFrame([
['2026-08-10',4342.50,4396.71,4312.45,4388.96],['2026-08-11',4389.82,4435.47,4356.49,4368.46],['2026-08-12',4368.48,4441.26,4360.82,4408.70],['2026-08-13',4409.88,4450.23,4343.76,4351.34],['2026-08-14',4351.28,4397.25,4310.73,4376.60],
['2026-08-17',4381.12,4429.26,4367.24,4416.82],['2026-08-18',4417.55,4436.39,4328.86,4334.52],['2026-08-19',4334.68,4524.70,4324.49,4522.80],['2026-08-20',4522.28,4541.49,4450.52,4519.08],['2026-08-21',4519.09,4632.61,4508.83,4603.56],
['2026-08-24',4618.79,4681.40,4594.68,4651.87],['2026-08-25',4654.11,4697.66,4605.17,4658.59],['2026-08-26',4655.20,4674.20,4582.82,4593.68],['2026-08-27',4596.75,4643.35,4566.17,4601.25],['2026-08-28',4601.84,4630.25,4445.39,4455.15],
['2026-08-31',4453.21,4472.10,4396.48,4448.92],['2026-09-01',4449.90,4465.55,4322.37,4329.50],['2026-09-02',4330.70,4397.53,4282.71,4387.40],['2026-09-03',4388.38,4511.00,4381.01,4474.06],['2026-09-04',4481.02,4492.50,4365.59,4430.25]],
columns=['Fecha','Apertura','Máximo','Mínimo','Cierre'])
hist['Fecha']=pd.to_datetime(hist['Fecha'])
hist['Rango']=hist['Máximo']-hist['Mínimo']
hist['Cambio %']=hist['Cierre'].pct_change()*100

proj = pd.DataFrame([
['2026-09-13','Domingo',4360,4315,4410,'Neutral / apertura'],
['2026-09-14','Lunes',4340,4285,4415,'Bajista moderado'],
['2026-09-15','Martes',4375,4300,4450,'Rebote'],
['2026-09-16','Miércoles',4405,4330,4480,'Alcista moderado'],
['2026-09-17','Jueves',4370,4290,4460,'Volátil / neutral'],
['2026-09-18','Viernes',4400,4320,4490,'Neutral-alcista']],
columns=['Fecha','Día','Centro','Banda baja','Banda alta','Sesgo'])
proj['Fecha']=pd.to_datetime(proj['Fecha'])

st.title('YERFOREX — XAUUSD · D1')
st.caption('Reporte cuantitativo | 4 semanas completas: 10 Ago–4 Sep 2026 | Proyección: 13–18 Sep 2026')

c1,c2,c3,c4=st.columns(4)
c1.metric('Cierre 04 Sep',f"${hist.iloc[-1]['Cierre']:,.2f}")
c2.metric('Máximo 20D',f"${hist['Máximo'].max():,.2f}")
c3.metric('Mínimo 20D',f"${hist['Mínimo'].min():,.2f}")
c4.metric('Rango D1 promedio',f"${hist['Rango'].mean():,.2f}")

st.markdown('<div class="fact"><b>HECHOS.</b> La muestra contiene 20 sesiones D1 completas. Cierre inicial $4,388.96 → cierre final $4,430.25 (+0.94%). Máximo del periodo $4,697.66; mínimo $4,282.71. SMA5 de cierres: $4,414.03; SMA10: $4,503.07. Fuente OHLC: Investing.com XAU/USD histórico.</div>', unsafe_allow_html=True)

fig=go.Figure(data=[go.Candlestick(x=hist['Fecha'],open=hist['Apertura'],high=hist['Máximo'],low=hist['Mínimo'],close=hist['Cierre'],name='XAUUSD')])
fig.update_layout(template='plotly_dark',height=520,title='XAUUSD — 20 sesiones D1 verificadas',xaxis_rangeslider_visible=False,margin=dict(l=20,r=20,t=60,b=20))
st.plotly_chart(fig,use_container_width=True)

st.subheader('Tabla D1 — 20 sesiones')
show=hist.copy(); show['Fecha']=show['Fecha'].dt.strftime('%Y-%m-%d')
st.dataframe(show.style.format({'Apertura':'{:,.2f}','Máximo':'{:,.2f}','Mínimo':'{:,.2f}','Cierre':'{:,.2f}','Rango':'{:,.2f}','Cambio %':'{:+.2f}%'}),use_container_width=True,hide_index=True)

st.subheader('Lectura de patrones')
st.markdown('''
- **Expansión de volatilidad:** el rango D1 medio fue **$107.22**; 19 Ago ($200.21) y 28 Ago ($184.86) fueron sesiones de expansión destacadas.
- **Impulso y reversión:** tras el máximo de $4,697.66 (25 Ago), el precio corrigió con fuerza y marcó $4,282.71 el 2 Sep antes de rebotar.
- **Estructura al 4 Sep:** cierre $4,430.25, por encima de SMA5 ($4,414.03) pero por debajo de SMA10 ($4,503.07): recuperación corta dentro de una estructura todavía volátil.
- **Zonas cuantitativas de referencia:** soporte histórico de muestra $4,283–$4,325; pivote $4,400–$4,450; resistencia $4,510 y luego $4,630–$4,698.
''')

st.markdown('<div class="proj"><b>PROYECCIÓN — NO ES DATO OBSERVADO.</b> Escenario central para 13–18 Sep construido con estructura D1 de la muestra, rango medio y el régimen macro vigente. Las bandas son zonas de incertidumbre, no objetivos garantizados.</div>', unsafe_allow_html=True)

pfig=go.Figure()
pfig.add_trace(go.Scatter(x=proj['Fecha'],y=proj['Banda alta'],mode='lines',line=dict(width=0),showlegend=False,hoverinfo='skip'))
pfig.add_trace(go.Scatter(x=proj['Fecha'],y=proj['Banda baja'],mode='lines',fill='tonexty',line=dict(width=0),name='Banda proyectada'))
pfig.add_trace(go.Scatter(x=proj['Fecha'],y=proj['Centro'],mode='lines+markers',name='Escenario central'))
pfig.update_layout(template='plotly_dark',height=460,title='PROYECCIÓN XAUUSD · Domingo–Viernes',yaxis_title='USD por onza',margin=dict(l=20,r=20,t=60,b=20))
st.plotly_chart(pfig,use_container_width=True)

p=proj.copy(); p['Fecha']=p['Fecha'].dt.strftime('%Y-%m-%d')
st.dataframe(p.style.format({'Centro':'{:,.0f}','Banda baja':'{:,.0f}','Banda alta':'{:,.0f}'}),use_container_width=True,hide_index=True)

st.subheader('Contexto macro actual')
st.write('El 10 Sep, Reuters informó presión bajista sobre el oro tras un PPI estadounidense de +0.4% mensual, fortalecimiento del dólar y alza de rendimientos; al mismo tiempo, petróleo por encima de $100 y tensiones geopolíticas elevan el riesgo inflacionario y pueden sostener demanda defensiva. El resultado es un régimen de alta volatilidad y señales macro contrapuestas.')

st.info('Uso educativo y analítico. La proyección es probabilística y puede fallar; no constituye recomendación de compra/venta ni sustituye gestión de riesgo.')
st.caption('Fuentes verificadas al 10 Sep 2026: Investing.com — XAU/USD Historical Data; Reuters — Gold falls over 1% as US inflation data boosts Fed hike bets; Reuters — US producer prices increase as expected in August; Reuters — Oil surges 6%, Brent and US crude both surpass $100.')

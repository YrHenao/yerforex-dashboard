import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="YerForex Trading — XAU/USD", layout="wide")
st.title("YerForex Trading — Reporte XAU/USD")
st.caption("Estructura D1 · 4 semanas completas · Datos históricos validados antes de construir el reporte")

rows = [
("Semana 1","Lun 10 Ago","2026-08-09 18:00 EDT",4342.50,"2026-08-10 17:00 EDT",4388.96),
("Semana 1","Mar 11 Ago","2026-08-10 18:00 EDT",4389.82,"2026-08-11 17:00 EDT",4368.46),
("Semana 1","Mié 12 Ago","2026-08-11 18:00 EDT",4368.48,"2026-08-12 17:00 EDT",4408.70),
("Semana 1","Jue 13 Ago","2026-08-12 18:00 EDT",4409.88,"2026-08-13 17:00 EDT",4351.34),
("Semana 1","Vie 14 Ago","2026-08-13 18:00 EDT",4351.28,"2026-08-14 17:00 EDT",4376.60),
("Semana 2","Lun 17 Ago","2026-08-16 18:00 EDT",4381.12,"2026-08-17 17:00 EDT",4416.82),
("Semana 2","Mar 18 Ago","2026-08-17 18:00 EDT",4417.55,"2026-08-18 17:00 EDT",4334.52),
("Semana 2","Mié 19 Ago","2026-08-18 18:00 EDT",4334.68,"2026-08-19 17:00 EDT",4522.80),
("Semana 2","Jue 20 Ago","2026-08-19 18:00 EDT",4522.28,"2026-08-20 17:00 EDT",4519.08),
("Semana 2","Vie 21 Ago","2026-08-20 18:00 EDT",4519.09,"2026-08-21 17:00 EDT",4603.56),
("Semana 3","Lun 24 Ago","2026-08-23 18:00 EDT",4618.79,"2026-08-24 17:00 EDT",4651.87),
("Semana 3","Mar 25 Ago","2026-08-24 18:00 EDT",4654.11,"2026-08-25 17:00 EDT",4658.59),
("Semana 3","Mié 26 Ago","2026-08-25 18:00 EDT",4655.20,"2026-08-26 17:00 EDT",4593.68),
("Semana 3","Jue 27 Ago","2026-08-26 18:00 EDT",4596.75,"2026-08-27 17:00 EDT",4601.25),
("Semana 3","Vie 28 Ago","2026-08-27 18:00 EDT",4601.84,"2026-08-28 17:00 EDT",4455.15),
("Semana 4","Lun 31 Ago","2026-08-30 18:00 EDT",4453.21,"2026-08-31 17:00 EDT",4448.92),
("Semana 4","Mar 01 Sep","2026-08-31 18:00 EDT",4449.90,"2026-09-01 17:00 EDT",4329.50),
("Semana 4","Mié 02 Sep","2026-09-01 18:00 EDT",4330.70,"2026-09-02 17:00 EDT",4387.40),
("Semana 4","Jue 03 Sep","2026-09-02 18:00 EDT",4388.38,"2026-09-03 17:00 EDT",4474.06),
("Semana 4","Vie 04 Sep","2026-09-03 18:00 EDT",4481.02,"2026-09-04 17:00 EDT",4430.25),
]
df=pd.DataFrame(rows,columns=["Semana","Vela Diaria (TradingView)","Inicio de la Vela (Apertura)","Precio Apertura","Fin de la Vela (Cierre 17:00 EDT)","Precio Cierre"])
df["Variación (%)"]=(df["Precio Cierre"]/df["Precio Apertura"]-1)*100

def weekly_chart(d, title, projection=False):
    fig, ax=plt.subplots(figsize=(16,9))
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#e9e9f1")
    x=np.arange(len(d))
    ax.plot(x,d["Precio Apertura"],marker="o",linewidth=2.6,label="Precio de Apertura (Open)")
    ax.plot(x,d["Precio Cierre"],marker="s",linewidth=2.6,label="Precio de Cierre (Close)")
    ax.grid(True,linestyle="--",alpha=.65)
    ax.set_xticks(x)
    ax.set_xticklabels(d["Vela Diaria (TradingView)"],fontsize=12)
    ax.set_ylabel("Precio en USD ($/oz)",fontsize=12,fontweight="bold")
    ax.set_xlabel("Vela Diaria (TradingView)",fontsize=12,fontweight="bold")
    ax.set_title(title,fontsize=16,fontweight="bold",pad=18)
    ax.legend(loc="upper left",fontsize=11)
    span=max(d["Precio Apertura"].max(),d["Precio Cierre"].max())-min(d["Precio Apertura"].min(),d["Precio Cierre"].min())
    off=max(span*.035,4)
    for i,(o,c) in enumerate(zip(d["Precio Apertura"],d["Precio Cierre"])):
        ax.annotate(f"${o:,.2f}",(i,o),xytext=(0,-15),textcoords="offset points",ha="center",fontsize=10,fontweight="bold")
        ax.annotate(f"${c:,.2f}",(i,c),xytext=(0,10),textcoords="offset points",ha="center",fontsize=10,fontweight="bold")
    fig.tight_layout()
    return fig

ranges=[
("Semana 1","10 al 14 de Agosto de 2026"),
("Semana 2","17 al 21 de Agosto de 2026"),
("Semana 3","24 al 28 de Agosto de 2026"),
("Semana 4","31 de Agosto al 04 de Septiembre de 2026"),
]
for wk,label in ranges:
    d=df[df.Semana==wk].copy()
    st.header(f"{wk} — {label}")
    net=d.iloc[-1]["Precio Cierre"]-d.iloc[0]["Precio Apertura"]
    pct=(d.iloc[-1]["Precio Cierre"]/d.iloc[0]["Precio Apertura"]-1)*100
    c1,c2,c3=st.columns(3)
    c1.metric("Apertura semanal",f"${d.iloc[0]['Precio Apertura']:,.2f}")
    c2.metric("Cierre viernes",f"${d.iloc[-1]['Precio Cierre']:,.2f}")
    c3.metric("Rendimiento semanal",f"{pct:+.2f}%",f"${net:+,.2f}")
    st.pyplot(weekly_chart(d,f"Evolución Semanal del Oro (XAU/USD) - Semana del {label}"),use_container_width=True)

st.header("Tabla consolidada — 20 velas D1")
show=df.copy()
show["Precio Apertura"]=show["Precio Apertura"].map(lambda x:f"${x:,.2f}")
show["Precio Cierre"]=show["Precio Cierre"].map(lambda x:f"${x:,.2f}")
show["Variación (%)"]=show["Variación (%)"].map(lambda x:f"{x:+.2f}%")
st.dataframe(show,use_container_width=True,hide_index=True)

st.header("Patrones observados")
wd=np.tile(["Lunes","Martes","Miércoles","Jueves","Viernes"],4)
tmp=df.copy(); tmp["Día"]=wd
means=tmp.groupby("Día",sort=False)["Variación (%)"].mean().reindex(["Lunes","Martes","Miércoles","Jueves","Viernes"])
st.write("Promedio por día:", {k:f"{v:+.2f}%" for k,v in means.items()})
st.write("La mayor expansión absoluta de las 20 velas fue el miércoles 19 de agosto, con +4.34% de apertura a cierre. Los martes fueron el día promedio más débil (-1.24%); los miércoles, el más fuerte (+1.31%).")
st.info("No se calcula el rango dominical 18:05–23:30 porque estas fuentes D1 no aportan datos intradía suficientes para validarlo.")

st.header("PROYECCIÓN — semana del 07 al 11 de Septiembre de 2026")
last=4430.25
pred=[]
for day,pct in means.items():
    op=last
    cl=op*(1+pct/100)
    pred.append((day,op,pct,cl))
    last=cl
pr=pd.DataFrame(pred,columns=["Día / Sesión","Apertura Proyectada","Variación Promedio (4 Semanas)","Cierre Proyectado"])
disp=pr.copy()
disp["Apertura Proyectada"]=disp["Apertura Proyectada"].map(lambda x:f"${x:,.2f}")
disp["Variación Promedio (4 Semanas)"]=disp["Variación Promedio (4 Semanas)"].map(lambda x:f"{x:+.2f}%")
disp["Cierre Proyectado"]=disp["Cierre Proyectado"].map(lambda x:f"${x:,.2f}")
st.dataframe(disp,use_container_width=True,hide_index=True)

pg=pd.DataFrame({
    "Vela Diaria (TradingView)":["Lun 07","Mar 08","Mié 09","Jue 10","Vie 11"],
    "Precio Apertura":pr["Apertura Proyectada"],
    "Precio Cierre":pr["Cierre Proyectado"]
})
st.pyplot(weekly_chart(pg,"PROYECCIÓN — Evolución Semanal del Oro (XAU/USD) - 07 al 11 de Septiembre de 2026",True),use_container_width=True)

st.warning("PROYECCIÓN ESTADÍSTICA: se obtiene encadenando el promedio de variación apertura→cierre de cada día de la semana durante las cuatro semanas históricas. No garantiza resultados ni constituye una recomendación de compra o venta.")

st.header("Metodología y fuentes")
st.markdown("""
- Histórico principal: Investing.com, XAU/USD Historical Data, marco diario.
- Contraste: Myfxbook XAUUSD Historical Data para el tramo de agosto.
- Ventana histórica: 10 de agosto a 4 de septiembre de 2026 (4 semanas completas, 20 velas).
- La proyección parte del último cierre real del viernes 4 de septiembre: **$4,430.25**.
- Los horarios de la tabla expresan la convención operativa solicitada en EDT; los precios diarios provienen de las fuentes históricas citadas y pueden variar frente a un feed/broker específico por definición de sesión.
""")

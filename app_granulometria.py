import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import io  # <-- Para crear el archivo Excel en memoria

# Configuración de la página (layout ancho y tema oscuro)
st.set_page_config(page_title="Gestión de Procesos Metalúrgicos", layout="wide")

# --- CONTROL DE NAVEGACIÓN CON MENÚ DESPLEGABLE ---
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = "Inicio"

st.sidebar.title("Menú de Navegación")

# 1. Opción suelta: Inicio
if st.sidebar.button("🏠 Inicio", use_container_width=True):
    st.session_state.pagina_actual = "Inicio"

# 2. Categoría Desplegable: Caracterización Mineralógica
with st.sidebar.expander("🔬 Caracterización Mineralógica", expanded=True):
    if st.button("🟢 Minerales sulfurados", use_container_width=True):
        st.session_state.pagina_actual = "Minerales sulfurados"
        
    if st.button("🟤 Minerales oxidados", use_container_width=True):
        st.session_state.pagina_actual = "Minerales oxidados"

# 3. Categoría Desplegable: Conminución
with st.sidebar.expander("⚙️ Conminución", expanded=True):
    if st.button("📊 Análisis granulométrico", use_container_width=True):
        st.session_state.pagina_actual = "Análisis granulométrico"
        
    if st.button("⚡ Calculadora Ley de Bond", use_container_width=True):
        st.session_state.pagina_actual = "Calculadora Ley de Bond"
        
    if st.button("📐 Razón de Reducción", use_container_width=True):
        st.session_state.pagina_actual = "Razón de Reducción"

    if st.button("📈 Modelos Granulométricos (GS / RR)", use_container_width=True):
        st.session_state.pagina_actual = "Modelos Granulométricos"

seccion = st.session_state.pagina_actual


# =====================================================================
# --- FUNCIÓN AUXILIAR PARA TARJETAS DE MINERALES ---
# =====================================================================
def mineral_card(color, name, formula, grade_text):
    """Genera el HTML/CSS de una tarjeta de mineral responsiva para modo oscuro"""
    return f"""
    <div style="background-color: #1e222d; padding: 30px 15px; border-radius: 16px; text-align: center; margin-bottom: 20px; box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); border-bottom: 4px solid {color}; transition: transform 0.3s ease;">
        <div style="width: 55px; height: 55px; border-radius: 50%; background-color: {color}; margin: 0 auto 18px auto; box-shadow: 0 0 15px {color}aa; border: 2px solid rgba(255,255,255,0.2);"></div>
        <div style="font-size: 1.45rem; font-weight: 800; color: #ffffff; margin-bottom: 12px; letter-spacing: 0.5px;">{name}</div>
        <div style="font-size: 1rem; color: #a1aab5; margin-bottom: 10px; font-family: monospace;">{formula}</div>
        <div style="font-size: 1.15rem; color: #4ade80; font-weight: 700; background-color: rgba(74, 222, 128, 0.1); padding: 5px 10px; border-radius: 8px; display: inline-block;">{grade_text}</div>
    </div>
    """


# =====================================================================
# --- PÁGINA: INICIO ---
# =====================================================================
if seccion == "Inicio":
    st.title("Bienvenido a tu plataforma de Procesos Metalúrgicos")
    st.write("Una herramienta diseñada para apoyar el análisis, desarrollo y gestión de tus proyectos y procesos metalúrgicos.")
    
    st.info("Utiliza el menú de navegación para acceder a las diferentes herramientas y módulos de la plataforma. Explora las funcionalidades disponibles y lleva tus análisis metalúrgicos al siguiente nivel.", icon="👈")
    st.markdown("---") 

    col1, col2, col3, col4, col5 = st.columns(5)

    def process_card(emoji, title, desc, col, glow_color):
        with col:
            st.markdown(
                f"""
                <div style="background-color: #1e222d; padding: 20px 10px; border-radius: 12px; text-align: center; margin-bottom: 25px; box-shadow: 0 5px 10px -2px {glow_color}, 0 2px 5px -1px rgba(0, 0, 0, 0.06);">
                    <div style="font-size: 3.5rem; margin-bottom: 15px; filter: drop-shadow(0 0 7px {glow_color});">{emoji}</div>
                    <div style="font-size: 1.05rem; font-weight: bold; color: white; margin-bottom: 7px; text-transform: uppercase; white-space: nowrap; letter-spacing: -0.5px;">{title}</div>
                    <div style="font-size: 0.9rem; color: #a1aab5; line-height: 1.4; white-space: normal;">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    process_card("🔬", "CARACTERIZACIÓN", "MINERALES SULFURADOS Y OXIDADOS.", col1, "rgba(0, 191, 255, 0.3)")
    process_card("⛰️", "CONMINUCIÓN", "REDUCCIÓN DE TAMAÑO DEL MINERAL.", col2, "rgba(255, 255, 255, 0.3)")


# =====================================================================
# --- PÁGINAS: CARACTERIZACIÓN METALÚRGICA ---
# =====================================================================
elif seccion == "Minerales sulfurados":
    st.title("🟢 Minerales Sulfurados")
    st.write("Analiza las propiedades, leyes teóricas y comportamientos de las principales especies sulfuradas de cobre y molibdeno.")
    
    st.markdown("### 📚 Base de Propiedades")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(mineral_card("#eab308", "Calcopirita", "CuFeS₂", "Ley Cu: 34.6%"), unsafe_allow_html=True)
    with col2:
        st.markdown(mineral_card("#9d4edd", "Bornita", "Cu₅FeS₄", "Ley Cu: 63.3%"), unsafe_allow_html=True)
    with col3:
        st.markdown(mineral_card("#64748b", "Calcosina", "Cu₂S", "Ley Cu: 79.8%"), unsafe_allow_html=True)
    with col4:
        st.markdown(mineral_card("#3b82f6", "Covelina", "CuS", "Ley Cu: 66.4%"), unsafe_allow_html=True)

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.markdown(mineral_card("#475569", "Enargita", "Cu₃AsS₄", "Ley Cu: 48.4%"), unsafe_allow_html=True)
    with col6:
        st.markdown(mineral_card("#334155", "Tenantita", "Cu₁₂As₄S₁₃", "Ley Cu: 51.6%"), unsafe_allow_html=True)
    with col7:
        st.markdown(mineral_card("#94a3b8", "Molibdenita", "MoS₂", "Ley Mo: 59.9%"), unsafe_allow_html=True)
    with col8:
        st.markdown(mineral_card("#facc15", "Pirita", "FeS₂", "Ley Cu: 0.0%"), unsafe_allow_html=True)
        
    st.markdown("---")
    
    st.markdown("### 🧮 Estimador de Ley de Cabeza")
    st.write("**Composición Mineralógica de la Mena**")
    st.write("Ingresa el porcentaje en peso (%) que representa cada sulfuro dentro de la roca total para estimar la Ley de Cabeza (Cu y Mo).")
    
    c1, c2, c3, c4 = st.columns(4)
    pct_cpy = c1.number_input("% Calcopirita", min_value=0.0, max_value=100.0, value=0.0, format="%.2f", step=0.10)
    pct_brn = c2.number_input("% Bornita", min_value=0.0, max_value=100.0, value=0.0, format="%.2f", step=0.10)
    pct_ccs = c3.number_input("% Calcosina", min_value=0.0, max_value=100.0, value=0.0, format="%.2f", step=0.10)
    pct_cov = c4.number_input("% Covelina", min_value=0.0, max_value=100.0, value=0.0, format="%.2f", step=0.10)
    
    c5, c6, c7, c8 = st.columns(4)
    pct_ena = c5.number_input("% Enargita", min_value=0.0, max_value=100.0, value=0.0, format="%.2f", step=0.10)
    pct_ten = c6.number_input("% Tenantita", min_value=0.0, max_value=100.0, value=0.0, format="%.2f", step=0.10)
    pct_mol = c7.number_input("% Molibdenita", min_value=0.0, max_value=100.0, value=0.0, format="%.2f", step=0.10)
    pct_py  = c8.number_input("% Pirita", min_value=0.0, max_value=100.0, value=0.0, format="%.2f", step=0.10)
    
    ley_cpy, ley_brn, ley_ccs, ley_cov = 34.6, 63.3, 79.8, 66.4
    ley_ena, ley_ten, ley_py = 48.4, 51.6, 0.0
    ley_mol_mo = 59.9
    
    ley_cabeza_cu = (pct_cpy*ley_cpy + pct_brn*ley_brn + pct_ccs*ley_ccs + pct_cov*ley_cov + pct_ena*ley_ena + pct_ten*ley_ten) / 100
    ley_cabeza_mo = (pct_mol * ley_mol_mo) / 100
    
    pct_ganga = 100.0 - (pct_cpy + pct_brn + pct_ccs + pct_cov + pct_ena + pct_ten + pct_mol + pct_py)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if pct_ganga < 0:
        st.error("⚠️ La suma de los minerales no puede superar el 100%. Revisa los valores ingresados.")
    else:
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.success(f"**Ley Estimada de Cobre:** {ley_cabeza_cu:.3f} % Cu")
        with col_res2:
            st.info(f"**Ley Estimada de Molibdeno:** {ley_cabeza_mo:.4f} % Mo")
            
        st.caption(f"Ganga silícea / Otros minerales no reportados: {pct_ganga:.2f}% del peso de la muestra.")


elif seccion == "Minerales oxidados":
    st.title("🟤 Minerales Oxidados")
    st.write("Analiza las propiedades, leyes teóricas y comportamientos de las principales especies oxidadas de cobre (solubles en ácido).")
    
    st.markdown("### 📚 Base de Propiedades")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(mineral_card("#22c55e", "Malaquita", "Cu₂CO₃(OH)₂", "Ley Cu: 57.5%"), unsafe_allow_html=True)
    with col2:
        st.markdown(mineral_card("#2563eb", "Azurita", "Cu₃(CO₃)₂(OH)₂", "Ley Cu: 55.3%"), unsafe_allow_html=True)
    with col3:
        st.markdown(mineral_card("#06b6d4", "Crisocola", "(Cu,Al)₂H₂Si₂O₅...", "Ley Cu: 36.0%"), unsafe_allow_html=True)
    with col4:
        st.markdown(mineral_card("#ef4444", "Cuprita", "Cu₂O", "Ley Cu: 88.8%"), unsafe_allow_html=True)
        
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.markdown(mineral_card("#111827", "Tenorita", "CuO", "Ley Cu: 79.9%"), unsafe_allow_html=True)
    with col6:
        st.markdown(mineral_card("#15803d", "Atacamita", "Cu₂Cl(OH)₃", "Ley Cu: 59.5%"), unsafe_allow_html=True)
    with col7:
        st.markdown(mineral_card("#047857", "Brochantita", "Cu₄SO₄(OH)₆", "Ley Cu: 56.2%"), unsafe_allow_html=True)
    with col8:
        st.markdown(mineral_card("#0ea5e9", "Calcantita", "CuSO₄·5H₂O", "Ley Cu: 25.5%"), unsafe_allow_html=True)
        
    st.markdown("---")
    
    st.markdown("### 🧮 Estimador de Ley de Cabeza (Cobre Soluble / Total)")
    st.write("**Composición Mineralógica de la Mena**")
    st.write("Ingresa el porcentaje en peso (%) que representa cada mineral oxidado dentro de la roca total para estimar la Ley de Cabeza de Cobre.")
    
    c1, c2, c3, c4 = st.columns(4)
    pct_mal = c1.number_input("% Malaquita", min_value=0.0, max_value=100.0, value=0.0, format="%.2f", step=0.10)
    pct_azu = c2.number_input("% Azurita", min_value=0.0, max_value=100.0, value=0.0, format="%.2f", step=0.10)
    pct_cri = c3.number_input("% Crisocola", min_value=0.0, max_value=100.0, value=0.0, format="%.2f", step=0.10)
    pct_cup = c4.number_input("% Cuprita", min_value=0.0, max_value=100.0, value=0.0, format="%.2f", step=0.10)
    
    c5, c6, c7, c8 = st.columns(4)
    pct_ten = c5.number_input("% Tenorita", min_value=0.0, max_value=100.0, value=0.0, format="%.2f", step=0.10)
    pct_ata = c6.number_input("% Atacamita", min_value=0.0, max_value=100.0, value=0.0, format="%.2f", step=0.10)
    pct_bro = c7.number_input("% Brochantita", min_value=0.0, max_value=100.0, value=0.0, format="%.2f", step=0.10)
    pct_cal = c8.number_input("% Calcantita", min_value=0.0, max_value=100.0, value=0.0, format="%.2f", step=0.10)
    
    ley_mal, ley_azu, ley_cri, ley_cup = 57.5, 55.3, 36.0, 88.8
    ley_ten, ley_ata, ley_bro, ley_cal = 79.9, 59.5, 56.2, 25.5
    
    ley_cabeza_cu_ox = (pct_mal*ley_mal + pct_azu*ley_azu + pct_cri*ley_cri + pct_cup*ley_cup + pct_ten*ley_ten + pct_ata*ley_ata + pct_bro*ley_bro + pct_cal*ley_cal) / 100
    
    pct_ganga_ox = 100.0 - (pct_mal + pct_azu + pct_cri + pct_cup + pct_ten + pct_ata + pct_bro + pct_cal)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if pct_ganga_ox < 0:
        st.error("⚠️ La suma de los minerales no puede superar el 100%. Revisa los valores ingresados.")
    else:
        st.success(f"**Ley Estimada de Cobre (Oxidados):** {ley_cabeza_cu_ox:.3f} % Cu")
        st.caption(f"Ganga silícea / Otros minerales no reportados: {pct_ganga_ox:.2f}% del peso de la muestra.")


# =====================================================================
# --- PÁGINA: CONMINUCIÓN - ANÁLISIS GRANULOMÉTRICO ---
# =====================================================================
elif seccion == "Análisis granulométrico":
    st.title("📊 Análisis Granulométrico")

    MALLAS_STD = {
        "6": 3350.0, "10": 2000.0, "12": 1700.0, "14": 1400.0,
        "18": 1000.0, "20": 850.0, "30": 600.0, "40": 425.0,
        "50": 300.0, "70": 212.0, "100": 150.0, "140": 106.0,
        "200": 75.0, "270": 53.0, "Fondo": 0.0
    }

    if 'df_gran' not in st.session_state:
        st.session_state.df_gran = pd.DataFrame({
            "Malla": ["6", "10", "12", "14", "18", "30", "Fondo"],
            "Peso tamiz [g]": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "Peso tamiz + mineral [g]": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        })

    st.write("### 1. Ingreso de Datos")
    st.info("Puedes agregar, borrar o modificar filas haciendo doble clic en las celdas. Presiona el botón de 'Basurero' o '+' a la derecha de la tabla.")

    df_editado = st.data_editor(
        st.session_state.df_gran, 
        num_rows="dynamic", 
        use_container_width=True,
        column_config={
            "Peso tamiz [g]": st.column_config.NumberColumn(format="%.2f"),
            "Peso tamiz + mineral [g]": st.column_config.NumberColumn(format="%.2f")
        }
    )

    df_valido = df_editado.dropna(subset=['Malla']).copy()

    if not df_valido.empty:
        try:
            df_valido['Abertura [µm]'] = df_valido['Malla'].map(MALLAS_STD)
            df_valido['Peso mineral [g]'] = df_valido['Peso tamiz + mineral [g]'] - df_valido['Peso tamiz [g]']
            df_valido['Peso mineral [g]'] = df_valido['Peso mineral [g]'].clip(lower=0)
            
            peso_total = df_valido['Peso mineral [g]'].sum()
            
            if peso_total > 0:
                df_valido['Retenido parcial [%]'] = (df_valido['Peso mineral [g]'] / peso_total) * 100
                df_valido['Retenido acumulado [%]'] = df_valido['Retenido parcial [%]'].cumsum()
                df_valido['Pasante acumulado [%]'] = 100 - df_valido['Retenido acumulado [%]']
                
                st.write("### 2. Tabla Granulométrica Calculada")
                formatos_columnas = {
                    col: st.column_config.NumberColumn(format="%.2f") 
                    for col in df_valido.columns if col != 'Malla'
                }
                st.dataframe(df_valido, use_container_width=True, column_config=formatos_columnas)

                df_calc = df_valido[df_valido['Malla'] != 'Fondo'].dropna(subset=['Abertura [µm]', 'Pasante acumulado [%]'])
                
                if not df_calc.empty:
                    df_calc = df_calc.sort_values(by='Abertura [µm]', ascending=True)
                    t80 = np.interp(80.0, df_calc['Pasante acumulado [%]'], df_calc['Abertura [µm]'])
                    
                    # Guardar datos en la sesión para las demás herramientas
                    st.session_state['t80_calculado'] = float(t80)
                    st.session_state['df_granulometria_2'] = df_calc[['Abertura [µm]', 'Pasante acumulado [%]']].copy()
                    
                    st.write("### 3. Resultados y Gráfico")
                    st.success(f"**El $T_{{80}}$ estimado es: {t80:.2f} µm**")
                    
                    fig = px.line(df_calc, x='Abertura [µm]', y='Pasante acumulado [%]', 
                                  log_x=True, markers=True, 
                                  title="Curva Granulométrica")
                    fig.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="80% Pasante")
                    fig.add_vline(x=t80, line_dash="dash", line_color="red")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("✍️ Ingresa las masas en la tabla superior para generar los cálculos y la curva granulométrica.")
        except Exception as e:
            st.error(f"Error en los cálculos. Asegúrate de ingresar mallas válidas. Detalle: {e}")

    # Exportar Datos (Power BI y Excel)
    st.write("### 4. Exportar Datos")
    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        if st.button("💾 Actualizar datos para Power BI", use_container_width=True):
            df_editado.to_csv("datos_granulometria.csv", index=False, decimal=",", sep=";")
            st.success("¡Datos guardados exitosamente como 'datos_granulometria.csv'!")

    with col_btn2:
        if 'Pasante acumulado [%]' in df_valido.columns:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_valido.to_excel(writer, index=False, sheet_name='Resultados')
                
                workbook = writer.book
                worksheet = writer.sheets['Resultados']
                
                formato_decimal = workbook.add_format({'num_format': '0.00'})
                worksheet.set_column('B:H', 18, formato_decimal) 
                worksheet.set_column('A:A', 12) 
                
                chart = workbook.add_chart({'type': 'scatter', 'subtype': 'straight_with_markers'})
                max_row = len(df_valido)
                
                chart.add_series({
                    'name':       'Curva Granulométrica',
                    'categories': ['Resultados', 1, 3, max_row-1, 3], 
                    'values':     ['Resultados', 1, 7, max_row-1, 7],
                    'marker':     {'type': 'circle', 'size': 6},
                    'line':       {'color': '#1f77b4', 'width': 1.5}
                })
                
                chart.set_title({'name': 'Curva Granulométrica'})
                chart.set_x_axis({'name': 'Abertura [µm]', 'log_base': 10, 'major_gridlines': {'visible': True}})
                chart.set_y_axis({'name': 'Pasante acumulado [%]', 'max': 100, 'min': 0, 'major_gridlines': {'visible': True}})
                
                worksheet.insert_chart('J2', chart, {'x_scale': 1.4, 'y_scale': 1.2})
                
            excel_data = output.getvalue()
            
            st.download_button(
                label="📥 Descargar Reporte en Excel",
                data=excel_data,
                file_name="Reporte_Granulometria.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        else:
            st.button("📥 Descargar Reporte en Excel", disabled=True, use_container_width=True)


# =====================================================================
# --- PÁGINA: CALCULADORA LEY DE BOND ---
# =====================================================================
elif seccion == "Calculadora Ley de Bond":
    st.title("⚡ Calculadora de Energía (Ley de Bond)")
    st.write("Calcula la energía específica y la potencia requerida del molino utilizando la **Tercera Ley de Conminución** (Work Index de Bond).")
    
    st.latex(r"W = 10 \cdot W_i \left( \frac{1}{\sqrt{P_{80}}} - \frac{1}{\sqrt{F_{80}}} \right)")
    
    t80_guardado = st.session_state.get('t80_calculado', None)
    
    if 'f80_val' not in st.session_state:
        st.session_state['f80_val'] = 2000.0
    if 'p80_val' not in st.session_state:
        st.session_state['p80_val'] = 200.0
        
    if t80_guardado:
        st.info(f"💡 Se detectó un **$T_{{80}}$ = {t80_guardado:.2f} µm** calculado en la sección de Análisis Granulométrico.", icon="🧠")
        
        col_btn_f, col_btn_p, _ = st.columns([1, 1, 2])
        if col_btn_f.button("Usar como F80 (Alimentación)"):
            st.session_state['f80_val'] = t80_guardado
            st.rerun()
        if col_btn_p.button("Usar como P80 (Producto)"):
            st.session_state['p80_val'] = t80_guardado
            st.rerun()
            
    st.markdown("---")
    
    st.markdown("### 1. Parámetros de Operación")
    c1, c2 = st.columns(2)
    wi = c1.number_input("Work Index del mineral ($W_i$) [kWh/t]", min_value=0.1, value=15.0, step=0.5, format="%.2f")
    tph = c2.number_input("Flujo másico a procesar (TPH) [t/h]", min_value=0.1, value=100.0, step=10.0, format="%.2f")
    
    st.markdown("### 2. Tamaños Característicos")
    c3, c4 = st.columns(2)
    f80 = c3.number_input("Tamaño 80% Alimentación ($F_{80}$) [µm]", min_value=0.1, value=st.session_state['f80_val'], step=50.0, key="f80_input")
    p80 = c4.number_input("Tamaño 80% Producto ($P_{80}$) [µm]", min_value=0.1, value=st.session_state['p80_val'], step=10.0, key="p80_input")
    
    st.session_state['f80_val'] = f80
    st.session_state['p80_val'] = p80

    st.markdown("### 3. Resultados de Energía y Potencia")
    if f80 <= p80:
        st.error("⚠️ Error lógico: El tamaño de alimentación ($F_{80}$) debe ser mayor al tamaño del producto ($P_{80}$).")
    else:
        w_especifica = 10 * wi * ((1 / np.sqrt(p80)) - (1 / np.sqrt(f80)))
        potencia_kw = w_especifica * tph
        potencia_hp = potencia_kw * 1.34102
        
        col_res1, col_res2, col_res3 = st.columns(3)
        
        with col_res1:
            st.markdown(
                f"""
                <div style="background-color: #1e222d; padding: 20px; border-radius: 10px; border-left: 5px solid #3b82f6; text-align: center;">
                    <p style="color: #a1aab5; margin: 0; font-size: 1rem;">Energía Específica (kWh/t)</p>
                    <h2 style="color: white; margin: 5px 0;">{w_especifica:.2f}</h2>
                    <p style="color: #4ade80; margin: 0; font-weight: bold;">kWh/t</p>
                </div>
                """, unsafe_allow_html=True)
            
        with col_res2:
            st.markdown(
                f"""
                <div style="background-color: #1e222d; padding: 20px; border-radius: 10px; border-left: 5px solid #f59e0b; text-align: center;">
                    <p style="color: #a1aab5; margin: 0; font-size: 1rem;">Potencia Motor (kW)</p>
                    <h2 style="color: white; margin: 5px 0;">{potencia_kw:.2f}</h2>
                    <p style="color: #facc15; margin: 0; font-weight: bold;">kW</p>
                </div>
                """, unsafe_allow_html=True)
            
        with col_res3:
            st.markdown(
                f"""
                <div style="background-color: #1e222d; padding: 20px; border-radius: 10px; border-left: 5px solid #ef4444; text-align: center;">
                    <p style="color: #a1aab5; margin: 0; font-size: 1rem;">Potencia Motor (HP)</p>
                    <h2 style="color: white; margin: 5px 0;">{potencia_hp:.2f}</h2>
                    <p style="color: #f87171; margin: 0; font-weight: bold;">HP</p>
                </div>
                """, unsafe_allow_html=True)


# =====================================================================
# --- PÁGINA: RAZÓN DE REDUCCIÓN ---
# =====================================================================
elif seccion == "Razón de Reducción":
    st.title("📐 Razón de Reducción ($R_r$)")
    st.write("Calcula la eficiencia de reducción de tamaño en equipos de conminución (chancadores o molinos) comparando la alimentación y el producto.")
    
    st.latex(r"R_r = \frac{F_{80}}{P_{80}}")
    
    t80_guardado = st.session_state.get('t80_calculado', None)
    
    if 'rr_f80' not in st.session_state:
        st.session_state['rr_f80'] = 150000.0  
    if 'rr_p80' not in st.session_state:
        st.session_state['rr_p80'] = 15000.0   
        
    if t80_guardado:
        st.info(f"💡 Se detectó un **$T_{{80}}$ = {t80_guardado:.2f} µm** calculado en la sección de Análisis Granulométrico.", icon="🧠")
        
        col_btn_f, col_btn_p, _ = st.columns([1, 1, 2])
        if col_btn_f.button("Usar como F80 (Alimentación RR)"):
            st.session_state['rr_f80'] = t80_guardado
            st.rerun()
        if col_btn_p.button("Usar como P80 (Producto RR)"):
            st.session_state['rr_p80'] = t80_guardado
            st.rerun()
            
    st.markdown("---")
    
    st.markdown("### 1. Tamaños Característicos de Operación")
    c1, c2 = st.columns(2)
    rr_f80 = c1.number_input("Tamaño de Alimentación ($F_{80}$) [µm o mm]", min_value=0.01, value=st.session_state['rr_f80'], step=100.0, format="%.2f", key="rr_f80_input")
    rr_p80 = c2.number_input("Tamaño de Producto ($P_{80}$) [µm o mm]", min_value=0.01, value=st.session_state['rr_p80'], step=10.0, format="%.2f", key="rr_p80_input")
    
    st.session_state['rr_f80'] = rr_f80
    st.session_state['rr_p80'] = rr_p80

    st.markdown("### 2. Resultado y Diagnóstico de Etapa")
    if rr_f80 <= rr_p80:
        st.error("⚠️ Error lógico: El tamaño de alimentación ($F_{80}$) debe ser mayor al tamaño del producto ($P_{80}$).")
    else:
        razon_red = rr_f80 / rr_p80
        
        if razon_red < 3:
            etapa = "Clasificación / Etapa muy baja"
            color_etapa = "#64748b"
        elif 3 <= razon_red <= 7:
            etapa = "Chancado Primario o Secundario Típico"
            color_etapa = "#3b82f6"
        elif 7 < razon_red <= 15:
            etapa = "Chancado Terciario / Molino SAG"
            color_etapa = "#f59e0b"
        else:
            etapa = "Molienda de Bolas / Alta Reducción"
            color_etapa = "#10b981"
            
        col_res1, col_res2 = st.columns(2)
        
        with col_res1:
            st.markdown(
                f"""
                <div style="background-color: #1e222d; padding: 25px; border-radius: 10px; border-left: 5px solid #a855f7; text-align: center;">
                    <p style="color: #a1aab5; margin: 0; font-size: 1rem;">Razón de Reducción ($R_r$)</p>
                    <h1 style="color: white; margin: 10px 0;">{razon_red:.2f}</h1>
                    <p style="color: #c084fc; margin: 0; font-weight: bold;">Sin adimensional</p>
                </div>
                """, unsafe_allow_html=True)
                
        with col_res2:
            st.markdown(
                f"""
                <div style="background-color: #1e222d; padding: 25px; border-radius: 10px; border-left: 5px solid {color_etapa}; text-align: center;">
                    <p style="color: #a1aab5; margin: 0; font-size: 1rem;">Evaluación de Equipo / Etapa</p>
                    <h3 style="color: white; margin: 15px 0;">{etapa}</h3>
                    <p style="color: #a1aab5; margin: 0; font-size: 0.85rem;">Basado en estándares de la industria minera</p>
                </div>
                """, unsafe_allow_html=True)


# =====================================================================
# --- PÁGINA: MODELOS GRANULOMÉTRICOS (GAUDIN-SCHUHMANN / ROSIN-RAMMLER) ---
# =====================================================================
elif seccion == "Modelos Granulométricos":
    st.title("📈 Modelos Matemáticos de Distribución Granulométrica")
    st.write("Ajusta los datos experimentales de tu análisis granulométrico a modelos teóricos continuos para la simulación y análisis de conminución.")
    
    # Selector de Modelo
    modelo_elegido = st.radio(
        "Selecciona el modelo matemático a evaluar:",
        ["Gaudin-Schuhmann", "Rosin-Rammler"],
        horizontal=True
    )
    
    st.markdown("---")
    
    # Verificamos si hay datos guardados de granulometría
    df_gran_sesion = st.session_state.get('df_granulometria_2', None)
    
    if df_gran_sesion is not None and not df_gran_sesion.empty:
        st.success("✅ Se han cargado automáticamente los datos reales desde tu sección de **Análisis Granulométrico**.")
        df_GS = df_gran_sesion.copy()
    else:
        st.info("ℹ️ No se detectaron datos previos. Se cargará una muestra estándar por defecto. Puedes ingresar datos reales en 'Análisis granulométrico'.", icon="💡")
        df_GS = pd.DataFrame({
            'Abertura [µm]': [2000.0, 1000.0, 850.0, 600.0, 425.0, 300.0, 212.0, 150.0, 106.0, 75.0],
            'Pasante acumulado [%]': [98.50, 89.20, 82.10, 71.40, 58.30, 47.50, 36.20, 27.80, 19.50, 12.10]
        })
        
    st.markdown("### 1. Datos Experimentales")
    
    # Aplicar formato con dos decimales usando column_config en st.dataframe
    st.dataframe(
        df_GS, 
        use_container_width=True,
        column_config={
            "Abertura [µm]": st.column_config.NumberColumn(format="%.2f"),
            "Pasante acumulado [%]": st.column_config.NumberColumn(format="%.2f")
        }
    )
    
    if modelo_elegido == "Gaudin-Schuhmann":
        st.latex(r"Y = 100 \left( \frac{x}{k} \right)^m \implies \log(Y) = m \cdot \log(x) + c")
        
        # Filtrar datos válidos (excluir 0 o 100 absolutos para evitar errores de log)
        df_fit = df_GS[(df_GS['Pasante acumulado [%]'] > 0) & (df_GS['Pasante acumulado [%]'] < 100) & (df_GS['Abertura [µm]'] > 0)].copy()
        
        if len(df_fit) >= 2:
            log_x = np.log10(df_fit['Abertura [µm]'])
            log_y = np.log10(df_fit['Pasante acumulado [%]'])
            
            m, c = np.polyfit(log_x, log_y, 1)
            log_k = (2.0 - c) / m
            k = 10**log_k
            
            y_pred_log = m * log_x + c
            ss_res = np.sum((log_y - y_pred_log)**2)
            ss_tot = np.sum((log_y - np.mean(log_y))**2)
            r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
            
            st.markdown("### 2. Parámetros Ajustados (Gaudin-Schuhmann)")
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.metric(label="Módulo de Pendiente ($m$)", value=f"{m:.3f}", help="Indica la uniformidad del tamaño.")
            with col_m2:
                st.metric(label="Tamaño Máximo ($k$ [µm])", value=f"{k:.2f} µm", help="Parámetro de tamaño máximo teórico.")
            with col_m3:
                st.metric(label="Coeficiente de Ajuste ($R^2$)", value=f"{r2:.4f}")
                
            x_min = df_GS['Abertura [µm]'].min() * 0.8
            x_max = df_GS['Abertura [µm]'].max() * 1.2
            x_teorico = np.logspace(np.log10(x_min), np.log10(x_max), 100)
            y_teorico = 100 * (x_teorico / k)**m
            y_teorico = np.clip(y_teorico, 0, 100)
            
            df_teorico = pd.DataFrame({'Abertura [µm]': x_teorico, 'Pasante Teórico [%]': y_teorico})
            
            st.markdown("### 3. Curva Experimental vs. Modelo Gaudin-Schuhmann")
            fig = px.scatter(df_GS, x='Abertura [µm]', y='Pasante acumulado [%]', log_x=True, 
                             title="Ajuste - Gaudin-Schuhmann",
                             labels={'Abertura [µm]': 'Abertura (µm) - Escala Log', 'Pasante acumulado [%]': 'Pasante Acumulado (%)'})
            fig.add_scatter(x=df_teorico['Abertura [µm]'], y=df_teorico['Pasante Teórico [%]'], 
                            mode='lines', name=f'Modelo G-S (R² = {r2:.3f})', line=dict(color='orange', width=2))
            fig.update_layout(xaxis=dict(autorange="reversed"))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ Se requieren al menos 2 puntos válidos entre 0% y 100%.")

    else:  # Rosin-Rammler
        st.latex(r"Y = 100 \left[ 1 - \exp\left( -\left(\frac{x}{x_0}\right)^n \right) \right]")
        st.write("Transformación lineal: $\\ln\\left(\\ln\\left(\\frac{100}{100 - Y}\\right)\\right) = n \\cdot \\ln(x) - n \\cdot \\ln(x_0)$")
        
        # Filtrar datos válidos (excluir pasantes de 100% exactos para evitar división por cero en log)
        df_fit = df_GS[(df_GS['Pasante acumulado [%]'] > 0) & (df_GS['Pasante acumulado [%]'] < 100) & (df_GS['Abertura [µm]'] > 0)].copy()
        
        if len(df_fit) >= 2:
            y_val = df_fit['Pasante acumulado [%]'].values
            x_val = df_fit['Abertura [µm]'].values
            
            Y_rr = np.log(np.log(100.0 / (100.0 - y_val)))
            X_rr = np.log(x_val)
            
            n, intercept = np.polyfit(X_rr, Y_rr, 1)
            ln_x0 = -intercept / n
            x0 = np.exp(ln_x0)
            
            y_pred_rr = n * X_rr + intercept
            ss_res = np.sum((Y_rr - y_pred_rr)**2)
            ss_tot = np.sum((Y_rr - np.mean(Y_rr))**2)
            r2_rr = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
            
            st.markdown("### 2. Parámetros Ajustados (Rosin-Rammler)")
            col_r1, col_r2, col_r3 = st.columns(3)
            with col_r1:
                st.metric(label="Parámetro de Uniformidad ($n$)", value=f"{n:.3f}", help="Pendiente característica de Rosin-Rammler.")
            with col_r2:
                st.metric(label="Tamaño Característico ($x_0$ [µm])", value=f"{x0:.2f} µm", help="Tamaño donde el 63.2% pasa.")
            with col_r3:
                st.metric(label="Coeficiente de Ajuste ($R^2$)", value=f"{r2_rr:.4f}")
                
            x_min = df_GS['Abertura [µm]'].min() * 0.8
            x_max = df_GS['Abertura [µm]'].max() * 1.2
            x_teorico_rr = np.logspace(np.log10(x_min), np.log10(x_max), 100)
            y_teorico_rr = 100 * (1 - np.exp(- (x_teorico_rr / x0)**n ))
            
            df_teorico_rr = pd.DataFrame({'Abertura [µm]': x_teorico_rr, 'Pasante Teórico [%]': y_teorico_rr})
            
            st.markdown("### 3. Curva Experimental vs. Modelo Rosin-Rammler")
            fig_rr = px.scatter(df_GS, x='Abertura [µm]', y='Pasante acumulado [%]', log_x=True, 
                                title="Ajuste - Rosin-Rammler",
                                labels={'Abertura [µm]': 'Abertura (µm) - Escala Log', 'Pasante acumulado [%]': 'Pasante Acumulado (%)'})
            fig_rr.add_scatter(x=df_teorico_rr['Abertura [µm]'], y=df_teorico_rr['Pasante Teórico [%]'], 
                               mode='lines', name=f'Modelo R-R (R² = {r2_rr:.3f})', line=dict(color='cyan', width=2))
            fig_rr.update_layout(xaxis=dict(autorange="reversed"))
            st.plotly_chart(fig_rr, use_container_width=True)
        else:
            st.warning("⚠️ Se requieren al menos 2 puntos válidos entre 0% y 100% para Rosin-Rammler.")


# =====================================================================
# --- PIE DE PÁGINA ---
# =====================================================================
st.markdown("---")
st.markdown("<p style='text-align: center; color: #a1aab5;'>Creado por grupo DiRoPS</p>", unsafe_allow_html=True)
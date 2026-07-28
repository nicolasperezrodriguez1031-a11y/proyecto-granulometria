import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

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
        
    if st.button("🚧 Próxima sección...", use_container_width=True):
        st.session_state.pagina_actual = "Próxima sección"

seccion = st.session_state.pagina_actual


# =====================================================================
# --- FUNCIÓN AUXILIAR PARA TARJETAS DE MINERALES ---
# =====================================================================
def mineral_card(color, name, formula, grade):
    """Genera el HTML/CSS de una tarjeta de mineral responsiva para modo oscuro"""
    return f"""
    <div style="background-color: #1e222d; padding: 30px 15px; border-radius: 16px; text-align: center; margin-bottom: 20px; box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); border-bottom: 4px solid {color}; transition: transform 0.3s ease;">
        <div style="width: 55px; height: 55px; border-radius: 50%; background-color: {color}; margin: 0 auto 18px auto; box-shadow: 0 0 15px {color}aa; border: 2px solid rgba(255,255,255,0.2);"></div>
        <div style="font-size: 1.45rem; font-weight: 800; color: #ffffff; margin-bottom: 12px; letter-spacing: 0.5px;">{name}</div>
        <div style="font-size: 1rem; color: #a1aab5; margin-bottom: 10px; font-family: monospace;">{formula}</div>
        <div style="font-size: 1.15rem; color: #4ade80; font-weight: 700; background-color: rgba(74, 222, 128, 0.1); padding: 5px 10px; border-radius: 8px; display: inline-block;">Ley Cu: {grade}</div>
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

    # Creamos 5 columnas para mantener el tamaño de las tarjetas
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

    # Tarjetas visibles en el inicio
    process_card("🔬", "CARACTERIZACIÓN", "MINERALES SULFURADOS Y OXIDADOS.", col1, "rgba(0, 191, 255, 0.3)")
    process_card("⛰️", "CONMINUCIÓN", "REDUCCIÓN DE TAMAÑO DEL MINERAL.", col2, "rgba(255, 255, 255, 0.3)")


# =====================================================================
# --- PÁGINAS: CARACTERIZACIÓN METALÚRGICA ---
# =====================================================================
elif seccion == "Minerales sulfurados":
    st.title("🟢 Minerales Sulfurados")
    st.write("Analiza las propiedades, leyes teóricas y comportamientos de las principales especies sulfuradas de cobre.")
    
    st.markdown("### 📚 Base de Propiedades")
    
    # Creamos una cuadrícula de 4 columnas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(mineral_card("#eab308", "Calcopirita", "CuFeS₂", "34.6%"), unsafe_allow_html=True)
    with col2:
        st.markdown(mineral_card("#9d4edd", "Bornita", "Cu₅FeS₄", "63.3%"), unsafe_allow_html=True)
    with col3:
        st.markdown(mineral_card("#64748b", "Calcosina", "Cu₂S", "79.8%"), unsafe_allow_html=True)
    with col4:
        st.markdown(mineral_card("#3b82f6", "Covelita", "CuS", "66.4%"), unsafe_allow_html=True)
        
    st.markdown("---")
    st.info("💡 **Próximamente:** Herramientas de cálculo de recuperación esperada e interpolación de cinéticas de flotación según la especie mineralógica.")


elif seccion == "Minerales oxidados":
    st.title("🟤 CMinerales Oxidados")
    st.write("Analiza las propiedades, leyes teóricas y comportamientos de las principales especies oxidadas de cobre (solubles en ácido).")
    
    st.markdown("### 📚 Base de Propiedades")
    
    # Creamos una cuadrícula de 4 columnas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(mineral_card("#22c55e", "Malaquita", "Cu₂CO₃(OH)₂", "57.5%"), unsafe_allow_html=True)
    with col2:
        st.markdown(mineral_card("#2563eb", "Azurita", "Cu₃(CO₃)₂(OH)₂", "55.3%"), unsafe_allow_html=True)
    with col3:
        st.markdown(mineral_card("#06b6d4", "Crisocola", "(Cu,Al)₂H₂Si₂O₅...", "~36.0%"), unsafe_allow_html=True)
    with col4:
        st.markdown(mineral_card("#ef4444", "Cuprita", "Cu₂O", "88.8%"), unsafe_allow_html=True)
        
    st.markdown("---")
    st.info("💡 **Próximamente:** Calculadora de consumo teórico de ácido sulfúrico (H₂SO₄) por tonelada según la ley de óxidos.")


# =====================================================================
# --- PÁGINA: CONMINUCIÓN - ANÁLISIS GRANULOMÉTRICO ---
# =====================================================================
elif seccion == "Análisis granulométrico":
    st.title("Análisis Granulométrico")

    MALLAS_STD = {
        "6": 3350.0, "10": 2000.0, "12": 1700.0, "14": 1400.0,
        "18": 1000.0, "20": 850.0, "30": 600.0, "40": 425.0,
        "50": 300.0, "70": 212.0, "100": 150.0, "140": 106.0,
        "200": 75.0, "270": 53.0, "Fondo": 0.0
    }

    # Inicializamos todo en 0.0
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

    # Cálculos Automáticos
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

    st.write("### 4. Exportar a Power BI")
    st.info("Guarda los datos actuales para que Power BI pueda leerlos y graficarlos.")

    if st.button("💾 Actualizar datos para Power BI"):
        df_editado.to_csv("datos_granulometria.csv", index=False, decimal=",", sep=";")
        st.success("¡Datos guardados exitosamente como 'datos_granulometria.csv'!")


# =====================================================================
# --- PÁGINA: PRÓXIMA SECCIÓN ---
# =====================================================================
elif seccion == "Próxima sección":
    st.title("Próximamente")
    st.write("Aquí podrás visualizar nuevos módulos (por ejemplo: Chancado, Molienda, etc.) en el futuro.")


# =====================================================================
# --- PIE DE PÁGINA ---
# =====================================================================
st.markdown("---")
st.markdown("<p style='text-align: center; color: #a1aab5;'>Creado por grupo DiRoPS</p>", unsafe_allow_html=True)
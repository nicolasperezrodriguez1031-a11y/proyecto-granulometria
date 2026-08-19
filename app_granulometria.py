import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import io  # <-- Para crear el archivo Excel en memoria

# Configuración de la página (layout ancho y tema oscuro)
st.set_page_config(page_title="Gestión de Procesos Metalúrgicos de Minerales Oxidados", layout="wide")

# --- CONTROL DE NAVEGACIÓN CON MENÚ DESPLEGABLE ---
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = "Inicio"

st.sidebar.title("Menú de Navegación")

# 1. Opciones principales en la barra lateral
if st.sidebar.button("🏠 Inicio", use_container_width=True):
    st.session_state.pagina_actual = "Inicio"

if st.sidebar.button("👥 Quiénes somos", use_container_width=True):
    st.session_state.pagina_actual = "Quiénes somos"

# 2. Categoría Desplegable: Caracterización Mineralógica (Solo Oxidados)
with st.sidebar.expander("🔬 Caracterización Mineralógica", expanded=True):
    if st.button("🟤 Minerales oxidados", use_container_width=True):
        st.session_state.pagina_actual = "Minerales oxidados"
        
    if st.button("🧮 Estimador Ley de Cabeza", use_container_width=True):
        st.session_state.pagina_actual = "Estimador Ley de Cabeza"

# 3. Categoría Desplegable: Conminución
with st.sidebar.expander("⚙️ Conminución", expanded=True):
    if st.button("🔨 Chancado (Primario, Secundario y Terciario)", use_container_width=True):
        st.session_state.pagina_actual = "Chancado"
        
    if st.button("📊 Análisis granulométrico", use_container_width=True):
        st.session_state.pagina_actual = "Análisis granulométrico"
        
    if st.button("⚡ Calculadora Ley de Bond", use_container_width=True):
        st.session_state.pagina_actual = "Calculadora Ley de Bond"
        
    if st.button("📐 Razón de Reducción", use_container_width=True):
        st.session_state.pagina_actual = "Razón de Reducción"

    if st.button("📈 Modelos Granulométricos (GS / RR)", use_container_width=True):
        st.session_state.pagina_actual = "Modelos Granulométricos"

# 4. Categoría Desplegable: Hidrometalurgia
with st.sidebar.expander("🧪 Hidrometalurgia", expanded=True):
    if st.button("💧 Procesos Hidrometalúrgicos", use_container_width=True):
        st.session_state.pagina_actual = "Procesos Hidrometalúrgicos"
        
    if st.button("🧮 Calculadora de Aglomeración", use_container_width=True):
        st.session_state.pagina_actual = "Calculadora de Aglomeración"

    if st.button("🧪 Preparación de Solución LX", use_container_width=True):
        st.session_state.pagina_actual = "Preparación de Solución LX"

    if st.button("🧲 Extracción por Solventes", use_container_width=True):
        st.session_state.pagina_actual = "Extracción por Solventes"

seccion = st.session_state.pagina_actual


# =====================================================================
# --- FUNCIÓN AUXILIAR PARA TARJETAS DE MINERALES ---
# =====================================================================
def mineral_card(color, name, formula, grade_text, density, mohs, acid_consumption, solubility):
    """Genera el HTML/CSS de una tarjeta de mineral responsiva con altura automática"""
    return f"""
    <div style="background-color: #1e222d; padding: 25px 15px; border-radius: 16px; margin-bottom: 20px; box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); border-bottom: 4px solid {color}; transition: transform 0.3s ease;">
        <div style="width: 45px; height: 45px; border-radius: 50%; background-color: {color}; margin: 0 auto 12px auto; box-shadow: 0 0 15px {color}aa; border: 2px solid rgba(255,255,255,0.2);"></div>
        <div style="font-size: 1.35rem; font-weight: 800; color: #ffffff; margin-bottom: 6px; text-align: center; letter-spacing: 0.5px;">{name}</div>
        <div style="font-size: 0.95rem; color: #a1aab5; margin-bottom: 12px; text-align: center; font-family: monospace;">{formula}</div>
        <div style="text-align: center; margin-bottom: 15px;">
            <span style="font-size: 1.05rem; color: #4ade80; font-weight: 700; background-color: rgba(74, 222, 128, 0.1); padding: 4px 10px; border-radius: 8px; display: inline-block;">{grade_text}</span>
        </div>
        <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.1); margin: 5px 0 12px 0;">
        <div style="font-size: 0.85rem; color: #cbd5e1; line-height: 1.5;">
            <div style="margin-bottom: 4px;"><b>Densidad:</b> {density}</div>
            <div style="margin-bottom: 4px;"><b>Dureza (Mohs):</b> {mohs}</div>
            <div style="margin-bottom: 4px;"><b>Consumo Ácido:</b> {acid_consumption}</div>
            <div><b>Solubilidad:</b> {solubility}</div>
        </div>
    </div>
    """


# =====================================================================
# --- PÁGINA: INICIO ---
# =====================================================================
if seccion == "Inicio":
    st.title("Bienvenido a tu plataforma de Minerales Oxidados")
    st.write("Una herramienta diseñada para la caracterización, análisis y optimización de procesos metalúrgicos de minerales oxidados. Diseñada para potenciar el desarrollo, cálculo y control de tus proyectos.")
    
    st.info("Utiliza el menú de navegación para acceder al nuevo módulo interactivo de cálculo de aglomeración y demás herramientas de análisis.", icon="👈")
    st.markdown("---") 

    st.markdown("### 💡 ¿Qué son los minerales oxidados?")
    st.write("Los minerales oxidados son todos aquellos que contienen el oxígeno (O) como elemento principal de su composición.")
    st.markdown("---")

    # --- DIAGRAMA INTERACTIVO DE PROCESOS (NATIVO STREAMLIT) ---
    st.markdown("### ⚙️ Diagrama del Proceso Metalúrgico de Minerales Oxidados")
    
    pasos_proceso = [
        ("1. EXTRACCIÓN MINERA", "Extracción del mineral desde la mina a cielo abierto o subterránea para su posterior procesamiento metalúrgico."),
        ("2. CONMINUCIÓN (CHANCADO)", "Reducción progresiva del tamaño de roca mediante chancado y molienda para liberar las especies valiosas."),
        ("3. AGLOMERACIÓN", "Mezcla del mineral fino con agua y ácido sulfúrico para formar glóbulos homogéneos y evitar la segregación en pilas."),
        ("4. LIXIVIACIÓN", "Disolución selectiva de los metales valiosos contenidos en el mineral mediante una solución acuosa ácida."),
        ("5. EXTRACCIÓN POR SOLVENTES", "Purificación y concentración de la solución rica obtenida en lixiviación mediante un reactivo orgánico."),
        ("6. ELECTRO - OBTENCIÓN", "Proceso electroquímico donde se aplica corriente eléctrica para depositar el metal disuelto en cátodos de alta pureza."),
        ("7. CÁTODO", "Producto final de cobre u otro metal altamente refinado listo para su comercialización y exportación internacional.")
    ]

    for titulo, descripcion in pasos_proceso:
        col_box, col_arrow, col_desc = st.columns([2.5, 0.4, 4.5])
        with col_box:
            st.markdown(
                f"""
                <div style="background-color: #1e222d; border: 2px solid #ffffff; color: #ffffff; padding: 15px; border-radius: 12px; text-align: center; font-weight: bold; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">
                    {titulo}
                </div>
                """, unsafe_allow_html=True
            )
        with col_arrow:
            st.markdown("<h3 style='text-align: center; color: white; margin-top: 10px;'>➔</h3>", unsafe_allow_html=True)
        with col_desc:
            st.markdown(
                f"""
                <div style="background-color: #1e222d; border: 2px solid #ffffff; color: #ffffff; padding: 15px; border-radius: 12px; font-size: 0.9rem; line-height: 1.4; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">
                    {descripcion}
                </div>
                """, unsafe_allow_html=True
            )
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

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

    process_card("🔬", "CARACTERIZACIÓN", "MINERALES OXIDADOS.", col1, "rgba(0, 191, 255, 0.3)")
    process_card("⛰️", "CONMINUCIÓN", "REDUCCIÓN DE TAMAÑO DEL MINERAL.", col2, "rgba(255, 255, 255, 0.3)")
    process_card("🧪", "HIDROMETALURGIA", "AGLOMERACIÓN, LIXIVIACIÓN, SX Y EW.", col3, "rgba(74, 222, 128, 0.3)")


# =====================================================================
# --- PÁGINA: QUIÉNES SOMOS ---
# =====================================================================
elif seccion == "Quiénes somos":
    st.title("👥 Quiénes Somos")
    st.write("Conoce al equipo detrás del desarrollo de esta plataforma enfocada en la optimización y cálculo de procesos metalúrgicos para minerales oxidados.")
    
    st.markdown("---")
    st.markdown("### 🎓 Autores del Proyecto de Tesis")
    st.write("Esta plataforma digital forma parte de nuestra idea y desarrollo de tesis orientada a la ingeniería de procesos y metalurgia extractiva.")
    
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.markdown(
            """
            <div style="background-color: #1e222d; padding: 30px; border-radius: 16px; text-align: center; box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); border-bottom: 4px solid #3b82f6;">
                <div style="width: 90px; height: 90px; border-radius: 50%; background-color: #3b82f6; margin: 0 auto 18px auto; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; color: white; box-shadow: 0 0 15px rgba(59, 130, 246, 0.5);">👨‍🎓</div>
                <div style="font-size: 1.5rem; font-weight: 800; color: #ffffff; margin-bottom: 8px;">Héctor Díaz</div>
                <div style="font-size: 1rem; color: #38bdf8; font-weight: 600;">Estudiante Tesista</div>
            </div>
            """, unsafe_allow_html=True
        )
        
    with col_t2:
        st.markdown(
            """
            <div style="background-color: #1e222d; padding: 30px; border-radius: 16px; text-align: center; box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); border-bottom: 4px solid #10b981;">
                <div style="width: 90px; height: 90px; border-radius: 50%; background-color: #10b981; margin: 0 auto 18px auto; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; color: white; box-shadow: 0 0 15px rgba(16, 185, 129, 0.5);">👨‍🎓</div>
                <div style="font-size: 1.5rem; font-weight: 800; color: #ffffff; margin-bottom: 8px;">Nicolás Pérez</div>
                <div style="font-size: 1rem; color: #34d399; font-weight: 600;">Estudiante Tesista</div>
            </div>
            """, unsafe_allow_html=True
        )


# =====================================================================
# --- PÁGINAS: CARACTERIZACIÓN METALÚRGICA ---
# =====================================================================
elif seccion == "Minerales oxidados":
    st.title("🟤 Minerales Oxidados")
    st.write("Analiza las propiedades físicas, químicas, leyes teóricas y comportamientos metalúrgicos de las principales especies oxidadas y óxidos metálicos.")
    
    st.markdown("### 📚 Base de Propiedades")
    
    st.markdown("#### 🟢 Minerales de Cobre")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(mineral_card("#22c55e", "Malaquita", "Cu₂CO₃(OH)₂", "Ley Cu: 57.5%", "3.75 - 4.0 g/cm³", "3.5 - 4.0", "Alto (consume ácido por carbonatos)", "Soluble en ácidos diluidos con efervescencia"), unsafe_allow_html=True)
        with st.expander("📊 Ver % de elementos (Malaquita)"):
            st.write("- **Cobre (Cu):** 57.5%")
            st.write("- **Oxígeno (O):** 28.9%")
            st.write("- **Carbono (C):** 5.4%")
            st.write("- **Hidrógeno (H):** 8.2%")
    with col2:
        st.markdown(mineral_card("#2563eb", "Azurita", "Cu₃(CO₃)₂(OH)₂", "Ley Cu: 55.3%", "3.77 - 3.83 g/cm³", "3.5 - 4.0", "Alto (consume ácido por carbonatos)", "Soluble en ácidos diluidos con efervescencia"), unsafe_allow_html=True)
        with st.expander("📊 Ver % de elementos (Azurita)"):
            st.write("- **Cobre (Cu):** 55.3%")
            st.write("- **Oxígeno (O):** 34.6%")
            st.write("- **Carbono (C):** 6.9%")
            st.write("- **Hidrógeno (H):** 3.2%")
    with col3:
        st.markdown(mineral_card("#06b6d4", "Crisocola", "(Cu,Al)₂H₂Si₂O₅...", "Ley Cu: 36.0%", "2.0 - 2.4 g/cm³", "2.0 - 4.0", "Moderado a Bajo", "Soluble en ácidos diluidos (gelatinoso)"), unsafe_allow_html=True)
        with st.expander("📊 Ver % de elementos (Crisocola)"):
            st.write("- **Cobre (Cu):** ~36.0%")
            st.write("- **Silicio (Si):** ~15.2%")
            st.write("- **Aluminio (Al):** Variable")
            st.write("- **Oxígeno / Hidrógeno / Agua:** Restante")
    with col4:
        st.markdown(mineral_card("#ef4444", "Cuprita", "Cu₂O", "Ley Cu: 88.8%", "6.10 g/cm³", "3.5 - 4.0", "Bajo", "Soluble en ácidos diluidos (requiere oxidantes/reductores según condición)"), unsafe_allow_html=True)
        with st.expander("📊 Ver % de elementos (Cuprita)"):
            st.write("- **Cobre (Cu):** 88.8%")
            st.write("- **Oxígeno (O):** 11.2%")
        
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.markdown(mineral_card("#111827", "Tenorita", "CuO", "Ley Cu: 79.9%", "6.30 - 6.45 g/cm³", "3.0 - 4.0", "Bajo", "Soluble en ácidos diluidos"), unsafe_allow_html=True)
        with st.expander("📊 Ver % de elementos (Tenorita)"):
            st.write("- **Cobre (Cu):** 79.9%")
            st.write("- **Oxígeno (O):** 20.1%")
    with col6:
        st.markdown(mineral_card("#15803d", "Atacamita", "Cu₂Cl(OH)₃", "Ley Cu: 59.5%", "3.75 - 3.77 g/cm³", "3.0 - 3.5", "Bajo", "Soluble en ácidos diluidos y parcialmente en agua"), unsafe_allow_html=True)
        with st.expander("📊 Ver % de elementos (Atacamita)"):
            st.write("- **Cobre (Cu):** 59.5%")
            st.write("- **Cloro (Cl):** 16.6%")
            st.write("- **Oxígeno (O):** 22.4%")
            st.write("- **Hidrógeno (H):** 1.5%")
    with col7:
        st.markdown(mineral_card("#047857", "Brochantita", "Cu₄SO₄(OH)₆", "Ley Cu: 56.2%", "3.90 g/cm³", "3.5 - 4.0", "Bajo", "Soluble en ácidos diluidos"), unsafe_allow_html=True)
        with st.expander("📊 Ver % de elementos (Brochantita)"):
            st.write("- **Cobre (Cu):** 56.2%")
            st.write("- **Azufre (S):** 7.1%")
            st.write("- **Oxígeno (O):** 33.8%")
            st.write("- **Hidrógeno (H):** 2.7%")
    with col8:
        st.markdown(mineral_card("#0ea5e9", "Calcantita", "CuSO₄·5H₂O", "Ley Cu: 25.5%", "2.28 g/cm³", "2.5", "Nulo / Aporte de acidez", "Alta solubilidad en agua"), unsafe_allow_html=True)
        with st.expander("📊 Ver % de elementos (Calcantita)"):
            st.write("- **Cobre (Cu):** 25.5%")
            st.write("- **Azufre (S):** 12.8%")
            st.write("- **Oxígeno (O):** 57.6%")
            st.write("- **Hidrógeno (H):** 4.1%")

    st.markdown("---")
    st.markdown("#### 🟡 Otros Óxidos / Minerales Metálicos")
    col9, col10, col11, col12 = st.columns(4)
    with col9:
        st.markdown(mineral_card("#eab308", "Óxido áurico", "Au₂O₃", "Ley Au: 78.8%", "11.0 g/cm³ (est.)", "Refractario", "Muy bajo / Nulo", "Insoluble en ácidos comunes; requiere cianuración o condiciones especiales"), unsafe_allow_html=True)
        with st.expander("📊 Ver % de elementos (Óxido áurico)"):
            st.write("- **Oro (Au):** 78.8%")
            st.write("- **Oxígeno (O):** 21.2%")
    with col10:
        st.markdown(mineral_card("#64748b", "Cincita", "ZnO", "Ley Zn: 80.3%", "5.43 - 5.70 g/cm³", "4.0", "Moderado", "Soluble en ácidos diluidos"), unsafe_allow_html=True)
        with st.expander("📊 Ver % de elementos (Cincita)"):
            st.write("- **Zinc (Zn):** 80.3%")
            st.write("- **Oxígeno (O):** 19.7%")
    with col11:
        st.markdown(mineral_card("#9a3412", "Hematita", "Fe₂O₃", "Ley Fe: 69.9%", "5.26 g/cm³", "5.5 - 6.5", "Bajo a Moderado", "Insoluble en agua; solubilidad lenta en ácidos fuertes calientes"), unsafe_allow_html=True)
        with st.expander("📊 Ver % de elementos (Hematita)"):
            st.write("- **Hierro (Fe):** 69.9%")
            st.write("- **Oxígeno (O):** 30.1%")
    with col12:
        st.markdown(mineral_card("#334155", "Magnetita", "Fe₃O₄", "Ley Fe: 72.4%", "5.15 - 5.18 g/cm³", "5.5 - 6.5", "Bajo", "Insoluble en agua; magnético, requiere ácidos fuertes o alta temperatura"), unsafe_allow_html=True)
        with st.expander("📊 Ver % de elementos (Magnetita)"):
            st.write("- **Hierro (Fe):** 72.4%")
            st.write("- **Oxígeno (O):** 27.6%")


elif seccion == "Estimador Ley de Cabeza":
    st.title("🧮 Estimador de Ley de Cabeza")
    st.write("Ingresa el porcentaje en peso (%) que representa cada especie mineralógica dentro de la roca total para estimar las leyes de cabeza correspondientes.")
    
    st.markdown("#### 🟢 Minerales de Cobre")
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

    st.markdown("#### 🟡 Otros Óxidos / Minerales Metálicos")
    c9, c10, c11, c12 = st.columns(4)
    pct_aur = c9.number_input("% Óxido áurico", min_value=0.0, max_value=100.0, value=0.0, format="%.2f", step=0.10)
    pct_cin = c10.number_input("% Cincita", min_value=0.0, max_value=100.0, value=0.0, format="%.2f", step=0.10)
    pct_hem = c11.number_input("% Hematita", min_value=0.0, max_value=100.0, value=0.0, format="%.2f", step=0.10)
    pct_mag = c12.number_input("% Magnetita", min_value=0.0, max_value=100.0, value=0.0, format="%.2f", step=0.10)
    
    ley_mal, ley_azu, ley_cri, ley_cup = 57.5, 55.3, 36.0, 88.8
    ley_ten, ley_ata, ley_bro, ley_cal = 79.9, 59.5, 56.2, 25.5
    ley_aur, ley_cin, ley_hem, ley_mag = 78.8, 80.3, 69.9, 72.4
    
    ley_cabeza_cu_ox = (pct_mal*ley_mal + pct_azu*ley_azu + pct_cri*ley_cri + pct_cup*ley_cup + pct_ten*ley_ten + pct_ata*ley_ata + pct_bro*ley_bro + pct_cal*ley_cal) / 100
    ley_cabeza_au = (pct_aur * ley_aur) / 100
    ley_cabeza_zn = (pct_cin * ley_cin) / 100
    ley_cabeza_fe = (pct_hem * ley_hem + pct_mag * ley_mag) / 100
    
    suma_total_minerales = (pct_mal + pct_azu + pct_cri + pct_cup + pct_ten + pct_ata + pct_bro + pct_cal + pct_aur + pct_cin + pct_hem + pct_mag)
    pct_ganga_ox = 100.0 - suma_total_minerales
    
    st.markdown("<br>", unsafe_allow_html=True)
    if pct_ganga_ox < 0:
        st.error("⚠️ La suma de los minerales no puede superar el 100%. Revisa los valores ingresados.")
    else:
        st.success(f"**Ley Estimada de Cobre (Cu):** {ley_cabeza_cu_ox:.3f} %")
        if pct_aur > 0:
            st.info(f"**Ley Estimada de Oro (Au):** {ley_cabeza_au:.3f} %")
        if pct_cin > 0:
            st.info(f"**Ley Estimada de Zinc (Zn):** {ley_cabeza_zn:.3f} %")
        if (pct_hem > 0) or (pct_mag > 0):
            st.info(f"**Ley Estimada de Hierro (Fe):** {ley_cabeza_fe:.3f} %")
            
        st.caption(f"Ganga silícea / Otros minerales no reportados: {pct_ganga_ox:.2f}% del peso de la muestra.")


# =====================================================================
# --- PÁGINA: CONMINUCIÓN - CHANCADO ---
# =====================================================================
elif seccion == "Chancado":
    st.title("🔨 Etapas de Chancado")
    st.write("Módulo dedicado a las operaciones de reducción de tamaño por fractura mecánica (chancado primario, secundario y terciario) en la conminución de minerales oxidados.")
    
    st.markdown("---")
    
    col_ch1, col_ch2, col_ch3 = st.columns(3)
    
    with col_ch1:
        st.markdown(
            """
            <div style="background-color: #1e222d; padding: 20px; border-radius: 12px; border-left: 5px solid #3b82f6; height: 100%;">
                <h3 style="color: #ffffff; margin-top: 0;">1. Chancado Primario</h3>
                <p style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.5;">
                    <b>Equipos principales:</b> Chancadores de mandíbulas o giratorios.<br>
                    <b>Alimentación:</b> Roca corrida de mina (ROM) de gran tamaño (hasta 1,000 - 1,500 mm).<br>
                    <b>Producto:</b> Reduce el material a tamaños de 100 a 150 mm, preparándolo para las etapas intermedias de reducción.
                </p>
            </div>
            """, unsafe_allow_html=True
        )
        
    with col_ch2:
        st.markdown(
            """
            <div style="background-color: #1e222d; padding: 20px; border-radius: 12px; border-left: 5px solid #f59e0b; height: 100%;">
                <h3 style="color: #ffffff; margin-top: 0;">2. Chancado Secundario</h3>
                <p style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.5;">
                    <b>Equipos principales:</b> Chancadores de cono (standard) o de quijada secundarios.<br>
                    <b>Alimentación:</b> Producto del chancado primario (100 - 150 mm).<br>
                    <b>Producto:</b> Reduce el tamaño de roca típicamente entre 25 a 50 mm, operando usualmente en circuitos abiertos o cerrados con harneros.
                </p>
            </div>
            """, unsafe_allow_html=True
        )
        
    with col_ch3:
        st.markdown(
            """
            <div style="background-color: #1e222d; padding: 20px; border-radius: 12px; border-left: 5px solid #10b981; height: 100%;">
                <h3 style="color: #ffffff; margin-top: 0;">3. Chancado Terciario</h3>
                <p style="color: #cbd5e1; font-size: 0.9rem; line-height: 1.5;">
                    <b>Equipos principales:</b> Chancadores de cono de cabeza corta (short head).<br>
                    <b>Alimentación:</b> Producto del chancado secundario.<br>
                    <b>Producto:</b> Reduce el material a granulometrías finas (generalmente entre 8 a 12 mm), tamaño óptimo para alimentar los procesos de aglomeración y lixiviación en pilas.
                </p>
            </div>
            """, unsafe_allow_html=True
        )


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
    
    modelo_elegido = st.radio(
        "Selecciona el modelo matemático a evaluar:",
        ["Gaudin-Schuhmann", "Rosin-Rammler"],
        horizontal=True
    )
    
    st.markdown("---")
    
    df_gran_sesion = st.session_state.get('df_granulometria_2', None)
    
    if df_gran_sesion is not None and not df_gran_sesion.empty:
        st.success("✅ Se han cargado automáticamente los datos reales desde tu sección de **Análisis Granulométrico**.")
        df_GS = df_granulometria_2.copy() if 'df_granulometria_2' in locals() else df_gran_sesion.copy()
    else:
        st.info("ℹ️ No se detectaron datos previos. Se cargará una muestra estándar por defecto. Puedes ingresar datos reales en 'Análisis granulométrico'.", icon="💡")
        df_GS = pd.DataFrame({
            'Abertura [µm]': [2000.0, 1000.0, 850.0, 600.0, 425.0, 300.0, 212.0, 150.0, 106.0, 75.0],
            'Pasante acumulado [%]': [98.50, 89.20, 82.10, 71.40, 58.30, 47.50, 36.20, 27.80, 19.50, 12.10]
        })
        
    st.markdown("### 1. Datos Experimentales")
    
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
# --- PÁGINA: HIDROMETALURGIA ---
# =====================================================================
elif seccion == "Procesos Hidrometalúrgicos":
    st.title("🧪 Procesos Hidrometalúrgicos")
    st.write("Módulo dedicado a los fundamentos y operaciones clave en la recuperación de metales a partir de minerales oxidados mediante soluciones acuosas.")
    
    st.markdown("---")
    st.markdown("### 💧 Fases Principales del Proceso Hidrometalúrgico")
    
    col_h1, col_h2 = st.columns(2)
    with col_h1:
        st.markdown(
            """
            <div style="background-color: #1e222d; padding: 20px; border-radius: 12px; border-left: 5px solid #a855f7; height: 100%;">
                <h3 style="color: #ffffff; margin-top: 0;">1. Aglomeración</h3>
                <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.5;">
                    Mezcla del mineral fino con agua y ácido sulfúrico concentrado para formar glóbulos o aglomerados homogéneos. 
                    Su objetivo principal es evitar la segregación de partículas finas y asegurar una adecuada permeabilidad (porosidad) del lecho en la pila de lixiviación.
                </p>
            </div>
            """, unsafe_allow_html=True
        )
    with col_h2:
        st.markdown(
            """
            <div style="background-color: #1e222d; padding: 20px; border-radius: 12px; border-left: 5px solid #22c55e; height: 100%;">
                <h3 style="color: #ffffff; margin-top: 0;">2. Lixiviación (En Pilas / Bateas)</h3>
                <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.5;">
                    Consiste en la disolución selectiva de los minerales oxidados de cobre u otros metales utilizando una solución acuosa de ácido sulfúrico ($H_2SO_4$). 
                    El mineral aglomerado se apila sobre patios impermeabilizados para permitir la percolación, generando una Solución Rica en Cobre (PLS).
                </p>
            </div>
            """, unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)
    
    col_h3, col_h4 = st.columns(2)
    with col_h3:
        st.markdown(
            """
            <div style="background-color: #1e222d; padding: 20px; border-radius: 12px; border-left: 5px solid #3b82f6; height: 100%;">
                <h3 style="color: #ffffff; margin-top: 0;">3. Extracción por Solventes (SX)</h3>
                <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.5;">
                    Etapa de purificación y concentración. La Solución Rica (PLS) se pone en contacto con un reactivo orgánico disuelto en kerosene. 
                    El orgánico extrae selectivamente los iones de cobre, separándolos de las impurezas (hierro, aluminio, sílice) presentes en el PLS.
                </p>
            </div>
            """, unsafe_allow_html=True
        )
    with col_h4:
        st.markdown(
            """
            <div style="background-color: #1e222d; padding: 20px; border-radius: 12px; border-left: 5px solid #f59e0b; height: 100%;">
                <h3 style="color: #ffffff; margin-top: 0;">4. Electro-Obtención (EW)</h3>
                <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.5;">
                    Proceso electroquímico en celdas donde se aplica corriente continua. Los iones de cobre purificados se reducen y 
                    depositan en forma sólida sobre cátodos permanentes de acero inoxidable, logrando cátodos de alta pureza (99.99% Cu).
                </p>
            </div>
            """, unsafe_allow_html=True
        )


# =====================================================================
# --- PÁGINA: CALCULADORA DE AGLOMERACIÓN ---
# =====================================================================
elif seccion == "Calculadora de Aglomeración":
    st.title("🧮 Simulador y Diagrama de Balance de Masas: Aglomeración")
    st.write("Modifica los flujos de entrada. El diagrama interactivo calculará instantáneamente todas las corrientes y el porcentaje real de humedad de salida.")
    
    st.markdown("---")
    
    # -------------------------------------------------------------
    # ENTRADAS
    # -------------------------------------------------------------
    st.markdown("### 📥 Parámetros de Operación de Entrada")
    
    col_in1, col_in2, col_in3, col_in4 = st.columns(4)
    
    with col_in1:
        tipo_mineral_input = st.radio("Base de Mineral Ingresado:", ["Mineral Húmedo (ton/h)", "Mineral Seco (ton/h)"])
        val_mineral = st.number_input("Valor de Mineral Ingresado", min_value=0.0, value=736.5, step=50.0)
        
    with col_in2:
        humedad_mineral = st.number_input("% Humedad inicial del mineral", min_value=0.0, max_value=99.9, value=2.0, step=0.1)
        
    with col_in3:
        tipo_agua_adic = st.radio("Unidad Agua Adicional:", ["kg/h", "ton/h", "ton/min"])
        val_agua_adic = st.number_input("Valor de Agua Adicional", min_value=0.0, value=0.5, step=0.1)
        
    with col_in4:
        tipo_acido = st.radio("Unidad de Ácido H₂SO₄:", ["kg/h", "ton/h", "kg/ton de seco"])
        val_acido = st.number_input("Valor de Ácido H₂SO₄", min_value=0.0, value=33500.0, step=500.0)

    # -------------------------------------------------------------
    # CÁLCULOS DE BALANCE
    # -------------------------------------------------------------
    if tipo_agua_adic == "kg/h":
        agua_adicional_tph = val_agua_adic / 1000.0
    elif tipo_agua_adic == "ton/min":
        agua_adicional_tph = val_agua_adic * 60.0
    else:
        agua_adicional_tph = val_agua_adic

    h = humedad_mineral / 100.0
    if "Húmedo" in tipo_mineral_input:
        mineral_humedo_tph = val_mineral
        agua_mineral_tph = mineral_humedo_tph * h
        mineral_seco_tph = mineral_humedo_tph - agua_mineral_tph
    else:
        mineral_seco_tph = val_mineral
        if h > 0 and h < 1.0:
            agua_mineral_tph = mineral_seco_tph * (h / (1.0 - h))
            mineral_humedo_tph = mineral_seco_tph + agua_mineral_tph
        else:
            agua_mineral_tph = 0.0
            mineral_humedo_tph = mineral_seco_tph

    if tipo_acido == "kg/h":
        acido_tph = val_acido / 1000.0
    elif tipo_acido == "kg/ton de seco":
        acido_tph = (val_acido * mineral_seco_tph) / 1000.0
    else:
        acido_tph = val_acido

    agua_total_salida_tph = agua_mineral_tph + agua_adicional_tph
    mineral_aglomerado_tph = mineral_humedo_tph + agua_adicional_tph + acido_tph
    
    # % Humedad de salida contando todos los líquidos de entrada (agua mineral + agua adicional + ácido)
    liquidos_totales_tph = agua_mineral_tph + agua_adicional_tph + acido_tph
    humedad_salida_pct = (liquidos_totales_tph / mineral_aglomerado_tph) * 100.0 if mineral_aglomerado_tph > 0 else 0.0

    # -------------------------------------------------------------
    # REPRESENTACIÓN VISUAL PERFECTA
    # -------------------------------------------------------------
    st.markdown("---")
    st.markdown("### 🔄 Diagrama del Proceso de Aglomeración (Tiempo Real)")
    
    col_d1, col_d2, col_d3 = st.columns([3.5, 3.2, 3.5])

    with col_d1:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="background-color: #1e222d; border: 2px solid #64748b; padding: 15px; border-radius: 12px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">
                <div style="font-size: 0.95rem; color: #cbd5e1; font-weight: bold;">Masa de Mineral Húmedo</div>
                <div style="font-size: 1.3rem; font-weight: bold; color: white; margin-top: 6px;">{mineral_humedo_tph:.2f} ton/h</div>
            </div>
            """, unsafe_allow_html=True
        )
        
        col_sub1, col_plus, col_sub2 = st.columns([4, 1, 4])
        with col_sub1:
            st.markdown("<div style='text-align: center; color: white; font-weight: bold; font-size: 1.2rem;'>↑</div>", unsafe_allow_html=True)
            st.markdown(
                f"""
                <div style="background-color: #1e222d; border: 2px solid #64748b; padding: 10px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 0.8rem; color: #cbd5e1;">mineral seco</div>
                    <div style="font-size: 1rem; font-weight: bold; color: white;">{mineral_seco_tph:.2f} t/h</div>
                </div>
                """, unsafe_allow_html=True
            )
        with col_plus:
            st.markdown("<div style='text-align: center; color: white; font-weight: bold; font-size: 1.5rem; margin-top: 35px;'>+</div>", unsafe_allow_html=True)
        with col_sub2:
            st.markdown("<div style='text-align: center; color: white; font-weight: bold; font-size: 1.2rem;'>↑</div>", unsafe_allow_html=True)
            st.markdown(
                f"""
                <div style="background-color: #1e222d; border: 2px solid #64748b; padding: 10px; border-radius: 8px; text-align: center;">
                    <div style="font-size: 0.8rem; color: #cbd5e1;">agua del mineral</div>
                    <div style="font-size: 1rem; font-weight: bold; color: white;">{agua_mineral_tph:.2f} t/h</div>
                </div>
                """, unsafe_allow_html=True
            )

    with col_d2:
        col_sup1, col_sup2 = st.columns(2)
        with col_sup1:
            st.markdown(
                f"""
                <div style="background-color: #1e222d; border: 2px solid #64748b; padding: 8px; border-radius: 8px; text-align: center; font-size: 0.75rem;">
                    <span style="color: #cbd5e1; font-weight: bold;">Masa de agua adicional</span><br>
                    <b style="color: white;">{agua_adicional_tph:.2f} t/h</b>
                </div>
                <div style="text-align: center; color: white; font-weight: bold; line-height: 1;">↓</div>
                """, unsafe_allow_html=True
            )
        with col_sup2:
            st.markdown(
                f"""
                <div style="background-color: #1e222d; border: 2px solid #64748b; padding: 8px; border-radius: 8px; text-align: center; font-size: 0.75rem;">
                    <span style="color: #cbd5e1; font-weight: bold;">Masa de H2SO4</span><br>
                    <b style="color: white;">{acido_tph:.2f} t/h</b>
                </div>
                <div style="text-align: center; color: white; font-weight: bold; line-height: 1;">↓</div>
                """, unsafe_allow_html=True
            )
            
        col_t_left, col_drum, col_t_right = st.columns([1, 4, 1])
        with col_t_left:
            st.markdown("<br><div style='color: white; font-size: 1.8rem; font-weight: bold;'>➔</div>", unsafe_allow_html=True)
        with col_drum:
            st.markdown(
                """
                <div style="background-color: #2563eb; color: white; padding: 35px 10px; border-radius: 20px; text-align: center; box-shadow: 0 0 25px rgba(37, 99, 235, 0.6); border: 2px solid #93c5fd; margin-top: 5px;">
                    <div style="font-size: 1.3rem; font-weight: 900; font-style: italic;">Aglomerador</div>
                </div>
                """, unsafe_allow_html=True
            )
        with col_t_right:
            st.markdown("<br><div style='color: white; font-size: 1.8rem; font-weight: bold;'>➔</div>", unsafe_allow_html=True)

    with col_d3:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="background-color: #1e222d; border: 2px solid #64748b; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">
                <div style="font-size: 0.95rem; color: #cbd5e1; font-weight: bold;">Masa de mineral aglomerado</div>
                <div style="font-size: 1.3rem; font-weight: bold; color: white; margin-top: 6px;">{mineral_aglomerado_tph:.2f} ton/h</div>
                <div style="font-size: 0.8rem; color: #38bdf8; margin-top: 6px;">(% Humedad Salida: {humedad_salida_pct:.2f}%)</div>
            </div>
            """, unsafe_allow_html=True
        )

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 📋 Resumen de Masas del Proceso")
    
    res_c1, res_c2, res_c3, res_c4 = st.columns(4)
    res_c1.metric("Mineral Seco", f"{mineral_seco_tph:.2f} ton/h")
    res_c2.metric("Agua del Mineral", f"{agua_mineral_tph:.2f} ton/h")
    res_c3.metric("Mineral Húmedo Total", f"{mineral_humedo_tph:.2f} ton/h")
    res_c4.metric("Mineral Aglomerado Salida", f"{mineral_aglomerado_tph:.2f} ton/h")


# =====================================================================
# --- PÁGINA: PREPARACIÓN DE SOLUCIÓN PARA LIXIVIACIÓN (LX) POR pH ---
# =====================================================================
elif seccion == "Preparación de Solución LX":
    st.title("🧪 Preparación y Dosificación de Solución para Lixiviación (LX) por pH")
    st.write("Calcula los caudales de ácido sulfúrico ($H_2SO_4$) y agua requeridos para alcanzar un **pH objetivo** en la solución de riego de lixiviación.")
    
    st.latex(r"[\text{H}^+] = 10^{-\text{pH}} \quad (\text{mol/L}) \implies C_{\text{ácido}} = [\text{H}^+] \cdot \text{PM}_{H_2SO_4} / 2 \quad (\text{g/L})")
    
    st.markdown("---")
    st.markdown("### 📥 Parámetros de Diseño y Operación")
    
    c_p1, c_p2 = st.columns(2)
    with c_p1:
        q_solucion_objetivo = st.number_input("Caudal de Solución Deseado ($Q$) [m³/h]", min_value=0.1, value=1000.0, step=10.0, format="%.2f")
        ph_objetivo = st.number_input("pH Objetivo de la Solución", min_value=0.0, max_value=7.0, value=0.50, step=0.1, format="%.2f")
    with c_p2:
        pureza_acido_pct = st.number_input("Pureza Comercial del Ácido H₂SO₄ [%]", min_value=50.0, max_value=100.0, value=98.0, step=0.5, format="%.2f")
        densidad_acido = st.number_input("Densidad del Ácido Comercial [t/m³ o g/cm³]", min_value=1.0, max_value=2.5, value=1.84, step=0.01, format="%.2f")

    # Cálculos basados en pH
    h_conc_mol_l = 10.0 ** (-ph_objetivo)
    g_pl_acido_puro = (h_conc_mol_l * 98.079) / 2.0 
    
    acido_puro_kg_h = g_pl_acido_puro * q_solucion_objetivo
    pureza_fraccion = pureza_acido_pct / 100.0
    acido_comercial_t_h = (acido_puro_kg_h / pureza_fraccion) / 1000.0
    volumen_acido_m3_h = acido_comercial_t_h / densidad_acido
    caudal_agua_m3_h = q_solucion_objetivo - volumen_acido_m3_h

    st.markdown("---")
    st.markdown("### 📊 Resultados de Dosificación por pH")
    
    r_c1, r_c2 = st.columns(2)
            
    with r_c1:
        st.markdown(
            f"""
            <div style="background-color: #1e222d; padding: 20px; border-radius: 10px; border-left: 5px solid #f59e0b; text-align: center;">
                <p style="color: #a1aab5; margin: 0; font-size: 0.95rem;">Volumen de Ácido (m³/h)</p>
                <h2 style="color: white; margin: 5px 0;">{volumen_acido_m3_h:.2f}</h2>
                <p style="color: #facc15; margin: 0; font-weight: bold;">m³ / hora</p>
            </div>
            """, unsafe_allow_html=True)
            
    with r_c2:
        st.markdown(
            f"""
            <div style="background-color: #1e222d; padding: 20px; border-radius: 10px; border-left: 5px solid #10b981; text-align: center;">
                <p style="color: #a1aab5; margin: 0; font-size: 0.95rem;">Caudal de Agua (m³/h)</p>
                <h2 style="color: white; margin: 5px 0;">{caudal_agua_m3_h:.2f}</h2>
                <p style="color: #34d399; margin: 0; font-weight: bold;">m³ / hora</p>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("<br>", unsafe_allow_html=True)
    st.info(f"💡 Para preparar un caudal de **{q_solucion_objetivo:.2f} m³/h** con un **pH de {ph_objetivo:.2f}** (equivalente a ~{g_pl_acido_puro:.2f} g/L de $H_2SO_4$ puro), se deben mezclar **{caudal_agua_m3_h:.2f} m³/h de agua** con **{volumen_acido_m3_h:.2f} m³/h de ácido sulfúrico**.")


# =====================================================================
# --- PÁGINA: EXTRACCIÓN POR SOLVENTES (SX) ---
# =====================================================================
elif seccion == "Extracción por Solventes":
    st.title("🧲 Extracción por Solventes (SX)")
    st.write("Selecciona la etapa específica del circuito de extracción por solventes para realizar los balances y cálculos operacionales correspondientes.")
    
    sub_sx = st.radio(
        "Selecciona el sub-módulo de SX:",
        ["Extracción", "Re-extracción", "Circuito Completo"],
        horizontal=True
    )
    
    st.markdown("---")
    
    if sub_sx == "Extracción":
        st.subheader("💧 Módulo de Extracción (Extraction)")
        st.write("Calcula la transferencia de cobre desde la solución rica (PLS) hacia la fase orgánica mediante un reactivo extractante.")
        
        st.latex(r"Cu^{2+}_{\text{(acuoso)}} + 2RH_{\text{(orgánico)}} \rightleftharpoons CuR_{2\text{(orgánico)}} + 2H^+_{\text{(acuoso)}}")
        
        col_ex1, col_ex2 = st.columns(2)
        with col_ex1:
            pls_flow = st.number_input("Caudal de PLS ($Q_{\text{PLS}}$) [m³/h]", min_value=0.1, value=500.0, step=10.0, format="%.2f")
            cu_pls = st.number_input("Ley de Cu en PLS ($Cu_{\text{PLS}}$) [g/L]", min_value=0.1, value=4.50, step=0.1, format="%.2f")
        with col_ex2:
            org_flow = st.number_input("Caudal de Orgánico ($Q_{\text{Org}}$) [m³/h]", min_value=0.1, value=400.0, step=10.0, format="%.2f")
            cu_raff = st.number_input("Ley de Cu en Refino ($Cu_{\text{Raf}}$) [g/L]", min_value=0.0, value=0.15, step=0.01, format="%.2f")
            
        cu_carga_org = cu_pls + (pls_flow / org_flow) * (cu_pls - cu_raff)
        recuperacion_ex = ((cu_pls - cu_raff) / cu_pls) * 100.0
        
        st.markdown("---")
        st.markdown("### 📊 Resultados de Extracción")
        
        res_ex1, res_ex2 = st.columns(2)
        with res_ex1:
            st.markdown(
                f"""
                <div style="background-color: #1e222d; padding: 20px; border-radius: 10px; border-left: 5px solid #3b82f6; text-align: center;">
                    <p style="color: #a1aab5; margin: 0; font-size: 0.95rem;">Cobre en Orgánico Cargado</p>
                    <h2 style="color: white; margin: 5px 0;">{cu_carga_org:.2f}</h2>
                    <p style="color: #60a5fa; margin: 0; font-weight: bold;">g/L</p>
                </div>
                """, unsafe_allow_html=True)
        with res_ex2:
            st.markdown(
                f"""
                <div style="background-color: #1e222d; padding: 20px; border-radius: 10px; border-left: 5px solid #10b981; text-align: center;">
                    <p style="color: #a1aab5; margin: 0; font-size: 0.95rem;">Eficiencia de Extracción</p>
                    <h2 style="color: white; margin: 5px 0;">{recuperacion_ex:.2f}</h2>
                    <p style="color: #34d399; margin: 0; font-weight: bold;">%</p>
                </div>
                """, unsafe_allow_html=True)
                
    elif sub_sx == "Re-extracción":
        st.subheader("🔄 Módulo de Re-extracción (Stripping)")
        st.write("Calcula la transferencia de cobre desde el orgánico cargado hacia el electrolito pobre utilizando una solución ácida de avance.")
        
        st.latex(r"CuR_{2\text{(orgánico)}} + 2H^+_{\text{(acuoso)}} \rightleftharpoons Cu^{2+}_{\text{(acuoso)}} + 2RH_{\text{(orgánico)}}")
        
        col_str1, col_str2 = st.columns(2)
        with col_str1:
            org_cargado_flow = st.number_input("Caudal de Orgánico Cargado [m³/h]", min_value=0.1, value=400.0, step=10.0, format="%.2f", key="oc_flow")
            cu_org_cargado = st.number_input("Cu en Orgánico Cargado [g/L]", min_value=0.1, value=5.80, step=0.1, format="%.2f", key="coc_flow")
        with col_str2:
            electrolito_pobre_flow = st.number_input("Caudal de Electrolito Pobre ($Q_{\text{EP}}$) [m³/h]", min_value=0.1, value=100.0, step=5.0, format="%.2f")
            cu_electrolito_pobre = st.number_input("Cu en Electrolito Pobre [g/L]", min_value=0.0, value=35.00, step=1.0, format="%.2f")
            
        cu_electrolito_rico = cu_electrolito_pobre + (org_cargado_flow / electrolito_pobre_flow) * (cu_org_cargado * 0.90)
        
        st.markdown("---")
        st.markdown("### 📊 Resultados de Re-extracción")
        
        res_st1, res_st2 = st.columns(2)
        with res_st1:
            st.markdown(
                f"""
                <div style="background-color: #1e222d; padding: 20px; border-radius: 10px; border-left: 5px solid #f59e0b; text-align: center;">
                    <p style="color: #a1aab5; margin: 0; font-size: 0.95rem;">Cu en Electrolito Rico (ELR)</p>
                    <h2 style="color: white; margin: 5px 0;">{cu_electrolito_rico:.2f}</h2>
                    <p style="color: #facc15; margin: 0; font-weight: bold;">g/L</p>
                </div>
                """, unsafe_allow_html=True)
        with res_st2:
            st.markdown(
                f"""
                <div style="background-color: #1e222d; padding: 20px; border-radius: 10px; border-left: 5px solid #a855f7; text-align: center;">
                    <p style="color: #a1aab5; margin: 0; font-size: 0.95rem;">Relación de Caudales ($O/A$)</p>
                    <h2 style="color: white; margin: 5px 0;">{(org_cargado_flow / electrolito_pobre_flow):.2f}</h2>
                    <p style="color: #c084fc; margin: 0; font-weight: bold;">Adimensional</p>
                </div>
                """, unsafe_allow_html=True)
                
    else:  # Circuito Completo
        st.subheader("🌐 Balance General del Circuito Completo de SX")
        st.write("Simulación integrada de las etapas de Extracción y Re-extracción para evaluar el comportamiento global de la planta.")
        
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            q_pls_tot = st.number_input("Caudal de PLS Total [m³/h]", min_value=0.1, value=500.0, step=10.0, format="%.2f", key="qp_tot")
            ley_pls_tot = st.number_input("Ley de Cu en PLS [g/L]", min_value=0.1, value=4.50, step=0.1, format="%.2f", key="lp_tot")
        with col_g2:
            q_org_tot = st.number_input("Caudal de Orgánico Total [m³/h]", min_value=0.1, value=400.0, step=10.0, format="%.2f", key="qo_tot")
            eficiencia_global = st.slider("Eficiencia Global Estimada del Circuito [%]", min_value=80.0, max_value=99.9, value=95.0, step=0.5)
            
        cu_recuperado_tph = (q_pls_tot * ley_pls_tot * (eficiencia_global / 100.0)) / 1000.0
        
        st.markdown("---")
        st.markdown("### 📋 Resumen Global del Proceso SX")
        
        res_g1, res_g2, res_g3 = st.columns(3)
        res_g1.metric("Caudal PLS", f"{q_pls_tot:.2f} m³/h")
        res_g2.metric("Caudal Orgánico", f"{q_org_tot:.2f} m³/h")
        res_g3.metric("Producción Est. Cobre", f"{cu_recuperado_tph:.2f} t/h")


# =====================================================================
# --- PIE DE PÁGINA ---
# =====================================================================
st.markdown("---")
st.markdown("<p style='text-align: center; color: #a1aab5;'>Creado por D&P</p>", unsafe_allow_html=True)
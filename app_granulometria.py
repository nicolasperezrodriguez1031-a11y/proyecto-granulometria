import streamlit as st

# Importar todos los módulos desde la carpeta 'modulos' con las funciones reales
from modulos.inicio import mostrar_inicio, mostrar_quienes_somos
from modulos.caracterizacion import mostrar_minerales, mostrar_estimador_ley
from modulos.conminucion import mostrar_chancado, mostrar_granulometria, mostrar_ley_bond, mostrar_razon_reduccion
from modulos.aglomeracion_lx import mostrar_procesos_hidro, mostrar_aglomeracion, mostrar_preparacion_lx
from modulos.sx import mostrar_sx
from modulos.electroobtencion import mostrar_fundamentos_ew, mostrar_calculadora_ew
from modulos.asistente import mostrar_asistente

# Configuración de la página (layout ancho y tema oscuro)
st.set_page_config(page_title="Gestión de Procesos Metalúrgicos de Minerales Oxidados", layout="wide")

# --- CONTROL DE NAVEGACIÓN EN LOS APARTADOS ---
if 'pagina_actual' not in st.session_state:
    st.session_state.pagina_actual = "Inicio"

st.sidebar.title("Menú de Navegación")

if st.sidebar.button("🏠 Inicio", use_container_width=True):
    st.session_state.pagina_actual = "Inicio"

if st.sidebar.button("👥 Quiénes somos", use_container_width=True):
    st.session_state.pagina_actual = "Quiénes somos"

st.sidebar.markdown("---")

# 1. CARACTERIZACIÓN MINERALÓGICA
with st.sidebar.expander("1️⃣ Caracterización mineralógica", expanded=True):
    if st.button("🟤 Minerales oxidados", use_container_width=True):
        st.session_state.pagina_actual = "Minerales oxidados"
    if st.button("🧮 Estimador Ley de Cabeza", use_container_width=True):
        st.session_state.pagina_actual = "Estimador Ley de Cabeza"

# 2. CONMINUCIÓN
with st.sidebar.expander("2️⃣ Conminución", expanded=True):
    if st.button("🔨 Chancado", use_container_width=True):
        st.session_state.pagina_actual = "Chancado"
    if st.button("📊 Análisis granulométrico", use_container_width=True):
        st.session_state.pagina_actual = "Análisis granulométrico"
    if st.button("⚡ Calculadora Ley de Bond", use_container_width=True):
        st.session_state.pagina_actual = "Calculadora Ley de Bond"
    if st.button("📐 Razón de Reducción", use_container_width=True):
        st.session_state.pagina_actual = "Razón de Reducción"

# 3. AGLOMERACIÓN Y LX
with st.sidebar.expander("3️⃣ Aglomeración y LX", expanded=True):
    if st.button("💧 Procesos Hidrometalúrgicos", use_container_width=True):
        st.session_state.pagina_actual = "Procesos Hidrometalúrgicos"
    if st.button("🧮 Calculadora de Aglomeración", use_container_width=True):
        st.session_state.pagina_actual = "Calculadora de Aglomeración"
    if st.button("🧪 Preparación de Solución LX", use_container_width=True):
        st.session_state.pagina_actual = "Preparación de Solución LX"

# 4. EXTRACCIÓN POR SOLVENTES
with st.sidebar.expander("4️⃣ Extracción por solventes", expanded=True):
    if st.button("🧲 Módulo Extracción / SX", use_container_width=True):
        st.session_state.pagina_actual = "Módulo Extracción / SX"

# 5. ELECTROOBTENCIÓN
with st.sidebar.expander("5️⃣ Electroobtención", expanded=True):
    if st.button("⚡ Fundamentos EW", use_container_width=True):
        st.session_state.pagina_actual = "Fundamentos EW"
    if st.button("🧮 Calculadora de Electrodepósito", use_container_width=True):
        st.session_state.pagina_actual = "Calculadora de Electrodepósito"

st.sidebar.markdown("---")
# BOTÓN PARA EL ASISTENTE IA EN LA BARRA LATERAL
if st.sidebar.button("🤖 Asistente Metalúrgico IA", use_container_width=True):
    st.session_state.pagina_actual = "Asistente Metalúrgico IA"

seccion = st.session_state.pagina_actual

# --- RUTEO PRINCIPAL DE PÁGINAS ---
if seccion == "Inicio":
    mostrar_inicio()
elif seccion == "Quiénes somos":
    mostrar_quienes_somos()
elif seccion == "Minerales oxidados":
    mostrar_minerales()
elif seccion == "Estimador Ley de Cabeza":
    mostrar_estimador_ley()
elif seccion == "Chancado":
    mostrar_chancado()
elif seccion == "Análisis granulométrico":
    mostrar_granulometria()
elif seccion == "Calculadora Ley de Bond":
    mostrar_ley_bond()
elif seccion == "Razón de Reducción":
    mostrar_razon_reduccion()
elif seccion == "Procesos Hidrometalúrgicos":
    mostrar_procesos_hidro()
elif seccion == "Calculadora de Aglomeración":
    mostrar_aglomeracion()
elif seccion == "Preparación de Solución LX":
    mostrar_preparacion_lx()
elif seccion == "Módulo Extracción / SX":
    mostrar_sx()
elif seccion == "Fundamentos EW":
    mostrar_fundamentos_ew()
elif seccion == "Calculadora de Electrodepósito":
    mostrar_calculadora_ew()
elif seccion == "Asistente Metalúrgico IA":
    mostrar_asistente()

# Pie de página
st.markdown("---")
st.markdown("<p style='text-align: center; color: #a1aab5;'>Creado por D&P</p>", unsafe_allow_html=True)
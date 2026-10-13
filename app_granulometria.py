
import streamlit as st

# ============================================================
# IMPORTACIÓN DE MÓDULOS
# ============================================================

from modulos.inicio import mostrar_inicio, mostrar_quienes_somos

from modulos.caracterizacion import (
    mostrar_minerales,
    mostrar_estimador_ley
)

from modulos.conminucion import (
    mostrar_chancado,
    mostrar_granulometria,
    mostrar_razon_reduccion
)

from modulos.aglomeracion_lx import (
    mostrar_procesos_hidro,
    mostrar_aglomeracion,
    mostrar_preparacion_lx
)

from modulos.sx import mostrar_sx

from modulos.electroobtencion import (
    mostrar_fundamentos_ew,
    mostrar_calculadora_ew
)

from modulos.asistente import mostrar_asistente


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

st.set_page_config(
    page_title="Gestión de Procesos Metalúrgicos de Minerales Oxidados",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# REGISTRO CENTRAL DE PÁGINAS
# ============================================================

PAGINAS = {
    "Inicio": mostrar_inicio,
    "Quiénes somos": mostrar_quienes_somos,

    "Minerales oxidados": mostrar_minerales,
    "Estimador Ley de Cabeza": mostrar_estimador_ley,

    "Chancado": mostrar_chancado,
    "Análisis granulométrico": mostrar_granulometria,
    "Razón de Reducción": mostrar_razon_reduccion,

    "Procesos Hidrometalúrgicos": mostrar_procesos_hidro,
    "Calculadora de Aglomeración": mostrar_aglomeracion,
    "Preparación de Solución LX": mostrar_preparacion_lx,

    "Módulo Extracción / SX": mostrar_sx,

    "Fundamentos EW": mostrar_fundamentos_ew,
    "Calculadora de Electrodepósito": mostrar_calculadora_ew,

    "Asistente Metalúrgico IA": mostrar_asistente
}


# ============================================================
# ESTADO DE NAVEGACIÓN
# ============================================================

if "pagina_actual" not in st.session_state:
    st.session_state.pagina_actual = "Inicio"


def cambiar_pagina(nombre_pagina):
    """Actualiza la página seleccionada."""
    if nombre_pagina in PAGINAS:
        st.session_state.pagina_actual = nombre_pagina


# ============================================================
# FUNCIÓN AUXILIAR PARA BOTONES
# ============================================================

def boton_navegacion(texto, pagina):
    """Genera un botón de navegación."""

    st.button(
        texto,
        key=f"nav_{pagina}",
        use_container_width=True,
        on_click=cambiar_pagina,
        args=(pagina,)
    )


# ============================================================
# MENÚ LATERAL
# ============================================================

with st.sidebar:

    st.title("Menú de Navegación")

    boton_navegacion("🏠 Inicio", "Inicio")
    boton_navegacion("👥 Quiénes somos", "Quiénes somos")

    st.markdown("---")

    # 1. CARACTERIZACIÓN MINERALÓGICA

    with st.expander(
        "1️⃣ Caracterización mineralógica",
        expanded=True
    ):

        boton_navegacion(
            "🟤 Minerales oxidados",
            "Minerales oxidados"
        )

        boton_navegacion(
            "🧮 Estimador Ley de Cabeza",
            "Estimador Ley de Cabeza"
        )

    # 2. CONMINUCIÓN

    with st.expander(
        "2️⃣ Conminución",
        expanded=True
    ):

        boton_navegacion(
            "🔨 Chancado",
            "Chancado"
        )

        boton_navegacion(
            "📊 Análisis granulométrico",
            "Análisis granulométrico"
        )

        boton_navegacion(
            "📐 Razón de Reducción",
            "Razón de Reducción"
        )

    # 3. AGLOMERACIÓN Y LIXIVIACIÓN

    with st.expander(
        "3️⃣ Aglomeración y LX",
        expanded=True
    ):

        boton_navegacion(
            "💧 Procesos Hidrometalúrgicos",
            "Procesos Hidrometalúrgicos"
        )

        boton_navegacion(
            "🧮 Calculadora de Aglomeración",
            "Calculadora de Aglomeración"
        )

        boton_navegacion(
            "🧪 Preparación de Solución LX",
            "Preparación de Solución LX"
        )

    # 4. EXTRACCIÓN POR SOLVENTES

    with st.expander(
        "4️⃣ Extracción por solventes",
        expanded=True
    ):

        boton_navegacion(
            "🧲 Módulo Extracción / SX",
            "Módulo Extracción / SX"
        )

    # 5. ELECTROOBTENCIÓN

    with st.expander(
        "5️⃣ Electroobtención",
        expanded=True
    ):

        boton_navegacion(
            "⚡ Fundamentos EW",
            "Fundamentos EW"
        )

        boton_navegacion(
            "🧮 Calculadora de Electrodepósito",
            "Calculadora de Electrodepósito"
        )

    st.markdown("---")

    # 6. ASISTENTE IA

    boton_navegacion(
        "🤖 Asistente Metalúrgico IA",
        "Asistente Metalúrgico IA"
    )


# ============================================================
# EJECUCIÓN DE LA PÁGINA SELECCIONADA
# ============================================================

pagina_actual = st.session_state.pagina_actual

if pagina_actual not in PAGINAS:
    st.warning(
        "La página seleccionada no existe. "
        "Se mostrará la página de inicio."
    )
    pagina_actual = "Inicio"
    st.session_state.pagina_actual = pagina_actual

funcion_pagina = PAGINAS[pagina_actual]

funcion_pagina()


# ============================================================
# PIE DE PÁGINA
# ============================================================

st.markdown("---")

st.markdown(
    """
    <p style="
        text-align: center;
        color: #a1aab5;
        font-size: 0.9rem;
    ">
        Creado por D&P
    </p>
    """,
    unsafe_allow_html=True
)

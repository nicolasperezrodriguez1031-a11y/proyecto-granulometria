
import streamlit as st


# ============================================================
# CONSTANTES ELECTROQUÍMICAS
# ============================================================

MASA_MOLAR_CU = 63.546       # g/mol
CONSTANTE_FARADAY = 96485.0  # C/mol
ELECTRONES_CU = 2


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def tarjeta_resultado(titulo, valor, unidad, color):
    """Genera una tarjeta de resultados."""

    return f"""
    <div style="
        background-color: #1e222d;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid {color};
        text-align: center;
        margin-bottom: 12px;
    ">
        <p style="
            color: #a1aab5;
            margin: 0;
            font-size: 0.95rem;
        ">
            {titulo}
        </p>

        <h2 style="
            color: white;
            margin: 8px 0;
        ">
            {valor}
        </h2>

        <p style="
            color: {color};
            margin: 0;
            font-weight: bold;
        ">
            {unidad}
        </p>
    </div>
    """


def calcular_deposito(
    corriente_ka,
    eficiencia_pct,
    numero_celdas,
    voltaje_celda
):
    """
    Calcula producción y consumo eléctrico
    de un conjunto de celdas de electroobtención.

    Supuestos:
    - Corriente constante.
    - Eficiencia de corriente constante.
    - Celdas idénticas.
    - Operación continua.
    """

    corriente_a = corriente_ka * 1000.0
    eficiencia = eficiencia_pct / 100.0

    # --------------------------------------------------------
    # LEY DE FARADAY
    # --------------------------------------------------------

    masa_teorica_g_h_celda = (
        corriente_a
        * 3600.0
        * MASA_MOLAR_CU
        / (ELECTRONES_CU * CONSTANTE_FARADAY)
    )

    masa_real_g_h_celda = (
        masa_teorica_g_h_celda * eficiencia
    )

    # --------------------------------------------------------
    # PRODUCCIÓN
    # --------------------------------------------------------

    produccion_horaria_t = (
        masa_real_g_h_celda
        * numero_celdas
        / 1_000_000.0
    )

    produccion_diaria_t = (
        produccion_horaria_t * 24.0
    )

    produccion_mensual_t = (
        produccion_diaria_t * 30.0
    )

    # --------------------------------------------------------
    # POTENCIA ELÉCTRICA
    # --------------------------------------------------------

    potencia_celda_kw = (
        corriente_ka * voltaje_celda
    )

    potencia_total_kw = (
        potencia_celda_kw * numero_celdas
    )

    # --------------------------------------------------------
    # ENERGÍA
    # --------------------------------------------------------

    energia_diaria_kwh = (
        potencia_total_kw * 24.0
    )

    consumo_especifico_kwh_t = (
        energia_diaria_kwh / produccion_diaria_t
        if produccion_diaria_t > 0
        else 0.0
    )

    return {
        "masa_teorica_g_h_celda": masa_teorica_g_h_celda,
        "masa_real_g_h_celda": masa_real_g_h_celda,
        "produccion_horaria_t": produccion_horaria_t,
        "produccion_diaria_t": produccion_diaria_t,
        "produccion_mensual_t": produccion_mensual_t,
        "potencia_celda_kw": potencia_celda_kw,
        "potencia_total_kw": potencia_total_kw,
        "energia_diaria_kwh": energia_diaria_kwh,
        "consumo_especifico_kwh_t": consumo_especifico_kwh_t
    }


# ============================================================
# 1. FUNDAMENTOS DE ELECTROOBTENCIÓN
# ============================================================

def mostrar_fundamentos_ew():

    st.title("⚡ Fundamentos de Electroobtención")

    st.write(
        "La electroobtención de cobre es un proceso "
        "electroquímico que utiliza corriente continua "
        "para reducir los iones de cobre presentes "
        "en una solución electrolítica y depositarlos "
        "como cobre metálico sobre cátodos."
    )

    st.markdown("---")

    st.markdown("### 🔬 Reacciones Electroquímicas")

    st.markdown("#### Cátodo: reducción del cobre")

    st.latex(
        r"Cu^{2+}_{(ac)} + 2e^- "
        r"\rightarrow Cu^0_{(s)}"
    )

    st.write(
        "En el cátodo, los iones de cobre ganan "
        "electrones y se depositan en forma metálica."
    )

    st.markdown("#### Ánodo: oxidación del agua")

    st.latex(
        r"H_2O \rightarrow "
        r"\frac{1}{2}O_{2(g)} + 2H^+_{(ac)} + 2e^-"
    )

    st.write(
        "En un sistema convencional con ánodos "
        "insolubles, el agua se oxida y se genera "
        "oxígeno gaseoso."
    )

    st.markdown("---")

    st.markdown("### ⚙️ Principales Variables Operacionales")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            tarjeta_resultado(
                "Densidad de Corriente",
                "Variable",
                "A/m²",
                "#3b82f6"
            ),
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            tarjeta_resultado(
                "Eficiencia de Corriente",
                "Variable",
                "%",
                "#22c55e"
            ),
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            tarjeta_resultado(
                "Voltaje de Celda",
                "Variable",
                "V",
                "#f59e0b"
            ),
            unsafe_allow_html=True
        )

    st.info(
        "La producción de cobre depende de la "
        "corriente aplicada, el tiempo de operación "
        "y la eficiencia de corriente. El consumo "
        "energético depende también del voltaje "
        "de las celdas."
    )


# ============================================================
# 2. CALCULADORA DE ELECTRODEPÓSITO
# ============================================================

def mostrar_calculadora_ew():

    st.title("🧮 Calculadora de Electrodepósito")

    st.write(
        "Calcula la producción de cobre depositado, "
        "la potencia eléctrica requerida y el "
        "consumo energético mediante la Ley de Faraday."
    )

    st.latex(
        r"m = \frac{I \cdot t \cdot M \cdot \eta}"
        r"{z \cdot F}"
    )

    st.markdown("---")

    # --------------------------------------------------------
    # PARÁMETROS DE OPERACIÓN
    # --------------------------------------------------------

    st.markdown("### 📥 Parámetros de Operación")

    ce1, ce2 = st.columns(2)

    with ce1:

        i_ka = st.number_input(
            "Corriente Total por Celda (I) [kA]",
            min_value=0.01,
            value=35.0,
            step=1.0,
            format="%.2f",
            key="ew_corriente"
        )

        ef_c = st.number_input(
            "Eficiencia de Corriente [%]",
            min_value=0.0,
            max_value=100.0,
            value=92.0,
            step=0.5,
            format="%.2f",
            key="ew_eficiencia"
        )

    with ce2:

        n_cel = st.number_input(
            "Número de Celdas en Operación",
            min_value=1,
            value=40,
            step=1,
            key="ew_num_celdas"
        )

        v_cel = st.number_input(
            "Voltaje por Celda [V]",
            min_value=0.01,
            value=2.10,
            step=0.05,
            format="%.2f",
            key="ew_voltaje"
        )

    # --------------------------------------------------------
    # CÁLCULOS
    # --------------------------------------------------------

    resultados = calcular_deposito(
        corriente_ka=i_ka,
        eficiencia_pct=ef_c,
        numero_celdas=n_cel,
        voltaje_celda=v_cel
    )

    # --------------------------------------------------------
    # RESULTADOS PRINCIPALES
    # --------------------------------------------------------

    st.markdown("---")

    st.markdown("### 📊 Resultados de Operación EW")

    rc1, rc2 = st.columns(2)

    with rc1:

        st.markdown(
            tarjeta_resultado(
                "Producción Diaria de Cobre",
                f"{resultados['produccion_diaria_t']:.2f}",
                "toneladas / día",
                "#22c55e"
            ),
            unsafe_allow_html=True
        )

    with rc2:

        st.markdown(
            tarjeta_resultado(
                "Potencia Total Requerida",
                f"{resultados['potencia_total_kw']:.2f}",
                "kW",
                "#3b82f6"
            ),
            unsafe_allow_html=True
        )

    # --------------------------------------------------------
    # PRODUCCIÓN
    # --------------------------------------------------------

    st.markdown("### ⚖️ Producción de Cobre")

    p1, p2, p3 = st.columns(3)

    p1.metric(
        "Producción por Hora",
        f"{resultados['produccion_horaria_t']:.3f} t/h"
    )

    p2.metric(
        "Producción Diaria",
        f"{resultados['produccion_diaria_t']:.3f} t/día"
    )

    p3.metric(
        "Producción Mensual Estimada",
        f"{resultados['produccion_mensual_t']:.2f} t/mes"
    )

    st.caption(
        "La producción mensual considera "
        "30 días de operación continua."
    )

    # --------------------------------------------------------
    # MASA POR CELDA
    # --------------------------------------------------------

    st.markdown("### 🔬 Depósito por Celda")

    m1, m2 = st.columns(2)

    m1.metric(
        "Masa Teórica",
        f"{resultados['masa_teorica_g_h_celda']:.2f} g/h"
    )

    m2.metric(
        "Masa Real Estimada",
        f"{resultados['masa_real_g_h_celda']:.2f} g/h"
    )

    # --------------------------------------------------------
    # ENERGÍA
    # --------------------------------------------------------

    st.markdown("---")

    st.markdown("### ⚡ Consumo Energético")

    e1, e2 = st.columns(2)

    e1.metric(
        "Energía Diaria",
        f"{resultados['energia_diaria_kwh']:,.2f} kWh"
    )

    if resultados["produccion_diaria_t"] > 0:

        e2.metric(
            "Consumo Específico",
            f"{resultados['consumo_especifico_kwh_t']:,.2f} kWh/t"
        )

    else:

        e2.metric(
            "Consumo Específico",
            "No calculable"
        )

        st.warning(
            "La eficiencia de corriente es 0%, "
            "por lo que no existe producción "
            "de cobre para calcular el "
            "consumo específico."
        )

    st.markdown("---")

    st.info(
        "Los resultados se obtienen suponiendo "
        "corriente y voltaje constantes, "
        "eficiencia de corriente uniforme "
        "y operación continua de todas las celdas."
    )

    st.caption(
        "El consumo específico calculado considera "
        "únicamente la potencia eléctrica de las "
        "celdas. No incluye pérdidas en rectificadores, "
        "bombas, sistemas auxiliares ni otros "
        "consumos de la nave de electroobtención."
    )

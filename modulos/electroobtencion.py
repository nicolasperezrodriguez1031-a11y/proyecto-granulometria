
import streamlit as st
import pandas as pd
from html import escape


# ============================================================
# CONSTANTES ELECTROQUÍMICAS
# ============================================================

CONSTANTE_FARADAY = 96485.0

METALES = {
    "Cobre (Cu)": {
        "simbolo": "Cu",
        "ion": "Cu²⁺",
        "masa_molar": 63.546,
        "electrones": 2,
        "reaccion": r"Cu^{2+} + 2e^- \rightarrow Cu_{(s)}",
    },
    "Zinc (Zn)": {
        "simbolo": "Zn",
        "ion": "Zn²⁺",
        "masa_molar": 65.38,
        "electrones": 2,
        "reaccion": r"Zn^{2+} + 2e^- \rightarrow Zn_{(s)}",
    },
    "Níquel (Ni)": {
        "simbolo": "Ni",
        "ion": "Ni²⁺",
        "masa_molar": 58.6934,
        "electrones": 2,
        "reaccion": r"Ni^{2+} + 2e^- \rightarrow Ni_{(s)}",
    },
    "Plata (Ag)": {
        "simbolo": "Ag",
        "ion": "Ag⁺",
        "masa_molar": 107.8682,
        "electrones": 1,
        "reaccion": r"Ag^+ + e^- \rightarrow Ag_{(s)}",
    },
    "Hierro (Fe)": {
        "simbolo": "Fe",
        "ion": "Fe²⁺",
        "masa_molar": 55.845,
        "electrones": 2,
        "reaccion": r"Fe^{2+} + 2e^- \rightarrow Fe_{(s)}",
    },
    "Estaño (Sn)": {
        "simbolo": "Sn",
        "ion": "Sn²⁺",
        "masa_molar": 118.710,
        "electrones": 2,
        "reaccion": r"Sn^{2+} + 2e^- \rightarrow Sn_{(s)}",
    },
    "Plomo (Pb)": {
        "simbolo": "Pb",
        "ion": "Pb²⁺",
        "masa_molar": 207.2,
        "electrones": 2,
        "reaccion": r"Pb^{2+} + 2e^- \rightarrow Pb_{(s)}",
    },
    "Cobalto (Co)": {
        "simbolo": "Co",
        "ion": "Co²⁺",
        "masa_molar": 58.933,
        "electrones": 2,
        "reaccion": r"Co^{2+} + 2e^- \rightarrow Co_{(s)}",
    },
    "Cadmio (Cd)": {
        "simbolo": "Cd",
        "ion": "Cd²⁺",
        "masa_molar": 112.414,
        "electrones": 2,
        "reaccion": r"Cd^{2+} + 2e^- \rightarrow Cd_{(s)}",
    },
    "Oro (Au)": {
        "simbolo": "Au",
        "ion": "Au³⁺",
        "masa_molar": 196.96657,
        "electrones": 3,
        "reaccion": r"Au^{3+} + 3e^- \rightarrow Au_{(s)}",
    },
}


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def formatear_numero(valor, decimales=2):
    """
    Presenta los números con punto de miles y coma decimal.

    Por defecto se muestran dos decimales.
    Los cálculos conservan su precisión interna.
    """
    numero = f"{float(valor):,.{decimales}f}"

    return (
        numero.replace(",", "TEMP")
        .replace(".", ",")
        .replace("TEMP", ".")
    )


def tarjeta_resultado(
    titulo,
    valor,
    unidad,
    color,
    descripcion=""
):
    """
    Genera una tarjeta visual de resultados.
    """

    titulo = escape(str(titulo))
    valor = escape(str(valor))
    unidad = escape(str(unidad))
    color = escape(str(color))
    descripcion = escape(str(descripcion))

    return (
        f'<div style="'
        f'background:#1e2430;'
        f'border:1px solid #374151;'
        f'border-top:4px solid {color};'
        f'border-radius:14px;'
        f'padding:24px 16px;'
        f'text-align:center;'
        f'min-height:185px;'
        f'box-sizing:border-box;'
        f'margin-bottom:12px;'
        f'">'
        f'<div style="'
        f'font-size:15px;'
        f'font-weight:600;'
        f'color:#cbd5e1;'
        f'margin-bottom:14px;'
        f'">{titulo}</div>'
        f'<div style="'
        f'font-size:clamp(25px,3vw,39px);'
        f'font-weight:800;'
        f'color:{color};'
        f'line-height:1.2;'
        f'overflow-wrap:anywhere;'
        f'">{valor}</div>'
        f'<div style="'
        f'font-size:16px;'
        f'font-weight:600;'
        f'color:#ffffff;'
        f'margin-top:8px;'
        f'">{unidad}</div>'
        f'<div style="'
        f'font-size:12px;'
        f'color:#94a3b8;'
        f'margin-top:12px;'
        f'">{descripcion}</div>'
        f'</div>'
    )


# ============================================================
# FUNCIONES DE CÁLCULO
# ============================================================

def calcular_intensidad_corriente(
    densidad_corriente,
    area_catodica
):
    """
    I = j * A

    j: densidad de corriente en A/m²
    A: área catódica en m²
    I: intensidad de corriente en A
    """

    return densidad_corriente * area_catodica


def calcular_masa_depositada(
    intensidad_corriente,
    tiempo_segundos,
    masa_molar=63.546,
    electrones=2
):
    """
    Calcula exclusivamente la masa teórica mediante
    la primera Ley de Faraday.

    m_F = (I * t * M) / (n * F)

    No se aplica una eficiencia supuesta.
    """

    if electrones <= 0:
        raise ValueError(
            "El número de electrones debe ser positivo."
        )

    masa_teorica_g = (
        intensidad_corriente
        * tiempo_segundos
        * masa_molar
        / (electrones * CONSTANTE_FARADAY)
    )

    return {
        "masa_teorica_g": masa_teorica_g
    }


def calcular_masa_real(
    masa_inicial_g,
    masa_final_g
):
    """
    Masa real depositada:

    m_real = m_final - m_inicial
    """

    return masa_final_g - masa_inicial_g


def calcular_eficiencia_corriente(
    masa_real_g,
    masa_teorica_g
):
    """
    Eficiencia de corriente experimental:

    eficiencia = (m_real / m_F) * 100
    """

    if masa_teorica_g <= 0:
        return None

    return (
        masa_real_g
        / masa_teorica_g
        * 100.0
    )


def calcular_deposito_laboratorio(
    densidad_corriente,
    area_catodica,
    tiempo_segundos,
    masa_molar=63.546,
    electrones=2,
    intensidad_manual=None,
    masa_inicial_g=None,
    masa_final_g=None
):
    """
    Calcula los resultados de un ensayo de laboratorio.

    Permite:
    - Calcular la intensidad mediante j * A.
    - Utilizar una intensidad manual.
    - Determinar la masa teórica por Faraday.
    - Calcular la masa real experimental.
    - Calcular la eficiencia experimental.
    """

    intensidad_calculada = calcular_intensidad_corriente(
        densidad_corriente=densidad_corriente,
        area_catodica=area_catodica
    )

    if intensidad_manual is None:
        intensidad_utilizada = intensidad_calculada
    else:
        intensidad_utilizada = intensidad_manual

    resultados_masa = calcular_masa_depositada(
        intensidad_corriente=intensidad_utilizada,
        tiempo_segundos=tiempo_segundos,
        masa_molar=masa_molar,
        electrones=electrones
    )

    masa_teorica_g = resultados_masa["masa_teorica_g"]

    masa_real_g = None
    eficiencia_experimental = None

    if (
        masa_inicial_g is not None
        and masa_final_g is not None
    ):
        masa_real_g = calcular_masa_real(
            masa_inicial_g,
            masa_final_g
        )

        eficiencia_experimental = calcular_eficiencia_corriente(
            masa_real_g,
            masa_teorica_g
        )

    return {
        "densidad_corriente": densidad_corriente,
        "area_catodica": area_catodica,
        "intensidad_calculada": intensidad_calculada,
        "intensidad_corriente": intensidad_utilizada,
        "tiempo_segundos": tiempo_segundos,
        "masa_molar": masa_molar,
        "electrones": electrones,
        "masa_teorica_g": masa_teorica_g,
        "masa_inicial_g": masa_inicial_g,
        "masa_final_g": masa_final_g,
        "masa_real_g": masa_real_g,
        "eficiencia_corriente": eficiencia_experimental,
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
        "La masa teórica depositada depende de la "
        "intensidad de corriente, el tiempo de electrólisis "
        "y las propiedades electroquímicas del metal. "
        "La eficiencia experimental se determina "
        "comparando la masa realmente depositada "
        "con la masa teórica de Faraday."
    )


# ============================================================
# 2. CALCULADORA DE ELECTRODEPÓSITO
# ============================================================

def mostrar_calculadora_ew():

    st.title("🧮 Calculadora de Electrodepósito")

    st.write(
        "Calculadora de laboratorio para determinar "
        "la intensidad de corriente, la masa teórica "
        "depositada, la masa real experimental y "
        "la eficiencia de corriente."
    )

    st.markdown("---")

    # ========================================================
    # 1. INTENSIDAD DE CORRIENTE
    # ========================================================

    st.header("1. Intensidad de Corriente")

    st.write(
        "La intensidad de corriente se determina "
        "multiplicando la densidad de corriente "
        "por el área catódica expuesta."
    )

    st.latex(r"I = j \cdot A")

    st.markdown("### 📥 Parámetros de Corriente")

    col1, col2 = st.columns(2)

    with col1:

        densidad_corriente = st.number_input(
            "Densidad de corriente (j) [A/m²]",
            min_value=0.0,
            value=250.0,
            step=10.0,
            format="%.2f",
            key="ew_lab_densidad_corriente"
        )

    with col2:

        unidad_area = st.selectbox(
            "Unidad de medida del área catódica",
            options=["m²", "cm²"],
            index=1,
            key="ew_lab_unidad_area"
        )

        if unidad_area == "m²":

            area_ingresada = st.number_input(
                "Área catódica (A) [m²]",
                min_value=0.0,
                value=0.01,
                step=0.01,
                format="%.2f",
                key="ew_lab_area_m2"
            )

            area_m2 = area_ingresada

        else:

            area_ingresada = st.number_input(
                "Área catódica (A) [cm²]",
                min_value=0.0,
                value=100.0,
                step=10.0,
                format="%.2f",
                key="ew_lab_area_cm2"
            )

            area_m2 = area_ingresada / 10000.0

    intensidad_calculada = calcular_intensidad_corriente(
        densidad_corriente,
        area_m2
    )

    st.markdown("### 📊 Resultado de Intensidad")

    st.markdown(
        tarjeta_resultado(
            titulo="⚡ Intensidad de Corriente Calculada",
            valor=formatear_numero(intensidad_calculada),
            unidad="amperios (A)",
            color="#38bdf8",
            descripcion="Resultado de I = j × A"
        ),
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ========================================================
    # 2. MASA TEÓRICA DEPOSITADA
    # ========================================================

    st.header("2. Masa Teórica de Metal Depositada")

    st.write(
        "Selecciona el metal y las condiciones "
        "del ensayo. La masa teórica se calcula "
        "mediante la primera Ley de Faraday."
    )

    st.latex(
        r"m_F = \frac{I \cdot t \cdot M}"
        r"{n \cdot F}"
    )

    # --------------------------------------------------------
    # SELECCIÓN DEL METAL
    # --------------------------------------------------------

    st.markdown("### 🔬 Selección del Metal")

    metal_seleccionado = st.selectbox(
        "Metal a depositar",
        options=list(METALES.keys()),
        index=None,
        placeholder="Selecciona un metal",
        key="ew_lab_metal"
    )

    if metal_seleccionado is None:

        st.info(
            "Selecciona un metal para continuar "
            "con el cálculo de la masa depositada."
        )

        return

    metal = METALES[metal_seleccionado]

    masa_molar = metal["masa_molar"]
    electrones = metal["electrones"]

    st.markdown("#### Semirreacción de Deposición")

    st.latex(metal["reaccion"])

    info1, info2 = st.columns(2)

    with info1:

        st.metric(
            "Masa molar del metal",
            f"{formatear_numero(masa_molar)} g/mol"
        )

    with info2:

        st.metric(
            "Electrones transferidos",
            str(electrones)
        )

    st.caption(
        "La masa molar y el número de electrones "
        "se actualizan automáticamente según "
        "el metal seleccionado."
    )

    st.markdown("---")

    # --------------------------------------------------------
    # INTENSIDAD PARA EL CÁLCULO DE MASA
    # --------------------------------------------------------

    st.markdown("### ⚡ Intensidad de Corriente a Utilizar")

    modo_corriente = st.radio(
        "Selecciona cómo utilizar la intensidad de corriente",
        options=[
            "Utilizar intensidad calculada anteriormente",
            "Ingresar una intensidad diferente"
        ],
        index=0,
        key="ew_lab_modo_corriente"
    )

    if modo_corriente == (
        "Utilizar intensidad calculada anteriormente"
    ):

        intensidad_utilizada = intensidad_calculada

        st.success(
            "Se utilizará la intensidad calculada "
            "en el punto 1: "
            f"{formatear_numero(intensidad_utilizada)} A."
        )

        origen_corriente = "Calculada mediante j × A"

    else:

        intensidad_utilizada = st.number_input(
            "Intensidad de corriente para la deposición [A]",
            min_value=0.0,
            value=2.50,
            step=0.10,
            format="%.2f",
            key="ew_lab_corriente_manual"
        )

        st.info(
            "La intensidad ingresada se utilizará "
            "únicamente para calcular la masa depositada. "
            "No modifica el resultado del punto 1."
        )

        origen_corriente = "Ingresada manualmente"

    # --------------------------------------------------------
    # TIEMPO DE ELECTRÓLISIS
    # --------------------------------------------------------

    st.markdown("### 📥 Parámetros de Electrodeposición")

    col3, col4 = st.columns(2)

    with col3:

        unidad_tiempo = st.selectbox(
            "Unidad de medida del tiempo",
            options=[
                "minutos",
                "segundos",
                "horas"
            ],
            index=0,
            key="ew_lab_unidad_tiempo"
        )

    with col4:

        if unidad_tiempo == "minutos":
            tiempo_predeterminado = 60.0

        elif unidad_tiempo == "segundos":
            tiempo_predeterminado = 3600.0

        else:
            tiempo_predeterminado = 1.0

        tiempo_experimental = st.number_input(
            f"Tiempo de electrólisis [{unidad_tiempo}]",
            min_value=0.0,
            value=tiempo_predeterminado,
            step=1.0,
            format="%.2f",
            key=f"ew_lab_tiempo_{unidad_tiempo}"
        )

    # --------------------------------------------------------
    # CONVERSIÓN DEL TIEMPO
    # --------------------------------------------------------

    if unidad_tiempo == "segundos":

        tiempo_segundos = tiempo_experimental

    elif unidad_tiempo == "minutos":

        tiempo_segundos = tiempo_experimental * 60.0

    else:

        tiempo_segundos = tiempo_experimental * 3600.0

    # --------------------------------------------------------
    # CÁLCULO DE MASA TEÓRICA
    # --------------------------------------------------------

    resultados = calcular_masa_depositada(
        intensidad_corriente=intensidad_utilizada,
        tiempo_segundos=tiempo_segundos,
        masa_molar=masa_molar,
        electrones=electrones
    )

    masa_teorica = resultados["masa_teorica_g"]

    st.markdown("### 📊 Resultado de Masa Teórica")

    st.markdown(
        tarjeta_resultado(
            titulo="⚖️ Masa Teórica Depositada",
            valor=formatear_numero(masa_teorica),
            unidad="gramos (g)",
            color="#22c55e",
            descripcion=(
                "Masa calculada mediante la Ley de Faraday, "
                "sin aplicar una eficiencia supuesta"
            )
        ),
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ========================================================
    # 3. MASA REAL DEPOSITADA
    # ========================================================

    st.header("3. Masa Real Depositada")

    st.write(
        "La masa real corresponde a la cantidad "
        "de metal obtenida experimentalmente. "
        "Se determina mediante la diferencia "
        "entre la masa final y la masa inicial "
        "del cátodo."
    )

    st.latex(
        r"m_{\mathrm{real}} = m_f - m_i"
    )

    st.markdown("### ⚖️ Mediciones del Cátodo")

    unidad_masa = st.selectbox(
        "Unidad de medida de las masas",
        options=["g", "kg"],
        index=0,
        key="ew_lab_unidad_masa"
    )

    masa_col1, masa_col2 = st.columns(2)

    with masa_col1:

        masa_inicial = st.number_input(
            f"Masa inicial del cátodo [{unidad_masa}]",
            min_value=0.0,
            value=0.0,
            step=0.01,
            format="%.2f",
            key=f"ew_lab_masa_inicial_{unidad_masa}"
        )

    with masa_col2:

        masa_final = st.number_input(
            f"Masa final del cátodo [{unidad_masa}]",
            min_value=0.0,
            value=0.0,
            step=0.01,
            format="%.2f",
            key=f"ew_lab_masa_final_{unidad_masa}"
        )

    # --------------------------------------------------------
    # CONVERSIÓN A GRAMOS
    # --------------------------------------------------------

    if unidad_masa == "kg":

        masa_inicial_g = masa_inicial * 1000.0
        masa_final_g = masa_final * 1000.0

    else:

        masa_inicial_g = masa_inicial
        masa_final_g = masa_final

    # --------------------------------------------------------
    # VALIDACIÓN DE LAS MEDICIONES
    # --------------------------------------------------------

    masas_ingresadas = (
        masa_inicial > 0
        or masa_final > 0
    )

    mediciones_validas = (
        masas_ingresadas
        and masa_final_g >= masa_inicial_g
    )

    if (
        masas_ingresadas
        and masa_final_g < masa_inicial_g
    ):

        st.error(
            "La masa final es menor que la masa inicial. "
            "Revisa los datos del ensayo. "
            "Para calcular una masa depositada positiva, "
            "la masa final debe ser igual o superior "
            "a la masa inicial."
        )

    if mediciones_validas:

        masa_real = calcular_masa_real(
            masa_inicial_g,
            masa_final_g
        )

        st.markdown("### 📊 Resultado de Masa Real")

        st.markdown(
            tarjeta_resultado(
                titulo="🧪 Masa Real Depositada",
                valor=formatear_numero(masa_real),
                unidad="gramos (g)",
                color="#38bdf8",
                descripcion=(
                    "Diferencia entre la masa final "
                    "y la masa inicial del cátodo"
                )
            ),
            unsafe_allow_html=True
        )

    else:

        masa_real = None

        if not masas_ingresadas:

            st.info(
                "Ingresa la masa inicial y la masa final "
                "del cátodo para calcular la masa real."
            )

    st.markdown("---")

    # ========================================================
    # 4. EFICIENCIA DE CORRIENTE EXPERIMENTAL
    # ========================================================

    st.header("4. Eficiencia de Corriente Experimental")

    st.write(
        "La eficiencia de corriente expresa qué "
        "porcentaje de la masa teórica calculada "
        "mediante Faraday se obtuvo realmente "
        "durante el ensayo."
    )

    st.latex(
        r"\eta_I = "
        r"\frac{m_{\mathrm{real}}}{m_F}"
        r"\times 100"
    )

    eficiencia_experimental = None

    if masa_real is not None:

        eficiencia_experimental = calcular_eficiencia_corriente(
            masa_real_g=masa_real,
            masa_teorica_g=masa_teorica
        )

        if eficiencia_experimental is None:

            st.warning(
                "No es posible calcular la eficiencia "
                "porque la masa teórica es igual a cero. "
                "Revisa la intensidad y el tiempo "
                "de electrólisis."
            )

        else:

            st.markdown(
                tarjeta_resultado(
                    titulo="⚡ Eficiencia de Corriente Calculada",
                    valor=formatear_numero(
                        eficiencia_experimental
                    ),
                    unidad="porcentaje (%)",
                    color="#fbbf24",
                    descripcion=(
                        "Relación entre la masa real "
                        "y la masa teórica de Faraday"
                    )
                ),
                unsafe_allow_html=True
            )

            if eficiencia_experimental > 100.0:

                st.warning(
                    "La eficiencia calculada supera "
                    "el 100 %. Esto puede indicar "
                    "humedad en el depósito, impurezas, "
                    "errores de pesaje o diferencias "
                    "entre la corriente registrada "
                    "y la corriente real del ensayo."
                )

            elif eficiencia_experimental == 0.0:

                st.info(
                    "La masa real registrada es cero. "
                    "Por lo tanto, la eficiencia "
                    "experimental también es cero."
                )

            else:

                st.success(
                    "La eficiencia experimental "
                    "se calculó correctamente "
                    "a partir de las masas medidas."
                )

    else:

        st.info(
            "Para obtener la eficiencia experimental, "
            "primero debes ingresar las masas "
            "inicial y final del cátodo."
        )

    st.markdown("---")

    # ========================================================
    # 5. RESUMEN DE RESULTADOS
    # ========================================================

    st.header("5. Resultados del Ensayo")

    st.write(
        f"Resumen del ensayo de laboratorio "
        f"para la deposición de {metal_seleccionado}."
    )

    resumen1, resumen2, resumen3 = st.columns(3)

    with resumen1:

        st.markdown(
            tarjeta_resultado(
                titulo="⚖️ Masa Teórica",
                valor=formatear_numero(masa_teorica),
                unidad="gramos (g)",
                color="#22c55e",
                descripcion="Ley de Faraday"
            ),
            unsafe_allow_html=True
        )

    with resumen2:

        st.markdown(
            tarjeta_resultado(
                titulo="🧪 Masa Real",
                valor=(
                    formatear_numero(masa_real)
                    if masa_real is not None
                    else "—"
                ),
                unidad="gramos (g)",
                color="#38bdf8",
                descripcion="Medición experimental"
            ),
            unsafe_allow_html=True
        )

    with resumen3:

        st.markdown(
            tarjeta_resultado(
                titulo="⚡ Eficiencia Experimental",
                valor=(
                    formatear_numero(eficiencia_experimental)
                    if eficiencia_experimental is not None
                    else "—"
                ),
                unidad="%",
                color="#fbbf24",
                descripcion="Masa real / masa teórica"
            ),
            unsafe_allow_html=True
        )

    # --------------------------------------------------------
    # TABLA DE RESULTADOS
    # --------------------------------------------------------

    st.markdown("### 📋 Tabla de Resultados del Ensayo")

    datos_tabla = [
        {
            "Parámetro": "Metal seleccionado",
            "Valor": metal_seleccionado,
            "Unidad": "—"
        },
        {
            "Parámetro": "Ion metálico",
            "Valor": metal["ion"],
            "Unidad": "—"
        },
        {
            "Parámetro": "Densidad de corriente",
            "Valor": formatear_numero(densidad_corriente),
            "Unidad": "A/m²"
        },
        {
            "Parámetro": "Área catódica",
            "Valor": formatear_numero(area_ingresada),
            "Unidad": unidad_area
        },
        {
            "Parámetro": "Intensidad calculada",
            "Valor": formatear_numero(intensidad_calculada),
            "Unidad": "A"
        },
        {
            "Parámetro": "Origen de la corriente utilizada",
            "Valor": origen_corriente,
            "Unidad": "—"
        },
        {
            "Parámetro": "Intensidad utilizada para la masa",
            "Valor": formatear_numero(intensidad_utilizada),
            "Unidad": "A"
        },
        {
            "Parámetro": "Tiempo de electrólisis",
            "Valor": formatear_numero(tiempo_experimental),
            "Unidad": unidad_tiempo
        },
        {
            "Parámetro": "Masa molar del metal",
            "Valor": formatear_numero(masa_molar),
            "Unidad": "g/mol"
        },
        {
            "Parámetro": "Electrones transferidos",
            "Valor": str(electrones),
            "Unidad": "—"
        },
        {
            "Parámetro": "Masa teórica depositada",
            "Valor": formatear_numero(masa_teorica),
            "Unidad": "g"
        },
        {
            "Parámetro": "Masa inicial del cátodo",
            "Valor": (
                formatear_numero(masa_inicial)
                if masas_ingresadas
                else "Pendiente"
            ),
            "Unidad": unidad_masa
        },
        {
            "Parámetro": "Masa final del cátodo",
            "Valor": (
                formatear_numero(masa_final)
                if masas_ingresadas
                else "Pendiente"
            ),
            "Unidad": unidad_masa
        },
        {
            "Parámetro": "Masa real depositada",
            "Valor": (
                formatear_numero(masa_real)
                if masa_real is not None
                else "Pendiente"
            ),
            "Unidad": "g"
        },
        {
            "Parámetro": "Eficiencia de corriente experimental",
            "Valor": (
                formatear_numero(eficiencia_experimental)
                if eficiencia_experimental is not None
                else "Pendiente"
            ),
            "Unidad": "%"
        }
    ]

    tabla_resultados = pd.DataFrame(datos_tabla)

    st.dataframe(
        tabla_resultados,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Parámetro": st.column_config.TextColumn(
                "Parámetro",
                width="large"
            ),
            "Valor": st.column_config.TextColumn(
                "Valor",
                width="medium"
            ),
            "Unidad": st.column_config.TextColumn(
                "Unidad",
                width="small"
            )
        }
    )

    st.info(
        "La masa teórica se obtiene mediante "
        "la Ley de Faraday. La masa real se determina "
        "mediante las mediciones del cátodo y la "
        "eficiencia experimental se calcula "
        "automáticamente. No se utiliza una "
        "eficiencia de corriente supuesta."
    )

    st.caption(
        "Los resultados corresponden a un ensayo "
        "de laboratorio. Se supone una intensidad "
        "de corriente constante y que el cambio "
        "de masa del cátodo corresponde al metal "
        "seleccionado. Las mediciones deben "
        "realizarse sobre un cátodo adecuadamente "
        "lavado y seco."
    )

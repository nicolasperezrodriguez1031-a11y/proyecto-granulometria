
import streamlit as st
import pandas as pd
from html import escape
from decimal import Decimal, ROUND_HALF_UP

def _excel_desde_tabla(tabla, nombre_hoja):
    """Genera el Excel en memoria para descargar desde Streamlit."""
    from io import BytesIO
    salida = BytesIO()
    with pd.ExcelWriter(salida, engine="openpyxl") as escritor:
        tabla.to_excel(escritor, sheet_name=nombre_hoja, index=False)
        hoja = escritor.sheets[nombre_hoja]
        from openpyxl.styles import Font, PatternFill, Alignment
        for celda in hoja[1]:
            celda.font = Font(bold=True, color="FFFFFF")
            celda.fill = PatternFill("solid", fgColor="17365D")
            celda.alignment = Alignment(wrap_text=True)
        for columna in hoja.columns:
            letra = columna[0].column_letter
            largo = max(len(str(c.value or "")) for c in columna)
            hoja.column_dimensions[letra].width = min(max(largo + 3, 14), 65)
        hoja.freeze_panes = "A2"
    return salida.getvalue()



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
    """

    numero = f"{float(valor):,.{decimales}f}"

    return (
        numero.replace(",", "TEMP")
        .replace(".", ",")
        .replace("TEMP", ".")
    )


def redondear_dos_decimales(valor):
    """
    Redondea una masa a dos decimales para su utilización
    en el cálculo de eficiencia de corriente.

    Se utiliza ROUND_HALF_UP para establecer un criterio
    explícito de redondeo decimal.
    """

    return float(
        Decimal(str(valor)).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )
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

    Las dos masas se redondean a dos decimales
    ANTES de realizar la división.

    Ejemplo:
    m_real = 0.88 g
    m_F = 0.99 g

    eficiencia = (0.88 / 0.99) * 100
    eficiencia = 88.89 %
    """

    if masa_real_g is None or masa_teorica_g is None:
        return None

    masa_real_2d = redondear_dos_decimales(masa_real_g)
    masa_teorica_2d = redondear_dos_decimales(masa_teorica_g)

    if masa_teorica_2d <= 0:
        return None

    eficiencia = (
        masa_real_2d
        / masa_teorica_2d
        * 100.0
    )

    return redondear_dos_decimales(eficiencia)


def calcular_deposito_laboratorio(
    densidad_corriente,
    area_catodica,
    tiempo_segundos,
    masa_molar=63.546,
    electrones=2,
    intensidad_manual=None,
    masa_inicial_g=None,
    masa_final_g=None,
    masa_lamina_g=None
):
    """
    Calcula los resultados de un ensayo de laboratorio.

    Permite:
    - Calcular la intensidad mediante j * A.
    - Utilizar una intensidad manual.
    - Determinar la masa teórica por Faraday.
    - Calcular la masa real experimental.
    - Utilizar la masa de una lámina depositada.
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

    if masa_lamina_g is not None:
        masa_real_g = masa_lamina_g

    elif (
        masa_inicial_g is not None
        and masa_final_g is not None
    ):
        masa_real_g = calcular_masa_real(
            masa_inicial_g,
            masa_final_g
        )

    if masa_real_g is not None:
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
        "masa_lamina_g": masa_lamina_g,
        "masa_real_g": masa_real_g,
        "eficiencia_corriente": eficiencia_experimental,
    }


# ============================================================
# 1. FUNDAMENTOS DE ELECTROOBTENCIÓN
# ============================================================

def mostrar_fundamentos_ew():
    st.title("⚡ Fundamentos de Electroobtención")

    st.write(
        "La electroobtención (EW) es un proceso electroquímico que permite recuperar "
        "cobre desde una solución electrolítica mediante la aplicación de corriente "
        "eléctrica continua. Los iones de cobre se reducen y se depositan como "
        "cobre metálico sobre el cátodo."
    )

    st.header("1. Fundamentos electroquímicos")
    st.write(
        "La electroobtención se fundamenta en reacciones de oxidación y reducción "
        "(redox), que implican transferencia de electrones. La electrólisis utiliza "
        "una diferencia de potencial externa para impulsar reacciones no espontáneas."
    )
    st.markdown("**Oxidación:** pérdida de electrones.")
    st.latex(r"Cu_{(s)} \rightarrow Cu^{2+}_{(ac)} + 2e^-")
    st.markdown("**Reducción:** ganancia de electrones.")
    st.latex(r"Cu^{2+}_{(ac)} + 2e^- \rightarrow Cu_{(s)}")
    st.caption(
        "Las dos expresiones anteriores ilustran las semirreacciones generales "
        "de oxidación y reducción del cobre; "
        "no representan por sí solas las dos reacciones de una celda EW convencional."
    )

    st.header("2. Ánodo y cátodo en electroobtención")
    col_anodo, col_catodo = st.columns(2)
    with col_anodo:
        st.markdown("**Ánodo (+): oxidación**")
        st.write(
            "En una celda de electroobtención convencional con ánodos insolubles, "
            "ocurre la oxidación del agua y se libera oxígeno."
        )
        st.latex(r"H_2O \rightarrow \frac{1}{2}O_{2(g)} + 2H^+_{(ac)} + 2e^-")
    with col_catodo:
        st.markdown("**Cátodo (−): reducción**")
        st.write(
            "Los iones de cobre de la solución reciben electrones y forman "
            "un depósito de cobre metálico."
        )
        st.latex(r"Cu^{2+}_{(ac)} + 2e^- \rightarrow Cu_{(s)}")

    st.header("3. Electrolito")
    st.write(
        "El electrolito es una solución que contiene iones móviles y permite "
        "el transporte de corriente eléctrica mediante movimiento iónico. "
        "Su composición influye en la conductividad, la eficiencia de corriente "
        "y la calidad del depósito catódico."
    )
    st.markdown("**Composición referencial del electrolito:**")
    st.dataframe(
        pd.DataFrame({
            "Componente": ["Ácido sulfúrico (H₂SO₄)", "Cobre (Cu²⁺)",
                           "Hierro (Fe²⁺/Fe³⁺)", "Cloruro (Cl⁻)", "Arsénico (As)"],
            "Concentración": ["150–200 g/L", "35–45 g/L", "< 2 g/L",
                              "< 30 g/L", "< 5 g/L"],
            "Observación": ["Acidez", "Metal de interés", "Impureza",
                            "Impureza", "Impureza"]
        }),
        hide_index=True,
        use_container_width=True
    )
    st.caption(
        "Los valores indicados son referenciales; "
        "no se presentan como límites universales de operación."
    )
    st.markdown(
        "- **Conductividad:** una conductividad elevada disminuye la resistencia eléctrica.\n"
        "- **Concentración de Cu²⁺:** influye en la disponibilidad de cobre y en la morfología del depósito.\n"
        "- **Impurezas:** pueden perjudicar la pureza y la calidad del cátodo."
    )

    st.header("4. Electrólisis y tipos de celdas")
    st.write(
        "La electrólisis es un proceso electroquímico no espontáneo que consume "
        "energía eléctrica para producir transformaciones químicas. En EW se "
        "utilizan celdas electrolíticas con ánodos, cátodos y una solución conductora."
    )
    st.table(pd.DataFrame({
        "Característica": ["Reacción redox", "Electricidad", "Ánodo",
                           "Cátodo", "Transformación de energía"],
        "Celda galvánica": ["Espontánea", "Genera", "Negativo (oxidación)",
                             "Positivo (reducción)", "Química → eléctrica"],
        "Celda electrolítica": ["No espontánea", "Consume", "Positivo (oxidación)",
                                "Negativo (reducción)", "Eléctrica → química"]
    }))

    st.header("5. Variables operacionales")
    st.markdown(
        "- **Intensidad de corriente (A):** influye en la masa teórica que puede depositarse.\n"
        "- **Densidad de corriente (A/m²):** relaciona la intensidad con el área catódica activa.\n"
        "- **Voltaje de celda (V):** diferencia de potencial necesaria para sostener el proceso.\n"
        "- **Concentraciones de cobre y ácido sulfúrico:** afectan la disponibilidad de iones y las propiedades del electrolito.\n"
        "- **Impurezas:** pueden alterar la calidad del depósito.\n"
        "- **Temperatura:** modifica la conductividad, la viscosidad y la transferencia de masa.\n"
        "- **Circulación del electrolito y distribución de corriente:** influyen en la uniformidad del depósito."
    )

    st.header("6. Potencial estándar de reducción")
    st.write(
        "El potencial estándar de reducción expresa la tendencia de una especie "
        "a ganar electrones bajo condiciones estándar. Se mide respecto del "
        "electrodo estándar de hidrógeno, cuyo potencial es 0,00 V."
    )
    st.latex(r"E^\circ_{\mathrm{celda}} = E^\circ_{\mathrm{cátodo}} - E^\circ_{\mathrm{ánodo}}")
    st.write(
        "Un potencial de reducción más positivo indica una mayor tendencia relativa "
        "a reducirse; uno más negativo indica una menor tendencia relativa. "
        "Los potenciales estándar no describen por sí solos el comportamiento "
        "real de una celda, que también depende de temperatura, concentración "
        "y fenómenos superficiales."
    )

    st.header("7. Intensidad y densidad de corriente")
    st.write(
        "La intensidad de corriente es la cantidad de carga que circula por unidad "
        "de tiempo. La densidad de corriente relaciona esta intensidad con "
        "la superficie catódica activa."
    )
    st.latex(r"I = j \cdot A")
    st.latex(r"j = \frac{I}{A}")
    st.caption("I: intensidad (A); j: densidad de corriente (A/m²); A: área catódica activa (m²).")
    st.write(
        "Una densidad de corriente excesiva respecto de las condiciones de "
        "transferencia de masa puede favorecer depósitos irregulares."
    )

    st.header("8. Ley de Faraday y masa depositada")
    st.write(
        "La primera ley de Faraday establece que la masa depositada es proporcional "
        "a la carga eléctrica que circula. Permite estimar la masa teórica "
        "de cobre depositable a partir de la intensidad, el tiempo y las "
        "propiedades electroquímicas del metal."
    )
    st.latex(r"m_F = \frac{I \cdot t \cdot M}{n \cdot F}")
    st.markdown(
        "**Donde:** m_F es la masa teórica (g); I, la intensidad (A); "
        "t, el tiempo (s); M, la masa molar (g/mol); n, el número de electrones; "
        "y F, la constante de Faraday (96.485 C/mol de electrones)."
    )
    st.write(
        "La masa experimental corresponde al metal efectivamente depositado. "
        "Puede determinarse por diferencia entre la masa final y la inicial "
        "del cátodo, después de su limpieza y secado."
    )
    st.latex(r"m_{\mathrm{real}} = m_f - m_i")
    st.latex(r"\eta = \frac{m_{\mathrm{real}}}{m_F} \times 100\%")
    st.info(
        "La masa farádica es un valor teórico. La eficiencia de corriente "
        "permite comparar la masa realmente obtenida con la masa calculada "
        "mediante la ley de Faraday."
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

        # CORRECCIÓN:
        # La densidad de corriente comienza en 0,00.

        densidad_corriente = st.number_input(
            "Densidad de corriente (j) [A/m²]",
            min_value=0.0,
            value=0.0,
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

            # CORRECCIÓN:
            # El área en m² comienza en 0,00.

            area_ingresada = st.number_input(
                "Área catódica (A) [m²]",
                min_value=0.0,
                value=0.0,
                step=0.01,
                format="%.2f",
                key="ew_lab_area_m2"
            )

            area_m2 = area_ingresada

        else:

            # CORRECCIÓN:
            # El área en cm² comienza en 0,00.

            area_ingresada = st.number_input(
                "Área catódica (A) [cm²]",
                min_value=0.0,
                value=0.0,
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

    info1, info2, info3 = st.columns(3)

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

    with info3:

        st.metric(
            "Constante de Faraday",
            f"{formatear_numero(CONSTANTE_FARADAY)} C/mol e⁻"
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
        "Puede determinarse mediante la diferencia "
        "entre la masa final y la masa inicial "
        "del cátodo, o mediante la medición directa "
        "de la masa de la lámina metálica obtenida."
    )

    # --------------------------------------------------------
    # MÉTODO PARA DETERMINAR LA MASA REAL
    # --------------------------------------------------------

    st.markdown("### ⚖️ Método de Medición")

    metodo_masa_real = st.radio(
        "Selecciona cómo se determinó la masa real",
        options=[
            "Diferencia entre masa final e inicial del cátodo",
            "Masa directa de la lámina depositada"
        ],
        index=0,
        key="ew_lab_metodo_masa_real"
    )

    if metodo_masa_real == (
        "Diferencia entre masa final e inicial del cátodo"
    ):

        st.latex(
            r"m_{\mathrm{real}} = m_f - m_i"
        )

        st.write(
            "Se utiliza la diferencia entre la masa "
            "final y la masa inicial del cátodo."
        )

        origen_masa_real = "Diferencia de masas del cátodo"

    else:

        st.latex(
            r"m_{\mathrm{real}} = m_{\mathrm{lámina}}"
        )

        st.write(
            "Se utiliza directamente la masa de la "
            "lámina metálica obtenida durante el ensayo."
        )

        origen_masa_real = "Medición directa de la lámina"

    st.markdown("### ⚖️ Mediciones Experimentales")

    unidad_masa = st.selectbox(
        "Unidad de medida de las masas",
        options=["g", "kg"],
        index=0,
        key="ew_lab_unidad_masa"
    )

    factor_masa = 1000.0 if unidad_masa == "kg" else 1.0

    masa_inicial = None
    masa_final = None
    masa_lamina = None

    masa_inicial_g = None
    masa_final_g = None
    masa_lamina_g = None

    masa_real = None
    mediciones_validas = False

    # --------------------------------------------------------
    # MÉTODO A: DIFERENCIA DE MASAS DEL CÁTODO
    # --------------------------------------------------------

    if metodo_masa_real == (
        "Diferencia entre masa final e inicial del cátodo"
    ):

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

        masa_inicial_g = masa_inicial * factor_masa
        masa_final_g = masa_final * factor_masa

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

        elif not masas_ingresadas:

            st.info(
                "Ingresa la masa inicial y la masa final "
                "del cátodo para calcular la masa real."
            )

    # --------------------------------------------------------
    # MÉTODO B: MASA DIRECTA DE LA LÁMINA
    # --------------------------------------------------------

    else:

        masa_lamina = st.number_input(
            f"Masa de la lámina depositada [{unidad_masa}]",
            min_value=0.0,
            value=0.0,
            step=0.01,
            format="%.2f",
            key=f"ew_lab_masa_lamina_{unidad_masa}"
        )

        masa_lamina_g = masa_lamina * factor_masa

        mediciones_validas = masa_lamina > 0

        if mediciones_validas:

            masa_real = masa_lamina_g

        else:

            st.info(
                "Ingresa la masa de la lámina metálica "
                "obtenida experimentalmente para "
                "determinar la masa real depositada."
            )

    # --------------------------------------------------------
    # RESULTADO DE MASA REAL
    # --------------------------------------------------------

    if mediciones_validas:

        st.markdown("### 📊 Resultado de Masa Real")

        st.markdown(
            tarjeta_resultado(
                titulo="🧪 Masa Real Depositada",
                valor=formatear_numero(masa_real),
                unidad="gramos (g)",
                color="#38bdf8",
                descripcion=origen_masa_real
            ),
            unsafe_allow_html=True
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

    # --------------------------------------------------------
    # SELECCIÓN DEL ORIGEN DE LAS MASAS
    # --------------------------------------------------------

    st.markdown("### 📥 Selección de Datos para la Eficiencia")

    st.write(
        "Puedes utilizar los resultados calculados "
        "en los puntos anteriores o ingresar otros "
        "valores de masa teórica y masa real."
    )

    eficiencia_col1, eficiencia_col2 = st.columns(2)

    with eficiencia_col1:

        modo_masa_teorica = st.radio(
            "Masa teórica a utilizar",
            options=[
                "Utilizar masa teórica calculada en el punto 2",
                "Ingresar otra masa teórica"
            ],
            index=0,
            key="ew_lab_modo_masa_teorica_eficiencia"
        )

    with eficiencia_col2:

        modo_masa_real = st.radio(
            "Masa real a utilizar",
            options=[
                "Utilizar masa real calculada en el punto 3",
                "Ingresar otra masa real"
            ],
            index=0,
            key="ew_lab_modo_masa_real_eficiencia"
        )

    # --------------------------------------------------------
    # MASA TEÓRICA PARA EFICIENCIA
    # --------------------------------------------------------

    if modo_masa_teorica == (
        "Utilizar masa teórica calculada en el punto 2"
    ):

        masa_teorica_eficiencia = masa_teorica

        origen_masa_teorica_eficiencia = (
            "Calculada en el punto 2"
        )

        st.info(
            "Masa teórica seleccionada: "
            f"{formatear_numero(masa_teorica_eficiencia)} g."
        )

    else:

        masa_teorica_eficiencia = st.number_input(
            "Masa teórica para eficiencia [g]",
            min_value=0.0,
            value=0.0,
            step=0.01,
            format="%.2f",
            key="ew_lab_masa_teorica_manual_eficiencia"
        )

        origen_masa_teorica_eficiencia = (
            "Ingresada manualmente"
        )

    # --------------------------------------------------------
    # MASA REAL PARA EFICIENCIA
    # --------------------------------------------------------

    if modo_masa_real == (
        "Utilizar masa real calculada en el punto 3"
    ):

        masa_real_eficiencia = masa_real

        origen_masa_real_eficiencia = (
            "Calculada en el punto 3"
        )

        if masa_real_eficiencia is not None:

            st.info(
                "Masa real seleccionada: "
                f"{formatear_numero(masa_real_eficiencia)} g."
            )

        else:

            st.info(
                "Todavía no hay una masa real disponible "
                "en el punto 3. Ingresa las mediciones "
                "correspondientes o selecciona la opción "
                "de ingresar otra masa real."
            )

    else:

        masa_real_eficiencia = st.number_input(
            "Masa real para eficiencia [g]",
            min_value=0.0,
            value=0.0,
            step=0.01,
            format="%.2f",
            key="ew_lab_masa_real_manual_eficiencia"
        )

        origen_masa_real_eficiencia = (
            "Ingresada manualmente"
        )

    # --------------------------------------------------------
    # CÁLCULO DE EFICIENCIA
    # --------------------------------------------------------

    eficiencia_experimental = None

    # Se redondean las masas a dos decimales antes
    # de realizar el cálculo de eficiencia.

    masa_teorica_eficiencia_2d = (
        redondear_dos_decimales(masa_teorica_eficiencia)
        if masa_teorica_eficiencia is not None
        else None
    )

    masa_real_eficiencia_2d = (
        redondear_dos_decimales(masa_real_eficiencia)
        if masa_real_eficiencia is not None
        else None
    )

    datos_eficiencia_validos = (
        masa_teorica_eficiencia_2d is not None
        and masa_teorica_eficiencia_2d > 0
        and masa_real_eficiencia_2d is not None
    )

    if datos_eficiencia_validos:

        eficiencia_experimental = calcular_eficiencia_corriente(
            masa_real_g=masa_real_eficiencia_2d,
            masa_teorica_g=masa_teorica_eficiencia_2d
        )

        st.markdown("### 📊 Resultado de Eficiencia")

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
                    "y la masa teórica seleccionadas"
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
                "a partir de las masas seleccionadas."
            )

    else:

        if (
            masa_teorica_eficiencia_2d is None
            or masa_teorica_eficiencia_2d <= 0
        ):

            st.warning(
                "Para calcular la eficiencia debes "
                "disponer de una masa teórica "
                "mayor que cero después de redondearla "
                "a dos decimales."
            )

        if masa_real_eficiencia_2d is None:

            st.info(
                "Para obtener la eficiencia experimental, "
                "primero debes ingresar una masa real "
                "en el punto 3 o seleccionar la opción "
                "de ingresar otra masa real."
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
            "Parámetro": "Constante de Faraday",
            "Valor": formatear_numero(CONSTANTE_FARADAY),
            "Unidad": "C/mol e⁻"
        },
        {
            "Parámetro": "Masa teórica depositada",
            "Valor": formatear_numero(masa_teorica),
            "Unidad": "g"
        },
        {
            "Parámetro": "Método de medición de masa real",
            "Valor": origen_masa_real,
            "Unidad": "—"
        },
    ]

    # --------------------------------------------------------
    # FILAS SEGÚN EL MÉTODO DE MASA REAL
    # --------------------------------------------------------

    if metodo_masa_real == (
        "Diferencia entre masa final e inicial del cátodo"
    ):

        datos_tabla.extend([
            {
                "Parámetro": "Masa inicial del cátodo",
                "Valor": (
                    formatear_numero(masa_inicial)
                    if mediciones_validas
                    else "Pendiente"
                ),
                "Unidad": unidad_masa
            },
            {
                "Parámetro": "Masa final del cátodo",
                "Valor": (
                    formatear_numero(masa_final)
                    if mediciones_validas
                    else "Pendiente"
                ),
                "Unidad": unidad_masa
            },
        ])

    else:

        datos_tabla.append({
            "Parámetro": "Masa de la lámina depositada",
            "Valor": (
                formatear_numero(masa_lamina)
                if mediciones_validas
                else "Pendiente"
            ),
            "Unidad": unidad_masa
        })

    # --------------------------------------------------------
    # RESULTADOS FINALES DE MASA Y EFICIENCIA
    # --------------------------------------------------------

    datos_tabla.extend([
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
            "Parámetro": "Origen masa teórica para eficiencia",
            "Valor": origen_masa_teorica_eficiencia,
            "Unidad": "—"
        },
        {
            "Parámetro": "Masa teórica utilizada en eficiencia",
            "Valor": (
                formatear_numero(masa_teorica_eficiencia_2d)
                if masa_teorica_eficiencia_2d is not None
                else "Pendiente"
            ),
            "Unidad": "g"
        },
        {
            "Parámetro": "Origen masa real para eficiencia",
            "Valor": origen_masa_real_eficiencia,
            "Unidad": "—"
        },
        {
            "Parámetro": "Masa real utilizada en eficiencia",
            "Valor": (
                formatear_numero(masa_real_eficiencia_2d)
                if masa_real_eficiencia_2d is not None
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
    ])

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

    st.download_button(
        "📥 Exportar resultados de electrodeposición a Excel",
        data=_excel_desde_tabla(tabla_resultados, "Electrodeposición"),
        file_name="resultados_electrodeposicion.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="ew_exportar_excel",
        use_container_width=True,
    )

    st.info(
        "La masa teórica se obtiene mediante "
        "la Ley de Faraday. La masa real puede "
        "determinarse mediante la diferencia "
        "de masas del cátodo o mediante la "
        "medición directa de la lámina depositada. "
        "Para calcular la eficiencia experimental "
        "pueden utilizarse los resultados anteriores "
        "o valores ingresados manualmente. "
        "No se utiliza una eficiencia de corriente supuesta."
    )

    st.caption(
        "Los resultados corresponden a un ensayo "
        "de laboratorio. Se supone una intensidad "
        "de corriente constante y que la masa "
        "registrada corresponde al metal "
        "seleccionado. Las mediciones deben "
        "realizarse sobre un cátodo o una lámina "
        "adecuadamente lavados y secos."
    )


    # ========================================================
    # 6. EXPLICACIÓN DEL RESULTADO CON IA
    # ========================================================

    st.markdown("---")
    st.header("6. 🤖 Explicación del resultado con IA")
    st.write(
        "Solicita al asistente metalúrgico una interpretación "
        "de los resultados de electrodeposición calculados."
    )

    if st.button(
        "🤖 Explicar resultado con IA",
        key="ew_lab_explicar_resultado_ia",
        use_container_width=True
    ):
        from modulos.asistente import (
            obtener_api_key,
            generar_respuesta,
            interpretar_error
        )

        api_key = obtener_api_key()

        if not api_key:
            st.error("No se encontró la clave API de Gemini.")
            st.info(
                "Configura GEMINI_API_KEY en "
                ".streamlit/secrets.toml para activar la explicación."
            )
        else:
            pregunta_ia = (
                "Organiza obligatoriamente la respuesta en cuatro apartados, "
                "en este orden: 1. Resultados; 2. Explicación metalúrgica; "
                "3. Análisis técnico; 4. Recomendaciones. "
                "No añadas apartados adicionales ni inventes mediciones. "
                "Respeta las cifras calculadas y las unidades originales. "
                "Distingue claramente las hipótesis de los datos medidos.\n\n"
                "INSTRUCCIONES ESPECÍFICAS PARA ELECTRODEPOSICIÓN: "
                "En 1. Resultados, incluye metal, densidad de corriente, área, "
                "intensidad realmente utilizada y su origen, tiempo, masa teórica, "
                "método y masa real si existe, y eficiencia experimental solo si fue calculada. "
                "No confundas intensidad calculada con intensidad manual utilizada. "
                "En 2. Explicación metalúrgica, explica la reducción catódica del metal "
                "seleccionado, I=j·A y la ley de Faraday, usando el número de electrones correcto. "
                "En 3. Análisis técnico, compara masa teórica y masa real solo cuando ambas existan; "
                "interpreta la eficiencia tal como la calcula la plataforma, considerando que "
                "las masas se redondean a dos decimales antes de dividir. "
                "No atribuyas diferencias a reacciones secundarias, desprendimiento, "
                "impurezas ni pérdidas de material como hechos comprobados. "
                "En 4. Recomendaciones, propone comprobaciones de área activa, intensidad, "
                "tiempo, limpieza y secado del cátodo, y precisión del pesaje según los datos. "
                "No inventes eficiencia si no hay masa real ni recomiendes consumo energético. "
                "No presentes condiciones industriales como si hubieran sido medidas. "
                "Cuando sea pertinente, menciona precauciones eléctricas y de manejo de electrolitos "
                "dentro de las recomendaciones, sin crear una quinta sección.\n\n"
                "Eres un asistente especializado en electroobtención "
                "y electrodeposición de metales. Explica exclusivamente "
                "los resultados reales de este ensayo, en español, "
                "sin inventar datos ni modificar las cifras. "
                "Usa dos decimales para los resultados numéricos.\n\n"
                f"Metal: {metal_seleccionado}\n"
                f"Densidad de corriente: {densidad_corriente:.2f} A/m²\n"
                f"Área catódica ingresada: {area_ingresada:.2f} {unidad_area}\n"
                f"Área equivalente para cálculo: {area_m2:.8f} m²\n"
                f"Intensidad calculada: {intensidad_calculada:.2f} A\n"
                f"Intensidad usada: {intensidad_utilizada:.2f} A "
                f"({origen_corriente})\n"
                f"Tiempo ingresado: {tiempo_experimental:.2f} {unidad_tiempo}\n"
                f"Tiempo equivalente para cálculo: {tiempo_segundos:.2f} s\n"
                f"Masa molar: {masa_molar:.2f} g/mol\n"
                f"Electrones transferidos: {electrones}\n"
                f"Constante de Faraday: {CONSTANTE_FARADAY:.2f} C/mol\n"
                f"Masa teórica: {masa_teorica:.2f} g\n"
                f"Método de masa real: {origen_masa_real}\n"
                f"Masa real: "
                f"{f'{masa_real:.2f} g' if masa_real is not None else 'No disponible'}\n"
                f"Masa teórica para eficiencia: "
                f"{masa_teorica_eficiencia_2d:.2f} g\n"
                f"Masa real para eficiencia: "
                f"{f'{masa_real_eficiencia_2d:.2f} g' if masa_real_eficiencia_2d is not None else 'No disponible'}\n"
                f"Eficiencia experimental: "
                f"{f'{eficiencia_experimental:.2f} %' if eficiencia_experimental is not None else 'No calculada'}\n\n"
                "Explica I = j·A, la ley de Faraday, la diferencia "
                "entre masa teórica y masa real y, si existe, "
                "la eficiencia experimental. Señala las limitaciones "
                "del ensayo sin asumir datos no proporcionados. "
                "No calcules consumo energético. No interpretes una eficiencia "
                "no calculada como cero ni atribuyas causas a las pérdidas "
                "sin mediciones que lo sustenten."
            )

            indicador_ia = st.empty()
            try:
                respuesta_ia, modelo_ia = generar_respuesta(
                    api_key=api_key,
                    mensajes=[],
                    pregunta=pregunta_ia,
                    indicador=indicador_ia
                )
                st.session_state["ew_lab_ia_respuesta"] = respuesta_ia
                st.session_state["ew_lab_ia_modelo"] = modelo_ia
            except Exception as error:
                st.error(interpretar_error(error))
                with st.expander("Ver detalles del error de IA"):
                    st.code(str(error))

    if st.session_state.get("ew_lab_ia_respuesta"):
        st.markdown("### 🤖 Interpretación del asistente")
        st.markdown(st.session_state["ew_lab_ia_respuesta"])
        if st.session_state.get("ew_lab_ia_modelo"):
            st.caption(
                f"Modelo utilizado: {st.session_state['ew_lab_ia_modelo']}"
            )

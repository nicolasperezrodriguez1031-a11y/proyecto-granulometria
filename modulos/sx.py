import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from html import escape


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def tarjeta_resultado(titulo, valor, unidad, color):
    """Genera una tarjeta de resultados compatible con Streamlit."""

    return (
        f'<div style="background-color:#1e222d;'
        f'padding:20px;border-radius:10px;'
        f'border-left:5px solid {color};'
        f'text-align:center;margin-bottom:12px;'
        f'overflow-wrap:anywhere;">'
        f'<p style="color:#a1aab5;margin:0;'
        f'font-size:0.95rem;">{titulo}</p>'
        f'<h2 style="color:white;margin:8px 0;">'
        f'{valor}</h2>'
        f'<p style="color:{color};margin:0;'
        f'font-weight:bold;">{unidad}</p>'
        f'</div>'
    )


def flujo_cobre(q_m3_h, concentracion_g_l):
    """
    Calcula el flujo másico de cobre en t/h.

    Q [m³/h] * C [g/L] = kg/h

    Para obtener t/h se divide entre 1000.
    """

    return q_m3_h * concentracion_g_l / 1000.0


def flujo_cobre_kg_h(q_m3_h, concentracion_g_l):
    """Calcula el flujo másico de cobre en kg/h."""

    return q_m3_h * concentracion_g_l


def convertir_flujo_masico(valor_kg_h, unidad):
    """Convierte un flujo de kg/h a g/h, kg/h o t/h."""

    if unidad == "g/h":
        return valor_kg_h * 1000.0

    if unidad == "t/h":
        return valor_kg_h / 1000.0

    return valor_kg_h


def formato_numero(valor, decimales=2):
    """Formato numérico con separador de miles."""

    return f"{valor:,.{decimales}f}"


def balance_extraccion(
    q_pls,
    cu_pls,
    q_org,
    cu_org_desc,
    cu_refino
):
    """Balance simplificado de extracción de cobre."""

    cobre_pls = flujo_cobre(q_pls, cu_pls)

    cobre_refino = flujo_cobre(q_pls, cu_refino)

    cobre_transferido = cobre_pls - cobre_refino

    cu_org_cargado = (
        cu_org_desc
        + (q_pls / q_org) * (cu_pls - cu_refino)
    )

    recuperacion = (
        cobre_transferido / cobre_pls * 100.0
        if cobre_pls > 0 else 0.0
    )

    return {
        "cobre_pls": cobre_pls,
        "cobre_refino": cobre_refino,
        "cobre_transferido": cobre_transferido,
        "cu_org_cargado": cu_org_cargado,
        "recuperacion": recuperacion,
        "cierre": (
            cobre_pls
            + flujo_cobre(q_org, cu_org_desc)
            - cobre_refino
            - flujo_cobre(q_org, cu_org_cargado)
        )
    }


def balance_reextraccion(
    q_org,
    cu_org_cargado,
    cu_org_descargado,
    q_electrolito,
    cu_electrolito_pobre
):
    """Balance simplificado de reextracción."""

    cobre_transferido = flujo_cobre(
        q_org,
        cu_org_cargado - cu_org_descargado
    )

    cu_electrolito_rico = (
        cu_electrolito_pobre
        + (q_org / q_electrolito)
        * (cu_org_cargado - cu_org_descargado)
    )

    eficiencia = (
        (cu_org_cargado - cu_org_descargado)
        / cu_org_cargado * 100.0
        if cu_org_cargado > 0 else 0.0
    )

    cierre = (
        flujo_cobre(q_org, cu_org_cargado)
        + flujo_cobre(q_electrolito, cu_electrolito_pobre)
        - flujo_cobre(q_org, cu_org_descargado)
        - flujo_cobre(q_electrolito, cu_electrolito_rico)
    )

    return {
        "cobre_transferido": cobre_transferido,
        "cu_electrolito_rico": cu_electrolito_rico,
        "eficiencia": eficiencia,
        "cierre": cierre
    }


def mostrar_cierre(error):
    """Comprueba el cierre numérico del balance."""

    if abs(error) < 1e-8:

        st.success(
            "Balance de cobre cerrado correctamente."
        )

    else:

        st.error(
            f"El balance presenta una diferencia "
            f"de {error:.8f} t/h."
        )


# ============================================================
# DIAGRAMA INTERACTIVO DE EXTRACCIÓN SX
# ============================================================

def mostrar_diagrama_extraccion(
    q_pls,
    cu_pls,
    q_org,
    cu_org_desc,
    cu_refino,
    cu_org_cargado,
    unidad_masa
):
    """
    Dibuja el diagrama de extracción SX.

    Corrientes:
    - PLS: entrada acuosa.
    - Orgánico descargado: entrada orgánica.
    - Refino: salida acuosa.
    - Orgánico cargado: salida orgánica.

    Los valores se actualizan cuando Streamlit
    vuelve a ejecutar la aplicación.
    """

    corrientes = {
        "pls": {
            "nombre": "PLS",
            "caudal": q_pls,
            "concentracion": cu_pls,
            "color": "#38bdf8"
        },
        "refino": {
            "nombre": "REFINO",
            "caudal": q_pls,
            "concentracion": cu_refino,
            "color": "#60a5fa"
        },
        "organico_descargado": {
            "nombre": "ORGÁNICO DESCARGADO",
            "caudal": q_org,
            "concentracion": cu_org_desc,
            "color": "#fbbf24"
        },
        "organico_cargado": {
            "nombre": "ORGÁNICO CARGADO",
            "caudal": q_org,
            "concentracion": cu_org_cargado,
            "color": "#34d399"
        }
    }

    for corriente in corrientes.values():

        masa_kg_h = flujo_cobre_kg_h(
            corriente["caudal"],
            corriente["concentracion"]
        )

        corriente["masa"] = convertir_flujo_masico(
            masa_kg_h,
            unidad_masa
        )

    def tarjeta_svg(clave, x, y, ancho=270, alto=130):

        corriente = corrientes[clave]

        nombre = escape(corriente["nombre"])
        color = corriente["color"]

        caudal = formato_numero(corriente["caudal"])
        concentracion = formato_numero(
            corriente["concentracion"]
        )
        masa = formato_numero(corriente["masa"])

        return f"""
        <g class="corriente">
            <rect
                x="{x}"
                y="{y}"
                width="{ancho}"
                height="{alto}"
                rx="12"
                fill="#1d2430"
                stroke="{color}"
                stroke-width="2"
            />

            <rect
                x="{x}"
                y="{y}"
                width="{ancho}"
                height="35"
                rx="12"
                fill="{color}"
                fill-opacity="0.14"
            />

            <text
                x="{x + ancho / 2}"
                y="{y + 23}"
                text-anchor="middle"
                fill="{color}"
                font-size="15"
                font-weight="bold"
            >
                {nombre}
            </text>

            <text
                x="{x + 15}"
                y="{y + 58}"
                fill="#e5e7eb"
                font-size="14"
            >
                Caudal: {caudal} m³/h
            </text>

            <text
                x="{x + 15}"
                y="{y + 85}"
                fill="#e5e7eb"
                font-size="14"
            >
                Cu: {concentracion} g/L
            </text>

            <text
                x="{x + 15}"
                y="{y + 112}"
                fill="#ffffff"
                font-size="14"
                font-weight="bold"
            >
                Masa Cu: {masa} {unidad_masa}
            </text>

            <title>
                {nombre}
                Caudal: {caudal} m³/h
                Concentración: {concentracion} g/L
                Flujo másico: {masa} {unidad_masa}
            </title>
        </g>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="utf-8">

        <style>
            html, body {{
                margin: 0;
                padding: 0;
                background: transparent;
                font-family: Arial, sans-serif;
            }}

            .contenedor {{
                width: 100%;
                background: #111722;
                border: 1px solid #303948;
                border-radius: 14px;
                padding: 12px;
                box-sizing: border-box;
                overflow-x: auto;
            }}

            svg {{
                display: block;
                width: 100%;
                min-width: 780px;
                height: auto;
            }}

            .corriente {{
                cursor: help;
                transition: opacity 0.2s;
            }}

            .corriente:hover {{
                opacity: 0.78;
            }}

            .flecha {{
                fill: none;
                stroke-width: 3;
                stroke-linecap: round;
                stroke-linejoin: round;
            }}
        </style>
    </head>

    <body>
        <div class="contenedor">

            <svg
                viewBox="0 0 900 440"
                xmlns="http://www.w3.org/2000/svg"
                role="img"
                aria-label="Diagrama de extracción por solventes"
            >

                <defs>
                    <marker
                        id="flechaAzul"
                        viewBox="0 0 10 10"
                        refX="9"
                        refY="5"
                        markerWidth="7"
                        markerHeight="7"
                        orient="auto-start-reverse"
                    >
                        <path
                            d="M 0 0 L 10 5 L 0 10 z"
                            fill="#38bdf8"
                        />
                    </marker>

                    <marker
                        id="flechaAmarilla"
                        viewBox="0 0 10 10"
                        refX="9"
                        refY="5"
                        markerWidth="7"
                        markerHeight="7"
                        orient="auto-start-reverse"
                    >
                        <path
                            d="M 0 0 L 10 5 L 0 10 z"
                            fill="#fbbf24"
                        />
                    </marker>

                    <marker
                        id="flechaVerde"
                        viewBox="0 0 10 10"
                        refX="9"
                        refY="5"
                        markerWidth="7"
                        markerHeight="7"
                        orient="auto-start-reverse"
                    >
                        <path
                            d="M 0 0 L 10 5 L 0 10 z"
                            fill="#34d399"
                        />
                    </marker>
                </defs>

                <!-- CORRIENTES SUPERIORES -->

                {tarjeta_svg("pls", 20, 15)}

                {tarjeta_svg("refino", 610, 15)}

                <!-- CORRIENTES INFERIORES -->

                {tarjeta_svg(
                    "organico_descargado", 20, 295
                )}

                {tarjeta_svg(
                    "organico_cargado", 610, 295
                )}

                <!-- EQUIPO CENTRAL -->

                <rect
                    x="325"
                    y="170"
                    width="250"
                    height="100"
                    rx="14"
                    fill="#343c49"
                    stroke="#e5e7eb"
                    stroke-width="2"
                />

                <text
                    x="450"
                    y="209"
                    text-anchor="middle"
                    fill="#ffffff"
                    font-size="22"
                    font-weight="bold"
                >
                    EXTRACCIÓN
                </text>

                <text
                    x="450"
                    y="235"
                    text-anchor="middle"
                    fill="#cbd5e1"
                    font-size="14"
                >
                    Transferencia de Cu
                </text>

                <!-- PLS HACIA EXTRACCIÓN -->

                <path
                    class="flecha"
                    d="M 155 145 V 200 H 325"
                    stroke="#38bdf8"
                    marker-end="url(#flechaAzul)"
                />

                <!-- EXTRACCIÓN HACIA REFINO -->

                <path
                    class="flecha"
                    d="M 575 200 H 745 V 145"
                    stroke="#38bdf8"
                    marker-end="url(#flechaAzul)"
                />

                <!-- ORGÁNICO DESCARGADO HACIA EXTRACCIÓN -->

                <path
                    class="flecha"
                    d="M 155 295 V 245 H 325"
                    stroke="#fbbf24"
                    marker-end="url(#flechaAmarilla)"
                />

                <!-- EXTRACCIÓN HACIA ORGÁNICO CARGADO -->

                <path
                    class="flecha"
                    d="M 575 245 H 745 V 295"
                    stroke="#34d399"
                    marker-end="url(#flechaVerde)"
                />

            </svg>
        </div>
    </body>
    </html>
    """

    components.html(
        html,
        height=485,
        scrolling=True
    )


# ============================================================
# CALCULADORA FA/FO INDEPENDIENTE
# ============================================================

def calcular_fa_fo(volumen_total, razon_fa_fo):
    """
    Calcula los volúmenes acuoso y orgánico.

    FA/FO = Va/Vo

    Vt = Va + Vo

    Vo = Vt / (1 + FA/FO)

    Va = Vt - Vo
    """

    volumen_organico = (
        volumen_total / (1.0 + razon_fa_fo)
    )

    volumen_acuoso = (
        volumen_total - volumen_organico
    )

    porcentaje_acuoso = (
        volumen_acuoso / volumen_total * 100.0
    )

    porcentaje_organico = (
        volumen_organico / volumen_total * 100.0
    )

    return {
        "volumen_acuoso": volumen_acuoso,
        "volumen_organico": volumen_organico,
        "porcentaje_acuoso": porcentaje_acuoso,
        "porcentaje_organico": porcentaje_organico,
        "volumen_total": volumen_total,
        "razon": razon_fa_fo
    }


def mostrar_calculadora_fa_fo():

    st.subheader(
        "🧪 Calculadora de Razón de Flujo FA/FO"
    )

    st.write(
        "Calcula los volúmenes de fase acuosa (FA) "
        "y fase orgánica (FO) necesarios para preparar "
        "una mezcla de extracción por solventes, "
        "a partir del volumen total y la razón FA/FO."
    )

    # --------------------------------------------------------
    # 1. FUNDAMENTO
    # --------------------------------------------------------

    st.markdown(
        "### 1. Fundamento de la Razón de Flujo"
    )

    st.latex(
        r"\frac{FA}{FO} = \frac{V_a}{V_o}"
    )

    st.write(
        "Donde FA corresponde a la fase acuosa, "
        "FO a la fase orgánica, Va al volumen acuoso "
        "y Vo al volumen orgánico."
    )

    st.latex(
        r"V_T = V_a + V_o"
    )

    st.markdown("---")

    # --------------------------------------------------------
    # 2. INGRESO DE PARÁMETROS
    # --------------------------------------------------------

    st.markdown(
        "### 2. Parámetros de Operación"
    )

    col1, col2 = st.columns(2)

    with col1:

        volumen_total = st.number_input(
            "Volumen total de la mezcla",
            min_value=0.01,
            value=500.0,
            step=10.0,
            format="%.2f",
            key="sx_fafo_volumen_total"
        )

        unidad = st.selectbox(
            "Unidad de volumen",
            ["mL", "L", "m³"],
            key="sx_fafo_unidad"
        )

    with col2:

        razon_fa_fo = st.number_input(
            "Razón de flujo FA/FO",
            min_value=0.01,
            value=0.80,
            step=0.05,
            format="%.2f",
            key="sx_fafo_razon"
        )

        st.caption(
            "Ejemplo: una razón FA/FO de 0,80 "
            "significa que por cada 1,00 unidad "
            "de volumen orgánico existen 0,80 "
            "unidades de volumen acuoso."
        )

    # --------------------------------------------------------
    # CÁLCULOS
    # --------------------------------------------------------

    resultados = calcular_fa_fo(
        volumen_total,
        razon_fa_fo
    )

    va = resultados["volumen_acuoso"]
    vo = resultados["volumen_organico"]

    porcentaje_a = resultados["porcentaje_acuoso"]
    porcentaje_o = resultados["porcentaje_organico"]

    st.markdown("---")

    # --------------------------------------------------------
    # 3. RESULTADOS FA/FO
    # --------------------------------------------------------

    st.markdown(
        "### 3. Resultados FA/FO"
    )

    col_a, col_o = st.columns(2)

    with col_a:

        st.markdown(
            tarjeta_resultado(
                "Volumen de Fase Acuosa (FA)",
                f"{va:.2f}",
                unidad,
                "#3b82f6"
            ),
            unsafe_allow_html=True
        )

    with col_o:

        st.markdown(
            tarjeta_resultado(
                "Volumen de Fase Orgánica (FO)",
                f"{vo:.2f}",
                unidad,
                "#10b981"
            ),
            unsafe_allow_html=True
        )

    st.success(
        f"Para preparar {volumen_total:.2f} {unidad} "
        f"de mezcla con una razón FA/FO de "
        f"{razon_fa_fo:.2f}, se requieren "
        f"{va:.2f} {unidad} de fase acuosa "
        f"y {vo:.2f} {unidad} de fase orgánica."
    )

    # --------------------------------------------------------
    # 4. DISTRIBUCIÓN DE FASES
    # --------------------------------------------------------

    st.markdown("---")

    st.markdown(
        "### 4. Distribución de Fases"
    )

    tabla_fases = pd.DataFrame({
        "Fase": [
            "Fase Acuosa (FA)",
            "Fase Orgánica (FO)",
            "Total"
        ],
        f"Volumen [{unidad}]": [
            va,
            vo,
            volumen_total
        ],
        "Porcentaje [%]": [
            porcentaje_a,
            porcentaje_o,
            100.0
        ]
    })

    st.dataframe(
        tabla_fases.style.format({
            f"Volumen [{unidad}]": "{:.2f}",
            "Porcentaje [%]": "{:.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Esta calculadora determina proporciones "
        "volumétricas de ambas fases. Se supone "
        "aditividad de volúmenes, sin contracción, "
        "pérdidas ni arrastres. La razón FA/FO "
        "no permite por sí sola determinar "
        "la eficiencia de extracción de cobre."
    )


# ============================================================
# MÓDULO PRINCIPAL SX
# ============================================================

def mostrar_sx():

    st.title(
        "🧲 Extracción por Solventes (SX)"
    )

    st.write(
        "Selecciona la etapa específica del circuito "
        "de extracción por solventes para realizar "
        "balances y cálculos operacionales."
    )

    sub_sx = st.radio(
        "Selecciona el sub-módulo de SX:",
        [
            "Extracción",
            "Re-extracción",
            "Circuito Completo"
        ],
        horizontal=True
    )

    st.markdown("---")

    # ========================================================
    # 1. EXTRACCIÓN
    # ========================================================

    if sub_sx == "Extracción":

        st.subheader(
            "💧 Módulo de Extracción (Extraction)"
        )

        st.write(
            "Calcula la transferencia de cobre desde "
            "la solución rica (PLS) hacia la fase "
            "orgánica mediante un reactivo extractante."
        )

        st.latex(
            r"Cu^{2+}_{(ac)} + 2RH_{(org)}"
            r"\rightleftharpoons "
            r"CuR_{2(org)} + 2H^+_{(ac)}"
        )

        # ====================================================
        # 1. PARÁMETROS DE OPERACIÓN
        # ====================================================

        st.markdown(
            "### 1. Parámetros de Operación"
        )

        st.write(
            "Ingresa los caudales y las concentraciones "
            "de cobre de las corrientes de alimentación "
            "y salida del proceso de extracción."
        )

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("**Fase acuosa**")

            pls_flow = st.number_input(
                "Caudal de PLS [m³/h]",
                min_value=0.1,
                value=500.0,
                step=10.0,
                format="%.2f",
                key="sx_ex_q_pls"
            )

            cu_pls = st.number_input(
                "Concentración Cu en PLS [g/L]",
                min_value=0.01,
                value=4.50,
                step=0.1,
                format="%.2f",
                key="sx_ex_cu_pls"
            )

            cu_raff = st.number_input(
                "Concentración Cu en Refino [g/L]",
                min_value=0.0,
                value=0.15,
                step=0.01,
                format="%.2f",
                key="sx_ex_cu_refino"
            )

        with col2:

            st.markdown("**Fase orgánica**")

            org_flow = st.number_input(
                "Caudal de Orgánico [m³/h]",
                min_value=0.1,
                value=400.0,
                step=10.0,
                format="%.2f",
                key="sx_ex_q_org"
            )

            cu_org_desc = st.number_input(
                "Cu en Orgánico Descargado [g/L]",
                min_value=0.0,
                value=0.50,
                step=0.1,
                format="%.2f",
                key="sx_ex_cu_org_desc"
            )

            unidad_masa = st.selectbox(
                "Unidad de masa de cobre transportada",
                ["kg/h", "t/h", "g/h"],
                index=0,
                key="sx_ex_unidad_masa"
            )

        if cu_raff > cu_pls:

            st.error(
                "La concentración de cobre del refino "
                "no puede superar la del PLS en este "
                "modelo de extracción."
            )

            return

        # ====================================================
        # CÁLCULOS DEL BALANCE
        # ====================================================

        resultados = balance_extraccion(
            pls_flow,
            cu_pls,
            org_flow,
            cu_org_desc,
            cu_raff
        )

        cu_org_cargado = resultados[
            "cu_org_cargado"
        ]

        # Flujos másicos de cobre en kg/h

        masa_pls = flujo_cobre_kg_h(
            pls_flow,
            cu_pls
        )

        masa_refino = flujo_cobre_kg_h(
            pls_flow,
            cu_raff
        )

        masa_org_desc = flujo_cobre_kg_h(
            org_flow,
            cu_org_desc
        )

        masa_org_cargado = flujo_cobre_kg_h(
            org_flow,
            cu_org_cargado
        )

        masa_entrada = (
            masa_pls + masa_org_desc
        )

        masa_salida = (
            masa_refino + masa_org_cargado
        )

        masa_transferida = (
            masa_pls - masa_refino
        )

        # ====================================================
        # 2. DIAGRAMA INTERACTIVO
        # ====================================================

        st.markdown("---")

        st.markdown(
            "### 2. Diagrama Interactivo de Extracción SX"
        )

        st.write(
            "El diagrama representa las corrientes "
            "de entrada y salida de la etapa de "
            "extracción por solventes. Los valores "
            "se actualizan automáticamente al modificar "
            "los parámetros de operación."
        )

        mostrar_diagrama_extraccion(
            q_pls=pls_flow,
            cu_pls=cu_pls,
            q_org=org_flow,
            cu_org_desc=cu_org_desc,
            cu_refino=cu_raff,
            cu_org_cargado=cu_org_cargado,
            unidad_masa=unidad_masa
        )

        st.caption(
            "PLS y orgánico descargado corresponden "
            "a las entradas del sistema. Refino y "
            "orgánico cargado corresponden a las "
            "salidas. Pasa el cursor sobre una "
            "corriente para consultar sus valores."
        )

        st.info(
            "La concentración de cobre del orgánico "
            "cargado se calcula automáticamente "
            "mediante balance de masa. Los caudales "
            "de las fases se consideran constantes "
            "entre la entrada y la salida."
        )

        # ====================================================
        # 3. RESULTADOS DE EXTRACCIÓN
        # ====================================================

        st.markdown("---")

        st.markdown(
            "### 3. Resultados de Extracción"
        )

        r1, r2 = st.columns(2)

        with r1:

            st.markdown(
                tarjeta_resultado(
                    "Cobre en Orgánico Cargado",
                    f"{cu_org_cargado:.2f}",
                    "g/L",
                    "#3b82f6"
                ),
                unsafe_allow_html=True
            )

        with r2:

            st.markdown(
                tarjeta_resultado(
                    "Recuperación de Extracción",
                    f"{resultados['recuperacion']:.2f}",
                    "%",
                    "#10b981"
                ),
                unsafe_allow_html=True
            )

        r3, r4 = st.columns(2)

        with r3:

            masa_transferida_unidad = convertir_flujo_masico(
                masa_transferida,
                unidad_masa
            )

            st.metric(
                "Cobre Transferido",
                f"{masa_transferida_unidad:,.2f} "
                f"{unidad_masa}"
            )

        # ====================================================
        # CORRECCIÓN 1: RELACIÓN A/O
        # ====================================================

        with r4:

            st.metric(
                "Relación A/O",
                f"{pls_flow / org_flow:.2f}"
            )

        # ====================================================
        # 4. CÁLCULO DE MASA DE COBRE TRANSPORTADA
        # ====================================================

        st.markdown("---")

        st.markdown(
            "### 4. Cálculo de Masa de Cobre Transportada"
        )

        st.write(
            "El flujo másico de cobre se determina "
            "a partir del caudal volumétrico "
            "y la concentración de cobre de cada "
            "corriente."
        )

        st.latex(
            r"\dot{m}_{Cu}=Q\times C_{Cu}"
        )

        st.write(
            "Donde Q corresponde al caudal en m³/h, "
            "la concentración de cobre se expresa "
            "en g/L y el resultado se obtiene en kg/h."
        )

        st.latex(
            r"\dot{m}_{Cu}\;[kg/h]"
            r"=Q\;[m^3/h]\times C_{Cu}\;[g/L]"
        )

        st.markdown(
            "#### Flujo másico de cobre por corriente"
        )

        datos_masa = [
            {
                "Corriente": "PLS",
                "Tipo": "Entrada",
                "Caudal [m³/h]": pls_flow,
                "Cu [g/L]": cu_pls,
                f"Masa Cu [{unidad_masa}]":
                    convertir_flujo_masico(
                        masa_pls, unidad_masa
                    )
            },
            {
                "Corriente": "Orgánico descargado",
                "Tipo": "Entrada",
                "Caudal [m³/h]": org_flow,
                "Cu [g/L]": cu_org_desc,
                f"Masa Cu [{unidad_masa}]":
                    convertir_flujo_masico(
                        masa_org_desc, unidad_masa
                    )
            },
            {
                "Corriente": "Refino",
                "Tipo": "Salida",
                "Caudal [m³/h]": pls_flow,
                "Cu [g/L]": cu_raff,
                f"Masa Cu [{unidad_masa}]":
                    convertir_flujo_masico(
                        masa_refino, unidad_masa
                    )
            },
            {
                "Corriente": "Orgánico cargado",
                "Tipo": "Salida",
                "Caudal [m³/h]": org_flow,
                "Cu [g/L]": cu_org_cargado,
                f"Masa Cu [{unidad_masa}]":
                    convertir_flujo_masico(
                        masa_org_cargado, unidad_masa
                    )
            }
        ]

        tabla_masa = pd.DataFrame(datos_masa)

        st.dataframe(
            tabla_masa.style.format({
                "Caudal [m³/h]": "{:,.2f}",
                "Cu [g/L]": "{:,.2f}",
                f"Masa Cu [{unidad_masa}]": "{:,.2f}"
            }),
            hide_index=True,
            use_container_width=True
        )

        # ====================================================
        # 5. BALANCE DE COBRE
        # ====================================================

        st.markdown("---")

        st.markdown(
            "### 5. Balance de Cobre"
        )

        st.write(
            "El balance considera el cobre presente "
            "en las corrientes de entrada y salida "
            "de la etapa de extracción."
        )

        st.latex(
            r"\dot{m}_{Cu,\ entrada}"
            r"=\dot{m}_{Cu,\ salida}"
        )

        st.latex(
            r"\dot{m}_{Cu,\ PLS}"
            r"+\dot{m}_{Cu,\ org.\ desc.}"
            r"="
            r"\dot{m}_{Cu,\ refino}"
            r"+\dot{m}_{Cu,\ org.\ carg.}"
        )

        masa_entrada_unidad = convertir_flujo_masico(
            masa_entrada,
            unidad_masa
        )

        masa_salida_unidad = convertir_flujo_masico(
            masa_salida,
            unidad_masa
        )

        b1, b2 = st.columns(2)

        with b1:

            st.metric(
                "Cobre Total de Entrada",
                f"{masa_entrada_unidad:,.2f} "
                f"{unidad_masa}"
            )

        with b2:

            st.metric(
                "Cobre Total de Salida",
                f"{masa_salida_unidad:,.2f} "
                f"{unidad_masa}"
            )

        diferencia_masa = (
            masa_entrada - masa_salida
        )

        diferencia_unidad = convertir_flujo_masico(
            diferencia_masa,
            unidad_masa
        )

        st.metric(
            "Diferencia del Balance",
            f"{diferencia_unidad:,.2f} "
            f"{unidad_masa}"
        )

        if abs(diferencia_masa) < 1e-8:

            st.success(
                "El balance de masa de cobre "
                "se encuentra cerrado correctamente."
            )

        else:

            st.warning(
                "Existe una diferencia entre "
                "la masa de cobre de entrada "
                "y la masa de cobre de salida."
            )

        # ====================================================
        # 6. CÁLCULOS OPERACIONALES
        # ====================================================

        st.markdown("---")

        st.markdown(
            "### 6. Cálculos Operacionales de Extracción"
        )

        st.markdown(
            "#### 6.1. Cobre transferido"
        )

        st.latex(
            r"\dot{m}_{Cu,\ transferido}"
            r"="
            r"\dot{m}_{Cu,\ PLS}"
            r"-"
            r"\dot{m}_{Cu,\ refino}"
        )

        st.metric(
            "Cobre Transferido a la Fase Orgánica",
            f"{masa_transferida_unidad:,.2f} "
            f"{unidad_masa}"
        )

        st.markdown(
            "#### 6.2. Recuperación de cobre"
        )

        st.latex(
            r"R_{Cu}="
            r"\frac{C_{PLS}-C_{Refino}}"
            r"{C_{PLS}}\times100"
        )

        st.metric(
            "Recuperación de Cobre",
            f"{resultados['recuperacion']:.2f}%"
        )

        # ====================================================
        # CORRECCIÓN 2: RAZÓN DE FLUJO A/O
        # ====================================================

        st.markdown(
            "#### 6.3. Razón de flujo A/O"
        )

        st.latex(
            r"\frac{A}{O}="
            r"\frac{Q_{PLS}}{Q_{Orgánico}}"
        )

        st.metric(
            "Razón Acuoso / Orgánico",
            f"{pls_flow / org_flow:.2f}"
        )

        st.markdown(
            "#### 6.4. Concentración del orgánico cargado"
        )

        st.latex(
            r"C_{Org,\ cargado}="
            r"C_{Org,\ descargado}"
            r"+\frac{Q_{PLS}}{Q_{Org}}"
            r"(C_{PLS}-C_{Refino})"
        )

        st.metric(
            "Concentración Cu Orgánico Cargado",
            f"{cu_org_cargado:.2f} g/L"
        )

        # ====================================================
        # 7. BALANCE ORIGINAL EN t/h
        # ====================================================

        st.markdown("---")

        st.markdown(
            "### 7. Balance de Cobre en t/h"
        )

        tabla = pd.DataFrame({
            "Corriente": [
                "PLS",
                "Orgánico descargado",
                "Refino",
                "Orgánico cargado"
            ],
            "Tipo": [
                "Entrada",
                "Entrada",
                "Salida",
                "Salida"
            ],
            "Cu [t/h]": [
                resultados["cobre_pls"],
                flujo_cobre(
                    org_flow,
                    cu_org_desc
                ),
                resultados["cobre_refino"],
                flujo_cobre(
                    org_flow,
                    cu_org_cargado
                )
            ]
        })

        st.dataframe(
            tabla,
            hide_index=True,
            use_container_width=True
        )

        mostrar_cierre(
            resultados["cierre"]
        )

        st.caption(
            "Se supone que los caudales volumétricos "
            "de cada fase permanecen constantes y "
            "que no existen pérdidas ni arrastres. "
            "La concentración del orgánico cargado "
            "se obtiene mediante balance de masa; "
            "no se verifica su capacidad máxima "
            "de carga ni el equilibrio químico. "
            "Las masas mostradas son flujos másicos "
            "de cobre por unidad de tiempo, no "
            "masas totales acumuladas."
        )

    # ========================================================
    # 2. REEXTRACCIÓN
    # ========================================================

    elif sub_sx == "Re-extracción":

        st.subheader(
            "🔄 Módulo de Re-extracción (Stripping)"
        )

        st.write(
            "Calcula la transferencia de cobre desde "
            "el orgánico cargado hacia el electrolito "
            "pobre mediante una solución ácida."
        )

        st.latex(
            r"CuR_{2(org)} + 2H^+_{(ac)}"
            r"\rightleftharpoons "
            r"Cu^{2+}_{(ac)} + 2RH_{(org)}"
        )

        st.markdown(
            "### 📥 Parámetros de Operación"
        )

        col1, col2 = st.columns(2)

        with col1:

            org_cargado_flow = st.number_input(
                "Caudal de Orgánico Cargado [m³/h]",
                min_value=0.1,
                value=400.0,
                step=10.0,
                format="%.2f",
                key="sx_re_q_org"
            )

            cu_org_cargado = st.number_input(
                "Cu en Orgánico Cargado [g/L]",
                min_value=0.01,
                value=5.80,
                step=0.1,
                format="%.2f",
                key="sx_re_cu_org_cargado"
            )

            cu_org_descargado = st.number_input(
                "Cu en Orgánico Descargado [g/L]",
                min_value=0.0,
                value=0.50,
                step=0.1,
                format="%.2f",
                key="sx_re_cu_org_desc"
            )

        with col2:

            electrolito_pobre_flow = st.number_input(
                "Caudal de Electrolito Pobre [m³/h]",
                min_value=0.1,
                value=100.0,
                step=5.0,
                format="%.2f",
                key="sx_re_q_ep"
            )

            cu_electrolito_pobre = st.number_input(
                "Cu en Electrolito Pobre [g/L]",
                min_value=0.0,
                value=35.0,
                step=1.0,
                format="%.2f",
                key="sx_re_cu_ep"
            )

        if cu_org_descargado > cu_org_cargado:

            st.error(
                "La concentración de cobre del "
                "orgánico descargado no puede "
                "superar la del orgánico cargado."
            )

            return

        resultados = balance_reextraccion(
            org_cargado_flow,
            cu_org_cargado,
            cu_org_descargado,
            electrolito_pobre_flow,
            cu_electrolito_pobre
        )

        st.markdown("---")

        st.markdown(
            "### 📊 Resultados de Re-extracción"
        )

        r1, r2 = st.columns(2)

        with r1:

            st.markdown(
                tarjeta_resultado(
                    "Cu en Electrolito Rico (ELR)",
                    f"{resultados['cu_electrolito_rico']:.2f}",
                    "g/L",
                    "#f59e0b"
                ),
                unsafe_allow_html=True
            )

        with r2:

            st.markdown(
                tarjeta_resultado(
                    "Relación de Caudales O/A",
                    f"{org_cargado_flow / electrolito_pobre_flow:.2f}",
                    "Adimensional",
                    "#a855f7"
                ),
                unsafe_allow_html=True
            )

        r3, r4 = st.columns(2)

        r3.metric(
            "Cobre Transferido al Electrolito",
            f"{resultados['cobre_transferido']:.3f} t/h"
        )

        r4.metric(
            "Reextracción de Cu del Orgánico",
            f"{resultados['eficiencia']:.2f}%"
        )

        st.markdown(
            "### 📋 Balance de Cobre"
        )

        tabla = pd.DataFrame({
            "Corriente": [
                "Orgánico cargado",
                "Electrolito pobre",
                "Orgánico descargado",
                "Electrolito rico"
            ],
            "Tipo": [
                "Entrada",
                "Entrada",
                "Salida",
                "Salida"
            ],
            "Cu [t/h]": [
                flujo_cobre(
                    org_cargado_flow,
                    cu_org_cargado
                ),
                flujo_cobre(
                    electrolito_pobre_flow,
                    cu_electrolito_pobre
                ),
                flujo_cobre(
                    org_cargado_flow,
                    cu_org_descargado
                ),
                flujo_cobre(
                    electrolito_pobre_flow,
                    resultados["cu_electrolito_rico"]
                )
            ]
        })

        st.dataframe(
            tabla,
            hide_index=True,
            use_container_width=True
        )

        mostrar_cierre(
            resultados["cierre"]
        )

        st.caption(
            "El modelo supone caudales constantes "
            "y ausencia de pérdidas. La concentración "
            "del electrolito rico se calcula por "
            "balance de cobre y no mediante "
            "equilibrio de reextracción."
        )

    # ========================================================
    # 3. CIRCUITO COMPLETO
    # ========================================================

    elif sub_sx == "Circuito Completo":

        st.subheader(
            "🌐 Balance General del Circuito Completo de SX"
        )

        st.write(
            "Simulación integrada de extracción "
            "y reextracción para estimar la "
            "transferencia global de cobre."
        )

        st.markdown(
            "### 📥 Alimentación y Extracción"
        )

        col1, col2 = st.columns(2)

        with col1:

            q_pls = st.number_input(
                "Caudal de PLS Total [m³/h]",
                min_value=0.1,
                value=500.0,
                step=10.0,
                format="%.2f",
                key="sx_c_q_pls"
            )

            cu_pls = st.number_input(
                "Concentración Cu en PLS [g/L]",
                min_value=0.01,
                value=4.50,
                step=0.1,
                format="%.2f",
                key="sx_c_cu_pls"
            )

            recuperacion_ex = st.slider(
                "Recuperación de Extracción [%]",
                min_value=0.0,
                max_value=100.0,
                value=95.0,
                step=0.5,
                key="sx_c_rec_ex"
            )

        with col2:

            q_org = st.number_input(
                "Caudal de Orgánico Total [m³/h]",
                min_value=0.1,
                value=400.0,
                step=10.0,
                format="%.2f",
                key="sx_c_q_org"
            )

            cu_org_desc = st.number_input(
                "Cu en Orgánico Descargado [g/L]",
                min_value=0.0,
                value=0.50,
                step=0.1,
                format="%.2f",
                key="sx_c_cu_org_desc"
            )

        # ----------------------------------------------------
        # CÁLCULOS DE EXTRACCIÓN
        # ----------------------------------------------------

        cu_refino = (
            cu_pls * (1.0 - recuperacion_ex / 100.0)
        )

        extraccion = balance_extraccion(
            q_pls,
            cu_pls,
            q_org,
            cu_org_desc,
            cu_refino
        )

        cu_org_cargado = extraccion[
            "cu_org_cargado"
        ]

        st.markdown("---")

        st.markdown(
            "### 🔄 Parámetros de Re-extracción"
        )

        col3, col4 = st.columns(2)

        with col3:

            q_electrolito = st.number_input(
                "Caudal de Electrolito Pobre [m³/h]",
                min_value=0.1,
                value=100.0,
                step=5.0,
                format="%.2f",
                key="sx_c_q_ep"
            )

            cu_electrolito_pobre = st.number_input(
                "Cu en Electrolito Pobre [g/L]",
                min_value=0.0,
                value=35.0,
                step=1.0,
                format="%.2f",
                key="sx_c_cu_ep"
            )

        with col4:

            recuperacion_re = st.slider(
                "Reextracción de Cu del Orgánico [%]",
                min_value=0.0,
                max_value=100.0,
                value=90.0,
                step=0.5,
                key="sx_c_rec_re"
            )

        # ----------------------------------------------------
        # CÁLCULOS DE REEXTRACCIÓN
        # ----------------------------------------------------

        cu_org_salida_re = (
            cu_org_cargado
            * (1.0 - recuperacion_re / 100.0)
        )

        reextraccion = balance_reextraccion(
            q_org,
            cu_org_cargado,
            cu_org_salida_re,
            q_electrolito,
            cu_electrolito_pobre
        )

        # ----------------------------------------------------
        # BALANCE GLOBAL
        # ----------------------------------------------------

        cobre_pls = extraccion["cobre_pls"]

        cobre_extraido = extraccion[
            "cobre_transferido"
        ]

        cobre_reextraido = reextraccion[
            "cobre_transferido"
        ]

        recuperacion_global = (
            cobre_reextraido / cobre_pls * 100.0
            if cobre_pls > 0 else 0.0
        )

        st.markdown("---")

        st.markdown(
            "### 📋 Resumen Global del Proceso SX"
        )

        r1, r2, r3 = st.columns(3)

        r1.metric(
            "Caudal PLS",
            f"{q_pls:.2f} m³/h"
        )

        r2.metric(
            "Caudal Orgánico",
            f"{q_org:.2f} m³/h"
        )

        r3.metric(
            "Cobre Transferido al Electrolito",
            f"{cobre_reextraido:.3f} t/h"
        )

        r4, r5, r6 = st.columns(3)

        r4.metric(
            "Cu en Refino",
            f"{cu_refino:.2f} g/L"
        )

        r5.metric(
            "Cu en Orgánico Cargado",
            f"{cu_org_cargado:.2f} g/L"
        )

        r6.metric(
            "Cu en Electrolito Rico",
            f"{reextraccion['cu_electrolito_rico']:.2f} g/L"
        )

        st.markdown(
            "### 📊 Recuperación Global"
        )

        st.markdown(
            tarjeta_resultado(
                "Transferencia Global Estimada de Cu",
                f"{recuperacion_global:.2f}",
                "% respecto al cobre del PLS",
                "#10b981"
            ),
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # COMPROBACIÓN DE CONTINUIDAD DEL ORGÁNICO
        # ----------------------------------------------------

        diferencia_org = (
            cu_org_salida_re - cu_org_desc
        )

        if abs(diferencia_org) > 1e-6:

            st.warning(
                "El orgánico descargado calculado "
                "en reextracción no coincide con "
                "el orgánico de entrada a extracción. "
                "Por lo tanto, los parámetros ingresados "
                "no representan un circuito cerrado "
                "en estado estacionario."
            )

            st.write(
                f"Cu en orgánico de entrada a extracción: "
                f"{cu_org_desc:.3f} g/L"
            )

            st.write(
                f"Cu en orgánico después de reextracción: "
                f"{cu_org_salida_re:.3f} g/L"
            )

        else:

            st.success(
                "La concentración del orgánico "
                "es consistente entre ambas etapas."
            )

        st.markdown(
            "### 📋 Resumen de Corrientes"
        )

        tabla = pd.DataFrame({
            "Corriente": [
                "PLS",
                "Refino",
                "Orgánico descargado inicial",
                "Orgánico cargado",
                "Orgánico después de reextracción",
                "Electrolito pobre",
                "Electrolito rico"
            ],
            "Caudal [m³/h]": [
                q_pls,
                q_pls,
                q_org,
                q_org,
                q_org,
                q_electrolito,
                q_electrolito
            ],
            "Cu [g/L]": [
                cu_pls,
                cu_refino,
                cu_org_desc,
                cu_org_cargado,
                cu_org_salida_re,
                cu_electrolito_pobre,
                reextraccion["cu_electrolito_rico"]
            ]
        })

        st.dataframe(
            tabla,
            hide_index=True,
            use_container_width=True
        )

        mostrar_cierre(
            extraccion["cierre"]
        )

        mostrar_cierre(
            reextraccion["cierre"]
        )

        st.caption(
            "Los balances individuales cierran por "
            "construcción matemática. Esto no garantiza "
            "que el circuito sea físicamente viable. "
            "La recuperación global mostrada corresponde "
            "a la transferencia de cobre al electrolito "
            "respecto de la alimentación de PLS; "
            "no representa producción de cátodos."
        )
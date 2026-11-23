import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from html import escape


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

import io
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter


# Instrucciones comunes para las explicaciones de las calculadoras SX.
# Se añaden a los datos específicos de cada etapa sin alterar los cálculos.
INSTRUCCIONES_IA_SX = (
    "\n\nFORMATO OBLIGATORIO DE RESPUESTA (usa estos títulos exactos):\n"
    "## 1. Resultados\n"
    "## 2. Explicación metalúrgica\n"
    "## 3. Análisis técnico\n"
    "## 4. Recomendaciones\n\n"
    "En Resultados, presenta los valores entregados y sus unidades, "
    "sin inventar mediciones ni modificar los números. "
    "En Explicación metalúrgica, explica las ecuaciones, las corrientes "
    "y la transferencia de cobre propias de esta etapa. "
    "En Análisis técnico, interpreta los datos, los supuestos y las "
    "limitaciones, distinguiendo cálculos teóricos de mediciones reales. "
    "En Recomendaciones, propone verificaciones pertinentes a los datos, "
    "sin afirmar condiciones operacionales no proporcionadas. "
    "Mantén exactamente dos decimales para los resultados numéricos. "
    "No confundas masas con flujos másicos, ni relaciones de fases con "
    "eficiencia o recuperación de cobre. No añadas secciones adicionales "
    "ni advertencias sobre dilución de ácido cuando no corresponden."
)


def descargar_tabla_excel(datos, nombre_archivo, clave):
    """Exporta la tabla mostrada a un Excel con números y unidades originales."""
    tabla = datos.copy()
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as escritor:
        tabla.to_excel(escritor, index=False, sheet_name="Resultados SX")
        hoja = escritor.sheets["Resultados SX"]
        hoja.freeze_panes = "A2"
        hoja.auto_filter.ref = hoja.dimensions
        for celda in hoja[1]:
            celda.font = Font(bold=True, color="FFFFFF")
            celda.fill = PatternFill("solid", fgColor="17365D")
            celda.alignment = Alignment(wrap_text=True, vertical="center")
        hoja.row_dimensions[1].height = 30
        for columna in hoja.columns:
            letra = get_column_letter(columna[0].column)
            ancho = max(len(str(c.value or "")) for c in columna)
            hoja.column_dimensions[letra].width = min(max(ancho + 3, 14), 38)
            for celda in list(columna)[1:]:
                if isinstance(celda.value, (float, int)) and not isinstance(celda.value, bool):
                    celda.number_format = '#,##0.00'
    st.download_button(
        "📥 Exportar tabla a Excel",
        data=buffer.getvalue(),
        file_name=nombre_archivo,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key=clave,
        use_container_width=True,
    )

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


def convertir_resultado_extraccion(valor_kg, unidad, modo_laboratorio=False):
    """Convierte kg a masa o flujo másico según el modo seleccionado."""
    if modo_laboratorio:
        return valor_kg * 1000.0 if unidad == "g" else valor_kg
    return convertir_flujo_masico(valor_kg, unidad)


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
    unidad_masa,
    modo_laboratorio=False,
    unidad_volumen="m³/h"
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

        corriente["masa"] = convertir_resultado_extraccion(
            masa_kg_h, unidad_masa, modo_laboratorio
        )
        corriente["volumen_mostrado"] = (
            corriente["caudal"] * 1000.0
            if modo_laboratorio and unidad_volumen == "L"
            else corriente["caudal"] * 1000000.0
            if modo_laboratorio and unidad_volumen == "mL"
            else corriente["caudal"]
        )

    def tarjeta_svg(clave, x, y, ancho=270, alto=130):

        corriente = corrientes[clave]

        nombre = escape(corriente["nombre"])
        color = corriente["color"]

        caudal = formato_numero(corriente["volumen_mostrado"])
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
                {("Volumen" if modo_laboratorio else "Caudal")}: {caudal} {unidad_volumen}
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
                {("Volumen" if modo_laboratorio else "Caudal")}: {caudal} {unidad_volumen}
                Concentración: {concentracion} g/L
                {("Masa" if modo_laboratorio else "Flujo másico")}: {masa} {unidad_masa}
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
                min-width: 0;
                height: auto;
                max-height: 470px;
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
        height=500,
        scrolling=False
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
            min_value=0.0,
            value=0.0,
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
            min_value=0.0,
            value=0.0,
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
    ) if volumen_total > 0 and razon_fa_fo > 0 else {
        "volumen_acuoso": 0.0,
        "volumen_organico": 0.0,
        "porcentaje_acuoso": 0.0,
        "porcentaje_organico": 0.0,
        "volumen_total": volumen_total,
        "razon": razon_fa_fo
    }

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
            volumen_total if volumen_total > 0 and razon_fa_fo > 0 else 0.0
        ],
        "Porcentaje [%]": [
            porcentaje_a,
            porcentaje_o,
            100.0 if volumen_total > 0 and razon_fa_fo > 0 else 0.0
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

    descargar_tabla_excel(tabla_fases, "SX_tabla_01.xlsx", "sx_tabla_01")

    st.caption(
        "Esta calculadora determina proporciones "
        "volumétricas de ambas fases. Se supone "
        "aditividad de volúmenes, sin contracción, "
        "pérdidas ni arrastres. La razón FA/FO "
        "no permite por sí sola determinar "
        "la eficiencia de extracción de cobre."
    )

    # --------------------------------------------------------
    # 5. EXPLICACIÓN DEL RESULTADO CON IA
    # --------------------------------------------------------

    st.markdown("---")
    st.markdown("### 5. 🤖 Explicación del resultado con IA")
    st.write(
        "Solicita al asistente metalúrgico una interpretación "
        "de la razón FA/FO y de los volúmenes calculados."
    )

    datos_validos_ia = volumen_total > 0 and razon_fa_fo > 0
    firma_ia = (volumen_total, unidad, razon_fa_fo)

    if st.session_state.get("sx_fafo_ia_firma") != firma_ia:
        st.session_state["sx_fafo_ia_firma"] = firma_ia
        st.session_state.pop("sx_fafo_ia_respuesta", None)
        st.session_state.pop("sx_fafo_ia_modelo", None)

    if st.button(
        "🤖 Explicar resultado con IA",
        key="sx_fafo_boton_explicar_ia",
        use_container_width=True,
        disabled=not datos_validos_ia,
    ):
        try:
            from modulos.asistente import (
                obtener_api_key,
                generar_respuesta,
                interpretar_error,
            )

            prompt = (
                "Actúa como asistente académico especializado en "
                "hidrometalurgia y extracción por solventes (SX). "
                "Interpreta los siguientes resultados de una calculadora "
                "de razón volumétrica FA/FO. Responde en español claro, "
                "con rigor técnico y sin inventar datos.\n\n"
                f"Volumen total: {volumen_total:.2f} {unidad}\n"
                f"Razón FA/FO: {razon_fa_fo:.2f}\n"
                f"Volumen acuoso (FA): {va:.2f} {unidad}\n"
                f"Volumen orgánico (FO): {vo:.2f} {unidad}\n"
                f"Porcentaje acuoso: {porcentaje_a:.2f} %\n"
                f"Porcentaje orgánico: {porcentaje_o:.2f} %\n\n"
                "Explica el significado físico de la razón FA/FO, "
                "cómo se distribuye el volumen entre fases y qué "
                "implicaciones operacionales puede tener en un ensayo SX. "
                "Aclara que esta razón por sí sola no permite calcular "
                "la recuperación de cobre ni el equilibrio de extracción. "
                "No cambies los resultados calculados."
            )

            prompt += INSTRUCCIONES_IA_SX
            prompt += (
                "\n\nCRITERIOS ESPECÍFICOS PARA FA/FO:\n"
                "En 1. Resultados, presenta el volumen total, la razón FA/FO, "
                "los volúmenes de cada fase y sus porcentajes, con las unidades recibidas. "
                "En 2. Explicación metalúrgica, explica FA/FO = Va/Vo, la distribución "
                "volumétrica y el papel de ambas fases en la extracción por solventes. "
                "En 3. Análisis técnico, interpreta si predomina la fase acuosa u orgánica "
                "según los valores y comenta que se supone aditividad de volúmenes, "
                "sin pérdidas, contracción ni arrastres. Distingue esta razón volumétrica "
                "de los caudales reales y del rendimiento de extracción; no deduzcas "
                "recuperación, capacidad de carga, equilibrio ni separación de fases "
                "sin datos adicionales. En 4. Recomendaciones, sugiere comprobaciones "
                "de volúmenes, medición y homogeneidad de la preparación, y evaluación "
                "experimental de la separación cuando corresponda. "
                "No supongas tiempos de mezcla, pH, composición del orgánico ni concentraciones "
                "de cobre no proporcionadas. Mantén un lenguaje técnico conciso y preciso."
            )

            api_key = obtener_api_key()
            if not api_key:
                raise ValueError("No se encontró la clave API de Gemini.")
            indicador_ia = st.empty()
            try:
                respuesta, modelo = generar_respuesta(
                    api_key=api_key, mensajes=[], pregunta=prompt, indicador=indicador_ia, tipo_asistente="calculadora"
                )
            finally:
                indicador_ia.empty()
            if not respuesta:
                raise ValueError("El asistente no devolvió una respuesta.")

            st.session_state["sx_fafo_ia_respuesta"] = respuesta
            st.session_state["sx_fafo_ia_modelo"] = modelo
        except Exception as error:
            try:
                mensaje = interpretar_error(error)
            except Exception:
                mensaje = str(error)
            st.error(f"No se pudo generar la explicación con IA: {mensaje}")
            with st.expander("Ver detalles técnicos del error"):
                st.code(f"{type(error).__name__}: {error}")

    if not datos_validos_ia:
        st.info(
            "Ingresa un volumen total y una razón FA/FO mayores "
            "que cero para habilitar la explicación con IA."
        )
    elif st.session_state.get("sx_fafo_ia_respuesta"):
        st.markdown("#### 🤖 Interpretación del asistente")
        st.markdown(st.session_state["sx_fafo_ia_respuesta"])
        if st.session_state.get("sx_fafo_ia_modelo"):
            st.caption(
                "Modelo utilizado: "
                f"{st.session_state['sx_fafo_ia_modelo']}"
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
            "Re-extracción"
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

        # El modo industrial permanece implementado, pero no se muestra en la interfaz.
        modo_calculo = "Laboratorio (volúmenes)"
        modo_laboratorio = modo_calculo == "Laboratorio (volúmenes)"
        unidad_volumen = (
            st.selectbox(
                "Unidad de volumen de las soluciones",
                ["mL", "L"],
                key="sx_ex_unidad_volumen"
            )
            if modo_laboratorio else "m³/h"
        )

        corriente_a_calcular = st.selectbox(
            "Concentración de cobre que deseas calcular",
            ["Orgánico cargado", "PLS", "Refino", "Orgánico descargado"],
            key="sx_ex_corriente_concentracion"
        )
        st.caption(
            "Ingresa las concentraciones de las otras tres corrientes. "
            "La concentración seleccionada se calculará automáticamente "
            "y se utilizará en el diagrama y los balances."
        )

        st.markdown("#### Cálculo de fases mediante FA/FO")
        forma_ingreso_fases = st.radio(
            "¿Cómo deseas ingresar las fases?",
            [
                "Ingresar ambas fases manualmente",
                "Calcular ambas desde el total"
            ],
            horizontal=False,
            key="sx_ex_forma_ingreso_fases"
        )

        calculo_fafo_activo = (
            forma_ingreso_fases != "Ingresar ambas fases manualmente"
        )
        if calculo_fafo_activo:
            razon_fafo_ingresada = st.number_input(
                "Razón de flujo FA/FO",
                min_value=0.0,
                value=0.0,
                step=0.05,
                format="%.2f",
                key="sx_ex_razon_fafo"
            )

        if forma_ingreso_fases == "Calcular ambas desde el total":
            total_fases_ingresado = st.number_input(
                (
                    "Volumen total de las fases"
                    if modo_laboratorio else "Caudal total de las fases"
                ) + f" [{unidad_volumen}]",
                min_value=0.0,
                value=0.0,
                step=10.0,
                format="%.2f",
                key="sx_ex_total_fases"
            )

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("**Fase acuosa**")

            if forma_ingreso_fases == "Calcular ambas desde el total":
                pls_flow = (
                    total_fases_ingresado * razon_fafo_ingresada
                    / (1.0 + razon_fafo_ingresada)
                )
            else:
                pls_flow = st.number_input(
                    ("Volumen de PLS" if modo_laboratorio else "Caudal de PLS")
                    + f" [{unidad_volumen}]",
                    min_value=0.0,
                    value=0.0,
                    step=10.0,
                    format="%.2f",
                    key="sx_ex_q_pls"
                )

            if corriente_a_calcular == "PLS":
                cu_pls = None
                campo_calculado_pls = st.empty()
            else:
                cu_pls = st.number_input(
                    "Concentración Cu en PLS [g/L]",
                    min_value=0.0,
                    value=0.0,
                    step=0.1,
                    format="%.2f",
                    key="sx_ex_cu_pls"
                )

            if corriente_a_calcular == "Refino":
                cu_raff = None
                campo_calculado_refino = st.empty()
            else:
                cu_raff = st.number_input(
                    "Concentración Cu en Refino [g/L]",
                    min_value=0.0,
                    value=0.0,
                    step=0.01,
                    format="%.2f",
                    key="sx_ex_cu_refino"
                )

        with col2:

            st.markdown("**Fase orgánica**")

            if forma_ingreso_fases == "Calcular ambas desde el total":
                org_flow = (
                    total_fases_ingresado / (1.0 + razon_fafo_ingresada)
                )
            else:
                org_flow = st.number_input(
                    ("Volumen de Orgánico" if modo_laboratorio else "Caudal de Orgánico")
                    + f" [{unidad_volumen}]",
                    min_value=0.0,
                    value=0.0,
                    step=10.0,
                    format="%.2f",
                    key="sx_ex_q_org"
                )

            if corriente_a_calcular == "Orgánico descargado":
                cu_org_desc = None
                campo_calculado_org_desc = st.empty()
            else:
                cu_org_desc = st.number_input(
                    "Cu en Orgánico Descargado [g/L]",
                    min_value=0.0,
                    value=0.0,
                    step=0.1,
                    format="%.2f",
                    key="sx_ex_cu_org_desc"
                )

            if corriente_a_calcular != "Orgánico cargado":
                cu_org_cargado_ingresado = st.number_input(
                    "Cu en Orgánico Cargado [g/L]",
                    min_value=0.0,
                    value=0.0,
                    step=0.01,
                    format="%.2f",
                    key="sx_ex_cu_org_cargado"
                )
            else:
                cu_org_cargado_ingresado = None
                campo_calculado_org_cargado = st.empty()

            unidad_masa = st.selectbox(
                "Unidad de masa de cobre" if modo_laboratorio
                else "Unidad de masa de cobre transportada",
                ["g", "kg"] if modo_laboratorio else ["kg/h", "t/h", "g/h"],
                index=0,
                key="sx_ex_unidad_masa_lab" if modo_laboratorio
                else "sx_ex_unidad_masa"
            )

        if calculo_fafo_activo:
            st.markdown("**Fases calculadas automáticamente**")
            fa_col, fo_col = st.columns(2)
            with fa_col:
                st.metric(
                    f"Fase acuosa (FA) [{unidad_volumen}]",
                    f"{pls_flow:,.2f}"
                )
            with fo_col:
                st.metric(
                    f"Fase orgánica (FO) [{unidad_volumen}]",
                    f"{org_flow:,.2f}"
                )
            st.caption(
                "Los valores calculados se utilizan automáticamente "
                "en el diagrama de extracción y en los balances."
            )

        # Los balances originales trabajan con m³/h. En modo laboratorio
        # se introducen volúmenes equivalentes en m³; los resultados
        # numéricos en kg/h se interpretan como masas en kg.
        if modo_laboratorio:
            factor_volumen = 1_000_000.0 if unidad_volumen == "mL" else 1000.0
            pls_flow = pls_flow / factor_volumen
            org_flow = org_flow / factor_volumen

        # Mostrar los apartados aun cuando falten datos de entrada.
        def mostrar_apartados_sin_datos():
            st.info(
                "Ingresa caudales o volúmenes mayores que cero para "
                "habilitar los cálculos. Los apartados permanecen visibles."
            )
            st.markdown("---")
            st.markdown("### 2. Diagrama Interactivo de Extracción SX")
            mostrar_diagrama_extraccion(
                q_pls=pls_flow,
                cu_pls=0.0,
                q_org=org_flow,
                cu_org_desc=0.0,
                cu_refino=0.0,
                cu_org_cargado=0.0,
                unidad_masa=unidad_masa,
                modo_laboratorio=modo_laboratorio,
                unidad_volumen=unidad_volumen
            )
            st.caption("El diagrama se actualizará al ingresar datos válidos.")
            st.info(
                f"La concentración de cobre de {corriente_a_calcular.lower()} "
                "se calcula automáticamente mediante balance de masa. "
                "Los caudales de las fases se consideran constantes "
                "entre la entrada y la salida."
            )
            st.markdown("---")
            st.markdown("### 3. Resultados de Extracción")
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(
                    tarjeta_resultado(
                        f"Cobre en {corriente_a_calcular}", "0.00", "g/L", "#3b82f6"
                    ),
                    unsafe_allow_html=True
                )
            with col_b:
                st.markdown(
                    tarjeta_resultado(
                        "Recuperación de Extracción", "0.00", "%", "#10b981"
                    ),
                    unsafe_allow_html=True
                )
            col_c, col_d = st.columns(2)
            with col_c:
                st.metric("Cobre Transferido", f"0.00 {unidad_masa}")
            with col_d:
                st.metric("Relación A/O", "0.00")
            st.markdown("---")
            st.markdown("### 4. Cálculo de Masa de Cobre Transportada")
            st.markdown(
                "#### Masa de cobre por corriente" if modo_laboratorio
                else "#### Flujo másico de cobre por corriente"
            )
            nombre_caudal = (
                f"Volumen [{unidad_volumen}]" if modo_laboratorio
                else f"Caudal [{unidad_volumen}]"
            )
            tabla_vacia = pd.DataFrame([
                {"Corriente": nombre, "Tipo": tipo,
                 nombre_caudal: 0.0, "Cu [g/L]": 0.0,
                 f"Masa Cu [{unidad_masa}]": 0.0}
                for nombre, tipo in (
                    ("PLS", "Entrada"),
                    ("Orgánico descargado", "Entrada"),
                    ("Refino", "Salida"),
                    ("Orgánico cargado", "Salida")
                )
            ])
            st.dataframe(
                tabla_vacia.style.format({
                    nombre_caudal: "{:,.2f}",
                    "Cu [g/L]": "{:,.2f}",
                    f"Masa Cu [{unidad_masa}]": "{:,.2f}"
                }),
                hide_index=True,
                use_container_width=True
            )

            descargar_tabla_excel(tabla_vacia, "SX_tabla_02.xlsx", "sx_tabla_02")
            st.markdown("---")
            st.markdown("### 5. Balance de Cobre")
            st.metric("Cobre de entrada", f"0.00 {unidad_masa}")
            st.metric("Cobre de salida", f"0.00 {unidad_masa}")
            st.metric("Diferencia del balance", f"0.00 {unidad_masa}")
            st.markdown("---")
            st.markdown(
                "### 6. Balance de Cobre en g" if modo_laboratorio
                else "### 6. Balance de Cobre en t/h"
            )
            st.dataframe(
                pd.DataFrame({
                    "Corriente": [
                        "PLS", "Orgánico descargado",
                        "Refino", "Orgánico cargado"
                    ],
                    f"Cu [{'g' if modo_laboratorio else 't/h'}]": [
                        0.0, 0.0, 0.0, 0.0
                    ]
                }).style.format({
                    f"Cu [{'g' if modo_laboratorio else 't/h'}]": "{:,.2f}"
                }),
                hide_index=True,
                use_container_width=True
            )

            descargar_tabla_excel(pd.DataFrame({'Corriente': ['PLS', 'Orgánico descargado', 'Refino', 'Orgánico cargado'], f"Cu [{('g' if modo_laboratorio else 't/h')}]": [0.0, 0.0, 0.0, 0.0]}), "SX_tabla_03.xlsx", "sx_tabla_03")
            st.markdown("---")
            st.markdown("### 🤖 Explicación del resultado con IA")
            st.write(
                "Solicita al asistente metalúrgico una interpretación "
                "del balance de cobre y de las concentraciones de las corrientes SX."
            )
            st.button(
                "🤖 Explicar resultado con IA",
                key="sx_ex_boton_explicar_ia",
                use_container_width=True,
                disabled=True,
                help="Ingresa datos válidos para habilitar la explicación."
            )

        # Despeje de la concentración desconocida a partir del balance
        # de cobre, manteniendo las concentraciones en g/L.
        if pls_flow <= 0 or org_flow <= 0:
            mostrar_apartados_sin_datos()
            return

        if corriente_a_calcular == "PLS":
            cu_pls = cu_raff + (org_flow / pls_flow) * (
                cu_org_cargado_ingresado - cu_org_desc
            )
        elif corriente_a_calcular == "Refino":
            cu_raff = cu_pls - (org_flow / pls_flow) * (
                cu_org_cargado_ingresado - cu_org_desc
            )
        elif corriente_a_calcular == "Orgánico descargado":
            cu_org_desc = cu_org_cargado_ingresado - (pls_flow / org_flow) * (
                cu_pls - cu_raff
            )

        if min(cu_pls, cu_raff, cu_org_desc) < -1e-9:
            st.error(
                "El balance produce una concentración negativa. "
                "Revisa las concentraciones y los caudales ingresados."
            )
            mostrar_apartados_sin_datos()
            return

        if corriente_a_calcular != "Orgánico cargado":
            cu_org_cargado_calculado = (
                cu_org_desc + (pls_flow / org_flow) * (cu_pls - cu_raff)
            )
            if abs(cu_org_cargado_calculado - cu_org_cargado_ingresado) > 1e-8:
                st.error("Las concentraciones no cumplen el balance de cobre.")
                mostrar_apartados_sin_datos()
                return

        concentraciones_sx = {
            "PLS": cu_pls,
            "Refino": cu_raff,
            "Orgánico descargado": cu_org_desc,
            "Orgánico cargado": (
                cu_org_cargado_ingresado
                if cu_org_cargado_ingresado is not None else
                cu_org_desc + (pls_flow / org_flow) * (cu_pls - cu_raff)
            )
        }
        campos_calculados = {
            "PLS": "campo_calculado_pls",
            "Refino": "campo_calculado_refino",
            "Orgánico descargado": "campo_calculado_org_desc",
            "Orgánico cargado": "campo_calculado_org_cargado"
        }
        campo_seleccionado = locals()[campos_calculados[corriente_a_calcular]]
        with campo_seleccionado.container():
            st.number_input(
                f"Concentración Cu en {corriente_a_calcular} [g/L]",
                value=float(max(0.0, concentraciones_sx[corriente_a_calcular])),
                format="%.2f",
                disabled=True,
                key=f"sx_ex_resultado_calculado_{corriente_a_calcular}"
            )

        st.metric(
            f"Concentración Cu calculada en {corriente_a_calcular}",
            f"{concentraciones_sx[corriente_a_calcular]:,.2f} g/L"
        )

        if concentraciones_sx["Orgánico cargado"] < -1e-9:
            st.error("El balance produce una concentración negativa en el orgánico cargado.")
            mostrar_apartados_sin_datos()
            return

        if cu_raff > cu_pls:

            st.error(
                "La concentración de cobre del refino "
                "no puede superar la del PLS en este "
                "modelo de extracción."
            )

            mostrar_apartados_sin_datos()
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
            unidad_masa=unidad_masa,
            modo_laboratorio=modo_laboratorio,
            unidad_volumen=unidad_volumen
        )

        st.caption(
            "PLS y orgánico descargado corresponden "
            "a las entradas del sistema. Refino y "
            "orgánico cargado corresponden a las "
            "salidas. Pasa el cursor sobre una "
            "corriente para consultar sus valores."
        )

        st.info(
            f"La concentración de cobre de {corriente_a_calcular.lower()} "
            "se calcula automáticamente mediante balance de masa. Los caudales "
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
                    f"Cobre en {corriente_a_calcular}",
                    f"{concentraciones_sx[corriente_a_calcular]:.2f}",
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

            masa_transferida_unidad = convertir_resultado_extraccion(
                masa_transferida,
                unidad_masa, modo_laboratorio
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

        st.markdown(
            "#### Masa de cobre por corriente" if modo_laboratorio
            else "#### Flujo másico de cobre por corriente"
        )

        datos_masa = [
            {
                "Corriente": "PLS",
                "Tipo": "Entrada",
                f"{'Volumen' if modo_laboratorio else 'Caudal'} [{unidad_volumen}]": pls_flow * (factor_volumen if modo_laboratorio else 1),
                "Cu [g/L]": cu_pls,
                f"Masa Cu [{unidad_masa}]":
                    convertir_resultado_extraccion(
                        masa_pls, unidad_masa, modo_laboratorio
                    )
            },
            {
                "Corriente": "Orgánico descargado",
                "Tipo": "Entrada",
                f"{'Volumen' if modo_laboratorio else 'Caudal'} [{unidad_volumen}]": org_flow * (factor_volumen if modo_laboratorio else 1),
                "Cu [g/L]": cu_org_desc,
                f"Masa Cu [{unidad_masa}]":
                    convertir_resultado_extraccion(
                        masa_org_desc, unidad_masa, modo_laboratorio
                    )
            },
            {
                "Corriente": "Refino",
                "Tipo": "Salida",
                f"{'Volumen' if modo_laboratorio else 'Caudal'} [{unidad_volumen}]": pls_flow * (factor_volumen if modo_laboratorio else 1),
                "Cu [g/L]": cu_raff,
                f"Masa Cu [{unidad_masa}]":
                    convertir_resultado_extraccion(
                        masa_refino, unidad_masa, modo_laboratorio
                    )
            },
            {
                "Corriente": "Orgánico cargado",
                "Tipo": "Salida",
                f"{'Volumen' if modo_laboratorio else 'Caudal'} [{unidad_volumen}]": org_flow * (factor_volumen if modo_laboratorio else 1),
                "Cu [g/L]": cu_org_cargado,
                f"Masa Cu [{unidad_masa}]":
                    convertir_resultado_extraccion(
                        masa_org_cargado, unidad_masa, modo_laboratorio
                    )
            }
        ]

        tabla_masa = pd.DataFrame(datos_masa)

        st.dataframe(
            tabla_masa.style.format({
                f"{'Volumen' if modo_laboratorio else 'Caudal'} [{unidad_volumen}]": "{:,.2f}",
                "Cu [g/L]": "{:,.2f}",
                f"Masa Cu [{unidad_masa}]": "{:,.2f}"
            }),
            hide_index=True,
            use_container_width=True
        )

        descargar_tabla_excel(tabla_masa, "SX_tabla_04.xlsx", "sx_tabla_04")

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
            (r"m_{Cu,\ entrada}=m_{Cu,\ salida}" if modo_laboratorio else r"\dot{m}_{Cu,\ entrada}=\dot{m}_{Cu,\ salida}")
        )

        st.latex(
            (r"m_{Cu,\ PLS}+m_{Cu,\ org.\ desc.}=m_{Cu,\ refino}+m_{Cu,\ org.\ carg.}"
             if modo_laboratorio else
            r"\dot{m}_{Cu,\ PLS}"
            r"+\dot{m}_{Cu,\ org.\ desc.}"
            r"="
            r"\dot{m}_{Cu,\ refino}"
            r"+\dot{m}_{Cu,\ org.\ carg.}")
        )

        masa_entrada_unidad = convertir_resultado_extraccion(
            masa_entrada,
            unidad_masa, modo_laboratorio
        )

        masa_salida_unidad = convertir_resultado_extraccion(
            masa_salida,
            unidad_masa, modo_laboratorio
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

        diferencia_unidad = convertir_resultado_extraccion(
            diferencia_masa,
            unidad_masa, modo_laboratorio
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
        # 7. BALANCE ORIGINAL EN t/h
        # ====================================================

        st.markdown("---")

        st.markdown(
            "### 6. Balance de Cobre en g" if modo_laboratorio else "### 6. Balance de Cobre en t/h"
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
            f"Cu [{'g' if modo_laboratorio else 't/h'}]": [
                resultados["cobre_pls"] * (1_000_000 if modo_laboratorio else 1),
                flujo_cobre(
                    org_flow,
                    cu_org_desc
                ) * (1_000_000 if modo_laboratorio else 1),
                resultados["cobre_refino"] * (1_000_000 if modo_laboratorio else 1),
                flujo_cobre(
                    org_flow,
                    cu_org_cargado
                ) * (1_000_000 if modo_laboratorio else 1)
            ]
        })

        st.dataframe(
            tabla,
            hide_index=True,
            use_container_width=True
        )

        descargar_tabla_excel(tabla, "SX_tabla_05.xlsx", "sx_tabla_05")

        mostrar_cierre(
            resultados["cierre"]
        )

        st.caption(
            ("En modo laboratorio las cantidades son masas totales, "
             "no flujos másicos. " if modo_laboratorio else "") +
            "Se supone que los caudales volumétricos "
            "de cada fase permanecen constantes y "
            "que no existen pérdidas ni arrastres. "
            "La concentración del orgánico cargado "
            "se obtiene mediante balance de masa; "
            "no se verifica su capacidad máxima "
            "de carga ni el equilibrio químico. " +
            ("Las cantidades mostradas son masas de cobre."
             if modo_laboratorio else
             "Las masas mostradas son flujos másicos "
             "de cobre por unidad de tiempo, no "
             "masas totales acumuladas.")
        )

        # ====================================================
        # EXPLICACIÓN DEL RESULTADO CON IA
        # ====================================================
        st.markdown("---")
        st.markdown("### 🤖 Explicación del resultado con IA")
        st.write(
            "Solicita al asistente metalúrgico una interpretación "
            "del balance de cobre y de las concentraciones de las corrientes SX."
        )

        firma_ia_ex = (
            modo_calculo, unidad_volumen, corriente_a_calcular,
            round(pls_flow, 12), round(org_flow, 12),
            round(cu_pls, 12), round(cu_raff, 12),
            round(cu_org_desc, 12), round(cu_org_cargado, 12),
            unidad_masa,
        )
        if st.session_state.get("sx_ex_ia_firma") != firma_ia_ex:
            st.session_state["sx_ex_ia_firma"] = firma_ia_ex
            st.session_state.pop("sx_ex_ia_respuesta", None)
            st.session_state.pop("sx_ex_ia_modelo", None)

        if st.button(
            "🤖 Explicar resultado con IA",
            key="sx_ex_boton_explicar_ia",
            use_container_width=True,
        ):
            try:
                from modulos.asistente import (
                    obtener_api_key,
                    generar_respuesta,
                    interpretar_error,
                )

                prompt = (
                    "Actúa como asistente académico especializado en "
                    "hidrometalurgia y extracción por solventes (SX). "
                    "Interpreta los resultados siguientes en español, con rigor "
                    "técnico y sin inventar datos. No cambies los cálculos.\n\n"
                    f"Corriente cuya concentración se calculó: {corriente_a_calcular}\n"
                    f"{'Volumen' if modo_laboratorio else 'Caudal'} de fase acuosa: "
                    f"{pls_flow * factor_volumen if modo_laboratorio else pls_flow:.2f} {unidad_volumen}\n"
                    f"{'Volumen' if modo_laboratorio else 'Caudal'} de fase orgánica: "
                    f"{org_flow * factor_volumen if modo_laboratorio else org_flow:.2f} {unidad_volumen}\n"
                    f"Concentración Cu en PLS: {cu_pls:.2f} g/L\n"
                    f"Concentración Cu en refino: {cu_raff:.2f} g/L\n"
                    f"Concentración Cu en orgánico descargado: {cu_org_desc:.2f} g/L\n"
                    f"Concentración Cu en orgánico cargado: {cu_org_cargado:.2f} g/L\n"
                    f"Cobre total de entrada: {masa_entrada_unidad:.2f} {unidad_masa}\n"
                    f"Cobre total de salida: {masa_salida_unidad:.2f} {unidad_masa}\n"
                    f"Diferencia del balance: {diferencia_unidad:.2f} {unidad_masa}\n"
                    f"Recuperación de extracción calculada: {resultados['recuperacion']:.2f} %\n"
                    f"Cobre transferido: {masa_transferida_unidad:.2f} {unidad_masa}\n"
                    f"Relación A/O: {pls_flow / org_flow:.2f}\n\n"
                    "Explica el balance de cobre, la corriente calculada, "
                    "el significado de las concentraciones y los supuestos "
                    "del modelo. Interpreta las magnitudes usando las unidades "
                    "proporcionadas y no infieras recuperaciones experimentales no medidas."
                )
                prompt += INSTRUCCIONES_IA_SX
                prompt += (
                    "\n\nCRITERIOS ESPECÍFICOS PARA EXTRACCIÓN SX:\n"
                    "No menciones modos de cálculo, modalidades alternativas ni funciones ocultas. "
                    "En 1. Resultados, organiza los volúmenes de las fases, las cuatro "
                    "concentraciones de Cu, la concentración despejada, las masas de entrada "
                    "y salida y la diferencia del balance con sus unidades. Incluye "
                    "obligatoriamente la recuperación de extracción calculada, el cobre "
                    "transferido y la relación A/O que se entregan expresamente arriba. "
                    "No afirmes que estos indicadores faltan ni los recalcules; "
                    "distingue la recuperación calculada del modelo de una medición experimental. "
                    "En 2. Explicación metalúrgica, explica la transferencia de Cu desde "
                    "el PLS al orgánico mediante el extractante y la generación de refino; "
                    "distingue las corrientes de entrada y salida y describe el balance "
                    "de Cu como conservación de masa. "
                    "En 3. Análisis técnico, interpreta las diferencias entre Cu del PLS "
                    "y del refino y entre orgánico descargado y cargado; comenta el cierre "
                    "del balance como consecuencia del modelo y la hipótesis de volúmenes "
                    "constantes por fase. No afirmes equilibrio químico, selectividad, "
                    "cinética, extracción real medida ni eficiencia operacional a partir "
                    "del mero cierre matemático. Respeta que en modo laboratorio se usan "
                    "masas en g o kg y volúmenes en mL o L, NO flujos por hora. "
                    "En 4. Recomendaciones, propone verificar concentraciones analíticas, "
                    "volúmenes, muestreo de ambas fases y consistencia del balance, "
                    "sin imponer condiciones no entregadas. Evita confundir la relación "
                    "A/O con la recuperación de cobre."
                )
                api_key = obtener_api_key()
                if not api_key:
                    raise ValueError("No se encontró la clave API de Gemini.")
                indicador_ia = st.empty()
                try:
                    respuesta, modelo = generar_respuesta(
                        api_key=api_key, mensajes=[], pregunta=prompt, indicador=indicador_ia, tipo_asistente="calculadora"
                    )
                finally:
                    indicador_ia.empty()
                if not respuesta:
                    raise ValueError("El asistente no devolvió una respuesta.")
                st.session_state["sx_ex_ia_respuesta"] = respuesta
                st.session_state["sx_ex_ia_modelo"] = modelo
            except Exception as error:
                try:
                    mensaje = interpretar_error(error)
                except Exception:
                    mensaje = str(error)
                st.error(f"No se pudo generar la explicación con IA: {mensaje}")
                with st.expander("Ver detalles técnicos del error"):
                    st.code(f"{type(error).__name__}: {error}")

        if st.session_state.get("sx_ex_ia_respuesta"):
            st.markdown("#### 🤖 Interpretación del asistente")
            st.markdown(st.session_state["sx_ex_ia_respuesta"])
            if st.session_state.get("sx_ex_ia_modelo"):
                st.caption(
                    "Modelo utilizado: "
                    f"{st.session_state['sx_ex_ia_modelo']}"
                )

    # ========================================================
    # 2. REEXTRACCIÓN
    # ========================================================

    elif sub_sx == "Re-extracción":

        st.subheader("🔄 Módulo de Re-extracción (Stripping)")
        st.write(
            "Calcula la transferencia de cobre desde el orgánico cargado "
            "hacia el electrolito pobre, obteniendo orgánico descargado "
            "y electrolito rico mediante balance de cobre."
        )
        st.latex(
            r"CuR_{2(org)} + 2H^+_{(ac)}"
            r"\rightleftharpoons Cu^{2+}_{(ac)} + 2RH_{(org)}"
        )

        st.markdown("### 1. Parámetros de Operación")
        st.write(
            "Ingresa las cantidades de ambas fases y las concentraciones "
            "de tres corrientes. La cuarta se calculará automáticamente."
        )
        # El modo industrial permanece implementado, pero no se muestra en la interfaz.
        modo_calculo = "Laboratorio (volúmenes)"
        modo_laboratorio = modo_calculo == "Laboratorio (volúmenes)"
        unidad_volumen = (
            st.selectbox("Unidad de volumen de las soluciones", ["mL", "L"],
                         key="sx_re_unidad_volumen")
            if modo_laboratorio else "m³/h"
        )

        corriente_a_calcular = st.selectbox(
            "Concentración de cobre que deseas calcular",
            ["Electrolito rico", "Orgánico cargado", "Electrolito pobre", "Orgánico descargado"],
            key="sx_re_corriente_concentracion"
        )
        st.caption(
            "Ingresa las concentraciones de las otras tres corrientes. "
            "La seleccionada se determinará mediante balance de cobre."
        )
        st.markdown("#### Cálculo de fases mediante FA/FO")
        forma_ingreso_fases = st.radio(
            "¿Cómo deseas ingresar las fases?",
            ["Ingresar ambas fases manualmente", "Calcular ambas desde el total"],
            key="sx_re_forma_ingreso_fases"
        )
        if forma_ingreso_fases == "Calcular ambas desde el total":
            razon_ingresada = st.number_input(
                "Razón de flujo FA/FO", min_value=0.0, value=0.0,
                step=0.05, format="%.2f", key="sx_re_razon_fafo"
            )
            total_ingresado = st.number_input(
                ("Volumen total de las fases" if modo_laboratorio
                 else "Caudal total de las fases") + f" [{unidad_volumen}]",
                min_value=0.0, value=0.0, step=10.0, format="%.2f",
                key="sx_re_total_fases"
            )
            flujo_organico_ingresado = (
                total_ingresado / (1.0 + razon_ingresada)
            )
            flujo_acuoso_ingresado = total_ingresado - flujo_organico_ingresado

        col1, col2 = st.columns(2)
        concentraciones = {}
        campos_calculados = {}

        with col1:
            st.markdown("**Fase acuosa**")
            if forma_ingreso_fases == "Ingresar ambas fases manualmente":
                flujo_acuoso_ingresado = st.number_input(
                    ("Volumen de Electrolito" if modo_laboratorio
                     else "Caudal de Electrolito") + f" [{unidad_volumen}]",
                    min_value=0.0, value=0.0, step=10.0, format="%.2f",
                    key="sx_re_q_electrolito"
                )
            for nombre, etiqueta in [
                ("Electrolito pobre", "Concentración Cu en Electrolito Pobre [g/L]"),
                ("Electrolito rico", "Concentración Cu en Electrolito Rico [g/L]")
            ]:
                if corriente_a_calcular == nombre:
                    campos_calculados[nombre] = st.empty()
                else:
                    concentraciones[nombre] = st.number_input(
                        etiqueta, min_value=0.0, value=0.0, step=0.1,
                        format="%.2f", key="sx_re_cu_" + nombre.replace(" ", "_").lower()
                    )

        with col2:
            st.markdown("**Fase orgánica**")
            if forma_ingreso_fases == "Ingresar ambas fases manualmente":
                flujo_organico_ingresado = st.number_input(
                    ("Volumen de Orgánico" if modo_laboratorio
                     else "Caudal de Orgánico") + f" [{unidad_volumen}]",
                    min_value=0.0, value=0.0, step=10.0, format="%.2f",
                    key="sx_re_q_organico"
                )
            for nombre, etiqueta in [
                ("Orgánico cargado", "Cu en Orgánico Cargado [g/L]"),
                ("Orgánico descargado", "Cu en Orgánico Descargado [g/L]")
            ]:
                if corriente_a_calcular == nombre:
                    campos_calculados[nombre] = st.empty()
                else:
                    concentraciones[nombre] = st.number_input(
                        etiqueta, min_value=0.0, value=0.0, step=0.1,
                        format="%.2f", key="sx_re_cu_" + nombre.replace(" ", "_").lower()
                    )
            unidad_masa = st.selectbox(
                "Unidad de masa de cobre" if modo_laboratorio
                else "Unidad de masa de cobre transportada",
                ["g", "kg"] if modo_laboratorio else ["kg/h", "t/h", "g/h"],
                key="sx_re_unidad_masa_lab" if modo_laboratorio else "sx_re_unidad_masa"
            )

        if forma_ingreso_fases == "Calcular ambas desde el total":
            st.markdown("**Fases calculadas automáticamente**")
            fa, fo = st.columns(2)
            fa.metric(f"Fase acuosa (FA) [{unidad_volumen}]", f"{flujo_acuoso_ingresado:,.2f}")
            fo.metric(f"Fase orgánica (FO) [{unidad_volumen}]", f"{flujo_organico_ingresado:,.2f}")

        factor_volumen = (
            1_000_000.0 if unidad_volumen == "mL" else 1000.0
        ) if modo_laboratorio else 1.0
        q_a = flujo_acuoso_ingresado / factor_volumen
        q_o = flujo_organico_ingresado / factor_volumen
        datos_validos = q_a > 0 and q_o > 0

        # Balance: Qorg*Corg,carg + Qa*Cep = Qorg*Corg,desc + Qa*Cer.
        # Los valores iniciales se muestran sin ocultar ningún apartado.
        if datos_validos:
            cc = concentraciones.get("Orgánico cargado")
            cd = concentraciones.get("Orgánico descargado")
            cp = concentraciones.get("Electrolito pobre")
            cr = concentraciones.get("Electrolito rico")
            if corriente_a_calcular == "Electrolito rico":
                cr = cp + (q_o / q_a) * (cc - cd)
            elif corriente_a_calcular == "Electrolito pobre":
                cp = cr - (q_o / q_a) * (cc - cd)
            elif corriente_a_calcular == "Orgánico cargado":
                cc = cd + (q_a / q_o) * (cr - cp)
            else:
                cd = cc - (q_a / q_o) * (cr - cp)
            concentraciones.update({
                "Orgánico cargado": cc, "Orgánico descargado": cd,
                "Electrolito pobre": cp, "Electrolito rico": cr
            })
            if any(v < -1e-9 for v in concentraciones.values()):
                st.error("El balance produce una concentración negativa. Revisa los datos ingresados.")
                datos_validos = False
            elif cd > cc + 1e-9 or cr + 1e-9 < cp:
                st.error("Los datos no corresponden a una transferencia de cobre desde el orgánico al electrolito.")
                datos_validos = False
            else:
                with campos_calculados[corriente_a_calcular].container():
                    st.number_input(
                        f"Concentración Cu en {corriente_a_calcular} [g/L]",
                        value=float(max(0.0, concentraciones[corriente_a_calcular])),
                        format="%.2f", disabled=True,
                        key="sx_re_resultado_" + corriente_a_calcular.replace(" ", "_").lower()
                    )
        if not datos_validos:
            concentraciones = {nombre: 0.0 for nombre in [
                "Orgánico cargado", "Orgánico descargado",
                "Electrolito pobre", "Electrolito rico"
            ]}
            if q_a <= 0 or q_o <= 0:
                st.info("Ingresa caudales o volúmenes mayores que cero para habilitar los cálculos. Los apartados permanecen visibles.")

        cc = concentraciones["Orgánico cargado"]
        cd = concentraciones["Orgánico descargado"]
        cp = concentraciones["Electrolito pobre"]
        cr = concentraciones["Electrolito rico"]

        if datos_validos:
            st.metric(
                f"Concentración Cu calculada en {corriente_a_calcular}",
                f"{concentraciones[corriente_a_calcular]:,.2f} g/L"
            )

        corrientes = [
            ("Orgánico cargado", "Entrada", q_o, cc),
            ("Electrolito pobre", "Entrada", q_a, cp),
            ("Orgánico descargado", "Salida", q_o, cd),
            ("Electrolito rico", "Salida", q_a, cr)
        ]
        masas_kg = {nombre: flujo_cobre_kg_h(q, c)
                    for nombre, _, q, c in corrientes}
        entrada = masas_kg["Orgánico cargado"] + masas_kg["Electrolito pobre"]
        salida = masas_kg["Orgánico descargado"] + masas_kg["Electrolito rico"]
        transferido = masas_kg["Orgánico cargado"] - masas_kg["Orgánico descargado"]
        eficiencia = ((cc - cd) / cc * 100.0) if datos_validos and cc > 0 else 0.0
        relacion = (q_a / q_o) if datos_validos else 0.0
        mostrar_masa = lambda v: convertir_resultado_extraccion(v, unidad_masa, modo_laboratorio)

        st.markdown("---")
        st.markdown("### 2. Diagrama Interactivo de Re-extracción SX")
        st.write(
            "El diagrama representa las entradas de orgánico cargado y electrolito pobre, "
            "y las salidas de orgánico descargado y electrolito rico. "
            "Los valores se actualizan automáticamente."
        )
        # Diagrama específico de re-extracción; no altera el de extracción.
        def tarjeta_svg_re(nombre, x, y, q, c, color):
            masa = mostrar_masa(flujo_cobre_kg_h(q, c))
            volumen = q * factor_volumen if modo_laboratorio else q
            return f'''<g><rect x="{x}" y="{y}" width="270" height="130" rx="12" fill="#1d2430" stroke="{color}" stroke-width="2"/>
            <rect x="{x}" y="{y}" width="270" height="35" rx="12" fill="{color}" fill-opacity="0.14"/>
            <text x="{x+135}" y="{y+23}" text-anchor="middle" fill="{color}" font-size="14" font-weight="bold">{escape(nombre.upper())}</text>
            <text x="{x+15}" y="{y+58}" fill="#e5e7eb" font-size="14">{('Volumen' if modo_laboratorio else 'Caudal')}: {volumen:,.2f} {unidad_volumen}</text>
            <text x="{x+15}" y="{y+85}" fill="#e5e7eb" font-size="14">Cu: {c:,.2f} g/L</text>
            <text x="{x+15}" y="{y+112}" fill="#fff" font-size="14" font-weight="bold">Masa Cu: {masa:,.2f} {unidad_masa}</text></g>'''

        html_re = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"/>
        <style>html,body{{margin:0;background:transparent;font-family:Arial,sans-serif}}
        .contenedor{{background:#111722;border:1px solid #303948;border-radius:14px;padding:12px;overflow-x:auto}}
        svg{{display:block;width:100%;min-width:0;height:auto;max-height:470px}}</style></head><body>
        <div class="contenedor"><svg viewBox="0 0 900 440" xmlns="http://www.w3.org/2000/svg">
        <defs><marker id="flechaRe" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10z" fill="#38bdf8"/></marker></defs>
        {tarjeta_svg_re('Electrolito pobre',20,15,q_a,cp,'#38bdf8')}
        {tarjeta_svg_re('Electrolito rico',610,15,q_a,cr,'#60a5fa')}
        {tarjeta_svg_re('Orgánico cargado',20,295,q_o,cc,'#fbbf24')}
        {tarjeta_svg_re('Orgánico descargado',610,295,q_o,cd,'#34d399')}
        <rect x="325" y="170" width="250" height="100" rx="14" fill="#343c49" stroke="#e5e7eb" stroke-width="2"/>
        <text x="450" y="208" text-anchor="middle" fill="#fff" font-size="21" font-weight="bold">RE-EXTRACCIÓN</text>
        <text x="450" y="235" text-anchor="middle" fill="#cbd5e1" font-size="14">Transferencia de Cu</text>
        <g fill="none" stroke="#38bdf8" stroke-width="3" marker-end="url(#flechaRe)">
        <path d="M155 145 V200 H325"/><path d="M575 200 H745 V145"/>
        <path d="M155 295 V245 H325"/><path d="M575 245 H745 V295"/></g>
        </svg></div></body></html>'''
        components.html(html_re, height=500, scrolling=False)
        st.caption("Entradas: orgánico cargado y electrolito pobre. Salidas: orgánico descargado y electrolito rico.")
        st.info(
            f"La concentración de cobre de {corriente_a_calcular.lower()} "
            "se calcula automáticamente mediante el balance de masa de re-extracción. "
            "Los caudales o volúmenes de ambas fases se consideran "
            "constantes entre la entrada y la salida."
        )

        st.markdown("---")
        st.markdown("### 3. Resultados de Re-extracción")
        r1, r2 = st.columns(2)
        with r1:
            st.markdown(tarjeta_resultado(
                f"Cobre en {corriente_a_calcular}",
                f"{concentraciones[corriente_a_calcular]:.2f}", "g/L", "#3b82f6"
            ), unsafe_allow_html=True)
        with r2:
            st.markdown(tarjeta_resultado(
                "Re-extracción de Cu del Orgánico", f"{eficiencia:.2f}", "%", "#10b981"
            ), unsafe_allow_html=True)
        r3, r4 = st.columns(2)
        r3.metric("Cobre Transferido al Electrolito", f"{mostrar_masa(transferido):,.2f} {unidad_masa}")
        r4.metric("Relación A/O", f"{relacion:.2f}")

        st.markdown("---")
        st.markdown("### 4. Cálculo de Masa de Cobre Transportada")
        st.markdown("#### Masa de cobre por corriente" if modo_laboratorio
                    else "#### Flujo másico de cobre por corriente")
        nombre_caudal = f"{'Volumen' if modo_laboratorio else 'Caudal'} [{unidad_volumen}]"
        tabla_masa = pd.DataFrame([
            {"Corriente": nombre, "Tipo": tipo,
             nombre_caudal: q * factor_volumen,
             "Cu [g/L]": c, f"Masa Cu [{unidad_masa}]": mostrar_masa(masas_kg[nombre])}
            for nombre, tipo, q, c in corrientes
        ])
        st.dataframe(tabla_masa.style.format({
            nombre_caudal: "{:,.2f}", "Cu [g/L]": "{:,.2f}",
            f"Masa Cu [{unidad_masa}]": "{:,.2f}"
        }), hide_index=True, use_container_width=True)

        descargar_tabla_excel(tabla_masa, "SX_tabla_06.xlsx", "sx_tabla_06")

        st.markdown("---")
        st.markdown("### 5. Balance de Cobre")
        st.metric("Cobre de entrada", f"{mostrar_masa(entrada):,.2f} {unidad_masa}")
        st.metric("Cobre de salida", f"{mostrar_masa(salida):,.2f} {unidad_masa}")
        st.metric("Diferencia del balance", f"{mostrar_masa(entrada-salida):,.2f} {unidad_masa}")
        if datos_validos and abs(entrada - salida) < 1e-8:
            st.success("El balance de masa de cobre se encuentra cerrado correctamente.")

        st.markdown("---")
        st.markdown("### 6. Balance de Cobre en g" if modo_laboratorio
                    else "### 6. Balance de Cobre en t/h")
        unidad_balance = "g" if modo_laboratorio else "t/h"
        tabla_balance = pd.DataFrame([
            {"Corriente": nombre, "Tipo": tipo,
             f"Cu [{unidad_balance}]": masas_kg[nombre] * (1000.0 if modo_laboratorio else 0.001)}
            for nombre, tipo, _, _ in corrientes
        ])
        st.dataframe(tabla_balance.style.format({f"Cu [{unidad_balance}]": "{:,.2f}"}),
                     hide_index=True, use_container_width=True)

        descargar_tabla_excel(tabla_balance, "SX_tabla_07.xlsx", "sx_tabla_07")
        st.caption(
            "Se suponen cantidades constantes de cada fase, sin pérdidas ni arrastres. "
            "El balance no verifica el equilibrio químico ni la capacidad de re-extracción."
        )

        st.markdown("---")
        st.markdown("### 🤖 Explicación del resultado con IA")
        st.write(
            "Solicita al asistente metalúrgico una interpretación de las concentraciones, "
            "la transferencia de cobre y el balance de re-extracción SX."
        )
        firma_ia_re = (
            modo_calculo, unidad_volumen, corriente_a_calcular,
            round(q_a, 12), round(q_o, 12),
            *(round(concentraciones[nombre], 12) for nombre in [
                "Orgánico cargado", "Orgánico descargado", "Electrolito pobre", "Electrolito rico"
            ]), unidad_masa
        )
        if st.session_state.get("sx_re_ia_firma") != firma_ia_re:
            st.session_state["sx_re_ia_firma"] = firma_ia_re
            st.session_state.pop("sx_re_ia_respuesta", None)
            st.session_state.pop("sx_re_ia_modelo", None)
        if st.button("🤖 Explicar resultado con IA", key="sx_re_boton_explicar_ia",
                     use_container_width=True, disabled=not datos_validos):
            try:
                from modulos.asistente import obtener_api_key, generar_respuesta, interpretar_error
                prompt = (
                    "Actúa como asistente académico especializado en hidrometalurgia y "
                    "re-extracción de cobre por solventes (SX). Explica los siguientes "
                    "resultados en español, sin inventar datos ni cambiar los cálculos. "
                    "Distingue la transferencia desde el orgánico al electrolito y "
                    "aclara que un balance cerrado no demuestra equilibrio químico.\n\n"
                    f"Concentración calculada: {corriente_a_calcular}\n"
                    f"Fase acuosa: {flujo_acuoso_ingresado:.2f} {unidad_volumen}\n"
                    f"Fase orgánica: {flujo_organico_ingresado:.2f} {unidad_volumen}\n"
                    f"Orgánico cargado: {cc:.2f} g/L\n"
                    f"Orgánico descargado: {cd:.2f} g/L\n"
                    f"Electrolito pobre: {cp:.2f} g/L\n"
                    f"Electrolito rico: {cr:.2f} g/L\n"
                    f"Cobre transferido: {mostrar_masa(transferido):.2f} {unidad_masa}\n"
                    f"Porcentaje de reextracción calculado: {eficiencia:.2f} %\n"
                    f"Relación A/O: {relacion:.2f}\n"
                    f"Diferencia del balance: {mostrar_masa(entrada-salida):.2f} {unidad_masa}"
                )
                prompt += INSTRUCCIONES_IA_SX
                prompt += (
                    "\n\nCRITERIOS ESPECÍFICOS PARA REEXTRACCIÓN SX:\n"
                    "No menciones modos de cálculo, modalidades alternativas ni funciones ocultas. "
                    "En 1. Resultados, presenta las concentraciones de orgánico cargado, "
                    "orgánico descargado, electrolito pobre y rico, la concentración "
                    "despejada, cobre transferido, porcentaje de reextracción del orgánico, "
                    "relación A/O y diferencia del balance, con las unidades proporcionadas. "
                    "Incluye obligatoriamente el porcentaje de reextracción calculado "
                    "que se entrega arriba, sin omitirlo, inventarlo ni recalcularlo. "
                    "En 2. Explicación metalúrgica, explica que el Cu pasa desde el orgánico "
                    "cargado al electrolito acuoso, enriqueciendo el electrolito y dejando "
                    "orgánico descargado para su recirculación; explica el balance de Cu "
                    "sin atribuir composiciones de reactivos no indicadas. "
                    "En 3. Análisis técnico, interpreta la disminución de Cu en el orgánico "
                    "y el aumento en el electrolito; distingue el porcentaje calculado "
                    "de reextracción del orgánico de una recuperación global del circuito. "
                    "Aclara que el cierre del balance es matemático y no verifica por sí "
                    "mismo equilibrio, cinética ni resultados experimentales. "
                    "Respeta que en laboratorio se manejan volúmenes y masas, no flujos "
                    "másicos horarios. En 4. Recomendaciones, sugiere contrastar las "
                    "concentraciones mediante análisis, revisar volúmenes, muestreo y "
                    "separación de fases cuando sea pertinente. No inventes pH, acidez, "
                    "temperatura, número de etapas ni eficiencias experimentales."
                )
                api_key = obtener_api_key()
                if not api_key:
                    raise ValueError("No se encontró la clave API de Gemini.")
                indicador_ia = st.empty()
                try:
                    respuesta, modelo = generar_respuesta(
                        api_key=api_key, mensajes=[], pregunta=prompt, indicador=indicador_ia, tipo_asistente="calculadora"
                    )
                finally:
                    indicador_ia.empty()
                if not respuesta:
                    raise ValueError("El asistente no devolvió una respuesta.")
                st.session_state["sx_re_ia_respuesta"] = respuesta
                st.session_state["sx_re_ia_modelo"] = modelo
            except Exception as error:
                try:
                    mensaje = interpretar_error(error)
                except Exception:
                    mensaje = str(error)
                st.error(f"No se pudo generar la explicación con IA: {mensaje}")
                with st.expander("Ver detalles técnicos del error"):
                    st.code(f"{type(error).__name__}: {error}")
        if not datos_validos:
            st.info("Ingresa datos válidos para habilitar la explicación con IA.")
        elif st.session_state.get("sx_re_ia_respuesta"):
            st.markdown("#### 🤖 Interpretación del asistente")
            st.markdown(st.session_state["sx_re_ia_respuesta"])
            if st.session_state.get("sx_re_ia_modelo"):
                st.caption(f"Modelo utilizado: {st.session_state['sx_re_ia_modelo']}")

    # ========================================================
    # 3. CIRCUITO COMPLETO
    # ========================================================

    elif sub_sx == "Circuito Completo":
        st.subheader("🌐 Circuito Completo de Extracción por Solventes (SX)")
        st.write("Balance integrado de extracción y re-extracción con un único ingreso de datos, diagrama, resultados y explicación con IA.")
        st.markdown("### 1. Parámetros de Operación")
        modo = "Laboratorio (volúmenes)"  # Modo industrial conservado en el código
        lab = modo == "Laboratorio (volúmenes)"
        uv = st.selectbox("Unidad de volumen", ["mL", "L"], key="sx_cc_unidad_volumen") if lab else "m³/h"
        um = st.selectbox("Unidad de masa de cobre", ["g", "kg"] if lab else ["kg/h", "t/h", "g/h"], key="sx_cc_unidad_masa")
        factor = (1_000_000.0 if uv == "mL" else 1000.0) if lab else 1.0
        st.markdown("#### Cálculo de fases mediante FA/FO")
        forma = st.radio("¿Cómo deseas ingresar las fases?", ["Ingresar ambas fases manualmente", "Calcular ambas desde el total"], key="sx_cc_forma_unica")
        if forma == "Calcular ambas desde el total":
            razon = st.number_input("Razón FA/FO de extracción", min_value=0.0, value=0.0, format="%.2f", key="sx_cc_razon_unica")
            total = st.number_input(f"{'Volumen' if lab else 'Caudal'} total de extracción [{uv}]", min_value=0.0, value=0.0, format="%.2f", key="sx_cc_total_unico")
            qa_ex = total * razon / (1 + razon)
            qo = total / (1 + razon)
        else:
            qa_ex = qo = None
        c1, c2, c3 = st.columns(3)
        with c1:
            if qa_ex is None:
                qa_ex = st.number_input(f"{'Volumen' if lab else 'Caudal'} de PLS [{uv}]", min_value=0.0, value=0.0, format="%.2f", key="sx_cc_pls_flujo")
            else:
                st.metric(f"PLS [{uv}]", f"{qa_ex:,.2f}")
        with c2:
            if qo is None:
                qo = st.number_input(f"{'Volumen' if lab else 'Caudal'} de orgánico [{uv}]", min_value=0.0, value=0.0, format="%.2f", key="sx_cc_org_flujo")
            else:
                st.metric(f"Orgánico [{uv}]", f"{qo:,.2f}")
        with c3:
            qa_re = st.number_input(f"{'Volumen' if lab else 'Caudal'} de electrolito [{uv}]", min_value=0.0, value=0.0, format="%.2f", key="sx_cc_electrolito_flujo")
        st.caption("El orgánico circula entre ambas operaciones: se utiliza una sola cantidad de fase orgánica.")

        st.markdown("#### Concentraciones de cobre del circuito")
        st.write("Selecciona una concentración a calcular en extracción y otra en re-extracción. Las demás se ingresan una sola vez.")
        ex_opciones = ["PLS", "Refino", "Orgánico descargado", "Orgánico cargado"]
        re_opciones = ["Electrolito pobre", "Electrolito rico", "Orgánico cargado", "Orgánico descargado"]
        objetivo_ex = st.selectbox("Concentración a calcular en extracción", ex_opciones, key="sx_cc_objetivo_ex_unico")
        # No se puede despejar dos veces la misma concentración del orgánico.
        opciones_re = [n for n in re_opciones if n != objetivo_ex]
        objetivo_re = st.selectbox("Concentración a calcular en re-extracción", opciones_re, key="sx_cc_objetivo_re_unico")
        nombres = ["PLS", "Refino", "Orgánico descargado", "Orgánico cargado", "Electrolito pobre", "Electrolito rico"]
        valores = {}
        izquierda, derecha = st.columns(2)
        for i, nombre in enumerate(nombres):
            with (izquierda if i < 3 else derecha):
                if nombre in (objetivo_ex, objetivo_re):
                    st.caption(f"Cu en {nombre} [g/L]: cálculo automático")
                else:
                    valores[nombre] = st.number_input(f"Cu en {nombre} [g/L]", min_value=0.0, value=0.0, format="%.2f", key="sx_cc_conc_" + nombre.replace(" ", "_"))

        q_pls, q_org, q_e = qa_ex / factor, qo / factor, qa_re / factor
        valido = all(q > 0 for q in (q_pls, q_org, q_e))
        # Dos ecuaciones independientes, una por operación, con las mismas
        # concentraciones del orgánico compartidas por todo el circuito.
        ecuaciones = [
            ({"PLS": q_pls, "Refino": -q_pls, "Orgánico descargado": q_org, "Orgánico cargado": -q_org}, 0.0),
            ({"Orgánico cargado": q_org, "Orgánico descargado": -q_org, "Electrolito pobre": q_e, "Electrolito rico": -q_e}, 0.0),
        ]
        desconocidas = [objetivo_ex, objetivo_re]
        if valido:
            import numpy as np
            matriz = np.array([[eq.get(n, 0.0) for n in desconocidas] for eq, _ in ecuaciones], dtype=float)
            terminos = np.array([-sum(coef * valores.get(n, 0.0) for n, coef in eq.items() if n not in desconocidas) for eq, _ in ecuaciones], dtype=float)
            if abs(np.linalg.det(matriz)) < 1e-12:
                st.warning("La combinación de concentraciones seleccionada no permite determinar ambas incógnitas. Cambia una de las dos selecciones.")
                valido = False
            else:
                solucion = np.linalg.solve(matriz, terminos)
                for n, v in zip(desconocidas, solucion):
                    valores[n] = float(v)
                if any(v < -1e-9 for v in valores.values()):
                    st.error("El balance genera concentraciones negativas. Revisa los datos ingresados.")
                    valido = False
        if not valido:
            for n in nombres:
                valores.setdefault(n, 0.0)
            st.info("Ingresa los tres caudales o volúmenes mayores que cero y selecciona incógnitas compatibles para calcular el circuito. Los apartados permanecen visibles.")
        else:
            r1, r2 = st.columns(2)
            for columna, n in zip((r1, r2), desconocidas):
                columna.metric(f"Concentración calculada en {n}", f"{valores[n]:,.2f} g/L")

        # Se muestran siempre las seis corrientes, incluso con datos iniciales en cero.
        caudales = {"PLS": q_pls, "Refino": q_pls, "Orgánico descargado": q_org, "Orgánico cargado": q_org, "Electrolito pobre": q_e, "Electrolito rico": q_e}
        masas = {n: caudales[n] * valores[n] for n in nombres}
        def convertir(v):
            return convertir_resultado_extraccion(v, um, lab)
        entrada_ex = masas["PLS"] + masas["Orgánico descargado"]
        salida_ex = masas["Refino"] + masas["Orgánico cargado"]
        entrada_re = masas["Orgánico cargado"] + masas["Electrolito pobre"]
        salida_re = masas["Orgánico descargado"] + masas["Electrolito rico"]
        entrada_global = masas["PLS"] + masas["Electrolito pobre"]
        salida_global = masas["Refino"] + masas["Electrolito rico"]
        transferido_ex = masas["PLS"] - masas["Refino"]
        transferido_re = masas["Electrolito rico"] - masas["Electrolito pobre"]
        rec_ex = 100 * transferido_ex / masas["PLS"] if masas["PLS"] > 0 else 0.0
        rec_re = 100 * transferido_re / masas["Orgánico cargado"] if masas["Orgánico cargado"] > 0 else 0.0
        rec_global = 100 * transferido_re / masas["PLS"] if masas["PLS"] > 0 else 0.0

        st.markdown("---")
        st.markdown("### 2. Diagrama Interactivo del Circuito Completo SX")
        st.write("Un solo circuito con las corrientes de extracción y re-extracción conectadas por la fase orgánica.")
        def caja(nombre, x, y, color):
            q = caudales[nombre] * factor
            return f'''<g><rect x="{x}" y="{y}" width="250" height="110" rx="10" fill="#1d2430" stroke="{color}" stroke-width="2"/><text x="{x+125}" y="{y+22}" text-anchor="middle" fill="{color}" font-size="14" font-weight="bold">{escape(nombre.upper())}</text><text x="{x+12}" y="{y+48}" fill="white" font-size="13">{'Volumen' if lab else 'Caudal'}: {q:,.2f} {uv}</text><text x="{x+12}" y="{y+72}" fill="white" font-size="13">Cu: {valores[nombre]:,.2f} g/L</text><text x="{x+12}" y="{y+96}" fill="white" font-size="13">Masa Cu: {convertir(masas[nombre]):,.2f} {um}</text></g>'''
        # Disposición basada en el esquema de circuito cerrado:
        # PLS -> EX -> refino; orgánico cargado -> RE -> orgánico descargado
        # -> EX; electrolito pobre -> RE -> electrolito rico.
        cajas = "".join([
            caja("PLS", 10, 175, "#38bdf8"),
            caja("Refino", 10, 440, "#60a5fa"),
            caja("Orgánico descargado", 330, 10, "#fbbf24"),
            caja("Orgánico cargado", 625, 440, "#34d399"),
            caja("Electrolito pobre", 1040, 175, "#38bdf8"),
            caja("Electrolito rico", 1040, 440, "#60a5fa"),
        ])
        html = f'''<!doctype html>
<html><head><meta charset="utf-8"><style>
body{{margin:0;background:transparent;font-family:Arial,sans-serif}}
.wrap{{background:#111722;border:1px solid #303948;border-radius:14px;overflow-x:auto;padding:12px}}
svg{{width:100%;min-width:1040px;height:auto}}
</style></head><body><div class="wrap">
<svg viewBox="0 0 1300 580" xmlns="http://www.w3.org/2000/svg">
<defs><marker id="flechaSX" markerWidth="9" markerHeight="9" refX="9" refY="5" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="#a5b4fc"/></marker></defs>
{cajas}
<rect x="330" y="235" width="250" height="110" rx="12" fill="#343c49" stroke="white"/>
<text x="455" y="297" text-anchor="middle" font-size="23" fill="white">EXTRACCIÓN</text>
<rect x="720" y="235" width="250" height="110" rx="12" fill="#343c49" stroke="white"/>
<text x="845" y="297" text-anchor="middle" font-size="23" fill="white">RE-EXTRACCIÓN</text>
<g stroke="#a5b4fc" stroke-width="3" fill="none" marker-end="url(#flechaSX)">
<!-- PLS alimenta extracción -->
<path d="M260 230 H330"/>
<!-- Refino sale de extracción -->
<path d="M390 345 V495 H260"/>
<!-- Orgánico descargado recirculado entra a extracción -->
<path d="M455 120 V235"/>
<!-- Orgánico cargado sale de extracción hacia re-extracción -->
<path d="M580 285 H720"/>
<!-- Electrolito pobre alimenta re-extracción -->
<path d="M1040 230 H970"/>
<!-- Electrolito rico sale de re-extracción -->
<path d="M915 345 V495 H1040"/>
<!-- Orgánico cargado: caja informativa conectada a la línea entre etapas -->
<path d="M650 285 V380 H750 V440"/>
<!-- Retorno del orgánico descargado desde re-extracción hacia su caja -->
<path d="M845 235 V145 H550 V120"/>
</g>
<text x="655" y="266" text-anchor="middle" fill="#cbd5e1" font-size="13">Orgánico cargado</text>
<text x="710" y="128" text-anchor="middle" fill="#cbd5e1" font-size="13">Retorno de orgánico descargado</text>
</svg></div></body></html>'''
        components.html(html, height=550, scrolling=True)

        st.markdown("---")
        st.markdown("### 3. Resultados del Circuito Completo")
        a, b = st.columns(2)
        a.markdown(tarjeta_resultado(f"Cobre en {objetivo_ex}", f"{valores[objetivo_ex]:.2f}", "g/L", "#3b82f6"), unsafe_allow_html=True)
        b.markdown(tarjeta_resultado(f"Cobre en {objetivo_re}", f"{valores[objetivo_re]:.2f}", "g/L", "#10b981"), unsafe_allow_html=True)
        c, d, e = st.columns(3)
        c.metric("Recuperación de extracción", f"{rec_ex:.2f} %")
        d.metric("Recuperación de re-extracción", f"{rec_re:.2f} %")
        e.metric("Recuperación global", f"{rec_global:.2f} %")
        c2, d2 = st.columns(2)
        c2.metric("Cu transferido en extracción", f"{convertir(transferido_ex):,.2f} {um}")
        d2.metric("Cu transferido a electrolito", f"{convertir(transferido_re):,.2f} {um}")

        st.markdown("---")
        st.markdown("### 4. Cálculo de Masa de Cobre Transportada")
        col_q = f"{'Volumen' if lab else 'Caudal'} [{uv}]"
        col_m = f"Masa Cu [{um}]"
        tipos = {"PLS": "Entrada", "Refino": "Salida", "Orgánico descargado": "Recirculación", "Orgánico cargado": "Recirculación", "Electrolito pobre": "Entrada", "Electrolito rico": "Salida"}
        tabla = pd.DataFrame([{"Corriente": n, "Tipo": tipos[n], col_q: caudales[n] * factor, "Cu [g/L]": valores[n], col_m: convertir(masas[n])} for n in nombres])
        st.dataframe(tabla.style.format({col_q:"{:,.2f}", "Cu [g/L]":"{:,.2f}", col_m:"{:,.2f}"}), hide_index=True, use_container_width=True)

        descargar_tabla_excel(tabla, "SX_tabla_08.xlsx", "sx_tabla_08")

        st.markdown("---")
        st.markdown("### 5. Balance de Cobre")
        b1, b2, b3 = st.columns(3)
        b1.metric("Cobre de entrada al circuito", f"{convertir(entrada_global):,.2f} {um}")
        b2.metric("Cobre de salida del circuito", f"{convertir(salida_global):,.2f} {um}")
        b3.metric("Diferencia del balance global", f"{convertir(entrada_global-salida_global):,.2f} {um}")
        resumen = pd.DataFrame([
            {"Balance": "Extracción", "Entrada": convertir(entrada_ex), "Salida": convertir(salida_ex), "Diferencia": convertir(entrada_ex-salida_ex)},
            {"Balance": "Re-extracción", "Entrada": convertir(entrada_re), "Salida": convertir(salida_re), "Diferencia": convertir(entrada_re-salida_re)},
            {"Balance": "Circuito completo", "Entrada": convertir(entrada_global), "Salida": convertir(salida_global), "Diferencia": convertir(entrada_global-salida_global)}
        ])
        st.dataframe(resumen.style.format({"Entrada":"{:,.2f}","Salida":"{:,.2f}","Diferencia":"{:,.2f}"}), hide_index=True, use_container_width=True)

        descargar_tabla_excel(resumen, "SX_tabla_09.xlsx", "sx_tabla_09")
        if valido and abs(entrada_global-salida_global) < 1e-8:
            st.success("Balance global de cobre cerrado correctamente.")

        st.markdown("---")
        st.markdown("### 6. Balance de Cobre en g" if lab else "### 6. Balance de Cobre en t/h")
        ub = "g" if lab else "t/h"
        tabla_balance = pd.DataFrame([{"Corriente": n, "Tipo": tipos[n], f"Cu [{ub}]": masas[n] * (1000.0 if lab else 0.001)} for n in nombres])
        st.dataframe(tabla_balance.style.format({f"Cu [{ub}]":"{:,.2f}"}), hide_index=True, use_container_width=True)

        descargar_tabla_excel(tabla_balance, "SX_tabla_10.xlsx", "sx_tabla_10")
        st.caption("Balance ideal sin pérdidas, arrastres ni variaciones de volumen. La recirculación orgánica se considera cerrada; no se comprueba el equilibrio químico.")

        st.markdown("---")
        st.markdown("### 🤖 Explicación del resultado con IA")
        st.write("Solicita al asistente metalúrgico una interpretación conjunta de extracción, re-extracción y del balance global de cobre.")
        firma = (modo, uv, um, q_pls, q_org, q_e, objetivo_ex, objetivo_re, tuple(valores[n] for n in nombres))
        if st.session_state.get("sx_cc_ia_firma_unica") != firma:
            st.session_state["sx_cc_ia_firma_unica"] = firma
            st.session_state.pop("sx_cc_ia_respuesta_unica", None)
            st.session_state.pop("sx_cc_ia_modelo_unico", None)
        if st.button("🤖 Explicar resultado con IA", key="sx_cc_ia_boton_unico", disabled=not valido, use_container_width=True):
            try:
                from modulos.asistente import obtener_api_key, generar_respuesta, interpretar_error
                prompt = ("Actúa como asistente metalúrgico especializado en SX. Interpreta el circuito completo de extracción y re-extracción como un solo sistema. No inventes datos ni alteres resultados. "
                          f"Modo: {modo}. PLS: {qa_ex:.2f} {uv}; orgánico: {qo:.2f} {uv}; electrolito: {qa_re:.2f} {uv}. "
                          + "; ".join(f"{n}: {valores[n]:.2f} g/L" for n in nombres)
                          + f". Recuperación extracción: {rec_ex:.2f} %. Re-extracción: {rec_re:.2f} %. Recuperación global: {rec_global:.2f} %. "
                          + f"Diferencia del balance global: {convertir(entrada_global-salida_global):.2f} {um}. Explica las limitaciones de un balance ideal.")
                prompt += INSTRUCCIONES_IA_SX
                api_key = obtener_api_key()
                if not api_key:
                    raise ValueError("No se encontró la clave API de Gemini.")
                indicador_ia = st.empty()
                try:
                    respuesta, modelo = generar_respuesta(
                        api_key=api_key, mensajes=[], pregunta=prompt, indicador=indicador_ia, tipo_asistente="calculadora"
                    )
                finally:
                    indicador_ia.empty()
                if not respuesta:
                    raise ValueError("El asistente no devolvió una respuesta.")
                st.session_state["sx_cc_ia_respuesta_unica"] = respuesta
                st.session_state["sx_cc_ia_modelo_unico"] = modelo
            except Exception as error:
                try:
                    mensaje = interpretar_error(error)
                except Exception:
                    mensaje = str(error)
                st.error(f"No se pudo generar la explicación con IA: {mensaje}")
                with st.expander("Ver detalles técnicos del error"):
                    st.code(f"{type(error).__name__}: {error}")
        if st.session_state.get("sx_cc_ia_respuesta_unica"):
            st.markdown(st.session_state["sx_cc_ia_respuesta_unica"])
            if st.session_state.get("sx_cc_ia_modelo_unico"):
                st.caption(f"Modelo utilizado: {st.session_state['sx_cc_ia_modelo_unico']}")

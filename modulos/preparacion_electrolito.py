
import streamlit as st
from html import escape


# ============================================================
# CONSTANTES QUÍMICAS
# ============================================================

MASA_MOLAR_CU = 63.55
MASA_MOLAR_CUSO4_5H2O = 249.68
MASA_MOLAR_H2SO4 = 98.079


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def formatear_numero(valor, decimales=2):
    """
    Formatea números utilizando coma decimal
    y punto como separador de miles.
    """

    numero = f"{valor:,.{decimales}f}"

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
    Genera una tarjeta de resultados mediante HTML.

    El HTML se construye sin indentación inicial
    para evitar que Streamlit lo interprete
    como un bloque de código.
    """

    titulo = escape(str(titulo))
    valor = escape(str(valor))
    unidad = escape(str(unidad))
    descripcion = escape(str(descripcion))

    return (
        f'<div style="'
        f'background:#1e2430;'
        f'border:1px solid #374151;'
        f'border-top:4px solid {color};'
        f'border-radius:14px;'
        f'padding:24px 14px;'
        f'text-align:center;'
        f'min-height:185px;'
        f'box-sizing:border-box;'
        f'">'
        f'<div style="'
        f'font-size:15px;'
        f'font-weight:600;'
        f'color:#cbd5e1;'
        f'margin-bottom:15px;'
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

def calcular_preparacion_electrolito(
    volumen_l,
    concentracion_cobre,
    concentracion_acido,
    pureza_acido,
    densidad_acido
):
    """
    Calcula los reactivos necesarios para preparar
    una solución electrolítica de cobre y ácido sulfúrico.

    Parámetros:
    - volumen_l: volumen final en litros.
    - concentracion_cobre: Cu2+ en g/L.
    - concentracion_acido: H2SO4 en g/L.
    - pureza_acido: porcentaje de H2SO4 comercial.
    - densidad_acido: densidad en g/mL.

    Se considera CuSO4·5H2O puro.
    """

    # --------------------------------------------------------
    # MASA DE COBRE
    # --------------------------------------------------------

    masa_cobre_g = (
        concentracion_cobre * volumen_l
    )

    # --------------------------------------------------------
    # SULFATO DE COBRE PENTAHIDRATADO
    # --------------------------------------------------------

    masa_sulfato_g = (
        masa_cobre_g
        * MASA_MOLAR_CUSO4_5H2O
        / MASA_MOLAR_CU
    )

    # --------------------------------------------------------
    # MASA DE ÁCIDO SULFÚRICO PURO
    # --------------------------------------------------------

    masa_acido_puro_g = (
        concentracion_acido * volumen_l
    )

    # --------------------------------------------------------
    # MASA DE SOLUCIÓN COMERCIAL
    # --------------------------------------------------------

    masa_solucion_acido_g = (
        masa_acido_puro_g
        / (pureza_acido / 100.0)
    )

    # --------------------------------------------------------
    # VOLUMEN DE ÁCIDO COMERCIAL
    # --------------------------------------------------------

    volumen_acido_ml = (
        masa_solucion_acido_g
        / densidad_acido
    )

    return {
        "masa_cobre_g": masa_cobre_g,
        "masa_sulfato_g": masa_sulfato_g,
        "masa_acido_puro_g": masa_acido_puro_g,
        "masa_solucion_acido_g": masa_solucion_acido_g,
        "volumen_acido_ml": volumen_acido_ml
    }


# ============================================================
# PÁGINA DE PREPARACIÓN DE ELECTROLITO RICO
# ============================================================

def mostrar_preparacion_electrolito():

    st.title("🧪 Preparación de Electrolito Rico")

    st.write(
        "Esta calculadora permite determinar las cantidades "
        "de sulfato de cobre pentahidratado (CuSO₄·5H₂O) "
        "y ácido sulfúrico (H₂SO₄) necesarias para preparar "
        "un volumen definido de solución electrolítica."
    )

    st.info(
        "El cálculo considera la preparación de una solución "
        "a partir de reactivos químicos. No representa "
        "directamente el enriquecimiento industrial del "
        "electrolito mediante reextracción SX."
    )

    st.markdown("---")

    # ========================================================
    # 1. PARÁMETROS DE PREPARACIÓN
    # ========================================================

    st.header("1. Parámetros de Preparación")

    # --------------------------------------------------------
    # PRIMERA FILA: UNIDAD Y VOLUMEN
    # --------------------------------------------------------

    columna1, columna2 = st.columns(2)

    with columna1:

        unidad_volumen = st.selectbox(
            "Unidad de medida del volumen",
            options=["L", "mL"],
            index=0,
            key="prep_ew_unidad_volumen"
        )

    with columna2:

        if unidad_volumen == "L":

            volumen_ingresado = st.number_input(
                "Volumen final del electrolito [L]",
                min_value=0.001,
                value=1.0,
                step=0.5,
                format="%.3f",
                key="prep_ew_volumen_l"
            )

            volumen_l = volumen_ingresado

        else:

            volumen_ingresado = st.number_input(
                "Volumen final del electrolito [mL]",
                min_value=1.0,
                value=1000.0,
                step=100.0,
                format="%.2f",
                key="prep_ew_volumen_ml"
            )

            volumen_l = volumen_ingresado / 1000.0

    # --------------------------------------------------------
    # SEGUNDA FILA: CONCENTRACIONES
    # --------------------------------------------------------

    columna3, columna4 = st.columns(2)

    with columna3:

        concentracion_cobre = st.number_input(
            "Concentración objetivo de Cu²⁺ [g/L]",
            min_value=0.0,
            value=50.0,
            step=1.0,
            format="%.2f",
            key="prep_ew_cobre"
        )

    with columna4:

        concentracion_acido = st.number_input(
            "Concentración objetivo de H₂SO₄ [g/L]",
            min_value=0.0,
            value=170.0,
            step=5.0,
            format="%.2f",
            key="prep_ew_acido"
        )

    # --------------------------------------------------------
    # TERCERA FILA: PROPIEDADES DEL ÁCIDO
    # --------------------------------------------------------

    columna5, columna6 = st.columns(2)

    with columna5:

        pureza_acido = st.number_input(
            "Pureza del H₂SO₄ comercial [%]",
            min_value=0.01,
            max_value=100.0,
            value=97.0,
            step=0.5,
            format="%.2f",
            key="prep_ew_pureza_acido"
        )

    with columna6:

        densidad_acido = st.number_input(
            "Densidad del H₂SO₄ comercial [g/mL]",
            min_value=0.01,
            value=1.84,
            step=0.01,
            format="%.2f",
            key="prep_ew_densidad_acido"
        )

    # ========================================================
    # CÁLCULOS INTERNOS
    # ========================================================

    resultados = calcular_preparacion_electrolito(
        volumen_l=volumen_l,
        concentracion_cobre=concentracion_cobre,
        concentracion_acido=concentracion_acido,
        pureza_acido=pureza_acido,
        densidad_acido=densidad_acido
    )

    st.markdown("---")

    # ========================================================
    # 2. RESULTADOS DE PREPARACIÓN
    # ========================================================

    st.header("2. Resultados de Preparación")

    st.write(
        "Cantidades de reactivos necesarias para alcanzar "
        "las concentraciones seleccionadas."
    )

    resultado1, resultado2, resultado3 = st.columns(
        3,
        gap="medium"
    )

    # --------------------------------------------------------
    # TARJETA 1: SULFATO DE COBRE
    # --------------------------------------------------------

    with resultado1:

        st.markdown(
            tarjeta_resultado(
                titulo="🧪 CuSO₄·5H₂O requerido",
                valor=formatear_numero(
                    resultados["masa_sulfato_g"]
                ),
                unidad="gramos (g)",
                color="#22c55e",
                descripcion="Sulfato de cobre pentahidratado"
            ),
            unsafe_allow_html=True
        )

    # --------------------------------------------------------
    # TARJETA 2: ÁCIDO SULFÚRICO
    # --------------------------------------------------------

    with resultado2:

        st.markdown(
            tarjeta_resultado(
                titulo="💧 H₂SO₄ comercial requerido",
                valor=formatear_numero(
                    resultados["volumen_acido_ml"]
                ),
                unidad="mililitros (mL)",
                color="#38bdf8",
                descripcion="Volumen de ácido comercial"
            ),
            unsafe_allow_html=True
        )

    # --------------------------------------------------------
    # TARJETA 3: MASA DE SOLUCIÓN ÁCIDA
    # --------------------------------------------------------

    with resultado3:

        st.markdown(
            tarjeta_resultado(
                titulo="⚖️ Masa de solución ácida",
                valor=formatear_numero(
                    resultados["masa_solucion_acido_g"]
                ),
                unidad="gramos (g)",
                color="#fbbf24",
                descripcion="Masa total de ácido comercial"
            ),
            unsafe_allow_html=True
        )

    st.caption(
        "Los resultados se actualizan automáticamente "
        "al modificar los parámetros de preparación."
    )

    st.markdown("---")

    # ========================================================
    # 3. RESUMEN DE REACTIVOS
    # ========================================================

    st.header("3. Resumen de Reactivos")

    st.table(
        {
            "Reactivo": [
                "Sulfato de cobre pentahidratado",
                "Ácido sulfúrico comercial"
            ],
            "Cantidad requerida": [
                (
                    f"{formatear_numero(resultados['masa_sulfato_g'])} g"
                ),
                (
                    f"{formatear_numero(resultados['volumen_acido_ml'])} mL"
                )
            ]
        }
    )

    st.markdown("#### Condiciones de Preparación")

    resumen1, resumen2 = st.columns(2)

    with resumen1:

        st.write(
            "**Volumen final objetivo:** "
            f"{formatear_numero(volumen_ingresado)} "
            f"{unidad_volumen}"
        )

        st.write(
            "**Volumen equivalente:** "
            f"{formatear_numero(volumen_l, 3)} L"
        )

    with resumen2:

        st.write(
            "**Concentración de Cu²⁺:** "
            f"{formatear_numero(concentracion_cobre)} g/L"
        )

        st.write(
            "**Concentración de H₂SO₄:** "
            f"{formatear_numero(concentracion_acido)} g/L"
        )

    st.info(
        "El volumen ingresado corresponde al volumen "
        "final de la solución, no al volumen inicial "
        "de agua. Los volúmenes de los reactivos "
        "no deben sumarse directamente para determinar "
        "el volumen final."
    )

    st.warning(
        "Seguridad: la preparación de electrolitos "
        "con ácido sulfúrico concentrado requiere "
        "procedimientos de laboratorio autorizados, "
        "protección personal y control térmico. "
        "El ácido se incorpora lentamente al agua, "
        "nunca al revés. Los cálculos no sustituyen "
        "un procedimiento de seguridad."
    )

    st.caption(
        "Modelo de cálculo estequiométrico para "
        "preparación de soluciones. El sulfato de cobre "
        "pentahidratado se considera puro. No se "
        "contemplan impurezas adicionales, contracción "
        "de volumen ni cambios de densidad de la "
        "mezcla final."
    )

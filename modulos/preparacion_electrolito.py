
import streamlit as st
import pandas as pd
from html import escape

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

    # Evita división por cero cuando la pureza
    # todavía no ha sido ingresada.

    if pureza_acido > 0:

        masa_solucion_acido_g = (
            masa_acido_puro_g
            / (pureza_acido / 100.0)
        )

    else:

        masa_solucion_acido_g = 0.0

    # --------------------------------------------------------
    # VOLUMEN DE ÁCIDO COMERCIAL
    # --------------------------------------------------------

    # Evita división por cero cuando la densidad
    # todavía no ha sido ingresada.

    if densidad_acido > 0:

        volumen_acido_ml = (
            masa_solucion_acido_g
            / densidad_acido
        )

    else:

        volumen_acido_ml = 0.0

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
                min_value=0.0,
                value=0.0,
                step=0.5,
                format="%.2f",
                key="prep_ew_volumen_l"
            )

            volumen_l = volumen_ingresado

        else:

            volumen_ingresado = st.number_input(
                "Volumen final del electrolito [mL]",
                min_value=0.0,
                value=0.0,
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
            value=0.0,
            step=1.0,
            format="%.2f",
            key="prep_ew_cobre"
        )

    with columna4:

        concentracion_acido = st.number_input(
            "Concentración objetivo de H₂SO₄ [g/L]",
            min_value=0.0,
            value=0.0,
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
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=0.5,
            format="%.2f",
            key="prep_ew_pureza_acido"
        )

    with columna6:

        densidad_acido = st.number_input(
            "Densidad del H₂SO₄ comercial [g/mL]",
            min_value=0.0,
            value=0.0,
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

    tabla_reactivos = pd.DataFrame(
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
    st.table(tabla_reactivos)
    st.download_button(
        "📥 Exportar resumen de reactivos a Excel",
        data=_excel_desde_tabla(tabla_reactivos, "Reactivos EW"),
        file_name="preparacion_electrolito_reactivos.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="prep_ew_exportar_excel",
        use_container_width=True,
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

    # ========================================================
    # 4. EXPLICACIÓN DEL RESULTADO CON IA
    # ========================================================

    st.markdown("---")
    st.header("4. 🤖 Explicación del resultado con IA")
    st.write(
        "Solicita al asistente metalúrgico una explicación "
        "de las cantidades calculadas para preparar el electrolito rico."
    )

    datos_ia_validos = (
        volumen_l > 0
        and (concentracion_cobre > 0 or concentracion_acido > 0)
        and (
            concentracion_acido == 0
            or (pureza_acido > 0 and densidad_acido > 0)
        )
    )

    if st.button(
        "🤖 Explicar resultado con IA",
        key="prep_ew_explicar_resultado_ia",
        use_container_width=True,
        disabled=not datos_ia_validos
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
                "Añade solo la quinta sección de seguridad indicada abajo. "
                "No inventes mediciones. "
                "Respeta las cifras calculadas y las unidades originales. "
                "Distingue claramente las hipótesis de los datos medidos.\n\n"
                "Eres un asistente especializado en hidrometalurgia "
                "y preparación de electrolitos para electroobtención. "
                "Explica en español los resultados de esta calculadora, "
                "sin inventar datos y mostrando los valores con dos decimales.\n\n"
                f"Volumen final objetivo: {volumen_ingresado:.2f} {unidad_volumen}\n"
                f"Volumen equivalente para cálculo: {volumen_l:.8f} L\n"
                f"Concentración objetivo de Cu²⁺: {concentracion_cobre:.2f} g/L\n"
                f"Concentración objetivo de H₂SO₄: {concentracion_acido:.2f} g/L\n"
                f"Pureza del ácido comercial: {pureza_acido:.2f} %\n"
                f"Densidad del ácido comercial: {densidad_acido:.2f} g/mL\n"
                f"Masa de cobre objetivo: {resultados['masa_cobre_g']:.2f} g\n"
                f"Masa de CuSO₄·5H₂O requerida: {resultados['masa_sulfato_g']:.2f} g\n"
                f"Masa de H₂SO₄ puro: {resultados['masa_acido_puro_g']:.2f} g\n"
                f"Masa de solución ácida comercial: "
                f"{resultados['masa_solucion_acido_g']:.2f} g\n"
                f"Volumen de ácido comercial: "
                f"{resultados['volumen_acido_ml']:.2f} mL\n\n"
                "Explica el significado de las concentraciones objetivo, "
                "el uso de CuSO₄·5H₂O y cómo influyen la pureza y "
                "densidad del H₂SO₄ en las cantidades requeridas. "
                "Aclara que se trata de preparación a partir de reactivos "
                "y no de enriquecimiento industrial por SX; el sulfato "
                "de cobre se considera puro. No inventes condiciones "
                "experimentales ni supongas que la suma de volúmenes "
                "equivale al volumen final. Incluye una advertencia "
                "al final una quinta sección titulada "
                "'5. Advertencias de seguridad para la preparación'. "
                "Indica que el H₂SO₄ es corrosivo, que la dilución "
                "desprende calor, que se agrega lentamente ácido al agua "
                "y nunca agua al ácido, con protección personal y "
                "siguiendo los procedimientos del laboratorio. "
                "No supongas que el volumen inicial de agua es igual "
                "al volumen final de electrolito."
            )

            indicador_ia = st.empty()
            try:
                respuesta_ia, modelo_ia = generar_respuesta(
                    api_key=api_key,
                    mensajes=[],
                    pregunta=pregunta_ia,
                    indicador=indicador_ia
                )
                st.session_state["prep_ew_ia_respuesta"] = respuesta_ia
                st.session_state["prep_ew_ia_modelo"] = modelo_ia
            except Exception as error:
                st.error(interpretar_error(error))
                with st.expander("Ver detalles del error de IA"):
                    st.code(str(error))

    if not datos_ia_validos:
        st.info(
            "Ingresa un volumen final mayor que cero y al menos una "
            "concentración objetivo positiva. Si utilizas H₂SO₄, "
            "ingresa también su pureza y densidad para habilitar la IA."
        )
    elif st.session_state.get("prep_ew_ia_respuesta"):
        st.markdown("### 🤖 Interpretación del asistente")
        st.markdown(st.session_state["prep_ew_ia_respuesta"])
        if st.session_state.get("prep_ew_ia_modelo"):
            st.caption(
                f"Modelo utilizado: "
                f"{st.session_state['prep_ew_ia_modelo']}"
            )


import io
from html import escape

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# CONFIGURACIÓN DE MALLAS
# ============================================================

MALLAS_STD = {
    '1"': 25000.0,
    '3/4"': 19000.0,
    '1/2"': 12500.0,
    '3/8"': 9500.0,
    '5/16"': 8000.0,
    "4": 4750.0,
    "6": 3350.0,
    "10": 2000.0,
    "12": 1700.0,
    "14": 1400.0,
    "16": 1180.0,
    "18": 1000.0,
    "20": 850.0,
    "30": 600.0,
    "40": 425.0,
    "50": 300.0,
    "70": 212.0,
    "100": 150.0,
    "140": 106.0,
    "200": 75.0,
    "270": 53.0,
    "Fondo": 0.0
}


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def tarjeta_resultado(titulo, valor, unidad, color):
    """Genera una tarjeta HTML compacta."""

    titulo = escape(str(titulo))
    valor = escape(str(valor))
    unidad = escape(str(unidad))

    return (
        f'<div style="'
        f'background:linear-gradient(145deg,#202938,#151c29);'
        f'border:1px solid #344155;'
        f'border-top:3px solid {color};'
        f'border-radius:14px;'
        f'padding:22px;'
        f'text-align:center;'
        f'min-height:155px;'
        f'box-sizing:border-box;">'
        f'<div style="color:#aebdd0;font-size:.88rem;">'
        f'{titulo}</div>'
        f'<div style="color:{color};font-size:1.8rem;'
        f'font-weight:800;margin:12px 0 5px;'
        f'overflow-wrap:anywhere;">{valor}</div>'
        f'<div style="color:#cbd5e1;font-size:.84rem;">'
        f'{unidad}</div>'
        f'</div>'
    )


def calcular_t80(df):
    """
    Calcula T80 mediante interpolación logarítmica
    en ambos ejes: tamaño y porcentaje pasante.

    Se utilizan porcentajes pasantes redondeados a
    dos decimales, iguales a los mostrados en la tabla.

    Devuelve None si no es posible interpolar el 80%.
    """

    datos = df.loc[
        (df["Abertura [µm]"] > 0)
        & (df["Pasante acumulado [%]"] > 0),
        ["Abertura [µm]", "Pasante acumulado [%]"]
    ].copy()

    datos = datos.dropna()
    datos = datos.sort_values("Abertura [µm]")

    x = datos["Abertura [µm]"].to_numpy(dtype=float)

    # IMPORTANTE:
    # Se redondea a dos decimales para reproducir
    # el procedimiento manual con la tabla visible.
    y = np.round(
        datos["Pasante acumulado [%]"].to_numpy(dtype=float),
        2
    )

    if len(x) < 2:
        return None

    if not np.isfinite(x).all() or not np.isfinite(y).all():
        return None

    if 80 < y.min() or 80 > y.max():
        return None

    for i in range(len(x) - 1):

        x1, x2 = x[i], x[i + 1]
        y1, y2 = y[i], y[i + 1]

        if np.isclose(y1, 80):
            return float(x1)

        if np.isclose(y2, 80):
            return float(x2)

        if y1 < 80 < y2 and y2 > y1:

            # Interpolación logarítmica:
            #
            # (log(y2)-log(y1)) / (log(x2)-log(x1))
            # =
            # (log(80)-log(y1)) / (log(T80)-log(x1))

            log_t80 = np.log10(x1) + (
                (
                    np.log10(80.0)
                    - np.log10(y1)
                )
                /
                (
                    np.log10(y2)
                    - np.log10(y1)
                )
            ) * (
                np.log10(x2)
                - np.log10(x1)
            )

            return float(10 ** log_t80)

    return None


def usar_t80(clave_widget):
    """Transfiere T80 a Ley de Bond o Razón de Reducción."""

    t80 = st.session_state.get("t80_calculado")

    if t80 is None or t80 <= 0:
        return

    if clave_widget.startswith("rr_"):
        if st.session_state.get("rr_unidad", "µm") == "mm":
            t80 /= 1000.0

    st.session_state[clave_widget] = float(t80)


def convertir_unidad_rr():
    """Convierte ambos tamaños al cambiar de µm a mm."""

    nueva = st.session_state["rr_unidad"]

    anterior = st.session_state.get(
        "rr_unidad_anterior", "µm"
    )

    if nueva == anterior:
        return

    factor = 0.001 if nueva == "mm" else 1000.0

    for clave in ("rr_f80_input", "rr_p80_input"):
        st.session_state[clave] *= factor

    st.session_state["rr_unidad_anterior"] = nueva


# ============================================================
# 1. ETAPAS DE CHANCADO
# ============================================================

def mostrar_chancado():

    st.title("🔨 Fundamentos de Conminución")

    st.write(
        "El chancado es una operación mecánica que permite reducir "
        "progresivamente el tamaño de las rocas y minerales mediante "
        "fuerzas de compresión e impacto, con la finalidad de obtener "
        "una granulometría adecuada para las operaciones posteriores."
    )

    st.markdown("---")

    etapas = [
        {
            "titulo": "1. Chancado Primario",
            "color": "#3b82f6",
            "equipo": "Chancadores de mandíbulas y giratorios.",
            "alimentacion": (
                "Mineral proveniente de la mina, con fragmentos "
                "que pueden superar 1 m."
            ),
            "producto": "7–10 pulgadas, aproximadamente.",
            "extra_titulo": "RAZÓN DE REDUCCIÓN",
            "extra": "Mandíbulas: 3:1–5:1. Giratorios: 6:1–8:1.",
            "detalle": (
                "El chancador de mandíbulas utiliza una muela fija y "
                "otra móvil que comprimen el mineral. El giratorio "
                "emplea un cono que gira de forma excéntrica dentro "
                "de una carcasa y se utiliza principalmente para "
                "procesar grandes volúmenes de material."
            ),
        },
        {
            "titulo": "2. Chancado Secundario",
            "color": "#f59e0b",
            "equipo": "Chancadores de cono.",
            "alimentacion": (
                "Producto del chancado primario: 7–10 pulgadas."
            ),
            "producto": "2–4 pulgadas, aproximadamente.",
            "extra_titulo": "CAPACIDAD DE PROCESAMIENTO",
            "extra": "1.000–2.000 TPH, como referencia.",
            "detalle": (
                "Los chancadores de cono reducen el tamaño del mineral "
                "por compresión entre un elemento móvil y una cavidad "
                "fija. Esta etapa recibe material previamente "
                "fragmentado y prepara el producto para las "
                "operaciones posteriores."
            ),
        },
        {
            "titulo": "3. Chancado Terciario",
            "color": "#10b981",
            "equipo": (
                "Chancadores de cono de alta reducción y "
                "chancadores de impacto de eje vertical (VSI)."
            ),
            "alimentacion": (
                "Producto del chancado secundario: 2–4 pulgadas."
            ),
            "producto": "3/8–1/4 de pulgada, aproximadamente.",
            "extra_titulo": "CAPACIDAD DE PROCESAMIENTO",
            "extra": "500–1.500 TPH, como referencia.",
            "detalle": (
                "El chancado terciario busca obtener una granulometría "
                "más fina y controlada. Se emplean chancadores de cono "
                "de alta reducción o equipos VSI, de acuerdo con "
                "las necesidades del proceso posterior."
            ),
        },
    ]

    columnas = st.columns(3)

    for columna, etapa in zip(columnas, etapas):
        with columna:
            color = etapa["color"]
            titulo = escape(etapa["titulo"])
            equipo = escape(etapa["equipo"])
            alimentacion = escape(etapa["alimentacion"])
            producto = escape(etapa["producto"])
            extra_titulo = escape(etapa["extra_titulo"])
            extra = escape(etapa["extra"])

            tarjeta = (
                f'<div style="'
                f'background:linear-gradient(145deg,#202938,#151c29);'
                f'border:1px solid #344155;'
                f'border-top:4px solid {color};'
                f'border-radius:14px;'
                f'padding:22px;'
                f'min-height:410px;'
                f'box-sizing:border-box;'
                f'color:#f8fafc;">'
                f'<div style="font-size:1.3rem;'
                f'font-weight:750;margin-bottom:20px;">{titulo}</div>'
                f'<div style="font-size:.72rem;color:#94a3b8;'
                f'font-weight:700;letter-spacing:.7px;'
                f'margin-bottom:5px;">EQUIPOS PRINCIPALES</div>'
                f'<div style="font-size:.92rem;'
                f'margin-bottom:17px;">{equipo}</div>'
                f'<div style="border-top:1px solid #354052;'
                f'margin-bottom:16px;"></div>'
                f'<div style="font-size:.72rem;color:#94a3b8;'
                f'font-weight:700;letter-spacing:.7px;'
                f'margin-bottom:5px;">ALIMENTACIÓN</div>'
                f'<div style="font-size:.92rem;'
                f'margin-bottom:17px;">{alimentacion}</div>'
                f'<div style="font-size:.72rem;color:#94a3b8;'
                f'font-weight:700;letter-spacing:.7px;'
                f'margin-bottom:5px;">PRODUCTO</div>'
                f'<div style="font-size:.92rem;'
                f'margin-bottom:17px;">{producto}</div>'
                f'<div style="font-size:.72rem;color:#94a3b8;'
                f'font-weight:700;letter-spacing:.7px;'
                f'margin-bottom:5px;">{extra_titulo}</div>'
                f'<div style="font-size:.92rem;">{extra}</div>'
                f'</div>'
            )

            st.markdown(tarjeta, unsafe_allow_html=True)

            with st.expander(f"Funcionamiento: {etapa['titulo']}"):
                st.write(etapa["detalle"])

    st.caption(
        "Los tamaños, las razones de reducción y las capacidades "
        "indicados son referenciales. Los valores reales dependen "
        "del equipo, la configuración del circuito y las "
        "características del mineral."
    )


# ============================================================
# 2. ANÁLISIS GRANULOMÉTRICO
# ============================================================

def mostrar_granulometria():

    st.title("📊 Análisis Granulométrico")

    st.write(
        "Ingresa las masas de los tamices y del mineral "
        "para determinar la distribución granulométrica, "
        "la curva de porcentaje pasante y el T80."
    )

    # --------------------------------------------------------
    # INGRESO DE DATOS
    # --------------------------------------------------------

    columnas_antiguas = {
        "Peso tamiz [g]": "Masa tamiz [g]",
        "Peso tamiz + mineral [g]": "Masa tamiz + mineral [g]",
        "Peso mineral [g]": "Masa mineral [g]"
    }

    if "df_gran" not in st.session_state:

        st.session_state["df_gran"] = pd.DataFrame({
            "Malla": [
                "6", "10", "12", "14",
                "18", "30", "Fondo"
            ],
            "Masa tamiz [g]": [0.0] * 7,
            "Masa tamiz + mineral [g]": [0.0] * 7
        })

    else:

        df_guardado = st.session_state["df_gran"]

        if isinstance(df_guardado, pd.DataFrame):

            st.session_state["df_gran"] = df_guardado.rename(
                columns=columnas_antiguas
            ).copy()

    st.markdown("### 1. Ingreso de Datos")

    st.info(
        "Puedes agregar, eliminar o modificar filas. "
        "Selecciona las mallas utilizadas e ingresa "
        "las masas correspondientes."
    )

    df_editado = st.data_editor(
        st.session_state["df_gran"],
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config={
            "Malla": st.column_config.SelectboxColumn(
                "Malla",
                options=list(MALLAS_STD.keys()),
                required=True
            ),
            "Masa tamiz [g]": st.column_config.NumberColumn(
                "Masa tamiz [g]",
                min_value=0.0,
                format="%.2f"
            ),
            "Masa tamiz + mineral [g]":
                st.column_config.NumberColumn(
                    "Masa tamiz + mineral [g]",
                    min_value=0.0,
                    format="%.2f"
                )
        },
        key="editor_granulometria_masa"
    )

    # Se invalida el T80 anterior hasta recalcularlo.

    st.session_state["t80_calculado"] = None
    st.session_state.pop("df_granulometria_2", None)

    df_valido = df_editado.dropna(
        subset=["Malla"]
    ).copy()

    if df_valido.empty:
        st.warning("Ingresa al menos una malla.")
        return

    # --------------------------------------------------------
    # VALIDACIONES
    # --------------------------------------------------------

    if df_valido["Malla"].duplicated().any():

        st.error(
            "Existen mallas repetidas. "
            "Cada malla debe aparecer una sola vez."
        )

        return

    columnas_masa = [
        "Masa tamiz [g]",
        "Masa tamiz + mineral [g]"
    ]

    df_valido[columnas_masa] = (
        df_valido[columnas_masa]
        .apply(pd.to_numeric, errors="coerce")
    )

    if df_valido[columnas_masa].isna().any().any():

        st.error(
            "Todas las masas deben ser valores numéricos."
        )

        return

    if (df_valido[columnas_masa] < 0).any().any():

        st.error(
            "Las masas no pueden ser negativas."
        )

        return

    if (
        df_valido["Masa tamiz + mineral [g]"]
        < df_valido["Masa tamiz [g]"]
    ).any():

        st.error(
            "La masa del tamiz con mineral no puede "
            "ser menor que la masa del tamiz vacío."
        )

        return

    # --------------------------------------------------------
    # CÁLCULOS
    # --------------------------------------------------------

    df_valido["Abertura [µm]"] = (
        df_valido["Malla"].map(MALLAS_STD)
    )

    if df_valido["Abertura [µm]"].isna().any():

        st.error(
            "Se encontraron mallas no reconocidas."
        )

        return

    df_valido = df_valido.sort_values(
        "Abertura [µm]",
        ascending=False
    ).reset_index(drop=True)

    # Masa de mineral retenida en cada tamiz.

    df_valido["Masa mineral [g]"] = (
        df_valido["Masa tamiz + mineral [g]"]
        - df_valido["Masa tamiz [g]"]
    )

    # Masa total del mineral.

    masa_total = df_valido["Masa mineral [g]"].sum()

    if masa_total <= 0:

        st.warning(
            "Ingresa las masas de mineral para "
            "generar los resultados."
        )

        return

    # Porcentaje retenido parcial.

    df_valido["Retenido parcial [%]"] = (
        df_valido["Masa mineral [g]"]
        / masa_total * 100.0
    )

    # Porcentaje retenido acumulado.

    df_valido["Retenido acumulado [%]"] = (
        df_valido["Retenido parcial [%]"].cumsum()
    )

    # Porcentaje pasante acumulado.

    df_valido["Pasante acumulado [%]"] = (
        100.0 - df_valido["Retenido acumulado [%]"]
    ).clip(lower=0, upper=100)

    # --------------------------------------------------------
    # TABLA GRANULOMÉTRICA
    # --------------------------------------------------------

    st.markdown("---")

    st.markdown(
        "### 2. Tabla Granulométrica Calculada"
    )

    st.dataframe(
        df_valido.style.format({
            "Abertura [µm]": "{:.2f}",
            "Masa tamiz [g]": "{:.2f}",
            "Masa tamiz + mineral [g]": "{:.2f}",
            "Masa mineral [g]": "{:.2f}",
            "Retenido parcial [%]": "{:.2f}",
            "Retenido acumulado [%]": "{:.2f}",
            "Pasante acumulado [%]": "{:.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # T80: INTERPOLACIÓN LOGARÍTMICA CORREGIDA
    # --------------------------------------------------------

    df_curva = df_valido.loc[
        df_valido["Abertura [µm]"] > 0
    ].copy()

    t80 = calcular_t80(df_curva)

    st.markdown("---")

    st.markdown("### 3. Resultados y Gráfico")

    col1, col2 = st.columns(2)

    col1.metric(
        "Masa total de mineral",
        f"{masa_total:.2f} g"
    )

    if t80 is not None:

        st.session_state["t80_calculado"] = t80

        col2.metric(
            "T80 estimado",
            f"{t80:.2f} µm"
        )

        st.success(
            f"El T80 estimado es {t80:.2f} µm."
        )

    else:

        col2.metric(
            "T80 estimado",
            "No disponible"
        )

        st.warning(
            "No es posible interpolar el T80 con "
            "los datos disponibles. Se requieren "
            "valores que permitan ubicar el 80% "
            "pasante dentro del intervalo medido."
        )

    # --------------------------------------------------------
    # CURVA GRANULOMÉTRICA
    # --------------------------------------------------------

    if not df_curva.empty:

        df_grafico = df_curva.sort_values(
            "Abertura [µm]"
        )

        st.session_state["df_granulometria_2"] = (
            df_grafico[
                ["Abertura [µm]", "Pasante acumulado [%]"]
            ].copy()
        )

        fig = px.line(
            df_grafico,
            x="Abertura [µm]",
            y="Pasante acumulado [%]",
            log_x=True,
            markers=True,
            title="Curva Granulométrica"
        )

        fig.update_layout(
            xaxis_title="Abertura de malla [µm]",
            yaxis_title="Pasante acumulado [%]",
            yaxis_range=[0, 100],
            template="plotly_dark"
        )

        fig.add_hline(
            y=80,
            line_dash="dash",
            line_color="red",
            annotation_text="80% Pasante"
        )

        if t80 is not None:

            fig.add_vline(
                x=t80,
                line_dash="dash",
                line_color="red"
            )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # EXPORTACIÓN EN EXCEL
    # --------------------------------------------------------

    st.markdown("---")

    st.markdown("### 4. Exportar Datos")

    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="xlsxwriter"
    ) as writer:

        df_valido.to_excel(
            writer,
            index=False,
            sheet_name="Resultados"
        )

        workbook = writer.book
        worksheet = writer.sheets["Resultados"]

        formato_decimal = workbook.add_format({
            "num_format": "0.00"
        })

        worksheet.set_column(
            "B:H",
            20,
            formato_decimal
        )

        worksheet.set_column("A:A", 12)

        if len(df_curva) >= 2:

            chart = workbook.add_chart({
                "type": "scatter",
                "subtype": "straight_with_markers"
            })

            filas_grafico = len(df_curva)

            chart.add_series({
                "name": "Curva Granulométrica",
                "categories": [
                    "Resultados",
                    1, 3,
                    filas_grafico, 3
                ],
                "values": [
                    "Resultados",
                    1, 7,
                    filas_grafico, 7
                ],
                "marker": {
                    "type": "circle",
                    "size": 6
                },
                "line": {
                    "color": "#1f77b4",
                    "width": 1.5
                }
            })

            chart.set_title({
                "name": "Curva Granulométrica"
            })

            chart.set_x_axis({
                "name": "Abertura [µm]",
                "log_base": 10
            })

            chart.set_y_axis({
                "name": "Pasante acumulado [%]",
                "min": 0,
                "max": 100
            })

            worksheet.insert_chart(
                "J2",
                chart,
                {
                    "x_scale": 1.4,
                    "y_scale": 1.2
                }
            )

    st.download_button(
        "📥 Descargar Reporte en Excel",
        data=output.getvalue(),
        file_name="Reporte_Granulometria.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        use_container_width=True
    )

    # --------------------------------------------------------
    # EXPLICACIÓN DE RESULTADOS CON INTELIGENCIA ARTIFICIAL
    # --------------------------------------------------------

    st.markdown("---")

    st.markdown(
        "### 5. 🤖 Explicación del resultado con IA"
    )

    st.write(
        "Solicita al asistente metalúrgico una interpretación "
        "de la distribución granulométrica y del T80 calculado."
    )

    # Firma de datos para invalidar respuestas anteriores.

    firma_gran = tuple(
        (
            str(fila["Malla"]),
            float(fila["Masa tamiz [g]"]),
            float(fila["Masa tamiz + mineral [g]"])
        )
        for _, fila in df_valido.iterrows()
    )

    if st.session_state.get("gran_ia_firma") != firma_gran:

        st.session_state["gran_ia_firma"] = firma_gran

        st.session_state.pop(
            "gran_ia_respuesta",
            None
        )

        st.session_state.pop(
            "gran_ia_modelo",
            None
        )

    if st.button(
        "🤖 Explicar resultado con IA",
        key="gran_boton_explicar_ia",
        use_container_width=True
    ):

        from modulos.asistente import (
            obtener_api_key,
            generar_respuesta,
            interpretar_error
        )

        api_key = obtener_api_key()

        if not api_key:

            st.error(
                "No se encontró la clave API de Gemini."
            )

            st.info(
                "Configura GEMINI_API_KEY en "
                ".streamlit/secrets.toml para activar "
                "la explicación."
            )

        else:

            columnas_ia = [
                "Malla",
                "Abertura [µm]",
                "Masa mineral [g]",
                "Retenido parcial [%]",
                "Retenido acumulado [%]",
                "Pasante acumulado [%]"
            ]

            tabla_ia = df_valido[columnas_ia].copy()

            for columna in columnas_ia[1:]:

                tabla_ia[columna] = tabla_ia[columna].map(
                    lambda valor: f"{valor:.2f}"
                )

            detalle_t80 = (
                f"{t80:.2f} µm"
                if t80 is not None
                else (
                    "No disponible: el 80% pasante no puede "
                    "interpolarse con los puntos experimentales "
                    "disponibles."
                )
            )

            # El formato de cuatro secciones lo define el prompt central
            # INSTRUCCIONES_CALCULADORAS en modulos/asistente.py.
            pregunta_ia = (
                "CALCULADORA: Análisis Granulométrico.\n"
                "OBJETIVO: interpretar exclusivamente la distribución "
                "granulométrica calculada por la plataforma, sin modificar "
                "los valores ni realizar estimaciones nuevas.\n\n"
                "RESULTADOS PROPORCIONADOS:\n"
                f"Masa total de mineral: {masa_total:.2f} g\n"
                f"T80 estimado: {detalle_t80}\n\n"
                "TABLA GRANULOMÉTRICA (valores calculados):\n"
                f"{tabla_ia.to_string(index=False)}\n\n"
                "INSTRUCCIONES ESPECÍFICAS DE INTERPRETACIÓN:\n"
                "Utiliza exactamente estos cuatro encabezados Markdown: "
                "## 1. Resultados; ## 2. Explicación metalúrgica; "
                "## 3. Análisis técnico; ## 4. Recomendaciones. "
                "No agregues un quinto apartado de seguridad: esta "
                "calculadora no prepara soluciones químicas.\n"
                "1. RESULTADOS: destaca la masa total, el T80 si existe "
                "y las fracciones granulométricas con mayor retenido "
                "parcial, identificando sus mallas y aberturas reales. "
                "Usa solo cifras de la tabla, con dos decimales y unidades. "
                "No reproduzcas íntegramente la tabla ni inventes valores.\n"
                "2. EXPLICACIÓN METALÚRGICA: distingue masa retenida "
                "de retenido parcial, retenido acumulado y pasante "
                "acumulado. Explica la curva de pasante en función "
                "de la abertura y que el T80 representa la abertura "
                "asociada al 80 % pasante. Si existe T80, explica "
                "que la calculadora lo obtuvo mediante interpolación "
                "logarítmica en ambos ejes, usando porcentajes pasantes "
                "redondeados a dos decimales; no lo recalcules ni "
                "sustituyas ese método por interpolación lineal.\n"
                "3. ANÁLISIS TÉCNICO: identifica la distribución de "
                "material grueso y fino únicamente a partir de las "
                "mallas efectivamente medidas. Comenta dónde se "
                "concentra el retenido y qué implica para el control "
                "de tamaño en conminución, sin asignar una etapa "
                "de chancado o molienda no documentada. Distingue "
                "la estimación interpolada de una medición directa. "
                "Si no hay T80, explica que el 80 % pasante no "
                "queda delimitado por los datos válidos y no "
                "propongas un valor alternativo. No infieras "
                "recuperación metalúrgica, liberación mineral, "
                "eficiencia energética ni desempeño industrial.\n"
                "4. RECOMENDACIONES: propone verificaciones concretas "
                "según las fracciones y el rango de tamices presentes, "
                "como revisar representatividad de la muestra, "
                "limpieza y selección de mallas, pesaje, pérdidas "
                "de material y cobertura del entorno del 80 % "
                "pasante cuando sea pertinente. No atribuyas "
                "pérdidas ni errores experimentales que no fueron "
                "medidos.\n"
                "REGLAS: no confundas retenido con pasante; "
                "no trates la malla Fondo (abertura 0 µm) como "
                "punto de interpolación logarítmica; no inventes "
                "condiciones operacionales, objetivos de proceso "
                "ni valores de referencia. Explica con claridad "
                "y precisión, sin mencionar tesis ni marco teórico."
            )

            indicador_ia = st.empty()

            try:

                respuesta_ia, modelo_ia = generar_respuesta(
                    api_key=api_key,
                    mensajes=[],
                    pregunta=pregunta_ia,
                    indicador=indicador_ia
                )

                st.session_state[
                    "gran_ia_respuesta"
                ] = respuesta_ia

                st.session_state[
                    "gran_ia_modelo"
                ] = modelo_ia

            except Exception as error:

                st.error(
                    interpretar_error(error)
                )

                with st.expander(
                    "Ver detalles del error de IA"
                ):

                    st.code(
                        f"{type(error).__name__}: {error}"
                    )

            finally:

                indicador_ia.empty()

    if st.session_state.get("gran_ia_respuesta"):

        st.markdown(
            st.session_state["gran_ia_respuesta"]
        )

        st.caption(
            "Explicación generada con "
            f"{st.session_state.get('gran_ia_modelo', 'Gemini')}. "
            "Verifica la interpretación antes de aplicarla "
            "a decisiones operacionales."
        )


# ============================================================
# 3. CALCULADORA LEY DE BOND
# ============================================================

def mostrar_ley_bond():

    st.title("⚡ Calculadora de Energía (Ley de Bond)")

    st.write(
        "Calcula la energía específica y la potencia "
        "teórica requerida mediante la Tercera Ley "
        "de Conminución de Bond."
    )

    st.latex(
        r"W = 10 W_i \left("
        r"\frac{1}{\sqrt{P_{80}}}"
        r"-\frac{1}{\sqrt{F_{80}}}"
        r"\right)"
    )

    # --------------------------------------------------------
    # VALORES INICIALES
    # --------------------------------------------------------

    if "f80_input" not in st.session_state:
        st.session_state["f80_input"] = 2000.0

    if "p80_input" not in st.session_state:
        st.session_state["p80_input"] = 200.0

    t80 = st.session_state.get("t80_calculado")

    if t80 is not None and t80 > 0:

        st.info(
            f"Se detectó un T80 de {t80:.2f} µm "
            "en el análisis granulométrico."
        )

        col1, col2 = st.columns(2)

        col1.button(
            "Usar como F80 (Alimentación)",
            on_click=usar_t80,
            args=("f80_input",),
            use_container_width=True
        )

        col2.button(
            "Usar como P80 (Producto)",
            on_click=usar_t80,
            args=("p80_input",),
            use_container_width=True
        )

    st.markdown("---")

    # --------------------------------------------------------
    # PARÁMETROS DE OPERACIÓN
    # --------------------------------------------------------

    st.markdown("### 1. Parámetros de Operación")

    c1, c2 = st.columns(2)

    wi = c1.number_input(
        "Work Index del mineral (Wi) [kWh/t]",
        min_value=0.1,
        value=15.0,
        step=0.5,
        format="%.2f"
    )

    tph = c2.number_input(
        "Flujo másico a procesar [t/h]",
        min_value=0.1,
        value=100.0,
        step=10.0,
        format="%.2f"
    )

    st.markdown("### 2. Tamaños Característicos")

    c3, c4 = st.columns(2)

    f80 = c3.number_input(
        "Tamaño 80% Alimentación (F80) [µm]",
        min_value=0.1,
        step=50.0,
        format="%.2f",
        key="f80_input"
    )

    p80 = c4.number_input(
        "Tamaño 80% Producto (P80) [µm]",
        min_value=0.1,
        step=10.0,
        format="%.2f",
        key="p80_input"
    )

    # --------------------------------------------------------
    # VALIDACIÓN
    # --------------------------------------------------------

    st.markdown(
        "### 3. Resultados de Energía y Potencia"
    )

    if f80 <= p80:

        st.error(
            "El F80 debe ser mayor que el P80 "
            "para calcular la reducción de tamaño."
        )

        return

    # --------------------------------------------------------
    # CÁLCULOS
    # --------------------------------------------------------

    energia_especifica = 10 * wi * (
        (1 / np.sqrt(p80))
        - (1 / np.sqrt(f80))
    )

    potencia_kw = energia_especifica * tph

    potencia_hp = potencia_kw * 1.34102209

    # --------------------------------------------------------
    # RESULTADOS VISUALES
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            tarjeta_resultado(
                "Energía Específica",
                f"{energia_especifica:.2f}",
                "kWh/t",
                "#3b82f6"
            ),
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            tarjeta_resultado(
                "Potencia Teórica",
                f"{potencia_kw:.2f}",
                "kW",
                "#f59e0b"
            ),
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            tarjeta_resultado(
                "Potencia Teórica",
                f"{potencia_hp:.2f}",
                "HP",
                "#ef4444"
            ),
            unsafe_allow_html=True
        )

    st.caption(
        "El resultado corresponde a una estimación "
        "energética mediante la ecuación de Bond. "
        "No incluye factores de corrección del circuito, "
        "pérdidas mecánicas ni eficiencia del motor."
    )


# ============================================================
# 4. RAZÓN DE REDUCCIÓN
# ============================================================

def mostrar_razon_reduccion():

    st.title("📐 Razón de Reducción (Rr)")

    st.write(
        "Calcula la razón de reducción de tamaño "
        "comparando los tamaños característicos "
        "de alimentación y producto."
    )

    st.latex(
        r"R_r = \frac{F_{80}}{P_{80}}"
    )

    # --------------------------------------------------------
    # VALORES INICIALES
    # --------------------------------------------------------

    if "rr_f80_input" not in st.session_state:
        st.session_state["rr_f80_input"] = 0.0

    if "rr_p80_input" not in st.session_state:
        st.session_state["rr_p80_input"] = 0.0

    if "rr_unidad" not in st.session_state:
        st.session_state["rr_unidad"] = "µm"

    if "rr_unidad_anterior" not in st.session_state:
        st.session_state["rr_unidad_anterior"] = "µm"

    t80 = st.session_state.get("t80_calculado")

    if t80 is not None and t80 > 0:

        st.info(
            f"Se detectó un T80 de {t80:.2f} µm "
            "en el análisis granulométrico."
        )

        col1, col2 = st.columns(2)

        col1.button(
            "Usar como F80 (Alimentación RR)",
            on_click=usar_t80,
            args=("rr_f80_input",),
            use_container_width=True
        )

        col2.button(
            "Usar como P80 (Producto RR)",
            on_click=usar_t80,
            args=("rr_p80_input",),
            use_container_width=True
        )

    st.markdown("---")

    # --------------------------------------------------------
    # TAMAÑOS CARACTERÍSTICOS
    # --------------------------------------------------------

    st.markdown("### 1. Tamaños Característicos")

    unidad = st.selectbox(
        "Unidad de tamaño",
        ["µm", "mm"],
        key="rr_unidad",
        on_change=convertir_unidad_rr
    )

    c1, c2 = st.columns(2)

    f80 = c1.number_input(
        f"Tamaño de Alimentación (F80) [{unidad}]",
        min_value=0.0,
        step=100.0 if unidad == "µm" else 0.1,
        format="%.2f",
        key="rr_f80_input"
    )

    p80 = c2.number_input(
        f"Tamaño de Producto (P80) [{unidad}]",
        min_value=0.0,
        step=10.0 if unidad == "µm" else 0.1,
        format="%.2f",
        key="rr_p80_input"
    )

    # --------------------------------------------------------
    # VALIDACIÓN
    # --------------------------------------------------------

    st.markdown("### 2. Resultado y Diagnóstico")

    if f80 == 0 or p80 == 0:

        st.markdown(
            tarjeta_resultado(
                "Razón de Reducción (Rr)",
                "0.00",
                "Adimensional",
                "#a855f7"
            ),
            unsafe_allow_html=True
        )

        st.info(
            "Ingresa F80 y P80 mayores que cero "
            "para calcular la razón de reducción."
        )

        return

    if f80 <= p80:

        st.error(
            "El F80 debe ser mayor que el P80."
        )

        return

    # --------------------------------------------------------
    # CÁLCULO
    # --------------------------------------------------------

    razon_reduccion = f80 / p80

    # Clasificación orientativa, no normativa.

    if razon_reduccion < 3:

        etapa = "Reducción de tamaño baja"
        color = "#64748b"

    elif razon_reduccion <= 7:

        etapa = "Reducción de tamaño moderada"
        color = "#3b82f6"

    elif razon_reduccion <= 15:

        etapa = "Reducción de tamaño elevada"
        color = "#f59e0b"

    else:

        etapa = "Reducción de tamaño muy elevada"
        color = "#10b981"

    # --------------------------------------------------------
    # RESULTADOS VISUALES
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            tarjeta_resultado(
                "Razón de Reducción (Rr)",
                f"{razon_reduccion:.2f}",
                "Adimensional",
                "#a855f7"
            ),
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            tarjeta_resultado(
                "Evaluación de Reducción",
                etapa,
                "Clasificación orientativa",
                color
            ),
            unsafe_allow_html=True
        )

    st.caption(
        "La razón de reducción no representa por sí sola "
        "la eficiencia energética del equipo. "
        "La clasificación mostrada es orientativa y "
        "no determina de manera exclusiva el tipo "
        "de chancador o molino."
    )

    # --------------------------------------------------------
    # EXPLICACIÓN DEL CÁLCULO CON INTELIGENCIA ARTIFICIAL
    # --------------------------------------------------------

    st.markdown("---")

    st.markdown(
        "### 🤖 Explicación del resultado con IA"
    )

    st.write(
        "Solicita al asistente metalúrgico una explicación "
        "del cálculo realizado con tus valores de F80 y P80."
    )

    # --------------------------------------------------------
    # CONTROL DE RESULTADOS DE IA
    # --------------------------------------------------------

    firma_calculo = (
        float(f80),
        float(p80),
        unidad
    )

    if st.session_state.get("rr_ia_firma") != firma_calculo:

        st.session_state["rr_ia_firma"] = firma_calculo

        st.session_state.pop(
            "rr_ia_respuesta",
            None
        )

        st.session_state.pop(
            "rr_ia_modelo",
            None
        )

    # --------------------------------------------------------
    # BOTÓN PARA CONSULTAR GEMINI
    # --------------------------------------------------------

    if st.button(
        "🤖 Explicar resultado con IA",
        key="rr_boton_explicar_ia",
        use_container_width=True
    ):

        from modulos.asistente import (
            obtener_api_key,
            generar_respuesta,
            interpretar_error
        )

        api_key = obtener_api_key()

        if not api_key:

            st.error(
                "No se encontró la clave API de Gemini."
            )

            st.info(
                "Configura GEMINI_API_KEY en "
                ".streamlit/secrets.toml para activar "
                "la explicación."
            )

        else:

            # ------------------------------------------------
            # PREPARACIÓN DE LA CONSULTA
            # ------------------------------------------------

            # El formato de cuatro secciones lo define el prompt central
            # INSTRUCCIONES_CALCULADORAS en modulos/asistente.py.
            pregunta_ia = (
                "CALCULADORA: Razón de Reducción (Rr).\n"
                "OBJETIVO: interpretar exclusivamente el resultado "
                "de la plataforma, sin modificar los cálculos.\n\n"
                "DATOS DEL CÁLCULO:\n"
                f"F80 = {f80:.2f} {unidad}\n"
                f"P80 = {p80:.2f} {unidad}\n"
                "Fórmula utilizada: Rr = F80 / P80\n"
                f"Razón de reducción calculada: {razon_reduccion:.2f} "
                "(adimensional)\n"
                f"Clasificación orientativa: {etapa}\n\n"
                "INSTRUCCIONES ESPECÍFICAS DE INTERPRETACIÓN:\n"
                "Usa exactamente estos cuatro encabezados Markdown: "
                "## 1. Resultados; ## 2. Explicación metalúrgica; "
                "## 3. Análisis técnico; ## 4. Recomendaciones. "
                "No agregues un quinto apartado de seguridad: "
                "no se preparan soluciones químicas.\n"
                "1. RESULTADOS: informa F80, P80, Rr y la "
                "clasificación orientativa proporcionada. "
                "Conserva las unidades de tamaño seleccionadas "
                "y expresa Rr como valor adimensional, "
                "con dos decimales. No alteres las cifras.\n"
                "2. EXPLICACIÓN METALÚRGICA: define F80 como "
                "tamaño correspondiente al 80 % pasante de la "
                "alimentación y P80 como el del producto. Explica "
                "la relación Rr = F80/P80 y el significado "
                "físico de reducir el tamaño característico. "
                "No confundas la razón con un porcentaje de "
                "reducción, recuperación o eficiencia.\n"
                "3. ANÁLISIS TÉCNICO: interpreta la magnitud "
                "de la razón calculada y su clasificación "
                "exclusivamente como referencia orientativa, "
                "no como norma técnica. Señala que el indicador "
                "describe una relación de tamaños y por sí "
                "solo no permite determinar consumo energético, "
                "capacidad, liberación mineral, eficiencia "
                "del equipo ni tipo exacto de chancador. "
                "No compares con rangos de equipos como si "
                "fueran límites obligatorios.\n"
                "4. RECOMENDACIONES: plantea verificaciones "
                "específicas de F80 y P80 a partir de análisis "
                "granulométricos representativos y, si se "
                "requiere evaluar desempeño, solicita datos "
                "adicionales como distribución completa de "
                "tamaños, tipo de equipo, tonelaje y energía "
                "medida. Evita recomendar cambios de ajuste "
                "o equipos sin información operacional.\n"
                "REGLAS: conserva dos decimales, no recalcules "
                "ni cambies Rr, no inventes datos, metas "
                "industriales ni mediciones. No menciones "
                "tesis ni marco teórico."
            )

            # ------------------------------------------------
            # GENERACIÓN DE LA RESPUESTA
            # ------------------------------------------------

            indicador_ia = st.empty()

            try:

                respuesta_ia, modelo_ia = generar_respuesta(
                    api_key=api_key,
                    mensajes=[],
                    pregunta=pregunta_ia,
                    indicador=indicador_ia
                )

                st.session_state[
                    "rr_ia_respuesta"
                ] = respuesta_ia

                st.session_state[
                    "rr_ia_modelo"
                ] = modelo_ia

            except Exception as error:

                st.error(
                    interpretar_error(error)
                )

                with st.expander(
                    "Ver detalles del error de IA"
                ):

                    st.code(
                        f"{type(error).__name__}: {error}"
                    )

            finally:

                indicador_ia.empty()

    # --------------------------------------------------------
    # VISUALIZACIÓN DE LA EXPLICACIÓN GENERADA
    # --------------------------------------------------------

    if st.session_state.get("rr_ia_respuesta"):

        st.markdown(
            st.session_state["rr_ia_respuesta"]
        )

        st.caption(
            "Explicación generada con "
            f"{st.session_state.get('rr_ia_modelo', 'Gemini')}. "
            "Verifica la interpretación antes de aplicarla "
            "a decisiones operacionales."
        )
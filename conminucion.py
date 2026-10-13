
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
    "6": 3350.0,
    "10": 2000.0,
    "12": 1700.0,
    "14": 1400.0,
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
    Calcula T80 mediante interpolación semilogarítmica.
    Devuelve None si el 80% pasante no está comprendido
    dentro del intervalo experimental.
    """

    datos = df.loc[
        df["Abertura [µm]"] > 0,
        ["Abertura [µm]", "Pasante acumulado [%]"]
    ].copy()

    datos = datos.dropna()
    datos = datos.sort_values("Abertura [µm]")

    x = datos["Abertura [µm]"].to_numpy(dtype=float)
    y = datos["Pasante acumulado [%]"].to_numpy(dtype=float)

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
            log_t80 = np.log10(x1) + (
                (80 - y1) / (y2 - y1)
            ) * (np.log10(x2) - np.log10(x1))

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

    st.title("🔨 Etapas de Chancado")

    st.write(
        "Módulo dedicado a las operaciones de reducción "
        "de tamaño por fractura mecánica en la "
        "conminución de minerales oxidados."
    )

    st.markdown("---")

    etapas = [
        {
            "titulo": "1. Chancado Primario",
            "color": "#3b82f6",
            "equipo": (
                "Chancadores de mandíbulas o giratorios."
            ),
            "alimentacion": (
                "Roca corrida de mina (ROM), de gran tamaño."
            ),
            "producto": (
                "Reducción inicial del mineral, frecuentemente "
                "hacia tamaños del orden de 100 a 150 mm."
            )
        },
        {
            "titulo": "2. Chancado Secundario",
            "color": "#f59e0b",
            "equipo": (
                "Chancadores de cono u otros equipos secundarios."
            ),
            "alimentacion": (
                "Producto procedente del chancado primario."
            ),
            "producto": (
                "Reducción adicional, con tamaños que pueden "
                "encontrarse alrededor de 25 a 50 mm."
            )
        },
        {
            "titulo": "3. Chancado Terciario",
            "color": "#10b981",
            "equipo": (
                "Chancadores de cono de cabeza corta u otros "
                "equipos de trituración fina."
            ),
            "alimentacion": (
                "Producto del chancado secundario."
            ),
            "producto": (
                "Obtención de granulometrías más finas, "
                "según los requerimientos de aglomeración "
                "y lixiviación."
            )
        }
    ]

    columnas = st.columns(3)

    for columna, etapa in zip(columnas, etapas):

        with columna:
            color = etapa["color"]
            titulo = escape(etapa["titulo"])
            equipo = escape(etapa["equipo"])
            alimentacion = escape(etapa["alimentacion"])
            producto = escape(etapa["producto"])

            # HTML en una sola línea lógica:
            # evita que Markdown lo muestre como código.
            tarjeta = (
                f'<div style="'
                f'background:linear-gradient(145deg,#202938,#151c29);'
                f'border:1px solid #344155;'
                f'border-top:4px solid {color};'
                f'border-radius:14px;'
                f'padding:22px;'
                f'min-height:325px;'
                f'box-sizing:border-box;'
                f'color:#f8fafc;">'

                f'<div style="font-size:1.3rem;'
                f'font-weight:750;margin-bottom:20px;">'
                f'{titulo}</div>'

                f'<div style="font-size:.72rem;'
                f'color:#94a3b8;font-weight:700;'
                f'letter-spacing:.7px;margin-bottom:5px;">'
                f'EQUIPOS PRINCIPALES</div>'

                f'<div style="font-size:.92rem;'
                f'margin-bottom:17px;">{equipo}</div>'

                f'<div style="border-top:1px solid #354052;'
                f'margin-bottom:16px;"></div>'

                f'<div style="font-size:.72rem;'
                f'color:#94a3b8;font-weight:700;'
                f'letter-spacing:.7px;margin-bottom:5px;">'
                f'ALIMENTACIÓN</div>'

                f'<div style="font-size:.92rem;'
                f'margin-bottom:17px;">{alimentacion}</div>'

                f'<div style="font-size:.72rem;'
                f'color:#94a3b8;font-weight:700;'
                f'letter-spacing:.7px;margin-bottom:5px;">'
                f'PRODUCTO</div>'

                f'<div style="font-size:.92rem;">'
                f'{producto}</div>'
                f'</div>'
            )

            st.markdown(
                tarjeta,
                unsafe_allow_html=True
            )

    st.caption(
        "Los tamaños indicados son referenciales. "
        "Los valores reales dependen del equipo, "
        "la configuración del circuito y las "
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

    if "df_gran" not in st.session_state:

        st.session_state["df_gran"] = pd.DataFrame({
            "Malla": [
                "6", "10", "12", "14",
                "18", "30", "Fondo"
            ],
            "Peso tamiz [g]": [0.0] * 7,
            "Peso tamiz + mineral [g]": [0.0] * 7
        })

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
            "Peso tamiz [g]": st.column_config.NumberColumn(
                "Peso tamiz [g]",
                min_value=0.0,
                format="%.2f"
            ),
            "Peso tamiz + mineral [g]":
                st.column_config.NumberColumn(
                    "Peso tamiz + mineral [g]",
                    min_value=0.0,
                    format="%.2f"
                )
        },
        key="editor_granulometria"
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
        "Peso tamiz [g]",
        "Peso tamiz + mineral [g]"
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
        st.error("Las masas no pueden ser negativas.")
        return

    if (
        df_valido["Peso tamiz + mineral [g]"]
        < df_valido["Peso tamiz [g]"]
    ).any():

        st.error(
            "El peso del tamiz con mineral no puede "
            "ser menor que el peso del tamiz vacío."
        )
        return

    # --------------------------------------------------------
    # CÁLCULOS
    # --------------------------------------------------------

    df_valido["Abertura [µm]"] = (
        df_valido["Malla"].map(MALLAS_STD)
    )

    if df_valido["Abertura [µm]"].isna().any():
        st.error("Se encontraron mallas no reconocidas.")
        return

    df_valido = df_valido.sort_values(
        "Abertura [µm]",
        ascending=False
    ).reset_index(drop=True)

    df_valido["Peso mineral [g]"] = (
        df_valido["Peso tamiz + mineral [g]"]
        - df_valido["Peso tamiz [g]"]
    )

    peso_total = df_valido["Peso mineral [g]"].sum()

    if peso_total <= 0:
        st.warning(
            "Ingresa las masas de mineral para "
            "generar los resultados."
        )
        return

    df_valido["Retenido parcial [%]"] = (
        df_valido["Peso mineral [g]"]
        / peso_total * 100.0
    )

    df_valido["Retenido acumulado [%]"] = (
        df_valido["Retenido parcial [%]"].cumsum()
    )

    df_valido["Pasante acumulado [%]"] = (
        100.0 - df_valido["Retenido acumulado [%]"]
    ).clip(lower=0, upper=100)

    # --------------------------------------------------------
    # TABLA GRANULOMÉTRICA
    # --------------------------------------------------------

    st.markdown("---")
    st.markdown("### 2. Tabla Granulométrica Calculada")

    st.dataframe(
        df_valido.style.format({
            "Abertura [µm]": "{:.2f}",
            "Peso tamiz [g]": "{:.2f}",
            "Peso tamiz + mineral [g]": "{:.2f}",
            "Peso mineral [g]": "{:.2f}",
            "Retenido parcial [%]": "{:.2f}",
            "Retenido acumulado [%]": "{:.2f}",
            "Pasante acumulado [%]": "{:.2f}"
        }),
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # T80
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
        f"{peso_total:.2f} g"
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

        col2.metric("T80 estimado", "No disponible")

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
    # EXPORTACIÓN
    # --------------------------------------------------------

    st.markdown("---")
    st.markdown("### 4. Exportar Datos")

    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:

        if st.button(
            "💾 Actualizar datos para Power BI",
            use_container_width=True
        ):

            df_valido.to_csv(
                "datos_granulometria.csv",
                index=False,
                sep=";",
                decimal=",",
                encoding="utf-8-sig"
            )

            st.success(
                "Datos guardados en "
                "'datos_granulometria.csv'."
            )

    with col_btn2:

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
                "B:H", 20, formato_decimal
            )
            worksheet.set_column("A:A", 12)

            if len(df_curva) >= 2:

                chart = workbook.add_chart({
                    "type": "scatter",
                    "subtype": "straight_with_markers"
                })

                # La tabla está ordenada de mayor
                # a menor abertura. El fondo queda
                # al final y se excluye del gráfico.
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
        st.session_state["rr_f80_input"] = 150000.0

    if "rr_p80_input" not in st.session_state:
        st.session_state["rr_p80_input"] = 15000.0

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
        min_value=0.01,
        step=100.0 if unidad == "µm" else 0.1,
        format="%.2f",
        key="rr_f80_input"
    )

    p80 = c2.number_input(
        f"Tamaño de Producto (P80) [{unidad}]",
        min_value=0.01,
        step=10.0 if unidad == "µm" else 0.1,
        format="%.2f",
        key="rr_p80_input"
    )

    # --------------------------------------------------------
    # VALIDACIÓN
    # --------------------------------------------------------

    st.markdown("### 2. Resultado y Diagnóstico")

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

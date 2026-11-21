
import io
import html

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def numero(valor):
    """Presenta un valor con dos decimales."""
    return f"{valor:,.2f}"


def crear_excel(tabla, nombre_hoja="Balance de Masas"):
    """
    Crea un archivo Excel con datos numéricos reales
    y formato de dos decimales.
    """

    libro = Workbook()
    hoja = libro.active
    hoja.title = nombre_hoja[:31]

    encabezados = list(tabla.columns)

    hoja.append(encabezados)

    for fila in tabla.itertuples(index=False, name=None):
        hoja.append(list(fila))

    # Encabezado
    for celda in hoja[1]:
        celda.font = Font(
            bold=True,
            color="FFFFFF"
        )
        celda.fill = PatternFill(
            fill_type="solid",
            fgColor="17365D"
        )
        celda.alignment = Alignment(
            horizontal="center",
            vertical="center"
        )

    hoja.row_dimensions[1].height = 25

    # Datos
    for fila in hoja.iter_rows(
        min_row=2,
        max_row=hoja.max_row
    ):
        for celda in fila:

            if isinstance(
                celda.value,
                (int, float)
            ):
                celda.number_format = '#,##0.00'

            celda.alignment = Alignment(
                vertical="center"
            )

    # Ancho automático aproximado
    for indice, columna in enumerate(
        hoja.columns,
        start=1
    ):
        longitud = max(
            len(str(celda.value or ""))
            for celda in columna
        )

        hoja.column_dimensions[
            get_column_letter(indice)
        ].width = min(
            max(longitud + 4, 18),
            48
        )

    hoja.freeze_panes = "A2"
    hoja.auto_filter.ref = hoja.dimensions

    salida = io.BytesIO()

    libro.save(salida)
    salida.seek(0)

    return salida.getvalue()


def mostrar_tabla(tabla, clave, archivo):
    """
    Muestra una tabla con dos decimales
    y agrega su descarga en Excel.
    """

    columnas_numericas = [
        columna
        for columna in tabla.columns
        if pd.api.types.is_numeric_dtype(
            tabla[columna]
        )
    ]

    configuracion = {
        columna: st.column_config.NumberColumn(
            columna,
            format="%.2f"
        )
        for columna in columnas_numericas
    }

    st.dataframe(
        tabla,
        hide_index=True,
        use_container_width=True,
        column_config=configuracion
    )

    st.download_button(
        label="📥 Descargar tabla en Excel",
        data=crear_excel(tabla),
        file_name=archivo,
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        key=clave
    )


def tarjeta_fase(titulo, descripcion, color):

    titulo = html.escape(titulo)
    descripcion = html.escape(descripcion)

    contenido = f"""
    <div style="
        background:#1e2532;
        border:1px solid #334155;
        border-left:4px solid {color};
        border-radius:14px;
        padding:22px;
        min-height:180px;
        box-sizing:border-box;
    ">
        <h3 style="
            color:white;
            margin:0 0 14px 0;
        ">{titulo}</h3>

        <p style="
            color:#cbd5e1;
            line-height:1.6;
            margin:0;
        ">{descripcion}</p>
    </div>
    """

    st.markdown(
        contenido.replace("\n", ""),
        unsafe_allow_html=True
    )


# ============================================================
# DIAGRAMA DEL PROCESO DE AGLOMERACIÓN
# ============================================================

def mostrar_diagrama_aglomeracion(
    mineral_seco_tph,
    agua_mineral_tph,
    mineral_humedo_tph,
    agua_adicional_tph,
    acido_comercial_tph,
    mineral_aglomerado_tph,
    humedad_salida_pct,
    unidad_diagrama="t/h"
):

    factor_diagrama = {"g/h": 1_000_000.0, "kg/h": 1000.0, "t/h": 1.0}[unidad_diagrama]

    valores = {
        "SECO": numero(mineral_seco_tph * factor_diagrama),
        "AGUA_MINERAL": numero(agua_mineral_tph * factor_diagrama),
        "HUMEDO": numero(mineral_humedo_tph * factor_diagrama),
        "AGUA_ADICIONAL": numero(agua_adicional_tph * factor_diagrama),
        "ACIDO": numero(acido_comercial_tph * factor_diagrama),
        "PRODUCTO": numero(mineral_aglomerado_tph * factor_diagrama),
        "HUMEDAD": numero(humedad_salida_pct)
    }

    svg = """
    <svg xmlns="http://www.w3.org/2000/svg"
         viewBox="0 0 1200 560"
         width="100%">

      <defs>
        <marker id="flecha"
                viewBox="0 0 10 10"
                refX="9"
                refY="5"
                markerWidth="7"
                markerHeight="7"
                orient="auto">
          <path d="M0 0 L10 5 L0 10 Z"
                fill="#94a3b8"/>
        </marker>

        <marker id="flechaVerde"
                viewBox="0 0 10 10"
                refX="9"
                refY="5"
                markerWidth="7"
                markerHeight="7"
                orient="auto">
          <path d="M0 0 L10 5 L0 10 Z"
                fill="#22c55e"/>
        </marker>

        <linearGradient id="tambor"
                        x1="0" y1="0"
                        x2="1" y2="1">
          <stop offset="0%"
                stop-color="#3b82f6"/>
          <stop offset="100%"
                stop-color="#1d4ed8"/>
        </linearGradient>
      </defs>

      <style>
        .caja {
          fill:#1e2532;
          stroke:#64748b;
          stroke-width:2;
        }

        .titulo {
          fill:#e2e8f0;
          font-family:Arial,sans-serif;
          font-size:18px;
          font-weight:bold;
          text-anchor:middle;
        }

        .valor {
          fill:white;
          font-family:Arial,sans-serif;
          font-size:23px;
          font-weight:bold;
          text-anchor:middle;
        }

        .linea {
          fill:none;
          stroke:#94a3b8;
          stroke-width:3;
          stroke-linecap:round;
          stroke-linejoin:round;
        }

        .flujo {
          fill:none;
          stroke:#94a3b8;
          stroke-width:3;
          stroke-linecap:round;
          stroke-linejoin:round;
          marker-end:url(#flecha);
        }
      </style>

      <!-- ENTRADAS SUPERIORES -->

      <rect x="400" y="25"
            width="230" height="90"
            rx="12"
            fill="#1e2532"
            stroke="#38bdf8"
            stroke-width="2"/>

      <text x="515" y="60" class="titulo">
        Agua adicional
      </text>

      <text x="515" y="94" class="valor">
        {{AGUA_ADICIONAL}} {{UNIDAD}}
      </text>

      <rect x="715" y="25"
            width="230" height="90"
            rx="12"
            fill="#1e2532"
            stroke="#f59e0b"
            stroke-width="2"/>

      <text x="830" y="60" class="titulo">
        Ácido comercial
      </text>

      <text x="830" y="94" class="valor">
        {{ACIDO}} {{UNIDAD}}
      </text>

      <!-- FLECHAS HACIA AGLOMERADOR -->

      <path d="M515 115 V195 H545 V250"
            class="flujo"/>

      <path d="M830 115 V180 H670 V250"
            class="flujo"/>

      <!-- MINERAL HÚMEDO -->

      <rect x="35" y="265"
            width="255" height="95"
            rx="12"
            class="caja"/>

      <text x="162.5" y="301" class="titulo">
        Mineral húmedo
      </text>

      <text x="162.5" y="337" class="valor">
        {{HUMEDO}} {{UNIDAD}}
      </text>

      <path d="M290 312 H405"
            class="flujo"/>

      <!-- AGLOMERADOR -->

      <rect x="415" y="255"
            width="310" height="115"
            rx="28"
            fill="url(#tambor)"
            stroke="#93c5fd"
            stroke-width="3"/>

      <ellipse cx="725" cy="312.5"
               rx="25" ry="57.5"
               fill="#1d4ed8"
               stroke="#93c5fd"
               stroke-width="2"/>

      <text x="560" y="323"
            text-anchor="middle"
            fill="white"
            font-family="Arial,sans-serif"
            font-size="27"
            font-weight="bold">
        Aglomerador
      </text>

      <!-- SALIDA -->

      <path d="M750 312 H865"
            fill="none"
            stroke="#22c55e"
            stroke-width="3"
            marker-end="url(#flechaVerde)"/>

      <rect x="875" y="265"
            width="290" height="95"
            rx="12"
            fill="#1e2532"
            stroke="#22c55e"
            stroke-width="2"/>

      <text x="1020" y="301" class="titulo">
        Mineral aglomerado
      </text>

      <text x="1020" y="337" class="valor">
        {{PRODUCTO}} {{UNIDAD}}
      </text>

      <text x="1020" y="405"
            fill="#cbd5e1"
            text-anchor="middle"
            font-family="Arial,sans-serif"
            font-size="17">
        Humedad de salida
      </text>

      <text x="1020" y="445"
            fill="#22c55e"
            text-anchor="middle"
            font-family="Arial,sans-serif"
            font-size="32"
            font-weight="bold">
        {{HUMEDAD}}%
      </text>

      <!-- MINERAL SECO -->

      <rect x="25" y="470"
            width="185" height="75"
            rx="12"
            class="caja"/>

      <text x="117.5" y="499" class="titulo">
        Mineral seco
      </text>

      <text x="117.5" y="528" class="valor">
        {{SECO}} {{UNIDAD}}
      </text>

      <!-- SIGNO MÁS -->

      <text x="245" y="520"
            fill="white"
            text-anchor="middle"
            font-family="Arial,sans-serif"
            font-size="42"
            font-weight="bold">
        +
      </text>

      <!-- AGUA DEL MINERAL -->

      <rect x="280" y="470"
            width="195" height="75"
            rx="12"
            fill="#1e2532"
            stroke="#38bdf8"
            stroke-width="2"/>

      <text x="377.5" y="499" class="titulo">
        Agua del mineral
      </text>

      <text x="377.5" y="528" class="valor">
        {{AGUA_MINERAL}} {{UNIDAD}}
      </text>

      <!-- UNIÓN DE AMBOS COMPONENTES -->

      <path d="M117.5 470 V425 H162.5"
            class="linea"/>

      <path d="M377.5 470 V425 H162.5"
            class="linea"/>

      <path d="M162.5 425 V365"
            class="flujo"/>

    </svg>
    """

    valores["UNIDAD"] = unidad_diagrama

    for clave, valor in valores.items():
        svg = svg.replace(
            "{{" + clave + "}}",
            html.escape(valor)
        )

    pagina = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8">
      <style>
        html, body {{
          margin:0;
          padding:0;
          background:transparent;
          overflow:hidden;
        }}

        svg {{
          display:block;
          width:100%;
          height:auto;
        }}
      </style>
    </head>
    <body>
      {svg}
    </body>
    </html>
    """

    components.html(
        pagina,
        height=570,
        scrolling=False
    )


# ============================================================
# 1. FUNDAMENTOS DE AGLOMERACIÓN Y LIXIVIACIÓN
# Basado en los apartados 2.2.3.1 y 2.2.3.2 de la tesis.
# ============================================================

def mostrar_procesos_hidro():
    """Fundamentos teóricos; conserva el nombre para la navegación existente."""

    st.title("💧 Fundamentos de Aglomeración y Lixiviación")
    st.write(
        "Principios, equipos, métodos y variables operacionales del "
        "acondicionamiento y la lixiviación de minerales oxidados de cobre."
    )
    st.markdown("---")

    st.header("1. Aglomeración")
    st.write(
        "La aglomeración es una operación previa a la lixiviación en la que "
        "se unen partículas finas y gruesas mediante la incorporación "
        "controlada de humedad y, cuando corresponde, reactivos químicos. "
        "Se forman aglomerados o glómeros constituidos por partículas "
        "de distintos tamaños adheridas entre sí."
    )
    st.write(
        "Su finalidad es modificar la distribución física de las partículas "
        "y favorecer la formación de espacios interparticulares por los "
        "que circula la solución lixiviante. La acumulación de finos "
        "y una distribución granulométrica inadecuada pueden disminuir "
        "la permeabilidad de las pilas."
    )

    st.subheader("Variables operacionales de la aglomeración")
    variables_aglomeracion = [
        (
            "Humedad del mineral",
            "Una humedad insuficiente puede producir aglomerados débiles; "
            "el exceso de agua puede generar estructuras plásticas e inestables "
            "y perjudicar el drenaje del lecho."
        ),
        (
            "Dosificación de ácido sulfúrico",
            "La incorporación de ácido, cuando corresponde, permite "
            "iniciar reacciones con las especies minerales presentes."
        ),
        (
            "Distribución granulométrica",
            "Las partículas finas se adhieren a otras de mayor tamaño "
            "y forman estructuras más estables para su manipulación."
        ),
        (
            "Tiempo de residencia y mineralogía",
            "El acondicionamiento depende del tiempo de contacto, "
            "las características del mineral y las condiciones de operación."
        ),
    ]
    for i in range(0, len(variables_aglomeracion), 2):
        columnas = st.columns(2)
        for columna, (titulo, descripcion) in zip(
            columnas, variables_aglomeracion[i:i + 2]
        ):
            with columna:
                tarjeta_fase(titulo, descripcion, "#a855f7")
        st.write("")

    st.subheader("Equipo utilizado: tambor aglomerador")
    st.write(
        "El tambor aglomerador es un cilindro rotatorio que mezcla el "
        "mineral con agua y, cuando corresponde, ácido sulfúrico. "
        "La rotación, el revestimiento interior y los elementos "
        "levantadores favorecen el movimiento y la mezcla del mineral, "
        "facilitando la formación de aglomerados antes de la lixiviación."
    )

    st.subheader("Curado ácido")
    st.write(
        "El curado ácido es un acondicionamiento químico que puede "
        "realizarse durante la aglomeración o posteriormente. Consiste "
        "en incorporar ácido sulfúrico y mantener un período de contacto "
        "con el mineral para favorecer las reacciones de disolución y "
        "sulfatación de determinadas especies de cobre antes del riego "
        "de lixiviación. Su efecto depende de la mineralogía, la humedad, "
        "la disponibilidad de ácido y las condiciones de contacto."
    )

    st.markdown("---")
    st.header("2. Lixiviación")
    st.write(
        "La lixiviación es una operación hidrometalúrgica de extracción "
        "sólido-líquido que consiste en disolver selectivamente componentes "
        "metálicos de un mineral mediante el contacto con una solución "
        "química denominada agente lixiviante. En el tratamiento de "
        "minerales oxidados de cobre se utiliza habitualmente ácido "
        "sulfúrico (H₂SO₄)."
    )
    st.write(
        "Su objetivo es transferir el cobre desde la matriz mineral "
        "hacia una solución acuosa, conocida como solución rica de "
        "lixiviación o PLS (Pregnant Leach Solution), que puede "
        "alimentar operaciones posteriores de recuperación."
    )

    st.subheader("Métodos de lixiviación")
    metodos = [
        (
            "Lixiviación en pilas",
            "El mineral se deposita sobre una base acondicionada e "
            "impermeabilizada. La solución lixiviante se distribuye "
            "mediante sistemas de riego y atraviesa el lecho mineral. "
            "Las soluciones se recolectan en la base. Existen pilas "
            "estáticas (multi-lift) y dinámicas (on/off).",
            "#22c55e"
        ),
        (
            "Lixiviación en botaderos",
            "Se aplica principalmente a grandes volúmenes de mineral "
            "de baja ley o material minero de menor calidad. Permite "
            "tratar cantidades elevadas de material mediante "
            "soluciones lixiviantes.",
            "#3b82f6"
        ),
        (
            "Lixiviación por agitación",
            "El mineral permanece en suspensión dentro de un tanque "
            "mediante sistemas de mezclado mecánico o neumático. "
            "Favorece el contacto sólido-líquido y el control de "
            "temperatura, concentración de reactivos, tiempo de "
            "residencia y densidad de pulpa.",
            "#f59e0b"
        ),
        (
            "Lixiviación en columnas",
            "Se utiliza en ensayos de laboratorio para estudiar la "
            "circulación de soluciones a través de lechos minerales "
            "y analizar el comportamiento del material bajo "
            "condiciones controladas.",
            "#06b6d4"
        ),
    ]
    for i in range(0, len(metodos), 2):
        columnas = st.columns(2)
        for columna, metodo in zip(columnas, metodos[i:i + 2]):
            with columna:
                tarjeta_fase(*metodo)
        st.write("")

    with st.expander("Tipos de pilas de lixiviación", expanded=False):
        st.markdown(
            "**Pilas estáticas (multi-lift):** después de lixiviar "
            "un nivel, se apilan nuevos niveles sobre el material "
            "tratado.\n\n"
            "**Pilas dinámicas (on/off):** el mineral se apila "
            "en un nivel; después de lixiviarlo, el material agotado "
            "se retira y se reemplaza por mineral nuevo."
        )

    with st.expander("Sistemas de agitación", expanded=False):
        st.markdown(
            "**Agitación mecánica:** utiliza un impulsor o hélice "
            "para mantener el mineral en suspensión y promover "
            "la mezcla con la solución.\n\n"
            "**Agitación neumática:** utiliza aire comprimido "
            "para generar movimiento y circulación de la pulpa."
        )

    st.subheader("Solución lixiviante")
    st.write(
        "La preparación de la solución lixiviante permite establecer "
        "las condiciones químicas de la operación. Para minerales "
        "oxidados de cobre se emplean principalmente soluciones "
        "acuosas de ácido sulfúrico, cuya concentración se selecciona "
        "según la mineralogía, el consumo de ácido y las condiciones "
        "del proceso. Se consideran la concentración de H₂SO₄, "
        "el pH, la densidad, el volumen y la composición del agua."
    )

    st.subheader("Variables operacionales de la lixiviación")
    variables_lixiviacion = [
        (
            "Mineralogía",
            "Determina las especies de cobre presentes y su "
            "comportamiento frente al agente lixiviante."
        ),
        (
            "Granulometría",
            "Influye en la superficie disponible para la reacción "
            "y en la circulación de la solución; un exceso de "
            "finos puede reducir la permeabilidad."
        ),
        (
            "Concentración de ácido y pH",
            "Condicionan la disponibilidad del reactivo y la "
            "acidez de la solución. Una dosificación excesiva "
            "puede aumentar el consumo sin mejorar "
            "proporcionalmente la recuperación."
        ),
        (
            "Riego, permeabilidad, temperatura y tiempo",
            "La tasa de riego, el transporte de solución por el "
            "lecho, la temperatura y el tiempo de contacto "
            "afectan el desarrollo de la lixiviación."
        ),
    ]
    for i in range(0, len(variables_lixiviacion), 2):
        columnas = st.columns(2)
        for columna, (titulo, descripcion) in zip(
            columnas, variables_lixiviacion[i:i + 2]
        ):
            with columna:
                tarjeta_fase(titulo, descripcion, "#22c55e")
        st.write("")

    st.caption(
        "Contenido adaptado de los apartados 2.2.3.1 "
        "(Aglomeración) y 2.2.3.2 (Lixiviación) del marco "
        "teórico de la tesis."
    )


# ============================================================
# 2. CALCULADORA DE AGLOMERACIÓN
# ============================================================

def mostrar_aglomeracion():
    """Dosificación de reactivos para ensayos de aglomeración a escala de laboratorio."""

    st.title("🧪 Calculadora de Aglomeración y Curado de Laboratorio")
    st.write(
        "Calcula el ácido sulfúrico comercial y el agua adicional necesarios "
        "para acondicionar una muestra de mineral antes de su lixiviación. "
        "Se utiliza una dosificación de H₂SO₄ puro por tonelada de mineral seco "
        "y un porcentaje objetivo de acondicionamiento según el método de dosificación."
    )
    st.markdown("---")
    st.markdown("### 📥 Parámetros del ensayo")

    c1, c2, c3 = st.columns(3)
    with c1:
        base_mineral = st.radio(
            "Base de masa ingresada", ["Mineral seco", "Mineral húmedo"],
            key="agl_lab_base"
        )
        unidad_mineral = st.selectbox(
            "Unidad de masa del mineral", ["g", "kg"],
            key="agl_lab_unidad"
        )
        masa_ingresada = st.number_input(
            f"Masa de mineral [{unidad_mineral}]", min_value=0.0,
            value=0.0, step=10.0, format="%.2f", key="agl_lab_masa"
        )
    with c2:
        humedad_inicial = st.number_input(
            "Humedad inicial de mineral [%]",
            min_value=0.0, max_value=99.99, value=0.0,
            step=0.10, format="%.2f", key="agl_lab_humedad_inicial"
        )
        humedad_objetivo = st.number_input(
            "Porcentaje de humedad objetivo [%]",
            min_value=0.0, max_value=99.99, value=0.0,
            step=0.10, format="%.2f", key="agl_lab_humedad_objetivo"
        )
    with c3:
        dosificacion = st.number_input(
            "Dosificación [kg H₂SO₄ puro/t mineral seco]",
            min_value=0.0, value=0.0, step=1.0,
            format="%.2f", key="agl_lab_dosificacion"
        )
        concentracion = st.number_input(
            "Pureza del ácido [%]",
            min_value=0.0, max_value=100.0, value=0.0,
            step=0.50, format="%.2f", key="agl_lab_concentracion"
        )
        densidad = st.number_input(
            "Densidad del ácido comercial [g/mL]",
            min_value=0.0, value=0.0, step=0.01,
            format="%.2f", key="agl_lab_densidad"
        )

    st.caption(
        "Método de dosificación: el ácido comercial completo se incluye en el numerador "
        "de la ecuación de dosificación. Este porcentaje no representa la fracción "
        "másica real de agua. La dosificación de ácido se aplica al mineral seco."
    )

    datos_validos = masa_ingresada > 0 and concentracion > 0 and densidad > 0

    masa_base_g = (masa_ingresada if datos_validos else 0.0) * (1000.0 if unidad_mineral == "kg" else 1.0)
    fraccion_inicial = humedad_inicial / 100.0
    fraccion_objetivo = humedad_objetivo / 100.0
    fraccion_acido = concentracion / 100.0

    if base_mineral == "Mineral húmedo":
        mineral_humedo_g = masa_base_g
        mineral_seco_g = mineral_humedo_g * (1.0 - fraccion_inicial)
    else:
        mineral_seco_g = masa_base_g
        mineral_humedo_g = mineral_seco_g / (1.0 - fraccion_inicial)

    agua_inicial_g = mineral_humedo_g - mineral_seco_g
    # kg H₂SO₄/t mineral seco equivale a g H₂SO₄/kg mineral seco.
    acido_puro_g = mineral_seco_g * dosificacion / 1000.0
    acido_comercial_g = acido_puro_g / fraccion_acido if datos_validos else 0.0
    agua_acido_g = acido_comercial_g - acido_puro_g
    volumen_acido_ml = acido_comercial_g / densidad if datos_validos else 0.0

    # Método de dosificación empleado:
    # H = (agua inicial del mineral + ácido comercial + agua añadida) /
    #     (mineral seco + agua inicial + ácido comercial + agua añadida).
    # Este indicador NO representa la humedad másica real de agua.
    masa_previa_g = mineral_humedo_g + acido_comercial_g
    masa_numerador_previa_g = agua_inicial_g + acido_comercial_g
    agua_requerida_g = (
        fraccion_objetivo * masa_previa_g - masa_numerador_previa_g
    ) / (1.0 - fraccion_objetivo)
    agua_adicional_g = max(0.0, agua_requerida_g) if datos_validos else 0.0
    volumen_agua_ml = agua_adicional_g  # densidad de agua = 1,00 g/mL
    masa_final_g = masa_previa_g + agua_adicional_g
    indicador_final = (
        (masa_numerador_previa_g + agua_adicional_g) / masa_final_g * 100.0
        if masa_final_g and datos_validos else 0.0
    )

    st.markdown("---")
    st.markdown("### 📊 Resultados")
    r1, r2, r3 = st.columns(3)
    r1.metric("Ácido comercial", f"{numero(volumen_acido_ml)} mL")
    r2.metric("Agua adicional", f"{numero(volumen_agua_ml)} mL")
    r3.metric("Porcentaje de humedad calculada", f"{numero(indicador_final)} %")

    if datos_validos and agua_requerida_g < -1e-9:
        st.warning(
            "La mezcla ya supera la humedad objetivo antes de agregar agua. "
            "La calculadora establece el agua adicional en 0,00 mL; "
            "no puede alcanzar esa humedad agregando más agua."
        )
    elif datos_validos and abs(agua_requerida_g) < 1e-9:
        st.info("No es necesario agregar agua adicional para alcanzar la humedad objetivo.")

    st.markdown("### 📋 Tabla de resultados")
    tabla = pd.DataFrame({
        "Parámetro": [
            "Mineral seco", "Mineral húmedo inicial", "Agua inicial del mineral",
            "Dosificación de ácido", "Ácido comercial",
            "Volumen de ácido comercial", "Agua adicional",
            "Volumen de agua adicional", "Masa final estimada",
            "Porcentaje de humedad calculada"
        ],
        "Valor": [
            mineral_seco_g, mineral_humedo_g, agua_inicial_g,
            dosificacion, acido_comercial_g, volumen_acido_ml,
            agua_adicional_g, volumen_agua_ml, masa_final_g, indicador_final
        ],
        "Unidad": [
            "g", "g", "g", "kg/t", "g", "mL",
            "g", "mL", "g", "%"
        ]
    })

    mostrar_tabla(
        tabla, "agl_lab_descarga", "aglomeracion_curado_laboratorio.xlsx"
    )

    st.caption(
        "El porcentaje calculado sigue la ecuación de dosificación empleada: "
        "considera el ácido comercial completo en el numerador. "
        "No corresponde a una medición de humedad real. Se supone densidad "
        "del agua de 1,00 g/mL y ausencia de pérdidas."
    )
    st.warning(
        "Seguridad: el H₂SO₄ concentrado es corrosivo. Utiliza los elementos "
        "de protección y el procedimiento del laboratorio. Al diluir, "
        "agrega el ácido al agua, nunca al revés."
    )

    # ========================================================
    # EXPLICACIÓN CON IA: mismo asistente que Preparación LX
    # ========================================================
    st.markdown("---")
    st.markdown("### 🤖 Explicación del resultado con IA")
    st.write(
        "Solicita al asistente metalúrgico una interpretación de las "
        "cantidades calculadas para el ensayo de aglomeración y curado."
    )

    datos_actuales = (
        base_mineral, unidad_mineral, masa_ingresada, humedad_inicial,
        humedad_objetivo, dosificacion, concentracion, densidad
    )
    if st.session_state.get("agl_lab_ia_datos") != datos_actuales:
        st.session_state["agl_lab_ia_datos"] = datos_actuales
        st.session_state.pop("agl_lab_ia_respuesta", None)
        st.session_state.pop("agl_lab_ia_modelo", None)

    if st.button(
        "🤖 Explicar resultado con IA",
        key="agl_lab_boton_ia",
        use_container_width=True,
        disabled=not datos_validos,
    ):
        prompt = (
            "MÓDULO: Aglomeración y curado de mineral de cobre a escala de laboratorio.\n"
            "Interpreta exclusivamente los datos calculados a continuación. "
            "Utiliza exactamente estas secciones y en este orden: "
            "1. Resultados; 2. Explicación metalúrgica; "
            "3. Análisis técnico; 4. Recomendaciones; "
            "5. Advertencias de seguridad.\n\n"
            "DATOS Y RESULTADOS:\n"
            f"Base de mineral: {base_mineral}\n"
            f"Masa ingresada: {masa_ingresada:.2f} {unidad_mineral}\n"
            f"Mineral seco: {mineral_seco_g:.2f} g\n"
            f"Mineral húmedo inicial: {mineral_humedo_g:.2f} g\n"
            f"Agua inicial del mineral: {agua_inicial_g:.2f} g\n"
            f"Humedad inicial: {humedad_inicial:.2f} % base húmeda\n"
            f"Porcentaje de humedad objetivo: {humedad_objetivo:.2f} %\n"
            f"Dosificación: {dosificacion:.2f} kg H₂SO₄ puro/t mineral seco\n"
            f"Pureza del ácido: {concentracion:.2f} % m/m\n"
            f"Densidad del ácido comercial: {densidad:.2f} g/mL\n"
            f"Ácido puro requerido: {acido_puro_g:.2f} g\n"
            f"Ácido comercial requerido: {acido_comercial_g:.2f} g\n"
            f"Volumen de ácido comercial: {volumen_acido_ml:.2f} mL\n"
            f"Agua adicional: {agua_adicional_g:.2f} g "
            f"({volumen_agua_ml:.2f} mL)\n"
            f"Masa final estimada: {masa_final_g:.2f} g\n"
            f"Porcentaje de humedad calculada: {indicador_final:.2f} %\n"
            f"Agua adicional teórica antes de limitar a cero: {agua_requerida_g:.2f} g\n\n"
            "INDICACIONES ESPECÍFICAS:\n"
            "En Resultados destaca los volúmenes de ácido y agua y el porcentaje "
            "de acondicionamiento. En Explicación metalúrgica explica la función "
            "de la aglomeración, el curado y la dosificación de ácido. "
            "En Análisis técnico explica que el porcentaje de acondicionamiento "
            "utilizado es un indicador del método de dosificación: incluye la "
            "masa completa del ácido comercial en el numerador, y NO equivale "
            "a la humedad física real ni a una medición experimental. "
            "Si el agua adicional es cero por haberse superado el objetivo, "
            "señala que añadir agua no permite corregirlo. "
            "No supongas recuperación de cobre, calidad de aglomerados ni "
            "condiciones de curado no medidas. "
            "En Recomendaciones sugiere comprobar las condiciones del ensayo "
            "y verificar experimentalmente la humedad y la dosificación. "
            "En Advertencias de seguridad indica que el H₂SO₄ es corrosivo, "
            "que su dilución es exotérmica, que deben usarse EPP, procedimientos "
            "y ficha de seguridad del laboratorio; si se diluye, añadir "
            "lentamente ácido al agua, nunca agua al ácido. "
            "No presentes este balance como un protocolo operativo completo. "
            "No inventes valores, no confundas masa con flujo másico y "
            "muestra los resultados con dos decimales y sus unidades."
        )
        try:
            from modulos.asistente import (
                obtener_api_key,
                generar_respuesta,
                interpretar_error,
            )
            api_key = obtener_api_key()
            if not api_key:
                raise ValueError("No se encontró la clave API de Gemini.")

            indicador_ia = st.empty()
            try:
                respuesta, modelo = generar_respuesta(
                    api_key=api_key,
                    mensajes=[],
                    pregunta=prompt,
                    indicador=indicador_ia,
                )
            finally:
                indicador_ia.empty()
            if not respuesta:
                raise ValueError("El asistente no devolvió una respuesta.")
            st.session_state["agl_lab_ia_respuesta"] = respuesta
            st.session_state["agl_lab_ia_modelo"] = modelo
        except Exception as error:
            try:
                mensaje = interpretar_error(error)
            except Exception:
                mensaje = str(error)
            st.error(f"No se pudo generar la explicación con IA: {mensaje}")
            with st.expander("Ver detalles técnicos del error"):
                st.code(f"{type(error).__name__}: {error}")

    if st.session_state.get("agl_lab_ia_respuesta"):
        st.markdown("#### 🤖 Interpretación del asistente")
        st.markdown(st.session_state["agl_lab_ia_respuesta"])
        if st.session_state.get("agl_lab_ia_modelo"):
            st.caption(f"Modelo utilizado: {st.session_state['agl_lab_ia_modelo']}")


# ============================================================
# 3. PREPARACIÓN DE SOLUCIÓN LX
# ============================================================

def mostrar_preparacion_lx():

    st.title("🧪 Preparación de Solución para Lixiviación")

    st.write(
        "Estimación de la dosificación de ácido "
        "sulfúrico comercial y agua para preparar "
        "una solución de lixiviación a partir "
        "de un pH objetivo."
    )

    st.warning(
        "Este cálculo es una aproximación ideal. "
        "En soluciones reales, el pH no permite "
        "determinar por sí solo la concentración "
        "total de ácido sulfúrico."
    )

    st.markdown("---")
    st.markdown("### 📥 Parámetros de Operación")

    unidad_volumen = st.selectbox(
        "Unidad de volumen de la solución",
        ["mL", "L"],
        key="lx_unidad_volumen"
    )

    col1, col2 = st.columns(2)

    with col1:
        volumen_solucion = st.number_input(
            f"Volumen de solución [{unidad_volumen}]",
            min_value=0.0,
            value=0.0,
            step=1.0,
            format="%.2f",
            key="lx_volumen_solucion_laboratorio"
        )

        ph_objetivo = st.number_input(
            "pH objetivo",
            min_value=0.0,
            max_value=7.0,
            value=0.0,
            step=0.1,
            format="%.2f",
            key="lx_ph_objetivo"
        )

    with col2:
        pureza_acido = st.number_input(
            "Pureza del ácido comercial [%]",
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            step=0.5,
            format="%.2f",
            key="lx_pureza_acido"
        )

        densidad_acido = st.number_input(
            "Densidad del ácido comercial [g/mL]",
            min_value=0.0,
            max_value=2.5,
            value=0.0,
            step=0.01,
            format="%.2f",
            key="lx_densidad_acido"
        )

    # ========================================================
    # CÁLCULOS: MISMO MODELO, CONVERSIÓN A VOLUMEN DE LABORATORIO
    # ========================================================

    volumen_solucion_l = (
        volumen_solucion / 1000.0
        if unidad_volumen == "mL"
        else volumen_solucion
    )

    concentracion_h = 10.0 ** (-ph_objetivo)
    masa_molar_acido = 98.079

    # Aproximación ideal: dos protones por mol de H₂SO₄.
    acido_puro_g_l = concentracion_h * masa_molar_acido / 2.0
    acido_puro_g = acido_puro_g_l * volumen_solucion_l
    fraccion_pureza = pureza_acido / 100.0
    datos_validos = (
        volumen_solucion > 0 and pureza_acido > 0 and densidad_acido > 0
    )
    acido_comercial_g = (
        acido_puro_g / fraccion_pureza if datos_validos else 0.0
    )

    # g / (g/mL) = mL; se conserva la misma densidad 1,84.
    volumen_acido_ml = (
        acido_comercial_g / densidad_acido if datos_validos else 0.0
    )
    volumen_solucion_ml = volumen_solucion_l * 1000.0
    agua_ml = (volumen_solucion_ml - volumen_acido_ml) if datos_validos else 0.0

    factor_salida = 1.0 if unidad_volumen == "mL" else 1000.0
    volumen_acido = volumen_acido_ml / factor_salida
    volumen_agua = agua_ml / factor_salida

    if datos_validos and agua_ml < -1e-9:
        st.error(
            "El volumen calculado de ácido supera "
            "el volumen total de solución."
        )
        return

    # ========================================================
    # RESULTADOS
    # ========================================================

    st.markdown("---")
    st.markdown("### 📊 Resultados de Dosificación")

    # Presentación destacada: solo volúmenes de ácido y agua.
    # Los cálculos no cambian.
    acido_mostrado = html.escape(numero(volumen_acido))
    agua_mostrada = html.escape(numero(volumen_agua))
    unidad_mostrada = html.escape(unidad_volumen)

    st.markdown(
        f"""
        <div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));
                    gap:16px;margin:14px 0 18px 0;">
          <div style="background:#192737;border:1px solid #325e8a;
                      border-left:6px solid #38bdf8;border-radius:16px;
                      padding:26px 22px;min-width:0;">
            <div style="color:#bae6fd;font-size:17px;font-weight:600;">🧪 Ácido</div>
            <div style="color:#fff;font-size:clamp(28px,3.4vw,46px);
                        font-weight:750;margin-top:12px;">
              {acido_mostrado} <span style="font-size:0.55em;color:#7dd3fc;">{unidad_mostrada}</span>
            </div>
          </div>
          <div style="background:#182b2b;border:1px solid #286b60;
                      border-left:6px solid #34d399;border-radius:16px;
                      padding:26px 22px;min-width:0;">
            <div style="color:#a7f3d0;font-size:17px;font-weight:600;">💧 Agua</div>
            <div style="color:#fff;font-size:clamp(28px,3.4vw,46px);
                        font-weight:750;margin-top:12px;">
              {agua_mostrada} <span style="font-size:0.55em;color:#6ee7b7;">{unidad_mostrada}</span>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ========================================================
    # TABLA DE RESULTADOS LX
    # ========================================================

    st.markdown("---")
    st.markdown("### 📋 Resumen de Preparación de Solución LX")

    tabla_lx = pd.DataFrame({
        "Parámetro": [
            "Volumen de solución",
            "pH objetivo",
            "Pureza del ácido comercial",
            "Densidad del ácido comercial",
            "Volumen de ácido",
            "Volumen de agua"
        ],
        "Valor": [
            volumen_solucion,
            ph_objetivo,
            pureza_acido,
            densidad_acido,
            volumen_acido,
            volumen_agua
        ],
        "Unidad": [
            unidad_volumen,
            "pH",
            "%",
            "g/mL",
            unidad_volumen,
            unidad_volumen
        ]
    })

    mostrar_tabla(
        tabla=tabla_lx,
        clave="descarga_preparacion_lx",
        archivo="preparacion_solucion_lx.xlsx"
    )

    st.info(
        "Para preparar aproximadamente "
        f"{numero(volumen_solucion)} {unidad_volumen} de solución, "
        "el modelo estima "
        f"{numero(volumen_acido)} {unidad_volumen} "
        "de ácido comercial y "
        f"{numero(volumen_agua)} {unidad_volumen} de agua."
    )

    st.caption(
        "Supuestos: disociación completa de "
        "los dos protones del H₂SO₄, "
        "actividad igual a concentración "
        "y volúmenes aditivos."
    )

    st.warning(
        "Para soluciones reales se recomienda "
        "trabajar con concentración de H₂SO₄ "
        "en g/L y mediciones de acidez libre. "
        "Por seguridad, siempre se agrega "
        "el ácido al agua, nunca al revés."
    )

    # ========================================================
    # EXPLICACIÓN DEL RESULTADO CON IA
    # ========================================================

    st.markdown("---")
    st.markdown("### 🤖 Explicación del resultado con IA")
    st.write(
        "Solicita al asistente metalúrgico una interpretación "
        "de la preparación de la solución de lixiviación."
    )

    datos_actuales = (
        unidad_volumen, volumen_solucion, ph_objetivo,
        pureza_acido, densidad_acido
    )
    if st.session_state.get("lx_ia_datos") != datos_actuales:
        st.session_state["lx_ia_datos"] = datos_actuales
        st.session_state.pop("lx_ia_respuesta", None)
        st.session_state.pop("lx_ia_modelo", None)

    if st.button(
        "🤖 Explicar resultado con IA",
        key="lx_boton_explicar_ia",
        use_container_width=True,
        disabled=not datos_validos
    ):
        prompt = (
            "MÓDULO: Preparación de solución para lixiviación con H₂SO₄.\n"
            "Interpreta únicamente los resultados calculados. "
            "Utiliza exactamente estas secciones y en este orden: "
            "1. Resultados; 2. Explicación metalúrgica; "
            "3. Análisis técnico; 4. Recomendaciones; "
            "5. Advertencias de seguridad.\n\n"
            "DATOS Y RESULTADOS:\n"
            f"Volumen de solución objetivo: {volumen_solucion:.2f} {unidad_volumen}\n"
            f"pH objetivo: {ph_objetivo:.2f}\n"
            f"Pureza del ácido comercial: {pureza_acido:.2f} %\n"
            f"Densidad del ácido comercial: {densidad_acido:.2f} g/mL\n"
            f"Concentración ideal estimada de H₂SO₄: {acido_puro_g_l:.2f} g/L\n"
            f"Masa de H₂SO₄ puro: {acido_puro_g:.2f} g\n"
            f"Masa de ácido comercial: {acido_comercial_g:.2f} g\n"
            f"Volumen de ácido comercial: {volumen_acido:.2f} {unidad_volumen}\n"
            f"Volumen de agua estimado: {volumen_agua:.2f} {unidad_volumen}\n\n"
            "INDICACIONES ESPECÍFICAS:\n"
            "En Resultados destaca los volúmenes calculados de ácido y agua. "
            "En Explicación metalúrgica explica el papel del medio ácido "
            "en la lixiviación de minerales oxidados de cobre. "
            "En Análisis técnico señala explícitamente que el cálculo "
            "supone actividad igual a concentración, disociación ideal "
            "de dos protones por mol de H₂SO₄ y aditividad de volúmenes. "
            "El pH por sí solo NO determina la concentración total de ácido "
            "ni la acidez libre de una solución real; la segunda disociación "
            "del H₂SO₄ no es necesariamente completa. "
            "El volumen de agua calculado por diferencia es una "
            "aproximación, no una garantía del volumen final real. "
            "En Recomendaciones indica verificar el pH y la acidez libre "
            "experimentalmente, y ajustar al volumen final según el "
            "procedimiento validado del laboratorio. "
            "En Advertencias de seguridad señala el carácter corrosivo "
            "del H₂SO₄, el calentamiento exotérmico al diluir, el uso "
            "de EPP y procedimientos del laboratorio, y que siempre "
            "se agrega lentamente el ácido al agua, nunca al revés. "
            "No presentes las cantidades estimadas como una receta "
            "experimental validada. No inventes datos ni confundas "
            "masa con flujo másico. Presenta los valores numéricos "
            "con dos decimales y sus unidades."
        )
        try:
            from modulos.asistente import (
                obtener_api_key,
                generar_respuesta,
                interpretar_error,
            )
            api_key = obtener_api_key()
            if not api_key:
                raise ValueError("No se encontró la clave API de Gemini.")

            indicador_ia = st.empty()
            try:
                respuesta, modelo = generar_respuesta(
                    api_key=api_key,
                    mensajes=[],
                    pregunta=prompt,
                    indicador=indicador_ia,
                )
            finally:
                indicador_ia.empty()
            if not respuesta:
                raise ValueError("El asistente no devolvió una respuesta.")
            st.session_state["lx_ia_respuesta"] = respuesta
            st.session_state["lx_ia_modelo"] = modelo
        except Exception as error:
            try:
                mensaje = interpretar_error(error)
            except Exception:
                mensaje = str(error)
            st.error(f"No se pudo generar la explicación con IA: {mensaje}")
            with st.expander("Ver detalles técnicos del error"):
                st.code(f"{type(error).__name__}: {error}")

    if volumen_solucion <= 0:
        st.info("Ingresa un volumen de solución mayor que cero para habilitar la IA.")
    elif st.session_state.get("lx_ia_respuesta"):
        st.markdown("#### 🤖 Interpretación del asistente")
        st.markdown(st.session_state["lx_ia_respuesta"])
        if st.session_state.get("lx_ia_modelo"):
            st.caption(f"Modelo utilizado: {st.session_state['lx_ia_modelo']}")

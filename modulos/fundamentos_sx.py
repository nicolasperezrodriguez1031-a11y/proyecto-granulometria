
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components


# ============================================================
# FUNDAMENTOS DEL PROCESO DE EXTRACCIÓN POR SOLVENTES
# ============================================================

def mostrar_fundamentos_sx():

    st.title("📘 Fundamentos de Extracción por Solventes (SX)")

    st.write(
        "La extracción por solventes (SX) es una operación "
        "hidrometalúrgica utilizada para separar, concentrar "
        "y purificar el cobre contenido en soluciones acuosas "
        "provenientes de la lixiviación. Su objetivo es "
        "transferir selectivamente el cobre hacia una fase "
        "orgánica y posteriormente recuperarlo en un "
        "electrolito adecuado para electroobtención."
    )

    st.info(
        "La extracción por solventes constituye la etapa "
        "intermedia del circuito Lixiviación – Extracción "
        "por Solventes – Electroobtención (LX–SX–EW)."
    )

    st.markdown("---")

    # ========================================================
    # 1. OBJETIVO DEL PROCESO
    # ========================================================

    st.header("1. Objetivo del Proceso SX")

    st.write(
        "El propósito de SX es recuperar selectivamente "
        "los iones de cobre presentes en el PLS, disminuir "
        "la transferencia de impurezas y generar un "
        "electrolito rico en cobre para alimentar la "
        "etapa de electroobtención."
    )

    st.markdown(
        """
        **Principales funciones:**

        - Recuperar el cobre disuelto en el PLS.
        - Concentrar el cobre en una solución electrolítica.
        - Favorecer la separación del cobre respecto de impurezas.
        - Permitir la recirculación del orgánico.
        - Preparar la alimentación para electroobtención.
        """
    )

    st.markdown("---")

    # ========================================================
    # 2. FUNDAMENTO QUÍMICO
    # ========================================================

    st.header("2. Fundamento Químico")

    st.write(
        "La extracción por solventes se basa en la "
        "distribución selectiva de una especie química "
        "entre dos fases líquidas prácticamente inmiscibles: "
        "una fase acuosa y una fase orgánica."
    )

    st.subheader("2.1. Reacción de extracción")

    st.latex(
        r"Cu^{2+}_{(ac)} + 2RH_{(org)} "
        r"\rightleftharpoons "
        r"CuR_{2(org)} + 2H^{+}_{(ac)}"
    )

    st.write(
        "En esta representación simplificada, RH corresponde "
        "al extractante orgánico. Durante la extracción, "
        "el cobre pasa desde la solución acuosa hacia "
        "la fase orgánica y se liberan protones."
    )

    st.subheader("2.2. Reacción de reextracción")

    st.latex(
        r"CuR_{2(org)} + 2H^{+}_{(ac)} "
        r"\rightleftharpoons "
        r"Cu^{2+}_{(ac)} + 2RH_{(org)}"
    )

    st.write(
        "En la reextracción, una solución electrolítica "
        "ácida favorece la transferencia del cobre "
        "desde el orgánico cargado hacia la fase acuosa."
    )

    st.markdown("---")

    # ========================================================
    # 3. TÉCNICA DE EXTRACCIÓN
    # ========================================================

    st.header("3. Técnica de Extracción por Solventes")

    st.write(
        "Una configuración industrial habitual utiliza "
        "equipos mezcladores-decantadores "
        "(mixer-settlers), en los cuales las fases "
        "acuosa y orgánica se contactan y posteriormente "
        "se separan por diferencia de densidades."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Mezclador")

        st.write(
            "En el mezclador se ponen en contacto ambas "
            "fases mediante agitación controlada. "
            "Esto facilita la transferencia de cobre "
            "entre la solución acuosa y el orgánico."
        )

    with col2:

        st.subheader("Decantador")

        st.write(
            "En el decantador se reduce la turbulencia "
            "para permitir la separación de las fases. "
            "La fase orgánica y la acuosa se recuperan "
            "por salidas independientes."
        )

    st.warning(
        "Una agitación excesiva o condiciones "
        "inadecuadas pueden favorecer la formación "
        "de emulsiones y el arrastre de fases."
    )

    st.markdown("---")

    # ========================================================
    # 4. ETAPAS DEL CIRCUITO
    # ========================================================

    st.header("4. Etapas del Circuito SX")

    with st.expander("4.1. Extracción", expanded=True):

        st.write(
            "El PLS procedente de lixiviación entra en "
            "contacto con el orgánico descargado. "
            "El extractante retiene selectivamente "
            "el cobre y genera orgánico cargado."
        )

        st.markdown(
            """
            **Entradas:** PLS y orgánico descargado.

            **Salidas:** Refino y orgánico cargado.
            """
        )

    with st.expander("4.2. Lavado del orgánico"):

        st.write(
            "El lavado, cuando está incorporado al circuito, "
            "permite reducir el arrastre de solución acuosa "
            "y determinadas impurezas asociadas al "
            "orgánico cargado antes de la reextracción."
        )

        st.markdown(
            """
            **Entrada principal:** Orgánico cargado.

            **Otra alimentación:** Solución de lavado.

            **Salida principal:** Orgánico lavado.
            """
        )

    with st.expander("4.3. Reextracción"):

        st.write(
            "El orgánico cargado entra en contacto con "
            "electrolito pobre de elevada acidez. "
            "El cobre se transfiere a la solución "
            "electrolítica, formando electrolito rico."
        )

        st.markdown(
            """
            **Entradas:** Orgánico cargado y electrolito pobre.

            **Salidas:** Orgánico descargado y electrolito rico.
            """
        )

    with st.expander("4.4. Electroobtención"):

        st.write(
            "El electrolito rico alimenta las celdas "
            "de electroobtención, donde la corriente "
            "eléctrica permite depositar cobre metálico "
            "sobre los cátodos."
        )

        st.write(
            "El electrolito empobrecido en cobre puede "
            "retornar a reextracción, de acuerdo con "
            "el diseño y las condiciones del circuito."
        )

    st.markdown("---")

    # ========================================================
    # 5. DIAGRAMA GENERAL CORREGIDO
    # ========================================================

    st.header("5. Diagrama General del Proceso")

    st.write(
        "El siguiente esquema representa las etapas "
        "de extracción, lavado, reextracción y "
        "electroobtención, mostrando las corrientes "
        "acuosas, orgánicas y sus recirculaciones."
    )

    diagrama = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
    <meta charset="UTF-8">

    <style>
        html, body {
            margin: 0;
            padding: 0;
            background: transparent;
            font-family: Arial, sans-serif;
        }

        .contenedor {
            background: #111827;
            border: 1px solid #374151;
            border-radius: 12px;
            padding: 8px;
            box-sizing: border-box;
            width: 100%;
        }

        svg {
            width: 100%;
            height: auto;
            display: block;
        }
    </style>
    </head>

    <body>
    <div class="contenedor">

    <svg viewBox="0 0 1100 610"
         xmlns="http://www.w3.org/2000/svg">

        <defs>

            <marker id="flechaAzul"
                    viewBox="0 0 10 10"
                    refX="9"
                    refY="5"
                    markerWidth="7"
                    markerHeight="7"
                    orient="auto">
                <path d="M0 0 L10 5 L0 10 Z"
                      fill="#38bdf8"/>
            </marker>

            <marker id="flechaAmarilla"
                    viewBox="0 0 10 10"
                    refX="9"
                    refY="5"
                    markerWidth="7"
                    markerHeight="7"
                    orient="auto">
                <path d="M0 0 L10 5 L0 10 Z"
                      fill="#fbbf24"/>
            </marker>

            <marker id="flechaVerde"
                    viewBox="0 0 10 10"
                    refX="9"
                    refY="5"
                    markerWidth="7"
                    markerHeight="7"
                    orient="auto">
                <path d="M0 0 L10 5 L0 10 Z"
                      fill="#34d399"/>
            </marker>

        </defs>

        <!-- EQUIPOS PRINCIPALES -->

        <g fill="#1f2937"
           stroke="#64748b"
           stroke-width="2">

            <rect x="70" y="240"
                  width="200" height="100" rx="12"/>

            <rect x="345" y="240"
                  width="200" height="100" rx="12"/>

            <rect x="620" y="240"
                  width="200" height="100" rx="12"/>

            <rect x="895" y="240"
                  width="150" height="100" rx="12"/>

        </g>

        <!-- NOMBRES DE EQUIPOS -->

        <g fill="white"
           font-size="18"
           font-weight="bold"
           text-anchor="middle">

            <text x="170" y="285">EXTRACCIÓN</text>
            <text x="445" y="285">LAVADO</text>
            <text x="720" y="285">REEXTRACCIÓN</text>
            <text x="970" y="285">EW</text>

        </g>

        <!-- CORRIENTE ORGÁNICA PRINCIPAL -->

        <g stroke="#fbbf24"
           stroke-width="3"
           fill="none"
           marker-end="url(#flechaAmarilla)">

            <path d="M270 290 H345"/>
            <path d="M545 290 H620"/>

        </g>

        <g fill="#fbbf24"
           font-size="14"
           text-anchor="middle">

            <text x="307" y="260">
                Orgánico cargado
            </text>

            <text x="582" y="260">
                Orgánico lavado
            </text>

        </g>

        <!-- PLS HACIA EXTRACCIÓN -->

        <path d="M170 115 V240"
              stroke="#38bdf8"
              stroke-width="3"
              fill="none"
              marker-end="url(#flechaAzul)"/>

        <g fill="#38bdf8"
           font-size="15"
           text-anchor="middle">

            <text x="170" y="75">PLS</text>
            <text x="170" y="95">
                3–6 g/L Cu
            </text>

        </g>

        <!-- REFINO SALIENDO DE EXTRACCIÓN -->

        <path d="M110 340 V405 H45"
              stroke="#38bdf8"
              stroke-width="3"
              fill="none"
              marker-end="url(#flechaAzul)"/>

        <g fill="#38bdf8"
           font-size="15"
           text-anchor="middle">

            <text x="100" y="445">Refino</text>
            <text x="100" y="465">
                Menor concentración de Cu
            </text>

        </g>

        <!-- SOLUCIÓN DE LAVADO -->

        <path d="M445 115 V240"
              stroke="#38bdf8"
              stroke-width="3"
              fill="none"
              marker-end="url(#flechaAzul)"/>

        <text x="445" y="85"
              fill="#38bdf8"
              font-size="15"
              text-anchor="middle">
            Solución de lavado
        </text>

        <!-- ELECTROLITO POBRE HACIA REEXTRACCIÓN -->

        <path d="M720 115 V240"
              stroke="#38bdf8"
              stroke-width="3"
              fill="none"
              marker-end="url(#flechaAzul)"/>

        <g fill="#38bdf8"
           font-size="15"
           text-anchor="middle">

            <text x="720" y="75">
                Electrolito pobre
            </text>

            <text x="720" y="95">
                35–40 g/L Cu
            </text>

        </g>

        <!-- ELECTROLITO RICO HACIA EW -->

        <path d="M820 290 H895"
              stroke="#34d399"
              stroke-width="3"
              fill="none"
              marker-end="url(#flechaVerde)"/>

        <text x="855" y="245"
              fill="#34d399"
              font-size="14"
              text-anchor="middle">
            Electrolito rico
        </text>

        <!-- CÁTODOS DE COBRE -->

        <path d="M970 340 V410"
              stroke="#34d399"
              stroke-width="3"
              fill="none"
              marker-end="url(#flechaVerde)"/>

        <g fill="#34d399"
           font-size="15"
           text-anchor="middle">

            <text x="970" y="445">
                Cátodos de cobre
            </text>

        </g>

        <!-- RECIRCULACIÓN DEL ORGÁNICO DESCARGADO -->

        <path d="M720 340 V525 H220 V340"
              stroke="#fbbf24"
              stroke-width="3"
              fill="none"
              marker-end="url(#flechaAmarilla)"/>

        <text x="470" y="510"
              fill="#fbbf24"
              font-size="15"
              text-anchor="middle">
            Retorno de orgánico descargado
        </text>

        <!-- NOTA -->

        <text x="550" y="585"
              fill="#94a3b8"
              font-size="13"
              text-anchor="middle">
            Diagrama conceptual simplificado del circuito SX–EW
        </text>

    </svg>
    </div>
    </body>
    </html>
    """

    components.html(
        diagrama,
        height=620,
        scrolling=False
    )

    st.caption(
        "Diagrama conceptual. Las concentraciones "
        "mostradas son referenciales y dependen "
        "de las condiciones reales de operación."
    )

    st.markdown("---")

    # ========================================================
    # 6. CORRIENTES DEL PROCESO
    # ========================================================

    st.header("6. Corrientes del Proceso")

    tabla_corrientes = pd.DataFrame({
        "Corriente": [
            "PLS",
            "Orgánico descargado",
            "Refino",
            "Orgánico cargado",
            "Electrolito pobre",
            "Electrolito rico"
        ],
        "Descripción": [
            "Solución acuosa rica proveniente de lixiviación",
            "Fase orgánica que retorna desde reextracción",
            "Solución acuosa después de extracción",
            "Fase orgánica enriquecida en cobre",
            "Solución electrolítica que ingresa a reextracción",
            "Solución concentrada en cobre destinada a EW"
        ]
    })

    st.dataframe(
        tabla_corrientes,
        hide_index=True,
        use_container_width=True
    )

    st.markdown("---")

    # ========================================================
    # 7. CONCENTRACIONES REFERENCIALES
    # ========================================================

    st.header("7. Concentraciones Referenciales")

    st.write(
        "Los siguientes valores son ejemplos "
        "referenciales utilizados en el proyecto. "
        "No constituyen rangos universales de operación."
    )

    tabla_concentraciones = pd.DataFrame({
        "Corriente": [
            "PLS",
            "Refino",
            "Orgánico descargado",
            "Orgánico cargado",
            "Electrolito pobre",
            "Electrolito rico"
        ],
        "Concentración Cu": [
            "3–6 g/L",
            "Menor que 1 g/L",
            "Menor que 0,5 g/L",
            "4–8 g/L",
            "35–40 g/L",
            "40–46 g/L"
        ]
    })

    st.dataframe(
        tabla_concentraciones,
        hide_index=True,
        use_container_width=True
    )

    st.caption(
        "Las concentraciones reales dependen de la "
        "alimentación, del extractante, de la configuración "
        "del circuito y de las condiciones operacionales."
    )

    st.markdown("---")

    # ========================================================
    # 8. VARIABLES OPERACIONALES
    # ========================================================

    st.header("8. Principales Variables Operacionales")

    variables = pd.DataFrame({
        "Variable": [
            "pH",
            "Razón A/O",
            "Concentración de Cu",
            "Caudal",
            "Tiempo de contacto",
            "Temperatura",
            "Separación de fases"
        ],
        "Importancia": [
            "Influye en el equilibrio de extracción",
            "Relaciona el caudal acuoso con el orgánico",
            "Permite calcular la transferencia de cobre",
            "Determina la alimentación y capacidad hidráulica",
            "Influye en la aproximación al equilibrio",
            "Afecta propiedades físicas y equilibrio",
            "Controla arrastres y estabilidad operacional"
        ]
    })

    st.dataframe(
        variables,
        hide_index=True,
        use_container_width=True
    )

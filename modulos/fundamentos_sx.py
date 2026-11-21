
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components


# Fundamentos del proceso SX, basados en el apartado 2.2.3.3 de la tesis.
def mostrar_fundamentos_sx():
    st.title("📘 Fundamentos de Extracción por Solventes (SX)")
    st.write(
        "La extracción por solventes es una etapa posterior a la lixiviación. "
        "Utiliza la solución rica de lixiviación (PLS) para concentrar y purificar "
        "el cobre disuelto, preparando una solución adecuada para la electroobtención."
    )
    st.info("Circuito hidrometalúrgico: Lixiviación → Extracción → Lavado (cuando corresponde) → Reextracción → Electroobtención.")

    st.header("1. Fundamentos químicos")
    st.write(
        "El proceso se basa en el intercambio iónico de cobre entre dos fases "
        "líquidas inmiscibles: una acuosa y otra orgánica. El pH y la acidez "
        "de la fase acuosa condicionan el sentido de la transferencia de cobre. "
        "La extracción y la reextracción utilizan el mismo principio químico "
        "en condiciones opuestas."
    )
    st.subheader("1.1. Reacción de extracción")
    st.latex(r"Cu^{2+}_{(ac)} + 2RH_{(org)} \rightleftharpoons R_2Cu_{(org)} + 2H^{+}_{(ac)}")
    st.write("El cobre del PLS pasa al extractante orgánico y se liberan protones a la fase acuosa.")
    st.subheader("1.2. Reacción de reextracción")
    st.latex(r"R_2Cu_{(org)} + 2H^{+}_{(ac)} \rightleftharpoons Cu^{2+}_{(ac)} + 2RH_{(org)}")
    st.write("El contacto con un electrolito ácido permite devolver el cobre desde el orgánico cargado a la fase acuosa.")

    st.header("2. Separación de fases")
    st.markdown(
        """- **Inmiscibilidad:** las fases acuosa y orgánica no se mezclan completamente, lo que permite separarlas.
- **Diferencia de densidad:** normalmente, la fase orgánica es menos densa y se sitúa sobre la acuosa.
- **Tiempo de separación:** es un parámetro importante para evaluar la separabilidad y el funcionamiento de los sedimentadores."""
    )
    st.write("En laboratorio pueden emplearse embudos de agitación y equipos para evaluar el tiempo de separación de fases.")

    st.header("3. Etapas de extracción por solventes")
    st.write("El circuito comprende principalmente extracción y reextracción. Según su configuración, puede incluir una etapa intermedia de lavado.")
    with st.expander("3.1. Extracción", expanded=True):
        st.write("El PLS entra en contacto con orgánico descargado. El extractante transfiere cobre desde la fase acuosa hacia la orgánica; después de la separación se obtienen refino y orgánico cargado.")
        st.markdown("**Entradas:** PLS y orgánico descargado.  \n**Salidas:** refino y orgánico cargado.")
        st.markdown("**Concentraciones referenciales citadas en la tesis:** PLS 2–6 g/L de Cu; refino aproximadamente 0,3–0,5 g/L; orgánico cargado 4–8 g/L.")
        st.latex(r"2RH + CuSO_4 \rightarrow R_2Cu + H_2SO_4")
        st.caption("Ecuación simplificada del intercambio iónico durante la extracción.")
    with st.expander("3.2. Lavado"):
        st.write("El lavado busca disminuir el arrastre de soluciones acuosas y determinadas impurezas presentes en el orgánico cargado. Ayuda a limitar el transporte de contaminantes hacia el electrolito, incluidos cloruros y manganeso.")
        st.markdown("**Entradas:** orgánico cargado y solución de lavado.  \n**Salida principal:** orgánico lavado.")
    with st.expander("3.3. Reextracción"):
        st.write("El orgánico cargado entra en contacto con electrolito pobre ácido. El cobre pasa desde la fase orgánica al electrolito, generando electrolito rico; el orgánico descargado retorna a extracción.")
        st.markdown("**Entradas:** orgánico cargado y electrolito pobre.  \n**Salidas:** orgánico descargado y electrolito rico.")
        st.markdown("**Concentraciones referenciales citadas en la tesis:** electrolito pobre 32–36 g/L de Cu y electrolito rico 40–46 g/L de Cu.")
        st.latex(r"R_2Cu + H_2SO_4 \rightarrow 2RH + CuSO_4")
        st.caption("Ecuación simplificada del intercambio iónico durante la reextracción.")

    st.header("4. Razón de flujo acuoso/orgánico (FA/FO)")
    st.write("La razón de flujo relaciona los caudales de las fases acuosa y orgánica. Es relevante para la carga del orgánico, la extracción por etapa y la estabilidad hidráulica de la dispersión.")
    st.latex(r"FA/FO = \frac{Q_{acuoso}}{Q_{organico}}")
    st.write("La tesis también describe la razón inversa O/A. Un valor elevado de O/A puede favorecer la transferencia de cobre al orgánico, pero aumentar su inventario y afectar la hidráulica del circuito.")
    st.caption("FA/FO y O/A son razones inversas; debe verificarse cuál se está utilizando antes de comparar valores.")

    st.header("5. Diagrama general del proceso")
    st.write("Representación conceptual de las corrientes acuosas y orgánicas del circuito SX–EW, incluida la recirculación del orgánico descargado.")

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
                2–6 g/L Cu
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

        <!-- ELECTROLITO POBRE: RETORNO DESDE EW A REEXTRACCIÓN -->

        <path d="M970 240 V155 H720 V240"
              stroke="#38bdf8"
              stroke-width="3"
              fill="none"
              marker-end="url(#flechaAzul)"/>

        <g fill="#38bdf8"
           font-size="15"
           text-anchor="middle">

            <text x="845" y="115">
                Electrolito pobre
            </text>

            <text x="845" y="135">
                32–36 g/L Cu
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

    st.caption("Diagrama conceptual. Las concentraciones indicadas son referenciales y pueden variar según las condiciones de operación.")

    st.header("6. Corrientes principales")
    corrientes = pd.DataFrame({
        "Corriente": ["PLS", "Orgánico descargado", "Refino", "Orgánico cargado", "Electrolito pobre", "Electrolito rico"],
        "Función": [
            "Solución acuosa procedente de lixiviación que alimenta extracción",
            "Fase orgánica que retorna de reextracción hacia extracción",
            "Fase acuosa empobrecida en cobre que sale de extracción",
            "Fase orgánica enriquecida en cobre que pasa a lavado o reextracción",
            "Solución ácida que ingresa a reextracción desde el circuito EW",
            "Solución enriquecida en cobre que alimenta electroobtención"
        ]
    })
    st.dataframe(corrientes, hide_index=True, use_container_width=True)

    st.header("7. Concentraciones referenciales de la tesis")
    concentraciones = pd.DataFrame({
        "Corriente": ["PLS", "Refino", "Orgánico descargado", "Orgánico cargado", "Electrolito pobre", "Electrolito rico"],
        "Concentración de Cu": ["2–6 g/L", "Aproximadamente 0,3–0,5 g/L", "Aproximadamente 0,4–1,0 g/L", "4–8 g/L", "32–36 g/L", "40–46 g/L"]
    })
    st.dataframe(concentraciones, hide_index=True, use_container_width=True)
    st.caption("Valores presentados en el apartado 2.2.3.3 de la tesis; no constituyen límites universales de operación.")


import streamlit as st
import pandas as pd


# ============================================================
# DATOS DE POTENCIALES ESTÁNDAR DE REDUCCIÓN
# ============================================================

# Valores aproximados a 25 °C, referidos al electrodo
# estándar de hidrógeno (ESH).
#
# Todas las semirreacciones se expresan como reducciones.

POTENCIALES = [
    {
        "par": "Li⁺/Li",
        "reaccion": "Li⁺ + e⁻ → Li(s)",
        "potencial": -3.04
    },
    {
        "par": "K⁺/K",
        "reaccion": "K⁺ + e⁻ → K(s)",
        "potencial": -2.93
    },
    {
        "par": "Ca²⁺/Ca",
        "reaccion": "Ca²⁺ + 2e⁻ → Ca(s)",
        "potencial": -2.87
    },
    {
        "par": "Na⁺/Na",
        "reaccion": "Na⁺ + e⁻ → Na(s)",
        "potencial": -2.71
    },
    {
        "par": "Mg²⁺/Mg",
        "reaccion": "Mg²⁺ + 2e⁻ → Mg(s)",
        "potencial": -2.37
    },
    {
        "par": "Al³⁺/Al",
        "reaccion": "Al³⁺ + 3e⁻ → Al(s)",
        "potencial": -1.66
    },
    {
        "par": "Zn²⁺/Zn",
        "reaccion": "Zn²⁺ + 2e⁻ → Zn(s)",
        "potencial": -0.76
    },
    {
        "par": "Cr³⁺/Cr",
        "reaccion": "Cr³⁺ + 3e⁻ → Cr(s)",
        "potencial": -0.74
    },
    {
        "par": "Fe²⁺/Fe",
        "reaccion": "Fe²⁺ + 2e⁻ → Fe(s)",
        "potencial": -0.44
    },
    {
        "par": "Ni²⁺/Ni",
        "reaccion": "Ni²⁺ + 2e⁻ → Ni(s)",
        "potencial": -0.25
    },
    {
        "par": "Sn²⁺/Sn",
        "reaccion": "Sn²⁺ + 2e⁻ → Sn(s)",
        "potencial": -0.14
    },
    {
        "par": "Pb²⁺/Pb",
        "reaccion": "Pb²⁺ + 2e⁻ → Pb(s)",
        "potencial": -0.13
    },
    {
        "par": "H⁺/H₂",
        "reaccion": "2H⁺ + 2e⁻ → H₂(g)",
        "potencial": 0.00
    },
    {
        "par": "Cu²⁺/Cu⁺",
        "reaccion": "Cu²⁺ + e⁻ → Cu⁺",
        "potencial": 0.16
    },
    {
        "par": "Cu²⁺/Cu",
        "reaccion": "Cu²⁺ + 2e⁻ → Cu(s)",
        "potencial": 0.34
    },
    {
        "par": "Cu⁺/Cu",
        "reaccion": "Cu⁺ + e⁻ → Cu(s)",
        "potencial": 0.52
    },
    {
        "par": "I₂/I⁻",
        "reaccion": "I₂ + 2e⁻ → 2I⁻",
        "potencial": 0.54
    },
    {
        "par": "Fe³⁺/Fe²⁺",
        "reaccion": "Fe³⁺ + e⁻ → Fe²⁺",
        "potencial": 0.77
    },
    {
        "par": "Ag⁺/Ag",
        "reaccion": "Ag⁺ + e⁻ → Ag(s)",
        "potencial": 0.80
    },
    {
        "par": "Br₂/Br⁻",
        "reaccion": "Br₂ + 2e⁻ → 2Br⁻",
        "potencial": 1.09
    },
    {
        "par": "O₂/H₂O",
        "reaccion": "O₂ + 4H⁺ + 4e⁻ → 2H₂O",
        "potencial": 1.23
    },
    {
        "par": "Cl₂/Cl⁻",
        "reaccion": "Cl₂ + 2e⁻ → 2Cl⁻",
        "potencial": 1.36
    },
    {
        "par": "Au³⁺/Au",
        "reaccion": "Au³⁺ + 3e⁻ → Au(s)",
        "potencial": 1.50
    }
]


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def formatear_potencial(valor):
    """
    Formatea el potencial con signo y coma decimal.
    """

    return f"{valor:+.2f}".replace(".", ",")


def obtener_potencial(nombre_par):
    """
    Busca el potencial estándar de un par redox.
    """

    for elemento in POTENCIALES:

        if elemento["par"] == nombre_par:
            return elemento["potencial"]

    return None


# ============================================================
# PÁGINA PRINCIPAL
# ============================================================

def mostrar_potenciales_reduccion():

    st.title("🔋 Potenciales Estándar de Reducción")

    st.write(
        "Consulta los potenciales estándar de reducción "
        "de distintas especies químicas y calcula "
        "la diferencia de potencial entre dos pares redox."
    )

    st.markdown("---")

    # ========================================================
    # 1. TABLA DE POTENCIALES ESTÁNDAR
    # ========================================================

    st.header("1. Tabla de Potenciales Estándar")

    st.write(
        "La siguiente tabla presenta valores de referencia "
        "de potenciales estándar de reducción a 25 °C. "
        "Los valores pueden variar ligeramente según "
        "la fuente y las convenciones utilizadas."
    )

    datos_tabla = []

    for elemento in POTENCIALES:

        datos_tabla.append(
            {
                "Par redox": elemento["par"],
                "Semirreacción de reducción":
                    elemento["reaccion"],
                "E° (V)": elemento["potencial"]
            }
        )

    tabla = pd.DataFrame(datos_tabla)

    st.dataframe(
        tabla,
        use_container_width=True,
        hide_index=True,
        column_config={
            "E° (V)": st.column_config.NumberColumn(
                "E° (V)",
                format="%.2f"
            )
        }
    )

    st.caption(
        "Los valores corresponden a semirreacciones "
        "escritas en sentido de reducción."
    )

    st.markdown("---")

    # ========================================================
    # 2. CALCULADORA INTERACTIVA
    # ========================================================

    st.header(
        "2. Calculadora de Potencial Estándar de Celda"
    )

    st.write(
        "Selecciona dos pares redox para calcular "
        "la diferencia de potencial estándar "
        "de una celda electroquímica."
    )

    nombres_pares = [
        elemento["par"]
        for elemento in POTENCIALES
    ]

    indice_cobre = nombres_pares.index("Cu²⁺/Cu")
    indice_zinc = nombres_pares.index("Zn²⁺/Zn")

    columna_catodo, columna_anodo = st.columns(2)

    # --------------------------------------------------------
    # SELECCIÓN DEL CÁTODO
    # --------------------------------------------------------

    with columna_catodo:

        par_catodo = st.selectbox(
            "Par redox del cátodo (reducción)",
            options=nombres_pares,
            index=indice_cobre,
            key="potencial_par_catodo"
        )

    # --------------------------------------------------------
    # SELECCIÓN DEL ÁNODO
    # --------------------------------------------------------

    with columna_anodo:

        par_anodo = st.selectbox(
            "Par redox del ánodo (oxidación)",
            options=nombres_pares,
            index=indice_zinc,
            key="potencial_par_anodo"
        )

    # --------------------------------------------------------
    # CÁLCULO DE POTENCIALES
    # --------------------------------------------------------

    potencial_catodo = obtener_potencial(par_catodo)

    potencial_anodo = obtener_potencial(par_anodo)

    diferencia_potencial = (
        potencial_catodo - potencial_anodo
    )

    # --------------------------------------------------------
    # RESULTADOS
    # --------------------------------------------------------

    st.markdown("### 📊 Resultados del Cálculo")

    r1, r2, r3 = st.columns(3)

    with r1:

        st.metric(
            "E° del cátodo",
            f"{formatear_potencial(potencial_catodo)} V"
        )

    with r2:

        st.metric(
            "E° del ánodo (como reducción)",
            f"{formatear_potencial(potencial_anodo)} V"
        )

    with r3:

        st.metric(
            "E° de celda",
            f"{formatear_potencial(diferencia_potencial)} V"
        )

    # --------------------------------------------------------
    # FÓRMULA
    # --------------------------------------------------------

    st.markdown("### Fórmula del Potencial de Celda")

    st.latex(
        r"E^\circ_{celda}="
        r"E^\circ_{catodo}-E^\circ_{anodo}"
    )

    # --------------------------------------------------------
    # INTERPRETACIÓN DEL RESULTADO
    # --------------------------------------------------------

    st.markdown("### Interpretación del Resultado")

    if par_catodo == par_anodo:

        st.info(
            "Seleccionaste el mismo par redox "
            "para ambos electrodos. "
            "Con los mismos estados estándar, "
            "la diferencia de potencial es cero."
        )

    elif diferencia_potencial > 0:

        st.success(
            "E° de celda positivo: la reacción "
            "global, con las semirreacciones "
            "seleccionadas, es espontánea "
            "en condiciones estándar."
        )

    elif diferencia_potencial < 0:

        st.warning(
            "E° de celda negativo: la reacción "
            "global escrita no es espontánea "
            "en condiciones estándar. "
            "La reacción inversa presenta "
            "un potencial positivo."
        )

    else:

        st.info(
            "E° de celda igual a cero: "
            "no existe una fuerza electromotriz "
            "estándar neta para la combinación "
            "seleccionada."
        )

    st.caption(
        "El potencial del ánodo se introduce "
        "como potencial de reducción, aunque "
        "la semirreacción anódica ocurre "
        "en sentido de oxidación."
    )

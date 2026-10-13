
import html
import streamlit as st
import pandas as pd


# ============================================================
# BASE DE DATOS MINERALÓGICA
# ============================================================

MINERALES = [
    {
        "nombre": "Malaquita",
        "formula": "Cu₂CO₃(OH)₂",
        "grupo": "Cobre",
        "elemento": "Cu",
        "ley": 57.5,
        "densidad": "3.75 - 4.00 g/cm³",
        "dureza": "3.5 - 4.0",
        "acido": "Alto (carbonatos)",
        "solubilidad": "Soluble en ácidos diluidos",
        "color": "#22c55e",
        "composicion": {
            "Cobre (Cu)": "57.5%",
            "Oxígeno (O)": "37.1%",
            "Carbono (C)": "5.4%",
            "Hidrógeno (H)": "0.9%"
        }
    },
    {
        "nombre": "Azurita",
        "formula": "Cu₃(CO₃)₂(OH)₂",
        "grupo": "Cobre",
        "elemento": "Cu",
        "ley": 55.3,
        "densidad": "3.77 - 3.83 g/cm³",
        "dureza": "3.5 - 4.0",
        "acido": "Alto (carbonatos)",
        "solubilidad": "Soluble en ácidos diluidos",
        "color": "#3b82f6",
        "composicion": {
            "Cobre (Cu)": "55.3%",
            "Oxígeno (O)": "37.1%",
            "Carbono (C)": "7.0%",
            "Hidrógeno (H)": "0.6%"
        }
    },
    {
        "nombre": "Crisocola",
        "formula": "Silicato hidratado de cobre",
        "grupo": "Cobre",
        "elemento": "Cu",
        "ley": 36.0,
        "densidad": "2.0 - 2.4 g/cm³",
        "dureza": "2.0 - 4.0",
        "acido": "Variable",
        "solubilidad": "Comportamiento variable en medio ácido",
        "color": "#06b6d4",
        "composicion": {
            "Cobre (Cu)": "Variable; 36% referencial",
            "Silicio (Si)": "Variable",
            "Aluminio (Al)": "Variable",
            "Agua y otros": "Variable"
        }
    },
    {
        "nombre": "Cuprita",
        "formula": "Cu₂O",
        "grupo": "Cobre",
        "elemento": "Cu",
        "ley": 88.8,
        "densidad": "6.10 g/cm³",
        "dureza": "3.5 - 4.0",
        "acido": "Variable",
        "solubilidad": "Depende del medio y condiciones redox",
        "color": "#ef4444",
        "composicion": {
            "Cobre (Cu)": "88.8%",
            "Oxígeno (O)": "11.2%"
        }
    },
    {
        "nombre": "Tenorita",
        "formula": "CuO",
        "grupo": "Cobre",
        "elemento": "Cu",
        "ley": 79.9,
        "densidad": "6.30 - 6.45 g/cm³",
        "dureza": "3.0 - 4.0",
        "acido": "Variable",
        "solubilidad": "Soluble en ácidos diluidos",
        "color": "#94a3b8",
        "composicion": {
            "Cobre (Cu)": "79.9%",
            "Oxígeno (O)": "20.1%"
        }
    },
    {
        "nombre": "Atacamita",
        "formula": "Cu₂Cl(OH)₃",
        "grupo": "Cobre",
        "elemento": "Cu",
        "ley": 59.5,
        "densidad": "3.75 - 3.77 g/cm³",
        "dureza": "3.0 - 3.5",
        "acido": "Variable",
        "solubilidad": "Soluble en medios ácidos",
        "color": "#16a34a",
        "composicion": {
            "Cobre (Cu)": "59.5%",
            "Cloro (Cl)": "16.6%",
            "Oxígeno (O)": "22.4%",
            "Hidrógeno (H)": "1.4%"
        }
    },
    {
        "nombre": "Brochantita",
        "formula": "Cu₄SO₄(OH)₆",
        "grupo": "Cobre",
        "elemento": "Cu",
        "ley": 56.2,
        "densidad": "3.90 g/cm³",
        "dureza": "3.5 - 4.0",
        "acido": "Variable",
        "solubilidad": "Soluble en medios ácidos",
        "color": "#10b981",
        "composicion": {
            "Cobre (Cu)": "56.2%",
            "Azufre (S)": "7.1%",
            "Oxígeno (O)": "35.4%",
            "Hidrógeno (H)": "1.3%"
        }
    },
    {
        "nombre": "Calcantita",
        "formula": "CuSO₄·5H₂O",
        "grupo": "Cobre",
        "elemento": "Cu",
        "ley": 25.5,
        "densidad": "2.28 g/cm³",
        "dureza": "2.5",
        "acido": "No requiere ácido para disolverse",
        "solubilidad": "Alta solubilidad en agua",
        "color": "#0ea5e9",
        "composicion": {
            "Cobre (Cu)": "25.5%",
            "Azufre (S)": "12.8%",
            "Oxígeno (O)": "57.7%",
            "Hidrógeno (H)": "4.0%"
        }
    },
    {
        "nombre": "Óxido áurico",
        "formula": "Au₂O₃",
        "grupo": "Otros",
        "elemento": "Au",
        "ley": 89.1,
        "densidad": "Variable",
        "dureza": "No definida",
        "acido": "No aplica directamente",
        "solubilidad": "Compuesto poco estable; no es un mineral habitual",
        "color": "#eab308",
        "composicion": {
            "Oro (Au)": "89.1%",
            "Oxígeno (O)": "10.9%"
        }
    },
    {
        "nombre": "Cincita",
        "formula": "ZnO",
        "grupo": "Otros",
        "elemento": "Zn",
        "ley": 80.3,
        "densidad": "5.43 - 5.70 g/cm³",
        "dureza": "4.0",
        "acido": "Variable",
        "solubilidad": "Soluble en ácidos diluidos",
        "color": "#a1a1aa",
        "composicion": {
            "Zinc (Zn)": "80.3%",
            "Oxígeno (O)": "19.7%"
        }
    },
    {
        "nombre": "Hematita",
        "formula": "Fe₂O₃",
        "grupo": "Otros",
        "elemento": "Fe",
        "ley": 69.9,
        "densidad": "5.26 g/cm³",
        "dureza": "5.5 - 6.5",
        "acido": "Variable",
        "solubilidad": "Disolución lenta en ciertos medios ácidos",
        "color": "#c2410c",
        "composicion": {
            "Hierro (Fe)": "69.9%",
            "Oxígeno (O)": "30.1%"
        }
    },
    {
        "nombre": "Magnetita",
        "formula": "Fe₃O₄",
        "grupo": "Otros",
        "elemento": "Fe",
        "ley": 72.4,
        "densidad": "5.15 - 5.18 g/cm³",
        "dureza": "5.5 - 6.5",
        "acido": "Variable",
        "solubilidad": "Insoluble en agua; disolución ácida dependiente del medio",
        "color": "#64748b",
        "composicion": {
            "Hierro (Fe)": "72.4%",
            "Oxígeno (O)": "27.6%"
        }
    }
]


# ============================================================
# ESTILOS DE LAS TARJETAS
# ============================================================

def cargar_estilos_minerales():

    st.markdown(
        """
<style>
.mineral-card {
    background: linear-gradient(145deg, #202938, #151c29);
    border: 1px solid #344155;
    border-top: 3px solid var(--mineral-color);
    border-radius: 14px;
    padding: 16px;
    min-height: 235px;
    box-sizing: border-box;
    color: #f8fafc;
    font-family: inherit;
}

.mineral-header {
    display: flex;
    align-items: center;
    gap: 9px;
    margin-bottom: 4px;
}

.mineral-dot {
    width: 13px;
    height: 13px;
    border-radius: 50%;
    background: var(--mineral-color);
    box-shadow: 0 0 10px var(--mineral-color);
    flex-shrink: 0;
}

.mineral-name {
    font-size: 1.05rem;
    font-weight: 700;
    color: #f8fafc;
}

.mineral-formula {
    color: #aebdd0;
    font-size: 0.83rem;
    min-height: 34px;
    margin: 4px 0 12px 22px;
}

.mineral-law-label {
    color: #94a3b8;
    font-size: 0.70rem;
    font-weight: 700;
    letter-spacing: 0.7px;
    text-transform: uppercase;
}

.mineral-law {
    color: var(--mineral-color);
    font-size: 2rem;
    font-weight: 800;
    line-height: 1.15;
    margin: 4px 0 12px;
}

.mineral-divider {
    border-top: 1px solid #354052;
    margin-bottom: 10px;
}

.mineral-property {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 8px;
    font-size: 0.78rem;
    margin-bottom: 7px;
}

.mineral-property-label {
    color: #94a3b8;
    flex-shrink: 0;
}

.mineral-property-value {
    color: #e2e8f0;
    text-align: right;
    overflow-wrap: anywhere;
}

.mineral-detail {
    margin-top: 12px;
    color: #94a3b8;
    font-size: 0.77rem;
    line-height: 1.4;
}

@media (max-width: 900px) {
    .mineral-card {
        min-height: auto;
    }
}
</style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# GENERACIÓN DE TARJETAS
# ============================================================

def generar_html_mineral(mineral):

    def seguro(valor):
        return html.escape(str(valor), quote=True)

    nombre = seguro(mineral["nombre"])
    formula = seguro(mineral["formula"])
    elemento = seguro(mineral["elemento"])
    densidad = seguro(mineral["densidad"])
    dureza = seguro(mineral["dureza"])
    acido = seguro(mineral["acido"])
    solubilidad = seguro(mineral["solubilidad"])
    color = mineral["color"]

    # Se construye en una sola línea para impedir
    # que Markdown lo interprete como bloque de código.
    tarjeta = (
        f'<div class="mineral-card" style="--mineral-color:{color};">'
        f'<div class="mineral-header">'
        f'<span class="mineral-dot"></span>'
        f'<span class="mineral-name">{nombre}</span>'
        f'</div>'
        f'<div class="mineral-formula">{formula}</div>'
        f'<div class="mineral-law-label">Ley teórica de {elemento}</div>'
        f'<div class="mineral-law">{mineral["ley"]:.1f}%</div>'
        f'<div class="mineral-divider"></div>'
        f'<div class="mineral-property">'
        f'<span class="mineral-property-label">Densidad</span>'
        f'<span class="mineral-property-value">{densidad}</span>'
        f'</div>'
        f'<div class="mineral-property">'
        f'<span class="mineral-property-label">Dureza Mohs</span>'
        f'<span class="mineral-property-value">{dureza}</span>'
        f'</div>'
        f'<div class="mineral-property">'
        f'<span class="mineral-property-label">Consumo ácido</span>'
        f'<span class="mineral-property-value">{acido}</span>'
        f'</div>'
        f'<div class="mineral-detail">{solubilidad}</div>'
        f'</div>'
    )

    return tarjeta


def mostrar_tarjeta_mineral(mineral):

    st.markdown(
        generar_html_mineral(mineral),
        unsafe_allow_html=True
    )

    # El desplegable se mantiene como control
    # nativo de Streamlit.
    with st.expander("📊 Composición elemental"):

        for elemento, porcentaje in mineral[
            "composicion"
        ].items():

            col1, col2 = st.columns([3, 2])

            with col1:
                st.write(elemento)

            with col2:
                st.write(porcentaje)


def mostrar_grupo_minerales(minerales):

    for inicio in range(0, len(minerales), 4):

        fila = minerales[inicio:inicio + 4]
        columnas = st.columns(4)

        for columna, mineral in zip(columnas, fila):

            with columna:
                mostrar_tarjeta_mineral(mineral)


# ============================================================
# 1. MINERALES OXIDADOS
# ============================================================

def mostrar_minerales():

    cargar_estilos_minerales()

    st.title("🟤 Minerales Oxidados")

    st.write(
        "Analiza las propiedades físicas, químicas, "
        "leyes teóricas y comportamientos metalúrgicos "
        "de las principales especies oxidadas "
        "y óxidos metálicos."
    )

    st.markdown("---")

    st.subheader("📚 Base de Propiedades")

    minerales_cobre = [
        mineral
        for mineral in MINERALES
        if mineral["grupo"] == "Cobre"
    ]

    otros_minerales = [
        mineral
        for mineral in MINERALES
        if mineral["grupo"] == "Otros"
    ]

    st.markdown("### 🟢 Minerales de Cobre")

    mostrar_grupo_minerales(minerales_cobre)

    st.markdown("---")

    st.markdown(
        "### 🟡 Otros Óxidos / Minerales Metálicos"
    )

    mostrar_grupo_minerales(otros_minerales)

    st.markdown("---")

    st.info(
        "Las leyes teóricas corresponden a la "
        "proporción másica del elemento de interés "
        "en una especie pura. No representan "
        "necesariamente la ley real del mineral "
        "de alimentación."
    )

    st.caption(
        "La composición de la crisocola es variable. "
        "Su ley de 36% se utiliza únicamente "
        "como valor referencial. Los consumos "
        "de ácido son cualitativos."
    )


# ============================================================
# 2. ESTIMADOR DE LEY DE CABEZA
# ============================================================

def mostrar_estimador_ley():

    st.title("🧮 Estimador de Ley de Cabeza")

    st.write(
        "Ingresa el porcentaje en masa de cada "
        "especie mineralógica para estimar "
        "la ley de cabeza de los elementos "
        "presentes en la muestra."
    )

    st.markdown("---")

    st.latex(
        r"L_{\mathrm{cabeza}} = "
        r"\frac{\sum_{i=1}^{n}(w_i \cdot L_i)}{100}"
    )

    st.caption(
        "wᵢ: porcentaje en masa de la especie mineralógica. "
        "Lᵢ: ley teórica del elemento en dicha especie (%)."
    )

    # --------------------------------------------------------
    # ENTRADA DE COMPOSICIÓN
    # --------------------------------------------------------

    porcentajes = {}

    for grupo, titulo in [
        ("Cobre", "🟢 Minerales de Cobre"),
        ("Otros", "🟡 Otros Óxidos / Minerales Metálicos")
    ]:

        st.markdown(f"### {titulo}")

        minerales_grupo = [
            mineral
            for mineral in MINERALES
            if mineral["grupo"] == grupo
        ]

        for inicio in range(0, len(minerales_grupo), 4):

            columnas = st.columns(4)

            fila = minerales_grupo[inicio:inicio + 4]

            for columna, mineral in zip(columnas, fila):

                with columna:

                    porcentaje = st.number_input(
                        f"% {mineral['nombre']}",
                        min_value=0.0,
                        max_value=100.0,
                        value=0.0,
                        step=0.1,
                        format="%.2f",
                        key=(
                            "caracterizacion_pct_"
                            + mineral["nombre"]
                        )
                    )

                    porcentajes[
                        mineral["nombre"]
                    ] = porcentaje

    # --------------------------------------------------------
    # VALIDACIÓN DE LA MUESTRA
    # --------------------------------------------------------

    suma_total = sum(porcentajes.values())

    porcentaje_ganga = max(
        100.0 - suma_total,
        0.0
    )

    st.markdown("---")

    st.markdown("### 📋 Composición de la Muestra")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Minerales Declarados",
        f"{suma_total:.2f}%"
    )

    c2.metric(
        "Ganga / Otros Minerales",
        f"{porcentaje_ganga:.2f}%"
    )

    c3.metric(
        "Total de la Muestra",
        f"{suma_total + porcentaje_ganga:.2f}%"
    )

    if suma_total > 100.000001:

        st.error(
            "La suma de los porcentajes mineralógicos "
            "supera el 100%. Revisa los datos ingresados."
        )

        return

    # --------------------------------------------------------
    # CÁLCULO DE LEYES DE CABEZA
    # --------------------------------------------------------

    leyes_cabeza = {
        "Cu": 0.0,
        "Au": 0.0,
        "Zn": 0.0,
        "Fe": 0.0
    }

    registros = []

    for mineral in MINERALES:

        porcentaje = porcentajes[
            mineral["nombre"]
        ]

        contribucion = (
            porcentaje
            * mineral["ley"]
            / 100.0
        )

        elemento = mineral["elemento"]

        leyes_cabeza[elemento] += contribucion

        if porcentaje > 0:

            registros.append({
                "Mineral": mineral["nombre"],
                "Elemento": elemento,
                "Proporción mineral [%]": porcentaje,
                "Ley teórica [%]": mineral["ley"],
                "Aporte a ley de cabeza [%]": contribucion
            })

    # --------------------------------------------------------
    # RESULTADOS
    # --------------------------------------------------------

    st.markdown("---")

    st.markdown("### 📊 Leyes de Cabeza Estimadas")

    r1, r2, r3, r4 = st.columns(4)

    r1.metric(
        "Cobre (Cu)",
        f"{leyes_cabeza['Cu']:.3f}%"
    )

    r2.metric(
        "Oro (Au)",
        f"{leyes_cabeza['Au']:.3f}%"
    )

    r3.metric(
        "Zinc (Zn)",
        f"{leyes_cabeza['Zn']:.3f}%"
    )

    r4.metric(
        "Hierro (Fe)",
        f"{leyes_cabeza['Fe']:.3f}%"
    )

    # --------------------------------------------------------
    # TABLA DE CONTRIBUCIONES
    # --------------------------------------------------------

    st.markdown("---")

    st.markdown("### 📑 Contribución Mineralógica")

    if registros:

        tabla = pd.DataFrame(registros)

        st.dataframe(
            tabla,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Proporción mineral [%]":
                    st.column_config.NumberColumn(
                        format="%.2f"
                    ),
                "Ley teórica [%]":
                    st.column_config.NumberColumn(
                        format="%.2f"
                    ),
                "Aporte a ley de cabeza [%]":
                    st.column_config.NumberColumn(
                        format="%.3f"
                    )
            }
        )

    else:

        st.info(
            "Ingresa porcentajes mineralógicos "
            "para visualizar las contribuciones."
        )

    # --------------------------------------------------------
    # INTERPRETACIÓN
    # --------------------------------------------------------

    st.markdown("---")

    st.markdown("### 🔎 Interpretación de Resultados")

    st.success(
        f"La ley de cabeza estimada de cobre "
        f"es {leyes_cabeza['Cu']:.3f}%, "
        f"considerando la composición ingresada."
    )

    st.caption(
        f"Los minerales no declarados y la ganga "
        f"representan {porcentaje_ganga:.2f}% "
        f"de la masa total."
    )

    st.warning(
        "Este cálculo es una estimación teórica. "
        "Se supone que la ganga no aporta los "
        "elementos evaluados. Para obtener leyes "
        "reales de cabeza se requiere análisis "
        "químico y caracterización mineralógica."
    )

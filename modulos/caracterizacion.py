
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
        "ley": 57.48,
        "densidad": "3,6 - 4,0 g/cm³",
        "dureza": "3,5 - 4,0",
        "acido": "887 kg H₂SO₄/t",
        "solubilidad": "",
        "color": "#22c55e",
        "composicion": {
            "Hidrógeno (H)": "0,91%",
            "Oxígeno (O)": "36,18%",
            "Carbono (C)": "5,43%",
            "Cobre (Cu)": "57,48%"
        }
    },
    {
        "nombre": "Azurita",
        "formula": "Cu₃(CO₃)₂(OH)₂",
        "grupo": "Cobre",
        "elemento": "Cu",
        "ley": 55.31,
        "densidad": "3,8 - 3,9 g/cm³",
        "dureza": "3,5 - 4,0",
        "acido": "854 kg H₂SO₄/t",
        "solubilidad": "",
        "color": "#3b82f6",
        "composicion": {
            "Hidrógeno (H)": "0,58%",
            "Oxígeno (O)": "37,14%",
            "Cobre (Cu)": "55,31%",
            "Carbono (C)": "6,97%"
        }
    },
    {
        "nombre": "Crisocola",
        "formula": "Cu₂₋ₓAlₓ(H₂₋ₓSi₂O₅)(OH)₄·nH₂O",
        "grupo": "Cobre",
        "elemento": "Cu",
        "ley": 24.17,
        "densidad": "1,93 - 2,4 g/cm³",
        "dureza": "2,5 - 3,5",
        "acido": "496 kg H₂SO₄/t",
        "solubilidad": "",
        "color": "#06b6d4",
        "composicion": {
            "Hidrógeno (H)": "1,26%",
            "Aluminio (Al)": "1,47%",
            "Cobre (Cu)": "24,17%",
            "Silicio (Si)": "24,42%",
            "Agua (H₂O)": "3,91%",
            "Oxígeno (O)": "48,69%"
        }
    },
    {
        "nombre": "Cuprita",
        "formula": "Cu₂O",
        "grupo": "Cobre",
        "elemento": "Cu",
        "ley": 88.82,
        "densidad": "6,14 - 6,15 g/cm³",
        "dureza": "3,5 - 4,0",
        "acido": "685 kg H₂SO₄/t",
        "solubilidad": "",
        "color": "#ef4444",
        "composicion": {
            "Oxígeno (O)": "11,18%",
            "Cobre (Cu)": "88,82%"
        }
    },
    {
        "nombre": "Tenorita",
        "formula": "CuO",
        "grupo": "Cobre",
        "elemento": "Cu",
        "ley": 79.89,
        "densidad": "6,5 g/cm³",
        "dureza": "3,0 - 4,0",
        "acido": "1233 kg H₂SO₄/t",
        "solubilidad": "",
        "color": "#94a3b8",
        "composicion": {
            "Oxígeno (O)": "20,11%",
            "Cobre (Cu)": "79,89%"
        }
    },
    {
        "nombre": "Atacamita",
        "formula": "Cu₂Cl(OH)₃",
        "grupo": "Cobre",
        "elemento": "Cu",
        "ley": 59.51,
        "densidad": "3,75 - 3,78 g/cm³",
        "dureza": "3,0 - 3,5",
        "acido": "689 kg H₂SO₄/t",
        "solubilidad": "",
        "color": "#16a34a",
        "composicion": {
            "Hidrógeno (H)": "1,42%",
            "Cloro (Cl)": "16,60%",
            "Oxígeno (O)": "22,47%",
            "Cobre (Cu)": "59,51%"
        }
    },
    {
        "nombre": "Brochantita",
        "formula": "Cu₄SO₄(OH)₆",
        "grupo": "Cobre",
        "elemento": "Cu",
        "ley": 56.20,
        "densidad": "4,0 - 4,41 g/cm³",
        "dureza": "3,5 - 4,0",
        "acido": "651 kg H₂SO₄/t",
        "solubilidad": "",
        "color": "#10b981",
        "composicion": {
            "Hidrógeno (H)": "1,34%",
            "Oxígeno (O)": "35,37%",
            "Cobre (Cu)": "56,20%",
            "Azufre (S)": "7,09%"
        }
    },
    {
        "nombre": "Calcantita",
        "formula": "CuSO₄·5H₂O",
        "grupo": "Cobre",
        "elemento": "Cu",
        "ley": 25.45,
        "densidad": "2,1 - 2,3 g/cm³",
        "dureza": "2,5",
        "acido": "0 kg H₂SO₄/t",
        "solubilidad": "",
        "color": "#0ea5e9",
        "composicion": {
            "Azufre (S)": "12,84%",
            "Cobre (Cu)": "25,45%",
            "Agua (H₂O)": "36,04%",
            "Hidrógeno (H)": "4,04%",
            "Oxígeno (O)": "57,67%"
        }
    },
    {
        "nombre": "Cincita",
        "formula": "ZnO",
        "grupo": "Otros",
        "elemento": "Zn",
        "ley": 73.25,
        "densidad": "5,4 - 5,7 g/cm³",
        "dureza": "4,0 - 4,5",
        "acido": "1205 kg H₂SO₄/t",
        "solubilidad": "",
        "color": "#a1a1aa",
        "composicion": {
            "Oxígeno (O)": "19,91%",
            "Manganeso (Mn)": "6,84%",
            "Zinc (Zn)": "73,25%"
        }
    },
    {
        "nombre": "Hematita",
        "formula": "Fe₂O₃",
        "grupo": "Otros",
        "elemento": "Fe",
        "ley": 69.94,
        "densidad": "5,2 - 5,3 g/cm³",
        "dureza": "5,5 - 6,5",
        "acido": "1843 kg H₂SO₄/t",
        "solubilidad": "",
        "color": "#c2410c",
        "composicion": {
            "Oxígeno (O)": "30,06%",
            "Hierro (Fe)": "69,94%"
        }
    },
    {
        "nombre": "Magnetita",
        "formula": "Fe₃O₄",
        "grupo": "Otros",
        "elemento": "Fe",
        "ley": 72.36,
        "densidad": "5,1 - 5,2 g/cm³",
        "dureza": "5,5 - 6,5",
        "acido": "1694 kg H₂SO₄/t",
        "solubilidad": "",
        "color": "#64748b",
        "composicion": {
            "Oxígeno (O)": "27,64%",
            "Hierro (Fe)": "72,36%"
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
    etiqueta_acido = (
        "Consumo teórico de H₂SO₄"
        if mineral["nombre"] in {"Malaquita", "Azurita", "Crisocola", "Cuprita", "Tenorita", "Atacamita", "Brochantita", "Calcantita", "Cincita", "Hematita", "Magnetita"}
        else "Consumo ácido"
    )
    color = mineral["color"]

    detalle_solubilidad = (
        f'<div class="mineral-detail">{solubilidad}</div>'
        if solubilidad else ''
    )

    ley_formateada = f'{mineral["ley"]:.2f}%'

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
        f'<div class="mineral-law">{ley_formateada}</div>'
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
        f'<span class="mineral-property-label">{etiqueta_acido}</span>'
        f'<span class="mineral-property-value">{acido}</span>'
        f'</div>'
        f'{detalle_solubilidad}'
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
        "Las composiciones indicadas para la cincita corresponden a los datos "
        "de la tesis y no a la composición estequiométrica del ZnO puro. "
        "La composición real de la crisocola puede variar; "
        "el valor de 24,17% de Cu corresponde a la composición "
        "idealizada indicada en la tesis. Los consumos de ácido "
        "indicados para malaquita, azurita, crisocola y cuprita "
        "son valores teóricos, no consumos operacionales medidos."
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

    r1, r2, r3 = st.columns(3)

    r1.metric(
        "Cobre (Cu)",
        f"{leyes_cabeza['Cu']:.3f}%"
    )

    r2.metric(
        "Zinc (Zn)",
        f"{leyes_cabeza['Zn']:.3f}%"
    )

    r3.metric(
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

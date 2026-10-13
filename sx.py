
import streamlit as st
import pandas as pd


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def tarjeta_resultado(titulo, valor, unidad, color):
    """Genera una tarjeta de resultados de SX."""

    return f"""
    <div style="
        background-color: #1e222d;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid {color};
        text-align: center;
        margin-bottom: 12px;
        overflow-wrap: anywhere;
    ">
        <p style="
            color: #a1aab5;
            margin: 0;
            font-size: 0.95rem;
        ">
            {titulo}
        </p>

        <h2 style="
            color: white;
            margin: 8px 0;
        ">
            {valor}
        </h2>

        <p style="
            color: {color};
            margin: 0;
            font-weight: bold;
        ">
            {unidad}
        </p>
    </div>
    """


def flujo_cobre(q_m3_h, concentracion_g_l):
    """
    Calcula flujo de cobre en t/h.

    m³/h * g/L = kg/h
    t/h = kg/h / 1000
    """
    return q_m3_h * concentracion_g_l / 1000.0


def balance_extraccion(
    q_pls,
    cu_pls,
    q_org,
    cu_org_desc,
    cu_refino
):
    """Balance simplificado de extracción de cobre."""

    cobre_pls = flujo_cobre(q_pls, cu_pls)

    cobre_refino = flujo_cobre(q_pls, cu_refino)

    cobre_transferido = cobre_pls - cobre_refino

    cu_org_cargado = (
        cu_org_desc
        + (q_pls / q_org) * (cu_pls - cu_refino)
    )

    recuperacion = (
        cobre_transferido / cobre_pls * 100.0
        if cobre_pls > 0 else 0.0
    )

    return {
        "cobre_pls": cobre_pls,
        "cobre_refino": cobre_refino,
        "cobre_transferido": cobre_transferido,
        "cu_org_cargado": cu_org_cargado,
        "recuperacion": recuperacion,
        "cierre": (
            cobre_pls
            + flujo_cobre(q_org, cu_org_desc)
            - cobre_refino
            - flujo_cobre(q_org, cu_org_cargado)
        )
    }


def balance_reextraccion(
    q_org,
    cu_org_cargado,
    cu_org_descargado,
    q_electrolito,
    cu_electrolito_pobre
):
    """Balance simplificado de reextracción."""

    cobre_transferido = flujo_cobre(
        q_org,
        cu_org_cargado - cu_org_descargado
    )

    cu_electrolito_rico = (
        cu_electrolito_pobre
        + (q_org / q_electrolito)
        * (cu_org_cargado - cu_org_descargado)
    )

    eficiencia = (
        (cu_org_cargado - cu_org_descargado)
        / cu_org_cargado * 100.0
        if cu_org_cargado > 0 else 0.0
    )

    cierre = (
        flujo_cobre(q_org, cu_org_cargado)
        + flujo_cobre(q_electrolito, cu_electrolito_pobre)
        - flujo_cobre(q_org, cu_org_descargado)
        - flujo_cobre(q_electrolito, cu_electrolito_rico)
    )

    return {
        "cobre_transferido": cobre_transferido,
        "cu_electrolito_rico": cu_electrolito_rico,
        "eficiencia": eficiencia,
        "cierre": cierre
    }


def mostrar_cierre(error):
    """Comprueba el cierre numérico del balance."""

    if abs(error) < 1e-8:
        st.success("Balance de cobre cerrado correctamente.")
    else:
        st.error(
            f"El balance presenta una diferencia "
            f"de {error:.8f} t/h."
        )


# ============================================================
# MÓDULO PRINCIPAL SX
# ============================================================

def mostrar_sx():

    st.title("🧲 Extracción por Solventes (SX)")

    st.write(
        "Selecciona la etapa específica del circuito "
        "de extracción por solventes para realizar "
        "balances y cálculos operacionales."
    )

    sub_sx = st.radio(
        "Selecciona el sub-módulo de SX:",
        [
            "Extracción",
            "Re-extracción",
            "Circuito Completo"
        ],
        horizontal=True
    )

    st.markdown("---")

    # ========================================================
    # 1. EXTRACCIÓN
    # ========================================================

    if sub_sx == "Extracción":

        st.subheader("💧 Módulo de Extracción (Extraction)")

        st.write(
            "Calcula la transferencia de cobre desde "
            "la solución rica (PLS) hacia la fase "
            "orgánica mediante un reactivo extractante."
        )

        st.latex(
            r"Cu^{2+}_{(ac)} + 2RH_{(org)}"
            r"\rightleftharpoons"
            r"CuR_{2(org)} + 2H^+_{(ac)}"
        )

        st.markdown("### 📥 Parámetros de Operación")

        col1, col2 = st.columns(2)

        with col1:

            pls_flow = st.number_input(
                "Caudal de PLS [m³/h]",
                min_value=0.1,
                value=500.0,
                step=10.0,
                format="%.2f",
                key="sx_ex_q_pls"
            )

            cu_pls = st.number_input(
                "Concentración Cu en PLS [g/L]",
                min_value=0.01,
                value=4.50,
                step=0.1,
                format="%.2f",
                key="sx_ex_cu_pls"
            )

            cu_raff = st.number_input(
                "Concentración Cu en Refino [g/L]",
                min_value=0.0,
                value=0.15,
                step=0.01,
                format="%.2f",
                key="sx_ex_cu_refino"
            )

        with col2:

            org_flow = st.number_input(
                "Caudal de Orgánico [m³/h]",
                min_value=0.1,
                value=400.0,
                step=10.0,
                format="%.2f",
                key="sx_ex_q_org"
            )

            cu_org_desc = st.number_input(
                "Cu en Orgánico Descargado [g/L]",
                min_value=0.0,
                value=0.50,
                step=0.1,
                format="%.2f",
                key="sx_ex_cu_org_desc"
            )

        if cu_raff > cu_pls:

            st.error(
                "La concentración de cobre del refino "
                "no puede superar la del PLS en este "
                "modelo de extracción."
            )
            return

        resultados = balance_extraccion(
            pls_flow,
            cu_pls,
            org_flow,
            cu_org_desc,
            cu_raff
        )

        st.markdown("---")
        st.markdown("### 📊 Resultados de Extracción")

        r1, r2 = st.columns(2)

        with r1:
            st.markdown(
                tarjeta_resultado(
                    "Cobre en Orgánico Cargado",
                    f"{resultados['cu_org_cargado']:.2f}",
                    "g/L",
                    "#3b82f6"
                ),
                unsafe_allow_html=True
            )

        with r2:
            st.markdown(
                tarjeta_resultado(
                    "Recuperación de Extracción",
                    f"{resultados['recuperacion']:.2f}",
                    "%",
                    "#10b981"
                ),
                unsafe_allow_html=True
            )

        r3, r4 = st.columns(2)

        r3.metric(
            "Cobre Transferido",
            f"{resultados['cobre_transferido']:.3f} t/h"
        )

        r4.metric(
            "Relación O/A",
            f"{org_flow / pls_flow:.2f}"
        )

        st.markdown("### 📋 Balance de Cobre")

        tabla = pd.DataFrame({
            "Corriente": [
                "PLS",
                "Orgánico descargado",
                "Refino",
                "Orgánico cargado"
            ],
            "Tipo": [
                "Entrada",
                "Entrada",
                "Salida",
                "Salida"
            ],
            "Cu [t/h]": [
                resultados["cobre_pls"],
                flujo_cobre(org_flow, cu_org_desc),
                resultados["cobre_refino"],
                flujo_cobre(
                    org_flow,
                    resultados["cu_org_cargado"]
                )
            ]
        })

        st.dataframe(
            tabla,
            hide_index=True,
            use_container_width=True
        )

        mostrar_cierre(resultados["cierre"])

        st.caption(
            "Se supone que los caudales volumétricos "
            "de cada fase permanecen constantes y "
            "que no existen pérdidas ni arrastres. "
            "La concentración del orgánico cargado "
            "se obtiene mediante balance de masa; "
            "no se verifica su capacidad máxima "
            "de carga ni el equilibrio químico."
        )

    # ========================================================
    # 2. REEXTRACCIÓN
    # ========================================================

    elif sub_sx == "Re-extracción":

        st.subheader(
            "🔄 Módulo de Re-extracción (Stripping)"
        )

        st.write(
            "Calcula la transferencia de cobre desde "
            "el orgánico cargado hacia el electrolito "
            "pobre mediante una solución ácida."
        )

        st.latex(
            r"CuR_{2(org)} + 2H^+_{(ac)}"
            r"\rightleftharpoons"
            r"Cu^{2+}_{(ac)} + 2RH_{(org)}"
        )

        st.markdown("### 📥 Parámetros de Operación")

        col1, col2 = st.columns(2)

        with col1:

            org_cargado_flow = st.number_input(
                "Caudal de Orgánico Cargado [m³/h]",
                min_value=0.1,
                value=400.0,
                step=10.0,
                format="%.2f",
                key="sx_re_q_org"
            )

            cu_org_cargado = st.number_input(
                "Cu en Orgánico Cargado [g/L]",
                min_value=0.01,
                value=5.80,
                step=0.1,
                format="%.2f",
                key="sx_re_cu_org_cargado"
            )

            cu_org_descargado = st.number_input(
                "Cu en Orgánico Descargado [g/L]",
                min_value=0.0,
                value=0.50,
                step=0.1,
                format="%.2f",
                key="sx_re_cu_org_desc"
            )

        with col2:

            electrolito_pobre_flow = st.number_input(
                "Caudal de Electrolito Pobre [m³/h]",
                min_value=0.1,
                value=100.0,
                step=5.0,
                format="%.2f",
                key="sx_re_q_ep"
            )

            cu_electrolito_pobre = st.number_input(
                "Cu en Electrolito Pobre [g/L]",
                min_value=0.0,
                value=35.0,
                step=1.0,
                format="%.2f",
                key="sx_re_cu_ep"
            )

        if cu_org_descargado > cu_org_cargado:

            st.error(
                "La concentración de cobre del "
                "orgánico descargado no puede "
                "superar la del orgánico cargado."
            )
            return

        resultados = balance_reextraccion(
            org_cargado_flow,
            cu_org_cargado,
            cu_org_descargado,
            electrolito_pobre_flow,
            cu_electrolito_pobre
        )

        st.markdown("---")
        st.markdown("### 📊 Resultados de Re-extracción")

        r1, r2 = st.columns(2)

        with r1:
            st.markdown(
                tarjeta_resultado(
                    "Cu en Electrolito Rico (ELR)",
                    f"{resultados['cu_electrolito_rico']:.2f}",
                    "g/L",
                    "#f59e0b"
                ),
                unsafe_allow_html=True
            )

        with r2:
            st.markdown(
                tarjeta_resultado(
                    "Relación de Caudales O/A",
                    f"{org_cargado_flow / electrolito_pobre_flow:.2f}",
                    "Adimensional",
                    "#a855f7"
                ),
                unsafe_allow_html=True
            )

        r3, r4 = st.columns(2)

        r3.metric(
            "Cobre Transferido al Electrolito",
            f"{resultados['cobre_transferido']:.3f} t/h"
        )

        r4.metric(
            "Reextracción de Cu del Orgánico",
            f"{resultados['eficiencia']:.2f}%"
        )

        st.markdown("### 📋 Balance de Cobre")

        tabla = pd.DataFrame({
            "Corriente": [
                "Orgánico cargado",
                "Electrolito pobre",
                "Orgánico descargado",
                "Electrolito rico"
            ],
            "Tipo": [
                "Entrada",
                "Entrada",
                "Salida",
                "Salida"
            ],
            "Cu [t/h]": [
                flujo_cobre(
                    org_cargado_flow,
                    cu_org_cargado
                ),
                flujo_cobre(
                    electrolito_pobre_flow,
                    cu_electrolito_pobre
                ),
                flujo_cobre(
                    org_cargado_flow,
                    cu_org_descargado
                ),
                flujo_cobre(
                    electrolito_pobre_flow,
                    resultados["cu_electrolito_rico"]
                )
            ]
        })

        st.dataframe(
            tabla,
            hide_index=True,
            use_container_width=True
        )

        mostrar_cierre(resultados["cierre"])

        st.caption(
            "El modelo supone caudales constantes "
            "y ausencia de pérdidas. La concentración "
            "del electrolito rico se calcula por "
            "balance de cobre y no mediante "
            "equilibrio de reextracción."
        )

    # ========================================================
    # 3. CIRCUITO COMPLETO
    # ========================================================

    else:

        st.subheader(
            "🌐 Balance General del Circuito Completo de SX"
        )

        st.write(
            "Simulación integrada de extracción "
            "y reextracción para estimar la "
            "transferencia global de cobre."
        )

        st.markdown("### 📥 Alimentación y Extracción")

        col1, col2 = st.columns(2)

        with col1:

            q_pls = st.number_input(
                "Caudal de PLS Total [m³/h]",
                min_value=0.1,
                value=500.0,
                step=10.0,
                format="%.2f",
                key="sx_c_q_pls"
            )

            cu_pls = st.number_input(
                "Concentración Cu en PLS [g/L]",
                min_value=0.01,
                value=4.50,
                step=0.1,
                format="%.2f",
                key="sx_c_cu_pls"
            )

            recuperacion_ex = st.slider(
                "Recuperación de Extracción [%]",
                min_value=0.0,
                max_value=100.0,
                value=95.0,
                step=0.5,
                key="sx_c_rec_ex"
            )

        with col2:

            q_org = st.number_input(
                "Caudal de Orgánico Total [m³/h]",
                min_value=0.1,
                value=400.0,
                step=10.0,
                format="%.2f",
                key="sx_c_q_org"
            )

            cu_org_desc = st.number_input(
                "Cu en Orgánico Descargado [g/L]",
                min_value=0.0,
                value=0.50,
                step=0.1,
                format="%.2f",
                key="sx_c_cu_org_desc"
            )

        # ----------------------------------------------------
        # CÁLCULOS DE EXTRACCIÓN
        # ----------------------------------------------------

        cu_refino = (
            cu_pls * (1.0 - recuperacion_ex / 100.0)
        )

        extraccion = balance_extraccion(
            q_pls,
            cu_pls,
            q_org,
            cu_org_desc,
            cu_refino
        )

        cu_org_cargado = extraccion["cu_org_cargado"]

        st.markdown("---")
        st.markdown("### 🔄 Parámetros de Re-extracción")

        col3, col4 = st.columns(2)

        with col3:

            q_electrolito = st.number_input(
                "Caudal de Electrolito Pobre [m³/h]",
                min_value=0.1,
                value=100.0,
                step=5.0,
                format="%.2f",
                key="sx_c_q_ep"
            )

            cu_electrolito_pobre = st.number_input(
                "Cu en Electrolito Pobre [g/L]",
                min_value=0.0,
                value=35.0,
                step=1.0,
                format="%.2f",
                key="sx_c_cu_ep"
            )

        with col4:

            recuperacion_re = st.slider(
                "Reextracción de Cu del Orgánico [%]",
                min_value=0.0,
                max_value=100.0,
                value=90.0,
                step=0.5,
                key="sx_c_rec_re"
            )

        # ----------------------------------------------------
        # CÁLCULOS DE REEXTRACCIÓN
        # ----------------------------------------------------

        cu_org_salida_re = (
            cu_org_cargado
            * (1.0 - recuperacion_re / 100.0)
        )

        reextraccion = balance_reextraccion(
            q_org,
            cu_org_cargado,
            cu_org_salida_re,
            q_electrolito,
            cu_electrolito_pobre
        )

        # ----------------------------------------------------
        # BALANCE GLOBAL
        # ----------------------------------------------------

        cobre_pls = extraccion["cobre_pls"]

        cobre_extraido = extraccion["cobre_transferido"]

        cobre_reextraido = reextraccion["cobre_transferido"]

        recuperacion_global = (
            cobre_reextraido / cobre_pls * 100.0
            if cobre_pls > 0 else 0.0
        )

        st.markdown("---")
        st.markdown("### 📋 Resumen Global del Proceso SX")

        r1, r2, r3 = st.columns(3)

        r1.metric(
            "Caudal PLS",
            f"{q_pls:.2f} m³/h"
        )

        r2.metric(
            "Caudal Orgánico",
            f"{q_org:.2f} m³/h"
        )

        r3.metric(
            "Cobre Transferido al Electrolito",
            f"{cobre_reextraido:.3f} t/h"
        )

        r4, r5, r6 = st.columns(3)

        r4.metric(
            "Cu en Refino",
            f"{cu_refino:.2f} g/L"
        )

        r5.metric(
            "Cu en Orgánico Cargado",
            f"{cu_org_cargado:.2f} g/L"
        )

        r6.metric(
            "Cu en Electrolito Rico",
            f"{reextraccion['cu_electrolito_rico']:.2f} g/L"
        )

        st.markdown("### 📊 Recuperación Global")

        st.markdown(
            tarjeta_resultado(
                "Transferencia Global Estimada de Cu",
                f"{recuperacion_global:.2f}",
                "% respecto al cobre del PLS",
                "#10b981"
            ),
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # COMPROBACIÓN DE CONTINUIDAD DEL ORGÁNICO
        # ----------------------------------------------------

        diferencia_org = (
            cu_org_salida_re - cu_org_desc
        )

        if abs(diferencia_org) > 1e-6:

            st.warning(
                "El orgánico descargado calculado "
                "en reextracción no coincide con "
                "el orgánico de entrada a extracción. "
                "Por lo tanto, los parámetros ingresados "
                "no representan un circuito cerrado "
                "en estado estacionario."
            )

            st.write(
                f"Cu en orgánico de entrada a extracción: "
                f"{cu_org_desc:.3f} g/L"
            )

            st.write(
                f"Cu en orgánico después de reextracción: "
                f"{cu_org_salida_re:.3f} g/L"
            )

        else:

            st.success(
                "La concentración del orgánico "
                "es consistente entre ambas etapas."
            )

        st.markdown("### 📋 Resumen de Corrientes")

        tabla = pd.DataFrame({
            "Corriente": [
                "PLS",
                "Refino",
                "Orgánico descargado inicial",
                "Orgánico cargado",
                "Orgánico después de reextracción",
                "Electrolito pobre",
                "Electrolito rico"
            ],
            "Caudal [m³/h]": [
                q_pls,
                q_pls,
                q_org,
                q_org,
                q_org,
                q_electrolito,
                q_electrolito
            ],
            "Cu [g/L]": [
                cu_pls,
                cu_refino,
                cu_org_desc,
                cu_org_cargado,
                cu_org_salida_re,
                cu_electrolito_pobre,
                reextraccion["cu_electrolito_rico"]
            ]
        })

        st.dataframe(
            tabla,
            hide_index=True,
            use_container_width=True
        )

        mostrar_cierre(extraccion["cierre"])
        mostrar_cierre(reextraccion["cierre"])

        st.caption(
            "Los balances individuales cierran por "
            "construcción matemática. Esto no garantiza "
            "que el circuito sea físicamente viable. "
            "La recuperación global mostrada corresponde "
            "a la transferencia de cobre al electrolito "
            "respecto de la alimentación de PLS; "
            "no representa producción de cátodos."
        )


import streamlit as st
from html import escape


# ============================================================
# FUNCIONES AUXILIARES DE DISEÑO
# ============================================================

def tarjeta_proceso(titulo, descripcion):
    """
    Genera las tarjetas de las etapas del proceso metalúrgico.
    """

    titulo = escape(str(titulo))
    descripcion = escape(str(descripcion))

    html_etapa = (
        '<div style="'
        'background-color:#1e222d;'
        'border:2px solid #64748b;'
        'color:#ffffff;'
        'padding:18px;'
        'border-radius:12px;'
        'text-align:center;'
        'font-weight:700;'
        'min-height:85px;'
        'display:flex;'
        'align-items:center;'
        'justify-content:center;'
        'box-sizing:border-box;'
        '">'
        f'{titulo}'
        '</div>'
    )

    html_descripcion = (
        '<div style="'
        'background-color:#1e222d;'
        'border:1px solid #475569;'
        'color:#cbd5e1;'
        'padding:18px;'
        'border-radius:12px;'
        'font-size:0.95rem;'
        'line-height:1.5;'
        'min-height:85px;'
        'display:flex;'
        'align-items:center;'
        'box-sizing:border-box;'
        '">'
        f'{descripcion}'
        '</div>'
    )

    return html_etapa, html_descripcion


def tarjeta_modulo(emoji, titulo, descripcion, color):
    """
    Genera las tarjetas informativas de los módulos.
    """

    emoji = escape(str(emoji))
    titulo = escape(str(titulo))
    descripcion = escape(str(descripcion))

    return (
        '<div style="'
        'background:linear-gradient(145deg,#202938,#171d29);'
        f'border-top:3px solid {color};'
        'border-radius:16px;'
        'padding:28px 18px;'
        'text-align:center;'
        'min-height:215px;'
        'box-sizing:border-box;'
        'box-shadow:0 5px 18px rgba(0,0,0,0.20);'
        '">'
        '<div style="'
        'font-size:3.3rem;'
        'margin-bottom:16px;'
        '">'
        f'{emoji}'
        '</div>'
        '<div style="'
        'font-size:1.12rem;'
        'font-weight:800;'
        'color:#ffffff;'
        'margin-bottom:12px;'
        '">'
        f'{titulo}'
        '</div>'
        '<div style="'
        'font-size:0.92rem;'
        'color:#aebdd0;'
        'line-height:1.5;'
        '">'
        f'{descripcion}'
        '</div>'
        '</div>'
    )


def tarjeta_integrante(nombre, color):
    """
    Genera una tarjeta de presentación para cada integrante.
    """

    nombre = escape(str(nombre))

    return (
        '<div style="'
        'background:linear-gradient(145deg,#202938,#171d29);'
        'padding:32px 24px;'
        'border-radius:18px;'
        'text-align:center;'
        'border:1px solid #334155;'
        f'border-bottom:4px solid {color};'
        'box-shadow:0 8px 20px rgba(0,0,0,0.20);'
        'min-height:270px;'
        'box-sizing:border-box;'
        '">'
        '<div style="'
        'width:90px;'
        'height:90px;'
        'border-radius:50%;'
        f'background-color:{color};'
        'margin:0 auto 20px auto;'
        'display:flex;'
        'align-items:center;'
        'justify-content:center;'
        'font-size:2.7rem;'
        '">'
        '👨‍🎓'
        '</div>'
        '<div style="'
        'font-size:1.5rem;'
        'font-weight:800;'
        'color:#ffffff;'
        'margin-bottom:10px;'
        '">'
        f'{nombre}'
        '</div>'
        '<div style="'
        f'color:{color};'
        'font-size:1rem;'
        'font-weight:700;'
        'margin-bottom:10px;'
        '">'
        'Estudiante de Ingeniería en Metalurgia'
        '</div>'
        '<div style="'
        'color:#cbd5e1;'
        'font-size:0.95rem;'
        '">'
        'INACAP · Sede Maipú'
        '</div>'
        '</div>'
    )


# ============================================================
# PÁGINA DE INICIO
# ============================================================

def mostrar_inicio():

    st.title(
        "Bienvenido a tu plataforma de Minerales Oxidados"
    )

    st.write(
        "Una herramienta diseñada para la caracterización, "
        "análisis y cálculo de procesos metalúrgicos "
        "de minerales oxidados. Diseñada para potenciar "
        "el desarrollo, cálculo y control de tus proyectos."
    )

    # --------------------------------------------------------
    # MENSAJE INFORMATIVO
    # MODIFICACIÓN 1
    # --------------------------------------------------------

    st.info(
        "Utiliza el menú de navegación para acceder a "
        "los módulos interactivos de cálculo y demás "
        "herramientas de cálculo.",
        icon="👈"
    )

    st.markdown("---")

    # --------------------------------------------------------
    # INTRODUCCIÓN A LOS MINERALES OXIDADOS
    # --------------------------------------------------------

    st.markdown("### 💡 ¿Qué son los minerales oxidados?")

    st.write(
        "Los minerales oxidados son especies mineralógicas "
        "que contienen metales asociados principalmente "
        "a oxígeno u otros grupos químicos, como carbonatos, "
        "hidróxidos y sulfatos. En el caso del cobre, "
        "muchas de estas especies pueden procesarse "
        "mediante métodos hidrometalúrgicos."
    )

    st.markdown("---")

    # --------------------------------------------------------
    # DIAGRAMA DEL PROCESO METALÚRGICO
    # --------------------------------------------------------

    st.markdown(
        "### ⚙️ Diagrama del Proceso Metalúrgico "
        "de Minerales Oxidados"
    )

    pasos_proceso = [
        (
            "1. EXTRACCIÓN MINERA",
            "Extracción del mineral desde la mina a cielo "
            "abierto o subterránea para su posterior "
            "procesamiento metalúrgico."
        ),
        (
            "2. CONMINUCIÓN (CHANCADO)",
            "Reducción progresiva del tamaño de roca "
            "mediante etapas de chancado, preparando "
            "el mineral para las operaciones posteriores."
        ),
        (
            "3. AGLOMERACIÓN",
            "Mezcla del mineral con agua y, cuando "
            "corresponde, ácido sulfúrico para formar "
            "aglomerados y favorecer la permeabilidad "
            "del lecho mineral."
        ),
        (
            "4. LIXIVIACIÓN",
            "Disolución de los metales valiosos "
            "contenidos en el mineral mediante "
            "soluciones acuosas, generalmente ácidas "
            "para minerales oxidados de cobre."
        ),
        (
            "5. EXTRACCIÓN POR SOLVENTES",
            "Purificación y concentración del cobre "
            "contenido en la solución rica (PLS) "
            "mediante una fase orgánica extractante."
        ),
        (
            "6. ELECTROOBTENCIÓN",
            "Proceso electroquímico en el cual se "
            "aplica corriente eléctrica para depositar "
            "el cobre disuelto sobre los cátodos."
        ),
        (
            "7. CÁTODO",
            "Producto final de cobre de alta pureza "
            "obtenido mediante electroobtención, "
            "destinado a su comercialización."
        )
    ]

    for titulo, descripcion in pasos_proceso:

        col_etapa, col_flecha, col_descripcion = st.columns(
            [2.5, 0.4, 4.5],
            vertical_alignment="center"
        )

        html_etapa, html_descripcion = tarjeta_proceso(
            titulo,
            descripcion
        )

        with col_etapa:
            st.markdown(
                html_etapa,
                unsafe_allow_html=True
            )

        with col_flecha:
            st.markdown("### ➜")

        with col_descripcion:
            st.markdown(
                html_descripcion,
                unsafe_allow_html=True
            )

        st.write("")

    st.markdown("---")

    # --------------------------------------------------------
    # MÓDULOS DE LA PLATAFORMA
    # --------------------------------------------------------

    st.markdown("### 📚 Módulos de la Plataforma")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            tarjeta_modulo(
                "🔬",
                "CARACTERIZACIÓN",
                "MINERALES OXIDADOS.",
                "#38bdf8"
            ),
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            tarjeta_modulo(
                "⛰️",
                "CONMINUCIÓN",
                "REDUCCIÓN DE TAMAÑO DEL MINERAL.",
                "#94a3b8"
            ),
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            tarjeta_modulo(
                "🧪",
                "HIDROMETALURGIA",
                "AGLOMERACIÓN, LIXIVIACIÓN, SX Y EW.",
                "#22c55e"
            ),
            unsafe_allow_html=True
        )


# ============================================================
# PÁGINA QUIÉNES SOMOS
# ============================================================

def mostrar_quienes_somos():

    st.title("👥 Quiénes Somos")

    # --------------------------------------------------------
    # PRESENTACIÓN
    # --------------------------------------------------------

    st.write(
        "Somos estudiantes de la carrera de "
        "**Ingeniería en Metalurgia de INACAP, sede Maipú**, "
        "y estamos desarrollando esta plataforma digital "
        "como parte de nuestro proyecto de título."
    )

    # --------------------------------------------------------
    # DESCRIPCIÓN DEL PROYECTO
    # MODIFICACIÓN 2
    # --------------------------------------------------------

    st.write(
        "Nuestro proyecto está enfocado en el desarrollo "
        "de herramientas tecnológicas que permitan "
        "facilitar el análisis, cálculo y evaluación "
        "de procesos metalúrgicos, orientados "
        "al tratamiento de minerales oxidados."
    )

    st.markdown("---")

    # --------------------------------------------------------
    # AUTORES DEL PROYECTO
    # --------------------------------------------------------

    st.markdown("### 🎓 Autores del Proyecto de Título")

    st.write(
        "Esta plataforma digital forma parte de nuestro "
        "proyecto de título en Ingeniería en Metalurgia, "
        "desarrollado en INACAP, sede Maipú, "
        "con el propósito de integrar conocimientos "
        "metalúrgicos y herramientas de programación "
        "en una plataforma de apoyo al cálculo "
        "de procesos."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            tarjeta_integrante(
                "Héctor Díaz",
                "#3b82f6"
            ),
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            tarjeta_integrante(
                "Nicolás Pérez",
                "#10b981"
            ),
            unsafe_allow_html=True
        )

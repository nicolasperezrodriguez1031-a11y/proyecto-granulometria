
import time
import streamlit as st

from google import genai
from google.genai import types


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

MODELOS_GEMINI = [
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite"
]

MAX_INTENTOS = 3
ESPERAS = [2, 5]

INSTRUCCIONES_SISTEMA = """
Eres un asistente especializado en ingeniería metalúrgica,
con énfasis en el procesamiento hidrometalúrgico de
minerales oxidados de cobre.

Tu función es apoyar al usuario en los siguientes temas:

1. Caracterización mineralógica.
2. Conminución y análisis granulométrico.
3. Aglomeración y lixiviación.
4. Extracción por solventes (SX).
5. Electroobtención (EW).
6. Balances de masa y cálculos metalúrgicos.

Responde principalmente en español.

Utiliza terminología técnica metalúrgica y explica
los conceptos de manera clara.

Cuando el usuario solicite cálculos:
- Identifica los datos y sus unidades.
- Explica las fórmulas correspondientes.
- Muestra el procedimiento.
- Diferencia resultados teóricos de datos experimentales.
- Indica los supuestos y las limitaciones.

No inventes resultados experimentales ni condiciones
de operación que no hayan sido proporcionadas.

No afirmes que has realizado cálculos con los módulos
de la plataforma ni que has leído sus resultados,
a menos que esos datos se hayan compartido expresamente.

Cuando corresponda, recomienda validar los resultados
mediante ensayos de laboratorio y criterios de ingeniería.
"""


# ============================================================
# OBTENER CLAVE API
# ============================================================

def obtener_api_key():

    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        return ""

    if not isinstance(api_key, str):
        return ""

    return api_key.strip()


# ============================================================
# PREPARAR HISTORIAL
# ============================================================

def preparar_historial(mensajes):

    historial = []

    for mensaje in mensajes:

        rol = mensaje.get("role")
        contenido = mensaje.get("content", "")

        if not contenido:
            continue

        if rol == "user":
            rol_gemini = "user"

        elif rol == "assistant":
            rol_gemini = "model"

        else:
            continue

        historial.append(
            types.Content(
                role=rol_gemini,
                parts=[
                    types.Part.from_text(
                        text=str(contenido)
                    )
                ]
            )
        )

    return historial


# ============================================================
# IDENTIFICAR ERRORES DE LA API
# ============================================================

def obtener_codigo_error(error):

    codigo = getattr(error, "code", None)

    if codigo is not None:

        try:
            return int(codigo)
        except (TypeError, ValueError):
            pass

    mensaje = str(error).upper()

    if "503" in mensaje or "UNAVAILABLE" in mensaje:
        return 503

    if "429" in mensaje or "RESOURCE_EXHAUSTED" in mensaje:
        return 429

    if "404" in mensaje or "NOT_FOUND" in mensaje:
        return 404

    if "403" in mensaje or "PERMISSION_DENIED" in mensaje:
        return 403

    if "401" in mensaje:
        return 401

    return None


# ============================================================
# CONSULTAR UN MODELO
# ============================================================

def consultar_modelo(
    cliente,
    modelo,
    historial,
    pregunta
):

    chat = cliente.chats.create(
        model=modelo,
        history=historial,
        config=types.GenerateContentConfig(
            system_instruction=INSTRUCCIONES_SISTEMA,
            temperature=0.3
        )
    )

    respuesta = chat.send_message(pregunta)

    if not respuesta.text:
        raise ValueError(
            "Gemini no devolvió una respuesta de texto."
        )

    return respuesta.text


# ============================================================
# GENERAR RESPUESTA CON MODELOS ALTERNATIVOS
# ============================================================

def generar_respuesta(
    api_key,
    mensajes,
    pregunta,
    indicador=None
):

    cliente = genai.Client(api_key=api_key)

    try:

        historial = preparar_historial(mensajes)

        ultimo_error = None

        errores_modelos = []

        for indice_modelo, modelo in enumerate(MODELOS_GEMINI):

            for intento in range(MAX_INTENTOS):

                if indicador is not None:

                    if indice_modelo == 0:
                        estado = (
                            f"Consultando Gemini ({modelo})..."
                        )

                    else:
                        estado = (
                            f"Probando modelo alternativo "
                            f"({modelo})..."
                        )

                    if intento > 0:
                        estado += (
                            f" Intento {intento + 1} "
                            f"de {MAX_INTENTOS}."
                        )

                    indicador.info(estado)

                try:

                    respuesta = consultar_modelo(
                        cliente=cliente,
                        modelo=modelo,
                        historial=historial,
                        pregunta=pregunta
                    )

                    return respuesta, modelo

                except Exception as error:

                    ultimo_error = error
                    codigo = obtener_codigo_error(error)

                    if codigo == 404:

                        errores_modelos.append(
                            f"{modelo}: no disponible (404)"
                        )

                        # Pasar inmediatamente al
                        # siguiente modelo.
                        break

                    if codigo == 503:

                        if intento < MAX_INTENTOS - 1:

                            espera = ESPERAS[
                                min(
                                    intento,
                                    len(ESPERAS) - 1
                                )
                            ]

                            if indicador is not None:
                                indicador.warning(
                                    "El modelo está saturado. "
                                    f"Nuevo intento en "
                                    f"{espera} segundos..."
                                )

                            time.sleep(espera)

                            continue

                        errores_modelos.append(
                            f"{modelo}: saturado (503)"
                        )

                        break

                    if codigo == 429:

                        errores_modelos.append(
                            f"{modelo}: límite de cuota (429)"
                        )

                        # No continuar automáticamente:
                        # la cuota podría ser compartida.
                        raise

                    # Errores de autenticación y otros
                    # errores no se solucionan cambiando
                    # de modelo.
                    raise

        if ultimo_error is not None:

            detalle = "\n".join(errores_modelos)

            raise RuntimeError(
                "Ninguno de los modelos configurados "
                "pudo generar una respuesta.\n"
                f"{detalle}\n"
                f"Último error: {ultimo_error}"
            )

        raise RuntimeError(
            "No fue posible generar una respuesta."
        )

    finally:
        cliente.close()


# ============================================================
# MENSAJES DE ERROR
# ============================================================

def interpretar_error(error):

    codigo = obtener_codigo_error(error)

    mensaje = str(error)

    if "Ninguno de los modelos configurados" in mensaje:
        return (
            "Se intentaron los modelos de Gemini "
            "configurados, pero ninguno pudo responder. "
            "Revisa los detalles para conocer "
            "qué ocurrió con cada modelo."
        )

    if codigo == 503:
        return (
            "Gemini está temporalmente saturado. "
            "Se realizaron reintentos automáticos, "
            "pero no fue posible obtener una respuesta."
        )

    if codigo == 429:
        return (
            "Se alcanzó el límite de solicitudes "
            "o de cuota de Gemini. "
            "Intenta nuevamente más tarde."
        )

    if codigo == 404:
        return (
            "El modelo solicitado no está disponible "
            "para tu clave API."
        )

    if codigo in (401, 403):
        return (
            "La clave API no tiene autorización "
            "para realizar esta solicitud. "
            "Revisa GEMINI_API_KEY."
        )

    return (
        "No fue posible obtener una respuesta "
        "del asistente. Revisa los detalles del error."
    )


# ============================================================
# PÁGINA PRINCIPAL DEL ASISTENTE
# ============================================================

def mostrar_asistente():

    st.title("🤖 Asistente Metalúrgico IA")

    st.write(
        "Resuelve tus dudas sobre conminución, "
        "hidrometalurgia o cálculos de procesos."
    )

    # --------------------------------------------------------
    # INICIALIZAR MEMORIA DEL CHAT
    # --------------------------------------------------------

    if "ia_mensajes" not in st.session_state:
        st.session_state["ia_mensajes"] = []

    # --------------------------------------------------------
    # BOTÓN PARA REINICIAR CONVERSACIÓN
    # --------------------------------------------------------

    if st.button(
        "🔄 Borrar Memoria y Reiniciar Chat",
        key="reiniciar_chat_ia"
    ):

        st.session_state["ia_mensajes"] = []

        st.rerun()

    st.markdown("---")

    # --------------------------------------------------------
    # CONFIGURACIÓN API
    # --------------------------------------------------------

    api_key = obtener_api_key()

    if not api_key:

        st.error(
            "No se encontró la clave API de Gemini."
        )

        st.info(
            "Configura GEMINI_API_KEY en el archivo "
            ".streamlit/secrets.toml para activar "
            "el asistente."
        )

        return

    # --------------------------------------------------------
    # MOSTRAR HISTORIAL
    # --------------------------------------------------------

    for mensaje in st.session_state["ia_mensajes"]:

        with st.chat_message(mensaje["role"]):

            st.markdown(mensaje["content"])

    # --------------------------------------------------------
    # INGRESO DE MENSAJE
    # --------------------------------------------------------

    pregunta = st.chat_input(
        "Escribe tu duda aquí...",
        key="entrada_chat_ia"
    )

    if not pregunta:
        return

    historial_anterior = list(
        st.session_state["ia_mensajes"]
    )

    # --------------------------------------------------------
    # MOSTRAR MENSAJE DEL USUARIO
    # --------------------------------------------------------

    st.session_state["ia_mensajes"].append({
        "role": "user",
        "content": pregunta
    })

    with st.chat_message("user"):

        st.markdown(pregunta)

    # --------------------------------------------------------
    # GENERAR RESPUESTA
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        indicador = st.empty()

        try:

            respuesta, modelo_utilizado = generar_respuesta(
                api_key=api_key,
                mensajes=historial_anterior,
                pregunta=pregunta,
                indicador=indicador
            )

            indicador.empty()

            st.markdown(respuesta)

            st.session_state["ia_mensajes"].append({
                "role": "assistant",
                "content": respuesta
            })

            st.caption(
                f"Respuesta generada con {modelo_utilizado}"
            )

        except Exception as error:

            indicador.empty()

            st.error(
                interpretar_error(error)
            )

            # Eliminar la pregunta fallida del
            # historial enviado a Gemini.
            st.session_state["ia_mensajes"].pop()

            with st.expander(
                "Ver detalles del error"
            ):

                st.code(
                    f"{type(error).__name__}: {error}"
                )

    # --------------------------------------------------------
    # INFORMACIÓN FINAL
    # --------------------------------------------------------

    st.caption(
        "Asistente basado en Google Gemini. "
        "Las respuestas generadas por IA pueden "
        "contener errores y deben verificarse "
        "antes de utilizarlas en decisiones "
        "técnicas u operacionales."
    )


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
Eres un asistente académico especializado en ingeniería metalúrgica,
particularmente en minerales oxidados de cobre, caracterización mineralógica,
conminución, aglomeración, lixiviación, extracción por solventes (SX),
electroobtención (EW), balances de masa y operaciones de laboratorio.

OBJETIVO: Ayudar al usuario a comprender y evaluar técnicamente las ideas,
no limitarte a darle la razón.

PENSAMIENTO CRÍTICO:
- Examina las premisas de cada pregunta antes de responder.
- Detecta preguntas trampa, contradicciones, unidades incompatibles,
  afirmaciones absolutas injustificadas y datos insuficientes.
- Si la premisa es falsa, indícalo con claridad, explica el error y
  responde utilizando la premisa corregida.
- Si es parcialmente correcta, distingue lo válido de lo que depende
  de condiciones, supuestos o excepciones.
- No inventes errores ni cuestiones una afirmación correcta por sistema.
- No cambies una conclusión fundamentada solo porque el usuario insista.
- Si hay incertidumbre o varias interpretaciones posibles, explícalas.

RIGOR TÉCNICO:
- Distingue masa, volumen, concentración, caudal, recuperación y eficiencia.
- Diferencia resultados teóricos, estimaciones y mediciones experimentales.
- No inventes resultados de laboratorio, condiciones, normas ni referencias.
- Evita afirmar que un parámetro siempre mejora un proceso cuando depende
  de mineralogía, condiciones operacionales u otras variables.
- Si se solicita un cálculo, verifica datos y unidades, muestra la fórmula
  y el procedimiento pertinente, y señala supuestos y limitaciones.
- Presenta normalmente los resultados calculados con dos decimales,
  salvo que otra precisión sea técnicamente necesaria.
- Si faltan datos esenciales, pregunta por ellos en vez de inventarlos.
- No afirmes haber ejecutado módulos de la plataforma ni haber leído
  sus resultados si el usuario no los ha compartido expresamente.

SEGURIDAD:
- Cuando corresponda, señala riesgos químicos, térmicos, eléctricos
  y mecánicos, y remite a protocolos de laboratorio y fichas de seguridad.
- Para diluir ácido sulfúrico, indica añadir lentamente el ácido al agua,
  nunca agua al ácido, con protección y control del calentamiento.

ESTILO:
- Responde en español, con terminología metalúrgica precisa y comprensible.
- Mantén un tono académico, objetivo, respetuoso y directo.
- No felicites ni confirmes automáticamente afirmaciones sin verificarlas.
- Adapta la extensión y la estructura a la pregunta: este chat NO tiene
  una estructura fija de cuatro secciones.
- Reconoce explícitamente cuando no puedas determinar algo con los datos.
"""


INSTRUCCIONES_CALCULADORAS = """
Eres un asistente especializado en ingeniería metalúrgica que interpreta
EXCLUSIVAMENTE los resultados proporcionados por una calculadora de la
plataforma. Responde en español con precisión técnica y lenguaje académico.

Organiza SIEMPRE la respuesta en estas cuatro secciones, en este orden:

### 1. Resultados
Presenta los resultados principales, con valores y unidades, e indica qué
representan. Evita repetir íntegramente una tabla extensa.

### 2. Explicación metalúrgica
Explica el fundamento del proceso y la relación entre las variables y los
resultados efectivamente proporcionados.

### 3. Análisis técnico
Interpreta los resultados, relaciones, supuestos y limitaciones. Diferencia
cálculos teóricos de datos experimentales. Si los datos no permiten concluir
que un resultado es adecuado, indícalo claramente.

### 4. Recomendaciones
Propón verificaciones y recomendaciones técnicas pertinentes al proceso,
sin inventar parámetros ni criterios de aceptación.

SECCIÓN CONDICIONAL:
Si, y solo si, la calculadora corresponde a la preparación o dilución de
soluciones con ácido sulfúrico, agrega al final:
### 5. Advertencias de seguridad para la preparación
Advierte que el ácido sulfúrico es corrosivo y que su dilución libera calor.
Indica añadir lentamente el ácido al agua, nunca el agua al ácido, utilizar
protección personal adecuada, controlar el calentamiento y seguir el
procedimiento del laboratorio y la ficha de datos de seguridad.
No agregues esta sección a cálculos que solo mencionen ácido sulfúrico
como especie química, sin preparar ni diluir una solución.

REGLAS:
- No inventes datos, mediciones, condiciones ni conclusiones.
- Respeta exactamente los resultados y las unidades proporcionadas.
- Muestra los valores numéricos con dos decimales cuando corresponda.
- No recalcules ni cambies los resultados de la calculadora.
- Si detectas incoherencias, señálalas sin alterar silenciosamente los datos.
- Evita saludos, despedidas, secciones extra y conclusiones independientes.
- Las instrucciones específicas enviadas por cada módulo aportan el contexto
  del cálculo, pero no reemplazan esta estructura de respuesta.
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
    pregunta,
    instrucciones_sistema=INSTRUCCIONES_SISTEMA
):

    chat = cliente.chats.create(
        model=modelo,
        history=historial,
        config=types.GenerateContentConfig(
            system_instruction=instrucciones_sistema,
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
    indicador=None,
    tipo_asistente="calculadora"
):

    if tipo_asistente == "conversacion":
        instrucciones_sistema = INSTRUCCIONES_SISTEMA
    elif tipo_asistente == "calculadora":
        instrucciones_sistema = INSTRUCCIONES_CALCULADORAS
    else:
        raise ValueError("tipo_asistente debe ser conversacion o calculadora")

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
                        pregunta=pregunta,
                        instrucciones_sistema=instrucciones_sistema
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
                indicador=indicador,
                tipo_asistente="conversacion"
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

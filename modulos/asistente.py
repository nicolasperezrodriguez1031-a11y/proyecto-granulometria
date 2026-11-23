
import time
import re
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

FORMATO DE ECUACIONES QUÍMICAS Y MATEMÁTICAS:
- Escribe fórmulas y reacciones con LaTeX válido y delimitadores completos.
- Para ecuaciones independientes usa $$ ... $$ en una línea separada.
- Para expresiones dentro de una oración usa $ ... $.
- Nunca mezcles fragmentos LaTeX sin delimitar con texto normal.
- Evita comandos inventados, llaves desbalanceadas y barras invertidas duplicadas.
- Comprueba balance de masa, átomos y carga en cada reacción.
- No presentes relaciones cuantitativas operacionales como universales sin
  datos, condiciones o fuentes que las justifiquen.

ESTILO:
- Responde en español, con terminología metalúrgica precisa y comprensible.
- Mantén un tono académico, objetivo, respetuoso y directo.
- No felicites ni confirmes automáticamente afirmaciones sin verificarlas.
- Adapta la extensión y la estructura a la pregunta: este chat NO tiene
  una estructura fija de cuatro secciones.
- Reconoce explícitamente cuando no puedas determinar algo con los datos.
"""


INSTRUCCIONES_CALCULADORAS = """
Eres un especialista en ingeniería metalúrgica que interpreta únicamente los
DATOS ENVIADOS por la calculadora. Nunca cambies un resultado de la plataforma.
Responde SIEMPRE en español y con estas secciones, sin agregar otras:

### 1. Resultados
Indica resultados principales, sus unidades y significado. Conserva las
cifras suministradas y evita redondeos intermedios o conversiones innecesarias.

### 2. Explicación metalúrgica
Explica el mecanismo físico o químico aplicable a ESTA calculadora.
Si incluyes reacciones, comprueba conservación de elementos y carga,
especies, fases, sentido de reacción y condiciones. No inventes reacciones.
Usa LaTeX válido: $...$ en línea y $$...$$ para ecuaciones independientes;
no muestres comandos LaTeX como texto plano. Si una reacción depende del
reactivo, electrodo o medio no informado, describe el principio sin asumirlos.

### 3. Análisis técnico
Identifica los KPI REALMENTE calculados; interpreta sus valores, unidades,
significado y limitaciones. No deduzcas eficiencia, recuperación, pureza,
calidad o cumplimiento sin los datos necesarios. No confundas valores
teóricos, experimentales y objetivos operacionales.

### 4. Recomendaciones
Prioriza 2 a 4 acciones específicas vinculadas con los KPI disponibles.
Para cada acción explica QUÉ variable revisar, POR QUÉ afecta al proceso y
QUÉ medición permitiría confirmar la hipótesis. No inventes rangos óptimos,
fallas, umbrales, ni cambios de operación sin evidencia.

Si la calculadora PREPARA O DILUYE una solución que contiene ácido sulfúrico,
agrega exactamente una quinta sección:
### 5. Advertencias de seguridad para la preparación
Indica que el ácido es corrosivo, que su dilución libera calor y que debe
agregarse lentamente el ácido al agua, nunca agua al ácido; usar protección,
control térmico, procedimiento y ficha de datos de seguridad. No incluyas
esta sección en cálculos de SX, potenciales o electrodeposición que solo
mencionan ácido como parte del proceso.

FORMATO DE ECUACIONES:
- Utiliza $ ... $ para fórmulas en línea y $$ ... $$ para ecuaciones aisladas.
- Cierra todos los delimitadores y las llaves; no escribas comandos LaTeX
  fuera de los delimitadores matemáticos.
- No incluyas cifras de desempeño supuestamente universales sin respaldo.

REGLAS OBLIGATORIAS:
- La calculadora es la fuente de verdad de los valores. No los recalcules.
- Nunca confundas mL, L, m³, g/L, g/h, t/h, %, ni caudales con volúmenes.
- No conviertas una cifra pequeña a 0,00 por redondeo y luego la interpretes
  como cero: conserva la unidad original o utiliza más decimales si hace falta.
- No inventes datos de laboratorio, objetivos ni referencias bibliográficas.
- Si falta un KPI, explica que no puede evaluarse con los datos disponibles.
- Si detectas una contradicción, señálala sin corregir el resultado mostrado.
- Evita saludos, cierres, introducciones adicionales y secciones extra.
"""

# Instrucciones exclusivas de interpretación; no alteran ninguna calculadora.
PROMPTS_CALCULADORAS = {
    "granulometria": """ANÁLISIS GRANULOMÉTRICO: analiza masa retenida,
porcentaje retenido y pasante, curva granulométrica y P80/T80 solo si están
presentes. No equipares T80 y P80 sin definición explícita. Verifica el
sentido de las fracciones y señala posible segregación o muestreo no
representativo solo como hipótesis. Recomienda verificar tamices, cierre
de masa, representatividad y tendencia de la curva, sin inventar umbrales.""",
    "razon_reduccion": """RAZÓN DE REDUCCIÓN: interpreta RR como relación
entre tamaños de alimentación y producto según la definición recibida.
Distingue alimentación-primario, alimentación-secundario y primario-
secundario cuando estén disponibles. No concluyas eficiencia energética,
capacidad o desgaste solo a partir de RR. Recomienda verificar tamaños,
muestreo, ajustes y desempeño por etapa.""",
    "aglomeracion": """AGLOMERACIÓN Y CURADO: interpreta humedad inicial,
humedad objetivo, humedad calculada, masa de agua, ácido añadido y
condiciones de curado SOLO si se informan. Distingue humedad en base
húmeda de base seca. No equipares porcentaje de humedad con recuperación
metalúrgica. Relaciona recomendaciones con uniformidad de humectación,
formación de aglomerados, permeabilidad y control de dosificación.
No inventes reacciones específicas del mineral ni consumos reales.""",
    "solucion_lixiviante": """PREPARACIÓN DE SOLUCIÓN LIXIVIANTE:
interpreta concentración objetivo de H2SO4, volumen final, pureza,
densidad y cantidad de reactivo cuando se informen. Distingue masa de
ácido puro y masa o volumen de solución comercial. No interpretes la
preparación como una recuperación de cobre. Recomienda revisar aforo,
homogeneización y medición de concentración. Incluye seguridad de ácido.""",
    "fa_fo": """RELACIÓN DE FASES FA/FO: interpreta exactamente la
razón acuoso/orgánico o su inversa según lo indique la calculadora.
Distingue volumen de caudal y unidades de cada fase. No deduzcas porcentaje
de extracción, eficiencia o recuperación a partir de la razón FA/FO.
Recomienda revisar proporción de fases, mezcla, separación y arrastres
como variables de seguimiento, sin afirmar que existan problemas.""",
    "sx_extraccion": """EXTRACCIÓN POR SOLVENTES: el PORCENTAJE DE
EXTRACCIÓN, si fue enviado, es un KPI prioritario: repítelo exactamente,
explica qué fracción del Cu alimentado en PLS se transfiere al orgánico
y úsalo en análisis técnico y recomendaciones. No lo confundas con FA/FO,
concentración, porcentaje de reextracción ni recuperación global. Si NO
se proporcionó el porcentaje, NO lo inventes ni afirmes haberlo analizado:
indica que falta ese dato. Distingue PLS, refino, orgánico cargado y
orgánico descargado. La extracción con extractantes ácidos puede
representarse, solo si aplica, como
Cu^{2+}_{(ac)} + 2RH_{(org)} ⇌ R2Cu_{(org)} + 2H^{+}_{(ac)}.
Recomienda revisar pH, concentraciones de entrada/salida, razón de fases,
contacto y separación; no atribuyas causas sin mediciones.""",
    "sx_reextraccion": """REEXTRACCIÓN POR SOLVENTES: el PORCENTAJE DE
REEXTRACCIÓN, si fue enviado, es un KPI prioritario: repítelo exactamente,
explica la transferencia del Cu desde el orgánico cargado al electrolito
y úsalo en análisis técnico y recomendaciones. No lo confundas con
extracción ni recuperación global. Si no fue enviado, dilo claramente.
Distingue orgánico cargado/descargado y electrolito pobre/rico. Con
extractantes ácidos, la reextracción es el sentido inverso del equilibrio
de extracción; no inventes especies orgánicas ni estequiometría adicional.
Recomienda revisar acidez, concentración de Cu, razón de fases, contacto
y separación, condicionándolo a mediciones.""",
    "electrolito_rico": """PREPARACIÓN DE ELECTROLITO RICO EN LABORATORIO:
interpreta volumen final, Cu2+, H2SO4, masa de CuSO4·5H2O, masa de
ácido puro y cantidad de ácido comercial según datos. No confundas esta
preparación con el enriquecimiento industrial por SX. No supongas
impurezas del CuSO4·5H2O si la calculadora considera reactivo puro.
Recomienda revisar pureza informada del ácido, aforo, homogeneización,
concentraciones y temperatura. Incluye advertencias de seguridad.""",
    "potenciales": """POTENCIALES ESTÁNDAR DE REDUCCIÓN: distingue
E° de reducción del cátodo y E° de reducción del par elegido como ánodo.
E°celda = E°cátodo(reducción) - E°ánodo(reducción). No inviertas signos
dos veces. Explica que E°celda positivo favorece la espontaneidad bajo
condiciones estándar para la reacción escrita, mientras que una celda
electrolítica puede requerir energía externa. No infieras voltaje real,
sobrepotenciales, cinética o rendimiento sin datos.""",
    "electrodeposicion": """ELECTRODEPOSICIÓN: analiza metal e ion
seleccionados, I=j*A si corresponde, tiempo, masa teórica por Faraday,
masa experimental y eficiencia de corriente SOLO si están presentes.
Usa la semirreacción catódica del metal seleccionado con su carga y
número de electrones; no asumas que siempre es Cu. Distingue masa teórica
de masa real y eficiencia de corriente de recuperación global. En EW de
Cu con ánodo insoluble convencional puede ocurrir oxidación de agua,
no disolución de cobre anódico. Recomienda verificar corriente, área
activa, tiempo, pesaje, contactos y condiciones del electrolito.""",
}

# Se excluye deliberadamente el circuito completo SX, que permanece oculto.
# Las palabras clave se utilizan solo cuando el módulo no envía un ID explícito.
CLAVES_CALCULADORAS = (
    ("sx_reextraccion", ("reextracción", "reextraccion", "re-extracción", "reextraccion sx")),
    ("sx_extraccion", ("extracción por solventes", "extraccion por solventes", "extracción sx", "extraccion sx")),
    ("fa_fo", ("fa/fo", "fo/fa", "fase acuosa/fase orgánica", "razón de fases")),
    ("electrolito_rico", ("preparación de electrolito", "preparacion de electrolito", "sulfato de cobre pentahidratado")),
    ("solucion_lixiviante", ("preparación de solución", "preparacion de solucion", "solución lixiviante")),
    ("potenciales", ("potenciales estándar", "potenciales estandar", "potencial estándar de celda")),
    ("electrodeposicion", ("electrodeposición", "electrodeposicion", "masa depositada", "eficiencia de corriente")),
    ("aglomeracion", ("aglomeración", "aglomeracion", "humedad objetivo", "acondicionamiento")),
    ("granulometria", ("granulometría", "granulometria", "tamices", "porcentaje pasante")),
    ("razon_reduccion", ("razón de reducción", "razon de reduccion", "rr alimentación", "rr alimentacion")),
)


def identificar_calculadora(pregunta, calculadora=None):
    """Selecciona un prompt sin intervenir en las funciones de cálculo."""
    if calculadora is not None:
        clave = str(calculadora).strip().lower()
        if clave not in PROMPTS_CALCULADORAS:
            raise ValueError(f"Calculadora IA no reconocida: {calculadora}")
        return clave
    texto = str(pregunta).lower()
    # No interpretar información del circuito SX oculto.
    if "circuito completo" in texto or "circuito sx-ew" in texto:
        return None
    for clave, expresiones in CLAVES_CALCULADORAS:
        if any(expresion in texto for expresion in expresiones):
            return clave
    return None


def construir_instrucciones_calculadora(pregunta, calculadora=None):
    clave = identificar_calculadora(pregunta, calculadora)
    if clave is None:
        return INSTRUCCIONES_CALCULADORAS
    return INSTRUCCIONES_CALCULADORAS + "\n\nINSTRUCCIONES ESPECÍFICAS:\n" + PROMPTS_CALCULADORAS[clave]

# ============================================================
# NORMALIZAR DELIMITADORES MATEMÁTICOS PARA STREAMLIT
# ============================================================

def normalizar_latex_respuesta(texto):
    """Normaliza delimitadores habituales sin modificar cálculos ni química.

    No intenta reparar ecuaciones inválidas o alterar su significado.
    Respeta bloques de código Markdown para no modificar ejemplos literales.
    """
    if not isinstance(texto, str):
        return texto

    partes = re.split(r"(```[\s\S]*?```)", texto)

    def normalizar_parte(parte):
        # Delimitadores estándar de LaTeX a delimitadores compatibles con Markdown.
        parte = re.sub(r"\\\[\s*([\s\S]*?)\s*\\\]", r"\n\n$$\n\1\n$$\n\n", parte)
        parte = re.sub(r"\\\(([\s\S]*?)\\\)", r"$\1$", parte)
        # Los bloques $$ aislados entre párrafos evitan que se mezclen con texto.
        parte = re.sub(r"(?<!\$)\$\$\s*([\s\S]*?)\s*\$\$(?!\$)",
                       lambda m: "\n\n$$\n" + m.group(1).strip() + "\n$$\n\n", parte)
        return parte

    return "".join(
        bloque if indice % 2 else normalizar_parte(bloque)
        for indice, bloque in enumerate(partes)
    )


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
    tipo_asistente="calculadora",
    calculadora=None
):

    if tipo_asistente == "conversacion":
        instrucciones_sistema = INSTRUCCIONES_SISTEMA
    elif tipo_asistente == "calculadora":
        instrucciones_sistema = construir_instrucciones_calculadora(
            pregunta, calculadora
        )
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

            st.markdown(normalizar_latex_respuesta(mensaje["content"]))

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

            st.markdown(normalizar_latex_respuesta(respuesta))

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

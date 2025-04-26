import streamlit as st
import pandas as pd
import altair as alt
from textblob import TextBlob
import re
from googletrans import Translator

# 🎀 Configuración de la página
st.set_page_config(
    page_title="Analizador de Textos Cute ✨",
    page_icon="🌸",
    layout="wide"
)

# 🎀 Título principal
st.title("🌸 Analizador de Textos Cute con TextBlob 🌸")
st.markdown("""
Bienvenido a esta aplicación re tierna para analizar tus textos ✨.
Aquí podrás:
- Analizar sentimientos y subjetividad 💖
- Ver tus palabras más usadas 🌈
- Traducir tu texto si es necesario ✨
""")

# 🎀 Opciones de entrada
st.sidebar.title("🌸 Opciones mágicas")
modo = st.sidebar.selectbox(
    "¿Cómo quieres ingresar tu texto?",
    ["Escribir texto", "Subir un archivo"]
)

# 🎀 Función para contar palabras
def contar_palabras(texto):
    stop_words = set([
        "a", "al", "como", "con", "de", "del", "el", "ella", "ellos", "en", "es", "la", "lo", 
        "los", "las", "por", "para", "que", "un", "una", "y", "yo", "tú", "mi", "mis", "tu", "tus",
        "the", "and", "for", "from", "you", "your", "this", "that", "with", "was", "are", "have", "has"
    ])
    
    palabras = re.findall(r'\b\w+\b', texto.lower())
    palabras_filtradas = [p for p in palabras if p not in stop_words and len(p) > 2]
    
    contador = {}
    for palabra in palabras_filtradas:
        contador[palabra] = contador.get(palabra, 0) + 1
    
    return dict(sorted(contador.items(), key=lambda x: x[1], reverse=True))

# 🎀 Función para traducir texto
translator = Translator()

def traducir_texto(texto):
    try:
        traduccion = translator.translate(texto, src='es', dest='en')
        return traduccion.text
    except Exception as e:
        st.error(f"🌸 Error al traducir: {e}")
        return texto

# 🎀 Función para procesar el texto
def procesar_texto(texto):
    texto_original = texto
    texto_ingles = traducir_texto(texto)
    blob = TextBlob(texto_ingles)
    
    sentimiento = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity
    
    contador_palabras = contar_palabras(texto_ingles)
    
    return {
        "sentimiento": sentimiento,
        "subjetividad": subjetividad,
        "contador_palabras": contador_palabras,
        "texto_original": texto_original,
        "texto_traducido": texto_ingles
    }

# 🎀 Función para mostrar resultados lindos
def mostrar_resultados(resultados):
    st.subheader("💖 Resultados del Análisis")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🌟 Sentimiento:**")
        sentimiento_norm = (resultados["sentimiento"] + 1) / 2
        st.progress(sentimiento_norm)
        
        if resultados["sentimiento"] > 0.05:
            st.success(f"😊 Positivo ({resultados['sentimiento']:.2f})")
        elif resultados["sentimiento"] < -0.05:
            st.error(f"😢 Negativo ({resultados['sentimiento']:.2f})")
        else:
            st.info(f"😐 Neutral ({resultados['sentimiento']:.2f})")
        
        st.markdown("**🌟 Subjetividad:**")
        st.progress(resultados["subjetividad"])
        
        if resultados["subjetividad"] > 0.5:
            st.warning(f"💭 Alta subjetividad ({resultados['subjetividad']:.2f})")
        else:
            st.info(f"📋 Baja subjetividad ({resultados['subjetividad']:.2f})")
    
    with col2:
        st.markdown("**🎀 Palabras más frecuentes:**")
        if resultados["contador_palabras"]:
            df_palabras = pd.DataFrame(
                list(resultados["contador_palabras"].items())[:10],
                columns=["Palabra", "Frecuencia"]
            )
            chart = alt.Chart(df_palabras).mark_bar(
                color='#FFB6C1'  # ROSADITO 🎀
            ).encode(
                x=alt.X('Palabra:N', sort='-y'),
                y='Frecuencia:Q',
                tooltip=['Palabra', 'Frecuencia']
            ).properties(
                width=400,
                height=300
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.write("🌸 No hay suficientes palabras para mostrar.")

    # 🎀 Texto traducido
    st.subheader("🌸 Texto Traducido")
    with st.expander("✨ Ver traducción completa"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**🌼 Texto Original (Español):**")
            st.text(resultados["texto_original"])
        with col2:
            st.markdown("**🌼 Texto Traducido (Inglés):**")
            st.text(resultados["texto_traducido"])

# 🎀 Lógica principal
if modo == "Escribir texto":
    st.subheader("💌 Escribe tu texto aquí")
    texto = st.text_area("", height=200, placeholder="Escribe algo bonito...")
    
    if st.button("🌸 Analizar texto"):
        if texto.strip():
            with st.spinner("🌸 Analizando tu texto con amor..."):
                resultados = procesar_texto(texto)
                mostrar_resultados(resultados)
        else:
            st.warning("Por favor escribe algo para analizar 🌸.")

elif modo == "Subir un archivo":
    st.subheader("📂 Sube un archivo de texto")
    archivo = st.file_uploader("Elige tu archivo mágico:", type=["txt", "csv", "md"])
    
    if archivo is not None:
        contenido = archivo.getvalue().decode("utf-8")
        with st.expander("📖 Ver contenido del archivo"):
            st.text(contenido[:1000] + ("..." if len(contenido) > 1000 else ""))
        
        if st.button("🌸 Analizar archivo"):
            with st.spinner("🌸 Analizando tu archivo con cariño..."):
                resultados = procesar_texto(contenido)
                mostrar_resultados(resultados)

# 🎀 Footer
st.markdown("---")
st.markdown("Desarrollado con mucho 💖 y magia usando **Streamlit**, **TextBlob** y **Altair** ✨")

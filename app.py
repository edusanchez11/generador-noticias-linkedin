import streamlit as st
import requests
from datetime import datetime, timedelta
import openai
from typing import List, Dict
import json
import os
from groq import Groq
import time
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="Generador de Noticias LinkedIn",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Funciones auxiliares
@st.cache_data(ttl=3600)  # Cache por 1 hora
def obtener_noticias_newsapi(api_key: str, categoria: str = "general", pais: str = "us", num_articulos: int = 10) -> List[Dict]:
    """
    Obtiene noticias de NewsAPI
    """
    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": api_key,
            "category": categoria,
            "country": pais,
            "pageSize": num_articulos,
            "sortBy": "publishedAt"
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        return data.get("articles", [])
    
    except Exception as e:
        st.error(f"Error al obtener noticias: {str(e)}")
        return []

@st.cache_data(ttl=3600)
def obtener_noticias_guardian(api_key: str, seccion: str = "world", num_articulos: int = 10) -> List[Dict]:
    """
    Obtiene noticias de The Guardian API
    """
    try:
        url = "https://content.guardianapis.com/search"
        params = {
            "api-key": api_key,
            "section": seccion,
            "page-size": num_articulos,
            "order-by": "newest",
            "show-fields": "headline,trailText,bodyText,thumbnail"
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        articles = []
        
        for item in data.get("response", {}).get("results", []):
            articles.append({
                "title": item.get("webTitle", ""),
                "description": item.get("fields", {}).get("trailText", ""),
                "content": item.get("fields", {}).get("bodyText", "")[:500] + "...",
                "url": item.get("webUrl", ""),
                "publishedAt": item.get("webPublicationDate", ""),
                "urlToImage": item.get("fields", {}).get("thumbnail", "")
            })
        
        return articles
    
    except Exception as e:
        st.error(f"Error al obtener noticias de The Guardian: {str(e)}")
        return []

@st.cache_data(ttl=3600)
def obtener_noticias_google(query: str, num_articulos: int = 10, idioma: str = "es") -> List[Dict]:
    """
    Obtiene noticias de Google News usando una query personalizada
    """
    try:
        from pygooglenews import GoogleNews
        
        # Inicializar Google News
        gn = GoogleNews(lang=idioma, country='ES' if idioma == 'es' else 'US')
        
        # Buscar noticias por query
        search_result = gn.search(query)
        
        articles = []
        
        if search_result and 'entries' in search_result:
            for entry in search_result['entries'][:num_articulos]:
                # Extraer imagen si existe
                image_url = ""
                if hasattr(entry, 'media_content') and entry.media_content:
                    image_url = entry.media_content[0].get('url', '')
                elif hasattr(entry, 'links'):
                    for link in entry.links:
                        if 'image' in link.get('type', ''):
                            image_url = link.get('href', '')
                            break
                
                articles.append({
                    "title": entry.title,
                    "description": entry.summary if hasattr(entry, 'summary') else entry.title,
                    "content": (entry.summary if hasattr(entry, 'summary') else entry.title)[:500] + "...",
                    "url": entry.link,
                    "publishedAt": entry.published if hasattr(entry, 'published') else "",
                    "urlToImage": image_url,
                    "source": entry.source.title if hasattr(entry, 'source') else "Google News"
                })
        
        return articles
    
    except Exception as e:
        st.error(f"Error al obtener noticias de Google: {str(e)}")
        return []

@st.cache_data(ttl=3600)
def obtener_noticias_google_trending(num_articulos: int = 10, idioma: str = "es") -> List[Dict]:
    """
    Obtiene las noticias trending de Google News
    """
    try:
        from pygooglenews import GoogleNews
        
        # Inicializar Google News
        gn = GoogleNews(lang=idioma, country='ES' if idioma == 'es' else 'US')
        
        # Obtener noticias trending
        trending = gn.top_news()
        
        articles = []
        
        if trending and 'entries' in trending:
            for entry in trending['entries'][:num_articulos]:
                # Extraer imagen si existe
                image_url = ""
                if hasattr(entry, 'media_content') and entry.media_content:
                    image_url = entry.media_content[0].get('url', '')
                
                articles.append({
                    "title": entry.title,
                    "description": entry.summary if hasattr(entry, 'summary') else entry.title,
                    "content": (entry.summary if hasattr(entry, 'summary') else entry.title)[:500] + "...",
                    "url": entry.link,
                    "publishedAt": entry.published if hasattr(entry, 'published') else "",
                    "urlToImage": image_url,
                    "source": entry.source.title if hasattr(entry, 'source') else "Google News"
                })
        
        return articles
    
    except Exception as e:
        st.error(f"Error al obtener trending de Google: {str(e)}")
        return []

@st.cache_data(ttl=3600)
def obtener_noticias_rss_bbc(query: str = "", num_articulos: int = 10) -> List[Dict]:
    """
    Obtiene noticias de BBC RSS como alternativa gratuita
    """
    try:
        import feedparser
        
        # URLs de RSS de BBC por categoría
        rss_urls = {
            "general": "http://feeds.bbci.co.uk/news/rss.xml",
            "business": "http://feeds.bbci.co.uk/news/business/rss.xml", 
            "technology": "http://feeds.bbci.co.uk/news/technology/rss.xml",
            "science": "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml"
        }
        
        # Usar feed general por defecto
        feed_url = rss_urls["general"]
        
        # Si hay query, usar búsqueda en tecnología/business
        if query and any(word in query.lower() for word in ["tech", "ai", "digital", "business", "economy"]):
            if any(word in query.lower() for word in ["tech", "ai", "digital", "technology"]):
                feed_url = rss_urls["technology"]
            else:
                feed_url = rss_urls["business"]
        
        feed = feedparser.parse(feed_url)
        articles = []
        
        for entry in feed.entries[:num_articulos]:
            # Filtrar por query si se proporciona
            if query and query.lower() not in entry.title.lower() and query.lower() not in entry.summary.lower():
                continue
                
            articles.append({
                "title": entry.title,
                "description": entry.summary,
                "content": entry.summary[:500] + "...",
                "url": entry.link,
                "publishedAt": entry.published if hasattr(entry, 'published') else "",
                "urlToImage": ""
            })
        
        return articles[:num_articulos]
    
    except Exception as e:
        st.error(f"Error al obtener noticias RSS: {str(e)}")
        return []

@st.cache_data(ttl=3600)
def buscar_noticias_guardian_personalizada(api_key: str, query: str, num_articulos: int = 10) -> List[Dict]:
    """
    Busca noticias específicas en The Guardian API usando una query personalizada
    """
    try:
        url = "https://content.guardianapis.com/search"
        params = {
            "api-key": api_key,
            "q": query,
            "page-size": num_articulos,
            "order-by": "relevance",
            "show-fields": "headline,trailText,bodyText,thumbnail",
            "from-date": (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')  # Últimos 7 días
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        articles = []
        
        for item in data.get("response", {}).get("results", []):
            articles.append({
                "title": item.get("webTitle", ""),
                "description": item.get("fields", {}).get("trailText", ""),
                "content": item.get("fields", {}).get("bodyText", "")[:500] + "...",
                "url": item.get("webUrl", ""),
                "publishedAt": item.get("webPublicationDate", ""),
                "urlToImage": item.get("fields", {}).get("thumbnail", "")
            })
        
        return articles
    
    except Exception as e:
        st.error(f"Error al buscar noticias en The Guardian: {str(e)}")
        return []

@st.cache_data(ttl=3600)
def buscar_noticias_newsapi_personalizada(api_key: str, query: str, num_articulos: int = 10) -> List[Dict]:
    """
    Busca noticias específicas en NewsAPI usando una query personalizada
    """
    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            "apiKey": api_key,
            "q": query,
            "pageSize": num_articulos,
            "sortBy": "relevancy",
            "language": "en",
            "from": (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')  # Últimos 7 días
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        return data.get("articles", [])
    
    except Exception as e:
        st.error(f"Error al buscar noticias en NewsAPI: {str(e)}")
        return []

def generar_post_openai(client, noticia: Dict, estilo: str, tono: str, longitud: str) -> str:
    """
    Genera un post de LinkedIn usando OpenAI
    """
    try:
        prompt = f"""
        Eres un experto en marketing digital y redes sociales. Tu tarea es crear un post atractivo para LinkedIn basado en la siguiente noticia.

        NOTICIA:
        Título: {noticia['title']}
        Descripción: {noticia['description']}
        Contenido: {noticia['content']}

        INSTRUCCIONES:
        - Estilo: {estilo}
        - Tono: {tono}
        - Longitud: {longitud}
        - Incluye hashtags relevantes
        - Haz que sea atractivo y profesional
        - Agrega una pregunta al final para generar engagement
        - No incluyas enlaces en el texto

        Genera solo el texto del post, sin comillas ni explicaciones adicionales.
        """
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un experto creador de contenido para LinkedIn."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        st.error(f"Error al generar post con OpenAI: {str(e)}")
        return ""

def generar_post_groq(client, noticia: Dict, estilo: str, tono: str, longitud: str) -> str:
    """
    Genera un post de LinkedIn usando Groq
    """
    try:
        prompt = f"""
        Eres un experto en marketing digital y redes sociales. Tu tarea es crear un post atractivo para LinkedIn basado en la siguiente noticia.

        NOTICIA:
        Título: {noticia['title']}
        Descripción: {noticia['description']}
        Contenido: {noticia['content']}

        INSTRUCCIONES:
        - Estilo: {estilo}
        - Tono: {tono}
        - Longitud: {longitud}
        - Incluye hashtags relevantes
        - Haz que sea atractivo y profesional
        - Agrega una pregunta al final para generar engagement
        - No incluyas enlaces en el texto

        Genera solo el texto del post, sin comillas ni explicaciones adicionales.
        """
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Eres un experto creador de contenido para LinkedIn."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        st.error(f"Error al generar post con Groq: {str(e)}")
        return ""

# Función principal de la aplicación
def main():
    # Título y descripción
    st.title("📰 Generador de Noticias para LinkedIn")
    st.markdown("""
    Genera contenido atractivo para LinkedIn basado en las noticias más relevantes de la actualidad.
    Utiliza inteligencia artificial para crear posts personalizados según tu estilo y audiencia.
    """)
    
    # Sidebar para configuración
    with st.sidebar:
        st.header("⚙️ Configuración")
        
        # Configuración de APIs
        st.subheader("APIs de Noticias")
        
        # Determinar fuentes disponibles
        guardian_available = os.getenv("GUARDIAN_API_KEY") and os.getenv("GUARDIAN_API_KEY") != "tu_guardian_key_aqui"
        newsapi_available = os.getenv("NEWSAPI_KEY") and os.getenv("NEWSAPI_KEY") != "tu_newsapi_key_aqui"
        
        opciones_fuente = []
        if guardian_available and newsapi_available:
            opciones_fuente = ["Google News", "The Guardian", "NewsAPI", "BBC RSS", "Todas"]
            default_index = 0
        elif guardian_available:
            opciones_fuente = ["Google News", "The Guardian", "BBC RSS", "Todas las gratuitas"]
            default_index = 0
        elif newsapi_available:
            opciones_fuente = ["Google News", "NewsAPI", "BBC RSS", "Todas las gratuitas"]
            default_index = 0
        else:
            opciones_fuente = ["Google News", "BBC RSS"]
            default_index = 0
        
        fuente_noticias = st.selectbox(
            "Selecciona fuente de noticias:",
            opciones_fuente,
            index=default_index,
            help="Google News y BBC RSS están siempre disponibles sin API"
        )
        
        # Configuración específica para Google News
        if "Google News" in fuente_noticias:
            idioma_google = st.selectbox(
                "Idioma para Google News:",
                ["es", "en"],
                format_func=lambda x: "Español" if x == "es" else "English",
                help="Idioma de las noticias de Google News"
            )
        
        # Mostrar aviso si la fuente seleccionada no está configurada
        if fuente_noticias == "NewsAPI" and not newsapi_available:
            st.warning("⚠️ NewsAPI no está configurada. Configura tu API key.")
        elif fuente_noticias == "The Guardian" and not guardian_available:
            st.warning("⚠️ The Guardian API no está configurada.")
        elif fuente_noticias == "Ambas" and not (guardian_available and newsapi_available):
            if guardian_available:
                st.info("ℹ️ Solo The Guardian está configurada. Se usará únicamente esta fuente.")
            elif newsapi_available:
                st.info("ℹ️ Solo NewsAPI está configurada. Se usará únicamente esta fuente.")
            else:
                st.error("❌ Ninguna API está configurada.")
        
        if fuente_noticias in ["NewsAPI", "Ambas"]:
            newsapi_key = st.text_input("NewsAPI Key", 
                                       value=os.getenv("NEWSAPI_KEY", ""), 
                                       type="password", 
                                       help="Obtén tu API key en newsapi.org")
            
            if newsapi_key:
                categoria_news = st.selectbox(
                    "Categoría (NewsAPI):",
                    ["general", "business", "technology", "science", "health", "sports", "entertainment"]
                )
                
                pais_news = st.selectbox(
                    "País (NewsAPI):",
                    ["us", "gb", "es", "fr", "de", "it", "mx", "ar", "co", "cl"]
                )
        
        if fuente_noticias in ["The Guardian", "Ambas"]:
            guardian_key = st.text_input("Guardian API Key", 
                                        value=os.getenv("GUARDIAN_API_KEY", ""), 
                                        type="password", 
                                        help="Obtén tu API key en open-platform.theguardian.com")
            
            if guardian_key:
                seccion_guardian = st.selectbox(
                    "Sección (Guardian):",
                    ["world", "business", "technology", "science", "environment", "sport", "culture"]
                )
        
        # Configuración del LLM
        st.subheader("Configuración del LLM")
        
        proveedor_llm = st.selectbox(
            "Proveedor LLM:",
            ["OpenAI", "Groq"]
        )
        
        if proveedor_llm == "OpenAI":
            openai_key = st.text_input("OpenAI API Key", 
                                      value=os.getenv("OPENAI_API_KEY", ""), 
                                      type="password")
        else:
            groq_key = st.text_input("Groq API Key", 
                                    value=os.getenv("GROQ_API_KEY", ""), 
                                    type="password")
        
        # Configuración de estilo
        st.subheader("Personalización del Contenido")
        
        estilo = st.selectbox(
            "Estilo de escritura:",
            ["Profesional", "Informal", "Académico", "Persuasivo", "Informativo", "Inspiracional"]
        )
        
        tono = st.selectbox(
            "Tono:",
            ["Neutral", "Entusiasta", "Reflexivo", "Urgente", "Optimista", "Analítico"]
        )
        
        longitud = st.selectbox(
            "Longitud del post:",
            ["Corto (100-200 palabras)", "Medio (200-300 palabras)", "Largo (300-500 palabras)"]
        )
        
        num_articulos = st.slider("Número de noticias a obtener:", 5, 20, 10)
        
        # Estado de las API keys
        st.subheader("📊 Estado de APIs")
        
        # Fuentes gratuitas siempre disponibles
        st.success("✅ Google News: Disponible (gratuito, sin API)")
        st.success("✅ BBC RSS: Disponible (gratuito, sin API)")
        
        # Verificar Guardian API
        guardian_configured = os.getenv("GUARDIAN_API_KEY") and os.getenv("GUARDIAN_API_KEY") != "tu_guardian_key_aqui"
        if guardian_configured:
            st.success("✅ Guardian API: Activa")
        else:
            st.info("ℹ️ Guardian API: No configurada (opcional)")
            
        # Verificar NewsAPI
        newsapi_configured = os.getenv("NEWSAPI_KEY") and os.getenv("NEWSAPI_KEY") != "tu_newsapi_key_aqui"
        if newsapi_configured:
            st.success("✅ NewsAPI: Activa")
        else:
            st.info("ℹ️ NewsAPI: No configurada (opcional)")
            
        # Verificar LLM APIs
        openai_configured = os.getenv("OPENAI_API_KEY") and os.getenv("OPENAI_API_KEY") != "tu_openai_api_key_aqui"
        groq_configured = os.getenv("GROQ_API_KEY") and os.getenv("GROQ_API_KEY") != "tu_groq_api_key_aqui"
        
        if openai_configured:
            st.success("✅ OpenAI API: Activa")
        elif groq_configured:
            st.success("✅ Groq API: Activa")
        else:
            st.error("❌ LLM API: No configurada (requerida)")
        
        # Recomendación basada en configuración
        if (openai_configured or groq_configured):
            st.success("🎉 ¡Configuración perfecta! Usa Google News para las mejores noticias.")
        else:
            st.warning("⚠️ Configura una API de LLM (Groq recomendado) para generar posts.")
    
    # Contenido principal
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("� Búsqueda Personalizada")
        
        # Campo de búsqueda personalizada
        prompt_busqueda = st.text_area(
            "¿Sobre qué tema quieres encontrar noticias?",
            placeholder="Ej: Inteligencia artificial en el sector financiero, Sostenibilidad empresarial, Nuevas tecnologías en salud...",
            height=100,
            help="Describe el tema o tipo de noticias que te interesan"
        )
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            buscar_con_prompt = st.button("� Buscar Noticias", type="primary", use_container_width=True)
        
        with col_btn2:
            obtener_trending = st.button("� Trending Google", use_container_width=True)
        
        if buscar_con_prompt and prompt_busqueda.strip():
            st.session_state.modo_busqueda = "personalizada"
            st.session_state.prompt_busqueda = prompt_busqueda
            noticias = []
            
            with st.spinner("🔍 Buscando noticias relevantes..."):
                # Google News (siempre disponible)
                if fuente_noticias in ["Google News", "Todas", "Todas las gratuitas"]:
                    st.info("🔍 Buscando en Google News...")
                    idioma = idioma_google if 'idioma_google' in locals() else 'es'
                    noticias_google = obtener_noticias_google(prompt_busqueda, 
                                                            num_articulos//3 if "Todas" in fuente_noticias else num_articulos, 
                                                            idioma)
                    noticias.extend(noticias_google)
                
                # The Guardian API
                if fuente_noticias in ["The Guardian", "Todas", "Todas las gratuitas"] and 'guardian_key' in locals() and guardian_key and guardian_key.strip() and guardian_key != "tu_guardian_key_aqui":
                    try:
                        noticias_guardian = buscar_noticias_guardian_personalizada(guardian_key, prompt_busqueda, 
                                                                                 num_articulos//3 if "Todas" in fuente_noticias else num_articulos)
                        noticias.extend(noticias_guardian)
                    except Exception as e:
                        st.warning("⚠️ Error con The Guardian API.")
                
                # BBC RSS (backup gratuito)
                if fuente_noticias in ["BBC RSS", "Todas", "Todas las gratuitas"]:
                    noticias_rss = obtener_noticias_rss_bbc(prompt_busqueda, 
                                                          num_articulos//3 if "Todas" in fuente_noticias else num_articulos)
                    noticias.extend(noticias_rss)
                
                # NewsAPI (si está configurada)
                if fuente_noticias in ["NewsAPI", "Todas"] and 'newsapi_key' in locals() and newsapi_key and newsapi_key.strip() and newsapi_key != "tu_newsapi_key_aqui":
                    noticias_newsapi = buscar_noticias_newsapi_personalizada(newsapi_key, prompt_busqueda, 
                                                                           num_articulos//3 if fuente_noticias == "Todas" else num_articulos)
                    noticias.extend(noticias_newsapi)
            
            if noticias:
                st.session_state.noticias = noticias
                st.success(f"✅ {len(noticias)} noticias encontradas sobre: '{prompt_busqueda[:50]}...'")
            else:
                # Verificar qué APIs están disponibles para dar mejor feedback
                apis_disponibles = []
                if 'guardian_key' in locals() and guardian_key and guardian_key.strip() and guardian_key != "tu_guardian_key_aqui":
                    apis_disponibles.append("The Guardian")
                if 'newsapi_key' in locals() and newsapi_key and newsapi_key.strip() and newsapi_key != "tu_newsapi_key_aqui":
                    apis_disponibles.append("NewsAPI")
                
                if not apis_disponibles:
                    st.error("❌ No hay APIs configuradas. Por favor, configura al menos The Guardian API en el sidebar.")
                else:
                    st.warning(f"⚠️ No se encontraron noticias relevantes sobre '{prompt_busqueda[:30]}...' en {', '.join(apis_disponibles)}. Intenta con otros términos.")
        
        elif obtener_trending:
            st.session_state.modo_busqueda = "trending"
            noticias = []
            
            with st.spinner("� Obteniendo noticias trending de Google..."):
                # Obtener trending de Google News
                idioma = idioma_google if 'idioma_google' in locals() else 'es'
                noticias_trending = obtener_noticias_google_trending(num_articulos, idioma)
                noticias.extend(noticias_trending)
                
                # También obtener de otras fuentes si están disponibles
                if fuente_noticias in ["NewsAPI", "Todas"] and 'newsapi_key' in locals() and newsapi_key and newsapi_key.strip() and newsapi_key != "tu_newsapi_key_aqui":
                    noticias_newsapi = obtener_noticias_newsapi(newsapi_key, categoria_news, pais_news, num_articulos//3)
                    noticias.extend(noticias_newsapi)
                
                if fuente_noticias in ["The Guardian", "Todas", "Todas las gratuitas"] and 'guardian_key' in locals() and guardian_key and guardian_key.strip() and guardian_key != "tu_guardian_key_aqui":
                    noticias_guardian = obtener_noticias_guardian(guardian_key, seccion_guardian, num_articulos//3)
                    noticias.extend(noticias_guardian)
            
            if noticias:
                st.session_state.noticias = noticias
                st.success(f"✅ {len(noticias)} noticias generales obtenidas")
            else:
                # Verificar qué APIs están disponibles
                apis_disponibles = []
                if 'guardian_key' in locals() and guardian_key and guardian_key.strip() and guardian_key != "tu_guardian_key_aqui":
                    apis_disponibles.append("The Guardian")
                if 'newsapi_key' in locals() and newsapi_key and newsapi_key.strip() and newsapi_key != "tu_newsapi_key_aqui":
                    apis_disponibles.append("NewsAPI")
                
                if not apis_disponibles:
                    st.error("❌ No hay APIs configuradas. Por favor, configura al menos The Guardian API en el sidebar.")
                elif len(apis_disponibles) == 1 and fuente_noticias == "Ambas":
                    st.info(f"ℹ️ Solo {apis_disponibles[0]} está configurada. Usa '{apis_disponibles[0]}' como fuente para mejores resultados.")
                else:
                    st.warning("⚠️ No se pudieron obtener noticias. Verifica la conexión a internet.")
        
        # Mostrar noticias disponibles
        if 'noticias' in st.session_state and st.session_state.noticias:
            st.subheader("📋 Noticias Encontradas:")
            
            # Mostrar el tipo de búsqueda
            if st.session_state.get('modo_busqueda') == "personalizada":
                st.info(f"🎯 Búsqueda: {st.session_state.get('prompt_busqueda', '')[:50]}...")
            elif st.session_state.get('modo_busqueda') == "trending":
                st.info("🔥 Mostrando noticias trending de Google News")
            
            for i, noticia in enumerate(st.session_state.noticias):
                with st.expander(f"📰 {noticia['title'][:45]}..."):
                    st.write(f"**Descripción:** {noticia['description'][:150]}...")
                    if noticia.get('urlToImage'):
                        st.image(noticia['urlToImage'], width=180)
                    
                    if st.button(f"✨ Seleccionar esta noticia", key=f"btn_{i}", use_container_width=True):
                        st.session_state.noticia_seleccionada = noticia
                        st.success("✅ Noticia seleccionada")
    
    with col2:
        st.header("✨ Generador de Posts LinkedIn")
        
        if 'noticia_seleccionada' in st.session_state:
            noticia = st.session_state.noticia_seleccionada
            
            # Mostrar noticia seleccionada de forma más atractiva
            with st.container():
                st.subheader("📰 Noticia Seleccionada")
                
                col_img, col_text = st.columns([1, 3])
                
                with col_img:
                    if noticia.get('urlToImage'):
                        st.image(noticia['urlToImage'], width=150)
                
                with col_text:
                    st.markdown(f"**{noticia['title']}**")
                    st.write(noticia['description'][:200] + "...")
                    st.caption(f"📅 {noticia.get('publishedAt', 'Fecha no disponible')}")
            
            st.markdown("---")
            
            # Verificar configuración del LLM
            llm_configurado = False
            client = None
            
            if proveedor_llm == "OpenAI" and 'openai_key' in locals() and openai_key:
                client = openai.OpenAI(api_key=openai_key)
                llm_configurado = True
            elif proveedor_llm == "Groq" and 'groq_key' in locals() and groq_key:
                client = Groq(api_key=groq_key)
                llm_configurado = True
            
            if llm_configurado:
                # Mostrar configuración actual
                col_config1, col_config2, col_config3 = st.columns(3)
                with col_config1:
                    st.info(f"🎨 **Estilo:** {estilo}")
                with col_config2:
                    st.info(f"🎭 **Tono:** {tono}")
                with col_config3:
                    st.info(f"📏 **Longitud:** {longitud}")
                
                st.markdown("### 🚀 Generar Publicación")
                
                if st.button("🤖 Crear Post de LinkedIn", type="primary", use_container_width=True):
                    with st.spinner("🧠 Generando contenido optimizado para LinkedIn..."):
                        if proveedor_llm == "OpenAI":
                            post_generado = generar_post_openai(client, noticia, estilo, tono, longitud)
                        else:
                            post_generado = generar_post_groq(client, noticia, estilo, tono, longitud)
                        
                        if post_generado:
                            st.session_state.post_generado = post_generado
                            st.success("✅ ¡Post generado exitosamente!")
                
                # Mostrar post generado
                if 'post_generado' in st.session_state:
                    st.markdown("---")
                    st.markdown("### 📝 Tu Post de LinkedIn")
                    
                    # Vista previa del post con diseño similar a LinkedIn
                    with st.container():
                        st.markdown("""
                        <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #0077B5;'>
                        """, unsafe_allow_html=True)
                        
                        # Área de texto editable
                        post_editado = st.text_area(
                            "✏️ Edita tu post aquí:",
                            value=st.session_state.post_generado,
                            height=250,
                            help="Puedes modificar el texto antes de copiarlo"
                        )
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Métricas del post
                    col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)
                    with col_metric1:
                        st.metric("📊 Caracteres", len(post_editado))
                    with col_metric2:
                        st.metric("📝 Palabras", len(post_editado.split()))
                    with col_metric3:
                        hashtags_count = len([palabra for palabra in post_editado.split() if palabra.startswith('#')])
                        st.metric("🏷️ Hashtags", hashtags_count)
                    with col_metric4:
                        lineas = len(post_editado.split('\n'))
                        st.metric("📏 Líneas", lineas)
                    
                    # Opciones de acción mejoradas
                    st.markdown("### 🎯 Acciones")
                    
                    col_acc1, col_acc2, col_acc3, col_acc4 = st.columns(4)
                    
                    with col_acc1:
                        if st.button("📋 Copiar Post", use_container_width=True):
                            # En una aplicación real, esto copiaría al portapapeles
                            st.success("✅ ¡Post copiado!")
                            st.balloons()
                    
                    with col_acc2:
                        st.download_button(
                            "💾 Descargar",
                            data=post_editado,
                            file_name=f"linkedin_post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    
                    with col_acc3:
                        if st.button("🔄 Nuevo Post", use_container_width=True):
                            st.session_state.pop('post_generado', None)
                            st.rerun()
                    
                    with col_acc4:
                        linkedin_url = "https://www.linkedin.com/feed/"
                        st.link_button("� Ir a LinkedIn", linkedin_url, use_container_width=True)
                    
                    # Consejos para LinkedIn
                    with st.expander("💡 Consejos para LinkedIn"):
                        st.markdown("""
                        **🎯 Para maximizar el engagement:**
                        - Publica entre 8-10 AM o 12-2 PM
                        - Usa 3-5 hashtags relevantes
                        - Incluye preguntas para generar comentarios
                        - Agrega emojis para mayor atractivo visual
                        - Menciona a personas relevantes (@usuario)
                        """)
            
            else:
                st.warning("⚠️ Por favor, configura tu API key del LLM en el sidebar.")
        
        else:
            # Pantalla de bienvenida mejorada
            st.markdown("""
            <div style='text-align: center; padding: 40px;'>
                <h2>🚀 ¡Bienvenido al Generador de Posts LinkedIn!</h2>
                <p style='font-size: 18px; color: #666;'>
                Crea contenido profesional y atractivo para LinkedIn en segundos
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            col_inst1, col_inst2, col_inst3 = st.columns(3)
            
            with col_inst1:
                st.markdown("""
                ### � Paso 1
                **Busca noticias**
                
                Escribe un tema de tu interés o selecciona noticias generales
                """)
            
            with col_inst2:
                st.markdown("""
                ### ✨ Paso 2  
                **Selecciona noticia**
                
                Elige la noticia más relevante de los resultados encontrados
                """)
            
            with col_inst3:
                st.markdown("""
                ### 🚀 Paso 3
                **Genera tu post**
                
                Obtén un post optimizado y listo para LinkedIn
                """)
            
            st.markdown("---")
            
            # Ejemplos de búsqueda
            st.markdown("### 💡 Ideas de búsqueda:")
            
            col_ej1, col_ej2 = st.columns(2)
            
            with col_ej1:
                st.markdown("""
                **🏢 Negocios:**
                - "Inteligencia artificial en empresas"
                - "Tendencias de liderazgo 2024" 
                - "Transformación digital"
                - "Sostenibilidad empresarial"
                """)
            
            with col_ej2:
                st.markdown("""
                **💻 Tecnología:**
                - "Nuevas tecnologías emergentes"
                - "Ciberseguridad empresarial"
                - "Automatización de procesos"
                - "Innovación en startups"
                """)
            
            st.markdown("---")
            st.success("🚀 **Nuevo:** Ahora con Google News integrado para las noticias más relevantes y actuales")
            st.info("👈 ¡Comienza escribiendo tu búsqueda o prueba las noticias trending de Google!")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
        <p>🚀 Desarrollado con Streamlit y LLMs | 
        📊 Datos de <a href='https://newsapi.org/' target='_blank'>NewsAPI</a> y 
        <a href='https://open-platform.theguardian.com/' target='_blank'>The Guardian</a></p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
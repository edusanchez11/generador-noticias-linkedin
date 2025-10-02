"""
Utilidades adicionales para el generador de noticias LinkedIn
"""

import re
from typing import List, Dict, Tuple
import requests
from bs4 import BeautifulSoup
import feedparser
from datetime import datetime, timedelta

class NewsProcessor:
    """Clase para procesar y enriquecer noticias"""
    
    @staticmethod
    def extraer_palabras_clave(texto: str, num_palabras: int = 10) -> List[str]:
        """Extrae palabras clave del texto de la noticia"""
        # Lista de palabras comunes a filtrar
        stop_words = {
            'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 'le', 'da', 'su', 'por', 'son', 'con', 'para', 'al', 'del', 'los', 'las', 'pero', 'sus', 'una', 'como', 'está', 'han', 'más', 'sobre', 'hacer',
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
        }
        
        # Limpiar y dividir el texto
        texto_limpio = re.sub(r'[^\w\s]', ' ', texto.lower())
        palabras = texto_limpio.split()
        
        # Filtrar palabras cortas y stop words
        palabras_filtradas = [
            palabra for palabra in palabras 
            if len(palabra) > 3 and palabra not in stop_words
        ]
        
        # Contar frecuencias
        from collections import Counter
        contador = Counter(palabras_filtradas)
        
        return [palabra for palabra, _ in contador.most_common(num_palabras)]
    
    @staticmethod
    def generar_hashtags(palabras_clave: List[str], categoria: str = "") -> List[str]:
        """Genera hashtags relevantes basados en palabras clave"""
        hashtags = []
        
        # Hashtags base según categoría
        hashtags_base = {
            "business": ["#Business", "#Innovation", "#Leadership", "#Entrepreneurship"],
            "technology": ["#Technology", "#AI", "#Innovation", "#DigitalTransformation"],
            "science": ["#Science", "#Research", "#Innovation", "#Discovery"],
            "health": ["#Health", "#Wellness", "#Medicine", "#Healthcare"],
            "general": ["#News", "#Update", "#Important", "#Breaking"]
        }
        
        hashtags.extend(hashtags_base.get(categoria, hashtags_base["general"]))
        
        # Convertir palabras clave a hashtags
        for palabra in palabras_clave[:5]:
            hashtag = f"#{palabra.capitalize()}"
            if hashtag not in hashtags:
                hashtags.append(hashtag)
        
        return hashtags[:8]  # Limitar a 8 hashtags
    
    @staticmethod
    def resumir_noticia(noticia: Dict) -> str:
        """Crea un resumen conciso de la noticia"""
        titulo = noticia.get('title', '')
        descripcion = noticia.get('description', '')
        contenido = noticia.get('content', '')
        
        # Combinar información disponible
        texto_completo = f"{titulo}. {descripcion}. {contenido}"
        
        # Limitar a las primeras 200 palabras
        palabras = texto_completo.split()[:200]
        resumen = ' '.join(palabras)
        
        return resumen

class LinkedInOptimizer:
    """Clase para optimizar contenido para LinkedIn"""
    
    @staticmethod
    def optimizar_longitud(texto: str, longitud_objetivo: str) -> str:
        """Optimiza la longitud del texto según el objetivo"""
        palabras = texto.split()
        
        if longitud_objetivo == "Corto (100-200 palabras)":
            limite = 200
        elif longitud_objetivo == "Medio (200-300 palabras)":
            limite = 300
        else:  # Largo
            limite = 500
        
        if len(palabras) > limite:
            return ' '.join(palabras[:limite]) + "..."
        
        return texto
    
    @staticmethod
    def agregar_call_to_action(texto: str, tipo: str = "pregunta") -> str:
        """Agrega un call to action al final del post"""
        ctas = {
            "pregunta": [
                "¿Qué opinas sobre esto?",
                "¿Cómo crees que esto impactará en el futuro?",
                "¿Has experimentado algo similar?",
                "¿Cuál es tu perspectiva sobre este tema?"
            ],
            "accion": [
                "¡Comparte si estás de acuerdo!",
                "¡Deja tu opinión en los comentarios!",
                "¡Etiqueta a alguien que debería ver esto!",
                "¡Sígueme para más contenido como este!"
            ],
            "reflexion": [
                "Reflexionemos sobre esto juntos.",
                "¿Qué lecciones podemos aprender de esto?",
                "Es momento de repensar nuestro enfoque.",
                "Cada cambio trae nuevas oportunidades."
            ]
        }
        
        import random
        cta = random.choice(ctas.get(tipo, ctas["pregunta"]))
        
        return f"{texto}\n\n{cta}"
    
    @staticmethod
    def formatear_para_linkedin(texto: str, hashtags: List[str]) -> str:
        """Formatea el texto final para LinkedIn"""
        # Asegurar que el texto termine correctamente
        if not texto.endswith(('.', '!', '?')):
            texto += '.'
        
        # Agregar salto de línea antes de hashtags
        hashtags_texto = ' '.join(hashtags)
        
        return f"{texto}\n\n{hashtags_texto}"

class TrendAnalyzer:
    """Analizador de tendencias en noticias"""
    
    @staticmethod
    def obtener_trending_topics() -> List[str]:
        """Obtiene temas trending de diferentes fuentes"""
        # Esta función podría expandirse para incluir APIs de trending topics
        # Por ahora, devolvemos temas comunes actuales
        trending_base = [
            "Artificial Intelligence",
            "Remote Work",
            "Sustainability",
            "Digital Transformation",
            "Mental Health",
            "Cryptocurrency",
            "Climate Change",
            "Innovation",
            "Leadership",
            "Entrepreneurship"
        ]
        
        return trending_base
    
    @staticmethod
    def analizar_relevancia(noticia: Dict, trending_topics: List[str]) -> float:
        """Analiza qué tan relevante es una noticia basado en trending topics"""
        texto_noticia = f"{noticia.get('title', '')} {noticia.get('description', '')}".lower()
        
        coincidencias = 0
        for topic in trending_topics:
            if topic.lower() in texto_noticia:
                coincidencias += 1
        
        # Retorna un score de 0 a 1
        return min(coincidencias / len(trending_topics), 1.0)

def generar_prompt_personalizado(noticia: Dict, perfil_usuario: Dict) -> str:
    """
    Genera un prompt personalizado basado en el perfil del usuario
    
    Args:
        noticia: Diccionario con información de la noticia
        perfil_usuario: Diccionario con preferencias del usuario
    
    Returns:
        String con el prompt personalizado
    """
    
    sector = perfil_usuario.get('sector', 'general')
    audiencia = perfil_usuario.get('audiencia', 'profesional')
    objetivos = perfil_usuario.get('objetivos', 'informar')
    
    prompt_base = f"""
    Eres un experto en {sector} creando contenido para LinkedIn.
    
    NOTICIA:
    Título: {noticia['title']}
    Descripción: {noticia['description']}
    
    PERFIL DE USUARIO:
    - Sector: {sector}
    - Audiencia objetivo: {audiencia}
    - Objetivo principal: {objetivos}
    
    Crea un post que:
    1. Sea relevante para profesionales de {sector}
    2. Conecte con una audiencia {audiencia}
    3. Tenga como objetivo {objetivos}
    4. Incluya hashtags específicos del sector
    5. Genere engagement apropiado para el contexto profesional
    
    El post debe ser auténtico y aportar valor real a la red profesional.
    """
    
    return prompt_base

# Funciones de utilidad adicionales

def validar_api_keys(keys_dict: Dict[str, str]) -> Dict[str, bool]:
    """Valida que las API keys estén configuradas correctamente"""
    resultados = {}
    
    for servicio, key in keys_dict.items():
        if key and len(key) > 10:  # Validación básica
            resultados[servicio] = True
        else:
            resultados[servicio] = False
    
    return resultados

def calcular_metricas_post(texto: str) -> Dict[str, int]:
    """Calcula métricas básicas del post generado"""
    caracteres = len(texto)
    palabras = len(texto.split())
    lineas = len(texto.split('\n'))
    hashtags = len([palabra for palabra in texto.split() if palabra.startswith('#')])
    
    return {
        'caracteres': caracteres,
        'palabras': palabras,
        'lineas': lineas,
        'hashtags': hashtags,
        'tiempo_lectura': max(1, palabras // 200)  # minutos aproximados
    }
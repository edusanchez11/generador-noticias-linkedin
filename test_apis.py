"""
Script de prueba para verificar que todas las APIs funcionen correctamente
"""

import requests
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_guardian_api():
    """Prueba The Guardian API"""
    print("🔍 Probando The Guardian API...")
    
    api_key = os.getenv("GUARDIAN_API_KEY")
    if not api_key or api_key == "tu_guardian_key_aqui":
        print("❌ Guardian API key no configurada")
        return False
    
    try:
        url = "https://content.guardianapis.com/search"
        params = {
            "api-key": api_key,
            "q": "artificial intelligence",
            "page-size": 3,
            "order-by": "relevance",
            "show-fields": "headline,trailText,bodyText,thumbnail",
            "from-date": (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        results = data.get("response", {}).get("results", [])
        
        if results:
            print(f"✅ Guardian API funcionando - {len(results)} noticias encontradas")
            print(f"   Primera noticia: {results[0]['webTitle'][:60]}...")
            return True
        else:
            print("⚠️ Guardian API responde pero sin resultados")
            return False
            
    except Exception as e:
        print(f"❌ Error en Guardian API: {str(e)}")
        return False

def test_groq_api():
    """Prueba Groq API"""
    print("\n🤖 Probando Groq API...")
    
    try:
        from groq import Groq
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key == "tu_groq_api_key_aqui":
            print("❌ Groq API key no configurada")
            return False
        
        client = Groq(api_key=api_key)
        
        # Prueba simple
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "Eres un asistente conciso."},
                {"role": "user", "content": "Di 'Hola' en una sola palabra."}
            ],
            max_tokens=50,
            temperature=0.1
        )
        
        resultado = response.choices[0].message.content.strip()
        print(f"✅ Groq API funcionando - Respuesta: {resultado}")
        return True
        
    except Exception as e:
        print(f"❌ Error en Groq API: {str(e)}")
        return False

def test_bbc_rss():
    """Prueba BBC RSS (fuente gratuita)"""
    print("\n📰 Probando BBC RSS...")
    
    try:
        import feedparser
        
        feed_url = "http://feeds.bbci.co.uk/news/technology/rss.xml"
        feed = feedparser.parse(feed_url)
        
        if feed.entries:
            print(f"✅ BBC RSS funcionando - {len(feed.entries)} noticias disponibles")
            print(f"   Primera noticia: {feed.entries[0].title[:60]}...")
            return True
        else:
            print("⚠️ BBC RSS sin contenido")
            return False
            
    except Exception as e:
        print(f"❌ Error en BBC RSS: {str(e)}")
        return False

def main():
    """Ejecuta todas las pruebas"""
    print("🚀 INICIANDO PRUEBAS DE APIS")
    print("=" * 50)
    
    # Contar APIs funcionando
    apis_ok = 0
    total_apis = 3
    
    if test_guardian_api():
        apis_ok += 1
    
    if test_groq_api():
        apis_ok += 1
        
    if test_bbc_rss():
        apis_ok += 1
    
    print("\n" + "=" * 50)
    print(f"📊 RESULTADOS: {apis_ok}/{total_apis} APIs funcionando")
    
    if apis_ok == total_apis:
        print("🎉 ¡TODAS LAS APIS FUNCIONAN CORRECTAMENTE!")
        print("✅ La aplicación está lista para usar al 100%")
    elif apis_ok >= 2:
        print("✅ Configuración suficiente para usar la aplicación")
        if apis_ok == 2:
            print("💡 Tienes funcionalidad completa con las APIs disponibles")
    else:
        print("⚠️ Necesitas configurar más APIs para funcionalidad completa")
    
    print("\n🔗 Abre la aplicación en: http://localhost:8503")

if __name__ == "__main__":
    main()
"""
Sistema de Publicaciones Automáticas para LinkedIn
Genera contenido semanal sobre Data Science, Analysis e IA
"""

import streamlit as st
import schedule
import time
from datetime import datetime, timedelta
import json
import os
from app import obtener_noticias_guardian, obtener_noticias_google, generar_post_linkedin

class AutomacionLinkedIn:
    def __init__(self):
        self.temas = {
            'lunes': 'Data Science',
            'miercoles': 'Data Analysis', 
            'viernes': 'Inteligencia Artificial'
        }
        
        self.sectores = [
            'deportivos',
            'cadena de suministro',
            'banca',
            'estudiantes'
        ]
        
        self.semana_actual = 0
        self.posts_generados = []
        
    def obtener_tema_y_sector(self, dia_semana):
        """Obtiene el tema y sector según el día y semana actual"""
        temas_por_dia = {
            0: 'Data Science',      # Lunes
            2: 'Data Analysis',     # Miércoles  
            4: 'Inteligencia Artificial'  # Viernes
        }
        
        if dia_semana not in temas_por_dia:
            return None, None
            
        tema = temas_por_dia[dia_semana]
        sector = self.sectores[self.semana_actual % 4]
        
        return tema, sector
    
    def generar_query_busqueda(self, tema, sector):
        """Genera query específico para la búsqueda"""
        queries = {
            ('Data Science', 'deportivos'): f"{tema} sports analytics machine learning deportes",
            ('Data Science', 'cadena de suministro'): f"{tema} supply chain logistics optimization",
            ('Data Science', 'banca'): f"{tema} banking fintech financial analytics",
            ('Data Science', 'estudiantes'): f"{tema} education learning analytics university",
            
            ('Data Analysis', 'deportivos'): f"{tema} sports statistics performance analytics deportes",
            ('Data Analysis', 'cadena de suministro'): f"{tema} supply chain analytics inventory management",
            ('Data Analysis', 'banca'): f"{tema} banking data analytics financial insights",
            ('Data Analysis', 'estudiantes'): f"{tema} educational data analytics student performance",
            
            ('Inteligencia Artificial', 'deportivos'): f"AI artificial intelligence sports technology deportes",
            ('Inteligencia Artificial', 'cadena de suministro'): f"AI supply chain automation robotics",
            ('Inteligencia Artificial', 'banca'): f"AI banking fintech automation machine learning",
            ('Inteligencia Artificial', 'estudiantes'): f"AI education technology learning students"
        }
        
        return queries.get((tema, sector), f"{tema} {sector}")
    
    def buscar_noticias_relevantes(self, query):
        """Busca noticias usando múltiples fuentes"""
        noticias = []
        
        try:
            # Google News (fuente principal)
            noticias_google = obtener_noticias_google(query)
            if noticias_google:
                noticias.extend(noticias_google[:3])
        except Exception as e:
            print(f"Error Google News: {e}")
        
        try:
            # The Guardian como backup
            noticias_guardian = obtener_noticias_guardian(query)
            if noticias_guardian:
                noticias.extend(noticias_guardian[:2])
        except Exception as e:
            print(f"Error Guardian: {e}")
            
        return noticias[:5]  # Máximo 5 noticias
    
    def generar_post_automatico(self, tema, sector, noticia):
        """Genera un post optimizado para el tema y sector"""
        
        contexto_sector = {
            'deportivos': "sector deportivo y analytics deportivos",
            'cadena de suministro': "gestión de la cadena de suministro y logística",
            'banca': "sector bancario y fintech", 
            'estudiantes': "educación y formación académica"
        }
        
        prompt_personalizado = f"""
        Crea un post profesional para LinkedIn sobre {tema} en el {contexto_sector[sector]}.
        
        Noticia base: {noticia.get('title', '')}
        Descripción: {noticia.get('description', '')}
        
        ESTRUCTURA REQUERIDA:
        1. Hook inicial relacionando {tema} con {sector}
        2. Insight principal de la noticia
        3. 3 puntos clave aplicables al {contexto_sector[sector]}
        4. Call-to-action preguntando por experiencias del sector
        5. Hashtags: #{tema.replace(' ', '')} #{sector.replace(' ', '').title()} #LinkedIn #DataDriven
        
        Tono: Profesional pero accesible, enfocado en valor práctico.
        Longitud: 150-200 palabras.
        """
        
        return generar_post_linkedin(
            noticia_texto=f"{noticia.get('title', '')} - {noticia.get('description', '')}",
            estilo="profesional",
            tono="informativo", 
            longitud="medio",
            prompt_personalizado=prompt_personalizado
        )
    
    def ejecutar_publicacion_diaria(self):
        """Ejecuta la lógica de publicación para el día actual"""
        hoy = datetime.now()
        dia_semana = hoy.weekday()  # 0=Lunes, 1=Martes, etc.
        
        tema, sector = self.obtener_tema_y_sector(dia_semana)
        
        if not tema:
            print(f"No hay publicación programada para {hoy.strftime('%A')}")
            return None
            
        print(f"🚀 Generando post: {tema} x {sector}")
        
        # Buscar noticias
        query = self.generar_query_busqueda(tema, sector)
        noticias = self.buscar_noticias_relevantes(query)
        
        if not noticias:
            print("❌ No se encontraron noticias relevantes")
            return None
            
        # Generar post con la mejor noticia
        mejor_noticia = noticias[0]
        post_generado = self.generar_post_automatico(tema, sector, mejor_noticia)
        
        # Guardar resultado
        resultado = {
            'fecha': hoy.isoformat(),
            'tema': tema,
            'sector': sector,
            'noticia_fuente': mejor_noticia,
            'post_generado': post_generado,
            'query_usado': query
        }
        
        self.guardar_post(resultado)
        return resultado
    
    def guardar_post(self, post_data):
        """Guarda el post generado en archivo JSON"""
        filename = f"posts_automaticos_{datetime.now().strftime('%Y_%m')}.json"
        
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                posts = json.load(f)
        else:
            posts = []
            
        posts.append(post_data)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Post guardado en {filename}")
    
    def programar_publicaciones(self):
        """Programa las publicaciones semanales"""
        # Lunes a las 9:00 AM
        schedule.every().monday.at("09:00").do(self.ejecutar_publicacion_diaria)
        
        # Miércoles a las 9:00 AM  
        schedule.every().wednesday.at("09:00").do(self.ejecutar_publicacion_diaria)
        
        # Viernes a las 9:00 AM
        schedule.every().friday.at("09:00").do(self.ejecutar_publicacion_diaria)
        
        print("📅 Publicaciones programadas:")
        print("   • Lunes 9:00 AM - Data Science")
        print("   • Miércoles 9:00 AM - Data Analysis") 
        print("   • Viernes 9:00 AM - Inteligencia Artificial")
        print(f"   • Sector actual: {self.sectores[self.semana_actual % 4]}")
    
    def avanzar_semana(self):
        """Avanza a la siguiente semana (cambio de sector)"""
        self.semana_actual += 1
        print(f"🔄 Avanzando a sector: {self.sectores[self.semana_actual % 4]}")
    
    def ejecutar_scheduler(self):
        """Ejecuta el scheduler continuo"""
        print("🤖 Sistema de automatización iniciado...")
        
        # Programar cambio de sector cada lunes
        schedule.every().monday.at("08:00").do(self.avanzar_semana)
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Revisar cada minuto

# Función para testing inmediato
def test_generacion_inmediata():
    """Genera un post de prueba inmediatamente"""
    automator = AutomacionLinkedIn()
    
    # Simular diferentes combinaciones
    combinaciones = [
        ('Data Science', 'deportivos'),
        ('Data Analysis', 'banca'), 
        ('Inteligencia Artificial', 'estudiantes'),
        ('Data Science', 'cadena de suministro')
    ]
    
    for tema, sector in combinaciones:
        print(f"\n🧪 Testando: {tema} x {sector}")
        
        query = automator.generar_query_busqueda(tema, sector)
        noticias = automator.buscar_noticias_relevantes(query)
        
        if noticias:
            post = automator.generar_post_automatico(tema, sector, noticias[0])
            print(f"✅ Post generado: {post[:100]}...")
        else:
            print("❌ No se encontraron noticias")

if __name__ == "__main__":
    # Descomenta para testing
    # test_generacion_inmediata()
    
    # Para producción
    automator = AutomacionLinkedIn()
    automator.programar_publicaciones()
    automator.ejecutar_scheduler()
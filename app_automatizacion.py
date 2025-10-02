# Interfaz Streamlit para Automatización Semanal
import streamlit as st
import json
from datetime import datetime, timedelta
import pandas as pd
from automatizacion_semanal import AutomacionLinkedIn

def main():
    st.set_page_config(
        page_title="📅 Automatización Semanal LinkedIn",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Sistema de Publicaciones Automáticas LinkedIn")
    st.markdown("**Genera contenido semanal sobre Data Science, Analysis e IA**")
    
    # Sidebar con configuración
    with st.sidebar:
        st.header("⚙️ Configuración")
        
        # Inicializar automator
        if 'automator' not in st.session_state:
            st.session_state.automator = AutomacionLinkedIn()
        
        automator = st.session_state.automator
        
        st.subheader("📋 Programación Semanal")
        st.write("**Lunes:** Data Science")  
        st.write("**Miércoles:** Data Analysis")
        st.write("**Viernes:** Inteligencia Artificial")
        
        st.subheader("🎯 Rotación de Sectores")
        sector_actual = automator.sectores[automator.semana_actual % 4]
        st.info(f"**Sector Actual:** {sector_actual.title()}")
        
        # Botón para cambiar sector manualmente
        if st.button("🔄 Cambiar Sector"):
            automator.avanzar_semana()
            st.success(f"Cambiado a: {automator.sectores[automator.semana_actual % 4].title()}")
            st.rerun()
    
    # Tabs principales
    tab1, tab2, tab3, tab4 = st.tabs(["🚀 Generar Ahora", "📊 Histórico", "⚙️ Testing", "📋 Programación"])
    
    with tab1:
        st.header("🚀 Generar Post Inmediato")
        
        col1, col2 = st.columns(2)
        
        with col1:
            tema_seleccionado = st.selectbox(
                "📚 Selecciona el Tema:",
                ['Data Science', 'Data Analysis', 'Inteligencia Artificial']
            )
        
        with col2:
            sector_seleccionado = st.selectbox(
                "🎯 Selecciona el Sector:",
                ['deportivos', 'cadena de suministro', 'banca', 'estudiantes']
            )
        
        if st.button("🎯 Generar Post Ahora", type="primary"):
            with st.spinner(f"Generando post sobre {tema_seleccionado} en {sector_seleccionado}..."):
                
                # Generar query y buscar noticias
                query = automator.generar_query_busqueda(tema_seleccionado, sector_seleccionado)
                st.info(f"🔍 Búsqueda: {query}")
                
                noticias = automator.buscar_noticias_relevantes(query)
                
                if noticias:
                    st.success(f"✅ Encontradas {len(noticias)} noticias relevantes")
                    
                    # Mostrar noticias encontradas
                    with st.expander("📰 Noticias Encontradas"):
                        for i, noticia in enumerate(noticias):
                            st.write(f"**{i+1}.** {noticia.get('title', 'Sin título')}")
                            st.write(f"   {noticia.get('description', 'Sin descripción')[:150]}...")
                    
                    # Generar post con la mejor noticia
                    mejor_noticia = noticias[0]
                    post_generado = automator.generar_post_automatico(
                        tema_seleccionado, 
                        sector_seleccionado, 
                        mejor_noticia
                    )
                    
                    st.subheader("✨ Post Generado")
                    st.text_area(
                        "📝 Contenido del Post:",
                        post_generado,
                        height=300,
                        key="post_generado"
                    )
                    
                    # Guardar automáticamente
                    resultado = {
                        'fecha': datetime.now().isoformat(),
                        'tema': tema_seleccionado,
                        'sector': sector_seleccionado,
                        'noticia_fuente': mejor_noticia,
                        'post_generado': post_generado,
                        'query_usado': query
                    }
                    automator.guardar_post(resultado)
                    st.success("💾 Post guardado automáticamente")
                    
                else:
                    st.error("❌ No se encontraron noticias relevantes. Intenta con otro tema/sector.")
    
    with tab2:
        st.header("📊 Histórico de Posts Generados")
        
        # Cargar posts guardados
        import os
        import glob
        
        archivos_posts = glob.glob("posts_automaticos_*.json")
        
        if archivos_posts:
            # Selector de mes
            archivo_seleccionado = st.selectbox(
                "📅 Selecciona el mes:",
                archivos_posts,
                format_func=lambda x: x.replace('posts_automaticos_', '').replace('.json', '')
            )
            
            if archivo_seleccionado:
                with open(archivo_seleccionado, 'r', encoding='utf-8') as f:
                    posts_historicos = json.load(f)
                
                if posts_historicos:
                    # Convertir a DataFrame para mejor visualización
                    df = pd.DataFrame(posts_historicos)
                    df['fecha'] = pd.to_datetime(df['fecha']).dt.strftime('%Y-%m-%d %H:%M')
                    
                    st.subheader(f"📈 Resumen ({len(posts_historicos)} posts)")
                    
                    # Métricas
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("📊 Total Posts", len(posts_historicos))
                    with col2:
                        temas_unicos = df['tema'].nunique()
                        st.metric("📚 Temas", temas_unicos)
                    with col3:
                        sectores_unicos = df['sector'].nunique() 
                        st.metric("🎯 Sectores", sectores_unicos)
                    with col4:
                        ultimo_post = df['fecha'].iloc[-1] if len(df) > 0 else "N/A"
                        st.metric("🕐 Último Post", ultimo_post)
                    
                    # Tabla de posts
                    st.subheader("📋 Lista de Posts")
                    cols_mostrar = ['fecha', 'tema', 'sector', 'query_usado']
                    st.dataframe(df[cols_mostrar], use_container_width=True)
                    
                    # Selector para ver post completo
                    if len(posts_historicos) > 0:
                        post_idx = st.selectbox(
                            "👁️ Ver post completo:",
                            range(len(posts_historicos)),
                            format_func=lambda x: f"{df.iloc[x]['fecha']} - {df.iloc[x]['tema']} x {df.iloc[x]['sector']}"
                        )
                        
                        post_seleccionado = posts_historicos[post_idx]
                        
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            st.text_area(
                                "📝 Contenido:",
                                post_seleccionado['post_generado'],
                                height=300
                            )
                        with col2:
                            st.json({
                                'tema': post_seleccionado['tema'],
                                'sector': post_seleccionado['sector'], 
                                'fecha': post_seleccionado['fecha'],
                                'noticia_titulo': post_seleccionado['noticia_fuente'].get('title', 'N/A')[:100]
                            })
                else:
                    st.info("📭 No hay posts guardados en este archivo")
        else:
            st.info("📭 No hay posts históricos. ¡Genera tu primer post!")
    
    with tab3:
        st.header("🧪 Testing de Combinaciones")
        st.markdown("Prueba diferentes combinaciones de tema/sector antes de programar")
        
        if st.button("🚀 Test Todas las Combinaciones", type="primary"):
            combinaciones = [
                ('Data Science', 'deportivos'),
                ('Data Analysis', 'banca'),
                ('Inteligencia Artificial', 'estudiantes'), 
                ('Data Science', 'cadena de suministro')
            ]
            
            for i, (tema, sector) in enumerate(combinaciones):
                with st.expander(f"🧪 Test {i+1}: {tema} x {sector}"):
                    query = automator.generar_query_busqueda(tema, sector)
                    st.code(f"Query: {query}")
                    
                    with st.spinner("Buscando noticias..."):
                        noticias = automator.buscar_noticias_relevantes(query)
                    
                    if noticias:
                        st.success(f"✅ {len(noticias)} noticias encontradas")
                        st.write("**Primera noticia:**")
                        st.write(f"• {noticias[0].get('title', 'Sin título')}")
                    else:
                        st.error("❌ No se encontraron noticias")
    
    with tab4:
        st.header("📋 Configuración de Automatización")
        
        st.markdown("""
        ### 🤖 Sistema de Programación Automática
        
        **Horarios programados:**
        - **Lunes 9:00 AM:** Data Science
        - **Miércoles 9:00 AM:** Data Analysis  
        - **Viernes 9:00 AM:** Inteligencia Artificial
        
        **Rotación de sectores (cada semana):**
        1. **Semana 1:** Deportivos
        2. **Semana 2:** Cadena de Suministro
        3. **Semana 3:** Banca 
        4. **Semana 4:** Estudiantes
        """)
        
        st.warning("""
        ⚠️ **Nota:** Para activar la automatización completa, debes ejecutar:
        
        ```bash
        python automatizacion_semanal.py
        ```
        
        Este script mantendrá el sistema ejecutándose en segundo plano.
        """)
        
        st.info("""
        💡 **Alternativa:** Usa esta interfaz web para generar posts manualmente 
        cuando los necesites, sin necesidad de automatización completa.
        """)

if __name__ == "__main__":
    main()
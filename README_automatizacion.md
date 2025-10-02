# 🤖 Sistema de Automatización Semanal LinkedIn

## 📋 **Descripción**
Sistema automático que genera publicaciones de LinkedIn sobre **Data Science**, **Data Analysis** e **Inteligencia Artificial** para diferentes sectores industriales.

## 🎯 **Programación Semanal**

### **📅 Calendario de Publicaciones**
- **🟦 Lunes 9:00 AM:** Data Science
- **🟨 Miércoles 9:00 AM:** Data Analysis  
- **🟩 Viernes 9:00 AM:** Inteligencia Artificial

### **🔄 Rotación de Sectores (4 semanas)**
1. **Semana 1:** 🏆 Sector Deportivo
2. **Semana 2:** 📦 Cadena de Suministro
3. **Semana 3:** 🏦 Banca y Fintech
4. **Semana 4:** 🎓 Educación y Estudiantes

## 🚀 **Cómo Usar**

### **Opción 1: Interfaz Web (Recomendado)**
```bash
# Activa el entorno virtual
.\.venv\Scripts\Activate.ps1

# Ejecuta la interfaz de automatización
streamlit run app_automatizacion.py
```

### **Opción 2: Automatización Completa**
```bash
# Ejecuta el sistema en segundo plano
python automatizacion_semanal.py
```

## 📊 **Funcionalidades**

### **🎯 Generación Inteligente**
- ✅ Búsqueda automática de noticias relevantes
- ✅ Combinación de tema + sector específico
- ✅ Posts optimizados para LinkedIn
- ✅ Hashtags contextualmente relevantes

### **📈 Gestión de Contenido**
- ✅ Histórico de posts generados
- ✅ Métricas y estadísticas
- ✅ Exportación en JSON
- ✅ Preview antes de publicar

### **🧪 Testing y Configuración**
- ✅ Prueba de combinaciones tema/sector
- ✅ Validación de queries de búsqueda
- ✅ Control manual de rotación
- ✅ Logs detallados

## 🎨 **Ejemplos de Combinaciones**

| Día | Tema | Sector | Ejemplo de Query |
|-----|------|--------|------------------|
| Lunes | Data Science | Deportivos | "Data Science sports analytics machine learning deportes" |
| Miércoles | Data Analysis | Banca | "Data Analysis banking data analytics financial insights" |
| Viernes | IA | Estudiantes | "AI education technology learning students" |

## 📁 **Estructura de Archivos**

```
📦 Proyecto/
├── 🤖 automatizacion_semanal.py    # Motor de automatización
├── 🖥️ app_automatizacion.py        # Interfaz Streamlit
├── 📊 posts_automaticos_YYYY_MM.json # Histórico mensual
├── 📋 requirements.txt             # Dependencias
└── 🔧 .env                        # Configuración API
```

## ⚙️ **Configuración de APIs**

Crea un archivo `.env` con:
```env
GUARDIAN_API_KEY=tu_clave_guardian
GROQ_API_KEY=tu_clave_groq
```

## 📊 **Métricas Disponibles**

### **Estadísticas por Mes**
- 📈 Total de posts generados
- 📚 Temas más utilizados  
- 🎯 Sectores más activos
- 🕐 Horarios de generación

### **Análisis de Rendimiento**
- ✅ Tasa de éxito en búsqueda de noticias
- 🔍 Queries más efectivos
- 📰 Fuentes de noticias más utilizadas
- 💡 Temas con mayor engagement potencial

## 🎯 **Sectores y Casos de Uso**

### **🏆 Deportivo**
- **Data Science:** Analytics de rendimiento, predicciones
- **Data Analysis:** Estadísticas de jugadores, métricas de equipo
- **IA:** Computer vision, análisis de video, wearables

### **📦 Cadena de Suministro**
- **Data Science:** Optimización de rutas, predicción de demanda
- **Data Analysis:** KPIs logísticos, análisis de inventario  
- **IA:** Automatización de almacenes, robótica, IoT

### **🏦 Banca**
- **Data Science:** Credit scoring, detección de fraude
- **Data Analysis:** Análisis de riesgo, customer insights
- **IA:** Chatbots, trading algorítmico, RegTech

### **🎓 Estudiantes**  
- **Data Science:** Learning analytics, educational research
- **Data Analysis:** Performance tracking, institutional metrics
- **IA:** Sistemas tutores, personalización, EdTech

## 🔧 **Personalización**

### **Modificar Horarios**
Edita en `automatizacion_semanal.py`:
```python
# Cambiar horarios de publicación
schedule.every().monday.at("10:00").do(ejecutar_publicacion_diaria)
schedule.every().wednesday.at("14:00").do(ejecutar_publicacion_diaria)  
schedule.every().friday.at("16:00").do(ejecutar_publicacion_diaria)
```

### **Añadir Nuevos Sectores**
```python
self.sectores = [
    'deportivos',
    'cadena de suministro', 
    'banca',
    'estudiantes',
    'salud',           # Nuevo sector
    'retail',          # Nuevo sector
    'manufactura'      # Nuevo sector
]
```

### **Personalizar Templates**
Modifica los prompts en `generar_post_automatico()` para ajustar:
- Tono de voz
- Estructura del post
- Longitud de contenido
- Hashtags específicos

## 🚀 **Próximas Mejoras**

- [ ] 📱 Integración directa con LinkedIn API
- [ ] 📊 Dashboard analytics avanzado
- [ ] 🤖 IA para optimización de horarios
- [ ] 📈 A/B testing de diferentes formatos
- [ ] 🌐 Soporte multiidioma
- [ ] 📧 Notificaciones por email
- [ ] 🎨 Templates visuales personalizables

## 📞 **Soporte**

¿Preguntas o sugerencias? 
- 📧 Contacto: [tu-email]
- 🐙 GitHub: [link-repositorio]
- 💼 LinkedIn: [tu-perfil]

---

### 💡 **Tip Pro**
Usa la interfaz web para generar y revisar posts antes de activar la automatización completa. ¡Esto te permitirá ajustar el tono y estilo según tus preferencias!
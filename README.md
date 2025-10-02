# 📰 Generador de Noticias para LinkedIn

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-1.28+-red.svg" alt="Streamlit">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen.svg" alt="Status">
</p>

Una aplicación web desarrollada con Streamlit que utiliza inteligencia artificial para generar contenido atractivo de LinkedIn basado en noticias de actualidad. ¡Perfecto para mantener una presencia profesional activa en LinkedIn con solo 5-8 minutos por semana!

## 🎯 **Demo en Vivo**

¡Aplicación 100% funcional! Sigue las instrucciones de instalación y tendrás tu generador de contenido LinkedIn ejecutándose en minutos.

> **🔗 Uso rápido:** Ve a [GUIA_USO_SEMANAL.md](./GUIA_USO_SEMANAL.md) para instrucciones paso a paso

## 🚀 Características

### 📰 **Fuentes de Noticias Múltiples**
- **🔍 Google News**: Noticias más actuales y relevantes (104 resultados por búsqueda)
- **📰 The Guardian API**: Periodismo de alta calidad
- **📺 BBC RSS**: Noticias internacionales confiables
- **🌐 NewsAPI**: Amplia cobertura de fuentes globales

### 🤖 **Generación Inteligente con IA**
- **Groq LLaMA 3.1-8b**: Modelo optimizado y rápido
- **OpenAI GPT**: Compatible con modelos de OpenAI
- **Personalización avanzada**: Diferentes estilos, tonos y longitudes de posts
- **Interfaz intuitiva**: Diseño limpio y fácil de usar
- **Edición en tiempo real**: Modifica el contenido generado antes de publicar
- **Exportación**: Descarga o copia el contenido generado

## 📋 Requisitos

- Python 3.8+
- API Keys para:
  - [NewsAPI](https://newsapi.org/) (gratis hasta 1000 requests/mes)
  - [The Guardian](https://open-platform.theguardian.com/) (gratis)
  - [OpenAI](https://platform.openai.com/) o [Groq](https://console.groq.com/) para el LLM

## 🛠️ Instalación

1. Clona o descarga este repositorio
2. Navega al directorio del proyecto
3. Activa tu entorno virtual (si tienes uno)
4. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## ⚙️ Configuración

### Opción 1: Variables de entorno
1. Copia `.env.example` a `.env`
2. Completa tus API keys en el archivo `.env`

### Opción 2: Configuración en la aplicación
- Ingresa las API keys directamente en el sidebar de la aplicación

## 🚀 Uso

1. Ejecuta la aplicación:
```bash
streamlit run app.py
```

2. Abre tu navegador en `http://localhost:8501`

3. Configura tus API keys en el sidebar

4. Selecciona:
   - Fuente de noticias (NewsAPI, The Guardian, o ambas)
   - Categoría/sección de noticias
   - Proveedor de LLM (OpenAI o Groq)
   - Estilo y tono del contenido

5. Haz clic en "Obtener Noticias"

6. Selecciona una noticia y genera tu post de LinkedIn

## 📊 APIs Utilizadas

### NewsAPI
- **Ventajas**: Amplia cobertura internacional, múltiples categorías
- **Límites**: 1000 requests gratis/mes
- **Categorías**: General, Business, Technology, Science, Health, Sports, Entertainment

### The Guardian API
- **Ventajas**: Contenido de alta calidad, sin límites estrictos
- **Límites**: 12 requests por segundo, 5000 por día (gratis)
- **Secciones**: World, Business, Technology, Science, Environment, Sport, Culture

## 🤖 LLMs Compatibles

### OpenAI (GPT-3.5-turbo)
- **Modelo**: gpt-3.5-turbo
- **Ventajas**: Resultados consistentes y de alta calidad
- **Costo**: Por tokens consumidos

### Groq (LLaMA 3 70B)
- **Modelo**: llama3-70b-8192
- **Ventajas**: Procesamiento muy rápido
- **Costo**: Más económico que OpenAI

## 🎨 Personalización

### Estilos Disponibles
- **Profesional**: Lenguaje formal y corporativo
- **Informal**: Tono casual y cercano
- **Académico**: Enfoque analítico y detallado
- **Persuasivo**: Orientado a la acción
- **Informativo**: Centrado en datos y hechos
- **Inspiracional**: Motivacional y positivo

### Tonos
- Neutral, Entusiasta, Reflexivo, Urgente, Optimista, Analítico

### Longitudes
- Corto (100-200 palabras)
- Medio (200-300 palabras) 
- Largo (300-500 palabras)

## 📝 Ejemplo de Uso

1. **Configuración inicial**: Ingresa tu API key de NewsAPI y OpenAI
2. **Selección**: Elige "Technology" como categoría
3. **Personalización**: Estilo "Profesional", Tono "Entusiasta", Longitud "Medio"
4. **Generación**: La app creará un post optimizado para LinkedIn con hashtags relevantes
5. **Edición**: Modifica el contenido si es necesario
6. **Exportación**: Copia o descarga el resultado final

## 🔧 Estructura del Proyecto

```
📁 publicaciones-linkedin/
├── 📄 app.py                 # Aplicación principal
├── 📄 requirements.txt       # Dependencias
├── 📄 .env.example          # Plantilla de configuración
├── 📄 README.md             # Esta documentación
└── 📁 .venv/                # Entorno virtual (si aplica)
```

## 🛡️ Seguridad

- Las API keys se manejan de forma segura
- No se almacenan credenciales en el código
- Uso de variables de entorno recomendado

## 📈 Características Avanzadas

- **Cache inteligente**: Las noticias se cachean por 1 hora para optimizar requests
- **Manejo de errores**: Gestión robusta de errores de API
- **Interfaz responsive**: Funciona en desktop y móvil
- **Múltiples fuentes**: Combina noticias de diferentes APIs

## 🔄 Actualizaciones Futuras

- [ ] Integración con más fuentes de noticias
- [ ] Soporte para más LLMs (Anthropic Claude, etc.)
- [ ] Programación automática de posts
- [ ] Análisis de engagement
- [ ] Plantillas personalizadas
- [ ] Integración directa con LinkedIn API

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## � **Uso Semanal Recomendado**

### ⚡ **Rutina de 5-8 minutos por semana:**

📋 **Ve a [GUIA_USO_SEMANAL.md](./GUIA_USO_SEMANAL.md)** para instrucciones completas paso a paso.

**Comando rápido para iniciar:**
```powershell
cd "ruta/a/tu/proyecto"; .\.venv\Scripts\Activate.ps1; streamlit run app.py
```

### 🎯 **Temas Sugeridos por Día:**
- **🟦 Lunes**: Data Science
- **🟨 Miércoles**: Data Analysis  
- **🟩 Viernes**: Inteligencia Artificial

¡Con esta rutina tendrás contenido profesional para LinkedIn sin esfuerzo!

---

## �📞 Soporte

Si tienes algún problema o sugerencia, puedes:
- 📖 Consultar la [Guía de Uso Semanal](./GUIA_USO_SEMANAL.md)
- 🐛 Abrir un issue en el repositorio
- 💬 Contactar al desarrollador
- Contactar al desarrollador

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

**¡Feliz creación de contenido! 🚀📱**
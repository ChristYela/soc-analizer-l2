# 🛡️ SOC Analyzer - Analizador de Logs con IA

Sistema avanzado de análisis de logs de seguridad que utiliza Inteligencia Artificial para detectar indicadores de compromiso (IoCs), generar dashboards interactivos y crear reportes ejecutivos y técnicos automáticos.

## 📋 Descripción

Este proyecto fue desarrollado como parte del proyecto final del bootcamp de ciberseguridad. Simula el trabajo de un Analista SOC Nivel 2 en una consultora de ciberseguridad ubicada en Estocolmo, Suecia.

### Contexto
Una empresa cliente sufrió incidentes de seguridad y exportó sus logs en formato Excel. Tu misión es analizar estos logs, identificar qué happened, detectar IoCs y generar reportes para el cliente.

## ✨ Características

- 🤖 **Análisis con IA**: Utiliza OpenAI GPT-4 para analizar logs y detectar amenazas
- 📊 **Dashboard Interactivo**: Visualización de hallazgos con métricas de riesgo
- 📄 **Reportes PDF Automáticos**: Genera reportes ejecutivos y técnicos
- 🔍 **Detección de Amenazas**:
  - Fuerza bruta
  - Logins sospechosos
  - Actividad en horarios inusuales
  - Movimientos laterales
  - Comandos no autorizados
- 🎯 **Clasificación por Riesgo**: Bajo, Medio, Alto
- 📈 **Estadísticas Detalladas**: Métricas completas del análisis

## 🛠️ Tecnologías Utilizadas

- **Python 3.10+**
- **Streamlit**: Framework web para dashboards
- **Pandas**: Análisis y manipulación de datos
- **OpenAI API**: Inteligencia Artificial (GPT-4)
- **FPDF2**: Generación de PDFs
- **Plotly**: Visualizaciones (opcional)

## 📦 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/soc-analyzer.git
cd soc-analyzer

# 🎬 Guion del Video Demostrativo - SOC Analyzer

**Proyecto Final - Analista SOC Nivel 2**
**Duración estimada:** 5-7 minutos
**Herramienta recomendada:** SimpleScreenRecorder u OBS Studio en MX Linux

---

## 📋 Preparación antes de grabar

- [ ] Cerrar todas las aplicaciones innecesarias
- [ ] Desactivar notificaciones (WhatsApp, Telegram, correo)
- [ ] Abrir la terminal con el entorno virtual activado
- [ ] Tener el archivo Excel `SOC_L2_Logs_Ampliados_Multiples_Incidentes.xlsx` a la mano
- [ ] Tener el navegador abierto en `http://localhost:8501`
- [ ] Tener el repositorio de GitHub abierto en otra pestaña

---

## 🎥 GUION DETALLADO

### 🎬 [00:00 - 00:30] INTRODUCCIÓN

**[Acción: Mostrar escritorio de MX Linux con la terminal abierta]**

> "Hola, mi nombre es **[TU NOMBRE]** y soy Analista SOC Nivel 2.
>
> En este video les presento mi proyecto final del bootcamp de ciberseguridad: un sistema de análisis de logs con Inteligencia Artificial.
>
> El contexto es el siguiente: trabajo como analista en una consultora de ciberseguridad en Estocolmo, Suecia. Mi Tech Lead, Carlos, me asignó analizar los logs de un cliente que sufrió múltiples incidentes y me entregó un archivo Excel con más de 700 registros para identificar qué pasó, detectar indicadores de compromiso y generar reportes para el cliente."

---

### 🎬 [00:30 - 01:00] EXPLICACIÓN DEL PROYECTO

**[Acción: Mostrar la estructura de carpetas con `ls -la` o el explorador de archivos]**

> "Para resolver este reto, desarrollé una aplicación web en Python usando Streamlit, integrada con la API de Groq (modelo Llama 3.3 70B) como motor de IA.
>
> La aplicación tiene cuatro módulos principales:
>
> - `app.py`: La interfaz web con el dashboard interactivo
> - `ai_analyzer.py`: El módulo que se comunica con la IA y construye el prompt
> - `pdf_generator.py`: Genera los reportes ejecutivos y técnicos en PDF usando ReportLab
> - `utils.py`: Funciones auxiliares para detección por reglas como fuerza bruta y horarios inusuales
>
> Todo el código está documentado en mi repositorio de GitHub, que mostraré al final."

---

### 🎬 [01:00 - 01:30] DEMOSTRACIÓN - CARGA DEL EXCEL

**[Acción: Ejecutar `streamlit run app.py` y mostrar la app cargando en el navegador]**

> "Vamos a poner en marcha la aplicación.
>
> Como pueden ver, la interfaz es moderna e intuitiva, con un sidebar informativo y un diseño profesional.
>
> Ahora voy a cargar el archivo Excel oficial con los logs del cliente: `SOC_L2_Logs_Ampliados_Multiples_Incidentes.xlsx`."

**[Acción: Subir el archivo Excel]**

> "Perfecto. La aplicación cargó exitosamente 715 registros. Puedo ver una vista previa de los datos con columnas como Timestamp, Source_IP, Destination, Event_Description, User, Severity, entre otras."

---

### 🎬 [01:30 - 02:30] ANÁLISIS CON IA

**[Acción: Hacer clic en "🚀 Iniciar Análisis con IA"]**

> "Ahora viene la parte más importante: el análisis con Inteligencia Artificial.
>
> Al hacer clic en 'Iniciar Análisis con IA', la aplicación hace dos cosas:
>
> Primero, ejecuta un pre-análisis por reglas para detectar patrones obvios como fuerza bruta o actividad nocturna.
>
> Segundo, envía una muestra compacta de los logs a la IA, que actúa como un analista senior y busca indicadores de compromiso más sofisticados: movimientos laterales, exfiltración de datos, persistencia, anti-forensis, etc.
>
> Cada hallazgo es clasificado automáticamente por nivel de riesgo: alto, medio o bajo."

**[Acción: Esperar a que termine el análisis - mostrar el spinner]**

---

### 🎬 [02:30 - 04:00] DASHBOARD DE RESULTADOS

**[Acción: Mostrar el dashboard completo, hacer scroll para ver todos los hallazgos]**

> "El análisis ha terminado. Veamos los resultados en el dashboard.
>
> **Métricas principales:**
> - Detectamos 6 hallazgos de riesgo ALTO 🔴
> - 3 hallazgos de riesgo MEDIO 🟡
> - 2 hallazgos de riesgo BAJO 🟢
>
> **Resumen ejecutivo:**
> La IA identificó un incidente crítico de múltiples vectores. Un atacante externo desde la IP 203.0.113.74 realizó password spraying contra el controlador de dominio, y otra IP externa realizó múltiples intentos fallidos de inicio de sesión, lo que representa un riesgo alto y requiere acción inmediata.
>
> **Hallazgos críticos detectados:**
>
> 🔴 **ALTO - Fuerza bruta:**
> Múltiples intentos fallidos de inicio de sesión desde IPs externas, lo que sugiere un ataque coordinado.
>
> 🟡 **MEDIO - Login sospechoso:**
> Inicios de sesión desde ubicaciones o horarios inusuales que requieren investigación.
>
> 🟡 **MEDIO - Movimiento lateral:**
> Acceso a recursos compartidos entre servidores, posible enumeración de red.
>
> 🟢 **BAJO - Exfiltración y persistencia:**
> Actividades que requieren monitoreo continuo pero no son críticas de inmediato."

---

### 🎬 [04:00 - 05:00] GENERACIÓN DE PDFs

**[Acción: Hacer clic en los botones de generar PDF]**

> "Una vez completado el análisis, la aplicación genera automáticamente dos reportes en PDF usando ReportLab:
>
> **1. Reporte Ejecutivo:**
> Diseñado para gerencia y personal no técnico. Incluye un resumen del impacto en el negocio, hallazgos simplificados y recomendaciones estratégicas.
>
> **2. Reporte Técnico:**
> Diseñado para el equipo de TI y SOC. Incluye análisis detallado con tecnicismos, IoCs específicos, estadísticas y recomendaciones técnicas de remediación.
>
> Ambos PDFs están formateados profesionalmente con colores según el nivel de riesgo, tablas de IoCs y secciones claramente diferenciadas."

**[Acción: Descargar ambos PDFs y abrirlos brevemente para mostrar el contenido]**

> "Como pueden ver, con un solo clic tenemos reportes profesionales listos para entregar al cliente."

---

### 🎬 [05:00 - 05:45] REPOSITORIO DE GITHUB

**[Acción: Abrir el navegador y mostrar el repo de GitHub]**

> "Todo el código, los PDFs generados y la documentación están disponibles en mi repositorio de GitHub.
>
> El README incluye:
> - Descripción completa del proyecto
> - Stack tecnológico utilizado
> - Instrucciones detalladas de instalación
> - Formato esperado del archivo Excel
> - Ejemplos de los reportes generados
> - Link a este video demostrativo
>
> El repositorio está bien documentado y cualquiera puede replicarlo siguiendo los pasos. Además, el archivo `.env` está correctamente excluido del repositorio para proteger las API keys."

---

### 🎬 [05:45 - 06:15] CIERRE

**[Acción: Volver a la pantalla principal de la app]**

> "En resumen, este proyecto demuestra mis habilidades como Analista SOC Nivel 2 en:
>
> ✅ Análisis de logs y detección de IoCs
> ✅ Investigación y research técnico
> ✅ Programación en Python con Streamlit
> ✅ Integración de APIs de Inteligencia Artificial (Groq/OpenAI)
> ✅ Generación automatizada de reportes profesionales en PDF
> ✅ Comunicación técnica y ejecutiva
> ✅ Control de versiones con Git y GitHub
> ✅ Desarrollo en entorno Linux (MX Linux XFCE)
>
> Este es exactamente el tipo de solución que implementaría en un SOC real para acelerar el análisis de incidentes y entregar reportes de calidad al cliente en minutos, no en horas.
>
> Muchas gracias por su tiempo. El repositorio está disponible en:
> **https://github.com/TU_USUARIO/soc-analyzer-l2**"

---

## 💡 Consejos para la grabación

### Antes de grabar:
1. Practica el guion 2-3 veces en voz alta
2. Si te equivocas, **no detengas la grabación**, sigue y córtalo en edición
3. Habla claro y pausado
4. Usa zoom del navegador (`Ctrl + +`) para que el código se vea mejor

### Durante la grabación:
- Mueve el mouse con propósito, no nerviosamente
- Haz pausas breves entre secciones para facilitar la edición
- Si usas Kdenlive u OpenShot, puedes agregar títulos al inicio y final

### Herramientas recomendadas en MX Linux:
```bash
# Grabación de pantalla
sudo apt install simplescreenrecorder

# Edición de video
sudo apt install openshot-qt  # Más simple
sudo apt install kdenlive     # Más profesional

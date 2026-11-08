"""
Módulo para generar reportes en PDF usando ReportLab
Solución robusta que maneja perfectamente español y caracteres especiales
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
from typing import Dict, List
import os
import re

def limpiar_texto(texto: str) -> str:
    """Limpia emojis y caracteres especiales"""
    if not texto:
        return ""
    
    # Reemplazar emojis por texto plano
    reemplazos = {
        '🔴': '[ALTO]', '🟡': '[MEDIO]', '🟢': '[BAJO]',
        '✅': '[OK]', '❌': '[ERROR]', '⚠️': '[ADVERTENCIA]',
        '📊': '[ESTADISTICAS]', '🎯': '[HALLAZGOS]', '📄': '[DOCUMENTO]',
        '📋': '[RESUMEN]', '🛡️': '[SEGURIDAD]', '⏱️': '[TIEMPO]',
        '🛠️': '[HERRAMIENTAS]', '💡': '[NOTA]', '📌': '[NOTA]'
    }
    for emoji, texto_plano in reemplazos.items():
        texto = texto.replace(emoji, texto_plano)
    
    return texto

def generar_pdf_ejecutivo(resultado: Dict, ruta_salida: str) -> str:
    """Genera el PDF del resumen ejecutivo usando ReportLab"""
    
    # Crear documento
    doc = SimpleDocTemplate(
        ruta_salida,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # Estilos
    styles = getSampleStyleSheet()
    
    titulo_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=HexColor('#003366'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitulo_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=HexColor('#003366'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )
    
    texto_style = ParagraphStyle(
        'CustomText',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=8
    )
    
    # Construir contenido
    story = []
    
    # Título principal
    story.append(Paragraph("REPORTE SOC - EJECUTIVO", titulo_style))
    story.append(Spacer(1, 0.3*cm))
    
    # Información del reporte
    fecha_texto = f"<b>Fecha de generación:</b> {datetime.now().strftime('%d de %B de %Y')}<br/>"
    fecha_texto += "<b>Clasificación:</b> CONFIDENCIAL<br/>"
    fecha_texto += "<b>Elaborado por:</b> Analista SOC Nivel 2"
    story.append(Paragraph(fecha_texto, texto_style))
    story.append(Spacer(1, 0.5*cm))
    
    # Resumen Ejecutivo
    story.append(Paragraph("RESUMEN EJECUTIVO", subtitulo_style))
    resumen = limpiar_texto(resultado.get('resumen_ejecutivo', 'No disponible'))
    story.append(Paragraph(resumen, texto_style))
    story.append(Spacer(1, 0.5*cm))
    
    # Estadísticas
    if resultado.get('estadisticas'):
        story.append(Paragraph("ESTADÍSTICAS GENERALES", subtitulo_style))
        stats = resultado['estadisticas']
        
        stats_texto = f"<b>Total de eventos analizados:</b> {stats.get('total_eventos', 'N/A')}<br/>"
        stats_texto += f"<b>Eventos sospechosos detectados:</b> {stats.get('eventos_sospechosos', 'N/A')}<br/>"
        stats_texto += f"<b>Direcciones IP únicas:</b> {stats.get('ips_unicas', 'N/A')}<br/>"
        stats_texto += f"<b>Período de análisis:</b> {limpiar_texto(str(stats.get('periodo_analisis', 'N/A')))}"
        
        story.append(Paragraph(stats_texto, texto_style))
        story.append(Spacer(1, 0.5*cm))
    
    # Resumen de hallazgos
    story.append(Paragraph("RESUMEN DE HALLAZGOS", subtitulo_style))
    hallazgos = resultado.get('hallazgos', [])
    
    alto = sum(1 for h in hallazgos if h.get('riesgo', '').lower() == 'alto')
    medio = sum(1 for h in hallazgos if h.get('riesgo', '').lower() == 'medio')
    bajo = sum(1 for h in hallazgos if h.get('riesgo', '').lower() == 'bajo')
    
    hallazgos_texto = f"<b>Riesgo ALTO:</b> {alto} hallazgos<br/>"
    hallazgos_texto += f"<b>Riesgo MEDIO:</b> {medio} hallazgos<br/>"
    hallazgos_texto += f"<b>Riesgo BAJO:</b> {bajo} hallazgos"
    
    story.append(Paragraph(hallazgos_texto, texto_style))
    story.append(Spacer(1, 0.5*cm))
    
    # Recomendaciones
    story.append(Paragraph("RECOMENDACIONES PRINCIPALES", subtitulo_style))
    
    recomendaciones = []
    for h in hallazgos:
        if h.get('recomendacion') and h.get('riesgo', '').lower() in ['alto', 'medio']:
            recomendaciones.append(f"• {limpiar_texto(h['recomendacion'])}")
    
    if recomendaciones:
        reco_texto = "<br/>".join(recomendaciones[:10])
        story.append(Paragraph(reco_texto, texto_style))
    else:
        story.append(Paragraph("No hay recomendaciones críticas en este momento.", texto_style))
    
    # Generar PDF
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    doc.build(story)
    
    return ruta_salida


def generar_pdf_tecnico(resultado: Dict, ruta_salida: str) -> str:
    """Genera el PDF del resumen técnico detallado usando ReportLab"""
    
    # Crear documento
    doc = SimpleDocTemplate(
        ruta_salida,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # Estilos
    styles = getSampleStyleSheet()
    
    titulo_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=HexColor('#003366'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitulo_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=HexColor('#003366'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )
    
    texto_style = ParagraphStyle(
        'CustomText',
        parent=styles['Normal'],
        fontSize=10,
        leading=13,
        alignment=TA_JUSTIFY,
        spaceAfter=6
    )
    
    hallazgo_titulo_style = ParagraphStyle(
        'HallazgoTitulo',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        fontName='Helvetica-Bold',
        spaceAfter=4,
        spaceBefore=8
    )
    
    # Construir contenido
    story = []
    
    # Título principal
    story.append(Paragraph("REPORTE SOC - TÉCNICO DETALLADO", titulo_style))
    story.append(Spacer(1, 0.3*cm))
    
    # Información del reporte
    fecha_texto = f"<b>Fecha de generación:</b> {datetime.now().strftime('%d de %B de %Y')}<br/>"
    fecha_texto += "<b>Clasificación:</b> RESTRINGIDO<br/>"
    fecha_texto += "<b>Elaborado por:</b> Analista SOC Nivel 2"
    story.append(Paragraph(fecha_texto, texto_style))
    story.append(Spacer(1, 0.5*cm))
    
    # Resumen Técnico
    story.append(Paragraph("RESUMEN TÉCNICO DETALLADO", subtitulo_style))
    resumen = limpiar_texto(resultado.get('resumen_tecnico', 'No disponible'))
    story.append(Paragraph(resumen, texto_style))
    story.append(Spacer(1, 0.5*cm))
    
    # Estadísticas
    if resultado.get('estadisticas'):
        story.append(Paragraph("ESTADÍSTICAS TÉCNICAS", subtitulo_style))
        stats = resultado['estadisticas']
        
        for key, value in stats.items():
            clave_limpia = key.replace('_', ' ').title()
            valor_limpio = limpiar_texto(str(value))
            story.append(Paragraph(f"<b>{clave_limpia}:</b> {valor_limpio}", texto_style))
        
        story.append(Spacer(1, 0.5*cm))
    
    # Hallazgos detallados
    story.append(Paragraph("HALLAZGOS DETALLADOS", subtitulo_style))
    hallazgos = resultado.get('hallazgos', [])
    
    if hallazgos:
        # Ordenar por severidad
        hallazgos_ordenados = sorted(
            hallazgos,
            key=lambda x: {'alto': 0, 'medio': 1, 'bajo': 2}.get(x.get('riesgo', '').lower(), 3)
        )
        
        for hallazgo in hallazgos_ordenados:
            riesgo = hallazgo.get('riesgo', 'medio').lower()
            tipo = limpiar_texto(hallazgo.get('tipo', 'Sin categoría'))
            
            # Título del hallazgo con color según riesgo
            if riesgo == 'alto':
                color = '#FF0000'
            elif riesgo == 'medio':
                color = '#FFA500'
            else:
                color = '#00AA00'
            
            titulo_hallazgo = f'<font color="{color}">[{riesgo.upper()}]</font> {tipo}'
            story.append(Paragraph(titulo_hallazgo, hallazgo_titulo_style))
            
            # Descripción
            descripcion = limpiar_texto(hallazgo.get('descripcion', 'N/A'))
            story.append(Paragraph(f"<b>Descripción:</b> {descripcion}", texto_style))
            
            # Evidencia
            if hallazgo.get('evidencia'):
                evidencia = limpiar_texto(hallazgo.get('evidencia', 'N/A'))
                story.append(Paragraph(f"<b>Evidencia:</b> {evidencia}", texto_style))
            
            # Recomendación
            if hallazgo.get('recomendacion'):
                recomendacion = limpiar_texto(hallazgo.get('recomendacion', 'N/A'))
                story.append(Paragraph(f"<b>Recomendación:</b> {recomendacion}", texto_style))
            
            story.append(Spacer(1, 0.3*cm))
    else:
        story.append(Paragraph("No se detectaron hallazgos en el análisis.", texto_style))
    
    # Nueva página para IoCs
    story.append(PageBreak())
    
    # Indicadores de Compromiso
    story.append(Paragraph("INDICADORES DE COMPROMISO (IoCs)", subtitulo_style))
    
    ips_sospechosas = set()
    for h in hallazgos:
        evidencia = limpiar_texto(h.get('evidencia', ''))
        ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', evidencia)
        ips_sospechosas.update(ips)
    
    if ips_sospechosas:
        story.append(Paragraph("<b>Direcciones IP sospechosas detectadas:</b>", texto_style))
        for ip in sorted(ips_sospechosas):
            story.append(Paragraph(f"  • {ip}", texto_style))
    else:
        story.append(Paragraph("No se identificaron IoCs específicos en este análisis.", texto_style))
    
    # Generar PDF
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    doc.build(story)
    
    return ruta_salida

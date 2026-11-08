"""
Módulo de utilidades para el SOC Analyzer
"""
import pandas as pd
import re
from typing import List, Dict

def validar_excel(df: pd.DataFrame) -> tuple[bool, str]:
    """
    Valida que el DataFrame tenga las columnas necesarias para análisis de logs
    """
    columnas_requeridas = ['Timestamp', 'Source_IP', 'Destination', 'Event_Description']
    columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]
    
    if columnas_faltantes:
        return False, f"Faltan columnas requeridas: {', '.join(columnas_faltantes)}"
    
    if len(df) == 0:
        return False, "El archivo está vacío"
    
    return True, "Validación exitosa"

def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia y prepara los datos para el análisis
    """
    # Convertir Timestamp a datetime si es string
    if 'Timestamp' in df.columns:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    
    # Eliminar filas completamente vacías
    df = df.dropna(how='all')
    
    # Eliminar duplicados
    df = df.drop_duplicates()
    
    return df

def extraer_ips_sospechosas(df: pd.DataFrame) -> List[str]:
    """
    Extrae IPs que aparecen en múltiples eventos sospechosos
    """
    if 'Source_IP' not in df.columns:
        return []
    
    # Contar eventos por IP
    ip_counts = df['Source_IP'].value_counts()
    
    # IPs con más de 10 eventos (potencialmente sospechosas)
    ips_sospechosas = ip_counts[ip_counts > 10].index.tolist()
    
    return ips_sospechosas[:10]  # Top 10

def detectar_fuerza_bruta(df: pd.DataFrame, umbral: int = 5) -> List[Dict]:
    """
    Detecta intentos de fuerza bruta basados en múltiples logins fallidos
    """
    hallazgos = []
    
    if 'Event_Description' not in df.columns or 'Source_IP' not in df.columns:
        return hallazgos
    
    # Filtrar eventos de login fallido
    logins_fallidos = df[df['Event_Description'].str.contains('failed to log on|bad password', case=False, na=False)]
    
    if len(logins_fallidos) == 0:
        return hallazgos
    
    # Agrupar por IP y contar
    ip_counts = logins_fallidos.groupby('Source_IP').size()
    
    # IPs con más intentos que el umbral
    ips_atacante = ip_counts[ip_counts > umbral]
    
    for ip, count in ips_atacante.items():
        hallazgos.append({
            'tipo': 'fuerza_bruta',
            'ip': ip,
            'intentos': count,
            'descripcion': f'IP {ip} realizó {count} intentos de login fallidos'
        })
    
    return hallazgos

def detectar_horarios_inusuales(df: pd.DataFrame) -> List[Dict]:
    """
    Detecta actividades en horarios inusuales (ej: 2 AM - 5 AM)
    """
    hallazgos = []
    
    if 'Timestamp' not in df.columns:
        return hallazgos
    
    # Convertir a datetime si no lo está
    df_temp = df.copy()
    df_temp['Timestamp'] = pd.to_datetime(df_temp['Timestamp'], errors='coerce')
    
    # Extraer hora
    df_temp['hora'] = df_temp['Timestamp'].dt.hour
    
    # Filtrar eventos entre 1 AM y 5 AM
    eventos_nocturnos = df_temp[(df_temp['hora'] >= 1) & (df_temp['hora'] <= 5)]
    
    if len(eventos_nocturnos) > 0:
        # Agrupar por IP
        ips_nocturnas = eventos_nocturnos['Source_IP'].value_counts().head(5)
        
        for ip, count in ips_nocturnas.items():
            hallazgos.append({
                'tipo': 'actividad_nocturna',
                'ip': ip,
                'eventos': count,
                'descripcion': f'IP {ip} realizó {count} eventos entre 1 AM y 5 AM'
            })
    
    return hallazgos

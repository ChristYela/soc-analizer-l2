"""
Módulo de análisis con Inteligencia Artificial (Optimizado para límites de tokens)
"""
import os
import json
import pandas as pd
from dotenv import load_dotenv
from typing import Dict, List
import streamlit as st

load_dotenv()

class SOCAnalyzerAI:
    def __init__(self):
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
        if self.groq_api_key:
            from groq import Groq
            self.client = Groq(api_key=self.groq_api_key)
            self.model = "openai/gpt-oss-120b"
            self.provider = "Groq"
        elif self.openai_api_key:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.openai_api_key)
            self.model = "gpt-4o-mini"
            self.provider = "OpenAI"
        else:
            raise ValueError("No se encontró GROQ_API_KEY ni OPENAI_API_KEY en .env")

    def analizar_logs(self, df: pd.DataFrame, hallazgos_previos: List[Dict] = None) -> Dict:
        # 1. CREAR RESUMEN COMPACTO (Para no exceder 8000 tokens)
        total_registros = len(df)
        
        # Top 5 eventos más frecuentes
        top_eventos = df['Event_Description'].value_counts().head(5).to_dict()
        
        # Top 5 IPs de origen con más eventos
        top_ips = df['Source_IP'].value_counts().head(5).to_dict()
        
        # Filtrar solo eventos de severidad Media o Alta para la muestra
        df_sospechoso = df[df['Severity'].isin(['Medium', 'High', 'Warning'])]
        muestra_pequena = df_sospechoso.head(15).to_dict(orient='records')
        
        contexto_hallazgos = ""
        if hallazgos_previos:
            contexto_hallazgos = f"Hallazgos por reglas: {json.dumps(hallazgos_previos, indent=2, default=str)}"

        # 2. CONSTRUIR PROMPT ULTRA-COMPACTO
        prompt = f"""
Eres un analista SOC experto. Analiza este RESUMEN de logs de seguridad.

ESTADÍSTICAS:
- Total registros: {total_registros}
- Top Eventos: {json.dumps(top_eventos)}
- Top IPs Origen: {json.dumps(top_ips)}

MUESTRA DE EVENTOS SOSPECHOSOS (Max 15):
{json.dumps(muestra_pequena, indent=2, default=str)}

{contexto_hallazgos}

INSTRUCCIONES:
1. Detecta: fuerza bruta, logins sospechosos, movimientos laterales, exfiltración, persistencia.
2. Clasifica riesgo: BAJO, MEDIO, ALTO.
3. Genera resumen ejecutivo (para gerentes) y técnico (para analistas).

FORMATO DE RESPUESTA (JSON estricto):
{{
    "hallazgos": [
        {{
            "tipo": "categoria",
            "descripcion": "descripcion clara",
            "riesgo": "bajo|medio|alto",
            "evidencia": "detalle especifico (IP, evento, usuario)",
            "recomendacion": "accion a tomar"
        }}
    ],
    "resumen_ejecutivo": "texto para gerentes (2-3 párrafos)",
    "resumen_tecnico": "texto para analistas con Kill Chain (2-3 párrafos)",
    "estadisticas": {{
        "total_eventos": {total_registros},
        "eventos_sospechosos": {len(df_sospechoso)},
        "ips_unicas": {df['Source_IP'].nunique()},
        "periodo_analisis": "{str(df['Timestamp'].min())} a {str(df['Timestamp'].max())}"
    }}
}}
Responde SOLO con JSON válido.
"""
        try:
            if self.provider == "Groq":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "Eres un analista SOC experto. Responde SOLO con JSON válido."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                    max_tokens=3000,
                    response_format={"type": "json_object"}
                )
                resultado_texto = response.choices[0].message.content
            else:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "Eres un analista SOC experto. Responde SOLO con JSON válido."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.2,
                    max_tokens=3000
                )
                resultado_texto = response.choices[0].message.content
            
            return json.loads(resultado_texto)
            
        except Exception as e:
            st.error(f"Error IA: {str(e)}")
            raise e  # Esto activará el Modo Demo en app.py

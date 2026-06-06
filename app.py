import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de página
st.set_page_config(page_title="Test Vocacional CIP-R", layout="centered")

archivo_excel = "Test CIP-R 4to Medio 2026 (1).xlsx"

# Diccionario oficial de tributación de carreras por área CIP-R
DICCIONARIO_CARRERAS = {
    "Arte y Arquitectura": "Arquitectura, Diseño Gráfico, Diseño Industrial, Artes Visuales, Teatro, Música, Cine y Animación Digital.",
    "Ciencias Exactas y Naturales": "Licenciatura en Matemáticas, Física, Química, Astronomía, Geología, Estadística y Ciencias de de Datos.",
    "Ingeniería y Tecnología": "Ingeniería Civil (Industrial, Informática, Mecánica, Minas, Eléctrica), Ingeniería en Construcción y Telecomunicaciones.",
    "Ciencias Biológicas y de la Salud": "Medicina, Enfermería, Kinesiología, Psicología, Odontología, Medicina Veterinaria, Biología Marina y Biotecnología.",
    "Ciencias Sociales": "Sociología, Antropología, Trabajo Social, Ciencia Política, Psicología Social, Geografía e Historia.",
    "Humanidades y Letras": "Literatura, Filosofía, Traducción e Interpretación, Periodismo, Licenciatura en Historia y Arqueología.",
    "Administración, Economía y Comercio": "Ingeniería Comercial, Auditoría, Contador Público, Administración de Empresas, Comercio Exterior y Marketing.",
    "Derecho y Ciencias Jurídicas": "Derecho (Abogacía), Ciencias Policiales, Administración Pública, Consultoría Legal y Criminalística.",
    "Educación y Pedagogía": "Pedagogía en Educación Básica, Educación Parvularia, Pedagogía en Media (Inglés, Matemáticas, Historia), Educación Diferencial.",
    "Medios de Comunicación": "Periodismo, Comunicación Audiovisual, Publicidad, Relaciones Públicas, Locución y Gestión de Medios Digitales.",
    "Producción Gráfica e Imagen": "Diseño Editorial, Animación 2D/3D, Fotografía Profesional, Edición de Video, Diseño Web e Impresión Digital.",
    "Turismo, Hotelería y Gastronomía": "Administración de Empresas Turísticas, Gastronomía Internacional, Hotelería, Ecoturismo y Gestión de Eventos.",
    "Actividad Física y Deporte": "Pedagogía en Educación Física, Técnico en Deportes, Kinesiología Deportiva, Personal Trainer y Gestión Deportiva.",
    "Defensa y Seguridad": "Carreras Oficiales/Suboficiales en Fuerzas Armadas (Ejército, Armada, Fuerza Aérea), Carabineros de Chile y PDI."
}

@st.cache_data
def cargar_banco_preguntas():
    try:
        df = pd.read_excel(archivo_excel, sheet_name="Preguntas")
        df["Pregunta"] = df["Pregunta"].astype(str).str.strip()
        df["Area"] = df["Area"].astype(str).str.strip()
        return df
    except Exception as e:
        st.error(f"Error al cargar las preguntas del Excel: {e}")
        return None

df_preguntas = cargar_banco_preguntas()

def generar_html_reporte(nombre, apellido, rut, top_df):
    filas_tabla = ""
    for idx, row in enumerate(top_df.itertuples(), 1):
        carreras = DICCIONARIO_CARRERAS.get(row._1, "Carreras variadas del área.")
        filas_tabla += f"""
        <tr>
            <td style='padding: 12px; border: 1px solid #ddd; text-align: center; font-weight: bold;'>{idx}°</td>
            <td style='padding: 12px; border: 1px solid #ddd;'>
                <strong style='color:#1f77b4;'>{row._1}</strong><br>
                <span style='font-size: 12px; color: #555;'>Ocupaciones: {carreras}</span>
            </td>
            <td style='padding: 12px; border: 1px solid #ddd; text-align: center; color: #2e7d32; font-weight: bold;'>{row.Puntaje} pts</td>
        </tr>
        """
        
    html_content = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Arial', sans-serif; color: #333; margin: 40px; line-height: 1.5; }}
            .header {{ text-align: center; border-bottom: 3px solid #1f77b4; padding-bottom: 10px; }}
            .info {{ margin: 20px 0; padding: 15px; background-color: #f9f9f9; border-radius: 5px; border-left: 5px solid #1f77b4; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th {{ background-color: #1f77b4; color: white; padding: 12px; border: 1px solid #ddd; }}
            .footer {{ margin-top: 50px; text-align: center; font-size: 11px; color: #777; border-top: 1px solid #ddd; padding-top: 10px; }}
        </style>
    </head>
    <body>
        <div class='header'>
            <h2>RESULTADOS DIAGNÓSTICO VOCACIONAL CIP-R</h2>
            <p>Programa PACE</p>
        </div>
        <div class='info'>
            <p style='margin: 4px 0;'><strong>Estudiante:</strong> {nombre} {apellido}</p>
            <p style='margin: 4px 0;'><strong>RUT:</strong> {rut}</p>
        </div>
        <h3>🏆 Tus Principales Áreas de Interés Profesional</h3>
        <table>
            <thead>
                <tr>
                    <th style='width: 10%;'>Lugar</th>
                    <th>Área Vocacional y Carreras Afines</th>
                    <th style='width: 20%;'>Puntaje</th>
                </tr>
            </thead>
            <tbody>
                {filas_tabla}
            </tbody>
        </table>
        <div class='footer'>
            <p>Reporte generado automáticamente por la plataforma de orientación vocacional.</p>
        </div>
    </body>
    </html>
    """
    return html_content

if df_preguntas is not None:
    st.title("📋 Test de Intereses Profesionales CIP-R")
    st.markdown("Bienvenido/a. Responde con total sinceridad indicando tu nivel de agrado por cada actividad.")
    st.write("---")

    if "enviado" not in st.session_state:
        st.session_state.enviado = False

    # FASE 1: COMPLETAR EL TEST
    if not st.session_state.enviado:
        st.subheader("👤 I. Datos Personales")
        col1, col2 = st.columns(2)
        with col1:
            nombres = st.text_input("Nombres:", placeholder="Ej: Juan Andrés")
            apellido_p = st.text_input("Primer Apellido:", placeholder="Ej: Pérez")
        with col2:
            rut = st.text_input("RUT (Sin puntos y con guión):", placeholder="Ej: 12345678-9")

        st.write("---")
        st.subheader("🎯 II. Cuestionario de Intereses")
        st.info("Selecciona una opción para cada una de las siguientes actividades:")

        respuestas_estudiante = {}
        for idx, fila in df_preguntas.iterrows():
            num = fila["Numero"]
            texto_pregunta = fila["Pregunta"]
            texto_mostrar = texto_pregunta.replace("[", "").replace("]", "")
            
            opcion = st.radio(
                f"Pregunta {num}: {texto_mostrar}",
                ["Agrado", "Indiferencia", "Desagrado"],
                index=1,
                key=f"preg_{num}",
                horizontal=True
            )
            
            respuestas_estudiante[texto_pregunta] = {
                "area": fila["Area"],
                "puntaje": 2 if opcion == "Agrado" else (1 if opcion == "Indiferencia" else 0)
            }
            st.markdown("<div style='margin-bottom: 18px;'></div>", unsafe_allow_html=True)

        st.write("---")
        if st.button("🚀 Finalizar Test y Ver Resultados", type="primary"):
            if not nombres or not apellido_p or not rut:
                st.error("⚠️ Por favor, completa tus datos personales antes de enviar.")
            else:
                st.session_state.nombres_alumno = nombres
                st.session_state.apellido_alumno = apellido_p
                st.session_state.rut_alumno = rut
                
                puntajes_por_area = {}
                for preg, datos in respuestas_estudiante.items():
                    area = datos["area"]
                    puntajes_por_area[area] = puntajes_por_area.get(area, 0) + datos["puntaje"]
                
                df_res = pd.DataFrame(list(puntajes_por_area.items()), columns=["Área Vocacional", "Puntaje"])
                st.session_state.df_resultados = df_res.sort_values(by="Puntaje", ascending=True)
                st.session_state.enviado = True
                st.rerun()

    # FASE 2: VER RESULTADOS E IMPRIMIR
    else:
        st.balloons()
        st.success(f"🎉 ¡Felicidades {st.session_state.nombres_alumno}! Tu test ha sido procesado con éxito.")
        st.write("---")
        
        st.subheader(f"📊 Perfil Vocacional de: {st.session_state.nombres_alumno} {st.session_state.apellido_alumno}")
        
        fig = px.bar(
            st.session_state.df_resultados, 
            x="Puntaje", 
            y="Área Vocacional", 
            orientation='h',
            color="Puntaje",
            color_continuous_scale="Viridis",
            labels={"Puntaje": "Preferencia Acumulada"}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("---")
        st.markdown("### 🏆 Tus Áreas de Mayor Interés:")
        
        top_3 = st.session_state.df_resultados.sort_values(by="Puntaje", ascending=False).head(3)
        
        # Tarjetas interactivas con la descripción de carreras añadidas abajo
        for i, row in enumerate(top_3.itertuples(), 1):
            carreras_afines = DICCIONARIO_CARRERAS.get(row._1, "Ocupaciones asociadas al desarrollo del área.")
            st.markdown(f"""
            <div style="background-color: #1e2630; padding: 18px; border-radius: 8px; margin-bottom: 14px; border-left: 5px solid #4ade80;">
                <span style="color: #4ade80; font-size: 16px; font-weight: bold; background: #14532d; padding: 2px 10px; border-radius: 12px; float: right;">{row.Puntaje} pts</span>
                <span style="color: #94a3b8; font-size: 12px; font-weight: bold; display: block;">TOP {i} INTERÉS</span>
                <span style="color: white; font-size: 20px; font-weight: bold; display: inline-block; margin-top: 4px; margin-bottom: 6px;">{row._1}</span>
                <p style="color: #cbd5e1; font-size: 14px; margin: 0; border-top: 1px solid #334155; padding-top: 6px;">
                    <strong>🎓 Carreras / Ocupaciones afines:</strong> {carreras_afines}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        st.write("---")
        
        # El reporte HTML descargable ahora también incluye el desglose de carreras
        html_reporte = generar_html_reporte(
            st.session_state.nombres_alumno, 
            st.session_state.apellido_alumno, 
            st.session_state.rut_alumno, 
            top_3
        )
        
        st.download_button(
            label="📥 Descargar Reporte de Resultados (HTML/Imprimir)",
            data=html_reporte,
            file_name=f"Resultado_CIPR_{st.session_state.apellido_alumno}.html",
            mime="text/html",
            use_container_width=True
        )
        
        st.caption("💡 Consejo: Al abrir el archivo descargado, puedes presionar Ctrl+P en tu teclado y seleccionar 'Guardar como PDF' para guardarlo de manera permanente con el desglose completo.")
        
        if st.button("🔄 Volver a realizar el Test", use_container_width=True):
            st.session_state.clear()
            st.rerun()
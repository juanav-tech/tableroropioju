import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import cv2
import random

# 1. Configuración de la página
st.set_page_config(
    page_title="¡Pequeños Artistas! 🎨✨",
    page_icon="🎨",
    layout="wide"
)

# 2. Frase motivadora al inicio
st.markdown("""
    <div style="background-color: #FFE66D; padding: 15px; border-radius: 15px; text-align: center; margin-bottom: 20px;">
        <h3 style="color: #2B2D42; margin:0;">🌈 "Todo niño es un artista. El secreto es mantener la magia cuando crecemos." — Pablo Picasso 🚀</h3>
    </div>
""", unsafe_allow_html=True)

st.title("🌟 ¡El Lienzo Mágico de las Historias! 🎨")
st.write("Dibuja lo que te imagines en el lienzo para calificar tu obra y descubrir un cuento genial.")

# 3. Barra Lateral Infantil
with st.sidebar:
    st.header("🛠️ Tu Caja de Colores")
    
    drawing_mode = st.selectbox(
        "Herramienta:",
        ("freedraw", "line", "rect", "circle"),
        format_func=lambda x: {
            "freedraw": "✏️ Lápiz Mágico",
            "line": "📏 Línea Recta",
            "rect": "⬛ Cuadrado",
            "circle": "🔴 Círculo"
        }.get(x, x)
    )
    
    stroke_width = st.slider('Grosor del pincel 🖌️', 2, 40, 12)
    stroke_color = st.color_picker("Color de la pintura 🎨", "#FF6B6B")
    bg_color = st.color_picker("Color de la hoja 📄", "#FFFFFF")
    
    st.divider()
    st.subheader("Tamaño de la Hoja")
    canvas_width = st.slider("Ancho", 300, 700, 500, 50)
    canvas_height = st.slider("Alto", 200, 500, 350, 50)

# 4. Interfaz Principal
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("🖼️ ¡Dibuja aquí tu obra de arte!")
    canvas_result = st_canvas(
        fill_color="rgba(255, 230, 109, 0.4)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        height=canvas_height,
        width=canvas_width,
        drawing_mode=drawing_mode,
        key=f"canvas_infantil_{canvas_width}_{canvas_height}",
    )
    
    generar_btn = st.button("🚀 ¡Analizar mi dibujo y contar historia!", type="primary", use_container_width=True)

# Banco de cuentos tradicionales predefinidos
HISTORIAS = [
    "Había una vez un pequeño trazo mágico que decidió explorar el mundo de papel. Con cada paso que daba, creaba puentes de colores y reinos donde los lápices podías volar hacia las estrellas.",
    "Un día, las formas del lienzo cobraron vida y organizaron una gran fiesta. El cuadrado trajo galletas, el círculo rodó bailando y las líneas hicieron música alegre hasta el anochecer.",
    "En un bosque lleno de colores brillantes, vivía un pequeño creador que con solo tocar la hoja daba forma a aventuras fantásticas. Cada dibujo era un mapa secreto hacia un tesoro lleno de alegría."
]

MEDALLAS = [
    "🏅 ¡Medalla al Gran Creador de Colores!",
    "🏆 ¡Trofeo al Maestro del Lápiz Mágico!",
    "⭐ ¡Premio Especial a la Creatividad Infinita!"
]

with col2:
    st.subheader("⭐ Resultado de tu Obra")
    
    if generar_btn:
        if canvas_result.image_data is not None:
            # Procesamiento con OpenCV para analizar trazados sin usar IA
            img_data = canvas_result.image_data
            img = Image.fromarray(img_data.astype('uint8'), 'RGBA').convert('RGB')
            img_np = np.array(img)
            
            # Convertir a escala de grises
            gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
            
            # Detección de trazos mediante umbralizado y contornos
            _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Cálculo del área dibujada
            pixeles_dibujados = np.sum(thresh > 0)
            total_pixeles = thresh.shape[0] * thresh.shape[1]
            porcentaje_cobertura = (pixeles_dibujados / total_pixeles) * 100
            
            if len(contours) > 0 and porcentaje_cobertura > 0.1:
                # Sistema de calificación lógica según el esfuerzo/cobertura
                if porcentaje_cobertura > 15:
                    estrellas = "⭐⭐⭐⭐⭐ / 5"
                elif porcentaje_cobertura > 5:
                    estrellas = "⭐⭐⭐⭐ / 5"
                else:
                    estrellas = "⭐⭐⭐ / 5"
                
                medalla = random.choice(MEDALLAS)
                historia = random.choice(HISTORIAS)
                
                st.balloons()
                st.success("¡Tu dibujo ha sido procesado con éxito!")
                
                st.markdown(f"### 🌟 Calificación: {estrellas}")
                st.markdown(f"### {medalla}")
                st.markdown("---")
                st.markdown(f"**🔍 Elementos detectados:** Se identificaron **{len(contours)}** trazos en el lienzo.")
                st.markdown("---")
                st.markdown("### 📖 Cuento del Lienzo:")
                st.write(historia)
            else:
                st.warning("¡El lienzo parece estar vacío! Haz un trazo antes de analizar.")
        else:
            st.warning("¡Primero haz un dibujo en el papel para empezar! 🎨")

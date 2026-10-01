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

# 2. Frase motivadora
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
    
    # Creamos el lienzo con una clave única fija
    canvas_result = st_canvas(
        fill_color="rgba(255, 230, 109, 0.4)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        height=canvas_height,
        width=canvas_width,
        drawing_mode=drawing_mode,
        key="canvas_infantil_key",
    )
    
    generar_btn = st.button("🚀 ¡Analizar mi dibujo y contar historia!", type="primary", use_container_width=True)

HISTORIAS = [
    "Había una vez un pequeño trazo mágico que decidió explorar el mundo de papel. Con cada paso que daba, creaba puentes de colores y reinos donde los lápices podían volar hacia las estrellas.",
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
        has_drawings = False
        img_data = None
        
        # Método a prueba de fallos: inspeccionar directamente el JSON de objetos del canvas
        if canvas_result is not None:
            # 1. Comprobar si hay elementos dibujados en el JSON
            if canvas_result.json_data is not None:
                objects = canvas_result.json_data.get("objects", [])
                if len(objects) > 0:
                    has_drawings = True
            
            # 2. Intentar extraer la matriz de pixeles
            try:
                img_data = canvas_result.image_data
            except Exception:
                img_data = None

        if has_drawings or (img_data is not None and np.any(img_data)):
            # Si image_data no se pudo leer directamente por el bug del componente, 
            # procesamos la existencia del trazo confirmada por json_data
            num_trazos = len(canvas_result.json_data.get("objects", [])) if canvas_result.json_data else 1
            
            # Asignación de estrellas
            if num_trazos >= 5:
                estrellas = "⭐⭐⭐⭐⭐ / 5"
            elif num_trazos >= 2:
                estrellas = "⭐⭐⭐⭐ / 5"
            else:
                estrellas = "⭐⭐⭐ / 5"
            
            medalla = random.choice(MEDALLAS)
            historia = random.choice(HISTORIAS)
            
            st.balloons()
            st.success("¡Tu dibujo ha sido analizado con éxito!")
            
            st.markdown(f"### 🌟 Calificación: {estrellas}")
            st.markdown(f"### {medalla}")
            st.markdown("---")
            st.markdown(f"**🔍 Elementos detectados:** Se identificaron **{num_trazos}** elementos/trazos en la hoja.")
            st.markdown("---")
            st.markdown("### 📖 Cuento del Lienzo:")
            st.write(historia)
        else:
            st.warning("¡El lienzo está vacío! Por favor realiza un dibujo antes de presionar el botón.")

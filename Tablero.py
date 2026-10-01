import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import google.generativeai as genai

# 1. Configuración de la página
st.set_page_config(
    page_title="¡Pequeños Artistas! 🎨✨",
    page_icon="🎨",
    layout="wide"
)

# 2. Configuración de la API Key de Gemini
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "TU_API_KEY_AQUI")

if GEMINI_API_KEY != "TU_API_KEY_AQUI":
    genai.configure(api_key=GEMINI_API_KEY)

# 3. Frase motivadora al inicio
st.markdown("""
    <div style="background-color: #FFE66D; padding: 15px; border-radius: 15px; text-align: center; margin-bottom: 20px;">
        <h3 style="color: #2B2D42; margin:0;">🌈 "Todo niño es un artista. El secreto es mantener la magia cuando crecemos." — Pablo Picasso 🚀</h3>
    </div>
""", unsafe_allow_html=True)

st.title("🌟 ¡El Lienzo Mágico de las Historias! 🎨")
st.write("Dibuja o escribe lo que te imagines, ¡y la IA creará un cuento especial para ti con una súper calificación!")

# 4. Barra Lateral Infantil
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

# 5. Interfaz Principal
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
    
    generar_btn = st.button("🚀 ¡Dar vida a mi dibujo y contar historia!", type="primary", use_container_width=True)

with col2:
    st.subheader("⭐ La Magia del Cuento")
    
    if generar_btn:
        if canvas_result.image_data is not None:
            img_data = canvas_result.image_data
            img = Image.fromarray(img_data.astype('uint8'), 'RGBA').convert('RGB')
            
            with st.spinner("🧙‍♂️ El mago de los cuentos está observando tu dibujo..."):
                if GEMINI_API_KEY != "TU_API_KEY_AQUI":
                    try:
                        model = genai.GenerativeModel('gemini-2.5-flash')
                        
                        prompt = (
                            "Eres un narrador amable, divertido y entusiasta para niños. "
                            "Observa este dibujo y haz lo siguiente: "
                            "1. Dale una calificación súper positiva en estrellas ⭐ (ejemplo: ⭐⭐⭐⭐⭐ / 5). "
                            "2. Dale un título divertido a su medalla de artista (ej. ¡Medalla de Gran Creador de Dragones!). "
                            "3. Describe de forma entusiasta qué observas en el dibujo. "
                            "4. Escribe un cuento muy divertido, mágico y corto (máximo 2 o 3 párrafos) "
                            "adaptado para niños basado en lo que dibujaron o escribieron."
                        )
                        
                        response = model.generate_content([prompt, img])
                        
                        st.balloons()
                        st.success("¡Tu cuento está listo!")
                        st.markdown(response.text)
                        
                    except Exception as e:
                        st.error(f"¡Ups! Hubo un problema al conectar con el mago de los cuentos: {e}")
                else:
                    # Respuesta de prueba por si no se ha configurado la API Key
                    st.balloons()
                    st.info("💡 Mode de prueba (Agrega tu GEMINI_API_KEY en secrets para conectar con la IA en vivo):")
                    st.markdown("""
                        ### ⭐ Calificación: ⭐⭐⭐⭐⭐ / 5 Estrellas
                        **🏅 Medalla Mágica:** *¡Súper Maestro del Color y la Imaginación!*
                        
                        ---
                        
                        ### 🔍 ¿Qué vemos aquí?
                        ¡Veo trazos llenos de energía y mucha creatividad! Se nota que le pusiste muchas ganas a esta obra de arte.
                        
                        ---
                        
                        ### 📖 El Cuento de tu Dibujo
                        Había una vez en un reino donde los colores cobraban vida, un pequeño trazo que decidió salir a explorar el mundo. Mientras caminaba por la hoja de papel, se encontró con otros colores alegres que juntos formaron una aventura inolvidable.
                        
                        ¡Sigue dibujando y creando mundos mágicos! ✨
                    """)
        else:
            st.warning("¡Primero haz un dibujo o una marca en el papel para empezar la magia! 🎨")

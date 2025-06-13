import streamlit as st
from groq import Groq


st.set_page_config(page_title="Chat de Diego Fernandez", page_icon="6", layout="centered")
 
modelos = ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"]


def configurar_pagina():

 st.title("Mi primera aplicación con Streamlit")
 st.sidebar.title("Configuración de la IA")
 elegirModelo = st.sidebar.selectbox("Elegí un Modelo de IA", options=modelos, index=0)
 return elegirModelo 
 




def crear_usuario_groq():
 clave_secreta = st.secrets["CLAVE_API"]
 return Groq(api_key=clave_secreta)

def configurar_modelo(cliente, modelo, mensajeDeEntrada):
 return cliente.chat.completions.create(
  model=modelo,
  messages=[{"role": "user", "content": mensajeDeEntrada}],
  stream=True
 )



def inicializar_estado():
 if "mensajes" not in st.session_state:
  st.session_state.mensajes = []


def mostrar_historial():
 for mensaje in st.session_state.mensajes:
  with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
   st.markdown(mensaje["content"])


nombre = st.text_input("¿Cual es tu nombre?: ")
if st.button("Saludar"):
 st.write(f"¡Hola, {nombre}! gracias por venir a Talento Tech")
 st.title("Bienvenido", nombre)


def area_chat():
 contenedorDelChat = st.container(height=400, border=True)
 with contenedorDelChat:
  mostrar_historial()


def actualizar_historial(rol, contenido, avatar):
 st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})










def generar_respuesta(chat_completo):
 respuesta_completa =""
 for frase in chat_completo:
  if frase.choices[0].delta.content:
   respuesta_completa += frase.choices[0].delta.content
   yield frase.choices[0].delta.content
 return respuesta_completa

def main():
 modelo = configurar_pagina()

 clienteUsuario = crear_usuario_groq()
 inicializar_estado()  
 
 mensaje = st.chat_input("Escribí tu mensaje:")

 area_chat()
 if mensaje:
    actualizar_historial("user", mensaje, "🙂")  
    
    chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
    
    if chat_completo:
     with st.chat_message("assistant"):
       respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
    
    actualizar_historial("assistant", respuesta_completa, "🤖") 
    
    st.rerun()

if __name__ == "__main__":
 main()
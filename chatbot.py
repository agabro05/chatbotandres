import streamlit as st 
from groq import Groq #CLASE 7 

#Clase 6 
st.set_page_config(page_title="Mi Chat De IA", layout="centered",page_icon="🦌")
st.title("Primer app Andres con streamlit. ")
nombre=st.text_input("¿Cual es tu nombre")
if st.button("saludar"): 
    st.write(f"!Bienvenido al chatbot {nombre}")

#Clase 7 
def configurar_pagina(): 
    st.title("Chat de IA Andres")
    st.sidebar.title("configuracion del modelo")
    elegirmodelo= st.sidebar.selectbox('Elegi un modelo',options=MODELOS,index=0)
    return elegirmodelo

MODELOS = ['llama-3.1-8b-instant', 'llama-3.3-70b-versatile', 'deepseek-r1-distill-llama-70b']

#Funcion para crear un usuario
def crearusuariogroq():
    clave_secreta = st.secrets["clave_api"]
    return Groq(api_key=clave_secreta)

def configurar_modelo(cliente,modelo,mensajentrada): 
    return cliente.chat.completions.create(
        model=modelo,
        messages = [{"role" : "user", "content": mensajentrada}],
        stream=True
    )

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

#clase 8 
#Actualizar Historial 
def actualizarhistorial(rol,contenido,avatar):
    st.session_state.mensajes.append({"role": rol,"content":contenido,"avatar": avatar})


#mostrar historial
def mostrarhistorial():
    for mensaje in st.session_state.mensajes: 
        with st.chat_message(mensaje["role"],avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

#area historial
def areahistorial():
    contenedordelchat = st.container(height=400,border=True)
    with contenedordelchat:
        mostrarhistorial()

#Clase 9
#GenerarRespuesta
def generarRespuesta (chatcompleto):
    respuestacompleta=""
    for frase in chatcompleto:
        if frase.choices[0].delta.content: 
            respuestacompleta+=frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuestacompleta
    
#funcion main()
def main():
    elegirmodelo=configurar_pagina()
    clienteusuario=crearusuariogroq()
    inicializar_estado()
    areahistorial()
    mensaje = st.chat_input("escribi tu mensaje")
    if mensaje: 
        actualizarhistorial("user", mensaje, "🙍‍♂️")
        chatcompleto= configurar_modelo(clienteusuario,elegirmodelo,mensaje)
        if chatcompleto:
            with st.chat_message("assistant"):
                chatcompleto=st.write_stream(generarRespuesta(chatcompleto))
                actualizarhistorial("assistant",chatcompleto,"")
    st.rerun()
if __name__== "__main__":
    main()


import streamlit as st
import groq


altura_contenedor_chat = 400
stream_status = True


MODELOS = ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "llama-guard-4-12b"]



def configurar_pagina():

    st.set_page_config(page_title="Un chat muy girly", page_icon= "🌸")

    st.title("Un chat muy girly")

    nombre = st.text_input("¿Cuál es tu nombre?")

    if st.button("Saludar"):
        st.write("Hola " + nombre)

    st.subheader("Tu espacio para chatear con confianza 🌷")

    st.sidebar.title("Selección de modelos")

    elegirModelo = st.sidebar.selectbox("Elegí un modelo", options=MODELOS, index=0)

    return elegirModelo


def crear_usuario():
    clave_secreta = st.secrets["CLAVE_API"]
    return groq.Groq(api_key = clave_secreta)    


def configurar_modelo(cliente, modelo_elegido, prompt_usuario):
    return cliente.chat.completions.create(
        model = modelo_elegido,
        messages = [{"role" : "user", "content" : prompt_usuario}],
        stream = stream_status
    )

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.write(mensaje["content"])

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role" : rol, "content" : contenido,
                                      "avatar" : avatar})

def area_chat():
    contenedor = st.container(height=altura_contenedor_chat, border=True)
    with contenedor:
        mostrar_historial()

def generar_respuesta(respuesta_del_bot):
    _respuesta_real = ""
    for frase in respuesta_del_bot: 
        if frase.choices[0].delta.content:
            _respuesta_real += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return _respuesta_real

def main():

    modelo_elegido_por_el_usuario = configurar_pagina()

    cliente_usuario = crear_usuario()

    inicializar_estado()

    area_chat()

    prompt_del_usuario = st.chat_input("Escribí tu prompt: ")

    if prompt_del_usuario:
        actualizar_historial("user", prompt_del_usuario, "😉")
        respuesta_del_bot = configurar_modelo(cliente_usuario, modelo_elegido_por_el_usuario, prompt_del_usuario)

        if respuesta_del_bot:
            with st.chat_message("assistant"):
                respuesta_real = st.write_stream(generar_respuesta(respuesta_del_bot))
                actualizar_historial("assistant", respuesta_real, "🤖")

                st.rerun()
if __name__ == "__main__":
    main()


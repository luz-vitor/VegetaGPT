import streamlit as st
from openai import OpenAI
from context import context
from texto_desenvolvedor import texto_desenvolvedor
from texto_fonte import texto_fonte
import os

class Constants:
    ICON_PATH = os.path.join('images', 'icon_pag.png')
    ALUNO_IMAGE= os.path.join('images', 'aluno.png')
    VEGETA_IMAGE= os.path.join('images', 'vegeta-serio.png')
    DESENVOLVEDOR_IMAGE= os.path.join('images', 'desenvolvedor.jpg')
    OPENAI_MODEL = "gpt-3.5-turbo"
    MAX_INTERACTIONS = 10    

class VegetaGPT:
    def __init__(self):
        st.set_page_config(
            page_title="VegetaGPT - Aumente seu ki!",
            page_icon= Constants.ICON_PATH,
            layout="centered",
            initial_sidebar_state="expanded",
            menu_items={"About":"Obrigado pela visita! | LinkedIn: https://www.linkedin.com/in/vitor-luz-57b503182/ | Github:  https://github.com/luz-vitor"},

        )

        st.title("VegetaGPT - Aumente seu ki!")
        self.client = OpenAI(api_key= st.secrets['OPENAI_API_KEY'])
        self.context = context
        self.image_vegeta = Constants.VEGETA_IMAGE 
        self.image_aluno = Constants.ALUNO_IMAGE
        self.desenvolvedor= Constants.DESENVOLVEDOR_IMAGE
    
    def setup_background_styles(self):
        page_bg_img = """
        <style>
            [data-testid="ScrollToBottomContainer"] {
                background-image: url('https://i.ibb.co/DDBpDzJ/plano-fundo.png');
                background-size: wide; 
            }
            [data-testid="stChatInputSubmitButton"] {
                background-color: orange;
                color: white;
            }  
            @media (prefers-color-scheme: dark) {
                [data-testid="stAppViewBlockContainer"] {                    
                    color: white;
                    background-color: #333;
                }
            } 
            @media (max-width: 600px) {
                div[data-testid="stBlock"] {
                    width: 100% !important;
                }
            }               
        </style>
        """
        st.markdown(page_bg_img, unsafe_allow_html=True)

    def display_chat_messages(self):
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])       

    def user_input(self, prompt):
        if prompt:
            st.session_state.interaction_count = st.session_state.get("interaction_count", 0)
            st.session_state.interaction_count += 1

            if st.session_state.interaction_count > Constants.MAX_INTERACTIONS:
                st.warning(f"Desculpe, você atingiu o limite de {Constants.MAX_INTERACTIONS} interações. Como a API é paga, quero garantir que mais pessoas possam experimentar a aplicação. Obrigado pela compreensão!")
                return

            with st.chat_message("user"):
                st.image(self.image_aluno, width=75, caption="Você")
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content":prompt})

            with st.chat_message("system"):
                st.image(self.image_vegeta, width=75, caption="VegetaGPT")
                message_placeholder = st.empty()
                full_response = ""
                system_message = [{"role": "system", "content": self.context}]
                user_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                for response in self.client.chat.completions.create(
                    model= Constants.OPENAI_MODEL,                    
                    messages = system_message + user_messages,
                    stream = True,
                ):
                    full_response += response.choices[0].delta.content if response.choices[0].delta.content is not None else ""
                    message_placeholder.markdown(full_response + "")
                message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role":"system", "content":full_response})
    
    def display_sidebar_infos(self):
        st.sidebar.info('Desenvolvido por:')
        st.sidebar.image(self.desenvolvedor, width=300,caption="Vitor Luz")
        st.sidebar.write(texto_desenvolvedor)        
        st.sidebar.markdown('[![LinkedIn](https://img.shields.io/badge/LinkedIn-Vitor_Luz-blue)](https://www.linkedin.com/in/vitor-luz-57b503182/)')
        st.sidebar.markdown('[![GitHub](https://img.shields.io/badge/GitHub-Vitor_Luz-green)](https://github.com/luz-vitor)')
        st.sidebar.write(texto_fonte)

    def run(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []
                    
        self.setup_background_styles()
        self.display_chat_messages()
        
        prompt = st.chat_input("Insira sua mensagem aqui!")      

        self.user_input(prompt)
        self.display_sidebar_infos()

if __name__ == "__main__":
    vegeta_gpt_app = VegetaGPT()
    vegeta_gpt_app.run()

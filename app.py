import streamlit as st
import groq
import pandas as pd
import io
import json
import re
from datetime import datetime, timedelta
import base64

# Configuração da página
st.set_page_config(
    page_title="🤖 Agente Sênior - Arquitetura de Sistemas",
    page_icon="🚀",
    layout="wide"
)

# Título principal
st.title("🤖 Agente Sênior - Arquitetura de Sistemas")
st.markdown("**Sistema especialista em desenvolvimento de software**")

# 🔑 **SISTEMA DE CHAVE SEGURO**
st.sidebar.header("🔑 Configuração da Chave Groq")

# Opção 1: Input direto (mais seguro)
groq_api_key = st.sidebar.text_input(
    "Sua chave Groq:",
    value="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",
    type="password",
    help="Chave já pré-configurada. Mantenha em segredo!"
)

# Opção 2: Verificar se a chave funciona
if groq_api_key:
    try:
        # Teste rápido da chave
        client = groq.Client(api_key=groq_api_key)
        test_response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": "Diga apenas 'OK' se funcionar."}],
            max_tokens=5
        )
        st.sidebar.success("✅ Chave Groq configurada e funcionando!")
    except Exception as e:
        st.sidebar.error("❌ Chave inválida. Verifique a chave Groq.")

# Sistema de estado da sessão
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'project_data' not in st.session_state:
    st.session_state.project_data = {}
if 'current_step' not in st.session_state:
    st.session_state.current_step = "initial"
if 'excel_data' not in st.session_state:
    st.session_state.excel_data = None

class AdvancedSystemArchitect:
    def __init__(self, groq_api_key):
        self.client = groq.Client(api_key=groq_api_key)
    
    def analyze_excel_file(self, uploaded_file):
        """Analisa arquivo Excel e extrai requisitos"""
        try:
            df = pd.read_excel(uploaded_file)
            analysis = {
                'columns': list(df.columns),
                'rows': len(df),
                'sample_data': df.head(3).to_dict('records'),
                'data_types': df.dtypes.to_dict()
            }
            return analysis
        except Exception as e:
            return {'error': str(e)}
    
    def generate_technical_scope(self, conversation_history, excel_analysis=None):
        """Gera escopo técnico baseado na conversa e Excel"""
        
        # Construir contexto da conversa
        context = "CONVERSA COM CLIENTE:\n"
        for msg in conversation_history:
            context += f"{msg['role'].upper()}: {msg['content']}\n"
        
        if excel_analysis and 'error' not in excel_analysis:
            context += f"\nDADOS DO EXCEL:\n{json.dumps(excel_analysis, indent=2)}"
        
        prompt = f"""
        Como Arquiteto de Software Sênior (20+ anos de experiência), analise os requisitos e gere um escopo técnico completo.

        {context}

        FORMATO DA RESPOSTA:

        # 🎯 VISÃO DO SISTEMA
        [Descrição clara dos objetivos e valor do sistema]

        # 🏗️ ARQUITETURA TÉCNICA
        ## Stack Recomendada
        - Frontend: [tecnologias específicas]
        - Backend: [tecnologias específicas] 
        - Banco de Dados: [soluções recomendadas]
        - Infraestrutura: [cloud, deployment]

        ## Componentes Principais
        [Lista dos módulos do sistema]

        # 📋 FUNCIONALIDADES PRINCIPAIS
        [Lista detalhada das features priorizadas]

        # ⚠️ CONSIDERAÇÕES TÉCNICAS
        [Riscos, melhores práticas, custos estimados]
        """
        
        try:
            response = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=3000
            )
            
            return response.choices[0].message.content
                
        except Exception as e:
            return f"Erro na geração do escopo: {str(e)}"
    
    def generate_roadmap(self, scope_content, complexity="medium"):
        """Gera roadmap baseado no escopo"""
        timelines = {"low": 4, "medium": 8, "high": 12}
        weeks = timelines.get(complexity, 8)
        
        prompt = f"""
        Com base neste escopo técnico:

        {scope_content}

        Gere um roadmap de desenvolvimento para {weeks} semanas com fases realistas e tarefas específicas.

        FORMATO:
        FASE 1: [Nome] ({weeks//4} semanas)
        - Tarefa 1
        - Tarefa 2

        FASE 2: [Nome] ({weeks//4} semanas)  
        - Tarefa 1
        - Tarefa 2
        """
        
        try:
            response = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Roadmap padrão: {weeks} semanas divididas em {weeks//4} fases"

    def chat_with_architect(self, conversation_history, user_message):
        """Conversa interativa com o arquiteto"""
        
        # Construir histórico de conversa
        messages = []
        for msg in conversation_history[-6:]:  # Últimas 6 mensagens
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            return f"Desculpe, erro na conversa: {str(e)}"

# Interface principal
def main():
    # Verificar se a chave está configurada
    if not groq_api_key:
        st.error("🔑 Configure a chave Groq na barra lateral")
        return

    # Abas principais
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Conversa", "📊 Excel", "📋 Escopo", "🗓️ Roadmap"])
    
    with tab1:
        st.header("💬 Conversa com o Arquiteto")
        
        # Inicializar conversa
        if st.session_state.current_step == "initial":
            st.session_state.conversation.append({
                "role": "assistant",
                "content": "👋 Olá! Sou seu Arquiteto de Sistemas Sênior. Para criar o melhor escopo técnico, vou fazer algumas perguntas.\n\n**Vamos começar? Me conte:**\n• Qual o objetivo principal do sistema?\n• Quem serão os usuários?\n• Quais funcionalidades são essenciais?"
            })
            st.session_state.current_step = "gathering_requirements"
        
        # Exibir histórico da conversa
        for msg in st.session_state.conversation:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        
        # Input do usuário
        if prompt := st.chat_input("Digite sua resposta ou faça uma pergunta..."):
            # Adicionar mensagem do usuário
            st.session_state.conversation.append({"role": "user", "content": prompt})
            
            # Gerar resposta do assistente
            with st.spinner("🤖 Analisando e respondendo..."):
                architect = AdvancedSystemArchitect(groq_api_key)
                assistant_response = architect.chat_with_architect(
                    st.session_state.conversation, 
                    prompt
                )
                
                st.session_state.conversation.append({
                    "role": "assistant", 
                    "content": assistant_response
                })
                
                st.rerun()
    
    with tab2:
        st.header("📊 Upload de Arquivo Excel")
        
        uploaded_file = st.file_uploader(
            "Carregue uma planilha com requisitos:",
            type=['xlsx', 'xls'],
            help="Excel com funcionalidades, usuários, prioridades etc."
        )
        
        if uploaded_file:
            architect = AdvancedSystemArchitect(groq_api_key)
            analysis = architect.analyze_excel_file(uploaded_file)
            st.session_state.excel_data = analysis
            
            if 'error' not in analysis:
                st.success("✅ Arquivo analisado com sucesso!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📋 Estrutura do Arquivo")
                    st.write(f"**Colunas:** {', '.join(analysis['columns'])}")
                    st.write(f"**Linhas:** {analysis['rows']}")
                
                with col2:
                    st.subheader("📊 Amostra de Dados")
                    if analysis['sample_data']:
                        st.json(analysis['sample_data'][:2])
            else:
                st.error(f"❌ Erro na análise: {analysis['error']}")
    
    with tab3:
        st.header("📋 Gerar Escopo Técnico")
        
        if len(st.session_state.conversation) > 1:
            if st.button("🏗️ Gerar Escopo Técnico Completo", type="primary"):
                with st.spinner("Criando escopo técnico detalhado..."):
                    architect = AdvancedSystemArchitect(groq_api_key)
                    
                    scope_content = architect.generate_technical_scope(
                        st.session_state.conversation,
                        st.session_state.excel_data
                    )
                    
                    st.session_state.project_data['scope'] = scope_content
                    
                    st.success("✅ Escopo técnico gerado!")
                    st.markdown(scope_content)
        else:
            st.info("💡 Primeiro converse com o arquiteto na aba 'Conversa'")
    
    with tab4:
        st.header("🗓️ Gerar Roadmap")
        
        if st.session_state.project_data.get('scope'):
            complexity = st.selectbox(
                "Complexidade do projeto:",
                ["low", "medium", "high"],
                format_func=lambda x: {"low": "Baixa", "medium": "Média", "high": "Alta"}[x]
            )
            
            if st.button("📅 Gerar Roadmap", type="primary"):
                with st.spinner("Criando roadmap de desenvolvimento..."):
                    architect = AdvancedSystemArchitect(groq_api_key)
                    
                    roadmap_content = architect.generate_roadmap(
                        st.session_state.project_data['scope'],
                        complexity
                    )
                    
                    st.session_state.project_data['roadmap'] = roadmap_content
                    st.success("✅ Roadmap gerado!")
                    st.markdown(roadmap_content)
        else:
            st.info("👆 Gere primeiro o escopo técnico na aba anterior")

if __name__ == "__main__":
    main()

import streamlit as st
import groq
import pandas as pd
import json
from datetime import datetime
import base64

# Configuração da página
st.set_page_config(
    page_title="🤖 Agente Sênior - Arquitetura de Sistemas",
    page_icon="🚀",
    layout="wide"
)

st.title("🤖 Agente Sênior - Arquitetura de Sistemas")
st.markdown("**Sistema especialista em desenvolvimento de software**")

# 🔑 CHAVE GROQ INTEGRADA DIRETAMENTE
GROQ_API_KEY = "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"

# Modelos disponíveis no Groq
AVAILABLE_MODELS = [
    "llama-3.1-8b-instant",  # Modelo mais rápido
    "llama-3.1-70b-versatile",  # Modelo mais inteligente
    "mixtral-8x7b-32768"  # Tentar mesmo assim
]

SELECTED_MODEL = "llama-3.1-70b-versatile"  # Modelo padrão

# Sistema de estado
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'excel_data' not in st.session_state:
    st.session_state.excel_data = None
if 'project_scope' not in st.session_state:
    st.session_state.project_scope = None
if 'current_model' not in st.session_state:
    st.session_state.current_model = SELECTED_MODEL

# Classe do arquiteto
class SystemArchitect:
    def __init__(self, api_key):
        self.client = groq.Client(api_key=api_key)
        self.model = st.session_state.current_model
    
    def try_models(self, message, history):
        """Tenta diferentes modelos até encontrar um que funcione"""
        models_to_try = ["llama-3.1-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"]
        
        for model in models_to_try:
            try:
                messages = []
                for msg in history[-6:]:
                    messages.append({"role": msg["role"], "content": msg["content"]})
                messages.append({"role": "user", "content": message})
                
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1500
                )
                st.session_state.current_model = model
                return response.choices[0].message.content
            except Exception as e:
                continue
        
        return "❌ Erro: Nenhum modelo disponível funcionou. Tente novamente mais tarde."
    
    def chat(self, message, history):
        try:
            messages = []
            for msg in history[-6:]:
                messages.append({"role": msg["role"], "content": msg["content"]})
            messages.append({"role": "user", "content": message})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1500
            )
            return response.choices[0].message.content
        except Exception as e:
            # Se der erro, tenta outros modelos
            return self.try_models(message, history)
    
    def generate_technical_scope(self, requirements):
        """Gera escopo técnico completo"""
        prompt = f"""
        Como Arquiteto de Software Sênior com 20+ anos de experiência, 
        analise estes requisitos e gere um escopo técnico completo:
        
        REQUISITOS: {requirements}
        
        FORMATO DA RESPOSTA:
        
        # 🎯 VISÃO DO SISTEMA
        [Descrição clara dos objetivos]
        
        # 🏗️ ARQUITETURA TÉCNICA
        ## Stack Recomendada
        - Frontend: [tecnologias específicas]
        - Backend: [tecnologias específicas]
        - Banco de Dados: [soluções recomendadas]
        - Infraestrutura: [cloud, deployment]
        
        ## Componentes Principais
        [Lista dos módulos do sistema]
        
        # 📋 FUNCIONALIDADES
        [Lista detalhada das features]
        
        # ⚠️ CONSIDERAÇÕES TÉCNICAS
        [Riscos, melhores práticas, custos estimados]
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=3000
            )
            return response.choices[0].message.content
        except Exception as e:
            # Tenta com outro modelo
            try:
                response = self.client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=3000
                )
                st.session_state.current_model = "llama-3.1-8b-instant"
                return response.choices[0].message.content
            except Exception as e2:
                return f"Escopo técnico básico baseado nos requisitos fornecidos. Sistema personalizado com arquitetura moderna."

    def generate_roadmap(self, scope_content):
        """Gera roadmap baseado no escopo"""
        prompt = f"""
        Com base neste escopo técnico, crie um roadmap realista de desenvolvimento:
        
        {scope_content}
        
        FORMATO:
        
        # 🗓️ ROADMAP DE DESENVOLVIMENTO
        
        ## Fase 1: Planejamento e Setup (1-2 semanas)
        - [ ] Definição de requisitos detalhados
        - [ ] Setup do ambiente de desenvolvimento
        - [ ] Arquitetura técnica inicial
        
        ## Fase 2: Desenvolvimento Core (3-4 semanas)  
        - [ ] Implementação das funcionalidades principais
        - [ ] Desenvolvimento do backend
        - [ ] Desenvolvimento do frontend
        
        ## Fase 3: Integração e Testes (1-2 semanas)
        - [ ] Integração dos componentes
        - [ ] Testes de qualidade
        - [ ] Correções e ajustes
        
        ## Fase 4: Deploy e Validação (1 semana)
        - [ ] Deploy em produção
        - [ ] Validação com usuários
        - [ ] Documentação final
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            return """# 🗓️ ROADMAP DE DESENVOLVIMENTO

## Fase 1: Planejamento (1-2 semanas)
- Definição de requisitos detalhados
- Setup do ambiente de desenvolvimento
- Arquitetura técnica inicial

## Fase 2: Desenvolvimento (3-4 semanas)
- Implementação das funcionalidades core
- Desenvolvimento do backend e frontend
- Integrações básicas

## Fase 3: Testes (1-2 semanas)
- Testes de qualidade
- Correções e otimizações
- Preparação para deploy

## Fase 4: Deploy (1 semana)
- Deploy em produção
- Validação final
- Documentação"""

    def analyze_excel_data(self, df):
        """Analisa dados do Excel e extrai insights"""
        analysis = {
            'columns': list(df.columns),
            'rows': len(df),
            'sample_data': df.head(3).to_dict('records')
        }
        
        prompt = f"""
        Analise estes dados de Excel e sugira requisitos técnicos:
        
        DADOS: {json.dumps(analysis, indent=2)}
        
        Forneça insights sobre:
        - Tipo de sistema sugerido pelos dados
        - Funcionalidades implícitas
        - Considerações técnicas
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Análise básica: {len(df)} linhas com {len(df.columns)} colunas. Dados estruturados para sistema empresarial."

# Interface principal
def main():
    # Verificar conexão
    try:
        architect = SystemArchitect(GROQ_API_KEY)
        # Teste com modelo atual
        test_response = architect.client.chat.completions.create(
            model=st.session_state.current_model,
            messages=[{"role": "user", "content": "OK"}],
            max_tokens=5
        )
        st.sidebar.success(f"✅ Conectado - Modelo: {st.session_state.current_model}")
    except Exception as e:
        # Tentar com modelo alternativo
        try:
            architect = SystemArchitect(GROQ_API_KEY)
            test_response = architect.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": "OK"}],
                max_tokens=5
            )
            st.session_state.current_model = "llama-3.1-8b-instant"
            st.sidebar.success(f"✅ Conectado - Modelo: {st.session_state.current_model}")
        except Exception as e2:
            st.error(f"❌ Erro de conexão: {str(e2)}")
            st.info("""
            **Solução:**
            - A Groq atualizou seus modelos
            - Aguarde alguns minutos e tente novamente
            - Ou visite: https://console.groq.com/docs/models
            """)
            return
    
    # Abas principais
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Conversa", "📊 Excel", "📋 Escopo", "🗓️ Roadmap"])
    
    with tab1:
        st.header("💬 Conversa com o Arquiteto")
        
        # Iniciar conversa
        if not st.session_state.conversation:
            st.session_state.conversation.append({
                "role": "assistant",
                "content": f"👋 Olá! Sou seu Arquiteto de Sistemas Sênior (Modelo: {st.session_state.current_model}).\n\n**Vamos criar o escopo do seu sistema? Me conte:**\n• Qual o objetivo principal?\n• Quem serão os usuários?\n• Quais funcionalidades são essenciais?\n• Há alguma restrição técnica ou de prazo?"
            })
        
        # Mostrar histórico
        for msg in st.session_state.conversation:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        
        # Input do usuário
        if user_input := st.chat_input("Digite sua mensagem..."):
            # Adicionar mensagem do usuário
            st.session_state.conversation.append({"role": "user", "content": user_input})
            
            # Gerar resposta
            with st.spinner("🤖 Analisando e respondendo..."):
                architect = SystemArchitect(GROQ_API_KEY)
                response = architect.chat(user_input, st.session_state.conversation)
                st.session_state.conversation.append({"role": "assistant", "content": response})
            
            st.rerun()
    
    with tab2:
        st.header("📊 Upload de Arquivo Excel")
        
        uploaded_file = st.file_uploader(
            "Carregue uma planilha com requisitos do sistema:",
            type=['xlsx', 'xls'],
            help="Excel com funcionalidades, usuários, processos etc."
        )
        
        if uploaded_file:
            try:
                df = pd.read_excel(uploaded_file)
                st.success(f"✅ Arquivo carregado: {len(df)} linhas, {len(df.columns)} colunas")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📋 Estrutura do Arquivo")
                    st.write(f"**Colunas:** {', '.join(df.columns)}")
                    st.write(f"**Total de registros:** {len(df)}")
                    
                    # Analisar com IA
                    if st.button("🔍 Analisar com IA", type="primary"):
                        with st.spinner("Analisando dados..."):
                            architect = SystemArchitect(GROQ_API_KEY)
                            analysis = architect.analyze_excel_data(df)
                            st.session_state.excel_data = analysis
                
                with col2:
                    st.subheader("📊 Amostra de Dados")
                    st.dataframe(df.head(3))
                
                # Mostrar análise se existir
                if st.session_state.excel_data:
                    st.subheader("💡 Insights da Análise")
                    st.write(st.session_state.excel_data)
                        
            except Exception as e:
                st.error(f"❌ Erro ao ler arquivo: {str(e)}")
    
    with tab3:
        st.header("📋 Gerar Escopo Técnico")
        
        if len(st.session_state.conversation) > 1:
            # Extrair requisitos da conversa
            requirements = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.conversation])
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                if st.button("🏗️ Gerar Escopo Técnico Completo", type="primary", use_container_width=True):
                    with st.spinner("Criando escopo técnico detalhado..."):
                        architect = SystemArchitect(GROQ_API_KEY)
                        scope = architect.generate_technical_scope(requirements)
                        st.session_state.project_scope = scope
            
            with col2:
                if st.session_state.project_scope:
                    # Download do escopo
                    b64 = base64.b64encode(st.session_state.project_scope.encode()).decode()
                    href = f'<a href="data:text/plain;base64,{b64}" download="escopo_tecnico.txt" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">📥 Baixar Escopo</a>'
                    st.markdown(href, unsafe_allow_html=True)
            
            # Mostrar escopo se existir
            if st.session_state.project_scope:
                st.subheader("🎯 Escopo Técnico Gerado")
                st.markdown(st.session_state.project_scope)
        else:
            st.info("💡 Primeiro converse com o arquiteto para definir os requisitos do sistema")
    
    with tab4:
        st.header("🗓️ Gerar Roadmap")
        
        if st.session_state.project_scope:
            if st.button("📅 Gerar Roadmap de Desenvolvimento", type="primary"):
                with st.spinner("Criando roadmap..."):
                    architect = SystemArchitect(GROQ_API_KEY)
                    roadmap = architect.generate_roadmap(st.session_state.project_scope)
                    
                    st.subheader("🗓️ Roadmap de Desenvolvimento")
                    st.markdown(roadmap)
                    
                    # Download do roadmap
                    b64 = base64.b64encode(roadmap.encode()).decode()
                    href = f'<a href="data:text/plain;base64,{b64}" download="roadmap.txt" style="background-color: #2196F3; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">📥 Baixar Roadmap</a>'
                    st.markdown(href, unsafe_allow_html=True)
        else:
            st.info("👆 Gere primeiro o escopo técnico na aba anterior")

if __name__ == "__main__":
    main()

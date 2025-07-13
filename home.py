# Home.py
import streamlit as st

st.set_page_config(
    page_title="Página Inicial - Análise de Produtos",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Bem-vindo ao Dashboard de Análise de Viabilidade de Produtos!")

st.markdown("""
Este aplicativo foi projetado para ajudá-lo a analisar produtos de diferentes categorias da Amazon.

**Como usar:**
1.  **Navegue pelas páginas** no menu à esquerda para selecionar a categoria que deseja analisar.
2.  Use os **filtros** no topo de cada página para refinar sua busca por nome, preço, volume de vendas e tipo de entrega.
3.  **Analise as métricas e a tabela** para identificar oportunidades.

---

**Para começar, selecione uma categoria no menu lateral.**
""")

st.image("https://images.unsplash.com/photo-1586880244496-53d332b13e34?q=80&w=2070", caption="Analisando os dados para encontrar as melhores oportunidades.")
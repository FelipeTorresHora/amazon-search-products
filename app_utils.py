# app_utils.py

import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data(filepath):
    """Carrega e prepara os dados do arquivo CSV de forma segura."""
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        return None # Retorna None se o arquivo não for encontrado

    # Limpeza e Transformação dos Dados
    if 'product_price' in df.columns and not df['product_price'].isnull().all():
        df['product_price_cleaned'] = df['product_price'].astype(str).str.replace('R$', '', regex=False).str.replace('.', '', regex=False).str.replace(',', '.', regex=False).str.strip()
        df['product_price_cleaned'] = pd.to_numeric(df['product_price_cleaned'], errors='coerce')
        df.dropna(subset=['product_price_cleaned'], inplace=True)
    else:
        df['product_price_cleaned'] = 0.0

    if 'sales_volume' in df.columns and not df['sales_volume'].isnull().all():
        df['sales_volume_numeric'] = df['sales_volume'].str.extract(r'(\d+)').astype(float)
        df['sales_volume_numeric'] = df['sales_volume_numeric'].fillna(0)
        df['sales_volume_category'] = df['sales_volume'].fillna('Não informado')
    else:
        df['sales_volume_numeric'] = 0
        df['sales_volume_category'] = 'Não informado'

    for col in ['product_star_rating', 'product_num_ratings']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    return df

def create_analysis_page(category_name, file_path):
    """Função que cria uma página de análise completa no Streamlit."""
    
    st.set_page_config(layout="wide", page_title=f"{category_name} - Análise")
    
    st.title(f'Análise de Produtos: {category_name}')
    st.markdown("Use os filtros abaixo para explorar os dados.")

    df = load_data(file_path)

    if df is None:
        st.error(f"Arquivo de dados para '{category_name}' não encontrado.")
        st.info(f"Execute o script `busca_produtos.py` para gerar o arquivo em `{file_path}`.")
        return

    # --- FILTROS ---
    st.header("Filtros", divider='rainbow')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        product_name_filter = st.text_input("Nome do Produto", placeholder="Ex: mouse, ração, furadeira...")
    with col2:
        min_p, max_p = float(df['product_price_cleaned'].min()), float(df['product_price_cleaned'].max())
        price_range = st.slider('Faixa de Preço (R$)', min_p, max_p, (min_p, max_p))
    with col3:
        sales_options = sorted(df['sales_volume_category'].unique())
        selected_sales = st.multiselect('Volume de Vendas', sales_options, default=sales_options)
    with col4:
        delivery_term = st.text_input("Termo na Entrega", placeholder="Ex: GRÁTIS, Prime...")

    # --- LÓGICA DE FILTRAGEM ---
    df_filtered = df[
        (df['product_price_cleaned'] >= price_range[0]) &
        (df['product_price_cleaned'] <= price_range[1]) &
        (df['sales_volume_category'].isin(selected_sales)) &
        (df['product_title'].str.contains(product_name_filter, case=False, na=False)) &
        (df['delivery'].str.contains(delivery_term, case=False, na=False))
    ]

    # --- MÉTRICAS ---
    st.header("Métricas Resumidas", divider='rainbow')
    total_products = len(df_filtered)
    avg_price = df_filtered['product_price_cleaned'].mean() if not df_filtered.empty else 0
    avg_rating = df_filtered['product_star_rating'].mean() if not df_filtered.empty else 0
    total_ratings = int(df_filtered['product_num_ratings'].sum())

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Nº de Produtos", f"{total_products}")
    m2.metric("Preço Médio", f"R$ {avg_price:,.2f}")
    m3.metric("Avaliação Média", f"{avg_rating:,.1f} ⭐")
    m4.metric("Total de Avaliações", f"{total_ratings:,}")
    
    # --- TABELA ---
    st.header("Tabela de Produtos", divider='rainbow')
    columns_to_show = {'product_title': 'Título', 'product_price_cleaned': 'Preço (R$)', 'product_star_rating': 'Avaliação', 'product_num_ratings': 'Nº Avaliações', 'sales_volume_category': 'Vendas', 'product_url': 'Link'}
    df_display = df_filtered[list(columns_to_show.keys())].rename(columns=columns_to_show)
    st.dataframe(df_display, use_container_width=True, height=400, column_config={"Link": st.column_config.LinkColumn(display_text="🔗 Abrir")})
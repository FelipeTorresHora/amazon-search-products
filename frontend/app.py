"""
Amazon Search Products - Streamlit Frontend
Main application entry point
"""
import streamlit as st
import requests
from typing import Optional
import os

# Configuration
API_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
API_V1 = f"{API_URL}/api/v1"

# Page config
st.set_page_config(
    page_title="Amazon Search Products",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    if "access_token" not in st.session_state:
        st.session_state.access_token = None
    if "user" not in st.session_state:
        st.session_state.user = None


def is_authenticated() -> bool:
    """Check if user is authenticated."""
    return st.session_state.access_token is not None


def login_page():
    """Display login page."""
    st.markdown('<div class="main-header">🛒 Amazon Search Products</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.subheader("Login")

        with st.form("login_form"):
            email = st.text_input("Email", placeholder="seu@email.com")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Entrar", use_container_width=True)

            if submit:
                try:
                    # Call login API
                    response = requests.post(
                        f"{API_V1}/auth/login",
                        data={"username": email, "password": password}
                    )

                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.access_token = data["access_token"]

                        # Get user info
                        user_response = requests.get(
                            f"{API_V1}/auth/me",
                            headers={"Authorization": f"Bearer {data['access_token']}"}
                        )

                        if user_response.status_code == 200:
                            st.session_state.user = user_response.json()
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error("Failed to get user info")
                    else:
                        st.error("Invalid credentials")

                except Exception as e:
                    st.error(f"Login error: {str(e)}")

        st.markdown("---")

        st.subheader("Criar Conta")

        with st.form("register_form"):
            reg_name = st.text_input("Nome Completo")
            reg_email = st.text_input("Email")
            reg_password = st.text_input("Senha", type="password")
            reg_company = st.text_input("Empresa (opcional)")
            register = st.form_submit_button("Registrar", use_container_width=True)

            if register:
                try:
                    response = requests.post(
                        f"{API_V1}/auth/register",
                        json={
                            "email": reg_email,
                            "password": reg_password,
                            "full_name": reg_name,
                            "company": reg_company
                        }
                    )

                    if response.status_code == 201:
                        data = response.json()
                        st.session_state.access_token = data["access_token"]
                        st.success("Registration successful!")
                        st.rerun()
                    else:
                        st.error(f"Registration failed: {response.json().get('detail')}")

                except Exception as e:
                    st.error(f"Registration error: {str(e)}")


def main_app():
    """Display main application."""
    # Sidebar
    with st.sidebar:
        st.title("🛒 Amazon Search")

        user = st.session_state.user
        if user:
            st.write(f"👤 {user.get('full_name')}")
            st.write(f"📧 {user.get('email')}")
            st.write(f"📊 Plan: {user.get('role', 'Free').upper()}")

        st.markdown("---")

        menu = st.radio(
            "Menu",
            ["🏠 Dashboard", "🔍 Buscar Produtos", "🔔 Alertas", "📊 Uso", "⚙️ Configurações"]
        )

        st.markdown("---")

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.access_token = None
            st.session_state.user = None
            st.rerun()

    # Main content
    if "Dashboard" in menu:
        dashboard_page()
    elif "Buscar" in menu:
        search_page()
    elif "Alertas" in menu:
        alerts_page()
    elif "Uso" in menu:
        usage_page()
    elif "Configurações" in menu:
        settings_page()


def dashboard_page():
    """Dashboard page."""
    st.title("📊 Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Buscas Hoje", "12", "+3")
    with col2:
        st.metric("Alertas Ativos", "5", "0")
    with col3:
        st.metric("Produtos Monitorados", "23", "+2")
    with col4:
        st.metric("Economizado", "R$ 234", "+45")

    st.markdown("---")

    st.subheader("📈 Atividade Recente")
    st.info("Funcionalidade em desenvolvimento...")


def search_page():
    """Product search page."""
    st.title("🔍 Buscar Produtos")

    # Search form
    col1, col2 = st.columns([3, 1])

    with col1:
        query = st.text_input("", placeholder="Digite o produto que você procura...")

    with col2:
        category = st.selectbox(
            "Categoria",
            ["all", "eletronicos", "beleza", "brinquedos", "construcao", "pet"]
        )

    # Filters
    with st.expander("🔍 Filtros Avançados"):
        col1, col2, col3 = st.columns(3)

        with col1:
            min_price = st.number_input("Preço Mín (R$)", min_value=0, value=0)
        with col2:
            max_price = st.number_input("Preço Máx (R$)", min_value=0, value=1000)
        with col3:
            min_rating = st.slider("Avaliação Mín", 0.0, 5.0, 0.0, 0.5)

    if st.button("🔍 Buscar", use_container_width=True):
        if query:
            with st.spinner("Buscando produtos..."):
                try:
                    response = requests.get(
                        f"{API_V1}/products/search",
                        params={
                            "q": query,
                            "category": category,
                            "min_price": min_price if min_price > 0 else None,
                            "max_price": max_price if max_price < 1000 else None,
                            "min_rating": min_rating if min_rating > 0 else None
                        },
                        headers={"Authorization": f"Bearer {st.session_state.access_token}"}
                    )

                    if response.status_code == 200:
                        data = response.json()
                        products = data.get("products", [])

                        st.success(f"Encontrados {data.get('total', 0)} produtos")

                        for product in products:
                            with st.container():
                                col1, col2 = st.columns([1, 4])

                                with col1:
                                    if product.get("image_url"):
                                        st.image(product["image_url"], width=100)

                                with col2:
                                    st.subheader(product["title"][:80] + "...")
                                    st.write(f"💰 R$ {product.get('price', 'N/A')}")
                                    st.write(f"⭐ {product.get('rating', 'N/A')} ({product.get('num_ratings', 0)} avaliações)")

                                    if st.button("Ver no Amazon", key=product["asin"]):
                                        st.write(f"[Link]({product['product_url']})")

                                st.markdown("---")
                    else:
                        st.error(f"Erro na busca: {response.json().get('detail')}")

                except Exception as e:
                    st.error(f"Erro: {str(e)}")
        else:
            st.warning("Digite algo para buscar")


def alerts_page():
    """Alerts management page."""
    st.title("🔔 Meus Alertas")
    st.info("Funcionalidade em desenvolvimento...")


def usage_page():
    """Usage statistics page."""
    st.title("📊 Uso do Plano")

    try:
        response = requests.get(
            f"{API_V1}/subscriptions/usage",
            headers={"Authorization": f"Bearer {st.session_state.access_token}"}
        )

        if response.status_code == 200:
            data = response.json()

            st.subheader(f"Plano: {data['plan'].upper()}")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Buscas",
                    f"{data['searches_used']} / {data['searches_limit']}",
                    f"{data['searches_remaining']} restantes"
                )

            with col2:
                st.metric(
                    "Alertas",
                    f"{data['alerts_used']} / {data['alerts_limit']}",
                    f"{data['alerts_remaining']} restantes"
                )

            # Progress bars
            st.progress(data['searches_used'] / max(data['searches_limit'], 1))
            st.progress(data['alerts_used'] / max(data['alerts_limit'], 1))

        else:
            st.error("Erro ao carregar uso")

    except Exception as e:
        st.error(f"Erro: {str(e)}")


def settings_page():
    """Settings page."""
    st.title("⚙️ Configurações")
    st.info("Funcionalidade em desenvolvimento...")


def main():
    """Main application entry point."""
    init_session_state()

    if not is_authenticated():
        login_page()
    else:
        main_app()


if __name__ == "__main__":
    main()

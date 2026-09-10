import streamlit as st
import pandas as pd
import psycopg2

# 1. Configuración general de la página en modo ancho
st.set_page_config(
    page_title="Dashboard Operativo - Transportadores de Occidente",
    page_icon="🚌",
    layout="wide"
)

st.title("📊 Monitor Operativo: Transportadores de Occidente")
st.markdown("Consolidado central de redes, tiquetes y despachos de carga.")

# 2. Función segura de conexión a PostgreSQL usando los Secretos de Streamlit
@st.cache_data(ttl=300) # Los datos se actualizan en caché cada 5 minutos
def ejecutar_consulta(query):
    try:
        conn = psycopg2.connect(
            host=st.secrets["postgres"]["host"],
            port=st.secrets["postgres"]["port"],
            dbname=st.secrets["postgres"]["dbname"],
            user=st.secrets["postgres"]["user"],
            password=st.secrets["postgres"]["password"]
        )
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error al conectar con la base de datos central: {e}")
        return pd.DataFrame()

# 3. Estructura de Pestañas para organizar la visualización
pestana_resumen, pestana_tiquetes, pestana_carga = st.tabs([
    "📈 Resumen de Nodos", 
    "🎫 Módulo de Tiquetes", 
    "📦 Módulo de Carga"
])

with pestana_resumen:
    st.subheader("Estado de Conexión y Replicación por Sede")
    
    # Consulta de prueba para verificar esquemas o tablas disponibles en la BD
    # Nota: Puedes cambiar esta consulta por tu tabla real de logs (ej. SELECT * FROM log_replicacion)
    query_nodos = "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"
    df_nodos = ejecutar_consulta(query_nodos)
    
    if not df_nodos.empty:
        st.success("¡Conexión establecida correctamente con el servidor central!")
        st.dataframe(df_nodos, use_container_width=True)
    else:
        st.warning("No se encontraron registros o la consulta no arrojó resultados.")

with pestana_tiquetes:
    st.subheader("Control de Ventas de Pasajeros")
    st.info("Aquí puedes integrar la consulta SQL específica para las tablas de tiquetes y rutas.")
    # Ejemplo de estructura futura:
    # df_tiquetes = ejecutar_consulta("SELECT * FROM tiquetes_tabla WHERE fecha = CURRENT_DATE;")
    # st.dataframe(df_tiquetes)

with pestana_carga:
    st.subheader("Control de Despachos y Encomiendas")
    st.info("Aquí puedes integrar la consulta SQL para el peso facturado, guías y carga.")

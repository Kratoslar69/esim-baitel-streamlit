import streamlit as st
import pandas as pd
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import plotly.express as px
from datetime import datetime
import io
import requests
import time
from template_generator import generate_template, validate_import_data

# Cargar variables de entorno
load_dotenv()

# Configuración de la página
st.set_page_config(
    page_title="Sistema eSIM BAITEL",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL base del repositorio de QR
QR_BASE_URL = "https://raw.githubusercontent.com/Kratoslar69/esim-qr-baitel/main/"

# Inicializar modo oscuro en session_state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Inicializar vista por defecto
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = "Tarjetas"

# Colores BAITEL
BAITEL_YELLOW = "#FFD100"
BAITEL_BLUE = "#0089D0"
BAITEL_BLACK = "#000000"
BAITEL_WHITE = "#FFFFFF"

# Definir colores según modo
if st.session_state.dark_mode:
    BG_COLOR = "#1A1A1A"
    BG_SECONDARY = "#2C2C2C"
    TEXT_COLOR = "#FFFFFF"
    CARD_BG = "#2C2C2C"
    HEADER_GRADIENT = f"linear-gradient(135deg, {BAITEL_BLACK} 0%, {BAITEL_BLUE} 100%)"
else:
    BG_COLOR = "#FFFFFF"
    BG_SECONDARY = "#F5F5F5"
    TEXT_COLOR = "#000000"
    CARD_BG = "#FFFFFF"
    HEADER_GRADIENT = f"linear-gradient(135deg, {BAITEL_BLUE} 0%, {BAITEL_YELLOW} 100%)"

# CSS personalizado con colores BAITEL
st.markdown(f"""
<style>
    .main {{
        background-color: {BG_COLOR};
    }}
    .stApp {{
        background-color: {BG_COLOR};
    }}
    .block-container {{
        background-color: {BG_COLOR};
    }}
    div[data-testid="stMetricValue"] {{
        font-size: 28px;
        font-weight: bold;
        color: {TEXT_COLOR};
    }}
    div[data-testid="stMetricLabel"] {{
        color: {TEXT_COLOR};
    }}
    .stSelectbox label, .stTextInput label, .stMultiSelect label {{
        color: {TEXT_COLOR} !important;
    }}
    h1, h2, h3, h4, h5, h6, p, span, div {{
        color: {TEXT_COLOR};
    }}
    .qr-modal {{
        background: {CARD_BG};
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        max-width: 600px;
        margin: 0 auto;
        border: 1px solid {BG_SECONDARY};
    }}
    .qr-title {{
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 20px;
        color: {TEXT_COLOR};
    }}
    .qr-info {{
        background: {BG_SECONDARY};
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }}
    .qr-info-row {{
        display: flex;
        justify-content: space-between;
        padding: 10px 0;
        border-bottom: 1px solid {BG_SECONDARY};
    }}
    .qr-info-label {{
        font-weight: bold;
        color: {TEXT_COLOR};
    }}
    .qr-info-value {{
        color: {TEXT_COLOR};
    }}
</style>
""", unsafe_allow_html=True)

# Inicializar conexión a Supabase
@st.cache_resource
def init_supabase():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        st.error("❌ Error: Variables de entorno SUPABASE_URL y SUPABASE_KEY no configuradas")
        st.stop()
    
    try:
        client = create_client(url, key)
        return client
    except Exception as e:
        st.error(f"❌ Error conectando a Supabase: {str(e)}")
        st.stop()

supabase = init_supabase()

# Función para verificar si existe QR
def check_qr_exists(iccid):
    try:
        url = f"{QR_BASE_URL}{iccid}.png"
        response = requests.head(url, timeout=2)
        return response.status_code == 200
    except:
        return False

# Función para cargar datos
@st.cache_data(ttl=10)
def load_data():
    try:
        response = supabase.table('esim_data').select('*').order('id', desc=True).execute()
        if response.data:
            df = pd.DataFrame(response.data)
            return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error cargando datos: {str(e)}")
        return pd.DataFrame()

# Función para actualizar un registro
def update_record(record_id, updates):
    try:
        response = supabase.table('esim_data').update(updates).eq('id', record_id).execute()
        return True, "✅ Registro actualizado exitosamente"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

# Función para eliminar un registro
def delete_record(record_id):
    try:
        response = supabase.table('esim_data').delete().eq('id', record_id).execute()
        return True, "✅ Registro eliminado exitosamente"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

# Función para agregar un registro
def add_record(data):
    try:
        response = supabase.table('esim_data').insert(data).execute()
        return True, "✅ Registro agregado exitosamente"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

# Función para importar desde Excel/CSV
def import_from_file(file):
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        
        records = df.to_dict('records')
        response = supabase.table('esim_data').insert(records).execute()
        return True, f"✅ {len(records)} registros importados exitosamente"
    except Exception as e:
        return False, f"❌ Error importando: {str(e)}"

# Función para actualizar eSIM en Supabase
def update_esim(esim_id, asignado_a, estado):
    try:
        response = supabase.table('esim_data').update({
            'asignado_a': asignado_a,
            'estado': estado,
            'fecha_ultimo_cambio': datetime.now().isoformat()
        }).eq('id', esim_id).execute()
        return True, "✅ eSIM actualizada exitosamente"
    except Exception as e:
        return False, f"❌ Error al actualizar: {str(e)}"

# Función para mostrar QR con modal interactivo
def show_qr_modal(row):
    iccid = row['iccid']
    qr_url = f"{QR_BASE_URL}{iccid}.png"
    
    # Contenedor con fondo semi-transparente
    st.markdown("""
    <div style="background: rgba(0,0,0,0.5); padding: 20px; border-radius: 15px;">
    </div>
    """, unsafe_allow_html=True)
    
    # Título
    st.markdown(f"<h2 style='text-align: center; color: {TEXT_COLOR}; background: {CARD_BG}; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>{iccid}</h2>", unsafe_allow_html=True)
    
    # Imagen QR centrada
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            response = requests.get(qr_url)
            if response.status_code == 200:
                st.image(qr_url, use_container_width=True)
            else:
                st.warning(f"⚠️ No se encontró la imagen QR para {iccid}")
        except:
            st.error(f"❌ Error al cargar QR desde {qr_url}")
    
    # Información detallada
    st.markdown(f"<h3 style='text-align: center; margin-top: 20px; color: {TEXT_COLOR};'>Información Detallada</h3>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.write(f"**ICCID:** {row.get('iccid', 'N/A')}")
        st.write(f"**MSISDN:** {row.get('msisdn', 'N/A')}")
        st.write(f"**IMSI:** {row.get('imsi', 'N/A')}")
        st.write(f"**Serie:** {row.get('serie', 'N/A')}")
    
    with col_right:
        st.write(f"**PIN:** {row.get('pin', 'N/A')}")
        st.write(f"**PUK:** {row.get('puk', 'N/A')}")
        st.write(f"**IP:** {row.get('ip', 'N/A')}")
        st.write(f"**Producto:** {row.get('producto', 'N/A')}")
    
    st.divider()
    
    # Formulario de asignación
    st.markdown(f"<h3 style='text-align: center; color: {TEXT_COLOR};'>✏️ Asignar eSIM</h3>", unsafe_allow_html=True)
    
    current_asignado = row.get('asignado_a', '')
    current_estado = row.get('estado', 'Disponible')
    
    with st.form(key=f"form_assign_{row['id']}"):
        col_form1, col_form2 = st.columns(2)
        
        with col_form1:
            nuevo_asignado = st.text_input(
                "Asignar a:",
                value=current_asignado if current_asignado else "",
                placeholder="Ej: BT287, TIENDA, Cliente...",
                key=f"asignado_{row['id']}"
            )
        
        with col_form2:
            nuevo_estado = st.selectbox(
                "Estado:",
                ["Disponible", "Usado"],
                index=1 if current_estado == "Usado" else 0,
                key=f"estado_{row['id']}"
            )
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            submit = st.form_submit_button("💾 Guardar Cambios", use_container_width=True)
        
        with col_btn2:
            if st.form_submit_button("🗑️ Limpiar Asignación", use_container_width=True):
                nuevo_asignado = ""
                nuevo_estado = "Disponible"
                submit = True
        
        if submit:
            success, message = update_esim(row['id'], nuevo_asignado, nuevo_estado)
            if success:
                st.success(message)
                st.cache_data.clear()
                time.sleep(1)
                st.rerun()
            else:
                st.error(message)

# Header con toggle de modo oscuro
col_header, col_toggle_mode = st.columns([5, 1])

with col_header:
    st.markdown(f"""
    <div style='background: {HEADER_GRADIENT}; padding: 30px; border-radius: 15px; margin-bottom: 20px;'>
        <h1 style='color: white; text-align: center; margin: 0;'>🚀 Sistema eSIM BAITEL</h1>
        <p style='color: white; text-align: center; margin: 10px 0 0 0;'>Gestión de Inventario - Versión Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

with col_toggle_mode:
    st.write("")  # Espaciado
    st.write("")  # Espaciado
    mode_icon = "🌙" if st.session_state.dark_mode else "☀️"
    if st.button(f"{mode_icon} Modo {'Claro' if st.session_state.dark_mode else 'Oscuro'}", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# Cargar datos
df = load_data()

# Sidebar
with st.sidebar:
    st.header("🔧 Opciones")
    
    st.success("✅ Conectado a Supabase")
    
    if st.button("🔄 Actualizar Datos", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.divider()
    
    st.subheader("🔍 Filtros")
    
    filter_estado = st.selectbox(
        "Estado",
        ["Todos", "Disponible", "Usado"]
    )
    
    filter_producto = st.selectbox(
        "Producto",
        ["Todos", "MOV", "IP"]
    )
    
    filter_ip = st.multiselect(
        "IP",
        options=df['ip'].unique().tolist() if not df.empty else []
    )
    
    search_query = st.text_input("🔎 Buscar", placeholder="ICCID, MSISDN, Asignado a...")
    
    st.divider()
    
    st.subheader("📁 Importar/Exportar")
    
    # Descargar plantilla
    if st.button("📝 Descargar Plantilla Excel", use_container_width=True):
        template = generate_template()
        st.download_button(
            label="⬇️ Descargar Plantilla",
            data=template,
            file_name=f"plantilla_esim_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            help="Descarga esta plantilla, llénala con tus datos y súbela de nuevo"
        )
    
    # Exportar datos actuales
    if st.button("📊 Exportar Inventario Actual", use_container_width=True):
        if not df.empty:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='eSIM Data')
            output.seek(0)
            
            st.download_button(
                label="⬇️ Descargar Excel",
                data=output,
                file_name=f"esim_inventario_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
    
    st.divider()
    
    # Importar datos masivos
    st.markdown("**🚀 Carga Masiva**")
    uploaded_file = st.file_uploader(
        "Subir archivo Excel/CSV",
        type=['csv', 'xlsx'],
        help="Sube un archivo con el formato de la plantilla para agregar múltiples eSIMs"
    )
    
    if uploaded_file:
        try:
            # Leer archivo
            if uploaded_file.name.endswith('.csv'):
                import_df = pd.read_csv(uploaded_file)
            else:
                import_df = pd.read_excel(uploaded_file)
            
            # Validar datos
            is_valid, validation_msg = validate_import_data(import_df)
            
            if not is_valid:
                st.error(validation_msg)
            else:
                st.success(validation_msg)
                st.info(f"📄 {len(import_df)} registros listos para importar")
                
                # Mostrar preview
                with st.expander("👁️ Vista previa de datos"):
                    st.dataframe(import_df.head(10))
                
                # Botón para confirmar importación
                if st.button("✅ Confirmar e Importar", use_container_width=True, type="primary"):
                    with st.spinner("Importando datos..."):
                        try:
                            # Dividir en lotes de 1000 (límite de Supabase)
                            batch_size = 1000
                            total_imported = 0
                            
                            for i in range(0, len(import_df), batch_size):
                                batch = import_df.iloc[i:i+batch_size]
                                records = batch.to_dict('records')
                                
                                # Agregar timestamps si no existen
                                for record in records:
                                    if 'fecha_creacion' not in record or pd.isna(record['fecha_creacion']):
                                        record['fecha_creacion'] = datetime.now().isoformat()
                                    if 'fecha_ultimo_cambio' not in record or pd.isna(record['fecha_ultimo_cambio']):
                                        record['fecha_ultimo_cambio'] = datetime.now().isoformat()
                                
                                response = supabase.table('esim_data').insert(records).execute()
                                total_imported += len(records)
                            
                            st.success(f"✅ {total_imported} registros importados exitosamente")
                            st.cache_data.clear()
                            time.sleep(2)
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error al importar: {str(e)}")
        
        except Exception as e:
            st.error(f"❌ Error al leer archivo: {str(e)}")

# Aplicar filtros
filtered_df = df.copy()

if not filtered_df.empty:
    if filter_estado != "Todos":
        filtered_df = filtered_df[filtered_df['estado'] == filter_estado]
    
    if filter_producto != "Todos":
        filtered_df = filtered_df[filtered_df['producto'] == filter_producto]
    
    if filter_ip:
        filtered_df = filtered_df[filtered_df['ip'].isin(filter_ip)]
    
    if search_query:
        mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False, na=False)).any(axis=1)
        filtered_df = filtered_df[mask]

# Estadísticas principales
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📊 Total eSIM", len(df))

with col2:
    disponibles = len(df[df['estado'] == 'Disponible']) if not df.empty else 0
    st.metric("✅ Disponibles", disponibles)

with col3:
    usadas = len(df[df['estado'] == 'Usado']) if not df.empty else 0
    st.metric("🔴 Usadas", usadas)

with col4:
    st.metric("🔍 Filtrados", len(filtered_df))

st.divider()

# Tabs principales
tab1, tab2, tab3, tab4 = st.tabs(["📋 Tabla de Datos", "📊 Estadísticas", "➕ Agregar Nuevo", "📖 Instrucciones"])

with tab1:
    # Toggle para vista
    col_title, col_toggle = st.columns([3, 1])
    with col_title:
        st.subheader("📋 Inventario de eSIM")
    with col_toggle:
        view_mode = st.selectbox(
            "👁️ Vista",
            ["Tarjetas", "Lista"],
            index=0 if st.session_state.view_mode == "Tarjetas" else 1,
            label_visibility="collapsed"
        )
        st.session_state.view_mode = view_mode
    
    if not filtered_df.empty:
        if view_mode == "Lista":
            # Vista de lista (original)
            for idx, row in filtered_df.iterrows():
                with st.expander(f"📱 {row['iccid']} - {row['estado']} - {row.get('asignado_a', 'Sin asignar')}"):
                    col_info, col_qr = st.columns([2, 1])
                    
                    with col_info:
                        st.write(f"**MSISDN:** {row.get('msisdn', 'N/A')}")
                        st.write(f"**IMSI:** {row.get('imsi', 'N/A')}")
                        st.write(f"**Producto:** {row.get('producto', 'N/A')}")
                        st.write(f"**IP:** {row.get('ip', 'N/A')}")
                        st.write(f"**Estado:** {row.get('estado', 'N/A')}")
                        st.write(f"**Distribuidor:** {row.get('distribuidor', 'N/A')}")
                    
                    with col_qr:
                        if st.button(f"📱 Ver QR", key=f"qr_{row['id']}", use_container_width=True):
                            st.session_state[f'show_qr_{row["id"]}'] = True
                    
                    # Mostrar QR si se clickeó el botón
                    if st.session_state.get(f'show_qr_{row["id"]}', False):
                        show_qr_modal(row)
                        if st.button("❌ Cerrar QR", key=f"close_qr_{row['id']}"):
                            st.session_state[f'show_qr_{row["id"]}'] = False
                            st.rerun()
        
        else:
            # Vista de tarjetas (nueva)
            cols_per_row = 3  # 3 tarjetas por fila en desktop
            rows = [filtered_df.iloc[i:i+cols_per_row] for i in range(0, len(filtered_df), cols_per_row)]
            
            for row_data in rows:
                cols = st.columns(cols_per_row)
                for idx, (_, row) in enumerate(row_data.iterrows()):
                    with cols[idx]:
                        # Tarjeta con estilo
                        estado_color = "#27ae60" if row['estado'] == "Disponible" else "#e74c3c"
                        qr_url = f"{QR_BASE_URL}{row['iccid']}.png"
                        
                        st.markdown(f"""
                        <div style="
                            border: 2px solid {estado_color};
                            border-radius: 15px;
                            padding: 15px;
                            background: {CARD_BG};
                            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                            margin-bottom: 20px;
                            height: 100%;
                        ">
                            <div style="text-align: center; margin-bottom: 10px;">
                                <img src="{qr_url}" style="width: 150px; height: 150px; border-radius: 10px;" onerror="this.src='https://via.placeholder.com/150?text=QR+No+Disponible'">
                            </div>
                            <div style="background: {estado_color}; color: white; padding: 5px; border-radius: 5px; text-align: center; font-weight: bold; margin-bottom: 10px;">
                                {row['estado']}
                            </div>
                            <div style="font-size: 12px; color: {TEXT_COLOR};">
                                <strong>ICCID:</strong><br>{row['iccid'][:20]}...<br><br>
                                <strong>MSISDN:</strong> {row.get('msisdn', 'N/A')}<br>
                                <strong>Producto:</strong> {row.get('producto', 'N/A')}<br>
                                <strong>IP:</strong> {row.get('ip', 'N/A')}<br>
                                <strong>Asignado:</strong> {row.get('asignado_a', 'N/A')[:15]}...
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Botón para ver detalles
                        if st.button("🔍 Ver Detalles", key=f"card_{row['id']}", use_container_width=True):
                            st.session_state[f'show_qr_{row["id"]}'] = True
                        
                        # Mostrar modal si se clickeó
                        if st.session_state.get(f'show_qr_{row["id"]}', False):
                            show_qr_modal(row)
                            if st.button("❌ Cerrar", key=f"close_card_{row['id']}", use_container_width=True):
                                st.session_state[f'show_qr_{row["id"]}'] = False
                                st.rerun()
        
        st.info(f"💡 Mostrando {len(filtered_df)} de {len(df)} registros totales")
    else:
        st.warning("⚠️ No hay datos para mostrar")

with tab2:
    st.subheader("📊 Estadísticas y Gráficos")
    
    if not df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            estado_counts = df['estado'].value_counts()
            fig_estado = px.pie(
                values=estado_counts.values,
                names=estado_counts.index,
                title="Distribución por Estado",
                color_discrete_sequence=['#27ae60', '#e74c3c']
            )
            st.plotly_chart(fig_estado, use_container_width=True)
        
        with col2:
            producto_counts = df['producto'].value_counts()
            fig_producto = px.bar(
                x=producto_counts.index,
                y=producto_counts.values,
                title="Distribución por Producto",
                labels={'x': 'Producto', 'y': 'Cantidad'},
                color_discrete_sequence=['#3498db']
            )
            st.plotly_chart(fig_producto, use_container_width=True)
        
        st.subheader("Distribución por IP")
        ip_counts = df['ip'].value_counts().head(10)
        fig_ip = px.bar(
            x=ip_counts.index,
            y=ip_counts.values,
            title="Top 10 IPs con más eSIMs",
            labels={'x': 'IP', 'y': 'Cantidad'},
            color_discrete_sequence=['#9b59b6']
        )
        st.plotly_chart(fig_ip, use_container_width=True)
    else:
        st.warning("⚠️ No hay datos para generar estadísticas")

with tab3:
    st.subheader("➕ Agregar Nuevo Registro")
    
    with st.form("add_record_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            iccid = st.text_input("ICCID *")
            msisdn = st.text_input("MSISDN *")
            imsi = st.text_input("IMSI")
            pin = st.text_input("PIN", value="1234")
            puk = st.text_input("PUK")
            serie = st.text_input("Serie")
        
        with col2:
            asignado_a = st.text_input("Asignado a")
            distribuidor = st.text_input("Distribuidor", value="BAITEL")
            ip = st.text_input("IP")
            producto = st.selectbox("Producto *", ["MOV", "IP"])
            estado = st.selectbox("Estado *", ["Disponible", "Usado"])
        
        submitted = st.form_submit_button("➕ Agregar Registro", type="primary", use_container_width=True)
        
        if submitted:
            if not iccid or not msisdn:
                st.error("❌ ICCID y MSISDN son campos obligatorios")
            else:
                new_record = {
                    "iccid": iccid,
                    "msisdn": msisdn,
                    "imsi": imsi,
                    "pin": pin,
                    "puk": puk,
                    "serie": serie,
                    "asignado_a": asignado_a,
                    "distribuidor": distribuidor,
                    "ip": ip,
                    "producto": producto,
                    "estado": estado,
                    "fecha_creacion": datetime.now().strftime("%Y-%m-%d"),
                    "fecha_ultimo_cambio": datetime.now().isoformat()
                }
                
                success, message = add_record(new_record)
                if success:
                    st.success(message)
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error(message)

with tab4:
    st.subheader("📖 Instrucciones de Uso")
    
    st.markdown("""
    ### 🚀 Bienvenido al Sistema eSIM BAITEL
    
    Este sistema te permite gestionar tu inventario de eSIM de manera eficiente y confiable.
    
    #### 📋 Funcionalidades Principales:
    
    1. **Ver Inventario**: En la pestaña "Tabla de Datos" puedes ver todos tus registros
    2. **Ver Códigos QR**: Haz clic en "📱 Ver QR" para ver el código QR con toda la información
    3. **Filtrar Datos**: Usa los filtros en el panel lateral para encontrar registros específicos
    4. **Agregar Nuevos**: Ve a la pestaña "Agregar Nuevo" para crear registros
    5. **Importar/Exportar**: Usa los botones en el panel lateral para importar o exportar datos
    6. **Estadísticas**: Visualiza gráficos y métricas en la pestaña "Estadísticas"
    
    #### 📱 Códigos QR:
    
    - Los códigos QR se cargan automáticamente desde GitHub
    - Cada QR muestra toda la información detallada del eSIM
    - Los QR se pueden descargar haciendo clic derecho → Guardar imagen
    
    #### 🔄 Sincronización:
    
    - Los datos se guardan automáticamente en Supabase
    - Usa el botón "🔄 Actualizar Datos" para recargar la información
    - Todos los cambios son permanentes y se sincronizan en tiempo real
    
    #### 💡 Consejos:
    
    - Usa la búsqueda para encontrar rápidamente registros por ICCID, MSISDN, etc.
    - Exporta regularmente tus datos como respaldo
    - Los campos marcados con * son obligatorios
    
    #### 🆘 Soporte:
    
    Si tienes problemas, verifica que la conexión a Supabase esté activa (indicador verde en el panel lateral).
    """)

# Footer
st.divider()
st.markdown(f"""
<div style='text-align: center; color: {TEXT_COLOR}; padding: 20px;'>
    <p>Sistema eSIM BAITEL - Versión Streamlit | Conectado a Supabase ✅</p>
</div>
""", unsafe_allow_html=True)

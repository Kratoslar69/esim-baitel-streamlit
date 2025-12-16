# Sistema eSIM BAITEL - Streamlit

Sistema de gestión de inventario de eSIM construido con Streamlit y Supabase.

## 🚀 Características

- ✅ Gestión completa de inventario eSIM
- ✅ Conexión directa a Supabase
- ✅ Importar/Exportar Excel y CSV
- ✅ Filtros y búsqueda avanzada
- ✅ Estadísticas y gráficos en tiempo real
- ✅ Edición inline de registros
- ✅ 100% estable y confiable

## 📋 Requisitos

- Python 3.11+
- Cuenta de Supabase
- Cuenta de Railway (para despliegue)

## 🔧 Instalación Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales de Supabase

# Ejecutar aplicación
streamlit run app.py
```

## 🚂 Despliegue en Railway

### Opción 1: Desde GitHub

1. Sube este proyecto a tu repositorio de GitHub
2. Ve a [Railway.app](https://railway.app)
3. Crea un nuevo proyecto
4. Selecciona "Deploy from GitHub repo"
5. Selecciona tu repositorio
6. Agrega las variables de entorno:
   - `SUPABASE_URL`: Tu URL de Supabase
   - `SUPABASE_KEY`: Tu clave anónima de Supabase
7. Railway detectará automáticamente el Procfile y desplegará

### Opción 2: Desde Railway CLI

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Inicializar proyecto
railway init

# Agregar variables de entorno
railway variables set SUPABASE_URL=https://tu-proyecto.supabase.co
railway variables set SUPABASE_KEY=tu-clave-anonima

# Desplegar
railway up
```

## 🔐 Variables de Entorno

- `SUPABASE_URL`: URL de tu proyecto Supabase
- `SUPABASE_KEY`: Clave anónima de Supabase (anon/public key)

## 📊 Estructura del Proyecto

```
esim-baitel-streamlit/
├── app.py                 # Aplicación principal
├── requirements.txt       # Dependencias Python
├── Procfile              # Configuración Railway
├── .env.example          # Ejemplo de variables de entorno
├── .streamlit/
│   └── config.toml       # Configuración de Streamlit
└── README.md             # Este archivo
```

## 🆘 Soporte

Para problemas o preguntas, contacta al equipo de desarrollo.

## 📝 Licencia

Propiedad de BAITEL

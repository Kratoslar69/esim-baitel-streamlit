# 🚂 Guía de Despliegue en Railway

## 📋 Requisitos Previos

- ✅ Cuenta de Railway (https://railway.app)
- ✅ Cuenta de GitHub (ya conectada)
- ✅ Credenciales de Supabase (URL y clave anónima)

---

## 🚀 Pasos para Desplegar

### 1️⃣ Acceder a Railway

1. Ve a https://railway.app
2. Inicia sesión con tu cuenta de GitHub
3. Haz clic en **"New Project"**

### 2️⃣ Conectar el Repositorio

1. Selecciona **"Deploy from GitHub repo"**
2. Busca y selecciona el repositorio: **`esim-baitel-streamlit`**
3. Haz clic en **"Deploy Now"**

Railway detectará automáticamente:
- ✅ El archivo `Procfile`
- ✅ El archivo `requirements.txt`
- ✅ Python como lenguaje

### 3️⃣ Configurar Variables de Entorno

**IMPORTANTE:** Debes agregar las credenciales de Supabase como variables de entorno.

1. En el dashboard de Railway, haz clic en tu proyecto
2. Ve a la pestaña **"Variables"**
3. Agrega las siguientes variables:

```
SUPABASE_URL=https://owlqjsiyyqblgyxuevvg.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im93bHFqc2l5eXFibGd5eHVldnZnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTcyNzQ1MzgsImV4cCI6MjA3Mjg1MDUzOH0.xOrQeCDrWSTXLPJWbColCV9fFzaFVYOkJvROr1NoyR4
```

4. Haz clic en **"Add"** para cada variable

### 4️⃣ Configurar el Puerto (Opcional)

Railway asigna automáticamente un puerto mediante la variable `$PORT`. El `Procfile` ya está configurado para usar esta variable, así que **no necesitas hacer nada adicional**.

### 5️⃣ Esperar el Despliegue

1. Railway comenzará a construir y desplegar automáticamente
2. Verás los logs en tiempo real
3. El proceso toma aproximadamente **2-3 minutos**

Busca este mensaje en los logs:
```
You can now view your Streamlit app in your browser.
```

### 6️⃣ Obtener la URL Pública

1. En el dashboard de Railway, ve a la pestaña **"Settings"**
2. En la sección **"Domains"**, haz clic en **"Generate Domain"**
3. Railway generará una URL pública como:
   ```
   https://esim-baitel-streamlit-production.up.railway.app
   ```
4. ¡Copia esta URL y accede a tu sistema!

---

## ✅ Verificación

Una vez desplegado, deberías ver:

- ✅ Título: **"🚀 Sistema eSIM BAITEL"**
- ✅ Estado de conexión: **"✅ Conectado a Supabase"**
- ✅ Total de eSIM: **300**
- ✅ Disponibles: **17**
- ✅ Usadas: **283**

---

## 🔄 Actualizar el Sistema

Cada vez que hagas cambios en el código:

1. Haz commit y push a GitHub:
   ```bash
   git add .
   git commit -m "Descripción de cambios"
   git push origin master
   ```

2. Railway detectará automáticamente los cambios y **redesplegará** el sistema

---

## 🆘 Solución de Problemas

### Error: "Application failed to respond"

**Solución:** Verifica que las variables de entorno estén configuradas correctamente.

### Error: "No module named 'streamlit'"

**Solución:** Asegúrate de que `requirements.txt` esté en la raíz del repositorio.

### Error de conexión a Supabase

**Solución:** 
1. Verifica que `SUPABASE_URL` y `SUPABASE_KEY` estén correctamente configuradas
2. Asegúrate de que no haya espacios en blanco al inicio o final de las variables

### La aplicación se carga muy lento

**Solución:** Railway puede tardar un poco en el primer arranque. Espera 1-2 minutos.

---

## 💰 Costos

Railway ofrece:
- ✅ **$5 USD de crédito gratis** cada mes
- ✅ **500 horas de ejecución gratis** para proyectos pequeños

Para este proyecto (Streamlit + Supabase), el costo estimado es:
- **~$5-10 USD/mes** si está activo 24/7
- **Gratis** si solo lo usas ocasionalmente (dentro del crédito mensual)

**Tip:** Puedes configurar el proyecto para que se duerma después de 30 minutos de inactividad y ahorrar costos.

---

## 📊 Monitoreo

En el dashboard de Railway puedes ver:
- 📈 Uso de CPU y memoria
- 📝 Logs en tiempo real
- 🔄 Historial de despliegues
- 💰 Uso de créditos

---

## 🎉 ¡Listo!

Tu sistema eSIM BAITEL ahora está desplegado en Railway y es accesible desde cualquier lugar del mundo.

**URL del repositorio:** https://github.com/Kratoslar69/esim-baitel-streamlit

**Próximos pasos:**
1. Comparte la URL con tu equipo
2. Configura un dominio personalizado (opcional)
3. Activa HTTPS automático (Railway lo hace por defecto)

---

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en Railway
2. Verifica que Supabase esté funcionando
3. Contacta al equipo de desarrollo

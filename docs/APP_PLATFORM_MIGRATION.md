# Migración a Digital Ocean App Platform

## ¿Por qué migrar?

**Problemas del Droplet actual:**
- ❌ Gunicorn timeout de 60s mata el proceso de generación de PDFs
- ❌ Pagar $18/mes por servidor que solo se usa esporádicamente
- ❌ Mantenimiento manual: nginx, supervisor, SSL, actualizaciones
- ❌ No escala automáticamente

**Ventajas de App Platform:**
- ✅ Timeout configurable de 120s (suficiente para PDFs)
- ✅ Auto-sleep cuando no hay tráfico = **ahorro de costos**
- ✅ Plan básico desde **$5/mes** (vs $18/mes droplet)
- ✅ Deploy automático desde GitHub
- ✅ SSL/HTTPS automático
- ✅ Menos mantenimiento

## Costo Estimado

- **Droplet actual**: $18/mes (2 vCPUs, siempre activo)
- **App Platform**: 
  - Basic ($5/mes): 512MB RAM, auto-sleep
  - Professional ($12/mes): 1GB RAM, siempre activo
  
**Recomendación**: Empezar con Basic ($5/mes). Si el cold start molesta, upgrade a Professional.

## Pasos de Migración

### 1. Preparar el repositorio (✅ HECHO)

Los siguientes archivos ya están creados:
- `.do/app.yaml` - Configuración de App Platform
- `Procfile` - Comando de inicio
- `runtime.txt` - Versión de Python

### 2. Commit y push al repositorio

```bash
cd /Users/1di/Music_Bingo
git add .do/ Procfile runtime.txt
git commit -m "Configure Digital Ocean App Platform deployment"
git push origin main
```

### 3. Crear App en Digital Ocean

**Opción A: Usando doctl CLI**
```bash
doctl apps create --spec .do/app.yaml
```

**Opción B: Desde la web**
1. Ir a https://cloud.digitalocean.com/apps
2. Click "Create App"
3. Seleccionar GitHub → repo `1di210299/Music_Bingo`
4. Digital Ocean detectará automáticamente el `app.yaml`
5. Configurar variables de entorno:
   - `ELEVENLABS_API_KEY` (secret)
   - `OPENAI_API_KEY` (secret)
6. Click "Create Resources"

### 4. Migrar datos

Los datos persistentes (logos, pool.json) necesitan migrarse:

```bash
# Descargar datos del droplet
scp -r root@134.209.183.139:/var/www/music-bingo/data/ ./data_backup/

# Los datos se servirán desde el repo (ya están en ./data/)
# Verificar que estén en el repo:
ls -la data/logos/
```

**IMPORTANTE**: App Platform no tiene almacenamiento persistente. Las opciones son:

**Opción 1: Spaces (Object Storage)** - Recomendado para producción
- Crear un Space en Digital Ocean ($5/mes por 250GB)
- Actualizar `server.py` para subir logos a Spaces
- URLs permanentes, no se pierden con redeploys

**Opción 2: Commit al repo** - Más simple, para desarrollo
- Los logos se guardan en `data/logos/` y se hace commit
- Funciona pero no es ideal para producción

**Opción 3: Mount de volumen** - Solo en Professional ($12/mes)
- Persistencia real del filesystem

### 5. Actualizar DNS (si aplica)

Si tienes un dominio:
```bash
# App Platform te dará una URL tipo: music-bingo-xxxxx.ondigitalocean.app
# Actualiza tu DNS CNAME para apuntar ahí
```

### 6. Probar la aplicación

Una vez desplegada:
1. Visita la URL de App Platform
2. Prueba el setup inicial
3. Genera PDFs (debería tomar ~25-30s sin timeout)
4. Verifica que los logos se suban correctamente

### 7. Eliminar el droplet antiguo

```bash
# Hacer backup final
ssh root@134.209.183.139 'tar -czf /tmp/music-bingo-backup.tar.gz /var/www/music-bingo'
scp root@134.209.183.139:/tmp/music-bingo-backup.tar.gz ./

# Destruir droplet (recuperas $18/mes)
doctl compute droplet delete 542445355
```

## Próximos pasos

1. **Decidir sobre almacenamiento de logos**:
   - ¿Usar Spaces ($5/mes extra) para persistencia?
   - ¿O commit al repo (más simple)?

2. **Commit y push** los archivos de configuración

3. **Crear la App** en Digital Ocean

4. **Migrar datos** según la opción elegida

5. **Probar** la generación de PDFs

6. **Eliminar droplet** y ahorrar $13/mes

## Comandos Rápidos

```bash
# Commit configuración
git add .do/ Procfile runtime.txt
git commit -m "Configure App Platform with 120s timeout"
git push

# Crear app (CLI)
doctl apps create --spec .do/app.yaml

# Ver apps
doctl apps list

# Ver logs
doctl apps logs <app-id> --type=run

# Destruir droplet viejo
doctl compute droplet delete 542445355
```

## Estimación de Tiempo

- Configuración: ✅ 5 min (ya hecho)
- Commit y push: 1 min
- Crear app en DO: 5-10 min (build + deploy)
- Migrar datos: 5 min
- Probar: 5 min
- **Total: ~20-25 minutos**

## Costos Finales

- **Antes**: $18/mes (droplet 2 vCPUs)
- **Después**: $5/mes (App Platform Basic) o $12/mes (Professional)
- **Ahorro**: $13/mes (Basic) o $6/mes (Professional)
- **Ahorro anual**: $156 (Basic) o $72 (Professional)

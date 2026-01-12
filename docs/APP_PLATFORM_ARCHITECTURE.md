# App Platform - Dos Servicios Separados

## Arquitectura

```
┌─────────────────────────────────────────┐
│  Digital Ocean App Platform             │
├─────────────────────────────────────────┤
│                                          │
│  ┌────────────┐        ┌─────────────┐  │
│  │  Frontend  │◄───────┤   Backend   │  │
│  │  Service   │  API   │   Service   │  │
│  │ (Python)   │        │  (Flask)    │  │
│  │ port 8080  │        │  port 8080  │  │
│  └────────────┘        └─────────────┘  │
│       │                      │           │
│       │                      │           │
│    Static HTML          API Routes      │
│    CSS, JS             /api/*            │
│                        /data/*           │
└─────────────────────────────────────────┘
```

## Servicios

### 1. Backend Service
- **Lenguaje**: Python + Flask
- **Puerto**: 8080
- **Rutas**: `/api/*`, `/data/*`
- **Timeout**: 120s (suficiente para PDFs)
- **Workers**: 2 gunicorn workers
- **Variables**:
  - `ELEVENLABS_API_KEY` (secret)
  - `OPENAI_API_KEY` (secret)
  - `ELEVENLABS_VOICE_ID`
  - `VENUE_NAME`

### 2. Frontend Service
- **Servidor**: Python HTTP Server
- **Puerto**: 8080
- **Rutas**: `/` (catchall)
- **Variables**:
  - `BACKEND_URL`: URL pública del backend (auto-inyectada)
- **Startup**: `start.sh` reemplaza placeholders con URL real del backend

## Flujo de Deploy

1. **Push a GitHub** → Trigger automático
2. **Backend build**:
   - `pip install -r backend/requirements.txt`
   - Inicia gunicorn con timeout 120s
3. **Frontend build**:
   - Copia archivos estáticos
   - Ejecuta `start.sh` que:
     - Reemplaza `BACKEND_URL_PLACEHOLDER` con URL real
     - Inicia HTTP server en puerto 8080
4. **App Platform asigna URLs**:
   - `https://frontend-xxxxx.ondigitalocean.app/` → Frontend
   - `https://backend-xxxxx.ondigitalocean.app/` → Backend (interno)

## Ventajas vs Droplet

| Feature | Droplet ($18/mo) | App Platform ($5/mo x2) |
|---------|------------------|-------------------------|
| **Costo** | $18/mes | $10/mes (2 servicios Basic) |
| **Timeout** | 60s (problema) | 120s configurables ✅ |
| **Auto-sleep** | No | Sí (ahorra dinero) |
| **SSL/HTTPS** | Manual | Automático ✅ |
| **Deploy** | SSH + git pull | GitHub push automático ✅ |
| **Mantenimiento** | nginx, supervisor | Cero ✅ |
| **Escalado** | Manual | Automático ✅ |

## Costos Detallados

### Basic Plan (Recomendado para empezar)
- Frontend: $5/mes (512MB RAM, auto-sleep)
- Backend: $5/mes (512MB RAM, auto-sleep)
- **Total: $10/mes** (ahorro de $8/mes vs droplet)

### Professional Plan (Si cold start molesta)
- Frontend: $12/mes (1GB RAM, siempre activo)
- Backend: $12/mes (1GB RAM, siempre activo)
- **Total: $24/mes** (costo adicional de $6/mes, pero mejor performance)

### Híbrido (Óptimo)
- Frontend: $5/mes (Basic, auto-sleep ok)
- Backend: $12/mes (Professional, siempre disponible)
- **Total: $17/mes** (similar al droplet, pero mejor)

## Archivos Creados

- ✅ `.do/app.yaml` - Configuración de App Platform (2 servicios)
- ✅ `Procfile` - Comando de gunicorn para backend
- ✅ `runtime.txt` - Python 3.11
- ✅ `frontend/start.sh` - Script de inicio del frontend
- ✅ `frontend/config.js` - Detecta URL del backend automáticamente
- ✅ `frontend/index.html` - HTML con placeholder para BACKEND_URL

## Próximos Pasos

### 1. Commit y Push
```bash
cd /Users/1di/Music_Bingo
git add .do/ Procfile runtime.txt frontend/start.sh frontend/config.js frontend/index.html
git commit -m "Configure App Platform: separate frontend/backend services with 120s timeout"
git push origin main
```

### 2. Crear App en Digital Ocean

**Opción CLI:**
```bash
doctl apps create --spec .do/app.yaml
```

**Opción Web:**
1. https://cloud.digitalocean.com/apps
2. "Create App" → GitHub → `1di210299/Music_Bingo`
3. Digital Ocean detecta `app.yaml` automáticamente
4. Configurar secrets:
   - `ELEVENLABS_API_KEY`
   - `OPENAI_API_KEY`
5. Deploy (tarda ~10 min)

### 3. Migrar Datos

Los logos están en `data/logos/`. Dos opciones:

**Opción A: Commit al repo** (más simple)
```bash
git add data/logos/
git commit -m "Add existing logos for App Platform"
git push
```

**Opción B: Digital Ocean Spaces** (mejor para producción)
- Crear Space ($5/mo extra)
- Actualizar `server.py` para usar Spaces SDK
- URLs persistentes entre deploys

### 4. Probar

Una vez desplegado:
1. Visita URL del frontend: `https://frontend-xxxxx.ondigitalocean.app/`
2. Setup inicial con nuevo logo
3. Generar PDFs (debería tomar ~25-30s sin errores)

### 5. Eliminar Droplet

```bash
# Backup final
ssh root@134.209.183.139 'tar -czf /tmp/backup.tar.gz /var/www/music-bingo'
scp root@134.209.183.139:/tmp/backup.tar.gz ./

# Destruir (recuperas $18/mes)
doctl compute droplet delete 542445355
```

## Ventajas de Esta Arquitectura

✅ **Frontend y Backend separados** = deploy independiente
✅ **Timeout de 120s** = PDFs generan sin problemas
✅ **Auto-sleep** = Solo pagas cuando se usa
✅ **$10/mes** = Ahorro de $8/mes vs droplet actual
✅ **SSL automático** = HTTPS sin configuración
✅ **Git deploy** = Push → Deploy automático
✅ **Escalable** = Fácil upgrade a Professional si se necesita

## Troubleshooting

**Si el backend no conecta:**
```bash
# Ver logs del backend
doctl apps logs <app-id> --type=run --component=backend

# Ver variables de entorno
doctl apps list-components <app-id>
```

**Si el frontend no muestra datos:**
- Verificar que `window.BACKEND_URL` esté configurado (inspeccionar en browser)
- Revisar CORS en `server.py` (ya está configurado)

**Si hay timeout aún:**
- Verificar que gunicorn use `--timeout 120`
- Escalar backend a Professional (más CPU = más rápido)

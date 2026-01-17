# Jingle Manager - Lista de Tareas de Implementación

**Fecha:** 16 de enero de 2026  
**Proyecto:** Music Bingo - Jingle Scheduling System  
**Tiempo Estimado Total:** 8-10 horas  

---

## 📋 Resumen del Proyecto

Implementar un sistema de gestión de jingles con programación avanzada basada en:
- ✅ Nombre del jingle
- ✅ Rango de fechas (inicio/fin)
- ✅ Periodo de tiempo del día (HH:MM - HH:MM)
- ✅ Días de la semana específicos (M, T, W, Th, F, Sa, Su)
- ✅ Patrón de repetición (Occasional, Regular, Often)

---

## 🎯 FASE 1: Backend - Base de Datos y API
**Tiempo Estimado:** 2-3 horas

### Tarea 1: Crear Modelo Django `JingleSchedule`
**Archivo:** `backend/api/models.py`

**Descripción:**
- Crear modelo con todos los campos necesarios:
  - `jingle_name` (CharField, max 200)
  - `jingle_filename` (CharField, max 255)
  - `start_date` (DateField)
  - `end_date` (DateField, nullable)
  - `time_start` (TimeField, nullable)
  - `time_end` (TimeField, nullable)
  - `monday`, `tuesday`, `wednesday`, `thursday`, `friday`, `saturday`, `sunday` (BooleanField)
  - `repeat_pattern` (CharField con choices: occasional, regular, often)
  - `enabled` (BooleanField)
  - `priority` (IntegerField, 0-100)
  - `created_at`, `updated_at` (DateTimeField)

**Métodos del modelo:**
- `is_active_now()` - Evalúa si el horario está activo en el momento actual
- `get_interval()` - Retorna el intervalo de rounds según el patrón

**Código de Referencia:**
Ver `docs/JINGLE_MANAGER_DESIGN.md` sección "Database Schema"

---

### Tarea 2: Crear y Ejecutar Migraciones
**Comandos:**
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

**Verificación:**
```bash
python manage.py dbshell
.tables  # Debería mostrar api_jingleschedule
.schema api_jingleschedule
```

---

### Tarea 3: Crear Endpoint `POST /api/jingle-schedules`
**Archivo:** `backend/api/views.py`

**Descripción:**
- Crear vista `create_jingle_schedule(request)`
- Validar todos los campos requeridos
- Crear instancia de JingleSchedule
- Retornar ID del schedule creado

**Request Body:**
```json
{
  "jingle_name": "Tuesday Night Taco Promotion",
  "jingle_filename": "jingle_67890.mp3",
  "start_date": "2026-01-14",
  "end_date": "2026-03-31",
  "time_start": "17:00",
  "time_end": "22:00",
  "days_of_week": {
    "monday": false,
    "tuesday": true,
    "wednesday": false,
    "thursday": false,
    "friday": false,
    "saturday": false,
    "sunday": false
  },
  "repeat_pattern": "regular",
  "enabled": true,
  "priority": 10
}
```

**Response:**
```json
{
  "success": true,
  "schedule_id": 1,
  "message": "Schedule created successfully"
}
```

---

### Tarea 4: Crear Endpoint `GET /api/jingle-schedules`
**Archivo:** `backend/api/views.py`

**Descripción:**
- Crear vista `list_jingle_schedules(request)`
- Obtener todos los schedules ordenados por prioridad
- Incluir campo `is_active_now` calculado
- Serializar y retornar

**Response:**
```json
{
  "schedules": [
    {
      "id": 1,
      "jingle_name": "Tuesday Night Taco Promotion",
      "jingle_filename": "jingle_67890.mp3",
      "start_date": "2026-01-14",
      "end_date": "2026-03-31",
      "time_start": "17:00",
      "time_end": "22:00",
      "days_of_week": {...},
      "repeat_pattern": "regular",
      "enabled": true,
      "priority": 10,
      "is_active_now": true,
      "interval": 6,
      "created_at": "2026-01-16T10:00:00Z"
    }
  ]
}
```

---

### Tarea 5: Crear Endpoint `GET /api/jingle-schedules/active`
**Archivo:** `backend/api/views.py`

**Descripción:**
- Crear vista `get_active_jingles(request)`
- Filtrar schedules por `enabled=True`
- Llamar `is_active_now()` en cada uno
- Retornar solo los activos con su intervalo
- Ordenar por prioridad (descendente)

**Response:**
```json
{
  "active_jingles": [
    {
      "id": 1,
      "jingle_name": "Tuesday Night Taco Promotion",
      "jingle_filename": "jingle_67890.mp3",
      "interval": 6,
      "priority": 10
    }
  ]
}
```

**Lógica de Evaluación:**
1. Verificar fecha actual entre `start_date` y `end_date`
2. Verificar hora actual entre `time_start` y `time_end` (si están definidos)
3. Verificar día de la semana contra booleanos
4. Verificar `enabled=True`

---

### Tarea 6: Crear Endpoint `PUT /api/jingle-schedules/<id>`
**Archivo:** `backend/api/views.py`

**Descripción:**
- Crear vista `update_jingle_schedule(request, schedule_id)`
- Buscar schedule por ID
- Actualizar campos proporcionados
- Retornar schedule actualizado

**Request Body (parcial):**
```json
{
  "enabled": false
}
```

**Response:**
```json
{
  "success": true,
  "message": "Schedule updated successfully"
}
```

---

### Tarea 7: Crear Endpoint `DELETE /api/jingle-schedules/<id>`
**Archivo:** `backend/api/views.py`

**Descripción:**
- Crear vista `delete_jingle_schedule(request, schedule_id)`
- Buscar schedule por ID
- Eliminar de la base de datos
- Retornar confirmación

**Response:**
```json
{
  "success": true,
  "message": "Schedule deleted successfully"
}
```

---

### Tarea Extra: Actualizar URLs
**Archivo:** `backend/api/urls.py`

**Agregar:**
```python
# Jingle Schedule Management
path('jingle-schedules', views.list_jingle_schedules, name='list-schedules'),
path('jingle-schedules/create', views.create_jingle_schedule, name='create-schedule'),
path('jingle-schedules/active', views.get_active_jingles, name='active-schedules'),
path('jingle-schedules/<int:schedule_id>', views.update_jingle_schedule, name='update-schedule'),
path('jingle-schedules/<int:schedule_id>/delete', views.delete_jingle_schedule, name='delete-schedule'),
```

---

## 🎨 FASE 2: Frontend - Interfaz de Usuario
**Tiempo Estimado:** 3-4 horas

### Tarea 8: Crear Página `jingle-manager.html`
**Archivo:** `frontend/jingle-manager.html`

**Estructura:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Jingle Manager - Music Bingo</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>🎵 Jingle Manager</h1>
            <p>Schedule when your jingles play during games</p>
        </header>
        
        <div class="actions">
            <button id="createScheduleBtn">+ Create New Schedule</button>
            <a href="/game">← Back to Game</a>
            <a href="/jingle">→ Jingle Generator</a>
        </div>
        
        <div id="schedulesList">
            <!-- Schedules will be loaded here -->
        </div>
        
        <!-- Create/Edit Modal -->
        <div id="scheduleModal" class="modal hidden">
            <!-- Form will be here -->
        </div>
    </div>
    
    <script src="config.js"></script>
    <script src="jingle-manager.js"></script>
</body>
</html>
```

**Vista de Lista:**
- Card por cada schedule
- Badge verde si está activo ahora
- Botones: Preview, Edit, Delete, Toggle
- Mostrar info: nombre, fechas, días, horario, patrón

---

### Tarea 9: Construir Formulario Crear/Editar
**Archivo:** `frontend/jingle-manager.html` (dentro del modal)

**Campos del Formulario:**

1. **Jingle Name** (text input)
2. **Select Jingle Audio** (dropdown desde librería)
3. **Start Date** (date picker)
4. **End Date** (date picker + checkbox "No end date")
5. **Time Start** (time picker + checkbox "All day")
6. **Time End** (time picker)
7. **Days of Week** (7 checkboxes: M, T, W, Th, F, Sa, Su)
8. **Repeat Pattern** (radio buttons: Occasional, Regular, Often)
9. **Priority** (number input o slider 0-100)
10. **Enabled** (toggle switch)

**Botones:**
- Cancel
- Save Schedule

---

### Tarea 10: Agregar Date/Time Pickers y Day Checkboxes
**Archivo:** `frontend/jingle-manager.html`

**Date Picker (HTML5 nativo):**
```html
<input type="date" id="startDate" required>
```

**Time Picker (HTML5 nativo):**
```html
<input type="time" id="timeStart">
```

**Day Checkboxes:**
```html
<div class="days-selector">
    <label><input type="checkbox" name="monday"> M</label>
    <label><input type="checkbox" name="tuesday"> T</label>
    <label><input type="checkbox" name="wednesday"> W</label>
    <label><input type="checkbox" name="thursday"> Th</label>
    <label><input type="checkbox" name="friday"> F</label>
    <label><input type="checkbox" name="saturday"> Sa</label>
    <label><input type="checkbox" name="sunday"> Su</label>
</div>
```

**Estilos CSS:**
- Botones de día con estilo toggle (gris/verde)
- Date/time inputs con buen padding
- Responsive layout

---

### Tarea 11: Agregar Selector de Patrón de Repetición
**Archivo:** `frontend/jingle-manager.html`

**HTML:**
```html
<div class="repeat-pattern">
    <label>
        <input type="radio" name="pattern" value="occasional">
        Occasional - Every 8-10 rounds
    </label>
    <label>
        <input type="radio" name="pattern" value="regular" checked>
        Regular - Every 5-7 rounds
    </label>
    <label>
        <input type="radio" name="pattern" value="often">
        Often - Every 3-4 rounds
    </label>
</div>
```

**Descripción visual:**
- Mostrar frecuencia estimada
- Ayuda contextual

---

### Tarea 12: Crear `jingle-manager.js` con CRUD
**Archivo:** `frontend/jingle-manager.js`

**Funciones Principales:**

```javascript
// State
let schedules = [];
let editingScheduleId = null;

// Initialization
document.addEventListener('DOMContentLoaded', () => {
    loadSchedules();
    setupEventListeners();
});

// API Calls
async function loadSchedules() {
    // GET /api/jingle-schedules
    // Display in list
}

async function createSchedule(scheduleData) {
    // POST /api/jingle-schedules
}

async function updateSchedule(scheduleId, scheduleData) {
    // PUT /api/jingle-schedules/<id>
}

async function deleteSchedule(scheduleId) {
    // DELETE /api/jingle-schedules/<id>
}

// UI Functions
function displaySchedules(schedules) {
    // Render schedule cards
}

function showScheduleModal(scheduleId = null) {
    // Open modal for create/edit
}

function hideScheduleModal() {
    // Close modal
}

function getFormData() {
    // Extract form values
    // Return schedule object
}

function setFormData(schedule) {
    // Populate form with schedule data
}

// Event Handlers
function setupEventListeners() {
    document.getElementById('createScheduleBtn').addEventListener('click', () => {
        showScheduleModal();
    });
    
    document.getElementById('saveScheduleBtn').addEventListener('click', async () => {
        const data = getFormData();
        if (editingScheduleId) {
            await updateSchedule(editingScheduleId, data);
        } else {
            await createSchedule(data);
        }
        hideScheduleModal();
        loadSchedules();
    });
}
```

**Validaciones:**
- Start date no puede ser después de end date
- Time start no puede ser después de time end
- Al menos un día debe estar seleccionado
- Jingle filename debe existir

---

## 🔗 FASE 3: Integración con el Juego
**Tiempo Estimado:** 1-2 horas

### Tarea 13: Actualizar `checkAndPlayJingle()` en game.js
**Archivo:** `frontend/game.js`

**Cambios:**

**ANTES:**
```javascript
async function checkAndPlayJingle() {
    if (!jinglePlaylist.enabled || jinglePlaylist.jingles.length === 0) {
        return;
    }
    
    const songsPlayed = gameState.called.length;
    
    if (songsPlayed > 0 && songsPlayed % jinglePlaylist.interval === 0) {
        const jingleFilename = jinglePlaylist.jingles[jinglePlaylist.currentIndex];
        await playJingleAudio(jingleFilename);
        jinglePlaylist.currentIndex = (jinglePlaylist.currentIndex + 1) % jinglePlaylist.jingles.length;
    }
}
```

**DESPUÉS:**
```javascript
async function checkAndPlayJingle() {
    // Fetch active schedules from backend
    const activeSchedules = await fetchActiveJingles();
    
    if (activeSchedules.length === 0) {
        console.log('No active jingle schedules');
        return;
    }
    
    const songsPlayed = gameState.called.length;
    
    // Check each schedule to see if it should play
    for (const schedule of activeSchedules) {
        const shouldPlay = (songsPlayed > 0 && songsPlayed % schedule.interval === 0);
        
        if (shouldPlay) {
            console.log(`🎵 Playing scheduled jingle: ${schedule.jingle_name}`);
            
            updateStatus('🎵 Playing promotional jingle...', true);
            
            try {
                await playJingleAudio(schedule.jingle_filename);
                
                // Track play event (optional)
                await trackJinglePlay(schedule.id, songsPlayed);
                
                await new Promise(resolve => setTimeout(resolve, 500));
                
                // Only play ONE jingle per round (highest priority wins)
                break;
            } catch (error) {
                console.error('Error playing jingle:', error);
            }
        }
    }
}
```

---

### Tarea 14: Agregar `fetchActiveJingles()` Function
**Archivo:** `frontend/game.js`

**Función Nueva:**
```javascript
/**
 * Fetch currently active jingle schedules from backend
 * Backend evaluates: date range, time period, day of week, enabled status
 * Returns schedules sorted by priority (highest first)
 */
async function fetchActiveJingles() {
    try {
        const apiUrl = CONFIG.API_URL || CONFIG.BACKEND_URL || 'http://localhost:8080';
        const url = apiUrl.endsWith('/api') 
            ? `${apiUrl}/jingle-schedules/active` 
            : `${apiUrl}/api/jingle-schedules/active`;
        
        const response = await fetch(url);
        
        if (!response.ok) {
            console.error('Error fetching active jingles:', response.status);
            return [];
        }
        
        const data = await response.json();
        return data.active_jingles || [];
    } catch (error) {
        console.error('Error fetching active jingles:', error);
        return [];
    }
}

/**
 * Track jingle play for analytics (optional)
 */
async function trackJinglePlay(scheduleId, roundNumber) {
    try {
        const apiUrl = CONFIG.API_URL || CONFIG.BACKEND_URL;
        const url = apiUrl.endsWith('/api') 
            ? `${apiUrl}/jingle-schedules/${scheduleId}/play` 
            : `${apiUrl}/api/jingle-schedules/${scheduleId}/play`;
        
        await fetch(url, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ round_number: roundNumber })
        });
    } catch (error) {
        console.error('Error tracking jingle play:', error);
    }
}
```

---

### Tarea 15: Agregar Links de Navegación
**Archivo:** `frontend/game.html`

**Agregar en la sección de navegación:**
```html
<div style="text-align: center; margin: 15px 0;">
    <a href="/jingle" style="...">
        🎤 Create Jingle
    </a>
    <a href="/jingle-manager" style="...">
        📅 Manage Schedules
    </a>
</div>
```

**Archivo:** `frontend/jingle.html`

**Agregar link similar:**
```html
<a href="/jingle-manager" class="back-link">📅 Manage Schedules</a>
```

---

## 🧪 FASE 4: Testing y Deployment
**Tiempo Estimado:** 1-2 horas

### Tarea 16: Probar API Backend con Postman/curl

**Test 1: Crear Schedule**
```bash
curl -X POST http://localhost:8080/api/jingle-schedules \
  -H "Content-Type: application/json" \
  -d '{
    "jingle_name": "Test Tuesday Tacos",
    "jingle_filename": "jingle_67890.mp3",
    "start_date": "2026-01-14",
    "end_date": "2026-03-31",
    "time_start": "17:00",
    "time_end": "22:00",
    "days_of_week": {
      "monday": false,
      "tuesday": true,
      "wednesday": false,
      "thursday": false,
      "friday": false,
      "saturday": false,
      "sunday": false
    },
    "repeat_pattern": "regular",
    "enabled": true,
    "priority": 10
  }'
```

**Test 2: Listar Todos**
```bash
curl http://localhost:8080/api/jingle-schedules
```

**Test 3: Obtener Activos (martes a las 7pm)**
```bash
curl http://localhost:8080/api/jingle-schedules/active
```

**Test 4: Actualizar**
```bash
curl -X PUT http://localhost:8080/api/jingle-schedules/1 \
  -H "Content-Type: application/json" \
  -d '{"enabled": false}'
```

**Test 5: Eliminar**
```bash
curl -X DELETE http://localhost:8080/api/jingle-schedules/1
```

---

### Tarea 17: Probar Lógica de Activación

**Casos de Prueba:**

1. **Schedule activo ahora:**
   - Crear schedule para hoy, hora actual, día correcto
   - Verificar que `is_active_now()` = true
   - Verificar que aparece en `/active`

2. **Schedule inactivo - día incorrecto:**
   - Crear schedule para lunes solamente
   - Probar en martes
   - Verificar que NO aparece en `/active`

3. **Schedule inactivo - hora incorrecta:**
   - Crear schedule para 5pm-10pm
   - Probar a las 2pm
   - Verificar que NO aparece en `/active`

4. **Schedule inactivo - fecha fuera de rango:**
   - Crear schedule con end_date en el pasado
   - Verificar que NO aparece en `/active`

5. **Schedule deshabilitado:**
   - Crear schedule válido pero con enabled=false
   - Verificar que NO aparece en `/active`

6. **Múltiples schedules - prioridad:**
   - Crear 2 schedules activos con diferentes prioridades
   - Verificar que se ordenan por prioridad

---

### Tarea 18: Probar Reproducción Durante Juego

**Pasos:**
1. Abrir game.html
2. Configurar juego con 10 jugadores
3. Crear schedule activo con pattern "often" (cada 3 rounds)
4. Iniciar juego
5. Avanzar rounds:
   - Round 3: Debería reproducir jingle
   - Round 6: Debería reproducir jingle
   - Round 9: Debería reproducir jingle
6. Verificar que el jingle correcto se reproduce
7. Verificar que el juego continúa normalmente después

**Verificar:**
- ✅ Jingle se reproduce en el intervalo correcto
- ✅ Solo se reproduce si está activo
- ✅ Solo se reproduce UN jingle por round (si hay múltiples)
- ✅ El jingle de mayor prioridad gana
- ✅ El juego no se rompe si hay error en el jingle

---

### Tarea 19: Agregar Manejo de Errores y Validación

**Backend Validations:**

```python
# En views.py
def create_jingle_schedule(request):
    data = request.data
    
    # Validar fechas
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    if end_date and start_date > end_date:
        return Response({
            'error': 'End date must be after start date'
        }, status=400)
    
    # Validar horas
    time_start = data.get('time_start')
    time_end = data.get('time_end')
    if time_start and time_end and time_start > time_end:
        return Response({
            'error': 'End time must be after start time'
        }, status=400)
    
    # Validar al menos un día seleccionado
    days = data.get('days_of_week', {})
    if not any(days.values()):
        return Response({
            'error': 'At least one day must be selected'
        }, status=400)
    
    # Validar que el archivo existe
    jingle_filename = data.get('jingle_filename')
    jingles_dir = DATA_DIR / 'jingles'
    if not (jingles_dir / jingle_filename).exists():
        return Response({
            'error': 'Jingle file not found'
        }, status=404)
    
    # Crear schedule...
```

**Frontend Validations:**

```javascript
// En jingle-manager.js
function validateScheduleForm() {
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    
    if (endDate && new Date(startDate) > new Date(endDate)) {
        alert('End date must be after start date');
        return false;
    }
    
    const timeStart = document.getElementById('timeStart').value;
    const timeEnd = document.getElementById('timeEnd').value;
    
    if (timeStart && timeEnd && timeStart > timeEnd) {
        alert('End time must be after start time');
        return false;
    }
    
    // Check at least one day selected
    const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
    const anyDaySelected = days.some(day => 
        document.getElementById(day).checked
    );
    
    if (!anyDaySelected) {
        alert('Please select at least one day');
        return false;
    }
    
    return true;
}
```

**Error Handling:**
- Try-catch en todas las llamadas API
- Mensajes de error user-friendly
- Logging de errores en consola
- Fallback graceful si backend falla

---

### Tarea 20: Deploy a Producción

**Pre-Deploy Checklist:**
- [ ] Todas las migraciones ejecutadas
- [ ] Todos los endpoints probados localmente
- [ ] Frontend funciona correctamente
- [ ] Juego reproduce jingles correctamente
- [ ] Validaciones funcionando
- [ ] Error handling implementado
- [ ] Documentación actualizada

**Deploy Steps:**

1. **Commit Changes:**
```bash
git add .
git commit -m "feat: add jingle manager with advanced scheduling"
git push origin main
```

2. **Verify Build:**
- DigitalOcean detectará el push
- Build se ejecutará automáticamente
- Verificar logs de build

3. **Run Migrations en Producción:**
```bash
# SSH a la app o usar console de DigitalOcean
python manage.py migrate
```

4. **Verificar en Producción:**
- Abrir https://music-bingo-x7qwu.ondigitalocean.app/jingle-manager
- Crear un schedule de prueba
- Verificar que aparece en la lista
- Verificar que se reproduce en el juego

5. **Monitorear Logs:**
```bash
# Verificar por errores
tail -f /var/log/gunicorn/error.log
```

---

## 📊 Checklist de Completitud

### Backend ✅
- [ ] Modelo JingleSchedule creado
- [ ] Migraciones ejecutadas
- [ ] POST /api/jingle-schedules funciona
- [ ] GET /api/jingle-schedules funciona
- [ ] GET /api/jingle-schedules/active funciona
- [ ] PUT /api/jingle-schedules/<id> funciona
- [ ] DELETE /api/jingle-schedules/<id> funciona
- [ ] Validaciones implementadas
- [ ] Error handling implementado

### Frontend ✅
- [ ] jingle-manager.html creado
- [ ] Formulario completo con 5 parámetros
- [ ] Date/time pickers funcionando
- [ ] Day checkboxes funcionando
- [ ] Repeat pattern selector funcionando
- [ ] jingle-manager.js con CRUD completo
- [ ] Vista de lista con schedules
- [ ] Modal de crear/editar funcionando
- [ ] Validaciones de formulario

### Integración ✅
- [ ] checkAndPlayJingle() actualizado
- [ ] fetchActiveJingles() implementado
- [ ] Links de navegación agregados
- [ ] Jingles se reproducen correctamente
- [ ] Prioridad funciona correctamente

### Testing ✅
- [ ] API probada con Postman/curl
- [ ] Lógica de activación probada
- [ ] Reproducción en juego probada
- [ ] Casos edge probados
- [ ] Error handling probado

### Deployment ✅
- [ ] Código commiteado
- [ ] Push a GitHub
- [ ] Build exitoso
- [ ] Migraciones en producción
- [ ] Verificado en producción
- [ ] Logs monitoreados

---

## 📚 Recursos Adicionales

**Documentos de Referencia:**
- `docs/JINGLE_MANAGER_DESIGN.md` - Diseño completo del sistema
- `docs/SESSION_REPORT_2026-01-14_JINGLE_PLAYLIST.md` - Sistema de playlist anterior
- `docs/SESSION_REPORT_2026-01-16_AUDIO_FIXES.md` - Fixes recientes de audio

**Archivos Clave:**
- `backend/api/models.py` - Modelos de datos
- `backend/api/views.py` - Endpoints API
- `backend/api/urls.py` - Rutas
- `frontend/jingle-manager.html` - UI principal
- `frontend/jingle-manager.js` - Lógica frontend
- `frontend/game.js` - Integración con juego

**Testing URLs:**
- Local: http://localhost:8080/jingle-manager
- Producción: https://music-bingo-x7qwu.ondigitalocean.app/jingle-manager

---

## 🎯 Orden de Ejecución Recomendado

**Día 1 (4 horas):**
1. Tareas 1-2: Modelo + Migraciones (30 min)
2. Tareas 3-7: Endpoints API completos (2.5 horas)
3. Tarea 16: Testing API con Postman (1 hora)

**Día 2 (4 horas):**
1. Tarea 8-9: HTML estructura + formulario (1.5 horas)
2. Tarea 10-11: Date pickers + pattern selector (1 hora)
3. Tarea 12: JavaScript CRUD completo (1.5 horas)

**Día 3 (2 horas):**
1. Tareas 13-15: Integración con game.js (1 hora)
2. Tareas 17-18: Testing completo (30 min)
3. Tarea 19: Validaciones y error handling (30 min)
4. Tarea 20: Deploy a producción (30 min)

---

**Total:** 10 horas distribuidas en 3 días  
**Prioridad:** Alta  
**Impacto:** Alto - Feature clave solicitada por cliente

---

**Última Actualización:** 16 de enero de 2026  
**Autor:** GitHub Copilot  
**Estado:** Listo para implementación

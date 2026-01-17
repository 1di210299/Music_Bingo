# Roadmap - Philip's Vision
**Fecha:** 17 de enero de 2026

## 🎯 Filosofía del Proyecto
- **NO sobre-refinar antes de validar**: Crear MVPs funcionales básicos
- **Estrategia**: Demostrar → Recibir Feedback → Iterar
- **Visión**: Plataforma integrada con múltiples modos de entretenimiento para pubs

---

## 📊 Estado Actual

### ✅ Music Bingo (COMPLETO - En Producción)
- Sistema funcional con control centralizado del host
- Participantes con tarjetas de bingo en sus teléfonos
- Generación de audio con TTS y mezcla de música
- Sistema de jingles para anuncios

**Pendiente:**
- [ ] Terminar sistema de jingles (casi listo)
- [ ] Recibir feedback de clientes reales

---

## 🎤 PRIORIDAD 1: Karaoke System

### Concepto
Sistema de karaoke interactivo donde clientes eligen canciones desde sus teléfonos y el host gestiona la cola.

### Flujo del Cliente/Cantante
1. **Unirse:**
   - Escanear QR code en el pub
   - Ingresar nombre
   
2. **Seleccionar:**
   - Navegar catálogo de canciones (Karafun API)
   - Elegir una canción
   - Escribir mensaje opcional para la audiencia
   - Unirse a la cola

3. **Esperar:**
   - Ver posición en cola
   - Sistema muestra "Estás en 4 minutos"
   - Notificación cuando sea su turno

4. **Cantar:**
   - Ver letra sincronizada en su teléfono
   - Música instrumental se reproduce en speakers del pub

### Flujo del Host/DJ
1. **Setup:**
   - Navegador conectado al sistema de sonido del pub
   - Ver cola de cantantes

2. **Gestión:**
   - Ver próximos cantantes
   - Poder reordenar cola
   - Poder saltar/cancelar canciones

3. **Reproducción:**
   - Anuncio automático: "Tenemos a John aquí, quiere cantar 'I Want to Break Free' de Queen, dedicado a sus amigos"
   - Reproducir música instrumental desde navegador
   - Sincronizar letra en teléfonos de participantes

### Diferencias vs Music Bingo
| Aspecto | Music Bingo | Karaoke |
|---------|-------------|---------|
| Control | Solo host | Host + Participantes |
| Participación | Pasiva (escuchar) | Activa (cantar) |
| Selección | Host elige todo | Clientes eligen canciones |
| Cola | No hay cola | Sistema de cola |
| Display | Tarjetas de bingo | Letra sincronizada |

### Tecnología
- **API**: Karafun (Philip enviará credenciales y documentación)
- **Backend**: Django REST API para gestión de cola
- **Frontend Host**: Control de cola y reproducción
- **Frontend Cliente**: Selección de canciones y display de letra
- **Sync**: WebSockets para sincronización de letra en tiempo real

### Tareas

#### Backend
- [ ] Estudiar documentación de Karafun API (esperar credenciales)
- [ ] Crear modelos:
  - [ ] `KaraokeSession` (venue_name, status, created_at)
  - [ ] `KaraokeQueue` (session, name, song_id, song_title, artist, message, position, status, requested_at)
- [ ] Endpoints API:
  - [ ] `POST /api/karaoke/session` - Crear sesión
  - [ ] `GET /api/karaoke/session/<venue>` - Estado de sesión
  - [ ] `POST /api/karaoke/queue` - Agregar a cola
  - [ ] `GET /api/karaoke/queue/<session_id>` - Ver cola
  - [ ] `PATCH /api/karaoke/queue/<id>/reorder` - Reordenar
  - [ ] `DELETE /api/karaoke/queue/<id>` - Cancelar
  - [ ] `PATCH /api/karaoke/queue/<id>/complete` - Marcar como completado
- [ ] Integración con Karafun API:
  - [ ] Búsqueda de canciones
  - [ ] Obtener URL de streaming
  - [ ] Obtener letra sincronizada (LRC format)

#### Frontend Host (`karaoke-host.html`)
- [ ] Crear página de control para DJ
- [ ] Setup modal (nombre del venue)
- [ ] Display de cola en tiempo real:
  - [ ] Próximo cantante (destacado)
  - [ ] Lista de espera
  - [ ] Tiempo estimado
- [ ] Controles:
  - [ ] Play/Pause
  - [ ] Skip
  - [ ] Reordenar cola (drag & drop)
  - [ ] Cancelar entrada
- [ ] Reproductor de audio (música instrumental)
- [ ] Sistema de anuncios automáticos (TTS)
- [ ] WebSocket para updates en tiempo real

#### Frontend Cliente (`karaoke.html`)
- [ ] Crear página de participante
- [ ] QR code scanner o input manual de venue
- [ ] Formulario de unión:
  - [ ] Nombre
  - [ ] Búsqueda de canciones
  - [ ] Preview de canción
  - [ ] Mensaje opcional
- [ ] Display de cola:
  - [ ] Tu posición
  - [ ] Tiempo estimado
  - [ ] Cantante actual
- [ ] Display de letra:
  - [ ] Sincronización con música
  - [ ] Highlight de línea actual
  - [ ] Auto-scroll
- [ ] WebSocket para sincronización

#### Testing
- [ ] Test básico con 2-3 canciones
- [ ] Test de cola (agregar, reordenar, cancelar)
- [ ] Test de sincronización de letra
- [ ] Test con múltiples clientes simultáneos

---

## 🔔 PRIORIDAD 2: Pub Quiz con Buzzers Bluetooth

### Concepto
Quiz interactivo estilo "quickfire" donde participantes presionan buzzers físicos para responder preguntas.

### Componentes Físicos
- **Buzzers Bluetooth**: Philip está adquiriendo
- **Cantidad**: TBD (basado en capacidad del venue)

### Flujo del Participante
1. **Setup:**
   - Escanear QR code
   - Ingresar nombre
   - Emparejar buzzer Bluetooth con su teléfono
   - Ver número de buzzer asignado

2. **Durante Quiz:**
   - Escuchar pregunta (TTS desde speakers del pub)
   - Si sabe respuesta, presionar buzzer
   - Esperar si le toca responder
   - Ver puntaje actual

### Flujo del Host
1. **Setup:**
   - Crear sesión de quiz
   - Configurar número de rondas
   - Cargar banco de preguntas

2. **Durante Quiz:**
   - Sistema lee pregunta por TTS
   - Sistema detecta quién presionó primero
   - Sistema anuncia: "John Smith puede responder"
   - Host valida respuesta (botones Correcto/Incorrecto)
   - Sistema actualiza puntajes
   - Ver tabla de posiciones en tiempo real

### Diferencias vs Quiz Tradicional
| Aspecto | Quiz Tradicional | Quiz con Buzzers |
|---------|------------------|------------------|
| Formato | Múltiple opción (A/B/C/D) | Respuesta abierta |
| Velocidad | Todos responden | Primero en presionar |
| Interacción | Baja | Alta |
| Emoción | Media | Alta (competitivo) |

### Tecnología
- **Hardware**: Buzzers Bluetooth (modelo TBD)
- **API**: Web Bluetooth API
- **Backend**: Django REST API para gestión de partidas
- **Frontend**: WebSockets para detección en tiempo real
- **Audio**: TTS para lectura de preguntas

### Tareas

#### Investigación
- [ ] Investigar modelo de buzzers que Philip comprará
- [ ] Estudiar Web Bluetooth API
- [ ] Probar conectividad buzzer → navegador
- [ ] Determinar límite de buzzers simultáneos

#### Backend
- [ ] Crear modelos:
  - [ ] `QuizSession` (venue_name, status, current_question, created_at)
  - [ ] `QuizPlayer` (session, name, buzzer_id, score, joined_at)
  - [ ] `QuizQuestion` (category, question, answer, difficulty, created_at)
  - [ ] `QuizAnswer` (session, question, player, was_correct, answered_at)
- [ ] Endpoints API:
  - [ ] `POST /api/quiz/session` - Crear sesión
  - [ ] `POST /api/quiz/session/<id>/join` - Unirse a quiz
  - [ ] `POST /api/quiz/session/<id>/buzz` - Registrar buzzer press
  - [ ] `POST /api/quiz/session/<id>/answer` - Validar respuesta
  - [ ] `GET /api/quiz/session/<id>/leaderboard` - Tabla de posiciones
- [ ] Sistema de detección de "primero en presionar"
- [ ] Banco de preguntas (CRUD)

#### Frontend Host
- [ ] Página de control del quiz
- [ ] Setup: cargar preguntas, configurar rondas
- [ ] Display de pregunta actual
- [ ] Display de quién presionó primero
- [ ] Botones Correcto/Incorrecto
- [ ] Tabla de posiciones en tiempo real
- [ ] Timer por pregunta (opcional)

#### Frontend Cliente
- [ ] QR code scanner
- [ ] Formulario de unión + nombre
- [ ] Interface de emparejamiento Bluetooth
- [ ] Display de pregunta actual
- [ ] Indicador de "has presionado"
- [ ] Display de puntaje personal
- [ ] Tabla de posiciones

#### Testing
- [ ] Test con 2-3 buzzers
- [ ] Test de detección simultánea (conflictos)
- [ ] Test de latencia
- [ ] Test con 10+ participantes

---

## 📋 Tareas Compartidas / Infraestructura

### Navegación y UX
- [ ] Crear landing page principal con 3 modos:
  - [ ] Music Bingo
  - [ ] Karaoke
  - [ ] Pub Quiz
- [ ] Sistema de navegación entre modos
- [ ] QR code generator para cada modo/venue

### Backend
- [ ] Refactorizar para soportar múltiples "modos" de juego
- [ ] Sistema de venue puede tener múltiples sesiones activas
- [ ] Logging y analytics para cada modo

### Deployment
- [ ] Asegurar que cada modo funcione en producción
- [ ] Considerar separar en subdominios:
  - `bingo.music-bingo.app`
  - `karaoke.music-bingo.app`
  - `quiz.music-bingo.app`

---

## 🎯 Próximos Pasos Inmediatos

### Esta Semana
1. ✅ Terminar sistema de jingles en Music Bingo
2. ⏳ Esperar credenciales de Karafun API de Philip
3. 📖 Leer documentación de Karafun API
4. 🎨 Diseñar mockups de interfaz de Karaoke (host + cliente)

### Cuando lleguen credenciales Karafun
1. 🔌 Probar API de Karafun (búsqueda, streaming, letras)
2. 🏗️ Implementar MVP de Karaoke:
   - Backend básico (cola simple)
   - Frontend host (reproducción + cola)
   - Frontend cliente (selección + letra)
3. 🧪 Demo con Philip
4. 🔄 Iterar basado en feedback

### Después de Karaoke MVP
1. 🛒 Esperar que lleguen buzzers Bluetooth
2. 🔬 Investigar Web Bluetooth API
3. 🏗️ Implementar MVP de Quiz
4. 🧪 Demo con Philip
5. 🔄 Iterar basado en feedback

---

## 💡 Notas Importantes

### Estrategia de Desarrollo
- **MVP primero**: Funcionalidad básica, interfaz simple
- **No sobre-ingeniería**: Validar con usuarios reales antes de refinar
- **Demos frecuentes**: Mostrar a Philip cada milestone
- **Feedback rápido**: Ajustar basado en respuesta de clientes reales de pub

### Prioridades
1. **Funcionalidad** > Estética (por ahora)
2. **Confiabilidad** > Features avanzadas
3. **Simplicidad** > Complejidad

### Riesgos / Consideraciones
- **Karafun API**: Dependemos de API externa (latencia, límites, costos)
- **Buzzers Bluetooth**: Compatibilidad de navegador, límite de conexiones simultáneas
- **Sincronización**: Letra de karaoke debe estar perfectamente sincronizada
- **Latencia**: Crítico en Quiz (detección de primer buzzer)
- **Escalabilidad**: Múltiples venues usando la plataforma simultáneamente

---

## 📞 Pendiente de Philip

- [ ] Enviar credenciales de Karafun API
- [ ] Enviar documentación de Karafun API
- [ ] Confirmar modelo de buzzers Bluetooth
- [ ] Feedback de clientes reales sobre Music Bingo actual

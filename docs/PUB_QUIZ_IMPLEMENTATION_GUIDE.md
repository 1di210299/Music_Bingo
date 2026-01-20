# 🎤 Perfect DJ Pub Quiz - Guía de Implementación

## 📋 Resumen

Sistema completo de Pub Quiz basado en IA con registro por QR, votación de géneros, generación automática de preguntas, y sistema de buzzers (opcional).

**Características extraídas de los PDFs:**
- ✅ 40-60 preguntas típicas (configurable)
- ✅ 5-7 rondas temáticas
- ✅ 50 géneros disponibles para votación
- ✅ Sistema de registro con QR en cada mesa
- ✅ Incentivos de redes sociales (+1 punto bonus)
- ✅ Hojas de respuesta personalizadas
- ✅ Sistema de buzzers BLE (estructura lista)

---

## 🚀 Quick Start

### 1. Inicializar Base de Datos

```bash
# Crear migración para los nuevos modelos
cd /Users/1di/Music_Bingo/backend
python manage.py makemigrations api
python manage.py migrate

# Inicializar los 50 géneros de quiz
curl http://localhost:8000/api/pub-quiz/initialize-genres
```

### 2. Crear una Sesión de Quiz

```bash
curl -X POST http://localhost:8000/api/pub-quiz/create-session \
  -H "Content-Type: application/json" \
  -d '{
    "venue_name": "The Cross Keys",
    "host_name": "Perfect DJ",
    "total_rounds": 6,
    "questions_per_round": 10,
    "duration_minutes": 120
  }'
```

Respuesta:
```json
{
  "success": true,
  "session_id": 1,
  "registration_url": "http://localhost:8000/pub-quiz/register/1"
}
```

### 3. Generar Códigos QR para las Mesas

```bash
# Descargar QR para la sesión 1
curl http://localhost:8000/api/pub-quiz/1/qr-code -o mesa_qr.png

# Imprimir estos QR en tarjetas para cada mesa
```

### 4. Equipos Se Registran

Los equipos escanean el QR y llenan el formulario en `pub-quiz-register.html`:
- Nombre del equipo
- Número de mesa
- Número de jugadores
- Email (opcional)
- Instagram/Social handle (opcional)
- **Votan por sus 5 géneros favoritos**
- ✅ Checkbox para seguir @PerfectDJ (+1 punto bonus)

### 5. Generar Preguntas Basado en Votos

```bash
# Una vez que todos los equipos están registrados
curl -X POST http://localhost:8000/api/pub-quiz/1/generate-questions
```

Esto:
1. Cuenta los votos de géneros de todos los equipos
2. Selecciona los 6 géneros más votados
3. Genera 10 preguntas por género (usando IA - placeholder por ahora)
4. Crea las rondas en la base de datos
5. Marca el quiz como "ready"

### 6. Iniciar el Quiz (Vista del Host)

Abrir en navegador: `http://localhost:8000/pub-quiz/host/1`

**Funcionalidades de la Vista del Host:**
- Dashboard en tiempo real con estadísticas
- Pregunta actual grande y clara (lista para TTS)
- Botón "Show Answer" para revelar respuesta + fun fact
- Botón "Next Question" para avanzar
- Leaderboard en vivo de equipos
- Progress bar del quiz
- Control de halftime automático

---

## 📁 Archivos Creados

### Backend (Django)

1. **`backend/api/pub_quiz_models.py`** - Modelos de datos
   - `PubQuizSession` - Sesión del quiz
   - `QuizTeam` - Equipos participantes
   - `QuizGenre` - Géneros/categorías (50 tipos)
   - `QuizQuestion` - Preguntas individuales
   - `TeamAnswer` - Respuestas de equipos
   - `QuizRound` - Información de rondas
   - `BuzzerDevice` - Dispositivos BLE (opcional)
   - `GenreVote` - Votos de equipos por géneros

2. **`backend/api/pub_quiz_generator.py`** - Generador de preguntas
   - Lista de 50 géneros con íconos
   - Lógica de selección basada en votos
   - Prompts para IA
   - Estructura de quiz completa

3. **`backend/api/pub_quiz_views.py`** - API endpoints
   - Creación de sesiones
   - Registro de equipos
   - Generación de QR
   - Generación de preguntas
   - Control del quiz en vivo
   - Leaderboard
   - Estadísticas

### Frontend

4. **`frontend/pub-quiz-host.html`** - Vista del host/quizmaster
   - Dashboard profesional
   - Control de preguntas
   - Leaderboard en vivo
   - Estadísticas en tiempo real

5. **`frontend/pub-quiz-register.html`** - Formulario de registro
   - Registro de equipo
   - Votación de géneros (hasta 5)
   - Incentivo de redes sociales
   - Diseño mobile-friendly

### URLs Configuradas

```python
# Ya agregadas a backend/api/urls.py
/api/pub-quiz/initialize-genres          # Inicializar géneros
/api/pub-quiz/create-session             # Crear sesión
/api/pub-quiz/<id>/register-team         # Registrar equipo
/api/pub-quiz/<id>/generate-questions    # Generar preguntas
/api/pub-quiz/<id>/start                 # Iniciar quiz
/api/pub-quiz/<id>/next                  # Siguiente pregunta
/api/pub-quiz/<id>/current-question      # Pregunta actual
/api/pub-quiz/<id>/leaderboard           # Tabla de posiciones
/api/pub-quiz/<id>/stats                 # Estadísticas
/api/pub-quiz/<id>/qr-code               # Generar QR
```

---

## 🎯 50 Géneros Disponibles

1. General Knowledge
2. Pop Music
3. Movies & Film
4. Television & Streaming Shows
5. 80s Nostalgia
6. 90s Nostalgia
7. 2000s Throwback
8. 2010s Pop Culture
9. Current Events & News (2025-2026)
10. Sports
11. Geography & World Capitals
12. History
13. Science & Inventions
14. Food & Drink
15. Cocktails & Alcohol
16. Celebrities & Gossip
17. Disney & Pixar
18. Harry Potter
19. Superheroes & Marvel/DC
20. Video Games
21. Animals & Nature
22. Mythology & Legends
23. Literature & Books
24. Broadway & Musicals
25. Art & Famous Paintings
26. Tech & Gadgets
27. AI & Future Tech
28. Memes & Viral Trends
29. Picture Round
30. Music Round (Name That Tune)
31. Connections
32. Anagrams & Wordplay
33. Riddles & Brain Teasers
34. What Happened Next?
35. Wrong Answers Only
36. Hidden Theme Rounds
37. Slogans & Brands
38. Toys & Games
39. Fashion & Style
40. Holidays & Seasonal
41. New York City Trivia
42. Famous Quotes
43. True or False
44. Rapid Fire / Buzzer Questions
45. 70s Disco & Funk
46. Hip-Hop & Rap
47. Classic Rock
48. Country Music
49. Horror Movies
50. Space & Astronomy

---

## 🔧 Integración con IA (TODO)

El generador actual usa preguntas placeholder. Para producción:

### Opción 1: OpenAI GPT
```python
import openai

prompt = generator.generate_ai_prompt_for_questions(genre, num_questions=10)
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7
)
questions = json.loads(response.choices[0].message.content)
```

### Opción 2: Claude (Anthropic)
```python
import anthropic

client = anthropic.Anthropic(api_key="...")
response = client.messages.create(
    model="claude-3-sonnet-20240229",
    messages=[{"role": "user", "content": prompt}]
)
```

### Opción 3: Base de Datos de Preguntas
Crear una librería de preguntas pre-generadas por género.

---

## 📱 Sistema de Buzzers BLE (Opcional)

### Hardware Recomendado
- **ESP32** (~$5-10) con botón físico
- **Adafruit Circuit Playground Bluefruit** (~$25)
- **Arduino Nano + HM-10 BLE** (~$10)

### Flujo
1. Cada equipo recibe un buzzer BLE
2. App móvil se empareja con el buzzer vía Bluetooth
3. Al presionar, el app envía timestamp al servidor
4. Servidor ordena por timestamp y anuncia vía TTS

### Estructura Ya Creada
- Modelo `BuzzerDevice` en DB
- Campo `buzz_timestamp` en `TeamAnswer`
- Endpoints listos para implementar

---

## 🎨 Personalización

### Branding
Editar en `pub_quiz_views.py`:
```python
session = PubQuizSession.objects.create(
    host_name="Tu Nombre DJ",
    social_hashtag="#TuHashtag",
    social_handle="@TuHandle"
)
```

### Hojas de Respuesta Personalizadas
Usar servicios como:
- Vistaprint
- Canva (diseño)
- Incluir: Logo, redes sociales, QR code, espacios para respuestas

### TTS para Anuncios
Integrar con el sistema existente de Music Bingo:
```python
from .views import generate_tts

# Anunciar pregunta
tts_audio = generate_tts(question.question_text)

# Anunciar respuesta
tts_audio = generate_tts(f"The answer is {question.correct_answer}")
```

---

## 📊 Flujo Completo de un Evento

### Preparación (1 hora antes)
1. ✅ Crear sesión de quiz
2. ✅ Generar QR codes
3. ✅ Imprimir hojas de respuesta con branding
4. ✅ Colocar QR en cada mesa

### Registro (30 min)
5. ✅ Equipos escanean QR y se registran
6. ✅ Votan por géneros favoritos
7. ✅ Host monitorea registros en dashboard

### Pre-inicio (15 min)
8. ✅ Host genera preguntas basado en votos
9. ✅ Anuncia géneros seleccionados
10. ✅ Explica reglas y puntos bonus

### Durante el Quiz (2 horas)
11. ✅ Host inicia quiz
12. ✅ TTS lee cada pregunta en voz alta
13. ✅ Equipos escriben respuestas
14. ✅ Host revela respuesta + fun fact
15. ✅ Leaderboard se actualiza automáticamente
16. ✅ Halftime después de ronda 3
17. ✅ Ronda final (opcional: buzzers)

### Final
18. ✅ Anunciar ganadores
19. ✅ Promover redes sociales
20. ✅ Invitar a próximo evento

---

## 🔐 Seguridad y Validación

- CSRF tokens en formularios
- Validación de datos en backend
- Límite de equipos por sesión
- Rate limiting en APIs
- Sanitización de nombres de equipo

---

## 📈 Métricas y Analytics

El sistema rastrea:
- Total de equipos/jugadores
- Géneros más votados
- Tasa de seguimiento en redes sociales
- Tiempo promedio por pregunta
- Engagement por ronda

---

## 🎁 Sistema de Puntos Bonus

- **+1 punto** por seguir redes sociales
- **+2 puntos** por ser el primero en buzzer
- **+1 punto** por mencionar en Instagram
- **+1 punto** por respuesta creativa (discreción del host)

---

## 🚨 Troubleshooting

### No se generan preguntas
- Verificar que hay equipos registrados
- Verificar que hay votos de géneros
- Revisar logs del servidor

### QR no funciona
- Verificar URL completa
- Asegurar que el servidor está accesible
- Probar en navegador primero

### Leaderboard no actualiza
- Verificar conexión JavaScript
- Revisar console del navegador
- Verificar endpoints de API

---

## 📞 Próximos Pasos

1. **Migrar base de datos** ✅ (ejecutar makemigrations/migrate)
2. **Probar flujo completo** con datos de prueba
3. **Integrar IA real** para generación de preguntas
4. **Diseñar hojas de respuesta** en Canva
5. **Implementar buzzers** (opcional)
6. **Integrar TTS** del sistema Music Bingo
7. **Agregar autenticación** para hosts
8. **Crear admin Django** para gestión

---

## 💡 Ideas Futuras

- Sistema de premios automático
- Exportar resultados a PDF
- Galería de fotos de equipos
- Modo "Tema de la Noche" (solo 1 género)
- Integración con Spotify para rondas musicales
- Dashboard de analíticas post-evento
- Sistema de reservas de mesas
- Notificaciones push para equipos

---

¡El sistema está listo para usar! 🎉

**Creado por:** Perfect DJ
**Basado en:** Especificaciones de PDFs de Pub Quiz
**Tecnología:** Django + Vanilla JS + IA

Para soporte: @PerfectDJ

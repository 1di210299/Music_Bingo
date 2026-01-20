#!/bin/bash

# 🎤 Perfect DJ Pub Quiz - Setup Script
# Inicialización rápida del sistema de Pub Quiz

echo "🎤 Perfect DJ Pub Quiz - Setup"
echo "================================"
echo ""

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar que estamos en el directorio correcto
if [ ! -f "backend/manage.py" ]; then
    echo "❌ Error: Este script debe ejecutarse desde el directorio raíz del proyecto Music_Bingo"
    exit 1
fi

echo -e "${BLUE}Paso 1: Migrando base de datos...${NC}"
cd backend
python3 manage.py makemigrations api
python3 manage.py migrate
echo -e "${GREEN}✅ Migraciones completadas${NC}"
echo ""

echo -e "${BLUE}Paso 2: Inicializando 50 géneros de quiz...${NC}"
python3 manage.py shell << EOF
from api.pub_quiz_generator import initialize_genres_in_db
initialize_genres_in_db()
EOF
echo -e "${GREEN}✅ Géneros inicializados${NC}"
echo ""

echo -e "${BLUE}Paso 3: Creando sesión de prueba...${NC}"
cd ..
curl -X POST http://localhost:8000/api/pub-quiz/create-session \
  -H "Content-Type: application/json" \
  -d '{
    "venue_name": "The Test Pub",
    "host_name": "Perfect DJ",
    "total_rounds": 6,
    "questions_per_round": 10,
    "duration_minutes": 120
  }' 2>/dev/null | python3 -m json.tool

echo ""
echo -e "${GREEN}✅ Sesión de prueba creada${NC}"
echo ""

echo "================================"
echo -e "${GREEN}🎉 Setup completado!${NC}"
echo ""
echo -e "${YELLOW}Próximos pasos:${NC}"
echo ""
echo "1. Iniciar el servidor Django (si no está corriendo):"
echo "   cd backend && python3 manage.py runserver"
echo ""
echo "2. Abrir vista del host:"
echo "   http://localhost:8000/pub-quiz/host/1"
echo ""
echo "3. URL de registro para equipos:"
echo "   http://localhost:8000/pub-quiz/register/1"
echo ""
echo "4. Generar QR code:"
echo "   http://localhost:8000/api/pub-quiz/1/qr-code"
echo ""
echo -e "${BLUE}📚 Documentación:${NC}"
echo "   - docs/PUB_QUIZ_README.md"
echo "   - docs/PUB_QUIZ_IMPLEMENTATION_GUIDE.md"
echo "   - docs/PUB_QUIZ_EXTRACTED_INFO.md"
echo ""
echo "🎤 ¡Que empiece el quiz! 🎵"

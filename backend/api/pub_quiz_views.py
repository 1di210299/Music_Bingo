"""
Vistas y API para el sistema Pub Quiz
"""

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db.models import Count, Q
import json
import qrcode
from io import BytesIO
import base64

from .pub_quiz_models import (
    PubQuizSession, QuizTeam, QuizGenre, QuizQuestion,
    QuizRound, TeamAnswer, BuzzerDevice, GenreVote
)
from .pub_quiz_generator import PubQuizGenerator, initialize_genres_in_db


# ============================================================================
# VISTAS DE ADMINISTRACIÓN
# ============================================================================

def pub_quiz_admin(request):
    """Vista principal de administración del Pub Quiz"""
    sessions = PubQuizSession.objects.all().order_by('-date')[:10]
    return render(request, 'pub_quiz_admin.html', {
        'sessions': sessions
    })


@csrf_exempt
@require_http_methods(["POST"])
def create_quiz_session(request):
    """Crea una nueva sesión de Pub Quiz"""
    try:
        data = json.loads(request.body)
        
        session = PubQuizSession.objects.create(
            venue_name=data.get('venue_name', 'The Pub'),
            host_name=data.get('host_name', 'Perfect DJ'),
            total_rounds=data.get('total_rounds', 6),
            questions_per_round=data.get('questions_per_round', 10),
            duration_minutes=data.get('duration_minutes', 120),
            status='registration',
        )
        
        # Generar URL de registro con QR
        registration_url = f"{request.scheme}://{request.get_host()}/pub-quiz/register/{session.id}"
        
        return JsonResponse({
            'success': True,
            'session_id': session.id,
            'registration_url': registration_url,
            'session': {
                'id': session.id,
                'venue_name': session.venue_name,
                'status': session.status,
                'total_rounds': session.total_rounds,
                'questions_per_round': session.questions_per_round,
            }
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


# ============================================================================
# REGISTRO DE EQUIPOS Y QR
# ============================================================================

def team_registration_page(request, session_id):
    """Página de registro para equipos (acceso vía QR)"""
    session = get_object_or_404(PubQuizSession, id=session_id)
    genres = QuizGenre.objects.filter(is_active=True).order_by('order')
    
    return render(request, 'team_registration.html', {
        'session': session,
        'genres': genres,
    })


@csrf_exempt
@require_http_methods(["POST"])
def register_team(request, session_id):
    """Registra un nuevo equipo en la sesión"""
    try:
        session = get_object_or_404(PubQuizSession, id=session_id)
        data = json.loads(request.body)
        
        # Crear equipo
        team = QuizTeam.objects.create(
            session=session,
            team_name=data.get('team_name'),
            table_number=data.get('table_number'),
            num_players=data.get('num_players', 4),
            contact_email=data.get('contact_email', ''),
            contact_phone=data.get('contact_phone', ''),
            social_handle=data.get('social_handle', ''),
            followed_social=data.get('followed_social', False),
        )
        
        # Bonus por seguir redes sociales
        if team.followed_social:
            team.bonus_points = 1
            team.save()
        
        # Registrar votos de géneros (top 3-5)
        genre_votes = data.get('genre_votes', [])
        for i, genre_id in enumerate(genre_votes[:5], 1):
            try:
                genre = QuizGenre.objects.get(id=genre_id)
                GenreVote.objects.create(
                    team=team,
                    genre=genre,
                    priority=i
                )
            except QuizGenre.DoesNotExist:
                pass
        
        return JsonResponse({
            'success': True,
            'team_id': team.id,
            'team_name': team.team_name,
            'bonus_points': team.bonus_points,
            'message': '¡Equipo registrado! Sigan @PerfectDJ para más diversión!'
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def generate_qr_code(request, session_id):
    """Genera código QR para registro del equipo"""
    session = get_object_or_404(PubQuizSession, id=session_id)
    registration_url = f"{request.scheme}://{request.get_host()}/pub-quiz/register/{session_id}"
    
    # Generar QR
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(registration_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convertir a base64 o retornar imagen
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='image/png')
    response['Content-Disposition'] = f'inline; filename="qr_code_session_{session_id}.png"'
    
    return response


# ============================================================================
# GESTIÓN DE PREGUNTAS Y RONDAS
# ============================================================================

@csrf_exempt
@require_http_methods(["POST"])
def generate_quiz_questions(request, session_id):
    """Genera preguntas para el quiz basado en votación de géneros"""
    try:
        session = get_object_or_404(PubQuizSession, id=session_id)
        
        # Contar votos por género
        genre_votes = GenreVote.objects.filter(team__session=session).values('genre_id').annotate(
            vote_count=Count('genre_id')
        ).order_by('-vote_count')
        
        votes_dict = {v['genre_id']: v['vote_count'] for v in genre_votes}
        
        # Usar generador para seleccionar géneros
        generator = PubQuizGenerator()
        selected_genres = generator.select_genres_by_votes(votes_dict, session.total_rounds)
        
        # Crear estructura de rondas
        structure = generator.create_quiz_structure(
            selected_genres,
            questions_per_round=session.questions_per_round,
            include_halftime=True,
            include_buzzer_round=False
        )
        
        # Crear rondas en DB
        for round_data in structure['rounds']:
            genre = QuizGenre.objects.get(name=round_data['genre']['name'])
            
            quiz_round = QuizRound.objects.create(
                session=session,
                round_number=round_data['round_number'],
                genre=genre,
                round_name=round_data['round_name'],
                is_buzzer_round=round_data['is_buzzer_round'],
                is_halftime_before=round_data['is_halftime_before'],
            )
            
            # Aquí iría la integración con IA para generar preguntas reales
            # Por ahora, usar samples
            sample_questions = generator.generate_sample_questions(
                genre.name, 
                round_data['questions_per_round']
            )
            
            for q_data in sample_questions:
                QuizQuestion.objects.create(
                    session=session,
                    genre=genre,
                    round_number=round_data['round_number'],
                    question_number=q_data['question_number'],
                    question_text=q_data['question'],
                    correct_answer=q_data['answer'],
                    alternative_answers=q_data.get('alternative_answers', []),
                    difficulty=q_data.get('difficulty', 'medium'),
                    fun_fact=q_data.get('fun_fact', ''),
                    hints=q_data.get('hints', ''),
                )
        
        # Actualizar estado de sesión
        session.status = 'ready'
        session.save()
        
        # Agregar géneros seleccionados a la sesión
        for genre_data in selected_genres:
            genre = QuizGenre.objects.get(name=genre_data['name'])
            session.selected_genres.add(genre)
        
        return JsonResponse({
            'success': True,
            'message': 'Quiz generado exitosamente',
            'structure': structure,
            'selected_genres': [g['name'] for g in selected_genres]
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


# ============================================================================
# CONTROL DEL QUIZ EN VIVO
# ============================================================================

def quiz_host_view(request, session_id):
    """Vista del host para controlar el quiz"""
    session = get_object_or_404(PubQuizSession, id=session_id)
    teams = session.teams.all().order_by('-total_score')
    rounds = session.rounds.all()
    
    return render(request, 'quiz_host.html', {
        'session': session,
        'teams': teams,
        'rounds': rounds,
    })


@csrf_exempt
@require_http_methods(["POST"])
def start_quiz(request, session_id):
    """Inicia el quiz"""
    session = get_object_or_404(PubQuizSession, id=session_id)
    session.status = 'in_progress'
    session.current_round = 1
    session.current_question = 1
    session.save()
    
    # Marcar primera ronda como iniciada
    first_round = session.rounds.filter(round_number=1).first()
    if first_round:
        first_round.started_at = timezone.now()
        first_round.save()
    
    return JsonResponse({'success': True, 'status': 'in_progress'})


@csrf_exempt
@require_http_methods(["POST"])
def next_question(request, session_id):
    """Avanza a la siguiente pregunta"""
    session = get_object_or_404(PubQuizSession, id=session_id)
    
    total_questions_in_round = session.questions_per_round
    
    if session.current_question < total_questions_in_round:
        session.current_question += 1
    else:
        # Siguiente ronda
        current_round = session.rounds.filter(round_number=session.current_round).first()
        if current_round:
            current_round.is_completed = True
            current_round.completed_at = timezone.now()
            current_round.save()
        
        if session.current_round < session.total_rounds:
            session.current_round += 1
            session.current_question = 1
            
            # Verificar si es halftime
            next_round = session.rounds.filter(round_number=session.current_round).first()
            if next_round and next_round.is_halftime_before:
                session.status = 'halftime'
            
            if next_round:
                next_round.started_at = timezone.now()
                next_round.save()
        else:
            session.status = 'completed'
    
    session.save()
    
    return JsonResponse({
        'success': True,
        'current_round': session.current_round,
        'current_question': session.current_question,
        'status': session.status
    })


def get_current_question(request, session_id):
    """Obtiene la pregunta actual"""
    session = get_object_or_404(PubQuizSession, id=session_id)
    
    question = QuizQuestion.objects.filter(
        session=session,
        round_number=session.current_round,
        question_number=session.current_question
    ).first()
    
    if not question:
        return JsonResponse({'success': False, 'error': 'No question found'})
    
    return JsonResponse({
        'success': True,
        'question': {
            'id': question.id,
            'round_number': question.round_number,
            'question_number': question.question_number,
            'genre': question.genre.name if question.genre else 'General',
            'question_text': question.question_text,
            'difficulty': question.difficulty,
            'question_type': question.question_type,
            'media_url': question.media_url,
            'hints': question.hints,
            'points': question.points,
        }
    })


# ============================================================================
# LEADERBOARD Y ESTADÍSTICAS
# ============================================================================

def get_leaderboard(request, session_id):
    """Obtiene el ranking actual de equipos"""
    session = get_object_or_404(PubQuizSession, id=session_id)
    teams = session.teams.all().order_by('-total_score', '-bonus_points', 'team_name')
    
    leaderboard = []
    for i, team in enumerate(teams, 1):
        leaderboard.append({
            'position': i,
            'team_name': team.team_name,
            'table_number': team.table_number,
            'total_score': team.total_score,
            'bonus_points': team.bonus_points,
            'final_score': team.final_score,
            'social_handle': team.social_handle,
        })
    
    return JsonResponse({
        'success': True,
        'leaderboard': leaderboard,
        'total_teams': len(leaderboard)
    })


def get_session_stats(request, session_id):
    """Estadísticas de la sesión"""
    session = get_object_or_404(PubQuizSession, id=session_id)
    
    stats = {
        'total_teams': session.teams.count(),
        'total_players': sum(team.num_players for team in session.teams.all()),
        'social_followers': session.teams.filter(followed_social=True).count(),
        'current_round': session.current_round,
        'total_rounds': session.total_rounds,
        'progress_percent': (session.current_round / session.total_rounds * 100) if session.total_rounds > 0 else 0,
        'status': session.status,
        'selected_genres': [g.name for g in session.selected_genres.all()],
    }
    
    return JsonResponse({'success': True, 'stats': stats})


# ============================================================================
# INICIALIZACIÓN
# ============================================================================

def initialize_quiz_genres(request):
    """Endpoint para inicializar los 50 géneros"""
    try:
        initialize_genres_in_db()
        count = QuizGenre.objects.count()
        return JsonResponse({
            'success': True,
            'message': f'{count} géneros inicializados correctamente'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

#!/usr/bin/env python3
"""
Script para añadir más canciones al pool usando iTunes Search API
Uso: python add_songs_to_pool.py
"""

import requests
import json
import time
from pathlib import Path

# iTunes Search API endpoint
ITUNES_API = "https://itunes.apple.com/search"

# Términos de búsqueda por género/época para variedad
SEARCH_QUERIES = [
    # Pop hits por década
    {"term": "pop hits 2020s", "limit": 50},
    {"term": "pop hits 2010s", "limit": 50},
    {"term": "pop hits 2000s", "limit": 50},
    {"term": "pop hits 90s", "limit": 50},
    {"term": "pop hits 80s", "limit": 50},
    {"term": "pop hits 70s", "limit": 50},
    
    # Rock por década
    {"term": "rock classics", "limit": 50},
    {"term": "rock hits 2010s", "limit": 50},
    {"term": "rock hits 2000s", "limit": 50},
    {"term": "rock hits 90s", "limit": 50},
    {"term": "alternative rock", "limit": 50},
    {"term": "indie rock", "limit": 50},
    
    # Dance/Electronic
    {"term": "dance hits", "limit": 50},
    {"term": "electronic music", "limit": 50},
    {"term": "house music", "limit": 50},
    {"term": "edm hits", "limit": 50},
    
    # R&B/Soul/Hip-Hop
    {"term": "rnb hits", "limit": 50},
    {"term": "soul classics", "limit": 50},
    {"term": "hip hop hits", "limit": 50},
    {"term": "rap hits", "limit": 50},
    
    # Latino
    {"term": "latin hits", "limit": 50},
    {"term": "reggaeton", "limit": 50},
    {"term": "salsa", "limit": 50},
    {"term": "bachata", "limit": 50},
    
    # Disco/Funk/Motown
    {"term": "disco classics", "limit": 50},
    {"term": "funk hits", "limit": 50},
    {"term": "motown classics", "limit": 50},
    
    # Country/Folk
    {"term": "country hits", "limit": 50},
    {"term": "folk music", "limit": 50},
    
    # Jazz/Blues
    {"term": "jazz standards", "limit": 50},
    {"term": "blues classics", "limit": 50},
]

def search_itunes(term, limit=50, country="US"):
    """Busca canciones en iTunes API"""
    params = {
        "term": term,
        "media": "music",
        "entity": "song",
        "limit": limit,
        "country": country,
        "explicit": "No"  # Evitar contenido explícito
    }
    
    try:
        response = requests.get(ITUNES_API, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error buscando '{term}': {e}")
        return None

def format_song(track):
    """Formatea canción al formato del pool"""
    return {
        "id": str(track.get("trackId", "")),
        "title": track.get("trackName", "Unknown"),
        "artist": track.get("artistName", "Unknown"),
        "preview_url": track.get("previewUrl", ""),
        "artwork_url": track.get("artworkUrl100", "").replace("100x100bb", "600x600bb"),
        "duration_ms": track.get("trackTimeMillis", 0),
        "genre": track.get("primaryGenreName", "Pop"),
        "release_year": track.get("releaseDate", "2000")[:4],
        "has_duplicate_artist": False
    }

def load_current_pool():
    """Carga el pool actual"""
    pool_path = Path(__file__).parent.parent / "data" / "pool.json"
    
    if pool_path.exists():
        with open(pool_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    return {"songs": [], "total_songs": 0}

def save_pool(pool_data):
    """Guarda el pool actualizado"""
    pool_path = Path(__file__).parent.parent / "data" / "pool.json"
    
    with open(pool_path, 'w', encoding='utf-8') as f:
        json.dump(pool_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Pool guardado en {pool_path}")

def main():
    print("🎵 AÑADIENDO CANCIONES AL POOL DE MUSIC BINGO")
    print("=" * 50)
    
    # Cargar pool actual
    pool = load_current_pool()
    existing_ids = {song["id"] for song in pool["songs"]}
    initial_count = len(pool["songs"])
    
    print(f"📊 Pool actual: {initial_count} canciones")
    print()
    
    new_songs = []
    
    for query in SEARCH_QUERIES:
        term = query["term"]
        limit = query["limit"]
        
        print(f"🔍 Buscando: {term} (limit={limit})")
        
        result = search_itunes(term, limit)
        
        if not result or "results" not in result:
            continue
        
        tracks = result["results"]
        added = 0
        
        for track in tracks:
            track_id = str(track.get("trackId", ""))
            preview_url = track.get("previewUrl", "")
            
            # Solo añadir si tiene preview URL y no está duplicada
            if track_id and preview_url and track_id not in existing_ids:
                formatted = format_song(track)
                new_songs.append(formatted)
                existing_ids.add(track_id)
                added += 1
        
        print(f"   ✅ Encontradas: {len(tracks)}, Nuevas: {added}")
        
        # Respetar rate limit (20 llamadas/minuto)
        time.sleep(3)
    
    print()
    print(f"🎉 Total canciones nuevas encontradas: {len(new_songs)}")
    
    if new_songs:
        # Añadir al pool
        pool["songs"].extend(new_songs)
        pool["total_songs"] = len(pool["songs"])
        pool["generated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Guardar
        save_pool(pool)
        
        print(f"✅ Pool actualizado: {initial_count} → {pool['total_songs']} canciones")
        print(f"   (+{len(new_songs)} canciones nuevas)")
    else:
        print("ℹ️  No se encontraron canciones nuevas")
    
    print()
    print("🎵 ¡Listo! Ya puedes usar el pool actualizado")

if __name__ == "__main__":
    main()

# Jingle Manager - Advanced Scheduling System Design

**Date:** January 16, 2026  
**Feature:** Jingle Manager with Time-based Scheduling  
**Status:** Design & Implementation Plan

---

## 🎯 Overview

The Jingle Manager extends the existing jingle playlist system with advanced scheduling capabilities, allowing venue owners to configure when specific jingles play based on:

- **Date ranges** (start/end dates)
- **Time periods** (specific hours of the day)
- **Days of the week** (M, T, W, Th, F, Sa, Su)
- **Repeat patterns** (Occasional, Regular, Often)

---

## 📊 Current System Analysis

### Existing Features (Already Implemented)
✅ Jingle generation with TTS + AI music  
✅ Jingle library with metadata storage  
✅ Basic playlist system (play every N rounds)  
✅ Manual jingle selection for playlist  
✅ File storage in `/data/jingles/`  
✅ Metadata storage as `.json` files  

### Current Limitations
❌ No time-based scheduling  
❌ No date range support  
❌ No day-of-week filtering  
❌ Only round-based intervals (not time-aware)  
❌ No scheduling priority/conflict management  

### Current Architecture
```
Backend (Django):
- /api/generate-jingle → Create jingle
- /api/jingles → List all jingles
- /api/jingles/<filename> → Download jingle
- /api/playlist → Get/update playlist settings

Frontend:
- jingle.html → Generator wizard + library
- jingle.js → Playlist management
- game.js → checkAndPlayJingle() function

Data Storage:
- /data/jingles/*.mp3 → Audio files
- /data/jingles/*.json → Metadata
- /data/jingle_playlist.json → Current playlist config
```

---

## 🗄️ Database Schema Design

### Option 1: SQLite Database (Recommended)

**Advantages:**
- Django ORM support
- Relational data integrity
- Easy querying with complex filters
- Atomic transactions
- Migration support

**New Model: `JingleSchedule`**

```python
# backend/api/models.py

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class JingleSchedule(models.Model):
    """
    Scheduled jingle with time-based playback rules
    """
    
    # Jingle Identification
    jingle_name = models.CharField(
        max_length=200,
        help_text="Display name (e.g., 'Tuesday Night Taco Promotion')"
    )
    jingle_filename = models.CharField(
        max_length=255,
        help_text="Actual audio file (e.g., 'jingle_12345.mp3')"
    )
    
    # Date Range
    start_date = models.DateField(
        help_text="First day this jingle becomes active"
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        help_text="Last day this jingle is active (null = no end)"
    )
    
    # Time Period (Optional)
    time_start = models.TimeField(
        null=True,
        blank=True,
        help_text="Start time (e.g., 17:00 for 5pm)"
    )
    time_end = models.TimeField(
        null=True,
        blank=True,
        help_text="End time (e.g., 22:00 for 10pm)"
    )
    
    # Days of Week (Bitmask)
    monday = models.BooleanField(default=True)
    tuesday = models.BooleanField(default=True)
    wednesday = models.BooleanField(default=True)
    thursday = models.BooleanField(default=True)
    friday = models.BooleanField(default=True)
    saturday = models.BooleanField(default=True)
    sunday = models.BooleanField(default=True)
    
    # Repeat Pattern
    REPEAT_CHOICES = [
        ('occasional', 'Occasional - Every 8-10 rounds'),
        ('regular', 'Regular - Every 5-7 rounds'),
        ('often', 'Often - Every 3-4 rounds'),
    ]
    repeat_pattern = models.CharField(
        max_length=20,
        choices=REPEAT_CHOICES,
        default='regular'
    )
    
    # Status
    enabled = models.BooleanField(
        default=True,
        help_text="Master on/off switch for this schedule"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Priority (for conflict resolution)
    priority = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Higher priority wins if multiple jingles qualify (0-100)"
    )
    
    class Meta:
        ordering = ['-priority', '-created_at']
        verbose_name = "Jingle Schedule"
        verbose_name_plural = "Jingle Schedules"
    
    def __str__(self):
        return f"{self.jingle_name} ({self.start_date} to {self.end_date or 'ongoing'})"
    
    def is_active_now(self):
        """Check if this schedule is currently active"""
        from datetime import datetime, date
        
        if not self.enabled:
            return False
        
        now = datetime.now()
        today = date.today()
        
        # Check date range
        if today < self.start_date:
            return False
        if self.end_date and today > self.end_date:
            return False
        
        # Check time range (if specified)
        if self.time_start and self.time_end:
            current_time = now.time()
            if not (self.time_start <= current_time <= self.time_end):
                return False
        
        # Check day of week
        day_map = {
            0: self.monday,
            1: self.tuesday,
            2: self.wednesday,
            3: self.thursday,
            4: self.friday,
            5: self.saturday,
            6: self.sunday,
        }
        if not day_map[today.weekday()]:
            return False
        
        return True
    
    def get_interval(self):
        """Get the round interval based on repeat pattern"""
        patterns = {
            'occasional': 9,  # Average of 8-10
            'regular': 6,     # Average of 5-7
            'often': 3,       # Average of 3-4
        }
        return patterns.get(self.repeat_pattern, 6)


class JinglePlayHistory(models.Model):
    """
    Track when jingles were played for analytics
    """
    schedule = models.ForeignKey(
        JingleSchedule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='play_history'
    )
    jingle_filename = models.CharField(max_length=255)
    played_at = models.DateTimeField(auto_now_add=True)
    round_number = models.IntegerField()
    
    class Meta:
        ordering = ['-played_at']
        verbose_name = "Jingle Play History"
        verbose_name_plural = "Jingle Play History"
```

### Option 2: JSON-based Storage (Simpler, No Migration)

**Advantages:**
- No database migrations
- Easier deployment
- Matches current architecture

**File: `/data/jingle_schedules.json`**

```json
{
  "schedules": [
    {
      "id": "schedule_12345",
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
      "priority": 10,
      "created_at": "2026-01-16T10:00:00Z"
    }
  ]
}
```

---

## 🔌 Backend API Design

### New Endpoints

#### 1. Create Jingle Schedule
```http
POST /api/jingle-schedules
Content-Type: application/json

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

Response: 201 Created
{
  "success": true,
  "schedule_id": "schedule_12345",
  "message": "Schedule created successfully"
}
```

#### 2. List All Schedules
```http
GET /api/jingle-schedules

Response: 200 OK
{
  "schedules": [
    {
      "id": "schedule_12345",
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
      "next_play_round": 6
    }
  ]
}
```

#### 3. Update Schedule
```http
PUT /api/jingle-schedules/<schedule_id>
Content-Type: application/json

{
  "enabled": false
}

Response: 200 OK
{
  "success": true,
  "message": "Schedule updated"
}
```

#### 4. Delete Schedule
```http
DELETE /api/jingle-schedules/<schedule_id>

Response: 200 OK
{
  "success": true,
  "message": "Schedule deleted"
}
```

#### 5. Get Active Jingles (Critical for Playback)
```http
GET /api/jingle-schedules/active

Response: 200 OK
{
  "active_jingles": [
    {
      "jingle_filename": "jingle_67890.mp3",
      "jingle_name": "Tuesday Night Taco Promotion",
      "interval": 6,
      "priority": 10
    }
  ]
}
```

---

## 🎨 Frontend UI/UX Design

### New Page: Jingle Manager Dashboard

**Location:** `/jingle-manager` (new page)  
**Access:** Link from game.html and jingle.html

### Layout

```
┌─────────────────────────────────────────────────────────┐
│  🎵 JINGLE MANAGER                                      │
│  Schedule when your jingles play during games           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [+ Create New Schedule]    [View Calendar]            │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │ 📅 Tuesday Night Taco Promotion                   │ │
│  │ ──────────────────────────────────────────────── │ │
│  │ Status: 🟢 Active Now                            │ │
│  │ Dates: Jan 14 - Mar 31, 2026                     │ │
│  │ Time: 5:00 PM - 10:00 PM                         │ │
│  │ Days: [T]                                        │ │
│  │ Pattern: Regular (every 5-7 rounds)              │ │
│  │ File: jingle_67890.mp3                           │ │
│  │                                                   │ │
│  │ [▶️ Preview] [✏️ Edit] [🗑️ Delete] [Toggle ⚫]   │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │ 📅 Weekend Happy Hour                             │ │
│  │ ──────────────────────────────────────────────── │ │
│  │ Status: ⚫ Inactive (wrong day)                   │ │
│  │ Dates: Ongoing                                    │ │
│  │ Time: 4:00 PM - 7:00 PM                          │ │
│  │ Days: [F] [Sa] [Su]                              │ │
│  │ Pattern: Often (every 3-4 rounds)                │ │
│  │ File: jingle_55555.mp3                           │ │
│  │                                                   │ │
│  │ [▶️ Preview] [✏️ Edit] [🗑️ Delete] [Toggle ⚫]   │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Create/Edit Schedule Form

```
┌─────────────────────────────────────────────────────────┐
│  ✏️ Edit Schedule: Tuesday Night Taco Promotion         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1️⃣ Jingle Name                                        │
│  ┌───────────────────────────────────────────────────┐ │
│  │ Tuesday Night Taco Promotion                      │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  2️⃣ Select Jingle Audio                                │
│  ┌───────────────────────────────────────────────────┐ │
│  │ [Dropdown: Select from library]                   │ │
│  │ > jingle_67890.mp3 - "Tuesday Tacos..."           │ │
│  │   jingle_12345.mp3 - "Happy Hour Special"         │ │
│  └───────────────────────────────────────────────────┘ │
│  [▶️ Preview Selected Jingle]                           │
│                                                         │
│  3️⃣ Date Range                                         │
│  Start Date: [2026-01-14 📅]                           │
│  End Date:   [2026-03-31 📅]  ☑️ No end date          │
│                                                         │
│  4️⃣ Time Period (Optional)                             │
│  ☑️ Play only during specific hours                    │
│  Start Time: [17:00] (5:00 PM)                         │
│  End Time:   [22:00] (10:00 PM)                        │
│                                                         │
│  5️⃣ Days of Week                                       │
│  ┌─────────────────────────────────────────────────┐   │
│  │ [M] [T] [W] [Th] [F] [Sa] [Su]                  │   │
│  │  ☐   ☑   ☐   ☐   ☐   ☐    ☐                    │   │
│  └─────────────────────────────────────────────────┘   │
│  Tip: Click days to toggle                             │
│                                                         │
│  6️⃣ Repeat Pattern                                     │
│  ┌─────────────────────────────────────────────────┐   │
│  │ ○ Occasional - Every 8-10 rounds                │   │
│  │ ● Regular - Every 5-7 rounds                    │   │
│  │ ○ Often - Every 3-4 rounds                      │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  7️⃣ Priority (Optional)                                │
│  [──────────●─────────] 10                             │
│  Higher priority wins if multiple jingles qualify      │
│                                                         │
│  ☑️ Enabled (schedule is active)                       │
│                                                         │
│  [Cancel]  [Save Schedule]                             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### UI Components Needed

1. **Date Picker** - For start/end dates
2. **Time Picker** - For time ranges
3. **Day Toggle Buttons** - Visual day selector
4. **Radio Buttons** - Repeat pattern selection
5. **Dropdown** - Jingle selection from library
6. **Priority Slider** - 0-100 range
7. **Status Badge** - Active/Inactive indicator

---

## ⚙️ Playback Scheduler Logic

### Enhanced `checkAndPlayJingle()` Function

**Location:** `frontend/game.js`

**Current Logic:**
```javascript
// CURRENT: Simple interval-based
if (songsPlayed % interval === 0) {
    playJingle();
}
```

**New Logic:**
```javascript
async function checkAndPlayJingle() {
    // 1. Fetch active schedules from backend
    const activeSchedules = await fetchActiveJingles();
    
    if (activeSchedules.length === 0) {
        console.log('No active jingle schedules');
        return;
    }
    
    // 2. Check if any jingle should play this round
    const songsPlayed = gameState.called.length;
    
    for (const schedule of activeSchedules) {
        const shouldPlay = (songsPlayed > 0 && songsPlayed % schedule.interval === 0);
        
        if (shouldPlay) {
            console.log(`🎵 Playing scheduled jingle: ${schedule.jingle_name}`);
            
            updateStatus('🎵 Playing promotional jingle...', true);
            
            try {
                await playJingleAudio(schedule.jingle_filename);
                
                // Track play event (optional analytics)
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

async function fetchActiveJingles() {
    try {
        const apiUrl = CONFIG.API_URL || CONFIG.BACKEND_URL;
        const response = await fetch(`${apiUrl}/api/jingle-schedules/active`);
        const data = await response.json();
        return data.active_jingles || [];
    } catch (error) {
        console.error('Error fetching active jingles:', error);
        return [];
    }
}

async function trackJinglePlay(scheduleId, roundNumber) {
    try {
        const apiUrl = CONFIG.API_URL || CONFIG.BACKEND_URL;
        await fetch(`${apiUrl}/api/jingle-schedules/${scheduleId}/play`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ round_number: roundNumber })
        });
    } catch (error) {
        console.error('Error tracking jingle play:', error);
    }
}
```

### Backend Schedule Evaluator

**Location:** `backend/api/views.py`

```python
@api_view(['GET'])
def get_active_jingles(request):
    """
    Get all currently active jingle schedules
    Evaluates: date range, time period, day of week, enabled status
    Returns sorted by priority (highest first)
    """
    from datetime import datetime, date
    
    # Option A: Database-backed
    if USE_DATABASE:
        from .models import JingleSchedule
        all_schedules = JingleSchedule.objects.filter(enabled=True)
        active = [s for s in all_schedules if s.is_active_now()]
        
        return Response({
            'active_jingles': [
                {
                    'id': s.id,
                    'jingle_name': s.jingle_name,
                    'jingle_filename': s.jingle_filename,
                    'interval': s.get_interval(),
                    'priority': s.priority
                }
                for s in active
            ]
        })
    
    # Option B: JSON-backed
    else:
        schedules_file = DATA_DIR / 'jingle_schedules.json'
        if not schedules_file.exists():
            return Response({'active_jingles': []})
        
        with open(schedules_file, 'r') as f:
            data = json.load(f)
        
        now = datetime.now()
        today = date.today()
        current_time = now.time()
        current_weekday = today.weekday()  # 0=Mon, 6=Sun
        
        active_jingles = []
        
        for schedule in data.get('schedules', []):
            if not schedule.get('enabled', False):
                continue
            
            # Check date range
            start_date = datetime.fromisoformat(schedule['start_date']).date()
            if today < start_date:
                continue
            
            end_date_str = schedule.get('end_date')
            if end_date_str:
                end_date = datetime.fromisoformat(end_date_str).date()
                if today > end_date:
                    continue
            
            # Check time range
            time_start_str = schedule.get('time_start')
            time_end_str = schedule.get('time_end')
            if time_start_str and time_end_str:
                time_start = datetime.strptime(time_start_str, '%H:%M').time()
                time_end = datetime.strptime(time_end_str, '%H:%M').time()
                if not (time_start <= current_time <= time_end):
                    continue
            
            # Check day of week
            day_map = ['monday', 'tuesday', 'wednesday', 'thursday', 
                       'friday', 'saturday', 'sunday']
            current_day = day_map[current_weekday]
            if not schedule['days_of_week'].get(current_day, False):
                continue
            
            # Calculate interval
            pattern_intervals = {
                'occasional': 9,
                'regular': 6,
                'often': 3
            }
            interval = pattern_intervals.get(schedule['repeat_pattern'], 6)
            
            active_jingles.append({
                'id': schedule['id'],
                'jingle_name': schedule['jingle_name'],
                'jingle_filename': schedule['jingle_filename'],
                'interval': interval,
                'priority': schedule.get('priority', 0)
            })
        
        # Sort by priority (highest first)
        active_jingles.sort(key=lambda x: x['priority'], reverse=True)
        
        return Response({'active_jingles': active_jingles})
```

---

## 🔄 Implementation Phases

### Phase 1: Database & Backend (2-3 hours)
1. ✅ Create Django model `JingleSchedule`
2. ✅ Run migrations
3. ✅ Create API endpoints (CRUD + active)
4. ✅ Test with Postman/curl

### Phase 2: Frontend Manager UI (3-4 hours)
1. ✅ Create `jingle-manager.html` page
2. ✅ Build schedule list view
3. ✅ Build create/edit form with date/time pickers
4. ✅ Add validation and error handling
5. ✅ Test CRUD operations

### Phase 3: Game Integration (1-2 hours)
1. ✅ Update `checkAndPlayJingle()` in `game.js`
2. ✅ Add `fetchActiveJingles()` function
3. ✅ Test during actual game playback
4. ✅ Handle edge cases (no active schedules, API errors)

### Phase 4: Polish & Testing (1-2 hours)
1. ✅ Add analytics tracking
2. ✅ Add calendar view (optional)
3. ✅ Add conflict resolution (multiple schedules)
4. ✅ User documentation
5. ✅ Deploy to production

**Total Estimated Time:** 7-11 hours

---

## 📝 User Stories

### Story 1: Tuesday Taco Night
**As a** pub owner  
**I want to** schedule a jingle about "Tuesday Taco Night 2-for-1"  
**So that** it only plays on Tuesdays between 5pm-10pm

**Solution:**
- Jingle Name: "Tuesday Taco Night"
- Days: [Tuesday only]
- Time: 17:00 - 22:00
- Repeat: Regular (every 5-7 rounds)
- Dates: Ongoing

### Story 2: St. Patrick's Day Promotion
**As a** bar manager  
**I want to** promote our St. Patrick's Day event for 3 weeks leading up to March 17  
**So that** customers are reminded during games

**Solution:**
- Jingle Name: "St. Patrick's Day Countdown"
- Days: [All days]
- Time: [All day]
- Repeat: Often (every 3-4 rounds)
- Dates: Feb 24 - Mar 17
- Priority: 20 (high)

### Story 3: Weekend Happy Hour
**As a** venue manager  
**I want to** announce happy hour specials only on Friday, Saturday, Sunday  
**So that** weekday customers aren't confused

**Solution:**
- Jingle Name: "Weekend Happy Hour"
- Days: [Fri] [Sat] [Sun]
- Time: 16:00 - 19:00
- Repeat: Occasional (every 8-10 rounds)
- Dates: Ongoing

---

## 🎨 UI Mockup - Calendar View (Future Enhancement)

```
┌─────────────────────────────────────────────────────────┐
│  📅 Jingle Calendar - January 2026                      │
├─────────────────────────────────────────────────────────┤
│  Mon   Tue   Wed   Thu   Fri   Sat   Sun               │
│  ───   ───   ───   ───   ───   ───   ───               │
│   13    14    15    16    17    18    19               │
│        🎵    🎵          🎵    🎵🎵   🎵🎵              │
│                         (3)   (2)    (2)               │
│                                                         │
│  🎵 = Scheduled jingle                                  │
│  Click date to see scheduled jingles for that day      │
└─────────────────────────────────────────────────────────┘
```

---

## 🔐 Security Considerations

1. **Input Validation**
   - Validate date ranges (start < end)
   - Validate time ranges (start < end)
   - Sanitize jingle names (prevent XSS)
   - Validate filename exists before saving

2. **Authorization**
   - Only authenticated users can create schedules
   - Consider role-based access (admin vs. staff)

3. **File Access**
   - Verify jingle file exists on server
   - Prevent directory traversal in filenames
   - Check file size limits

4. **Rate Limiting**
   - Limit API calls to prevent abuse
   - Cache active schedules for performance

---

## 📊 Analytics & Reporting (Future)

### Potential Metrics to Track:

1. **Play Frequency**
   - Total plays per jingle
   - Average plays per game
   - Most popular jingles

2. **Timing Analytics**
   - Peak play times
   - Day-of-week distribution
   - Schedule effectiveness

3. **Engagement Metrics**
   - Round-by-round playback
   - Skip rate (if added)
   - Duration analysis

### Reports Dashboard:
- Weekly summary email
- Top performing jingles
- Schedule conflicts detected
- Coverage gaps (days with no jingles)

---

## 🚀 Deployment Checklist

- [ ] Run database migrations
- [ ] Update requirements.txt (if new dependencies)
- [ ] Test all API endpoints
- [ ] Test frontend UI flow
- [ ] Test game integration
- [ ] Add admin documentation
- [ ] Create user guide
- [ ] Deploy to staging
- [ ] User acceptance testing
- [ ] Deploy to production
- [ ] Monitor logs for errors

---

## 📚 Documentation Updates Needed

1. **User Guide**
   - How to create schedules
   - Best practices for scheduling
   - Troubleshooting common issues

2. **API Documentation**
   - New endpoints reference
   - Request/response examples
   - Error codes

3. **Developer Guide**
   - Architecture overview
   - Database schema
   - Frontend-backend integration

---

## 🎯 Success Metrics

**Definition of Done:**
- ✅ Pub owner can create named schedule with all 5 parameters
- ✅ Schedules only activate during specified date/time/days
- ✅ Repeat patterns work correctly (occasional/regular/often)
- ✅ Multiple schedules can coexist without conflicts
- ✅ Game correctly fetches and plays active jingles
- ✅ UI is intuitive and mobile-friendly
- ✅ System is stable and performant in production

**Key Performance Indicators:**
- Schedule creation time: < 2 minutes
- API response time: < 200ms
- Zero schedule conflicts
- 100% uptime during games

---

## 💡 Future Enhancements

1. **Smart Scheduling**
   - AI-powered optimal play times
   - Crowd size detection (play more when busy)
   - Weather-based scheduling (e.g., "Rainy Day Specials")

2. **A/B Testing**
   - Multiple jingles for same slot
   - Performance comparison
   - Automatic optimization

3. **Integration Features**
   - Import from Google Calendar
   - Sync with POS system
   - Social media cross-posting

4. **Advanced Controls**
   - Skip button during game
   - Volume control per jingle
   - Fade in/out options

5. **Multi-Venue Support**
   - Venue-specific schedules
   - Chain-wide campaigns
   - Regional promotions

---

**Document Version:** 1.0  
**Author:** GitHub Copilot  
**Review Status:** Ready for Implementation  
**Next Step:** Review with stakeholder and begin Phase 1

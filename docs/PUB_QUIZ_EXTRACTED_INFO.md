# Información Extraída de PDFs de Pub Quiz

Fecha de extracción: Tue Jan 20 10:04:27 -05 2026

---


## Pub Quiz 1 - Quizz Format.pdf

**Páginas:** 2


============================================================
Página 1 (OCR)
============================================================
Average Number of Questions in a Pub Quiz

Based on common practices, the average pub quiz typically features between 40 and 60
questions in total. This range allows for a balanced event that lasts around 1.5 to 2.5 hours
without overwhelming participants. Some formats go as low as 20-25 questions for shorter
bar trivia nights, while others extend to 70-80 for more comprehensive quizzes, especially
fundraisers or longer evenings. Aim for this sweet spot in your Al-generated quiz to keep

engagement high.

Number of Quiz Sessions (Rounds) Offered

Most pub quizzes are structured into 4-8 rounds, with 5-7 being the most typical to
maintain rhythm and prevent fatigue. Each round usually contains 10 questions, though
some vary to 8-12 per round for variety. If "sessions" refers to the overall event frequency
(e.g., how many quizzes a pub offers), it's often weekly, but your query seems focused on
the internal structure of a single quiz. For your automated setup, dividing into 5-6 rounds

would work well with TTS announcements.

General Format of Most Pub Quizzes

Pub quizzes are usually team-based events (teams of 4-6 people) held weekly in bars or
pubs, starting in the evening with an advertised time. A quizmaster (or in your case, Al with
TTS) announces questions aloud, while teams write answers on sheets; scoring happens

per round or at the end, with prizes for top teams.

The format often includes:


============================================================
Página 2 (OCR)
============================================================
» Rounds by theme: General knowledge, music (e.g., identify songs or artists), picture
rounds (visual identification), entertainment, geography, history, science, sports, and

sometimes a wildcard or puzzle round.

- Breaks and pacing: A halftime break for drinks/scoring, plus optional table rounds

(e.g., handouts teams complete at their pace).

* Question style: Mix of difficulties (easy, medium, hard) to engage everyone; avoid

multiple-choice to encourage discussion, and keep questions concise.
* Duration: 1.5-3 hours total, with 2 minutes per question as a rough guide.
This setup translates well to an Al version: Generate themed rounds, use TTS for

announcements, and perhaps integrate scoring via an app or simple input. If you're building

it automated, focus on variety to mimic the social, fun vibe of traditional pub quizzes.




---


## Pub Quiz 2 - Printed Answer Sheets.pdf

**Páginas:** 3


============================================================
Página 1 (OCR)
============================================================
QR Code for Team Registration and Social Media Engagement

Using a QR code on each pub table is a smart, contactless way to streamline registration

while boosting your social media presence. Here's how to implement it effectively:

* QR Code Design and Placement: Generate a QR code that links directly to a simple
registration form (e.g., via Google Forms, Typeform, or a custom web app). Include
fields for team name, number of players, and optional contact info like email or social
handles. Print the QR code on durable, laminated table tents or stickers that say
something inviting like "Scan to Join the Quiz & Follow Us for More Fun!" Place one per
table to make it easy and visible. To tie in your "Perfect DJ" brand, incorporate your

logo into the QR code design using tools like QR Code Monkey for a customized look.

+ Incentivizing Social Follows via QR: Make the QR code multifunctional. After
registration, redirect users to a landing page that prompts them to follow your social

media accounts (e.g., Instagram, X/Twitter, or Facebook) for a bonus. Ideas include:

+ Entry Bonus: "Follow @PerfectDJQuiz on Instagram for an extra point on tonight's

quiz!" or "Tag us in your team photo for a chance to win a free drink."

+ Exclusive Content: Promise followers access to quiz hints, behind-the-scenes DJ
mixes, or upcoming event teasers. For example, the landing page could say:

"Registered? Great! Follow us now for weekly quiz tips and DJ playlists."

+ Gamification: Use the QR to link to a social media poll or story where teams vote

on quiz themes, encouraging immediate engagement and follows.

+ Integration with Al Quiz: Since your quiz is Al-generated with TTS, have the
registration form feed data into a backend (like a Google Sheet or simple database)
that the Al can access for real-time team tracking. Announce registered teams via TTS

at the start, adding a fun, interactive element.

Custom Printed Answer Sheets for Promotion

Custom printing answer sheets adds a professional touch and turns them into mini
billboards for your brand and social media. Aim for high-quality paper (e.g., cardstock) to

make them feel premium. Here's how to maximize their impact:


============================================================
Página 2 (OCR)
============================================================
+ Layout and Content Ideas:

+ Header Branding: At the top, feature your "Perfect DJ" logo prominently, along
with the quiz name/date. Include a tagline like "Powered by Perfect DJ —- Where

Music Meets Trivia!"

+ Social Media Prompts: Dedicate space at the bottom or margins for calls-to-

action. Examples:
+ "Follow @PerfectDJ on X for live quiz updates and DJ gigs!"

+ "Share your scores on Instagram with #PerfectDJQuiz for a shoutout next

week."

+ Asmall QR code on the sheet itself linking to your social profiles or a

feedback form.

+ Themed Sections: Divide the sheet into rounds with space for answers (e.g.,
numbered lines or boxes). Add fun elements like a "Bonus Question" tied to social

media: "What's our latest DJ mix? Hint: Check our TikTok!"

+ Sponsorship Tie-Ins: If you have partners, include subtle promotions (e.g.,
“Brought to you by [Local Brewery] — Follow them too!"), but keep the focus on

your brand.

- Printing and Distribution Tips:

+ Batch Printing: Use services like Vistaprint or local printers for cost-effective
runs. Print in batches of 50-100 per event, customizing per quiz theme (e.g.,

music-themed borders for a DJ-branded night).

+ Eco-Friendly Option: Opt for recycled paper and note it on the sheet: "Printed on

eco-paper — Follow us for more green tips!"

+ Collection Strategy: At the end, have teams submit sheets for scoring, and use
this moment to remind them via TTS: "Don't forget to scan the QR or follow us on

the sheet for exclusive perks!"


============================================================
Página 3 (OCR)
============================================================
* Enhancing Professionalism: These sheets prevent messy handwriting issues and
make scoring easier (e.g., pre-printed grids). They also build loyalty — teams might

keep them as souvenirs, extending your brand reach.

Overall, this setup creates a seamless, engaging experience that boosts participation and
your online following. Start small with one event to test, then iterate based on feedback. If

you need help generating sample QR codes or sheet templates, let me know!




---


## Pub Quiz 3 - using Quiz Buzzers.pdf

**Páginas:** 4


============================================================
Página 1 (OCR)
============================================================
Hardware Selection for BLE Buzzers

To create physical BLE (Bluetooth Low Energy) buttons that teams can pair with their
phones, focus on affordable, programmable hardware that supports BLE peripherals. The
button acts as a BLE device advertising its state (e.g., pressed), and the phone connects as

the central device to receive notifications.
+ Recommended Components:

+ ESP32 Microcontroller: Inexpensive (around $5-10) with built-in BLE. Connect a
simple push button to a GPIO pin. When pressed, the ESP32 can send a BLE
notification. Tutorials like those using Arduino IDE make this straightforward—

program it to enter BLE mode and notify on press.

+ Adafruit Circuit Playground Bluefruit: A ready-made board (~$25) with built-in
buttons, LEDs, speaker, and BLE. It's perfect for prototyping; press the button to
trigger BLE events, add lights for visual feedback (e.g., pulsing for buzz order),
and even sounds. This was used in a DIY game show buzzer project where buzzers

connect to a central system.

+ Arduino Nano + HM-10 BLE Module: For a custom build, pair an Arduino (~$5)
with an HM-10 (~$5). Wire the button to the Arduino, and use the HM-10 for BLE
communication. This setup was detailed in a Bluetooth quiz buzzer Instructable,

including code for button detection and BLE transmission.

+ Power and Enclosure: Use rechargeable batteries (e.g., LiPo with TP4056
charger) for portability. 3D-print or buy enclosures to make them look

professional—add team colors or your "Perfect DJ" branding.

- Pairing Process: Each buzzer advertises a unique UUID or name (e.g., "Team1Buzzer").
Teams use their phone's Bluetooth settings or your app to pair once per event. Limit to

one phone per buzzer to avoid conflicts.

Mobile App for Phone Integration

Since participants pair their phones with the BLE buttons, you'll need a simple app to
handle the connection, detect presses, and relay them to the server. This keeps it user-

friendly—no need for everyone to be tech-savvy.


============================================================
Página 2 (OCR)
============================================================
+ App Development Options:

+ MIT App Inventor (No-Code Approach): Ideal for beginners. Create an
Android/iOS app that scans for BLE devices, connects to the buzzer, and
subscribes to a characteristic for button press notifications. On detection, the app
sends the event to your server. A tutorial shows this controlling an ESP32 via BLE
—adapt it for button input instead of output. Add features like team registration

(tie into your QR code system) and social media prompts post-quiz.

+ React Native or Flutter (Cross-Platform): For a polished app, use libraries like

react-native-ble-plx (for BLE handling). The app could:
+ Prompt users to pair via phone Bluetooth.
+ Listen for GATT notifications from the buzzer.

+ On press, capture a precise timestamp and send it via WebSocket/HTTP to

the server, including team ID.

+ Display buzz confirmation (e.g., "You buzzed first!") and encourage social

follows (e.g., "Share your win on @PerfectDJ!").

+ Hybrid with Web App: If avoiding native apps, use a Progressive Web App (PWA)
that accesses Bluetooth via Web Bluetooth API (supported in Chrome/Android).

Users scan the table QR to load it, then pair.

- User Flow: After QR registration, the app guides pairing: "Scan for your table's buzzer
and connect." Test for latency—BLE notifications are fast (~10-50ms), but add phone

vibration for feedback.

Server and Real-Time Processing

The server is the brain: It receives buzz signals, ranks them by timestamp, and integrates
with your Al/TTS for announcements. This ensures fair ordering and adds excitement with

lockouts.


============================================================
Página 3 (OCR)
============================================================
» Backend Setup:

+ Node.js with Socket.io: Host on a local pub computer or cloud (e.g.,
Heroku/AWS). Use Express for API endpoints where apps POST buzz events (e.g.,
{teamld: "Team1", timestamp: Date.now()}). Socket.io handles real-time
broadcasting of results to all connected devices or the main screen. In a Bluetooth
buzzer project, a Python script on a laptop managed similar multi-device

connections—adapt to Node for web integration.

+ Firebase Realtime Database: No-server alternative for simplicity. Apps write buzz
entries to a "buzzes" collection; a cloud function sorts by timestamp and triggers

updates. Great for scaling to multiple teams.

+ Handling Order and Lockouts: On receiving buzzes within a short window (e.g., 1-
2 seconds after question), sort by timestamp. Announce via TTS: "Team 1 buzzed
first, followed by Team 3!" Lock out further buzzes until reset. Add a reset

endpoint for the quizmaster (you or Al).

- Latency Mitigation: Use NTP sync for accurate timestamps across phones. Test in the

pub for Bluetooth range (up to 10-20m).

Integration with Al Quiz and TTS

Tie this into your existing setup for a seamless exciting finale:

- Warl flause


============================================================
Página 4 (OCR)
============================================================
> Wurniiuw.
1. Al generates 5-10 rapid-fire questions for the end round.
2. TTS announces: "Question: What is the capital of France? Buzz in!"
3. Teams press buttons; phones relay to server.

4. Server determines order, notifies Al/system.

5.

TTS calls out the order: "Team Blue first—your answer?" (Verbal response,

scored manually or via app input).
6. Reset for next question.
» Enhancements for Excitement:

+ Sounds and Lights: Program buzzers for buzz sounds/LED flashes. Server triggers

pub speakers for dramatic effects (e.g., "BOOM" like in game shows).
+ Scoring Boost: First buzz gets bonus points; promote via answer sheets.
* Social Tie-In: After round, app prompts: "Buzz king? Follow @PerfectDJ for more!"

+ Display: Project buzz order ona screen via server websocket.

Prototyping and Testing Tips

- Start small: Build 4 buzzers, test with friends. Use Arduino sketches from Instructables
for BLE code.

* Cost: ~$20-50 per buzzer, app dev free with MIT.
+ Security: Use auth tokens in app-server comms to prevent cheating.

- Alternatives: If BLE proves tricky, consider WiFi-based buttons (e.g., ESP32

connecting directly to server), but stick to BLE for phone pairing as specified.

This setup will amp up the energy—teams racing to buzz creates that game-show thrill. If

you need sample code snippets or specific wiring diagrams, provide more details!




---


## Pub Quiz 4 - Gentre Selection.pdf

**Páginas:** 3


============================================================
Página 1 (OCR)
============================================================
Here are 50 engaging quiz genres (themes/categories/round types) you can offer during

team registration via your QR code form. This lets participants vote or select preferences,

helping you tailor the night's quiz to the audience—ensuring high energy, broad appeal, and

inclusivity while encouraging discussion and social media shares (e.g., "We voted for 90s

Nostalgia—follow @PerfectDJ for hints!").

These draw from classic pub quiz staples, creative twists, and popular trends, mixing

evergreen favorites with fun, niche options to suit diverse crowds in a NYC pub setting.

1.

o 9 Nona fF WN

10.

11.

12.
13.
14.
15.
16.
17.
18.
19.

General Knowledge

Pop Music

Movies & Film

Television & Streaming Shows

80s Nostalgia

90s Nostalgia

2000s Throwback

2010s Pop Culture

Current Events & News (2025-2026 highlights)
Sports (General or specific like NFL, Soccer, Basketball)
Geography & World Capitals

History (World, US, or Ancient)

Science & Inventions

Food & Drink

Cocktails & Alcohol

Celebrities & Gossip

Disney & Pixar

Harry Potter

Superheroes & Marvel/DC


============================================================
Página 2 (OCR)
============================================================
20.

21.

22.

23.

24.

25.

26.

27.

28.

29.

30.

31.

32.
33.
34.
35.
36.
37.
38.
39.
40.

Al.

42.
43.
44.

Video Games

Animals & Nature

Mythology & Legends

Literature & Books

Broadway & Musicals

Art & Famous Paintings

Tech & Gadgets

Al & Future Tech

Memes & Viral Trends

Picture Round (Identify from images)

Music Round (Name That Tune)
Connections (Hidden links between answers)
Anagrams & Wordplay

Riddles & Brain Teasers

What Happened Next?

Wrong Answers Only (Funniest wins bonus)
Hidden Theme Rounds

Slogans & Brands

Toys & Games (Board games, childhood)
Fashion & Style

Holidays & Seasonal (e.g., upcoming events)
New York City Trivia

Famous Quotes

True or False

Rapid Fire / Buzzer Questions


============================================================
Página 3 (OCR)
============================================================
45.

46.

47.

48.

49.

50.

70s Disco & Funk
Hip-Hop & Rap
Classic Rock
Country Music
Horror Movies

Space & Astronomy

Implementation Tips for Registration

+ Dropdown or Multi-Select: Let teams pick their top 3-5 favorites during QR

registration. Use this data to prioritize rounds (e.g., if 70% pick Music and 90s, lean

heavy on those).

+ Engagement Boost: Display real-time vote tallies on a screen or via TTS

announcement: "Tonight's crowd loves 90s Nostalgia and Food & Drink—get ready!"

» Audience Suitability: For a mixed pub crowd, always include a few broad ones (like

General Knowledge or Pop Culture) as defaults, while niche picks (e.g., Harry Potter or

NYC Trivia) add excitement for superfans.

+ Tie to Your Brand: Theme some around music/DJ vibes, like "Name That Tune" or "80s

Nostalgia," to promote your Perfect DJ identity.

This variety keeps things fresh across events—rotate based on votes to build loyalty. If a

genre dominates, you could even run special theme nights announced on social media! Let

me know if you want sample questions for any of these.




---


# Smooth Onboard

Smarter starts for better learning journeys.

## Overview

Smooth Onboard is an AI-powered onboarding assistant that assesses student skill level, predicts retention, and enables personalized learning before the first lesson.

Instead of static forms, learners interact with an AI agent that gathers insights through conversation, combining responses, sentiment, and behavioral signals into actionable outputs.

---

## Motivation

### For Students
- Immediate understanding of their current skill level  
- Personalized feedback from the start  
- No scheduling required for initial assessment  

### For Tutors
- Pre-class overview of student strengths and weaknesses  
- Insight into motivation and learning intent  
- Retention likelihood (confidence score)  

### For the Platform
- Conversion rate estimation  
- Early identification of high-retention users  
- Improved matching and personalization  

We already collect most of this data during onboarding, this approach enhances it with sentiment analysis and behavioral biomarkers.

---

## How It Works

1. **Optional AI Onboarding**  
   Learners can opt in to preserve experience for AI-skeptical users.

2. **Native Language Start**  
   The agent begins in the learner’s native language and asks about motivation, goals, and background.  
   This enables sentiment and behavioral signal extraction.

3. **Language Switch**  
   The learner is invited to switch to the target language:  
   - If yes: assess initial language ability  
   - If no: continue collecting predictive signals  

4. **AI Analysis**  
   Responses, sentiment, and engagement patterns are combined into a confidence score predicting retention.

5. **Student Feedback**  
   - Skill level overview  
   - Strengths and areas for improvement  
   - Suggested focus areas  

   Potential extension: progress check-ins over time.

6. **Tutor Insight Sheet**  
   Tutors receive a summary before the first lesson including:  
   - Skill assessment  
   - Strengths and gaps  
   - Motivation insights  
   - Confidence score  

---

## Key Features

- Conversational AI onboarding  
- Sentiment and biomarker analysis  
- Retention prediction  
- Personalized learning insights  
- Instant assessment without scheduling  
- Tutor-ready summaries  

### Session Report System — Final Feature List

#### 1. Session Snapshot Generation
- Creates a complete session report at the end-of-session 
- Includes:
  - Transcript (all messages)
  - Biomarkers (Thymia)
  - Session metadata (channel, appId, agentId, endReason)
- Generates unique report IDs per session

#### 2. Idempotent Report Handling
- Prevents duplicate reports within a **5-second window per channel**
- Returns the latest report if re-triggered too quickly

#### 3. Transcript Structuring
- Normalizes messages into a clean, consistent format:
  - `role`, `content`, `timestamp`
  - Optional tool call data
- Ensures reports are reliable and easy to process

#### 4. Session Timing & Duration
- Automatically calculates:
  - Start time (first message)
  - End time (report generation)
  - Total duration in seconds
- Handles missing timestamps gracefully

#### 5. Biomarker Integration (Thymia)
- Attaches Thymia session metrics to each report
- Fails safely without interrupting report creation

#### 6. Storage (Memory + Disk)
- Caches recent reports in memory (max 50, oldest removed)
- Persists reports as JSON files in `./session-reports/`

#### 7. Report Access APIs
- Retrieve individual reports (`getReport`)
- Get latest report per channel
- List summarized reports (duration, size, biomarker presence)


### Student Dashboard — Final Feature List

#### 1. Conversational AI Assessment (Intake Flow)
- Starts in the student's **native language**, then invites switch to English for soft level signals.
- Collects:
  - Target language
  - Goal (career / kids / exams / culture)
  - Timeline (1–4 weeks → as long as it takes)
  - Inspiration (travel / culture / music / family / challenge)
  - Topic focus (conversational / beginner / intensive / business / American English)
  - Current level (self-reported: beginner → fluent)
  - Teaching style preferences (up to 3 traits)
  - Tutor country preference
  - Other languages tutor should speak
  - Weekly availability (schedule)
  - Budget / price range per lesson
  - Lessons per week & session duration
  - Prior learning experience

#### 2. Editable Preferences Panel
- Shows all collected filters as **editable chips**, grouped into:
  - **Learning Goals:** goal, inspiration, topic focus, timeline
  - **Tutor Preferences:** country, languages, teaching style
  - **Scheduling & Budget:** availability grid, price range, frequency, duration

#### 3. Proficiency Assessment
- AI-generated analysis from the conversation:
  - Skill bars: Speaking, Listening, Vocabulary, Grammar
  - Level labels: Beginner / Intermediate / Advanced
  - **Strengths:** 2–3 key positives
  - **Areas to improve:** 2–3 framed as opportunity
  - Overall level badge (e.g., Intermediate)

#### 4. Motivation Summary
- Friendly recap of AI understanding:
  - Goal in their own words (quote-style)
  - Inspiration tags
  - Timeline / urgency

#### 5. Tutor Match Preview
- Teaser: “We found X tutors matching your profile”
- 3 tutor cards (avatar, rating, price range, partially blurred) to build excitement

#### 6. "Find My Professor" CTA
- Large, prominent button
- Subtitle: “Your personalized matches are ready”
- Opens main Preply app with pre-filled filters

---

## Architecture

### Used APIs
The following APIs are used in this project:
* **Anam**: Simulating a lifelike human AI avatar to engage users and offer a familiar experience. 
* **Agora**: Decreasing latency via routing traffic through Agoras WebRTC to make the interaction smoother and more realistic. 
* **Thymia**: Real-time analysis of human-AI interaction via sentiment analysis to reliably predict retainment scores.
* **OpenAI**: Transforming speech-to-text and translating data from the human-AI onboarding call into tangible dashboard data.

### File Structure

```
submissions/
├── team-name/
│   ├── docs/              # Additional documentation and images
│   ├── src/               # The source code to our feature
│   ├── demo.mp4           # A short demo video from a students perspective
│   ├── HOW_WE_BUILT.md    # Documentation of our AI development process
│   └── README.md          # Description of our project
```
 
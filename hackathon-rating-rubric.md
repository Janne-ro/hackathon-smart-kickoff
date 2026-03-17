# Preply x Agora Hackathon: AI Agents for NextGen Language Learning - Judging Rubric

## Overview

This rubric provides a structured framework for evaluating hackathon submissions. Each project will be scored across 5 categories on a scale of 1-5, with specific criteria for each score level. All categories are weighted equally at 20%.

---

## Judging Panel

### Petro

**Petro** | Preply
_Expertise: Language learning and EdTech_

### Ben

**Ben** | Agora
_Expertise: Real-time communication and Conversational AI_

### Max

**Max** | OpenAI
_Expertise: AI and machine learning_

---

## Project Requirements

### Recommended Technologies

The following Agora products are available to all teams. Integrating partner technologies earns bonus points (see [Bonus Points](#bonus-points)).

| Technology                  | Description                                             | Documentation                                                                |
| --------------------------- | ------------------------------------------------------- | ---------------------------------------------------------------------------- |
| **Agora Conversational AI** | Voice AI agents with real-time STT → LLM → TTS pipeline | [Docs](https://docs.agora.io/en/conversational-ai/overview/product-overview) |
| **Agora RTC SDK**           | Real-time audio/video calling and streaming             | [Docs](https://docs.agora.io/en/video-calling/overview/product-overview)     |
| **Agora RTM (Signaling)**   | Real-time messaging, presence, and data channels        | [Docs](https://docs.agora.io/en/signaling/overview/product-overview)         |
| **Agora App Builder**       | No-code video calling experiences                       | [App Builder](https://appbuilder.agora.io/)                                  |
| **Agora Cloud Recording**   | Record calls and streams in the cloud                   | [Docs](https://docs.agora.io/en/cloud-recording/overview/product-overview)   |

### Project Rules

- Projects must address a language learning use case

- Code must be original work created during the hackathon

- Teams may use pre-existing libraries, frameworks, and APIs (with proper attribution)

- Teams must submit a working demo and source code via pull request

---

## Evaluation Process

Projects will be evaluated through a structured multi-phase process combining technical review, live demonstrations, and deliberation among judges.

### Evaluation Phases

**Submission Review**
Judges independently review code, documentation, and demo videos

**Live Demonstrations**
Teams present their projects and answer technical questions from judges

**Scoring & Deliberation**
Judges complete individual scoring, then meet to calibrate and finalize rankings

**Results Announcement**
Winners announced with feedback highlights for all teams

### Scoring Methodology

Each judge scores every category on a 1-5 scale. All 5 categories are weighted equally at 20%.

- 5 (High): Best possible — see category descriptors
- 4: Strong with minor gaps
- 3: Meets expectations, solid execution
- 2: Functional but lacking
- 1 (Low): Minimal — see category descriptors

Final scores are calculated as a simple average of the 5 category scores (maximum 5 points). Bonus points of up to +1 each may be awarded for integrating Agora ConvoAI, Thymia, or Anam.

---

## Scoring Categories

### Technology Use (20%)

_Breadth and depth of technologies combined in the project_

| Score | Description                                                                                                              |
| ----- | ------------------------------------------------------------------------------------------------------------------------ |
| 5     | Multiple technologies combined effectively (STT, TTS, LLMs, Avatars, etc.); thoughtful integration of diverse providers |
| 4     | Several technologies integrated well with minor gaps in depth                                                            |
| 3     | Reasonable technology stack with some variety; solid but not ambitious                                                   |
| 2     | Limited technology use; mostly a single provider or surface-level integration                                            |
| 1     | Single technology/provider used with minimal integration effort                                                          |

### Relevancy (20%)

_How relevant the project is for Preply and language learning_

| Score | Description                                                                                                              |
| ----- | ------------------------------------------------------------------------------------------------------------------------ |
| 5     | Could be added to the Preply product tomorrow; directly addresses a real language learning need                          |
| 4     | Highly relevant with a clear path to product integration; minor gaps in applicability                                    |
| 3     | Relevant to language learning with reasonable connection to Preply's mission                                             |
| 2     | Loosely connected to language learning; relevancy to Preply is a stretch                                                 |
| 1     | Not relevant for Preply or language learning                                                                             |

### Product Scope (20%)

_Scale of the problem being addressed_

| Score | Description                                                                                                              |
| ----- | ------------------------------------------------------------------------------------------------------------------------ |
| 5     | Aims to solve a global problem affecting millions of language learners                                                   |
| 4     | Targets a significant audience with broad applicability                                                                  |
| 3     | Addresses a meaningful problem for a moderate-sized audience                                                             |
| 2     | Solves a problem for a limited audience or narrow use case                                                               |
| 1     | Addresses a niche problem with minimal scale potential                                                                   |

### Presentation & Demo (20%)

_Quality of the pitch and live demonstration_

| Score | Description                                                                                                              |
| ----- | ------------------------------------------------------------------------------------------------------------------------ |
| 5     | Live demo, great pitch ready for YCombinator; compelling storytelling, smooth demonstration, handles questions well      |
| 4     | Strong presentation with a working live demo; minor rough edges in delivery                                              |
| 3     | Decent presentation with demo (live or recorded); gets the point across                                                  |
| 2     | Presentation covers the basics but demo is limited or pre-recorded only                                                  |
| 1     | Submitted and presented but no live demo                                                                                 |

### Quality (20%)

_Overall project quality including UX, bugs, and AI craftsmanship_

| Score | Description                                                                                                              |
| ----- | ------------------------------------------------------------------------------------------------------------------------ |
| 5     | Well thought-out UX, no bugs during live demo, good quality project. Includes documented AI development process (`HOW_WE_BUILT.md`) with prompts, model choices, and iteration. |
| 4     | Polished experience with minor rough edges. Some documentation of AI workflow.                                           |
| 3     | Functional with decent UX. Basic quality throughout.                                                                     |
| 2     | Works but clunky. Noticeable bugs or UX issues.                                                                          |
| 1     | Barely working, clunky UX, significant quality issues.                                                                   |

### Bonus Points

Each partner integration bonus is scored independently, up to +1 each.

#### Agora ConvoAI (up to +1)

_Teams that integrate Agora Conversational AI into their project_

| Score | Description                                                                                                              |
| ----- | ------------------------------------------------------------------------------------------------------------------------ |
| +1.0  | Deep, effective integration of Agora ConvoAI as a core part of the project; demonstrates strong understanding of the platform |
| +0.75 | Solid ConvoAI integration with meaningful use beyond basic setup                                                         |
| +0.5  | Working ConvoAI integration that adds value to the project                                                               |
| +0.25 | Basic ConvoAI integration; minimal use or largely unchanged from starter template                                        |
| +0    | No Agora ConvoAI integration                                                                                             |

#### Thymia Voice Biomarkers (up to +1)

_Teams that integrate Thymia's real-time voice biomarker analysis_

| Score | Description                                                                                                              |
| ----- | ------------------------------------------------------------------------------------------------------------------------ |
| +1.0  | Deep integration of Thymia biomarkers that meaningfully shapes the learning experience (e.g., agent adapts based on stress/emotion) |
| +0.75 | Solid biomarker integration with real-time display and some agent awareness                                              |
| +0.5  | Working Thymia integration that surfaces biomarker data to the user or agent                                             |
| +0.25 | Basic Thymia integration; biomarker data captured but minimally used                                                     |
| +0    | No Thymia integration                                                                                                    |

#### Anam Video Avatars (up to +1)

_Teams that integrate Anam's real-time video avatar rendering_

| Score | Description                                                                                                              |
| ----- | ------------------------------------------------------------------------------------------------------------------------ |
| +1.0  | Deep avatar integration that enhances the learning experience; lip-sync, expressions, and avatar choice add real value   |
| +0.75 | Solid avatar integration with good visual quality and meaningful use in the learning flow                                |
| +0.5  | Working Anam integration that adds a visual avatar to the conversation                                                   |
| +0.25 | Basic Anam integration; avatar present but minimally customized or utilized                                              |
| +0    | No Anam integration                                                                                                      |

---

## Scoring Sheet

| Team Name | Technology Use (20%) | Relevancy (20%) | Product Scope (20%) | Presentation & Demo (20%) | Quality (20%) | Agora Bonus | Thymia Bonus | Anam Bonus | Total Score | Notes |
| --------- | -------------------- | ---------------- | ------------------- | ------------------------- | ------------- | ----------- | ------------ | ---------- | ----------- | ----- |
|           |                      |                  |                     |                           |               |             |              |            |             |       |

## Final Score Calculation

- Each judge scores every category 1-5
- All 5 categories are weighted equally at 20%
- The category scores are averaged to produce the base score (maximum 5 points)
- Bonus points of up to **+1 each** are awarded for Agora ConvoAI, Thymia, and Anam integration
- Maximum possible score: **8** (5 base + 3 bonus)

## Feedback Section

For each submission, judges should provide:

1. **Strengths**: Key positive aspects of the project
2. **Areas for Improvement**: Constructive feedback on how the project could be enhanced
3. **Additional Comments**: Any other relevant observations or suggestions

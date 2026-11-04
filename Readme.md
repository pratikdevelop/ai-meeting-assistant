
# AI Meeting Assistant

An AI-powered real-time meeting assistant built with **Angular 22, Python, Pipecat, Groq, Kokoro TTS, FastAPI, and Supabase PostgreSQL**.

The application enables users to interact with an AI voice assistant through their browser in real time. It captures spoken conversations, converts speech into text, generates intelligent responses, and speaks those responses back to the user.

The long-term goal is to transform this real-time voice assistant into a complete AI meeting productivity platform that can automatically summarize meetings, extract important discussion points, identify action items, track decisions, and make meeting information searchable.

---

## Table of Contents

- [Introduction](#introduction)
- [Project Objectives](#project-objectives)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [Environment Variables](#environment-variables)
- [Running the Application](#running-the-application)
- [Development Roadmap](#development-roadmap)
- [Database Design](#database-design)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)

---

## Introduction

Meetings are an important part of collaboration, but managing meeting notes, remembering important discussions, tracking decisions, and following up on assigned tasks can be time-consuming.

The **AI Meeting Assistant** aims to solve these problems through real-time voice interaction and AI-powered meeting intelligence.

Users can communicate naturally with the assistant using their microphone. The system processes speech through an automatic speech recognition service, sends the recognized text to a large language model, and converts the generated response into natural speech.

In addition to voice interaction, the platform maintains meeting transcripts and is designed to generate structured meeting insights after a conversation ends.

### What makes this project useful?

- Real-time voice-based interaction.
- Automatic speech-to-text conversion.
- AI-generated conversational responses.
- Natural speech generation using a locally running Kokoro model.
- Persistent meeting and transcript storage.
- Planned automatic meeting summaries and action-item extraction.
- A centralized dashboard for managing meeting history and insights.

The project combines cloud-based AI services with local speech synthesis to create a flexible and extensible architecture.

---

## Project Objectives

1. Build a real-time browser-based AI voice assistant.
2. Process user speech and generate intelligent responses.
3. Provide natural speech output with low-latency audio streaming.
4. Save meeting information and transcripts in a PostgreSQL database.
5. Generate automatic summaries and structured meeting insights.
6. Provide an intuitive Angular dashboard for meeting management.
7. Introduce authentication, personalization, and secure data access.
8. Prepare the application for production deployment.

---

## Key Features

### 1. Real-Time Voice Conversation

- Browser microphone integration.
- Real-time audio communication using WebRTC.
- Speech recognition using Groq Whisper.
- AI response generation using Groq LLM.
- Speech generation using Kokoro TTS.
- Voice activity detection using Silero VAD.

### 2. AI-Powered Responses

- Natural language understanding.
- Context-aware conversations.
- Concise conversational responses.
- Streaming audio output through Pipecat.

### 3. Meeting Management

- Create meetings.
- Store meeting metadata.
- Save conversation transcripts.
- Track meeting status.
- View previous meetings.

### 4. Transcript Management

- Store user and assistant messages.
- Associate transcripts with individual meetings.
- Preserve conversation timestamps.
- Display conversation history.

### 5. Meeting Intelligence — Planned

- Automatic meeting summaries.
- Key discussion points.
- Action-item extraction.
- Decision tracking.
- AI-generated meeting insights.

### 6. User Management — Planned

- User registration and login.
- Personal meeting history.
- Secure access to meeting data.
- User-specific preferences.

---

## Technology Stack

| Category                   | Technology          |
| -------------------------- | ------------------- |
| Frontend                   | Angular 22          |
| Styling                    | Tailwind CSS        |
| UI Components              | Angular Material    |
| Programming Language       | TypeScript          |
| Backend API                | Python, FastAPI     |
| Real-Time AI Pipeline      | Pipecat             |
| Communication              | WebRTC, SmallWebRTC |
| Speech-to-Text             | Groq Whisper        |
| Large Language Model       | Groq LLM            |
| Text-to-Speech             | Kokoro TTS          |
| Voice Activity Detection   | Silero VAD          |
| Database                   | Supabase PostgreSQL |
| ORM                        | SQLAlchemy          |
| Numerical Audio Processing | NumPy               |
| Deep Learning Runtime      | PyTorch             |
| Version Control            | Git, GitHub         |

---

## System Architecture

The application follows a modular architecture that separates frontend interaction, backend APIs, real-time voice processing, and persistent storage.

```text
                 Angular 22 Frontend
                       |
             +---------+---------+
             |                   |
          REST API             WebRTC
             |                   |
             v                   v
         FastAPI             Pipecat Server
          :8000                 :7860
             |                   |
             |           +-------+-------+
             |           |       |       |
             |         Groq    Groq    Kokoro
             |         STT     LLM      TTS
             |           |       |       |
             |           +-------+-------+
             |                   |
             |              Audio Output
             |                   |
             +---------+---------+
                       |
                       v
                Supabase PostgreSQL
                       |
              Meeting Transcripts
                       |
                AI Meeting Analyzer
                  (Planned)
                       |
              +--------+--------+
              |        |        |
            Summary  Actions  Decisions
              |        |        |
              +--------+--------+
                       |
                       v
               Angular Dashboard
```

### Architecture Responsibilities

**Angular Frontend**

- User interface and meeting dashboard.
- Microphone and voice interaction controls.
- Meeting history and transcript display.
- Presentation of AI-generated insights.

**FastAPI Backend**

- REST API endpoints.
- Meeting creation and management.
- Transcript persistence.
- Database operations.
- Future meeting analysis endpoints.

**Pipecat Server**

- Real-time voice pipeline.
- WebRTC audio transport.
- Speech-to-text processing.
- LLM response generation.
- Text-to-speech processing.

**Supabase PostgreSQL**

- Meeting records.
- Transcript records.
- Meeting insights.
- Future user and application data.

---

## How It Works

### Real-Time Voice Processing

1. The user opens the Angular application.
2. The user creates or starts a meeting.
3. The browser requests microphone permission.
4. Audio is transmitted through WebRTC to the Pipecat server.
5. Groq Whisper converts speech into text.
6. The recognized text is passed to the LLM.
7. Groq generates a conversational response.
8. Kokoro converts the response into audio.
9. Pipecat streams audio frames back to the browser.
10. The conversation transcript is saved through FastAPI.

### Meeting Intelligence Processing — Planned

After a meeting ends:

1. Retrieve the meeting transcript.
2. Send the transcript to the AI meeting analyzer.
3. Generate a structured response.
4. Extract the meeting summary.
5. Identify key discussion points.
6. Extract action items and responsible participants when available.
7. Identify decisions and agreements.
8. Validate the generated structured data.
9. Save the results in Supabase PostgreSQL.
10. Display the insights on the meeting details page.

---

## Project Structure

The following represents the intended high-level organization. Some modules are already implemented, while others will be introduced in later phases.

```text
ai-meeting-assistant/
│
├── backend/
│   ├── api/
│   │   ├── meetings.py
│   │   └── insights.py                 # Planned
│   │
│   ├── db/
│   │   ├── database.py
│   │   └── models.py
│   │
│   ├── services/
│   │   └── meeting_analyzer.py         # Planned
│   │
│   └── app.py
│
├── chatbot/
│   ├── pipeline.py
│   ├── context.py
│   ├── llm.py
│   ├── aggregator.py
│   ├── tts.py
│   └── kokoro_service.py
│
├── config/
│   └── settings.py
│
├── processors/
│
├── services/
│   └── stt/
│
├── pipecat-ai-frontend/
│   └── src/
│       └── app/
│           ├── core/
│           ├── features/
│           ├── services/
│           └── shared/
│
├── bot.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Installation and Setup

### Prerequisites

Install the following before running the project:

- Python 3.11
- Node.js and npm
- Angular CLI compatible with Angular 22
- Git
- Supabase account
- Groq API key
- Microphone-enabled browser

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-meeting-assistant.git

cd ai-meeting-assistant
```

### 2. Create Python Virtual Environment

Windows PowerShell:

```powershell
python -m venv env

.\env\Scripts\Activate.ps1
```

### 3. Install Python Dependencies

```powershell
pip install -r requirements.txt
```

If dependencies are not yet recorded:

```powershell
pip install fastapi uvicorn pipecat-ai python-dotenv numpy kokoro sqlalchemy psycopg2-binary
```

Install any additional packages required by your configured Pipecat transports and integrations.

### 4. Install Angular Dependencies

```powershell
cd pipecat-ai-frontend

npm install
```

Return to the root directory when needed:

```powershell
cd ..
```

### 5. Configure Supabase

1. Create a Supabase project.
2. Open the project's database connection settings.
3. Obtain the appropriate PostgreSQL connection string.
4. Configure the connection string in your root `.env` file.
5. Keep your database credentials private.

---

## Environment Variables

Create a `.env` file in the project root.

Example:

```env
# Groq API
GROQ_API_KEY=your_groq_api_key

# LLM Configuration
MODEL=openai/gpt-oss-120b

# Speech Recognition
WHISPER_MODEL=whisper-large-v3

# Database
DATABASE_URL=your_supabase_postgresql_connection_string
```

The variable names must match the configuration used in `config/settings.py` and `backend/db/database.py`.

**Security:**

- Never commit `.env` to GitHub.
- Never expose API keys in frontend code.
- Use `.env.example` to document required variables without real credentials.
- Use secure database credentials and appropriate access controls.

---

## Running the Application

The project uses three separate processes.

### Terminal 1: FastAPI Backend

From the project root:

```powershell
uvicorn backend.app:app --reload --port 8000
```

API documentation:

```text
http://localhost:8000/docs
```

Backend health check:

```text
http://localhost:8000/health
```

### Terminal 2: Pipecat WebRTC Server

From the project root:

```powershell
python .\bot.py -t webrtc
```

Pipecat Playground:

```text
http://localhost:7860/client/
```

### Terminal 3: Angular Frontend

```powershell
cd pipecat-ai-frontend

npm start
```

Frontend:

```text
http://localhost:4200
```

### Local Development Ports

| Service             |         Port |
| ------------------- | -----------: |
| Angular             |         4200 |
| FastAPI             |         8000 |
| Pipecat WebRTC      |         7860 |
| Supabase PostgreSQL | Cloud hosted |

---

# Development Roadmap

The project is divided into six major development phases.

## Phase 1: Core Voice Assistant

<sub>STATUS: COMPLETED</sub>

**Objective:** Build a working browser-based real-time AI voice assistant.

Implemented:

- Angular 22 frontend.
- Tailwind CSS integration.
- FastAPI backend.
- Pipecat real-time voice pipeline.
- SmallWebRTC browser communication.
- Groq Whisper speech recognition.
- Groq LLM response generation.
- Kokoro local text-to-speech.
- Silero voice activity detection.
- Real-time audio streaming.
- Meeting creation and management APIs.
- Transcript storage.
- Supabase PostgreSQL integration.
- Assistant transcript duplication fix.

**Expected outcome:** Users can speak to the assistant through their browser and receive spoken AI responses while maintaining meeting transcripts.

## Phase 2: Meeting Intelligence and AI Insights

<sub>STATUS: NEXT PHASE</sub>

**Objective:** Transform conversation transcripts into meaningful meeting information.

Planned features:

### Automatic Meeting Summary

Generate a concise summary of the complete meeting.

### Key Discussion Points

Extract important topics, questions, and observations.

### Action Item Extraction

Identify tasks, assigned participants, and deadlines when explicitly mentioned.

### Decision Tracking

Extract decisions, agreements, and important conclusions.

### Structured AI Output

Use validated structured JSON responses rather than saving unstructured model output.

### Database Persistence

Store generated insights in the existing `MeetingInsight` model.

### Frontend Integration

Display summaries, discussion points, action items, and decisions on the meeting details page.

**Expected outcome:** Every completed meeting can have an automatically generated, organized meeting report.

## Phase 3: Advanced Meeting Management

<sub>STATUS: PLANNED</sub>

**Objective:** Build a complete meeting management experience.

Planned features:

- Meeting history dashboard.
- Search meetings by title and content.
- Filter by date and meeting status.
- Meeting detail pages.
- Edit meeting titles.
- Delete meetings with appropriate confirmation.
- Transcript browsing.
- Copy transcript.
- Export meeting summaries.
- Download meeting reports.
- Pagination for large meeting histories.

**Expected outcome:** Users can efficiently organize, retrieve, and manage their meetings.

## Phase 4: Authentication and User Management

<sub>STATUS: PLANNED</sub>

**Objective:** Introduce secure user accounts and personalized meeting experiences.

Planned features:

- User registration.
- Login and logout.
- Authentication and session management.
- Protected routes.
- User-specific meetings.
- User-specific transcripts and insights.
- Account settings.
- User preferences.
- Database access policies.
- Supabase Row Level Security (RLS).

**Expected outcome:** Each user can securely manage their own meetings and personal information.

## Phase 5: Advanced AI Capabilities

<sub>STATUS: PLANNED</sub>

**Objective:** Introduce advanced AI functionality to improve meeting productivity.

Planned features:

### Ask Questions About Meetings

Allow users to ask questions about previous meetings.

Example:

- What did we decide about the project deadline?
- What tasks were assigned to me?
- What were the important points from yesterday's meeting?

### Semantic Meeting Search

Search across meeting transcripts using natural language rather than only exact keywords.

### Retrieval-Augmented Generation (RAG)

Use embeddings and retrieval to provide answers grounded in saved meeting transcripts.

### Follow-Up Generation

Generate follow-up emails and task descriptions based on meeting discussions.

### Speaker Identification

Introduce speaker diarization to distinguish different speakers where supported by the audio pipeline.

### Integrations

Explore integrations with:

- Google Calendar.
- Gmail.
- Project management tools.
- External meeting platforms.

**Expected outcome:** Users can interact with their meeting history as an intelligent knowledge base.

## Phase 6: Production Deployment and Optimization

<sub>STATUS: PLANNED</sub>

**Objective:** Prepare the application for real-world production use.

Planned features:

- Production frontend deployment.
- Cloud deployment of FastAPI.
- Deployment of the Pipecat WebRTC service.
- Secure environment configuration.
- HTTPS and secure WebRTC connectivity.
- TURN/STUN configuration where required.
- API authentication and authorization.
- Rate limiting.
- Logging and monitoring.
- Error tracking.
- Database backup strategy.
- Performance optimization.
- Automated testing.
- CI/CD pipeline.
- Production security review.

**Expected outcome:** A secure, scalable, and reliable AI Meeting Assistant available to users online.

---

## Database Design

The application uses Supabase PostgreSQL as its persistent database.

### Meeting

Stores meeting metadata.

Potential fields:

- `id`
- `title`
- `started_at`
- `ended_at`
- `status`
- `summary`

### Transcript

Stores conversation messages.

Potential fields:

- `id`
- `meeting_id`
- `speaker`
- `text`
- `timestamp`

Relationship:

- One meeting can contain multiple transcript records.

### MeetingInsight

Stores AI-generated meeting intelligence.

Potential fields:

- `id`
- `meeting_id`
- `summary`
- `key_points`
- `action_items`
- `decisions`
- `created_at`
- `updated_at`

Relationship:

- One meeting has one associated insight record.

### Future Tables

Depending on future requirements, additional tables may include:

- `users`
- `meeting_participants`
- `meeting_embeddings`
- `user_preferences`
- `integrations`

Database schema changes should be managed through migrations as the application evolves.

---

## Future Enhancements

The following ideas may be explored after the six primary development phases:

- Meeting recording and playback.
- File and document attachments.
- Multi-language speech recognition.
- Multi-language text-to-speech.
- Calendar-based meeting scheduling.
- Real-time collaborative meeting notes.
- Custom AI assistant personalities.
- Meeting analytics and productivity reports.
- Automatic task synchronization.
- Mobile application.
- Subscription and billing functionality.

---

## Contributing

Contributions, suggestions, and feedback are welcome.

To contribute:

1. Fork the repository.
2. Create a feature branch.
3. Implement your changes.
4. Test the functionality.
5. Submit a pull request with a clear description.

---

## License

Choose and add an appropriate open-source license before publishing the project publicly.

---

## Project Vision

The vision is to build more than a simple voice chatbot.

The AI Meeting Assistant aims to become an intelligent meeting productivity platform that helps people capture conversations, understand discussions, remember decisions, organize tasks, and retrieve important information without manually managing every meeting note.

**From real-time voice conversations to intelligent meeting insights — one unified AI-powered platform.**

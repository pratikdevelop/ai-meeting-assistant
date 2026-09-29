from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.db.models import Meeting, Transcript


router = APIRouter(
    prefix="/api/meetings",
    tags=["meetings"],
)


@router.get("")
def list_meetings(
    db: Session = Depends(get_db),
):
    meetings = (
        db.query(Meeting)
        .order_by(Meeting.started_at.desc())
        .all()
    )

    return [
        {
            "id": meeting.id,
            "title": meeting.title,
            "startedAt": meeting.started_at,
            "endedAt": meeting.ended_at,
            "summary": meeting.summary,
            "status": meeting.status,
        }
        for meeting in meetings
    ]


@router.post("")
def create_meeting(
    title: str = "New Meeting",
    db: Session = Depends(get_db),
):
    meeting = Meeting(
        id=str(uuid4()),
        title=title,
        started_at=datetime.utcnow(),
        status="active",
    )

    db.add(meeting)
    db.commit()
    db.refresh(meeting)

    return {
        "id": meeting.id,
        "title": meeting.title,
        "startedAt": meeting.started_at,
        "status": meeting.status,
    }


@router.post("/{meeting_id}/end")
def end_meeting(
    meeting_id: str,
    db: Session = Depends(get_db),
):
    meeting = (
        db.query(Meeting)
        .filter(Meeting.id == meeting_id)
        .first()
    )

    if not meeting:
        return {
            "error": "Meeting not found"
        }

    meeting.ended_at = datetime.utcnow()
    meeting.status = "completed"

    db.commit()
    db.refresh(meeting)

    return {
        "id": meeting.id,
        "status": meeting.status,
        "endedAt": meeting.ended_at,
    }


@router.post("/{meeting_id}/transcript")
def save_transcript(
    meeting_id: str,
    messages: list[dict],
    db: Session = Depends(get_db),
):
    meeting = (
        db.query(Meeting)
        .filter(Meeting.id == meeting_id)
        .first()
    )

    if not meeting:
        return {
            "error": "Meeting not found"
        }

    saved = []

    for message in messages:

        text = str(
            message.get("text", "")
        ).strip()

        speaker = message.get(
            "role",
            "",
        )

        if not text:
            continue

        if speaker not in (
            "user",
            "assistant",
        ):
            continue

        transcript = Transcript(
            id=str(uuid4()),
            meeting_id=meeting_id,
            speaker=speaker,
            text=text,
            timestamp=datetime.utcnow(),
        )

        db.add(transcript)

        saved.append({
            "id": transcript.id,
            "speaker": transcript.speaker,
            "text": transcript.text,
        })

    db.commit()

    return {
        "meetingId": meeting_id,
        "count": len(saved),
        "transcript": saved,
    }



@router.get("/{meeting_id}/transcript")
def get_transcript(
    meeting_id: str,
    db: Session = Depends(get_db),
):
    transcripts = (
        db.query(Transcript)
        .filter(
            Transcript.meeting_id == meeting_id
        )
        .order_by(
            Transcript.timestamp.asc()
        )
        .all()
    )

    return [
        {
            "id": item.id,
            "speaker": item.speaker,
            "text": item.text,
            "timestamp": item.timestamp,
        }
        for item in transcripts
    ]

@router.get("/{meeting_id}")
def get_meeting(
    meeting_id: str,
    db: Session = Depends(get_db),
):
    meeting = (
        db.query(Meeting)
        .filter(
            Meeting.id == meeting_id
        )
        .first()
    )

    if not meeting:
        return {
            "error": "Meeting not found"
        }

    return {
        "id": meeting.id,
        "title": meeting.title,
        "startedAt": meeting.started_at,
        "endedAt": meeting.ended_at,
        "summary": meeting.summary,
        "status": meeting.status,
    }
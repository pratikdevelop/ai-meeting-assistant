import { Service } from '@angular/core';
import { MeetingData } from '../../services/meeting';

export interface Meeting {
  id: string;
  title: string;
  startedAt: string;
  endedAt?: string;
  summary?: string;
  status: string;
}

@Service()
export class Api {

  private readonly baseUrl =
    'http://localhost:8000';


  async getMeetings(): Promise<Meeting[]> {

    const response = await fetch(
      `${this.baseUrl}/api/meetings`,
    );

    if (!response.ok) {
      throw new Error(
        'Failed to load meetings',
      );
    }

    return response.json();
  }


  async createMeeting(
    title: string,
  ): Promise<Meeting> {

    const response = await fetch(
      `${this.baseUrl}/api/meetings?title=${encodeURIComponent(title)}`,
      {
        method: 'POST',
      },
    );

    if (!response.ok) {
      throw new Error(
        'Failed to create meeting',
      );
    }

    return response.json();
  }


  async endMeeting(
    meetingId: string,
  ): Promise<Meeting> {

    const response = await fetch(
      `${this.baseUrl}/api/meetings/${meetingId}/end`,
      {
        method: 'POST',
      },
    );

    if (!response.ok) {
      throw new Error(
        'Failed to end meeting',
      );
    }

    return response.json();
  }

  async saveTranscript(
  meetingId: string,
  messages: Array<{
    role: 'user' | 'assistant';
    text: string;
  }>,
): Promise<void> {

  const response = await fetch(
    `${this.baseUrl}/api/meetings/${meetingId}/transcript`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(messages),
    },
  );

  if (!response.ok) {
    throw new Error(
      `Failed to save transcript: HTTP ${response.status}`,
    );
  }
}
async getTranscript(
  meetingId: string,
): Promise<
  Array<{
    id: string;
    speaker: 'user' | 'assistant';
    text: string;
    timestamp: string;
  }>
> {

  const response = await fetch(
    `${this.baseUrl}/api/meetings/${meetingId}/transcript`,
  );

  if (!response.ok) {
    throw new Error(
      `Failed to load transcript: HTTP ${response.status}`,
    );
  }

  return response.json();
}
async getMeeting(
  meetingId: string,
): Promise<MeetingData> {

  const response =
    await fetch(
      `${this.baseUrl}/api/meetings/${meetingId}`,
    );

  if (!response.ok) {

    throw new Error(
      `Failed to load meeting: HTTP ${response.status}`,
    );
  }

  return response.json();
}
}
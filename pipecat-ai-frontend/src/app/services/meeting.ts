import {
  Service,
  signal,
} from '@angular/core';


export interface MeetingData {
  id: string;
  title: string;
  startedAt: string;
  endedAt: string | null;
  summary: string | null;
  status: 'active' | 'completed';
}


@Service()
export class Meeting {

  private readonly apiUrl =
    'http://localhost:8000/api/meetings';


  readonly meetings =
    signal<MeetingData[]>([]);

  readonly loading =
    signal(false);

  readonly error =
    signal<string | null>(null);


  async load(): Promise<void> {

    this.loading.set(true);
    this.error.set(null);

    try {

      const response =
        await fetch(this.apiUrl);

      if (!response.ok) {
        throw new Error(
          `HTTP ${response.status}`,
        );
      }

      const data: MeetingData[] =
        await response.json();

      this.meetings.set(data);

    } catch (error) {

      console.error(
        'Failed to load meetings:',
        error,
      );

      this.error.set(
        'Failed to load meetings.',
      );

    } finally {

      this.loading.set(false);
    }
  }


  async create(
    title: string,
  ): Promise<MeetingData> {

    const response =
      await fetch(
        `${this.apiUrl}?title=${encodeURIComponent(title)}`,
        {
          method: 'POST',
        },
      );

    if (!response.ok) {
      throw new Error(
        `Failed to create meeting: HTTP ${response.status}`,
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

    const response =
      await fetch(
        `${this.apiUrl}/${meetingId}/transcript`,
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

    const response =
      await fetch(
        `${this.apiUrl}/${meetingId}/transcript`,
      );

    if (!response.ok) {
      throw new Error(
        `Failed to load transcript: HTTP ${response.status}`,
      );
    }

    return response.json();
  }


  async end(
    meetingId: string,
  ): Promise<MeetingData> {

    const response =
      await fetch(
        `${this.apiUrl}/${meetingId}/end`,
        {
          method: 'POST',
        },
      );

    if (!response.ok) {
      throw new Error(
        `Failed to end meeting: HTTP ${response.status}`,
      );
    }

    return response.json();
  }
}
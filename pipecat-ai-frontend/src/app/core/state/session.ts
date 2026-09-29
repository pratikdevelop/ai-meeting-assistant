import {
  Service,
  inject,
  signal,
} from '@angular/core';

import {
  Api,
  Meeting,
} from '../api/api';

@Service()
export class Session {
  private readonly api = inject(Api);

  readonly currentMeeting =
    signal<Meeting | null>(null);

  readonly meetings =
    signal<Meeting[]>([]);

  readonly isMeetingActive =
    signal(false);

  async startMeeting(
    title = 'AI Voice Meeting',
  ): Promise<Meeting> {
    const meeting =
      await this.api.createMeeting(title);

    this.currentMeeting.set(meeting);
    this.isMeetingActive.set(true);

    return meeting;
  }

  async endMeeting(): Promise<void> {
    const meeting =
      this.currentMeeting();

    if (!meeting) {
      return;
    }

    const completed =
      await this.api.endMeeting(meeting.id);

    this.currentMeeting.set(null);
    this.isMeetingActive.set(false);

    this.meetings.update(
      (meetings) => [
        completed,
        ...meetings,
      ],
    );
  }

  clearSession(): void {
    this.currentMeeting.set(null);
    this.isMeetingActive.set(false);
  }


  async saveTranscript(
  messages: Array<{
    role: 'user' | 'assistant';
    text: string;
  }>,
): Promise<void> {

  const meeting =
    this.currentMeeting();

  if (!meeting) {
    return;
  }

  await this.api.saveTranscript(
    meeting.id,
    messages,
  );
}
}
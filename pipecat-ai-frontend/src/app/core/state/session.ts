import {
  Service,
  computed,
  signal,
} from '@angular/core';


export interface MeetingSession {
  id: string;
  title: string;
  startedAt: Date;
}


@Service()
export class Session {

  readonly currentMeeting =
    signal<MeetingSession | null>(null);

  readonly meetings =
    signal<MeetingSession[]>([]);

  readonly isMeetingActive =
    computed(
      () => this.currentMeeting() !== null,
    );


  startMeeting(
    title = 'New Meeting',
  ): void {

    const meeting: MeetingSession = {
      id: crypto.randomUUID(),
      title,
      startedAt: new Date(),
    };

    this.currentMeeting.set(meeting);

    this.meetings.update(
      (meetings) => [
        meeting,
        ...meetings,
      ],
    );
  }


  endMeeting(): void {
    this.currentMeeting.set(null);
  }


  getMeeting(
    id: string,
  ): MeetingSession | undefined {

    return this.meetings().find(
      (meeting) => meeting.id === id,
    );
  }
}
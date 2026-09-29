import {
  Component,
  computed,
  inject,
  signal,
} from '@angular/core';

import {
  ActivatedRoute,
  RouterLink,
} from '@angular/router';

import {
  Api,
  } from '../../core/api/api';
import { MeetingData } from '../../services/meeting';


interface TranscriptItem {
  id: string;
  speaker: 'user' | 'assistant';
  text: string;
  timestamp: string;
}


@Component({
  selector: 'app-meeting-details',
  imports: [RouterLink],
  templateUrl: './meeting-details.html',
})
export class MeetingDetails {

  private readonly route =
    inject(ActivatedRoute);

  private readonly api =
    inject(Api);


  // ==========================================
  // State
  // ==========================================

  readonly meeting =
    signal<MeetingData | null>(null);

  readonly transcript =
    signal<TranscriptItem[]>([]);

  readonly loading =
    signal(true);

  readonly error =
    signal<string | null>(null);

  readonly meetingId =
    this.route.snapshot.paramMap.get('id');


  // ==========================================
  // Computed values
  // ==========================================

  readonly totalMessages =
    computed(
      () => this.transcript().length,
    );

  readonly userMessages =
    computed(
      () =>
        this.transcript().filter(
          (item) =>
            item.speaker === 'user',
        ).length,
    );

  readonly assistantMessages =
    computed(
      () =>
        this.transcript().filter(
          (item) =>
            item.speaker === 'assistant',
        ).length,
    );


  constructor() {

    if (!this.meetingId) {

      this.loading.set(false);

      this.error.set(
        'Meeting ID is missing.',
      );

      return;
    }

    void this.loadMeeting(
      this.meetingId,
    );
  }


  // ==========================================
  // Load meeting + transcript
  // ==========================================

  async loadMeeting(
    meetingId: string,
  ): Promise<void> {

    this.loading.set(true);
    this.error.set(null);

    try {

      const [
        meeting,
        transcript,
      ] = await Promise.all([
        this.api.getMeeting(
          meetingId,
        ),
        this.api.getTranscript(
          meetingId,
        ),
      ]);

      this.meeting.set(meeting);
      this.transcript.set(transcript);

    } catch (error) {

      console.error(
        'Failed to load meeting:',
        error,
      );

      this.error.set(
        'Unable to load meeting details.',
      );

    } finally {

      this.loading.set(false);
    }
  }


  // ==========================================
  // Meeting title
  // ==========================================

  meetingTitle(): string {

    return (
      this.meeting()?.title ??
      'AI Voice Meeting'
    );
  }


  // ==========================================
  // Meeting date
  // ==========================================

  formatDate(): string {

    const startedAt =
      this.meeting()?.startedAt;

    if (!startedAt) {
      return '--';
    }

    const date =
      new Date(startedAt);

    if (
      Number.isNaN(
        date.getTime(),
      )
    ) {
      return '--';
    }

    return date.toLocaleDateString(
      'en-US',
      {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
      },
    );
  }


  // ==========================================
  // Transcript timestamp
  // ==========================================

  formatTimestamp(
    timestamp: string,
  ): string {

    if (!timestamp) {
      return '--:--';
    }

    const date =
      new Date(timestamp);

    if (
      Number.isNaN(
        date.getTime(),
      )
    ) {
      return timestamp;
    }

    return date.toLocaleTimeString(
      'en-US',
      {
        hour: 'numeric',
        minute: '2-digit',
      },
    );
  }


  // ==========================================
  // Retry
  // ==========================================

  retry(): void {

    if (!this.meetingId) {
      return;
    }

    void this.loadMeeting(
      this.meetingId,
    );
  }


  // ==========================================
  // Copy message
  // ==========================================

  async copyMessage(
    text: string,
  ): Promise<void> {

    try {

      await navigator.clipboard.writeText(
        text,
      );

      console.log(
        '✅ Message copied to clipboard',
      );

    } catch (error) {

      console.error(
        '❌ Failed to copy:',
        error,
      );
    }
  }


  // ==========================================
  // Share message
  // ==========================================

  async shareMessage(
    item: TranscriptItem,
  ): Promise<void> {

    const speaker =
      item.speaker === 'user'
        ? 'You'
        : 'AI Assistant';

    const text =
      `${speaker}: ${item.text}`;

    try {

      if (
        typeof navigator.share ===
        'function'
      ) {

        await navigator.share({
          title: 'AI Meeting Transcript',
          text,
        });

      } else {

        await this.copyMessage(text);
      }

    } catch (error) {

      if (
        error instanceof DOMException &&
        error.name === 'AbortError'
      ) {
        return;
      }

      console.error(
        '❌ Share failed:',
        error,
      );
    }
  }


  // ==========================================
  // Export transcript
  // ==========================================

  exportTranscript(): void {

    const transcript =
      this.transcript();

    if (!transcript.length) {
      return;
    }

    const content =
      transcript
        .map((item) => {

          const speaker =
            item.speaker === 'user'
              ? 'You'
              : 'AI Assistant';

          const timestamp =
            this.formatTimestamp(
              item.timestamp,
            );

          return `[${timestamp}] ${speaker}:\n${item.text}\n`;

        })
        .join('\n---\n\n');


    const blob =
      new Blob(
        [content],
        {
          type:
            'text/plain;charset=utf-8',
        },
      );

    const url =
      URL.createObjectURL(blob);

    const anchor =
      document.createElement('a');

    anchor.href = url;

    anchor.download =
      `transcript-${
        this.meetingId ??
        'meeting'
      }.txt`;

    document.body.appendChild(anchor);

    anchor.click();

    document.body.removeChild(anchor);

    URL.revokeObjectURL(url);
  }


  // ==========================================
  // Copy all transcript
  // ==========================================

  async copyAllTranscript(): Promise<void> {

    const content =
      this.transcript()
        .map((item) => {

          const speaker =
            item.speaker === 'user'
              ? 'You'
              : 'AI Assistant';

          return `[${speaker}] ${item.text}`;
        })
        .join('\n\n');

    if (!content.trim()) {
      return;
    }

    await this.copyMessage(content);
  }
}
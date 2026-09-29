import {
  Component,
  inject,
  signal,
  effect,
  OnDestroy,
} from '@angular/core';

import { Pipecat } from '../../core/pipecat';
import { Session } from '../../core/state/session';
import { Transcript } from '../transcript/transcript';

@Component({
  selector: 'app-voice',
  imports: [Transcript],
  templateUrl: './voice.html',
})
export class Voice implements OnDestroy {
  readonly pipecat = inject(Pipecat);
  readonly session = inject(Session);
  
  // ✅ Signal for reactive current time
  currentTime = signal<string>(new Date().toLocaleTimeString([], { 
    hour: '2-digit', 
    minute: '2-digit' 
  }));
  
  private timeInterval: any;

  constructor() {
    // Update time every 30 seconds
    this.timeInterval = setInterval(() => {
      this.currentTime.set(new Date().toLocaleTimeString([], { 
        hour: '2-digit', 
        minute: '2-digit' 
      }));
    }, 30000);
  }

  ngOnDestroy(): void {
    if (this.timeInterval) {
      clearInterval(this.timeInterval);
    }
  }

  async startConversation(): Promise<void> {
    try {
      const meeting = await this.session.startMeeting(
        'AI Voice Meeting',
      );

      console.log('✅ Meeting created:', meeting);

      await this.pipecat.connect();

      console.log('✅ Pipecat connected');
    } catch (error) {
      console.error(
        '❌ Failed to start conversation:',
        error,
      );

      this.session.clearSession();

      try {
        await this.pipecat.disconnect();
      } catch {
        // Ignore disconnect errors during startup failure.
      }
    }
  }

  async endConversation(): Promise<void> {
    try {
      const messages = this.pipecat.messages();

      const transcript = messages.map((message) => ({
        role: message.role,
        text: message.text,
      }));

      await this.session.saveTranscript(transcript);

      console.log('✅ Transcript saved');

      await this.pipecat.disconnect();

      await this.session.endMeeting();

      console.log('✅ Meeting ended');
    } catch (error) {
      console.error(
        '❌ Failed to end conversation:',
        error,
      );
    }
  }

  async toggleMicrophone(): Promise<void> {
    try {
      await this.pipecat.toggleMicrophone();
    } catch (error) {
      console.error(
        '❌ Microphone error:',
        error,
      );
    }
  }

  clearConversation(): void {
    this.pipecat.clearMessages();
  }

  isConnected(): boolean {
    const state = this.pipecat.connectionState();

    return (
      state === 'connected' ||
      state === 'ready'
    );
  }

  statusLabel(): string {
    switch (this.pipecat.connectionState()) {
      case 'connecting':
        return 'Connecting...';

      case 'connected':
        return 'Connected';

      case 'ready':
        return 'Ready';

      case 'disconnecting':
        return 'Disconnecting...';

      case 'error':
        return 'Connection Error';

      default:
        return 'Disconnected';
    }
  }
}
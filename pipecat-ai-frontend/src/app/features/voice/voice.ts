import {
  Component,
  inject,
} from '@angular/core';

import { Pipecat } from '../../core/pipecat';
import { Session } from '../../core/state/session';
import { Transcript } from '../transcript/transcript';


@Component({
  selector: 'app-voice',
  imports: [Transcript],
  templateUrl: './voice.html',
})
export class Voice {

  readonly pipecat = inject(Pipecat);
  readonly session = inject(Session);


  async startConversation(): Promise<void> {

    try {

      await this.pipecat.connect();

      this.session.startMeeting(
        'AI Voice Session',
      );

    } catch (error) {

      console.error(
        'Failed to start conversation:',
        error,
      );

    }
  }


  async endConversation(): Promise<void> {

    await this.pipecat.disconnect();

    this.session.endMeeting();
  }


  async toggleMicrophone(): Promise<void> {

    try {
      await this.pipecat.toggleMicrophone();
    } catch (error) {
      console.error(
        'Failed to toggle microphone:',
        error,
      );
    }
  }


  clearConversation(): void {
    this.pipecat.clearMessages();
  }


  isConnected(): boolean {

    const state =
      this.pipecat.connectionState();

    return (
      state === 'connected' ||
      state === 'ready'
    );
  }


  statusLabel(): string {

    switch (
      this.pipecat.connectionState()
    ) {

      case 'connecting':
        return 'Connecting...';

      case 'connected':
        return 'Connected';

      case 'ready':
        return 'Ready';

      case 'disconnecting':
        return 'Disconnecting...';

      case 'error':
        return 'Connection error';

      default:
        return 'Disconnected';
    }
  }
}
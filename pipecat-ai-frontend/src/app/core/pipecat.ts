import { Service, signal } from '@angular/core';

import {
  PipecatClient,
  type TransportState,
} from '@pipecat-ai/client-js';

import { SmallWebRTCTransport } from '@pipecat-ai/small-webrtc-transport';


export type ConnectionState =
  | 'disconnected'
  | 'connecting'
  | 'connected'
  | 'ready'
  | 'disconnecting'
  | 'error';


export interface TranscriptMessage {
  id: string;
  role: 'user' | 'assistant';
  text: string;
  final: boolean;
  timestamp: Date;
}


@Service()
export class Pipecat {

  // ==========================================
  // UI State
  // ==========================================

  readonly connectionState =
    signal<ConnectionState>('disconnected');

  readonly isListening =
    signal(false);

  readonly isSpeaking =
    signal(false);

  readonly isMicEnabled =
    signal(true);

  readonly error =
    signal<string | null>(null);

  readonly messages =
    signal<TranscriptMessage[]>([]);


  // ==========================================
  // Pipecat Client
  // ==========================================

  private readonly client: PipecatClient;


  constructor() {
    this.client = new PipecatClient({
      transport: new SmallWebRTCTransport(),

      enableMic: true,
      enableCam: false,

      callbacks: {

        // --------------------------------------
        // Connection
        // --------------------------------------

        onConnected: () => {
          console.log('✅ Pipecat connected');

          this.connectionState.set('connected');
        },

        onDisconnected: () => {
          console.log('🔌 Pipecat disconnected');

          this.connectionState.set('disconnected');
          this.isListening.set(false);
          this.isSpeaking.set(false);
        },

        onTransportStateChanged: (
          state: TransportState,
        ) => {
          console.log(
            '🔄 Transport state:',
            state,
          );

          this.connectionState.set(
            this.mapTransportState(state),
          );
        },

        onBotConnected: () => {
          console.log('🤖 Bot connected');
        },

        onBotReady: () => {
          console.log('🤖 Bot ready');

          this.connectionState.set('ready');
        },

        onBotDisconnected: () => {
          console.log('🤖 Bot disconnected');
        },


        // --------------------------------------
        // User Voice Activity
        // --------------------------------------

        onUserStartedSpeaking: () => {
          console.log(
            '🎤 User started speaking',
          );

          this.isListening.set(true);
        },

        onUserStoppedSpeaking: () => {
          console.log(
            '🛑 User stopped speaking',
          );

          this.isListening.set(false);
        },


        // --------------------------------------
        // User Transcript
        // --------------------------------------

        onUserTranscript: (data) => {
          console.log(
            '👤 User transcript:',
            data.text,
            'final:',
            data.final,
          );

          if (!data.text?.trim()) {
            return;
          }

          this.updateUserTranscript(
            data.text,
            data.final,
          );
        },


        // --------------------------------------
        // Bot Output
        // --------------------------------------

        onBotOutput: (data) => {
          console.log(
            '🤖 Bot output:',
            data.text,
          );

          if (!data.text?.trim()) {
            return;
          }

          this.addAssistantMessage(
            data.text,
          );
        },


        // --------------------------------------
        // Bot Speaking
        // --------------------------------------

        onBotStartedSpeaking: () => {
          console.log(
            '🔊 Bot started speaking',
          );

          this.isSpeaking.set(true);
        },

        onBotStoppedSpeaking: () => {
          console.log(
            '🔇 Bot stopped speaking',
          );

          this.isSpeaking.set(false);
        },


        // --------------------------------------
        // Errors
        // --------------------------------------

        onError: (data) => {
          console.error(
            '❌ Pipecat error:',
            data,
          );

          this.error.set(
            'Pipecat reported an error.',
          );

          this.connectionState.set('error');
        },

        onDeviceError: (error) => {
          console.error(
            '🎤 Device error:',
            error,
          );

          this.error.set(
            'Unable to access your microphone.',
          );
        },
      },
    });
  }


  // ==========================================
  // Connect
  // ==========================================

  async connect(): Promise<void> {

    this.error.set(null);

    this.connectionState.set(
      'connecting',
    );

    try {

      await this.client.connect({
        webrtcUrl:
          'http://localhost:7860/api/offer',
      });

      console.log(
        '✅ Connected to Pipecat bot',
      );

    } catch (error) {

      console.error(
        '❌ Failed to connect to Pipecat:',
        error,
      );

      this.error.set(
        'Could not connect to the voice assistant.',
      );

      this.connectionState.set(
        'error',
      );

      throw error;
    }
  }


  // ==========================================
  // Disconnect
  // ==========================================

  async disconnect(): Promise<void> {

    try {

      await this.client.disconnect();

    } catch (error) {

      console.error(
        '❌ Error during disconnect:',
        error,
      );

    } finally {

      this.connectionState.set(
        'disconnected',
      );

      this.isListening.set(false);
      this.isSpeaking.set(false);
    }
  }


  // ==========================================
  // Microphone
  // ==========================================

  async enableMicrophone(): Promise<void> {

    await this.client.enableMic(true);

    this.isMicEnabled.set(true);
  }


  async disableMicrophone(): Promise<void> {

    await this.client.enableMic(false);

    this.isMicEnabled.set(false);
    this.isListening.set(false);
  }


  async toggleMicrophone(): Promise<void> {

    const enabled = this.isMicEnabled();

    if (enabled) {
      await this.disableMicrophone();
    } else {
      await this.enableMicrophone();
    }
  }


  // ==========================================
  // Transcript
  // ==========================================

  clearMessages(): void {
    this.messages.set([]);
  }


  // ==========================================
  // Internal State Helpers
  // ==========================================

  private mapTransportState(
    state: TransportState,
  ): ConnectionState {

    switch (state) {

      case 'connecting':
        return 'connecting';

      case 'connected':
        return 'connected';

      case 'ready':
        return 'ready';

      case 'disconnecting':
        return 'disconnecting';

      case 'disconnected':
        return 'disconnected';

      default:
        return 'error';
    }
  }


  private updateUserTranscript(
    text: string,
    final: boolean,
  ): void {

    const cleanedText = text.trim();

    if (!cleanedText) {
      return;
    }

    this.messages.update(
      (messages) => {

        const last = messages.at(-1);

        // Update the latest user message when the
        // transcript is still partial.
        if (
          last?.role === 'user' &&
          !last.final
        ) {

          const updated = [
            ...messages,
          ];

          updated[updated.length - 1] = {
            ...last,
            text: cleanedText,
            final,
            timestamp: new Date(),
          };

          return updated;
        }

        return [
          ...messages,
          {
            id: crypto.randomUUID(),
            role: 'user',
            text: cleanedText,
            final,
            timestamp: new Date(),
          },
        ];
      },
    );
  }


  private addAssistantMessage(
    text: string,
  ): void {

    const cleanedText = text.trim();

    if (!cleanedText) {
      return;
    }

    this.messages.update(
      (messages) => {

        const last = messages.at(-1);

        // Bot output can arrive in multiple logical chunks.
        // Append to an active assistant message.
        if (
          last?.role === 'assistant'
        ) {

          const updated = [
            ...messages,
          ];

          updated[updated.length - 1] = {
            ...last,
            text: `${last.text}${cleanedText}`,
            timestamp: new Date(),
          };

          return updated;
        }

        return [
          ...messages,
          {
            id: crypto.randomUUID(),
            role: 'assistant',
            text: cleanedText,
            final: true,
            timestamp: new Date(),
          },
        ];
      },
    );
  }
}
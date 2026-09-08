import { Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';

import { Pipecat } from '../../core/pipecat';
import { Session } from '../../core/state/session';


@Component({
  selector: 'app-dashboard',
  imports: [RouterLink],
  templateUrl: './dashboard.html',
})
export class Dashboard {

  readonly pipecat = inject(Pipecat);
  readonly session = inject(Session);

  async startAssistant(): Promise<void> {
    await this.pipecat.connect();
  }
}
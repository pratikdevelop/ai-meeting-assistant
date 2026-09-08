import { Component, inject } from '@angular/core';

import { Pipecat } from '../../core/pipecat';


@Component({
  selector: 'app-transcript',
  templateUrl: './transcript.html',
})
export class Transcript {

  readonly pipecat = inject(Pipecat);
}
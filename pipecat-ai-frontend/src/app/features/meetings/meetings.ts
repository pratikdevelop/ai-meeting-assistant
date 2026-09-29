import {
  Component,
  inject,
} from '@angular/core';

import {
  RouterLink,
} from '@angular/router';

import {
  Meeting,
} from '../../services/meeting';


@Component({
  selector: 'app-meetings',

  imports: [
    RouterLink,
  ],

  templateUrl: './meetings.html',
})
export class Meetings {

  readonly meeting =
    inject(Meeting);


  constructor() {
    void this.loadMeetings();
  }


  private async loadMeetings(): Promise<void> {

    await this.meeting.load();

  }
}
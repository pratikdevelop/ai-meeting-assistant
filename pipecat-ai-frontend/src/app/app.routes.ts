import { Routes } from '@angular/router';

export const routes: Routes = [

  {
    path: '',
    redirectTo: 'dashboard',
    pathMatch: 'full',
  },

  {
    path: 'dashboard',
    loadComponent: () =>
      import('./features/dashboard/dashboard')
        .then((m) => m.Dashboard),
  },

  {
    path: 'voice',
    loadComponent: () =>
      import('./features/voice/voice')
        .then((m) => m.Voice),
  },

  {
    path: 'meetings',
    loadComponent: () =>
      import('./features/meetings/meetings')
        .then((m) => m.Meetings),
  },
  {
  path: 'meetings/:id',
  loadComponent: () =>
    import('./features/meeting-details/meeting-details')
      .then((m) => m.MeetingDetails),
},

  {
    path: 'settings',
    loadComponent: () =>
      import('./features/settings/settings')
        .then((m) => m.Settings),
  },

  {
    path: '**',
    redirectTo: 'dashboard',
  },
];
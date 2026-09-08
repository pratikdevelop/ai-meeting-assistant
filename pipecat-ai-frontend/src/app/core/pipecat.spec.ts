import { TestBed } from '@angular/core/testing';
import { Pipecat } from './pipecat';

describe('Pipecat', () => {
  let service: Pipecat;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Pipecat);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

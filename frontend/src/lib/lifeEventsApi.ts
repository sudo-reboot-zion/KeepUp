/**
 * Life Events API Client
 */
import { apiRequest } from './api';

export interface LifeEvent {
  id: number;
  event_type: string;
  description: string;
  impact_level: string;
  start_date?: string;
  created_at: string;
}

export interface LifeEventCreate {
  event_type: string;
  description: string;
  impact_level: string;
}

export async function createLifeEvent(event: LifeEventCreate): Promise<LifeEvent> {
  return apiRequest<LifeEvent>('/life-events', {
    method: 'POST',
    body: JSON.stringify(event)
  });
}

export async function getLifeEvents(): Promise<LifeEvent[]> {
  return apiRequest<LifeEvent[]>('/life-events');
}

export async function getActiveLifeEvents(): Promise<{ active_events: LifeEvent[] }> {
  return apiRequest('/life-events/active');
}


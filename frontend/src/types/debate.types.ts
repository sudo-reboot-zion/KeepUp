import { ReactElement } from 'react';

// ============================================================================
// DEBATE TYPES
// ============================================================================

/**
 * Type of message in the debate
 */
export type MessageType = 'proposal' | 'challenge' | 'synthesis';

/**
 * Individual agent message in the debate timeline
 */
export interface AgentMessage {
    id: string;
    agent: string;
    role: string;
    message: string;
    type: MessageType;
    timestamp: number;
}

/**
 * Agent styling configuration for UI display
 */
export interface AgentStyle {
    text: string;
    icon: ReactElement;
}

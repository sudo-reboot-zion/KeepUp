import { apiRequest } from './api';

export interface ChatMessage {
    message: string;
    context?: Record<string, any>;
}

export interface ChatResponse {
    message: string;
    data: Record<string, any>;
    actions: any[];
    confidence: number;
    timestamp: string;
}

/**
 * Send a message to the AI coach
 */
export async function sendChatMessage(message: string, context: Record<string, any> = {}): Promise<ChatResponse> {
    return apiRequest<ChatResponse>('/chat/send', {
        method: 'POST',
        body: JSON.stringify({
            message,
            context
        }),
    });
}

/**
 * Get conversation history
 */
export async function getChatHistory(): Promise<{ messages: any[] }> {
    return apiRequest<{ messages: any[] }>('/chat/history');
}

/**
 * Clear conversation history
 */
export async function clearChatHistory(): Promise<{ success: boolean }> {
    return apiRequest<{ success: boolean }>('/chat/history', {
        method: 'DELETE',
    });
}

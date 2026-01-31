import { apiRequest } from './api';
import type { OnboardingData, OnboardingResponse, FinalPlan, DebateSummary } from '@/types/onboarding.types';

/**
 * Start the onboarding process and trigger multi-agent debate
 */
export async function startOnboarding(data: OnboardingData): Promise<OnboardingResponse> {
    return apiRequest<OnboardingResponse>('/onboarding/start', {
        method: 'POST',
        body: JSON.stringify(data),
    });
}

/**
 * Send a single conversational step in the onboarding process
 */
export async function sendOnboardingStep(message: string, extractedData: Record<string, any> = {}): Promise<any> {
    return apiRequest<any>('/onboarding/step', {
        method: 'POST',
        body: JSON.stringify({
            message,
            extracted_data: extractedData
        }),
    });
}

// Re-export types for convenience
export type { OnboardingData, OnboardingResponse, FinalPlan, DebateSummary };

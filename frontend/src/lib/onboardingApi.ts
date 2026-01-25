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

// Re-export types for convenience
export type { OnboardingData, OnboardingResponse, FinalPlan, DebateSummary };

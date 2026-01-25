/**
 * Safety & Guardrails API Client
 * Frontend integration for Phase 3 safety endpoints
 */

import { apiRequest } from './api';
import type {
    BiometricCheckRequest,
    SafetyAlert,
    SafetyCheckResponse,
    ConfidenceCheckRequest,
    ConfidenceCheckResponse,
    OverttrainingRiskRequest,
    OverttrainingRiskResponse,
    MedicalThresholdsResponse,
    AlertAcknowledgmentRequest,
    AlertAcknowledgmentResponse,
    SafetyReportResponse,
} from '@/types/safety.types';
// ============================================================================
// BIOMETRIC SAFETY CHECKS
// ============================================================================

/**
 * Check biometric readings against medical safety thresholds
 */
export async function checkBiometricSafety(
    resolutionId: number,
    biometrics: BiometricCheckRequest
): Promise<SafetyCheckResponse> {
    return apiRequest<SafetyCheckResponse>(
        `/safety/check-biometrics/${resolutionId}`,
        {
            method: 'POST',
            body: JSON.stringify(biometrics)
        }
    );
}

/**
 * Get critical medical thresholds
 */
export async function getMedicalThresholds(): Promise<MedicalThresholdsResponse> {
    return apiRequest<MedicalThresholdsResponse>('/safety/thresholds', {
        method: 'GET'
    });
}

// ============================================================================
// CONFIDENCE VALIDATION
// ============================================================================

/**
 * Check recommendation confidence score
 */
export async function checkRecommendationConfidence(
    request: ConfidenceCheckRequest
): Promise<ConfidenceCheckResponse> {
    return apiRequest<ConfidenceCheckResponse>(
        '/safety/check-confidence',
        {
            method: 'POST',
            body: JSON.stringify(request)
        }
    );
}

// ============================================================================
// OVERTRAINING PREVENTION
// ============================================================================

/**
 * Check overtraining risk
 */
export async function checkOverttrainingRisk(
    resolutionId: number,
    request: OverttrainingRiskRequest
): Promise<OverttrainingRiskResponse> {
    return apiRequest<OverttrainingRiskResponse>(
        `/safety/check-overtraining/${resolutionId}`,
        {
            method: 'POST',
            body: JSON.stringify(request)
        }
    );
}

// ============================================================================
// ALERT MANAGEMENT
// ============================================================================

/**
 * Acknowledge a safety alert
 */
export async function acknowledgeSafetyAlert(
    request: AlertAcknowledgmentRequest
): Promise<AlertAcknowledgmentResponse> {
    return apiRequest<AlertAcknowledgmentResponse>(
        '/safety/acknowledge-alert',
        {
            method: 'POST',
            body: JSON.stringify(request)
        }
    );
}

// ============================================================================
// COMPREHENSIVE SAFETY REPORTS
// ============================================================================

/**
 * Get comprehensive safety report for resolution
 */
export async function getSafetyReport(
    resolutionId: number
): Promise<SafetyReportResponse> {
    return apiRequest<SafetyReportResponse>(
        `/safety/report/${resolutionId}`,
        {
            method: 'GET'
        }
    );
}

// ============================================================================
// EXPORT TYPES FOR COMPONENTS
// ============================================================================

export type {
    BiometricCheckRequest,
    SafetyAlert,
    SafetyCheckResponse,
    ConfidenceCheckRequest,
    ConfidenceCheckResponse,
    OverttrainingRiskRequest,
    OverttrainingRiskResponse,
    MedicalThresholdsResponse,
    AlertAcknowledgmentRequest,
    AlertAcknowledgmentResponse,
    SafetyReportResponse,
};

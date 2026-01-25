/**
 * React Hooks for Safety & Guardrails
 * Custom hooks to integrate safety checks into React components
 */

'use client';

import { useState, useCallback, useEffect } from 'react';
import {
    checkBiometricSafety,
    checkRecommendationConfidence,
    checkOverttrainingRisk,
    acknowledgeSafetyAlert,
    getMedicalThresholds,
    BiometricCheckRequest,
    ConfidenceCheckRequest,
    OverttrainingRiskRequest,
    SafetyAlert,
    MedicalThresholdsResponse,
    AlertAcknowledgmentRequest,
} from '../lib/safetyApi';

// ============================================================================
// BIOMETRIC SAFETY HOOK
// ============================================================================

interface UseBiometricSafetyReturn {
    checkBiometrics: (biometrics: BiometricCheckRequest) => Promise<void>;
    alerts: SafetyAlert[];
    isSafe: boolean;
    isLoading: boolean;
    error: string | null;
    lastChecked: string | null;
}

/**
 * Hook for checking biometric safety
 */
export function useBiometricSafety(resolutionId: number): UseBiometricSafetyReturn {
    const [alerts, setAlerts] = useState<SafetyAlert[]>([]);
    const [isSafe, setIsSafe] = useState(true);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [lastChecked, setLastChecked] = useState<string | null>(null);

    const checkBiometrics = useCallback(
        async (biometrics: BiometricCheckRequest) => {
            setIsLoading(true);
            setError(null);
            try {
                const response = await checkBiometricSafety(resolutionId, biometrics);
                setAlerts(response.alerts);
                setIsSafe(response.is_safe);
                setLastChecked(new Date().toISOString());
            } catch (err) {
                const errorMessage = err instanceof Error ? err.message : 'Failed to check biometrics';
                setError(errorMessage);
                setAlerts([]);
                setIsSafe(true);
            } finally {
                setIsLoading(false);
            }
        },
        [resolutionId]
    );

    return {
        checkBiometrics,
        alerts,
        isSafe,
        isLoading,
        error,
        lastChecked
    };
}

// ============================================================================
// CONFIDENCE CHECK HOOK
// ============================================================================

interface UseConfidenceCheckReturn {
    checkConfidence: (request: ConfidenceCheckRequest) => Promise<void>;
    isSafe: boolean;
    confidenceScore: number;
    alertLevel?: string;
    requiresDisclaimer: boolean;
    isLoading: boolean;
    error: string | null;
}

/**
 * Hook for checking recommendation confidence
 */
export function useConfidenceCheck(): UseConfidenceCheckReturn {
    const [isSafe, setIsSafe] = useState(true);
    const [confidenceScore, setConfidenceScore] = useState(0);
    const [alertLevel, setAlertLevel] = useState<string>();
    const [requiresDisclaimer, setRequiresDisclaimer] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const checkConfidence = useCallback(async (request: ConfidenceCheckRequest) => {
        setIsLoading(true);
        setError(null);
        try {
            const response = await checkRecommendationConfidence(request);
            setIsSafe(response.is_safe);
            setConfidenceScore(response.confidence_score);
            setAlertLevel(response.alert_level);
            setRequiresDisclaimer(response.requires_disclaimer || false);
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'Failed to check confidence';
            setError(errorMessage);
        } finally {
            setIsLoading(false);
        }
    }, []);

    return {
        checkConfidence,
        isSafe,
        confidenceScore,
        alertLevel,
        requiresDisclaimer,
        isLoading,
        error
    };
}

// ============================================================================
// OVERTRAINING RISK HOOK
// ============================================================================

interface UseOverttrainingRiskReturn {
    checkOvertraining: (request: OverttrainingRiskRequest) => Promise<void>;
    riskLevel: 'low' | 'medium' | 'high' | null;
    isSafe: boolean;
    alerts: SafetyAlert[];
    recommendations: string[];
    message: string | null;
    isLoading: boolean;
    error: string | null;
}

/**
 * Hook for checking overtraining risk
 */
export function useOverttrainingRisk(resolutionId: number): UseOverttrainingRiskReturn {
    const [riskLevel, setRiskLevel] = useState<'low' | 'medium' | 'high' | null>(null);
    const [isSafe, setIsSafe] = useState(true);
    const [alerts, setAlerts] = useState<SafetyAlert[]>([]);
    const [recommendations, setRecommendations] = useState<string[]>([]);
    const [message, setMessage] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const checkOvertraining = useCallback(
        async (request: OverttrainingRiskRequest) => {
            setIsLoading(true);
            setError(null);
            try {
                const response = await checkOverttrainingRisk(resolutionId, request);
                setRiskLevel(response.risk_level);
                setIsSafe(response.is_safe);
                setAlerts(response.alerts);
                setRecommendations(response.recommendations || []);
                setMessage(response.message || null);
            } catch (err) {
                const errorMessage = err instanceof Error ? err.message : 'Failed to check overtraining';
                setError(errorMessage);
                setRiskLevel(null);
                setIsSafe(true);
                setAlerts([]);
                setRecommendations([]);
                setMessage(null);
            } finally {
                setIsLoading(false);
            }
        },
        [resolutionId]
    );

    return {
        checkOvertraining,
        riskLevel,
        isSafe,
        alerts,
        recommendations,
        message,
        isLoading,
        error
    };
}

// ============================================================================
// ALERT ACKNOWLEDGMENT HOOK
// ============================================================================

interface UseAlertAcknowledgmentReturn {
    acknowledgeAlert: (request: AlertAcknowledgmentRequest) => Promise<void>;
    acknowledged: boolean;
    isLoading: boolean;
    error: string | null;
}

/**
 * Hook for acknowledging safety alerts
 */
export function useAlertAcknowledgment(): UseAlertAcknowledgmentReturn {
    const [acknowledged, setAcknowledged] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const acknowledgeAlert = useCallback(async (request: AlertAcknowledgmentRequest) => {
        setIsLoading(true);
        setError(null);
        try {
            await acknowledgeSafetyAlert(request);
            setAcknowledged(true);
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : 'Failed to acknowledge alert';
            setError(errorMessage);
        } finally {
            setIsLoading(false);
        }
    }, []);

    return {
        acknowledgeAlert,
        acknowledged,
        isLoading,
        error
    };
}

// ============================================================================
// MEDICAL THRESHOLDS HOOK
// ============================================================================

interface UseMedicalThresholdsReturn {
    thresholds: MedicalThresholdsResponse | null;
    isLoading: boolean;
    error: string | null;
}

/**
 * Hook for fetching medical thresholds
 */
export function useMedicalThresholds(): UseMedicalThresholdsReturn {
    const [thresholds, setThresholds] = useState<MedicalThresholdsResponse | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchThresholds = async () => {
            setIsLoading(true);
            setError(null);
            try {
                const data = await getMedicalThresholds();
                setThresholds(data);
            } catch (err) {
                const errorMessage = err instanceof Error ? err.message : 'Failed to fetch thresholds';
                setError(errorMessage);
            } finally {
                setIsLoading(false);
            }
        };

        fetchThresholds();
    }, []);

    return {
        thresholds,
        isLoading,
        error
    };
}

// ============================================================================
// COMBINED SAFETY CHECK HOOK
// ============================================================================

interface UseCombinedSafetyCheckReturn {
    performFullSafetyCheck: (biometrics: BiometricCheckRequest) => Promise<void>;
    biometricAlerts: SafetyAlert[];
    overtrainingAlerts: SafetyAlert[];
    confidenceIssues: boolean;
    overallSafe: boolean;
    isLoading: boolean;
    error: string | null;
}

/**
 * Hook that performs all safety checks together
 */
export function useCombinedSafetyCheck(resolutionId: number): UseCombinedSafetyCheckReturn {
    const biometric = useBiometricSafety(resolutionId);
    const overtraining = useOverttrainingRisk(resolutionId);
    const confidence = useConfidenceCheck();

    const performFullSafetyCheck = useCallback(
        async (biometrics: BiometricCheckRequest) => {
            await Promise.all([
                biometric.checkBiometrics(biometrics),
                overtraining.checkOvertraining({
                    proposed_workout_minutes: 60
                }),
                confidence.checkConfidence({
                    score: 0.75
                })
            ]);
        },
        [biometric, overtraining, confidence]
    );

    return {
        performFullSafetyCheck,
        biometricAlerts: biometric.alerts,
        overtrainingAlerts: overtraining.alerts,
        confidenceIssues: !confidence.isSafe,
        overallSafe: biometric.isSafe && overtraining.isSafe && confidence.isSafe,
        isLoading: biometric.isLoading || overtraining.isLoading || confidence.isLoading,
        error: biometric.error || overtraining.error || confidence.error
    };
}

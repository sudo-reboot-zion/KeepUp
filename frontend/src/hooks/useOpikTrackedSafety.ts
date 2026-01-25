/**
 * Combined Hook: useOpikTrackedSafetyCheck
 * Integrates safety checks with automatic Opik logging
 */

'use client';

import { useCallback } from 'react';
import { useDispatch } from 'react-redux';
import {
    checkBiometricSafetyAsync,
    checkConfidenceAsync,
    checkOverttrainingAsync,
    acknowledgeAlertAsync,
} from '@/redux/slices/safetySlice';
import {
    BiometricCheckRequest,
    ConfidenceCheckRequest,
    OverttrainingRiskRequest,
} from '@/lib/safetyApi';
import {
    opikLogger,
    createBiometricTracker,
    createWorkoutTracker,
} from '@/services/opikClient';
import type { AppDispatch } from '@/redux/store';

/**
 * Hook that combines safety checks with Opik logging
 * Automatically logs all safety events to Opik for observability
 */
export function useOpikTrackedSafetyCheck(resolutionId: number) {
    const dispatch = useDispatch<AppDispatch>();
    const biometricTracker = createBiometricTracker();
    const workoutTracker = createWorkoutTracker(resolutionId);

    /**
     * Perform biometric check with logging
     */
    const checkBiometricsWithLogging = useCallback(
        async (biometrics: BiometricCheckRequest) => {
            try {
                // Perform check
                const result = await dispatch(
                    checkBiometricSafetyAsync({
                        resolutionId,
                        biometrics,
                    })
                ).unwrap();

                // Log to Opik
                if (result.is_safe) {
                    await biometricTracker.logCheck('safe', { ...biometrics } as Record<string, number>);
                } else {
                    const criticalAlerts = result.alerts.filter(
                        (a) => (a.severity ?? '').toLowerCase() === 'critical'
                    );
                    if (criticalAlerts.length > 0) {
                        await biometricTracker.logCheck('critical', { ...biometrics } as Record<string, number>);
                    } else {
                        await biometricTracker.logCheck('warning', { ...biometrics } as Record<string, number>);
                    }
                }

                return result;
            } catch (error) {
                await opikLogger.logBiometricCheck('critical', {});
                throw error;
            }
        },
        [dispatch, resolutionId, biometricTracker]
    );

    /**
     * Perform confidence check with logging
     */
    const checkConfidenceWithLogging = useCallback(
        async (request: ConfidenceCheckRequest) => {
            try {
                const result = await dispatch(checkConfidenceAsync(request)).unwrap();

                // Log to Opik
                await opikLogger.logConfidenceCheck(
                    `confidence_threshold_${request.score}`,
                    request.score,
                    result.is_safe,
                    {
                        alert_level: result.alert_level,
                        requires_disclaimer: result.requires_disclaimer,
                    }
                );

                return result;
            } catch (error) {
                await opikLogger.logConfidenceCheck(
                    'confidence_check_error',
                    0,
                    false,
                    {
                        error: error instanceof Error ? error.message : 'Unknown error',
                    }
                );
                throw error;
            }
        },
        [dispatch]
    );

    /**
     * Perform overtraining check with logging
     */
    const checkOverttrainingWithLogging = useCallback(
        async (data: OverttrainingRiskRequest) => {
            try {
                const result = await dispatch(
                    checkOverttrainingAsync({
                        resolutionId,
                        data,
                    })
                ).unwrap();

                // Log to Opik
                await workoutTracker.logRiskAssessment(
                    result.risk_level,
                    data.proposed_workout_minutes || 0,
                    data.weekly_volume || 0
                );

                return result;
            } catch (error) {
                await workoutTracker.logRiskAssessment(
                    'high',
                    data.proposed_workout_minutes || 0,
                    data.weekly_volume || 0
                );
                throw error;
            }
        },
        [dispatch, resolutionId, workoutTracker]
    );

    /**
     * Acknowledge alert with logging
     */
    const acknowledgeAlertWithLogging = useCallback(
        async (alertId: string, alertType: string) => {
            try {
                await dispatch(
                    acknowledgeAlertAsync({
                        alert_type: alertType,
                        category: 'safety',
                        message: '',
                        action_taken: 'acknowledged',
                    })
                ).unwrap();

                // Log to Opik
                await opikLogger.logAlertAcknowledgment(alertId, alertType, 'acknowledged');

                return true;
            } catch (error) {
                await opikLogger.logAlertAcknowledgment(
                    alertId,
                    alertType,
                    'acknowledgment_failed'
                );
                throw error;
            }
        },
        [dispatch]
    );

    /**
     * Log user interaction with safety features
     */
    const logInteraction = useCallback(
        (component: string, interaction: string, details?: Record<string, unknown>) =>
            opikLogger.logUserInteraction(interaction, component, details),
        []
    );

    /**
     * Log a recommendation with safety context
     */
    const logRecommendationWithSafetyContext = useCallback(
        async (
            recommendationType: string,
            recommendation: unknown,
            confidence: number,
            safetyChecks: {
                biometricSafe?: boolean;
                confidencePass?: boolean;
                overtrainingRisk?: boolean;
            }
        ) => {
            await opikLogger.logUserInteraction(
                'recommendation_display',
                'safety_recommendation',
                {
                    recommendation_type: recommendationType,
                    confidence,
                    biometric_safe: safetyChecks.biometricSafe,
                    confidence_pass: safetyChecks.confidencePass,
                    overtraining_risk: safetyChecks.overtrainingRisk,
                    recommendation: String(recommendation),
                }
            );
        },
        []
    );

    return {
        checkBiometricsWithLogging,
        checkConfidenceWithLogging,
        checkOverttrainingWithLogging,
        acknowledgeAlertWithLogging,
        logInteraction,
        logRecommendationWithSafetyContext,
    };
}

/**
 * Hook for tracked biometric monitoring
 */
export function useTrackedBiometricMonitor(resolutionId: number) {
    const { checkBiometricsWithLogging, logInteraction } =
        useOpikTrackedSafetyCheck(resolutionId);

    return {
        checkBiometrics: checkBiometricsWithLogging,
        logViewing: () => logInteraction('BiometricMonitor', 'view_biometric_data'),
        logWarning: (metric: string, value: number, threshold: number) =>
            logInteraction('BiometricMonitor', 'biometric_warning', {
                metric,
                value,
                threshold,
            }),
    };
}

/**
 * Hook for tracked workout recommendations
 */
export function useTrackedWorkoutRecommendation(resolutionId: number) {
    const { checkOverttrainingWithLogging, logInteraction } =
        useOpikTrackedSafetyCheck(resolutionId);

    return {
        checkOvertraining: checkOverttrainingWithLogging,
        logRecommendationView: (duration: number) =>
            logInteraction('WorkoutRecommendation', 'view_recommendation', {
                proposed_duration: duration,
            }),
        logAcceptance: (duration: number, userConfidence: number) =>
            logInteraction('WorkoutRecommendation', 'accept_recommendation', {
                duration,
                user_confidence: userConfidence,
            }),
        logRejection: (reason: string) =>
            logInteraction('WorkoutRecommendation', 'reject_recommendation', {
                reason,
            }),
    };
}

/**
 * Hook for tracked coaching recommendations
 */
export function useTrackedCoachingRecommendation() {
    const dispatch = useDispatch<AppDispatch>();

    return {
        checkCoachingConfidence: async (request: ConfidenceCheckRequest) => {
            const result = await dispatch(checkConfidenceAsync(request)).unwrap();
            await opikLogger.logConfidenceCheck(
                'coaching_recommendation',
                request.score,
                result.is_safe,
                { requires_disclaimer: result.requires_disclaimer }
            );
            return result;
        },
        logCoachingView: (topic: string) =>
            opikLogger.logUserInteraction('view_coaching', 'CoachingPage', { topic }),
        logCoachingAcceptance: (topic: string, userConfidence: number) =>
            opikLogger.logUserInteraction('accept_coaching', 'CoachingPage', {
                topic,
                user_confidence: userConfidence,
            }),
    };
}

/**
 * Hook for tracked daily check-in
 */
export function useTrackedDailyCheckIn(resolutionId: number) {
    const { checkBiometricsWithLogging, logInteraction } =
        useOpikTrackedSafetyCheck(resolutionId);

    return {
        performCheckIn: async (biometrics: BiometricCheckRequest) => {
            await logInteraction('DailyCheckIn', 'start_check_in');
            const result = await checkBiometricsWithLogging(biometrics);
            await logInteraction('DailyCheckIn', 'complete_check_in', {
                is_safe: result.is_safe,
                alert_count: result.alerts.length,
            });
            return result;
        },
        logMissedCheckIn: () =>
            logInteraction('DailyCheckIn', 'missed_check_in'),
        logSkipped: (reason: string) =>
            logInteraction('DailyCheckIn', 'skipped_check_in', { reason }),
    };
}

export default useOpikTrackedSafetyCheck;

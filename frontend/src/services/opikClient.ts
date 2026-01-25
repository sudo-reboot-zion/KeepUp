/**
 * Opik Frontend Event Logging Service
 * Tracks user interactions, alerts, and decisions for observability
 */

import { apiRequest } from '../lib/api';

// ============================================================================
// TYPES
// ============================================================================

interface OpikEventLog {
    event_type: string;
    event_name: string;
    timestamp: string;
    user_id?: number;
    resolution_id?: number;
    metadata: Record<string, unknown>;
    severity?: 'info' | 'warning' | 'error';
}

interface OpikDecisionLog {
    agent_name: string;
    decision_type: string;
    decision_value: string | boolean | number;
    confidence: number;
    reasoning: string;
    metadata: Record<string, unknown>;
}

interface OpikEventResponse {
    event_id: string;
    logged_at: string;
    status: 'success' | 'failed';
}

// ============================================================================
// OPIK FRONTEND CLIENT
// ============================================================================

export class OpikFrontendLogger {
    private static instance: OpikFrontendLogger;
    private userId?: number;
    private resolutionId?: number;

    private constructor() {}

    /**
     * Get or create singleton instance
     */
    static getInstance(): OpikFrontendLogger {
        if (!OpikFrontendLogger.instance) {
            OpikFrontendLogger.instance = new OpikFrontendLogger();
        }
        return OpikFrontendLogger.instance;
    }

    /**
     * Initialize with user and resolution context
     */
    initialize(userId?: number, resolutionId?: number) {
        this.userId = userId;
        this.resolutionId = resolutionId;
    }

    /**
     * Log a safety alert event
     */
    async logSafetyAlert(
        alertType: string,
        severity: 'critical' | 'high' | 'medium' | 'low',
        message: string,
        metadata?: Record<string, unknown>
    ): Promise<OpikEventResponse | null> {
        try {
            const opikSeverity = severity === 'critical' ? 'error' : severity === 'high' ? 'warning' : 'info';
            const event: OpikEventLog = {
                event_type: 'safety_alert',
                event_name: `Safety Alert: ${alertType}`,
                timestamp: new Date().toISOString(),
                user_id: this.userId,
                resolution_id: this.resolutionId,
                severity: opikSeverity,
                metadata: {
                    alert_type: alertType,
                    message,
                    ...metadata,
                },
            };

            return await this.logEvent(event);
        } catch (error) {
            console.error('Failed to log safety alert:', error);
            return null;
        }
    }

    /**
     * Log a biometric check event
     */
    async logBiometricCheck(
        status: 'safe' | 'warning' | 'critical',
        metrics: Record<string, number>,
        metadata?: Record<string, unknown>
    ): Promise<OpikEventResponse | null> {
        try {
            const event: OpikEventLog = {
                event_type: 'biometric_check',
                event_name: 'Biometric Safety Check',
                timestamp: new Date().toISOString(),
                user_id: this.userId,
                resolution_id: this.resolutionId,
                severity: status === 'safe' ? 'info' : status === 'warning' ? 'warning' : 'error',
                metadata: {
                    status,
                    metrics,
                    ...metadata,
                },
            };

            return await this.logEvent(event);
        } catch (error) {
            console.error('Failed to log biometric check:', error);
            return null;
        }
    }

    /**
     * Log an overtraining risk assessment
     */
    async logOverttrainingAssessment(
        riskLevel: 'low' | 'medium' | 'high',
        workoutMinutes: number,
        weeklyVolume: number,
        metadata?: Record<string, unknown>
    ): Promise<OpikEventResponse | null> {
        try {
            const event: OpikEventLog = {
                event_type: 'overtraining_check',
                event_name: `Overtraining Risk: ${riskLevel}`,
                timestamp: new Date().toISOString(),
                user_id: this.userId,
                resolution_id: this.resolutionId,
                severity: riskLevel === 'low' ? 'info' : riskLevel === 'medium' ? 'warning' : 'error',
                metadata: {
                    risk_level: riskLevel,
                    workout_minutes: workoutMinutes,
                    weekly_volume: weeklyVolume,
                    ...metadata,
                },
            };

            return await this.logEvent(event);
        } catch (error) {
            console.error('Failed to log overtraining assessment:', error);
            return null;
        }
    }

    /**
     * Log a confidence check on a recommendation
     */
    async logConfidenceCheck(
        recommendationType: string,
        confidence: number,
        isSafe: boolean,
        metadata?: Record<string, unknown>
    ): Promise<OpikEventResponse | null> {
        try {
            const event: OpikEventLog = {
                event_type: 'confidence_check',
                event_name: `Confidence Check: ${recommendationType}`,
                timestamp: new Date().toISOString(),
                user_id: this.userId,
                resolution_id: this.resolutionId,
                severity: isSafe ? 'info' : 'warning',
                metadata: {
                    recommendation_type: recommendationType,
                    confidence_score: confidence,
                    is_safe: isSafe,
                    ...metadata,
                },
            };

            return await this.logEvent(event);
        } catch (error) {
            console.error('Failed to log confidence check:', error);
            return null;
        }
    }

    /**
     * Log alert acknowledgment
     */
    async logAlertAcknowledgment(
        alertId: string,
        alertType: string,
        action: string,
        metadata?: Record<string, unknown>
    ): Promise<OpikEventResponse | null> {
        try {
            const event: OpikEventLog = {
                event_type: 'alert_acknowledgment',
                event_name: `Alert Acknowledged: ${alertType}`,
                timestamp: new Date().toISOString(),
                user_id: this.userId,
                resolution_id: this.resolutionId,
                severity: 'info',
                metadata: {
                    alert_id: alertId,
                    alert_type: alertType,
                    action_taken: action,
                    ...metadata,
                },
            };

            return await this.logEvent(event);
        } catch (error) {
            console.error('Failed to log alert acknowledgment:', error);
            return null;
        }
    }

    /**
     * Log user interaction with safety features
     */
    async logUserInteraction(
        interactionType: string,
        component: string,
        details?: Record<string, unknown>
    ): Promise<OpikEventResponse | null> {
        try {
            const event: OpikEventLog = {
                event_type: 'user_interaction',
                event_name: `User Interaction: ${interactionType}`,
                timestamp: new Date().toISOString(),
                user_id: this.userId,
                resolution_id: this.resolutionId,
                severity: 'info',
                metadata: {
                    interaction_type: interactionType,
                    component,
                    ...details,
                },
            };

            return await this.logEvent(event);
        } catch (error) {
            console.error('Failed to log user interaction:', error);
            return null;
        }
    }

    /**
     * Log an agent decision
     */
    async logAgentDecision(
        agentName: string,
        decisionType: string,
        decision: string | boolean | number,
        confidence: number,
        reasoning: string,
        metadata?: Record<string, unknown>
    ): Promise<OpikEventResponse | null> {
        try {
            const decisionLog: OpikDecisionLog = {
                agent_name: agentName,
                decision_type: decisionType,
                decision_value: decision,
                confidence,
                reasoning,
                metadata: {
                    user_id: this.userId,
                    resolution_id: this.resolutionId,
                    timestamp: new Date().toISOString(),
                    ...metadata,
                },
            };

            return await this.logDecision(decisionLog);
        } catch (error) {
            console.error('Failed to log agent decision:', error);
            return null;
        }
    }

    /**
     * Log a debate or discussion event
     */
    async logDebateEvent(
        debateType: string,
        participants: string[],
        outcome: string,
        consensus: number,
        metadata?: Record<string, unknown>
    ): Promise<OpikEventResponse | null> {
        try {
            const event: OpikEventLog = {
                event_type: 'debate',
                event_name: `Debate: ${debateType}`,
                timestamp: new Date().toISOString(),
                user_id: this.userId,
                resolution_id: this.resolutionId,
                severity: 'info',
                metadata: {
                    debate_type: debateType,
                    participants,
                    outcome,
                    consensus_percentage: consensus,
                    ...metadata,
                },
            };

            return await this.logEvent(event);
        } catch (error) {
            console.error('Failed to log debate event:', error);
            return null;
        }
    }

    /**
     * Generic event logging
     */
    private async logEvent(event: OpikEventLog): Promise<OpikEventResponse | null> {
        try {
            const response = await apiRequest<OpikEventResponse>('/api/opik/log-event', {
                method: 'POST',
                body: JSON.stringify(event),
            });

            return response;
        } catch (error) {
            console.warn('Opik event logging not available:', error);
            return null;
        }
    }

    /**
     * Generic decision logging
     */
    private async logDecision(decision: OpikDecisionLog): Promise<OpikEventResponse | null> {
        try {
            const response = await apiRequest<OpikEventResponse>('/api/opik/log-decision', {
                method: 'POST',
                body: JSON.stringify(decision),
            });

            return response;
        } catch (error) {
            console.warn('Opik decision logging not available:', error);
            return null;
        }
    }
}

// ============================================================================
// SINGLETON INSTANCE
// ============================================================================

export const opikLogger = OpikFrontendLogger.getInstance();

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

/**
 * Initialize Opik logger with user context
 */
export function initializeOpikLogger(userId?: number, resolutionId?: number) {
    opikLogger.initialize(userId, resolutionId);
}

/**
 * Create a safety alert tracker for a specific event
 */
export function createAlertTracker(alertType: string) {
    return {
        logAlert: (severity: 'critical' | 'high' | 'medium' | 'low', message: string) =>
            opikLogger.logSafetyAlert(alertType, severity, message),
        logAcknowledgment: (alertId: string, action: string) =>
            opikLogger.logAlertAcknowledgment(alertId, alertType, action),
    };
}

/**
 * Create a biometric tracker for monitoring health metrics
 */
export function createBiometricTracker() {
    return {
        logCheck: (
            status: 'safe' | 'warning' | 'critical',
            metrics: Record<string, number>
        ) =>
            opikLogger.logBiometricCheck(status, metrics),
        logCriticalReading: (metric: string, value: number, threshold: number) =>
            opikLogger.logBiometricCheck('critical', {
                [metric]: value,
                [`${metric}_threshold`]: threshold,
                exceeded_by: value - threshold,
            }),
    };
}

/**
 * Create a workout tracker for safety monitoring
 */
export function createWorkoutTracker(resolutionId: number) {
    return {
        logRiskAssessment: (
            riskLevel: 'low' | 'medium' | 'high',
            workoutMinutes: number,
            weeklyVolume: number
        ) =>
            opikLogger.logOverttrainingAssessment(riskLevel, workoutMinutes, weeklyVolume, {
                resolution_id: resolutionId,
            }),
    };
}

export default opikLogger;

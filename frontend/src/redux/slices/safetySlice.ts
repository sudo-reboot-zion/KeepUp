/**
 * Redux Slice for Safety & Guardrails State Management
 * Manages safety alerts, biometric checks, and risk assessments
 */

import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import {
    checkBiometricSafety,
    checkRecommendationConfidence,
    checkOverttrainingRisk,
    acknowledgeSafetyAlert,
    getMedicalThresholds,
    getSafetyReport,
    BiometricCheckRequest,
    ConfidenceCheckRequest,
    OverttrainingRiskRequest,
    SafetyAlert,
    SafetyCheckResponse,
    ConfidenceCheckResponse,
    OverttrainingRiskResponse,
    MedicalThresholdsResponse,
    SafetyReportResponse,
    AlertAcknowledgmentRequest,
} from '@/lib/safetyApi';

// ============================================================================
// TYPES
// ============================================================================

interface SafetyState {
    // Medical thresholds
    medicalThresholds: MedicalThresholdsResponse | null;
    thresholdsLoading: boolean;
    thresholdsError: string | null;

    // Current alerts
    alerts: SafetyAlert[];
    alertsLoading: boolean;

    // Biometric check state
    lastBiometricCheck: SafetyCheckResponse | null;
    biometricLoading: boolean;
    biometricError: string | null;

    // Confidence check state
    lastConfidenceCheck: ConfidenceCheckResponse | null;
    confidenceLoading: boolean;
    confidenceError: string | null;

    // Overtraining check state
    lastOverttrainingCheck: OverttrainingRiskResponse | null;
    overttrainingLoading: boolean;
    overttrainingError: string | null;

    // Overall safety status
    overallSafe: boolean;
    riskLevel: 'low' | 'medium' | 'high' | null;

    // Safety report
    latestReport: SafetyReportResponse | null;
    reportLoading: boolean;
    reportError: string | null;

    // Acknowledgment tracking
    acknowledgedAlerts: string[];
    acknowledgmentLoading: boolean;
    acknowledgmentError: string | null;
}

// ============================================================================
// ASYNC THUNKS
// ============================================================================

/**
 * Fetch medical thresholds
 */
export const fetchMedicalThresholds = createAsyncThunk(
    'safety/fetchMedicalThresholds',
    async (_, { rejectWithValue }) => {
        try {
            const data = await getMedicalThresholds();
            return data;
        } catch (error) {
            return rejectWithValue(error instanceof Error ? error.message : 'Failed to fetch thresholds');
        }
    }
);

/**
 * Check biometric safety
 */
export const checkBiometricSafetyAsync = createAsyncThunk(
    'safety/checkBiometrics',
    async (
        { resolutionId, biometrics }: { resolutionId: number; biometrics: BiometricCheckRequest },
        { rejectWithValue }
    ) => {
        try {
            const data = await checkBiometricSafety(resolutionId, biometrics);
            return data;
        } catch (error) {
            return rejectWithValue(error instanceof Error ? error.message : 'Failed to check biometrics');
        }
    }
);

/**
 * Check recommendation confidence
 */
export const checkConfidenceAsync = createAsyncThunk(
    'safety/checkConfidence',
    async (request: ConfidenceCheckRequest, { rejectWithValue }) => {
        try {
            const data = await checkRecommendationConfidence(request);
            return data;
        } catch (error) {
            return rejectWithValue(error instanceof Error ? error.message : 'Failed to check confidence');
        }
    }
);

/**
 * Check overtraining risk
 */
export const checkOverttrainingAsync = createAsyncThunk(
    'safety/checkOvertraining',
    async (
        { resolutionId, data }: { resolutionId: number; data: OverttrainingRiskRequest },
        { rejectWithValue }
    ) => {
        try {
            const result = await checkOverttrainingRisk(resolutionId, data);
            return result;
        } catch (error) {
            return rejectWithValue(error instanceof Error ? error.message : 'Failed to check overtraining');
        }
    }
);

/**
 * Acknowledge a safety alert
 */
export const acknowledgeAlertAsync = createAsyncThunk(
    'safety/acknowledgeAlert',
    async (request: AlertAcknowledgmentRequest, { rejectWithValue }) => {
        try {
            await acknowledgeSafetyAlert(request);
            return request.alert_id || request.alert_type;
        } catch (error) {
            return rejectWithValue(error instanceof Error ? error.message : 'Failed to acknowledge alert');
        }
    }
);

/**
 * Fetch safety report
 */
export const fetchSafetyReport = createAsyncThunk(
    'safety/fetchReport',
    async (resolutionId: number, { rejectWithValue }) => {
        try {
            const data = await getSafetyReport(resolutionId);
            return data;
        } catch (error) {
            return rejectWithValue(error instanceof Error ? error.message : 'Failed to fetch report');
        }
    }
);

// ============================================================================
// INITIAL STATE
// ============================================================================

const initialState: SafetyState = {
    medicalThresholds: null,
    thresholdsLoading: false,
    thresholdsError: null,

    alerts: [],
    alertsLoading: false,

    lastBiometricCheck: null,
    biometricLoading: false,
    biometricError: null,

    lastConfidenceCheck: null,
    confidenceLoading: false,
    confidenceError: null,

    lastOverttrainingCheck: null,
    overttrainingLoading: false,
    overttrainingError: null,

    overallSafe: true,
    riskLevel: null,

    latestReport: null,
    reportLoading: false,
    reportError: null,

    acknowledgedAlerts: [],
    acknowledgmentLoading: false,
    acknowledgmentError: null,
};

// ============================================================================
// SLICE
// ============================================================================

const safetySlice = createSlice({
    name: 'safety',
    initialState,
    reducers: {
        // Clear alerts
        clearAlerts: (state) => {
            state.alerts = [];
        },

        // Clear specific alert
        clearAlert: (state, action: PayloadAction<string>) => {
            state.alerts = state.alerts.filter((alert) => alert.id !== action.payload);
        },

        // Reset safety state
        resetSafetyState: (state) => {
            state.alerts = [];
            state.lastBiometricCheck = null;
            state.lastConfidenceCheck = null;
            state.lastOverttrainingCheck = null;
            state.overallSafe = true;
            state.riskLevel = null;
        },

        // Update overall safety status
        updateOverallSafety: (state, action: PayloadAction<boolean>) => {
            state.overallSafe = action.payload;
        },

        // Update risk level
        updateRiskLevel: (state, action: PayloadAction<'low' | 'medium' | 'high' | null>) => {
            state.riskLevel = action.payload;
        },

        // Add alert manually
        addAlert: (state, action: PayloadAction<SafetyAlert>) => {
            state.alerts.push(action.payload);
        },
    },

    extraReducers: (builder) => {
        // Fetch medical thresholds
        builder
            .addCase(fetchMedicalThresholds.pending, (state) => {
                state.thresholdsLoading = true;
                state.thresholdsError = null;
            })
            .addCase(fetchMedicalThresholds.fulfilled, (state, action) => {
                state.thresholdsLoading = false;
                state.medicalThresholds = action.payload;
            })
            .addCase(fetchMedicalThresholds.rejected, (state, action) => {
                state.thresholdsLoading = false;
                state.thresholdsError = action.payload as string;
            });

        // Check biometric safety
        builder
            .addCase(checkBiometricSafetyAsync.pending, (state) => {
                state.biometricLoading = true;
                state.biometricError = null;
            })
            .addCase(checkBiometricSafetyAsync.fulfilled, (state, action) => {
                state.biometricLoading = false;
                state.lastBiometricCheck = action.payload;
                state.alerts = [...action.payload.alerts];
                state.overallSafe = state.overallSafe && action.payload.is_safe;
            })
            .addCase(checkBiometricSafetyAsync.rejected, (state, action) => {
                state.biometricLoading = false;
                state.biometricError = action.payload as string;
            });

        // Check confidence
        builder
            .addCase(checkConfidenceAsync.pending, (state) => {
                state.confidenceLoading = true;
                state.confidenceError = null;
            })
            .addCase(checkConfidenceAsync.fulfilled, (state, action) => {
                state.confidenceLoading = false;
                state.lastConfidenceCheck = action.payload;
                state.overallSafe = state.overallSafe && action.payload.is_safe;
            })
            .addCase(checkConfidenceAsync.rejected, (state, action) => {
                state.confidenceLoading = false;
                state.confidenceError = action.payload as string;
            });

        // Check overtraining
        builder
            .addCase(checkOverttrainingAsync.pending, (state) => {
                state.overttrainingLoading = true;
                state.overttrainingError = null;
            })
            .addCase(checkOverttrainingAsync.fulfilled, (state, action) => {
                state.overttrainingLoading = false;
                state.lastOverttrainingCheck = action.payload;
                state.alerts = [...action.payload.alerts];
                state.riskLevel = action.payload.risk_level;
                state.overallSafe = state.overallSafe && action.payload.is_safe;
            })
            .addCase(checkOverttrainingAsync.rejected, (state, action) => {
                state.overttrainingLoading = false;
                state.overttrainingError = action.payload as string;
            });

        // Acknowledge alert
        builder
            .addCase(acknowledgeAlertAsync.pending, (state) => {
                state.acknowledgmentLoading = true;
                state.acknowledgmentError = null;
            })
            .addCase(acknowledgeAlertAsync.fulfilled, (state, action) => {
                state.acknowledgmentLoading = false;
            if (action.payload) {
                state.acknowledgedAlerts.push(String(action.payload));
            }
                state.alerts = state.alerts.filter((alert) => alert.id !== action.payload);
            })
            .addCase(acknowledgeAlertAsync.rejected, (state, action) => {
                state.acknowledgmentLoading = false;
                state.acknowledgmentError = action.payload as string;
            });

        // Fetch safety report
        builder
            .addCase(fetchSafetyReport.pending, (state) => {
                state.reportLoading = true;
                state.reportError = null;
            })
            .addCase(fetchSafetyReport.fulfilled, (state, action) => {
                state.reportLoading = false;
                state.latestReport = action.payload;
            })
            .addCase(fetchSafetyReport.rejected, (state, action) => {
                state.reportLoading = false;
                state.reportError = action.payload as string;
            });
    },
});

// ============================================================================
// EXPORTS
// ============================================================================

export const {
    clearAlerts,
    clearAlert,
    resetSafetyState,
    updateOverallSafety,
    updateRiskLevel,
    addAlert,
} = safetySlice.actions;

export default safetySlice.reducer;

// Selectors
export const selectMedicalThresholds = (state: { safety: SafetyState }) =>
    state.safety.medicalThresholds;
export const selectThresholdsLoading = (state: { safety: SafetyState }) =>
    state.safety.thresholdsLoading;
export const selectAlerts = (state: { safety: SafetyState }) => state.safety.alerts;
export const selectLastBiometricCheck = (state: { safety: SafetyState }) =>
    state.safety.lastBiometricCheck;
export const selectLastConfidenceCheck = (state: { safety: SafetyState }) =>
    state.safety.lastConfidenceCheck;
export const selectLastOverttrainingCheck = (state: { safety: SafetyState }) =>
    state.safety.lastOverttrainingCheck;
export const selectOverallSafe = (state: { safety: SafetyState }) => state.safety.overallSafe;
export const selectRiskLevel = (state: { safety: SafetyState }) => state.safety.riskLevel;
export const selectLatestReport = (state: { safety: SafetyState }) => state.safety.latestReport;
export const selectAcknowledgedAlerts = (state: { safety: SafetyState }) =>
    state.safety.acknowledgedAlerts;

import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import {
    startOnboarding,
} from '@/lib/onboardingApi';
import type {
    OnboardingData,
    FinalPlan,
    DebateSummary,
    GoalDomain
} from '@/types/onboarding.types';

interface OnboardingState {
    // Form state
    currentStep: number;
    formData: {
        domain: GoalDomain | undefined;
        resolution_text: string;
        past_attempts: string;
        life_constraints: string[];
        occupation: string;
        occupation_details: {
            hours_per_week: number;
            schedule_type: string;
            is_sedentary: boolean;
        };
    };

    // Results
    debateData: DebateSummary | null;
    finalPlan: FinalPlan | null;
    confidenceScore: number | null;

    // UI state
    isLoading: boolean;
    error: string | null;
    isComplete: boolean;
}

const initialState: OnboardingState = {
    currentStep: 1,
    formData: {
        domain: undefined,
        resolution_text: '',
        past_attempts: '',
        life_constraints: [],
        occupation: '',
        occupation_details: {
            hours_per_week: 40,
            schedule_type: '9-5',
            is_sedentary: true
        }
    },
    debateData: null,
    finalPlan: null,
    confidenceScore: null,
    isLoading: false,
    error: null,
    isComplete: false,
};

// ============================================================================
// ASYNC THUNKS
// ============================================================================

/**
 * Submit onboarding form and trigger multi-agent debate
 */
export const submitOnboardingAsync = createAsyncThunk(
    'onboarding/submit',
    async (data: OnboardingData, { rejectWithValue }) => {
        try {
            const response = await startOnboarding({
                ...data,
                occupation: data.occupation || undefined,
                occupation_details: data.occupation_details || undefined
            });
            return response;
        } catch (error: unknown) {
            return rejectWithValue(error instanceof Error ? error.message : 'Onboarding failed');
        }
    }
);

// ============================================================================
// SLICE
// ============================================================================

const onboardingSlice = createSlice({
    name: 'onboarding',
    initialState,
    reducers: {
        // Form navigation
        nextStep: (state) => {
            if (state.currentStep < 4) {
                state.currentStep += 1;
            }
        },
        previousStep: (state) => {
            if (state.currentStep > 1) {
                state.currentStep -= 1;
            }
        },
        setStep: (state, action: PayloadAction<number>) => {
            state.currentStep = action.payload;
        },

        // Form data updates
        updateFormData: (state, action: PayloadAction<Partial<OnboardingState['formData']>>) => {
            state.formData = {
                ...state.formData,
                ...action.payload,
            };
        },

        addLifeConstraint: (state, action: PayloadAction<string>) => {
            if (!state.formData.life_constraints.includes(action.payload)) {
                state.formData.life_constraints.push(action.payload);
            }
        },

        removeLifeConstraint: (state, action: PayloadAction<string>) => {
            state.formData.life_constraints = state.formData.life_constraints.filter(
                c => c !== action.payload
            );
        },

        // Reset
        resetOnboarding() {
            return initialState;
        },

        clearError: (state) => {
            state.error = null;
        },
    },

    extraReducers: (builder) => {
        // Submit onboarding
        builder
            .addCase(submitOnboardingAsync.pending, (state) => {
                state.isLoading = true;
                state.error = null;
            })
            .addCase(submitOnboardingAsync.fulfilled, (state, action) => {
                state.isLoading = false;
                state.debateData = action.payload.debate_summary;
                state.finalPlan = action.payload.final_plan;
                state.confidenceScore = action.payload.confidence_score;
                state.isComplete = true;
                state.error = null;
            })
            .addCase(submitOnboardingAsync.rejected, (state, action) => {
                state.isLoading = false;
                state.error = action.payload as string;
            });
    },
});

export const {
    nextStep,
    previousStep,
    setStep,
    updateFormData,
    addLifeConstraint,
    removeLifeConstraint,
    resetOnboarding,
    clearError,
} = onboardingSlice.actions;

export default onboardingSlice.reducer;


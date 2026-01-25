import { configureStore } from '@reduxjs/toolkit';
import uiReducer from './slices/uiSlice';
import authReducer from './slices/authSlice';
import onboardingReducer from './slices/onboardingSlice';

export const store = configureStore({
    reducer: {
        auth: authReducer,
        ui: uiReducer,
        onboarding: onboardingReducer
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware({
            serializableCheck: false,
        }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

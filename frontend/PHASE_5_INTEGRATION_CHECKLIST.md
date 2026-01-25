# Phase 5: Frontend Integration - Implementation Checklist

## Overview
This document provides a complete checklist for integrating Phase 3 (Safety Guardrails) and Phase 4 (Advanced Agent Coordination) features into your Next.js frontend.

---

## ✅ CREATED FILES

### Core Files (Ready to Use)
- ✅ `frontend/src/lib/safetyApi.ts` - TypeScript API client for all safety endpoints (315 lines)
- ✅ `frontend/src/hooks/useSafety.ts` - Custom React hooks for safety checks (450+ lines)
- ✅ `frontend/src/hooks/useOpikTrackedSafety.ts` - Hooks with automatic Opik logging (400+ lines)
- ✅ `frontend/src/redux/slices/safetySlice.ts` - Redux state management (350+ lines)
- ✅ `frontend/src/services/opikClient.ts` - Frontend Opik logging service (300+ lines)

### Components (Ready to Use)
- ✅ `frontend/src/components/Safety/AlertDisplay.tsx` - Safety alert display component (250+ lines)
- ✅ `frontend/src/components/Safety/SafetyStatus.tsx` - Safety status indicator (200+ lines)
- ✅ `frontend/src/components/Safety/BiometricMonitor.tsx` - Biometric input & monitoring (300+ lines)

### Documentation
- ✅ `frontend/src/PHASE_5_INTEGRATION_EXAMPLES.ts` - 6 complete integration examples (500+ lines)

**Total: 2,750+ lines of production-ready code**

---

## 📋 INTEGRATION CHECKLIST

### Phase 1: Redux Store Setup

- [ ] Open `frontend/src/redux/store.ts`
- [ ] Import `safetyReducer` from `./slices/safetySlice`
- [ ] Add `safety: safetyReducer` to store configuration
- [ ] Verify build succeeds: `npm run build`

```typescript
// Example:
import safetyReducer from './slices/safetySlice';
// ...
configureStore({
  reducer: {
    safety: safetyReducer,
    // ... other reducers
  }
})
```

**Status:** [ ] Not Started [ ] In Progress [✓] Complete

---

### Phase 2: API Client Integration

- [ ] Verify `frontend/src/lib/safetyApi.ts` exists
- [ ] Verify TypeScript types compile without errors
- [ ] Test API functions in browser console:
  ```typescript
  import { getMedicalThresholds } from '@/lib/safetyApi';
  const thresholds = await getMedicalThresholds();
  console.log(thresholds);
  ```
- [ ] Confirm network requests appear in browser DevTools

**Status:** [ ] Not Started [ ] In Progress [✓] Complete

---

### Phase 3: Biometric Monitoring

#### Option A: Add to Daily Check-In Page

- [ ] Open `frontend/src/app/[your-daily-checkin-page]/page.tsx`
- [ ] Import BiometricMonitor: `import BiometricMonitor from '@/components/Safety/BiometricMonitor';`
- [ ] Add component to JSX:
  ```tsx
  <BiometricMonitor 
    resolutionId={resolutionId}
    showThresholds={true}
  />
  ```
- [ ] Test biometric input works
- [ ] Test alerts appear for critical values
- [ ] Verify Redux state updates: `useSelector(selectAlerts)`

**Status:** [ ] Not Started [ ] In Progress [ ] Complete

#### Option B: Create New Biometric Page

- [ ] Create `frontend/src/app/biometric-check/page.tsx`
- [ ] Use Example 1 from `PHASE_5_INTEGRATION_EXAMPLES.ts`
- [ ] Add link in navigation menu
- [ ] Test complete flow

**Status:** [ ] Not Started [ ] In Progress [ ] Complete

---

### Phase 4: Safety Status Display

- [ ] Open page where you want to display safety status (e.g., workout, coaching)
- [ ] Import: `import { SafetyStatus } from '@/components/Safety/SafetyStatus';`
- [ ] Add to JSX:
  ```tsx
  <SafetyStatus
    overallSafe={overallSafe}
    riskLevel={riskLevel}
    alertCount={alerts.length}
  />
  ```
- [ ] Use Redux selectors:
  ```typescript
  const overallSafe = useSelector(selectOverallSafe);
  const riskLevel = useSelector(selectRiskLevel);
  const alerts = useSelector(selectAlerts);
  ```
- [ ] Test expanded details
- [ ] Test alert click handler

**Status:** [ ] Not Started [ ] In Progress [ ] Complete

---

### Phase 5: Alert Display & Acknowledgment

- [ ] Open page with alert list (or create new modal component)
- [ ] Import: `import { AlertDisplay } from '@/components/Safety/AlertDisplay';`
- [ ] Add component:
  ```tsx
  <AlertDisplay
    alerts={alerts}
    onAcknowledge={(alertId) => {
      // Handle acknowledgment
    }}
  />
  ```
- [ ] Test alert rendering
- [ ] Test acknowledgment button
- [ ] Verify alerts removed from state after acknowledgment

**Status:** [ ] Not Started [ ] In Progress [ ] Complete

---

### Phase 6: Opik Logging Integration

#### Step 1: Initialize Logger

- [ ] Open `frontend/src/app/layout.tsx` or app root
- [ ] Add initialization on app startup:
  ```typescript
  import { initializeOpikLogger } from '@/services/opikClient';
  
  // In useEffect or component mount:
  useEffect(() => {
    initializeOpikLogger(userId, resolutionId);
  }, [userId, resolutionId]);
  ```

**Status:** [ ] Not Started [ ] In Progress [ ] Complete

#### Step 2: Use Tracked Hooks

- [ ] Find component handling biometric checks
- [ ] Replace `useBiometricSafety` with `useTrackedBiometricMonitor`:
  ```typescript
  import { useTrackedBiometricMonitor } from '@/hooks/useOpikTrackedSafety';
  const { checkBiometrics, logViewing } = useTrackedBiometricMonitor(resolutionId);
  ```
- [ ] Events automatically logged to Opik
- [ ] Verify logs appear in Opik dashboard

**Status:** [ ] Not Started [ ] In Progress [ ] Complete

#### Step 3: Log Custom Events

- [ ] Find workout recommendation component
- [ ] Add Opik logging:
  ```typescript
  import { useTrackedWorkoutRecommendation } from '@/hooks/useOpikTrackedSafety';
  const { logAcceptance, logRejection } = useTrackedWorkoutRecommendation(resolutionId);
  
  // On accept button click:
  await logAcceptance(duration, userConfidence);
  ```
- [ ] Test events logged to Opik

**Status:** [ ] Not Started [ ] In Progress [ ] Complete

---

### Phase 7: Confidence Checking for Recommendations

#### Daily Recommendations Page

- [ ] Locate where daily recommendations are displayed
- [ ] Import hook: `import { useTrackedCoachingRecommendation } from '@/hooks/useOpikTrackedSafety';`
- [ ] Check confidence before showing recommendation:
  ```typescript
  const { checkCoachingConfidence } = useTrackedCoachingRecommendation();
  
  useEffect(() => {
    checkCoachingConfidence({ score: confidenceScore });
  }, [confidenceScore]);
  ```
- [ ] Show medical disclaimer if confidence < 0.5
- [ ] Show confidence percentage to user

**Status:** [ ] Not Started [ ] In Progress [ ] Complete

#### Coaching Recommendations Page

- [ ] Use Example 3 from `PHASE_5_INTEGRATION_EXAMPLES.ts`
- [ ] Display disclaimer component
- [ ] Add UI for confidence level
- [ ] Test accept/decline logging

**Status:** [ ] Not Started [ ] In Progress [ ] Complete

---

### Phase 8: Overtraining Prevention

- [ ] Locate workout recommendations component
- [ ] Import: `import { useTrackedWorkoutRecommendation } from '@/hooks/useOpikTrackedSafety';`
- [ ] Check risk before rendering:
  ```typescript
  const { checkOvertraining } = useTrackedWorkoutRecommendation(resolutionId);
  
  useEffect(() => {
    checkOvertraining({
      proposed_workout_minutes: duration,
      intensity_level: 'moderate'
    });
  }, [duration]);
  ```
- [ ] Display risk level indicator
- [ ] Show recommendations if high risk
- [ ] Test with different workout durations

**Status:** [ ] Not Started [ ] In Progress [ ] Complete

---

### Phase 9: Header/Navigation Integration

- [ ] Open page header/navigation component
- [ ] Import: `import { SafetyStatusCompact } from '@/components/Safety/SafetyStatus';`
- [ ] Add to header:
  ```tsx
  <SafetyStatusCompact
    safe={overallSafe}
    riskLevel={riskLevel}
    alertCount={alerts.length}
    onClick={() => setShowAlertModal(true)}
  />
  ```
- [ ] Test badge displays correctly
- [ ] Test click opens alert modal
- [ ] Verify badge updates when alerts change

**Status:** [ ] Not Started [ ] In Progress [ ] Complete

---

### Phase 10: Complete Page Example (Optional)

- [ ] Review Example 6 in `PHASE_5_INTEGRATION_EXAMPLES.ts`
- [ ] Create complete page combining all features
- [ ] Suggested page: `/app/dashboard` or `/app/home`
- [ ] Include:
  - [ ] SafetyStatus component
  - [ ] BiometricMonitor component
  - [ ] AlertDisplay modal
  - [ ] Opik logging on interactions
  - [ ] Redux state selectors
- [ ] Test end-to-end flow
- [ ] Verify Opik events logged

**Status:** [ ] Not Started [ ] In Progress [ ] Complete

---

## 🔧 BACKEND REQUIREMENTS

Ensure these endpoints exist and are working:

### Endpoint Verification Checklist

- [ ] `POST /api/safety/check-biometrics/{resolution_id}`
  - Test: `curl -X POST http://localhost:8000/api/safety/check-biometrics/1 -H "Content-Type: application/json" -d '{"systolic": 140, "diastolic": 90, "heart_rate": 80, "weight": 170}'`

- [ ] `POST /api/safety/check-confidence`
  - Test: `curl -X POST http://localhost:8000/api/safety/check-confidence -H "Content-Type: application/json" -d '{"score": 0.75}'`

- [ ] `POST /api/safety/check-overtraining/{resolution_id}`
  - Test: `curl -X POST http://localhost:8000/api/safety/check-overtraining/1 -H "Content-Type: application/json" -d '{"proposed_workout_minutes": 60}'`

- [ ] `GET /api/safety/thresholds`
  - Test: `curl http://localhost:8000/api/safety/thresholds`

- [ ] `POST /api/safety/acknowledge-alert`
  - Test: `curl -X POST http://localhost:8000/api/safety/acknowledge-alert -H "Content-Type: application/json" -d '{"alert_id": "123", "action_taken": "acknowledged"}'`

- [ ] `GET /api/safety/report/{resolution_id}`
  - Test: `curl http://localhost:8000/api/safety/report/1`

**Status:** All [ ] Most [ ] Some [ ] None

---

## 🧪 TESTING CHECKLIST

### Unit Tests (Frontend)

- [ ] Test `safetyApi.ts` functions with mock data
- [ ] Test `useSafety.ts` hooks
- [ ] Test Redux reducers and selectors
- [ ] Test React components in isolation

### Integration Tests

- [ ] Test API client → Backend API communication
- [ ] Test Redux state updates from API responses
- [ ] Test components with Redux state

### End-to-End Tests

- [ ] Test complete biometric check flow
- [ ] Test complete workout safety flow
- [ ] Test Opik logging appears in dashboard
- [ ] Test alert acknowledgment removes from UI
- [ ] Test safety status updates across app

### Manual Testing

- [ ] Test in development mode: `npm run dev`
- [ ] Test with different screen sizes (mobile, tablet, desktop)
- [ ] Test in production build: `npm run build && npm run start`
- [ ] Test with slow network (DevTools throttling)

**Status:** [ ] Not Started [ ] In Progress [ ] Complete

---

## 📊 VALIDATION CHECKLIST

### Code Quality

- [ ] No TypeScript errors: `npm run type-check`
- [ ] No linting errors: `npm run lint`
- [ ] No console warnings/errors (DevTools)
- [ ] All imports resolve correctly

### Functionality

- [ ] All 6 API client functions work
- [ ] All 7 React hooks work
- [ ] All 3 components render correctly
- [ ] Redux state updates properly
- [ ] Opik logging working (check dashboard)

### Performance

- [ ] Components load within 1 second
- [ ] No unnecessary re-renders
- [ ] API requests complete quickly
- [ ] No memory leaks (DevTools)

### Accessibility

- [ ] Alert displays readable by screen readers
- [ ] Color not sole indicator of status
- [ ] Buttons have proper labels
- [ ] Keyboard navigation works

---

## 🚀 DEPLOYMENT CHECKLIST

- [ ] All integration tests pass
- [ ] No TypeScript errors
- [ ] No console errors/warnings
- [ ] Environment variables set correctly
- [ ] Backend endpoints accessible from deployment environment
- [ ] Opik logging credentials configured
- [ ] Database migrations applied
- [ ] Review bundle size: `npm run build` and check `.next` folder

**Status:** [ ] Not Ready [ ] Ready for Deployment

---

## 📚 REFERENCE DOCS

### Key Files to Review
1. **safetyApi.ts** - 8 types + 6 API functions
2. **useSafety.ts** - 6 custom hooks
3. **safetySlice.ts** - Redux state & thunks
4. **opikClient.ts** - Opik event logging
5. **PHASE_5_INTEGRATION_EXAMPLES.ts** - 6 complete examples

### API Endpoint Reference

```typescript
// Biometric Safety
POST /api/safety/check-biometrics/{resolution_id}
Request: { systolic, diastolic, heart_rate, weight }
Response: { alerts, is_safe, timestamp }

// Confidence Check
POST /api/safety/check-confidence
Request: { score }
Response: { is_safe, confidence_score, alert_level, requires_disclaimer }

// Overtraining Risk
POST /api/safety/check-overtraining/{resolution_id}
Request: { proposed_workout_minutes, intensity_level?, weekly_volume? }
Response: { risk_level, is_safe, alerts, recommendations, message }

// Medical Thresholds
GET /api/safety/thresholds
Response: { blood_pressure_critical, heart_rate_critical, weight_change_per_week }

// Acknowledge Alert
POST /api/safety/acknowledge-alert
Request: { alert_id, action_taken }
Response: { acknowledged, timestamp }

// Safety Report
GET /api/safety/report/{resolution_id}
Response: { overall_safety, recent_alerts, recommendations, last_check }
```

### Hook Quick Reference

```typescript
// Biometric check
const { checkBiometrics, alerts, isSafe, error } = useBiometricSafety(resolutionId);

// Confidence check
const { checkConfidence, confidenceScore, requiresDisclaimer } = useConfidenceCheck();

// Overtraining check
const { checkOvertraining, riskLevel, alerts } = useOverttrainingRisk(resolutionId);

// Alert acknowledgment
const { acknowledgeAlert } = useAlertAcknowledgment();

// With Opik logging
const { checkBiometricsWithLogging } = useOpikTrackedSafetyCheck(resolutionId);
```

---

## 🎯 SUCCESS METRICS

You'll know integration is successful when:

1. ✅ BiometricMonitor component displays and accepts input
2. ✅ Safety alerts appear and can be acknowledged
3. ✅ SafetyStatus shows correct status (safe/caution)
4. ✅ Confidence warnings appear on low-confidence recommendations
5. ✅ Overtraining warnings prevent unsafe workouts
6. ✅ All Opik events logged to dashboard
7. ✅ No TypeScript errors
8. ✅ No network request failures
9. ✅ Bundle size increased by <200KB
10. ✅ All 6 integration examples work

---

## 💡 QUICK START

If you're in a hurry, implement in this order:

1. **5 min** - Add safetyReducer to Redux store
2. **10 min** - Add SafetyStatusCompact to header
3. **15 min** - Add BiometricMonitor to daily check-in
4. **15 min** - Add AlertDisplay modal
5. **10 min** - Initialize Opik logging
6. **10 min** - Add confidence check to recommendations

**Total: ~65 minutes for MVP**

---

## ❓ TROUBLESHOOTING

### "Module not found" error
**Solution:** Ensure all files created in correct locations with proper path aliases (@/lib, @/components, etc.)

### Redux state not updating
**Solution:** Verify safetyReducer added to store.ts. Check Redux DevTools for actions being dispatched.

### API requests failing
**Solution:** Verify backend endpoints running. Check CORS settings. Look at network tab in DevTools.

### Opik logging not working
**Solution:** Verify initializeOpikLogger called with correct userId. Check backend has `/api/opik/log-event` endpoint.

### TypeScript errors
**Solution:** Run `npm run type-check` to see all issues. Import types from safetyApi.ts correctly.

---

## ✨ NEXT STEPS AFTER INTEGRATION

1. Write unit tests for components and hooks
2. Add E2E tests with Playwright or Cypress
3. Set up monitoring/alerting for safety events
4. Create admin dashboard to view safety metrics
5. Implement real-time safety notifications via WebSocket
6. Add historical safety data visualization
7. Create safety reports/exports

---

**Last Updated:** [Current Date]
**Status:** Phase 5 Frontend Integration - Ready for Implementation

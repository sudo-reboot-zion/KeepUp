'use client';

import { useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import gsap from 'gsap';
import { useAppDispatch, useAppSelector } from '@/redux/hooks';
import {
    nextStep,
    previousStep,
    updateFormData,
    addLifeConstraint,
    removeLifeConstraint,
    submitOnboardingAsync,
    clearError,
} from '@/redux/slices/onboardingSlice';
import OnboardingHeader from './components/OnboardingHeader';
import ProgressIndicator from './components/ProgressIndicator';
import StepContent from './components/StepContent';
import NavigationButtons from './components/NavigationButtons';
import StepLabel from './components/StepLabel';

export default function OnboardingPage() {
    const router = useRouter();
    const dispatch = useAppDispatch();
    const { currentStep, formData, isLoading, error } = useAppSelector(state => state.onboarding);
    const formRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        dispatch(clearError());
        if (formRef.current) {
            gsap.fromTo(formRef.current, { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8, ease: 'power3.out' });
        }
    }, [currentStep, dispatch]);

    const handleNext = () => {
        if (currentStep === 1 && !formData.resolution_text.trim()) return;
        if (currentStep < 4) {
            dispatch(nextStep());
        } else {
            handleSubmit();
        }
    };

    const handleSubmit = async () => {
        const result = await dispatch(submitOnboardingAsync({
            resolution_text: formData.resolution_text,
            past_attempts: formData.past_attempts || undefined,
            life_constraints: formData.life_constraints.length > 0 ? formData.life_constraints : undefined,
            occupation: formData.occupation,
            occupation_details: formData.occupation_details
        }));
        if (submitOnboardingAsync.fulfilled.match(result)) {
            router.push('/onboarding/debate');
        }
    };

    const isNextDisabled = isLoading ||
        (currentStep === 1 && !formData.resolution_text.trim()) ||
        (currentStep === 4 && !formData.occupation);



    // ... (inside component)
    return (
        <main className="min-h-screen bg-[var(--bg)] text-[var(--fg)] selection:bg-[var(--primary)] selection:text-[var(--bg)]">

            <div className="relative min-h-screen flex items-center justify-center px-6 overflow-hidden">
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-[var(--primary)] rounded-full blur-[150px] opacity-10 animate-pulse duration-[5000ms]" />

                <div className="relative w-full max-w-2xl">
                    <OnboardingHeader />
                    <ProgressIndicator currentStep={currentStep} />

                    <div ref={formRef} className="bg-[var(--card)] backdrop-blur-xl border border-[var(--border)] p-6 rounded-3xl shadow-2xl">
                        {error && (
                            <div className="mb-6 bg-red-500/10 border border-red-500/50 rounded-xl px-4 py-3 text-red-400 text-sm">
                                {error}
                            </div>
                        )}

                        <StepContent
                            currentStep={currentStep}
                            formData={formData}
                            onUpdateText={(field, value) => dispatch(updateFormData({ [field]: value }))}
                            onUpdateDomain={(domain) => dispatch(updateFormData({ domain }))}
                            onUpdateOccupation={(value) => dispatch(updateFormData({ occupation: value }))}
                            onUpdateOccupationDetails={(details) => dispatch(updateFormData({
                                occupation_details: { ...formData.occupation_details, ...details }
                            }))}
                            onAddConstraint={(constraint) => dispatch(addLifeConstraint(constraint))}
                            onRemoveConstraint={(constraint) => dispatch(removeLifeConstraint(constraint))}
                        />

                        <NavigationButtons
                            currentStep={currentStep}
                            isLoading={isLoading}
                            isNextDisabled={isNextDisabled}
                            onBack={() => dispatch(previousStep())}
                            onNext={handleNext}
                        />
                    </div>

                    <StepLabel currentStep={currentStep} />
                </div>
            </div>
        </main>
    );
}

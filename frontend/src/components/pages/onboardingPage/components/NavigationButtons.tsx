import ArrowButton from '@/components/common/ArrowButton';

interface NavigationButtonsProps {
    currentStep: number;
    isLoading: boolean;
    isNextDisabled: boolean;
    onBack: () => void;
    onNext: () => void;
}

export default function NavigationButtons({
    currentStep,
    isLoading,
    isNextDisabled,
    onBack,
    onNext
}: NavigationButtonsProps) {
    return (
        <div className="flex justify-between mt-6 pt-4 border-t border-[var(--border)]">
            <button
                onClick={onBack}
                disabled={currentStep === 1}
                className="px-6 py-2 text-[var(--fg)] opacity-60 hover:opacity-100 transition-all disabled:opacity-0 disabled:cursor-not-allowed text-sm"
            >
                ← Back
            </button>

            <ArrowButton
                onClick={onNext}
                disabled={isNextDisabled}
                isLoading={isLoading}
                text={currentStep === 4 ? 'Start Debate' : 'Next'}
                className="bg-[var(--primary)] hover:bg-[var(--secondary)] text-[var(--bg)] border-none py-2 px-6 text-base"
            />
        </div>
    );
}

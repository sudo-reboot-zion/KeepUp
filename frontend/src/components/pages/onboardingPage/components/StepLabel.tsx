interface StepLabelProps {
    currentStep: number;
}

const stepLabels = ['Your Goal', 'Past Attempts', 'Life Constraints', 'Occupation'];

export default function StepLabel({ currentStep }: StepLabelProps) {
    return (
        <div className="mt-6 text-center text-sm text-[var(--fg)] opacity-40">
            Step {currentStep} of 4: {stepLabels[currentStep - 1]}
        </div>
    );
}

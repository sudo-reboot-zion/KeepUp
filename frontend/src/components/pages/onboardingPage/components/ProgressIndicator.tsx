interface ProgressIndicatorProps {
    currentStep: number;
}

const stepLabels = ['Goal', 'History', 'Constraints', 'Occupation'];

export default function ProgressIndicator({ currentStep }: ProgressIndicatorProps) {
    return (
        <div className="flex justify-center mb-8">
            {[1, 2, 3, 4].map((step) => (
                <div key={step} className="flex items-center relative">
                    <div className="flex flex-col items-center absolute -top-6 left-1/2 -translate-x-1/2 w-32">
                        <span className={`text-[10px] font-medium transition-colors duration-300 ${currentStep === step ? 'text-[var(--primary)]' : 'text-transparent'}`}>
                            {stepLabels[step - 1]}
                        </span>
                    </div>
                    <div
                        className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold transition-all duration-500 border-2 ${currentStep >= step
                            ? 'bg-[var(--primary)] border-[var(--primary)] text-[var(--bg)] shadow-[0_0_15px_var(--primary)]'
                            : 'bg-transparent border-[var(--border)] text-[var(--fg)] opacity-40'
                            }`}
                    >
                        {step}
                    </div>
                    {step < 4 && (
                        <div
                            className={`w-8 md:w-16 h-0.5 mx-1 transition-all duration-500 ${currentStep > step ? 'bg-[var(--primary)]' : 'bg-[var(--fg)] opacity-10'
                                }`}
                        />
                    )}
                </div>
            ))}
        </div>
    );
}

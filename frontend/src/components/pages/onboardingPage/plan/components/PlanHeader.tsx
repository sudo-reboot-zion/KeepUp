export default function PlanHeader() {
    return (
        <div className="mb-24 plan-header flex flex-col md:flex-row md:items-end justify-between gap-12">
            <h1 className="text-6xl md:text-8xl font-black tracking-tighter leading-[0.9]">
                Your Strategy <br />
                is Locked.
            </h1>

            <div className="flex items-center gap-8 max-w-md md:mb-2">
                {/* Vertical Gradient Line */}
                <div className="w-[2px] h-24 bg-gradient-to-b from-purple-500 to-[var(--primary)] shrink-0" />

                <p className="text-xl text-[var(--fg)] opacity-60 leading-relaxed font-medium">
                    The AI Council has finalized your personalized roadmap.
                </p>
            </div>
        </div>
    );
}

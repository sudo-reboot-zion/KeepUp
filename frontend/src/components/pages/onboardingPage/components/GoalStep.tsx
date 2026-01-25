import { Lightbulb, Dumbbell, Brain, Heart, Sun } from 'lucide-react';
import type { GoalDomain } from '@/types/onboarding.types';

interface GoalStepProps {
    value: string;
    onChange: (value: string) => void;
    domain?: GoalDomain;
    onDomainChange: (domain: GoalDomain) => void;
}

export default function GoalStep({ value, onChange, domain, onDomainChange }: GoalStepProps) {
    const domains: { id: GoalDomain; label: string; icon: React.ElementType; desc: string }[] = [
        { id: 'physical', label: 'Physical Vitality', icon: Dumbbell, desc: 'Fitness, sleep, nutrition' },
        { id: 'mental', label: 'Mental Clarity', icon: Brain, desc: 'Focus, learning, growth' },
        { id: 'emotional', label: 'Emotional Balance', icon: Heart, desc: 'Stress, resilience, peace' },
        { id: 'lifestyle', label: 'Lifestyle & Routine', icon: Sun, desc: 'Habits, discipline, work' },
    ];

    const getPlaceholder = () => {
        switch (domain) {
            case 'physical': return "e.g., 'I want to run a marathon', 'Lose 10kg', 'Fix my back pain'...";
            case 'mental': return "e.g., 'Read 20 books this year', 'Learn Spanish', 'Deep work for 4 hours/day'...";
            case 'emotional': return "e.g., 'Reduce anxiety', 'Start journaling', 'Meditate daily'...";
            case 'lifestyle': return "e.g., 'Wake up at 5am', 'Quit social media', 'Save money'...";
            default: return "e.g., 'I want to get fit', 'Lose 20 lbs', 'Run a marathon', 'Build muscle'...";
        }
    };

    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-2xl font-bold mb-2">What&apos;s your main focus?</h2>
                <p className="text-[var(--fg)] opacity-60 text-sm mb-4">
                    Choose a domain to help us understand your goal better.
                </p>
            </div>

            <div className="grid grid-cols-2 gap-3">
                {domains.map((d) => (
                    <button
                        key={d.id}
                        onClick={() => onDomainChange(d.id)}
                        className={`p-4 rounded-xl border text-left transition-all ${domain === d.id
                            ? 'bg-[var(--primary)] border-[var(--primary)] text-[var(--bg)]'
                            : 'bg-[var(--fg)]/5 border-[var(--border)] text-[var(--fg)] hover:border-[var(--primary)]/50'
                            }`}
                    >
                        <d.icon className={`w-6 h-6 mb-2 ${domain === d.id ? 'text-[var(--bg)]' : 'text-[var(--primary)]'}`} />
                        <div className="font-medium text-sm">{d.label}</div>
                        <div className={`text-xs mt-1 ${domain === d.id ? 'opacity-80' : 'opacity-50'}`}>{d.desc}</div>
                    </button>
                ))}
            </div>

            <div className={`space-y-2 transition-all duration-500 ${domain ? 'opacity-100 translate-y-0' : 'opacity-50 translate-y-4 grayscale pointer-events-none'}`}>
                <label className="text-sm font-medium text-[var(--fg)] opacity-60 ml-1">
                    Your Specific Goal
                </label>
                <textarea
                    value={value}
                    onChange={(e) => onChange(e.target.value)}
                    className="w-full bg-[var(--fg)]/5 border border-[var(--border)] rounded-xl px-4 py-3 text-[var(--fg)] placeholder-[var(--fg)]/40 focus:outline-none focus:border-[var(--primary)] focus:ring-1 focus:ring-[var(--primary)] transition-all min-h-[120px] resize-none"
                    placeholder={getPlaceholder()}
                    required
                    disabled={!domain}
                />
            </div>

            <div className="bg-[var(--fg)]/5 border border-[var(--border)] rounded-xl p-4 flex items-start gap-3">
                <Lightbulb className="w-5 h-5 text-[var(--primary)] shrink-0 mt-0.5" />
                <p className="text-xs text-[var(--fg)] opacity-60">
                    <strong>Tip:</strong> The more context you provide, the better your AI agents can help. But don&apos;t worry - they&apos;ll ask questions if needed.
                </p>
            </div>
        </div>
    );
}

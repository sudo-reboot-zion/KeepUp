import { Search } from 'lucide-react';

interface PastAttemptsStepProps {
    value: string;
    onChange: (value: string) => void;
}

export default function PastAttemptsStep({ value, onChange }: PastAttemptsStepProps) {
    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-2xl font-bold mb-2">Have you tried before?</h2>
                <p className="text-[var(--fg)] opacity-60 text-sm mb-4">
                    Our Failure Pattern Agent will analyze your history to prevent past mistakes.
                </p>
            </div>

            <div className="space-y-2">
                <label className="text-sm font-medium text-[var(--fg)] opacity-60 ml-1">
                    Past Attempts (Optional)
                </label>
                <textarea
                    value={value}
                    onChange={(e) => onChange(e.target.value)}
                    className="w-full bg-[var(--fg)]/5 border border-[var(--border)] rounded-xl px-4 py-3 text-[var(--fg)] placeholder-[var(--fg)]/40 focus:outline-none focus:border-[var(--primary)] focus:ring-1 focus:ring-[var(--primary)] transition-all min-h-[120px] resize-none"
                    placeholder="e.g., 'Tried going to gym 3 times, always quit after 2-3 weeks', 'Started running but got injured', 'Too busy with work'..."
                />
            </div>

            <div className="bg-[var(--fg)]/5 border border-[var(--border)] rounded-xl p-4 flex items-start gap-3">
                <Search className="w-5 h-5 text-[var(--primary)] shrink-0 mt-0.5" />
                <p className="text-xs text-[var(--fg)] opacity-60">
                    <strong>Why we ask:</strong> Our AI detects patterns in when and why people quit. This helps us design a plan that works for YOU.
                </p>
            </div>
        </div>
    );
}

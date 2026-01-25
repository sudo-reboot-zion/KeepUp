import { useState } from 'react';
import { Zap } from 'lucide-react';

interface ConstraintsStepProps {
    constraints: string[];
    onAdd: (constraint: string) => void;
    onRemove: (constraint: string) => void;
}

export default function ConstraintsStep({ constraints, onAdd, onRemove }: ConstraintsStepProps) {
    const [localConstraint, setLocalConstraint] = useState('');

    const handleAdd = () => {
        if (localConstraint.trim()) {
            onAdd(localConstraint.trim());
            setLocalConstraint('');
        }
    };

    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-2xl font-bold mb-2">What&apos;s your situation?</h2>
                <p className="text-[var(--fg)] opacity-60 text-sm mb-4">
                    Help us understand your life constraints so we can create a realistic plan.
                </p>
            </div>

            <div className="space-y-2">
                <label className="text-sm font-medium text-[var(--fg)] opacity-60 ml-1">
                    Add Constraints
                </label>
                <div className="flex gap-2">
                    <input
                        type="text"
                        value={localConstraint}
                        onChange={(e) => setLocalConstraint(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleAdd())}
                        className="flex-1 bg-[var(--fg)]/5 border border-[var(--border)] rounded-xl px-4 py-3 text-[var(--fg)] placeholder-[var(--fg)]/40 focus:outline-none focus:border-[var(--primary)] focus:ring-1 focus:ring-[var(--primary)] transition-all"
                        placeholder="e.g., 'Busy schedule', 'No gym access', 'Knee injury'..."
                    />
                    <button
                        type="button"
                        onClick={handleAdd}
                        className="px-6 py-3 bg-[var(--fg)]/10 text-[var(--fg)] rounded-xl hover:bg-[var(--primary)] hover:text-[var(--bg)] transition-all"
                    >
                        Add
                    </button>
                </div>
            </div>

            {/* Constraints List */}
            {constraints.length > 0 && (
                <div className="space-y-2">
                    <label className="text-sm font-medium text-[var(--fg)] opacity-60 ml-1">
                        Your Constraints
                    </label>
                    <div className="flex flex-wrap gap-2">
                        {constraints.map((constraint, index) => (
                            <div
                                key={index}
                                className="bg-[var(--fg)]/10 border border-[var(--border)] rounded-full px-4 py-2 flex items-center gap-2 group hover:border-red-500/50 transition-all"
                            >
                                <span className="text-sm">{constraint}</span>
                                <button
                                    onClick={() => onRemove(constraint)}
                                    className="text-[var(--fg)] opacity-40 hover:text-red-500 transition-colors"
                                >
                                    ×
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            <div className="bg-[var(--fg)]/5 border border-[var(--border)] rounded-xl p-4 flex items-start gap-3">
                <Zap className="w-5 h-5 text-[var(--primary)] shrink-0 mt-0.5" />
                <p className="text-xs text-[var(--fg)] opacity-60">
                    <strong>Examples:</strong> &quot;Work 60hrs/week&quot;, &quot;Home gym only&quot;, &quot;Shoulder injury&quot;, &quot;Single parent&quot;, &quot;Travel frequently&quot;
                </p>
            </div>
        </div>
    );
}

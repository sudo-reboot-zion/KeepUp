import React from 'react';
import { Send } from 'lucide-react';

interface OnboardingInputProps {
    value: string;
    onChange: (value: string) => void;
    onSubmit: () => void;
    disabled?: boolean;
}

export default function OnboardingInput({ value, onChange, onSubmit, disabled }: OnboardingInputProps) {
    return (
        <div className="p-4 border-t border-[var(--border)] bg-[var(--navbar-bg)] backdrop-blur-md rounded-b-3xl">
            <form
                onSubmit={(e) => {
                    e.preventDefault();
                    onSubmit();
                }}
                className="flex gap-3 items-center"
            >
                <input
                    type="text"
                    value={value}
                    onChange={(e) => onChange(e.target.value)}
                    placeholder="Type your answer..."
                    className="flex-1 bg-[var(--bg)] border border-[var(--border)] rounded-xl px-4 py-3 text-[var(--fg)] focus:outline-none focus:ring-2 focus:ring-[var(--primary)] transition-all placeholder:opacity-40"
                    disabled={disabled}
                />
                <button
                    type="submit"
                    disabled={!value.trim() || disabled}
                    className="p-3 rounded-xl bg-[var(--fg)] text-[var(--bg)] hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg"
                >
                    <Send size={20} />
                </button>
            </form>
        </div>
    );
}

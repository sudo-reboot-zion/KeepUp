import React, { useState } from 'react';
import { Settings, Bell, Users, Brain, Plus } from 'lucide-react';

interface ProfilePreferencesProps {
    onRecordEvent: () => void;
}

export default function ProfilePreferences({ onRecordEvent }: ProfilePreferencesProps) {
    return (
        <div className="p-8 md:p-12 space-y-8 bg-[var(--bg)]">
            <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-bold uppercase tracking-widest text-[var(--fg)]/50">Preferences</h3>
                <Settings className="w-5 h-5 text-[var(--fg)]/50" />
            </div>
            <div className="space-y-6">
                <PreferenceToggle label="Daily Reminders" icon={<Bell className="w-4 h-4" />} defaultOn={true} />
                <PreferenceToggle label="Partner Updates" icon={<Users className="w-4 h-4" />} defaultOn={true} />
                <PreferenceToggle label="AI Insights" icon={<Brain className="w-4 h-4" />} defaultOn={false} />
            </div>
            <button
                onClick={onRecordEvent}
                className="w-full py-4 bg-[var(--fg)]/5 hover:bg-[var(--fg)]/10 border border-[var(--border)] rounded-2xl font-bold flex items-center justify-center gap-3 transition-all group"
            >
                <Plus className="w-5 h-5 group-hover:rotate-90 transition-transform" />
                Record Life Event
            </button>
        </div>
    );
}

function PreferenceToggle({ label, icon, defaultOn }: { label: string; icon: React.ReactNode; defaultOn: boolean }) {
    const [isOn, setIsOn] = useState(defaultOn);
    return (
        <div className="flex items-center justify-between group/toggle">
            <div className="flex items-center gap-4">
                <div className="p-2 bg-[var(--fg)]/5 rounded-lg text-[var(--fg)]/50 group-hover/toggle:text-[var(--fg)] transition-colors">
                    {icon}
                </div>
                <p className="font-bold text-[var(--fg)]/80 group-hover/toggle:text-[var(--fg)] transition-colors">{label}</p>
            </div>
            <button
                onClick={() => setIsOn(!isOn)}
                className={`w-12 h-6 rounded-full transition-all relative ${isOn ? 'bg-[var(--primary)]' : 'bg-[var(--fg)]/10'}`}
            >
                <div className={`absolute top-1 w-4 h-4 rounded-full bg-[var(--bg)] transition-all ${isOn ? 'left-7' : 'left-1'}`} />
            </button>
        </div>
    );
}

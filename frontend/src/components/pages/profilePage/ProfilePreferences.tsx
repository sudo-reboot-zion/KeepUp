import React, { useState } from 'react';
import { Settings, Bell, Users, Brain, Plus, Sliders } from 'lucide-react';

interface ProfilePreferencesProps {
    onRecordEvent: () => void;
}

export default function ProfilePreferences({ onRecordEvent }: ProfilePreferencesProps) {
    return (
        <div className="space-y-10">
            <div className="flex items-center justify-between border-b border-border pb-4">
                <div className="flex items-center gap-3">
                    <Sliders size={18} className="text-secondary" />
                    <h3 className="text-xs font-black uppercase tracking-widest text-foreground">Protocol Overrides</h3>
                </div>
                <Settings className="w-4 h-4 text-muted-foreground animate-spin-slow" />
            </div>

            <div className="space-y-5">
                <PreferenceToggle label="Neural Reminders" icon={<Bell className="w-4 h-4" />} defaultOn={true} />
                <PreferenceToggle label="Sync Protocol" icon={<Users className="w-4 h-4" />} defaultOn={true} />
                <PreferenceToggle label="AI Optimization" icon={<Brain className="w-4 h-4" />} defaultOn={false} />
            </div>

            <button
                onClick={onRecordEvent}
                className="w-full py-4 bg-primary text-black hover:bg-primary/90 rounded-2xl font-black uppercase tracking-widest text-[10px] flex items-center justify-center gap-3 transition-all shadow-xl shadow-primary/10 group"
            >
                <Plus className="w-4 h-4 group-hover:rotate-90 transition-transform" />
                Record Protocol Event
            </button>
        </div>
    );
}

function PreferenceToggle({ label, icon, defaultOn }: { label: string; icon: React.ReactNode; defaultOn: boolean }) {
    const [isOn, setIsOn] = useState(defaultOn);
    return (
        <div className="flex items-center justify-between group/toggle p-3 bg-foreground/5 rounded-2xl border border-border/50 hover:border-primary/30 transition-all">
            <div className="flex items-center gap-4">
                <div className={`p-2 rounded-lg transition-colors ${isOn ? 'text-primary bg-primary/10' : 'text-muted-foreground bg-background'}`}>
                    {icon}
                </div>
                <p className={`text-[10px] font-black uppercase tracking-widest transition-colors ${isOn ? 'text-foreground' : 'text-muted-foreground'}`}>{label}</p>
            </div>
            <button
                onClick={() => setIsOn(!isOn)}
                className={`w-10 h-5 rounded-full transition-all relative ${isOn ? 'bg-primary' : 'bg-muted-foreground/20'}`}
            >
                <div className={`absolute top-1 w-3 h-3 rounded-full bg-background transition-all shadow-sm ${isOn ? 'left-6' : 'left-1'}`} />
            </button>
        </div>
    );
}

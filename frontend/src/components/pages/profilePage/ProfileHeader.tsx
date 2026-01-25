import React from 'react';

interface ProfileHeaderProps {
    displayName: string;
    username: string;
    resolution: string | null;
}

export default function ProfileHeader({ displayName, username, resolution }: ProfileHeaderProps) {
    return (
        <div className="bg-[var(--bg)] p-12 flex flex-col md:flex-row justify-between items-start gap-12 border-b border-[var(--border)]">
            <div className="space-y-8 flex-1">
                <div className="space-y-2">
                    <p className="text-[10px] tracking-[0.2em] text-[var(--fg)]/50 font-bold uppercase">Human Name:</p>
                    <h1 className="text-7xl md:text-8xl font-black leading-[0.85] tracking-tighter uppercase break-words">
                        {displayName || username}
                    </h1>
                </div>
                <p className="text-xl text-[var(--fg)]/60 max-w-xl leading-relaxed">
                    {resolution || "No resolution set. Start your journey to define your protocol and optimize your existence."}
                </p>
                <div className="flex gap-4 pt-4">
                    <div className="w-4 h-4 border-l border-b border-[var(--border)]" />
                    <div className="flex-1" />
                    <div className="w-4 h-4 border-r border-b border-[var(--border)]" />
                </div>
            </div>

            <div className="w-48 h-48 md:w-64 md:h-64 bg-gradient-to-br from-[var(--primary)] to-[var(--secondary)] rounded-[40px] flex items-center justify-center text-6xl md:text-8xl font-black text-[var(--bg)] shrink-0 shadow-[0_0_50px_rgba(201,252,110,0.2)]">
                {(displayName?.[0] || username?.[0] || 'U').toUpperCase()}
            </div>
        </div>
    );
}

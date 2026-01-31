import React from 'react';

interface ProfileHeaderProps {
    displayName: string;
    username: string;
    resolution: string | null;
}

export default function ProfileHeader({ displayName, username, resolution }: ProfileHeaderProps) {
    return (
        <div className="bg-background p-10 flex flex-col md:flex-row justify-between items-center gap-10">
            <div className="space-y-6 flex-1 text-center md:text-left">
                <div className="space-y-1">
                    <p className="text-[10px] tracking-[0.3em] text-muted-foreground font-black uppercase">Biological Identity</p>
                    <h1 className="text-5xl md:text-6xl font-black leading-none tracking-tighter uppercase break-words text-foreground">
                        {displayName || username}
                    </h1>
                </div>
                <p className="text-lg text-muted-foreground max-w-xl leading-relaxed font-medium italic">
                    "{resolution || "No dynamic resolution detected. Protocol pending initialization."}"
                </p>
            </div>

            <div className="w-40 h-40 md:w-48 md:h-48 bg-gradient-to-tr from-primary to-secondary rounded-[2.5rem] flex items-center justify-center text-5xl md:text-6xl font-black text-background shrink-0 shadow-2xl shadow-primary/20 rotate-3 hover:rotate-0 transition-transform duration-500">
                {(displayName?.[0] || username?.[0] || 'U').toUpperCase()}
            </div>
        </div>
    );
}

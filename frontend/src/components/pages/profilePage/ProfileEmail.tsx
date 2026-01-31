import React from 'react';
import { Mail, Edit2 } from 'lucide-react';

interface ProfileEmailProps {
    email: string;
}

export default function ProfileEmail({ email }: ProfileEmailProps) {
    return (
        <div className="space-y-4">
            <div className="flex items-center gap-2">
                <Mail size={14} className="text-muted-foreground" />
                <p className="text-[10px] tracking-[0.2em] text-muted-foreground font-black uppercase">Authentication Terminal</p>
            </div>
            <div className="flex items-center justify-between p-4 bg-foreground/5 rounded-2xl border border-border group cursor-pointer hover:border-primary/50 transition-all">
                <p className="text-sm font-black text-foreground truncate max-w-[200px]">{email}</p>
                <div className="w-8 h-8 rounded-full bg-background border border-border flex items-center justify-center text-muted-foreground group-hover:text-primary transition-all">
                    <Edit2 size={12} />
                </div>
            </div>
        </div>
    );
}

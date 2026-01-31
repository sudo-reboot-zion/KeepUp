import React from 'react';
import Link from 'next/link';
import {
    LayoutDashboard,
    Activity,
    Dumbbell,
    MessageSquare,
    Brain,
    Zap
} from 'lucide-react';

export default function ProfileQuickLinks() {
    return (
        <div className="grid grid-cols-3 gap-2">
            <QuickLinkIcon icon={<LayoutDashboard size={20} />} href="/dashboard" label="Home" />
            <QuickLinkIcon icon={<Activity size={20} />} href="/history" label="Logs" />
            <QuickLinkIcon icon={<Dumbbell size={20} />} href="/schedule" label="Train" />
            <QuickLinkIcon icon={<MessageSquare size={20} />} href="/chat" label="Sync" />
            <QuickLinkIcon icon={<Brain size={20} />} href="/debate" label="Council" />
            <QuickLinkIcon icon={<Zap size={20} />} href="/onboarding" label="Start" />
        </div>
    );
}

function QuickLinkIcon({ icon, href, label }: { icon: React.ReactNode; href: string; label: string }) {
    return (
        <Link
            href={href}
            className="flex flex-col items-center justify-center gap-2 p-4 bg-foreground/5 border border-border rounded-2xl hover:bg-primary hover:border-primary group transition-all duration-300"
        >
            <div className="text-foreground group-hover:text-background group-hover:scale-110 transition-all duration-300">
                {icon}
            </div>
            <span className="text-[9px] font-black uppercase tracking-widest text-muted-foreground group-hover:text-background transition-colors">
                {label}
            </span>
        </Link>
    );
}

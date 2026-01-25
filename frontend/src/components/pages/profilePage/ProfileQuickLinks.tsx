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
        <div className="grid grid-cols-3 md:grid-cols-6 bg-[var(--bg)] border-b border-[var(--border)]">
            <QuickLinkIcon icon={<LayoutDashboard className="w-6 h-6" />} href="/dashboard" />
            <QuickLinkIcon icon={<Activity className="w-6 h-6" />} href="/progress" />
            <QuickLinkIcon icon={<Dumbbell className="w-6 h-6" />} href="/workout" />
            <QuickLinkIcon icon={<MessageSquare className="w-6 h-6" />} href="/chat" />
            <QuickLinkIcon icon={<Brain className="w-6 h-6" />} href="/debate" />
            <QuickLinkIcon icon={<Zap className="w-6 h-6" />} href="/onboarding" />
        </div>
    );
}

function QuickLinkIcon({ icon, href }: { icon: React.ReactNode; href: string }) {
    return (
        <Link
            href={href}
            className="aspect-square flex items-center justify-center border-r border-[var(--border)] last:border-r-0 text-[var(--fg)] hover:bg-[var(--primary)] hover:text-[var(--bg)] transition-all duration-300 group"
        >
            <div className="group-hover:scale-125 transition-transform duration-300">
                {icon}
            </div>
        </Link>
    );
}

import React from 'react';
import Link from 'next/link';
import { ArrowRight } from 'lucide-react';

interface ProfileInfoProps {
    resolution: string | null;
    occupation: string | null;
}

export default function ProfileInfo({ resolution, occupation }: ProfileInfoProps) {
    return (
        <div className="grid md:grid-cols-[240px_1fr] bg-[var(--bg)] border-b border-[var(--border)] group">
            <div className="p-8 border-b md:border-b-0 md:border-r border-[var(--border)] bg-[var(--fg)]/5">
                <p className="text-[10px] tracking-[0.2em] text-[var(--fg)]/50 font-bold uppercase mb-4">Protocol:</p>
                <div className="w-2 h-24 bg-gradient-to-b from-[var(--primary)] to-transparent rounded-full opacity-20" />
            </div>
            <div className="divide-y divide-[var(--border)]">
                <InfoRow label="Resolution" value={resolution || "Not Defined"} href="/onboarding" />
                <InfoRow label="Occupation" value={occupation || "Not Specified"} />
                <InfoRow label="Status" value="Active Protocol" />
            </div>
        </div>
    );
}

function InfoRow({ label, value, href }: { label: string; value: string; href?: string }) {
    const content = (
        <div className="flex items-center justify-between p-8 group/row cursor-pointer hover:bg-[var(--fg)]/5 transition-colors">
            <div className="space-y-1">
                <p className="text-[10px] tracking-[0.2em] text-[var(--fg)]/50 font-bold uppercase">{label}:</p>
                <p className="text-2xl font-bold text-[var(--fg)] group-hover/row:text-[var(--primary)] transition-colors">{value}</p>
            </div>
            <ArrowRight className="w-6 h-6 text-[var(--fg)]/40 group-hover/row:text-[var(--primary)] group-hover/row:translate-x-2 transition-all" />
        </div>
    );

    return href ? <Link href={href}>{content}</Link> : content;
}

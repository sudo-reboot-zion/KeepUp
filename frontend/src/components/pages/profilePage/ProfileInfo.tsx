import React from 'react';
import Link from 'next/link';
import { ArrowRight, Fingerprint, Briefcase, Activity } from 'lucide-react';

interface ProfileInfoProps {
    resolution: string | null;
    occupation: string | null;
}

export default function ProfileInfo({ resolution, occupation }: ProfileInfoProps) {
    return (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-0 divide-y md:divide-y-0 md:divide-x divide-border">
            <InfoRow
                label="Dynamic Resolution"
                value={resolution || "Not Defined"}
                href="/onboarding"
                icon={<Fingerprint size={16} className="text-primary" />}
            />
            <InfoRow
                label="Professional Vector"
                value={occupation || "Not Specified"}
                icon={<Briefcase size={16} className="text-secondary" />}
            />
            <InfoRow
                label="Protocol Status"
                value="Optimized"
                icon={<Activity size={16} className="text-primary" />}
            />
        </div>
    );
}

function InfoRow({ label, value, href, icon }: { label: string; value: string; href?: string, icon?: React.ReactNode }) {
    const content = (
        <div className="flex flex-col gap-3 p-8 group/row cursor-pointer hover:bg-foreground/[0.02] transition-colors relative overflow-hidden">
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                    {icon}
                    <p className="text-[10px] tracking-[0.2em] text-muted-foreground font-black uppercase">{label}</p>
                </div>
                <ArrowRight className="w-4 h-4 text-muted-foreground opacity-0 group-hover/row:opacity-100 group-hover/row:translate-x-2 transition-all" />
            </div>
            <p className="text-xl font-black text-foreground group-hover/row:text-primary transition-colors uppercase tracking-tight truncate">{value}</p>
            <div className="absolute bottom-0 left-0 w-full h-[2px] bg-primary scale-x-0 group-hover/row:scale-x-100 transition-transform origin-left" />
        </div>
    );

    return href ? <Link href={href} className="block">{content}</Link> : content;
}

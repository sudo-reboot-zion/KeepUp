import { ReactElement } from 'react';

interface PlanCardProps {
    icon: ReactElement;
    title: string;
    description: string;
}

export default function PlanCard({ icon, title, description }: PlanCardProps) {
    return (
        <div className="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-8 hover:bg-[var(--muted)] transition-all duration-300 group plan-card flex flex-col items-start h-full">
            <div className="mb-6 text-[var(--fg)] opacity-60 group-hover:text-[var(--primary)] transition-colors">
                {icon}
            </div>
            <h3 className="text-xl font-semibold text-[var(--fg)] mb-3">{title}</h3>
            <p className="text-[var(--fg)] opacity-60 text-sm leading-relaxed">
                {description}
            </p>
        </div>
    );
}

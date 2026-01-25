import { Check, ShieldAlert } from 'lucide-react';
import type { AgentMessage } from '@/types/debate.types';
import { parseBold } from '../utils/textParser';
import { getAgentStyle } from '../utils/agentStyles';

interface AgentMessageCardProps {
    message: AgentMessage;
}

export default function AgentMessageCard({ message }: AgentMessageCardProps) {
    const style = getAgentStyle(message.agent);

    return (
        <div className="group relative p-8 border-b border-r border-[var(--border)] bg-[var(--card)] hover:bg-[var(--muted)] transition-colors duration-300 min-h-[300px] flex flex-col animate-fade-in">
            {/* Top Icon */}
            <div className="mb-8">
                {style.icon}
            </div>

            {/* Content */}
            <div className="flex-1">
                <div className={`font-bold text-xl mb-1 ${style.text}`}>{message.agent}</div>
                <div className="text-xs text-[var(--fg)] opacity-50 uppercase tracking-wider mb-6">{message.role}</div>

                <div className="text-[var(--fg)] opacity-80 leading-relaxed text-sm whitespace-pre-line">
                    {message.type === 'challenge' && message.message.includes('Challenge Initiated') ? (
                        <div className="flex items-start gap-3">
                            <ShieldAlert className="w-6 h-6 text-orange-500 shrink-0 mt-0.5" />
                            <div>{parseBold(message.message.replace(/⚠️|✓/g, ''))}</div>
                        </div>
                    ) : message.type === 'synthesis' ? (
                        <div className="flex items-start gap-3">
                            <Check className="w-6 h-6 text-[var(--primary)] shrink-0 mt-0.5" />
                            <div>{parseBold(message.message.replace(/⚠️|✓/g, ''))}</div>
                        </div>
                    ) : (
                        parseBold(message.message.replace(/⚠️|✓/g, ''))
                    )}
                </div>
            </div>
        </div>
    );
}

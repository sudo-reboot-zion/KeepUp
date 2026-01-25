import { Target, AlertTriangle, Scale, Bot } from 'lucide-react';
import type { AgentStyle } from '@/types/debate.types';

/**
 * Get agent-specific styling configuration
 */
export function getAgentStyle(agentName: string): AgentStyle {
    const name = agentName.toLowerCase();

    if (name.includes('goal')) {
        return {
            text: 'text-blue-500 dark:text-blue-400',
            icon: <Target className="w-12 h-12 text-blue-500 dark:text-blue-400" />
        };
    }

    if (name.includes('failure') || name.includes('pattern')) {
        return {
            text: 'text-orange-500 dark:text-orange-400',
            icon: <AlertTriangle className="w-12 h-12 text-orange-500 dark:text-orange-400" />
        };
    }

    if (name.includes('meta') || name.includes('coordinator') || name.includes('judge')) {
        return {
            text: 'text-[var(--primary)]',
            icon: <Scale className="w-12 h-12 text-[var(--primary)]" />
        };
    }

    return {
        text: 'text-[var(--fg)] opacity-50',
        icon: <Bot className="w-12 h-12 text-[var(--fg)] opacity-50" />
    };
}

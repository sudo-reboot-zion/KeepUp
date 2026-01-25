import React from 'react';

/**
 * Parse bold text in markdown format (**text**)
 */
export function parseBold(text: string): (string | React.ReactElement)[] {
    const parts = text.split(/(\*\*.*?\*\*)/g);
    return parts.map((part, index) => {
        if (part.startsWith('**') && part.endsWith('**')) {
            return <strong key={index} className="text-[var(--fg)] font-bold">{part.slice(2, -2)}</strong>;
        }
        return part;
    });
}

/**
 * Clean null or "null" string values
 */
export function clean(val: string | null | undefined): string | null {
    if (!val) return null;
    if (String(val).toLowerCase() === 'null') return null;
    return val;
}

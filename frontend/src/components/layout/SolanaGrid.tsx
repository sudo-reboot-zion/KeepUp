'use client';

import React from 'react';

interface SolanaGridProps {
    children: React.ReactNode;
    className?: string;
}

/**
 * SolanaGrid - A high-contrast layout wrapper with background grid lines
 * and neon accents inspired by Solana's aesthetic.
 */
export default function SolanaGrid({ children, className = '' }: SolanaGridProps) {
    return (
        <div className={`relative min-h-screen bg-[#0a0a0a] text-white overflow-hidden ${className}`}>
            {/* Background Grid Lines */}
            <div className="absolute inset-0 z-0 pointer-events-none opacity-20">
                <div
                    className="absolute inset-0"
                    style={{
                        backgroundImage: `
              linear-gradient(to right, #1e1e1e 1px, transparent 1px),
              linear-gradient(to bottom, #1e1e1e 1px, transparent 1px)
            `,
                        backgroundSize: '40px 40px'
                    }}
                />
            </div>

            {/* Neon Accents / Glows */}
            <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-[#14f195] opacity-[0.03] blur-[120px] rounded-full pointer-events-none" />
            <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-[#9945ff] opacity-[0.03] blur-[120px] rounded-full pointer-events-none" />

            {/* Scanline Effect (Subtle) */}
            <div className="absolute inset-0 z-0 pointer-events-none opacity-[0.02] bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.25)_50%),linear-gradient(90deg,rgba(255,0,0,0.06),rgba(0,255,0,0.02),rgba(0,0,255,0.06))] bg-[length:100%_2px,3px_100%]" />

            {/* Content Wrapper */}
            <div className="relative z-10 flex flex-col min-h-screen">
                {children}
            </div>

            {/* Decorative Border Lines (Solana Grid Style) */}
            <div className="absolute top-0 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-[#14f195]/30 to-transparent" />
            <div className="absolute bottom-0 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-[#9945ff]/30 to-transparent" />
            <div className="absolute top-0 left-0 w-[1px] h-full bg-gradient-to-b from-transparent via-[#14f195]/30 to-transparent" />
            <div className="absolute top-0 right-0 w-[1px] h-full bg-gradient-to-b from-transparent via-[#9945ff]/30 to-transparent" />
        </div>
    );
}

// Additional styling for grid cells if needed
export function GridCell({ children, className = '', title }: { children: React.ReactNode, className?: string, title?: string }) {
    return (
        <div className={`border border-[#1e1e1e] bg-[#0d0d0d]/80 backdrop-blur-sm relative group ${className}`}>
            {/* Corner Accents */}
            <div className="absolute top-0 left-0 w-2 h-2 border-t border-l border-[#14f195]/50 opacity-0 group-hover:opacity-100 transition-opacity" />
            <div className="absolute top-0 right-0 w-2 h-2 border-t border-r border-[#14f195]/50 opacity-0 group-hover:opacity-100 transition-opacity" />
            <div className="absolute bottom-0 left-0 w-2 h-2 border-b border-l border-[#9945ff]/50 opacity-0 group-hover:opacity-100 transition-opacity" />
            <div className="absolute bottom-0 right-0 w-2 h-2 border-b border-r border-[#9945ff]/50 opacity-0 group-hover:opacity-100 transition-opacity" />

            {title && (
                <div className="border-b border-[#1e1e1e] px-4 py-2 flex items-center justify-between">
                    <span className="text-[10px] uppercase tracking-[0.2em] font-bold text-gray-500">
                        {title}
                    </span>
                    <div className="w-1.5 h-1.5 rounded-full bg-[#14f195] shadow-[0_0_8px_#14f195]" />
                </div>
            )}

            <div className="p-4">
                {children}
            </div>
        </div>
    );
}

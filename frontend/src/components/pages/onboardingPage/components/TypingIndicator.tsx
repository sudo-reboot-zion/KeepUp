import React from 'react';
import { motion } from 'framer-motion';

export default function TypingIndicator() {
    return (
        <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex justify-start mb-4"
        >
            <div className="bg-[var(--muted)] p-4 rounded-2xl rounded-bl-sm border border-[var(--border)] flex gap-1.5 items-center h-12 relative">
                <motion.div
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ repeat: Infinity, duration: 1, delay: 0 }}
                    className="w-2 h-2 rounded-full bg-[var(--fg)] opacity-40"
                />
                <motion.div
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ repeat: Infinity, duration: 1, delay: 0.2 }}
                    className="w-2 h-2 rounded-full bg-[var(--fg)] opacity-40"
                />
                <motion.div
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ repeat: Infinity, duration: 1, delay: 0.4 }}
                    className="w-2 h-2 rounded-full bg-[var(--fg)] opacity-40"
                />
                {/* Tail SVG for typing indicator */}
                <svg
                    className="absolute bottom-[1px] w-4 h-4 z-0 -left-[6px] text-[var(--muted)] transform scale-x-[-1]"
                    viewBox="0 0 20 20"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                >
                    <path d="M0 20L20 20L0 0V20Z" fill="currentColor" />
                </svg>
            </div>
        </motion.div>
    );
}

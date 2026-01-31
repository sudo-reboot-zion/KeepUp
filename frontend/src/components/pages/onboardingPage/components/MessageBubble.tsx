import React from 'react';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import { Message } from '../types';

interface MessageBubbleProps {
    message: Message;
    onOptionClick?: (option: string) => void;
}

export default function MessageBubble({ message, onOptionClick }: MessageBubbleProps) {
    const isUser = message.sender === 'user';

    return (
        <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            transition={{ duration: 0.3, ease: "easeOut" }}
            className={cn(
                "flex w-full mb-4",
                isUser ? "justify-end" : "justify-start"
            )}
        >
            <div className="relative max-w-[80%]">
                <div
                    className={cn(
                        "p-4 rounded-2xl text-sm md:text-base leading-relaxed shadow-sm relative z-10",
                        isUser
                            ? "bg-[var(--fg)] text-[var(--bg)] rounded-br-sm"
                            : "bg-[var(--muted)] text-[var(--fg)] rounded-bl-sm border border-[var(--border)]"
                    )}
                >
                    <p>{message.text}</p>
                    <span className={cn(
                        "text-[10px] block text-right mt-1",
                        isUser ? "opacity-70" : "opacity-50"
                    )}>
                        {new Intl.DateTimeFormat('en-US', { hour: 'numeric', minute: 'numeric', hour12: true }).format(message.timestamp)}
                    </span>
                </div>

                {/* Tail SVG */}
                <svg
                    className={cn(
                        "absolute bottom-[1px] w-4 h-4 z-0",
                        isUser
                            ? "-right-[6px] text-[var(--fg)]"
                            : "-left-[6px] text-[var(--muted)] transform scale-x-[-1]"
                    )}
                    viewBox="0 0 20 20"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                >
                    <path d="M0 20L20 20L0 0V20Z" fill="currentColor" />
                </svg>

                {/* Options */}
                {message.type === 'options' && message.options && (
                    <div className="flex flex-wrap gap-2 mt-3">
                        {message.options.map((option, idx) => (
                            <motion.button
                                key={idx}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: idx * 0.1 }}
                                onClick={() => onOptionClick?.(option)}
                                className="px-4 py-2 rounded-full border border-[var(--primary)] text-[var(--primary)] hover:bg-[var(--primary)] hover:text-[var(--bg)] transition-all text-sm font-medium bg-[var(--bg)]"
                            >
                                {option}
                            </motion.button>
                        ))}
                    </div>
                )}
            </div>
        </motion.div>
    );
}

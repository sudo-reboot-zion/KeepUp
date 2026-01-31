'use client';

import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, X, Bot, User, Sparkles } from 'lucide-react';

interface Message {
    id: string;
    text: string;
    sender: 'user' | 'ai';
    timestamp: Date;
}

interface AskAIChatProps {
    isOpen: boolean;
    onClose: () => void;
}

import { sendChatMessage } from '@/lib/chatApi';

export default function AskAIChat({ isOpen, onClose }: AskAIChatProps) {
    const [messages, setMessages] = useState<Message[]>([
        {
            id: '1',
            text: "Welcome to KEEP UP. I am your protocol optimization assistant. How can I facilitate your progress today?",
            sender: 'ai',
            timestamp: new Date(),
        },
    ]);
    const [inputValue, setInputValue] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages, isTyping]);

    const handleSend = async () => {
        if (!inputValue.trim()) return;

        const userMsgText = inputValue;
        const userMessage: Message = {
            id: Date.now().toString(),
            text: userMsgText,
            sender: 'user',
            timestamp: new Date(),
        };

        setMessages(prev => [...prev, userMessage]);
        setInputValue('');
        setIsTyping(true);

        try {
            const response = await sendChatMessage(userMsgText, { stage: 'general' });

            const aiMessage: Message = {
                id: (Date.now() + 1).toString(),
                text: response.message,
                sender: 'ai',
                timestamp: new Date(),
            };
            setMessages(prev => [...prev, aiMessage]);
        } catch (error) {
            console.error('AI Protocol Link Error:', error);
            const errorMessage: Message = {
                id: (Date.now() + 2).toString(),
                text: "Signal interference detected. Please re-establish protocol link (Check your connection or backend status).",
                sender: 'ai',
                timestamp: new Date(),
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsTyping(false);
        }
    };

    return (
        <AnimatePresence>
            {isOpen && (
                <motion.div
                    initial={{ opacity: 0, scale: 0.9, y: 20, x: 20 }}
                    animate={{ opacity: 1, scale: 1, y: 0, x: 0 }}
                    exit={{ opacity: 0, scale: 0.9, y: 20, x: 20 }}
                    className="fixed bottom-24 right-8 w-[400px] h-[580px] bg-background border border-border rounded-[2.5rem] shadow-2xl z-[110] flex flex-col overflow-hidden shadow-black/40"
                >
                    {/* Decorative Top Bar */}
                    <div className="h-1.5 w-full bg-gradient-to-r from-primary via-secondary to-accent" />

                    {/* Header */}
                    <div className="p-6 border-b border-border flex items-center justify-between bg-card/50 backdrop-blur-md">
                        <div className="flex items-center gap-3">
                            <div className="relative">
                                <img
                                    src="/assets/images/keep-up-fixed.svg"
                                    alt="Keep Up"
                                    className="h-6 w-auto nav-logo"
                                />
                                <div className="absolute -top-1 -right-1 w-2 h-2 bg-primary rounded-full animate-pulse" />
                            </div>
                            <div className="h-4 w-px bg-border mx-1" />
                            <span className="text-[10px] font-black uppercase tracking-[0.2em] text-primary">Neural Link</span>
                        </div>
                        <button
                            onClick={onClose}
                            className="p-2 text-muted-foreground hover:text-foreground hover:bg-foreground/5 rounded-xl transition-all"
                        >
                            <X size={18} />
                        </button>
                    </div>

                    {/* Messages Area */}
                    <div
                        ref={scrollRef}
                        className="flex-1 overflow-y-auto p-6 space-y-6 custom-scrollbar bg-[radial-gradient(circle_at_top_right,var(--primary-color-20),transparent)]"
                    >
                        {messages.map((notif) => (
                            <div
                                key={notif.id}
                                className={`flex ${notif.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                            >
                                <div className={`flex gap-3 max-w-[85%] ${notif.sender === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                                    <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 border ${notif.sender === 'user'
                                        ? 'bg-foreground/5 border-border'
                                        : 'bg-primary/10 border-primary/20'
                                        }`}>
                                        {notif.sender === 'user' ? <User size={14} /> : <Bot size={14} className="text-primary" />}
                                    </div>
                                    <div className={`space-y-1 ${notif.sender === 'user' ? 'text-right' : 'text-left'}`}>
                                        <div className={`p-4 rounded-2xl text-sm leading-relaxed ${notif.sender === 'user'
                                            ? 'bg-foreground text-background font-medium rounded-tr-none shadow-lg'
                                            : 'bg-card border border-border text-foreground rounded-tl-none shadow-sm'
                                            }`}>
                                            {notif.text}
                                        </div>
                                        <p className="text-[8px] font-black uppercase tracking-widest text-muted-foreground opacity-50">
                                            {notif.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        ))}
                        {isTyping && (
                            <div className="flex justify-start">
                                <div className="flex gap-3">
                                    <div className="w-8 h-8 rounded-full bg-primary/10 border border-primary/20 flex items-center justify-center">
                                        <Bot size={14} className="text-primary" />
                                    </div>
                                    <div className="p-4 bg-card border border-border rounded-2xl rounded-tl-none flex gap-1">
                                        <span className="w-1 h-1 bg-primary rounded-full animate-bounce [animation-delay:-0.3s]" />
                                        <span className="w-1 h-1 bg-primary rounded-full animate-bounce [animation-delay:-0.15s]" />
                                        <span className="w-1 h-1 bg-primary rounded-full animate-bounce" />
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>

                    {/* Input Area */}
                    <div className="p-6 border-t border-border bg-card/30">
                        <div className="relative flex items-center">
                            <input
                                type="text"
                                value={inputValue}
                                onChange={(e) => setInputValue(e.target.value)}
                                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                                placeholder="Query system protocol..."
                                className="w-full bg-background border border-border rounded-2xl px-5 py-4 text-sm focus:outline-none focus:border-primary/50 transition-all pr-14 shadow-inner"
                            />
                            <button
                                onClick={handleSend}
                                disabled={!inputValue.trim()}
                                className={`absolute right-2 p-3 rounded-xl transition-all ${inputValue.trim()
                                    ? 'bg-primary text-black hover:scale-105 shadow-lg shadow-primary/20'
                                    : 'text-muted-foreground opacity-20'
                                    }`}
                            >
                                <Send size={18} />
                            </button>
                        </div>
                        <div className="mt-3 flex items-center justify-center gap-2">
                            <Sparkles size={10} className="text-primary" />
                            <p className="text-[8px] font-black uppercase tracking-[0.3em] text-muted-foreground">Neural Matrix Active</p>
                        </div>
                    </div>
                </motion.div>
            )}
        </AnimatePresence>
    );
}

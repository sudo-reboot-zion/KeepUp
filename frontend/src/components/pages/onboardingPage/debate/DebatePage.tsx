'use client';

import { useEffect, useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { useAppSelector } from '@/redux/hooks';
import { ArrowRight } from 'lucide-react';
import type { AgentMessage } from '@/types/debate.types';
import DebateHeader from './components/DebateHeader';
import AgentMessageCard from './components/AgentMessageCard';
import TypingIndicator from './components/TypingIndicator';
import { buildMessageTimeline } from './utils/messageBuilder';

export default function DebatePage() {
    const router = useRouter();
    const { debateData, isComplete } = useAppSelector(state => state.onboarding);

    const [messages, setMessages] = useState<AgentMessage[]>([]);
    const [visibleMessages, setVisibleMessages] = useState<AgentMessage[]>([]);
    const [currentMessageIndex, setCurrentMessageIndex] = useState(0);
    const [isTyping, setIsTyping] = useState(false);
    const [debateComplete, setDebateComplete] = useState(false);

    const messagesEndRef = useRef<HTMLDivElement>(null);

    // Redirect if no debate data
    useEffect(() => {
        if (!isComplete || !debateData) {
            router.push('/onboarding');
        }
    }, [isComplete, debateData, router]);

    // Build message timeline
    useEffect(() => {
        if (!debateData) return;
        const timeline = buildMessageTimeline(debateData);
        setMessages(timeline);
    }, [debateData]);

    // Animate messages appearing one by one
    useEffect(() => {
        if (messages.length === 0 || currentMessageIndex >= messages.length) {
            if (currentMessageIndex >= messages.length && messages.length > 0) {
                setDebateComplete(true);
            }
            return;
        }

        setIsTyping(true);

        const currentMessage = messages[currentMessageIndex];
        // Faster typing for grid layout feel
        const typingDelay = Math.min(currentMessage.message.length * 10, 1500);

        const timer = setTimeout(() => {
            setIsTyping(false);
            setVisibleMessages(prev => [...prev, currentMessage]);
            setCurrentMessageIndex(prev => prev + 1);

            if (currentMessageIndex > 2) {
                messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
            }
        }, typingDelay);

        return () => clearTimeout(timer);
    }, [messages, currentMessageIndex]);

    if (!debateData) return null;

    return (
        <main className="min-h-screen bg-[var(--bg)] text-[var(--fg)] selection:bg-[var(--primary)] selection:text-[var(--bg)]">
            <div className="relative min-h-screen px-6 py-12 pb-40">
                <div className="max-w-7xl mx-auto space-y-16">
                    {/* Header */}
                    <DebateHeader />

                    {/* Seamless Grid Layout */}
                    <div className="border-t border-l border-[var(--border)] rounded-tl-3xl rounded-tr-3xl overflow-hidden">
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
                            {visibleMessages.map((msg) => (
                                <AgentMessageCard key={msg.id} message={msg} />
                            ))}

                            {/* Typing Indicator Cell */}
                            {isTyping && <TypingIndicator />}
                        </div>
                        <div ref={messagesEndRef} />
                    </div>

                    {/* Completion Action */}
                    {debateComplete && (
                        <div className="flex justify-center pt-12 pb-20">
                            <button
                                onClick={() => router.push('/onboarding/plan')}
                                className="bg-[var(--primary)] text-[var(--bg)] font-black text-xl px-10 py-5 rounded-full hover:scale-105 hover:shadow-[0_0_40px_var(--primary)] transition-all duration-300 flex items-center gap-3"
                            >
                                View Final Plan <ArrowRight className="w-6 h-6" />
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </main>
    );
}
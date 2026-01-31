'use client';

import React, { useState, useEffect, useRef } from 'react';
import { AnimatePresence } from 'framer-motion';
import { useRouter } from 'next/navigation';
import { Message, UserGoal } from './types';
import OnboardingHeader from './components/OnboardingHeader';
import MessageBubble from './components/MessageBubble';
import TypingIndicator from './components/TypingIndicator';
import OnboardingInput from './components/OnboardingInput';

import { sendOnboardingStep } from '@/lib/onboardingApi';

export default function ConversationalOnboarding() {
    const router = useRouter();
    const [messages, setMessages] = useState<Message[]>([]);
    const [inputValue, setInputValue] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const [extractedData, setExtractedData] = useState<Record<string, any>>({});
    const [isComplete, setIsComplete] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const hasInitialized = useRef(false);

    // Initial greeting
    useEffect(() => {
        if (hasInitialized.current) return;
        hasInitialized.current = true;

        const initialGreeting = async () => {
            setIsTyping(true);
            // We can even send an initial empty message to get the backend's preferred greeting
            try {
                const response = await sendOnboardingStep("START_ONBOARDING", {});
                addMessage({
                    text: response.message,
                    sender: 'agent'
                });
            } catch (error) {
                console.error('Onboarding Init Error:', error);
                addMessage({
                    text: "Hi there. I'm your personal health architect. I'm here to build a plan that adapts to your life. To get started, tell me: what is the one thing you want to change most right now?",
                    sender: 'agent'
                });
            }
        };

        initialGreeting();
    }, []);

    // Auto-scroll to bottom
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages, isTyping]);

    const addMessage = (msg: Omit<Message, 'id' | 'timestamp'>) => {
        const newMessage: Message = {
            id: Math.random().toString(36).substring(7),
            timestamp: new Date(),
            ...msg
        };
        setMessages(prev => [...prev, newMessage]);
        setIsTyping(false);
    };

    const handleSendMessage = async (text: string) => {
        if (!text.trim()) return;

        // Special handling for the final button
        if (isComplete && text === "Let's go") {
            addMessage({ text, sender: 'user' });
            setIsTyping(true);
            await new Promise(resolve => setTimeout(resolve, 1500));
            router.push('/dashboard');
            return;
        }

        // Add user message
        addMessage({ text, sender: 'user' });
        setInputValue('');

        // Process response
        setIsTyping(true);
        await processUserResponse(text);
    };

    const processUserResponse = async (text: string) => {
        try {
            const response = await sendOnboardingStep(text, extractedData);

            // Update extracted data from backend
            if (response.data) {
                const newData = { ...extractedData, ...response.data };
                setExtractedData(newData);

                // If backend identified the primary goal, store it
                if (newData.primary_goal && newData.primary_goal !== 'unknown') {
                    localStorage.setItem('userPrimaryCategory', newData.primary_goal);
                    localStorage.setItem('userSpecificGoal', newData.specific_goal || text);
                }
            }

            addMessage({
                text: response.message,
                sender: 'agent'
            });

            // If the chat agent thinks we're done (or close), show the dashboard option
            // Note: chat_agent response schema has 'data' containing confidence/etc.
            if (response.data?.conversation_complete) {
                setIsComplete(true);
                await new Promise(resolve => setTimeout(resolve, 1000));
                setIsTyping(true);
                await new Promise(resolve => setTimeout(resolve, 1000));

                addMessage({
                    text: "I've designed a custom dashboard based on our conversation. Ready to see your protocol?",
                    sender: 'agent',
                    type: 'options',
                    options: ["Let's go", "Tell me more first"]
                });
            }
        } catch (error) {
            console.error('Onboarding Sync Error:', error);
            addMessage({
                text: "My neural link is flickering. Could you repeat that?",
                sender: 'agent'
            });
            setIsTyping(false);
        }
    };

    return (
        <div className="min-h-screen bg-[var(--bg)] text-[var(--fg)] flex flex-col items-center justify-center p-4 relative overflow-hidden">
            {/* Background Elements */}
            <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
                <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-[var(--primary)] opacity-[0.03] blur-[100px] rounded-full" />
                <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-[var(--secondary)] opacity-[0.03] blur-[100px] rounded-full" />
            </div>

            <div className="w-full max-w-2xl flex flex-col h-[80vh] glass-card rounded-3xl relative z-10 shadow-2xl border border-[var(--border)]">
                <OnboardingHeader />

                {/* Chat Area */}
                <div className="flex-1 overflow-y-auto p-6 space-y-6 custom-scrollbar">
                    <AnimatePresence initial={false}>
                        {messages.map((msg) => (
                            <MessageBubble
                                key={msg.id}
                                message={msg}
                                onOptionClick={handleSendMessage}
                            />
                        ))}
                    </AnimatePresence>

                    {isTyping && <TypingIndicator />}

                    <div ref={messagesEndRef} />
                </div>

                <OnboardingInput
                    value={inputValue}
                    onChange={setInputValue}
                    onSubmit={() => handleSendMessage(inputValue)}
                    disabled={isTyping || (messages.length > 0 && messages[messages.length - 1].type === 'options')}
                />
            </div>
        </div>
    );
}

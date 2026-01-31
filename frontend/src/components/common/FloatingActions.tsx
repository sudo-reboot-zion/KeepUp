"use client"

import { useState, useEffect } from 'react';
import { usePathname } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowUp } from 'lucide-react';
import SolidLogo from './SolidLogo';
import AskAIChat from './AskAIChat';

const FloatingActions = () => {
    const [isScrollVisible, setIsScrollVisible] = useState(false);
    const [isChatOpen, setIsChatOpen] = useState(false);
    const pathname = usePathname();

    useEffect(() => {
        const checkScrollPosition = () => {
            const scrolled = window.scrollY > 300;
            setIsScrollVisible(scrolled);
        };

        window.addEventListener('scroll', checkScrollPosition);
        return () => window.removeEventListener('scroll', checkScrollPosition);
    }, []);

    const scrollToTop = () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    };

    if (pathname === '/login' || pathname === '/register') return null;

    return (
        <div className="fixed bottom-8 right-8 z-[100] flex flex-col items-end gap-4">
            <AskAIChat isOpen={isChatOpen} onClose={() => setIsChatOpen(false)} />

            {/* Scroll to Top Button */}
            <AnimatePresence>
                {isScrollVisible && (
                    <motion.button
                        onClick={scrollToTop}
                        initial={{ opacity: 0, scale: 0, y: 20 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0, y: 20 }}
                        whileHover={{ scale: 1.1 }}
                        whileTap={{ scale: 0.9 }}
                        className="bg-foreground/10 backdrop-blur-md text-foreground p-3 rounded-full shadow-2xl border border-foreground/20 transition-colors hover:bg-foreground hover:text-background"
                        aria-label="Scroll to top"
                    >
                        <ArrowUp size={20} />
                    </motion.button>
                )}
            </AnimatePresence>

            {/* Ask AI Button */}
            <motion.button
                onClick={() => setIsChatOpen(!isChatOpen)}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                whileHover={{ scale: 1.05, boxShadow: "0 0 25px rgba(255, 255, 255, 0.2)" }}
                whileTap={{ scale: 0.95 }}
                className="group relative flex items-center gap-3 bg-foreground/80 backdrop-blur-xl px-6 py-3 rounded-full border border-background/10 shadow-2xl overflow-hidden"
            >
                {/* Animated Gradient Background */}
                <div className="absolute inset-0 bg-gradient-to-r from-purple-500/10 via-blue-500/10 to-purple-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500" />

                {/* Logo / Icon */}
                <div className="relative w-6 h-6 flex items-center justify-center">
                    <SolidLogo className="w-6 h-6 text-background" />
                </div>

                {/* Text */}
                <span className="relative text-sm font-medium text-background tracking-wide">
                    {isChatOpen ? 'Close Link' : 'Ask AI'}
                </span>

                {/* Glow Effect */}
                <div className="absolute -inset-1 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full blur opacity-20 group-hover:opacity-40 transition duration-500" />
            </motion.button>
        </div>
    );
};

export default FloatingActions;

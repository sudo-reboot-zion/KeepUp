'use client';

import { useEffect, useRef } from 'react';
import Link from 'next/link';
import gsap from 'gsap';
import { MoveLeft, Home } from 'lucide-react';

export default function NotFound() {
    const containerRef = useRef<HTMLDivElement>(null);
    const contentRef = useRef<HTMLDivElement>(null);
    const glowRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const tl = gsap.timeline();

        tl.fromTo(contentRef.current,
            { y: 40, opacity: 0 },
            { y: 0, opacity: 1, duration: 1, ease: 'power4.out' }
        )
            .fromTo(glowRef.current,
                { scale: 0.8, opacity: 0 },
                { scale: 1, opacity: 0.15, duration: 2, ease: 'power2.out' },
                "-=0.5"
            );

        // Subtle floating animation for the glow
        gsap.to(glowRef.current, {
            y: "+=30",
            x: "+=20",
            duration: 4,
            repeat: -1,
            yoyo: true,
            ease: "sine.inOut"
        });
    }, []);

    return (
        <main
            ref={containerRef}
            className="min-h-screen bg-[var(--bg)] text-[var(--fg)] flex items-center justify-center px-6 relative overflow-hidden selection:bg-[var(--primary)] selection:text-[var(--bg)]"
        >
            {/* Ambient Background Glow */}
            <div
                ref={glowRef}
                className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-[var(--primary)] rounded-full blur-[150px] opacity-0 pointer-events-none z-0"
            />

            <div
                ref={contentRef}
                className="relative z-10 text-center space-y-12 max-w-2xl opacity-0"
            >
                {/* 404 Header */}
                <div className="space-y-4">
                    <h1 className="text-[12rem] md:text-[16rem] font-black leading-none tracking-tighter text-transparent bg-clip-text bg-gradient-to-b from-[var(--fg)] to-[var(--fg)]/20">
                        404
                    </h1>
                    <div className="h-1 w-24 bg-[var(--primary)] mx-auto rounded-full" />
                </div>

                {/* Message */}
                <div className="space-y-4">
                    <h2 className="text-3xl md:text-5xl font-bold tracking-tight">
                        Lost in the Protocol.
                    </h2>
                    <p className="text-[var(--fg)] opacity-60 text-lg md:text-xl max-w-md mx-auto leading-relaxed">
                        The page you&apos;re looking for has drifted off course or never existed in this timeline.
                    </p>
                </div>

                {/* Actions */}
                <div className="flex flex-col sm:flex-row items-center justify-center gap-6 pt-8">
                    <Link
                        href="/"
                        className="group flex items-center gap-3 px-8 py-4 bg-[var(--fg)] text-[var(--bg)] rounded-full font-bold text-lg hover:opacity-90 transition-all duration-300"
                    >
                        <Home className="w-5 h-5" />
                        Return to Base
                    </Link>

                    <button
                        onClick={() => window.history.back()}
                        className="flex items-center gap-2 text-[var(--fg)] opacity-60 hover:opacity-100 transition-all font-medium group"
                    >
                        <MoveLeft className="w-5 h-5 group-hover:-translate-x-1 transition-transform" />
                        Go Back
                    </button>
                </div>
            </div>

            {/* Decorative Grid (Optional, matches app aesthetic) */}
            <div className="absolute inset-0 z-0 opacity-10 pointer-events-none">
                <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:40px_40px]" />
            </div>
        </main>
    );
}


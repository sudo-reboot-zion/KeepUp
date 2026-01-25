"use client";

import React, { useRef } from 'react';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { useGSAP } from '@gsap/react';

const howItWorksData = [
    {
        id: "01",
        title: "Create Your Account",
        description: "Join the OptimalYou ecosystem by creating your personalized profile. This is your first step towards a data-driven health and fitness journey tailored to your unique needs.",
        icon: (
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
                <circle cx="9" cy="7" r="4" />
                <path d="M19 8v6M16 11h6" />
            </svg>
        )
    },
    {
        id: "02",
        title: "Define Your Resolution",
        description: "Set your yearly health and fitness goals. Whether it's gaining weight, losing weight, or building resilience, our AI helps you structure your path with precision.",
        icon: (
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M12 2v20M2 12h20" />
                <circle cx="12" cy="12" r="10" />
            </svg>
        )
    },
    {
        id: "03",
        title: "Daily Check-in",
        description: "Log your sleep quality, energy levels, and mood every morning. We translate these subjective markers into objective readiness scores to guide your daily activity.",
        icon: (
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M12 20h9M3 20h.01M7 20h.01M11 20h.01M15 20h.01M19 20h.01M3 10c0-3.87 3.13-7 7-7s7 3.13 7 7v10H3V10z" />
            </svg>
        )
    },
    {
        id: "04",
        title: "Adaptive Planning",
        description: "Receive a personalized workout plan that adapts in real-time. If your recovery is low, our agents automatically adjust the intensity to ensure sustainable progress without burnout.",
        icon: (
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8" />
                <path d="M21 3v5h-5" />
            </svg>
        )
    },
    {
        id: "05",
        title: "AI-Driven Insights",
        description: "Get deep insights into your behavioral patterns. Our agents analyze your adherence and provide proactive recommendations to keep you aligned with your optimal self.",
        icon: (
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z" />
                <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h9z" />
            </svg>
        )
    },
    {
        id: "06",
        title: "Community & Accountability",
        description: "Share your wins and challenges with a like-minded community. Leverage social accountability to stay motivated and celebrate every milestone on your journey.",
        icon: (
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                <circle cx="9" cy="7" r="4" />
                <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
                <path d="M16 3.13a4 4 0 0 1 0 7.75" />
            </svg>
        )
    }
];

const HowItWorks = () => {
    const sectionRef = useRef<HTMLDivElement>(null);
    const leftColRef = useRef<HTMLDivElement>(null);

    useGSAP(() => {
        gsap.registerPlugin(ScrollTrigger);

        if (sectionRef.current && leftColRef.current) {
            ScrollTrigger.create({
                trigger: sectionRef.current,
                start: "top top",
                end: "bottom bottom",
                pin: leftColRef.current,
                pinSpacing: false,
                scrub: true,
                // markers: true, // Uncomment for debugging
            });
        }
    }, { scope: sectionRef });

    return (
        <section ref={sectionRef} className="how-it-works-section py-32 bg-[var(--bg)] relative transition-colors duration-300">
            <div className="max-w-7xl mx-auto px-8 lg:px-16 flex flex-col lg:flex-row gap-20">
                {/* Left Column - Pinned by GSAP */}
                <div ref={leftColRef} className="lg:w-[42%] h-fit pt-8">
                    <h2 className="text-5xl md:text-6xl font-medium tracking-tight leading-[1.1] text-[var(--fg)] font-[family-name:var(--font-ppMontreal)] mb-8 transition-colors duration-300">
                        How it <br />
                        <span className="text-[var(--fg)]/60">Works.</span>
                    </h2>
                    <p className="text-xl text-[var(--fg)]/50 leading-relaxed font-medium mb-12 max-w-md transition-colors duration-300">
                        OptimalYou is more than just a tracker. It&apos;s an intelligent ecosystem designed to evolve with your ambitions.
                    </p>
                    <button className="group flex items-center gap-4 bg-[var(--fg)] text-[var(--bg)] px-8 py-3 rounded-full font-bold text-lg hover:opacity-90 transition-all duration-300">
                        Start Journey
                        <div className="bg-[var(--bg)] rounded-full p-2 group-hover:translate-x-1 transition-transform duration-300 flex items-center justify-center">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" className="text-[var(--fg)]">
                                <path d="M5 12h14M12 5l7 7-7 7" />
                            </svg>
                        </div>
                    </button>
                </div>

                {/* Right Column - Scrollable Cards */}
                <div className="lg:w-[58%] flex flex-col gap-8">
                    {howItWorksData.map((item) => (
                        <div key={item.id} className="how-it-works-card">
                            <div className="card-icon-wrapper">
                                {item.icon}
                            </div>
                            <div className="card-content">
                                <span className="card-number">{item.id}</span>
                                <h3 className="card-title">{item.title}</h3>
                                <p className="card-description">{item.description}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
};

export default HowItWorks;

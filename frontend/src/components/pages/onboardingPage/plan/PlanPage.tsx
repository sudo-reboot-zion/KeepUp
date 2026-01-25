'use client';

import { useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import gsap from 'gsap';
import { useAppSelector } from '@/redux/hooks';
import { ArrowRight } from 'lucide-react';
import PlanHeader from './components/PlanHeader';
import PlanCard from './components/PlanCard';
import StatsRow from './components/StatsRow';

import { generatePlanCards } from './utils/planCards';
import { apiRequest } from '@/lib/api';
import { Loader } from 'lucide-react';
import { useState } from 'react';

export default function PlanPage() {
    const router = useRouter();
    const { finalPlan, confidenceScore, isComplete, formData, debateData } = useAppSelector(state => state.onboarding);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const containerRef = useRef<HTMLDivElement>(null);

    // Redirect if no plan
    useEffect(() => {
        if (!isComplete || !finalPlan) {
            router.push('/onboarding');
        }
    }, [isComplete, finalPlan, router]);

    // Entrance animations
    useEffect(() => {
        if (!containerRef.current) return;

        const tl = gsap.timeline();

        tl.fromTo(
            '.plan-header',
            { y: 30, opacity: 0 },
            { y: 0, opacity: 1, duration: 0.8, ease: 'power3.out' }
        )
            .fromTo(
                '.plan-card',
                { y: 30, opacity: 0 },
                { y: 0, opacity: 1, duration: 0.6, stagger: 0.1, ease: 'power3.out' },
                '-=0.4'
            )
            .fromTo(
                '.plan-cta',
                { y: 20, opacity: 0 },
                { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' },
                '-=0.2'
            );
    }, []);

    const handleInitiateProtocol = async () => {
        if (!finalPlan || isSubmitting) return;

        try {
            setIsSubmitting(true);
            setError(null);

            await apiRequest('/resolution/confirm', {
                method: 'POST',
                body: JSON.stringify({
                    resolution_text: formData.resolution_text,
                    past_attempts: formData.past_attempts,
                    life_constraints: formData.life_constraints,
                    final_plan: finalPlan,
                    debate_summary: debateData,
                    confidence_score: confidenceScore,
                    occupation: formData.occupation,
                    occupation_details: formData.occupation_details
                })
            });

            router.push('/dashboard');
        } catch (err) {
            console.error('Failed to confirm resolution:', err);
            setError('Failed to initiate protocol. Please try again.');
            setIsSubmitting(false);
        }
    };

    if (!finalPlan) {
        return null;
    }

    const cards = generatePlanCards(finalPlan);

    return (
        <main className="min-h-screen bg-[var(--bg)] text-[var(--fg)] selection:bg-[var(--primary)] selection:text-[var(--bg)]">
            <div ref={containerRef} className="max-w-7xl mx-auto px-6 py-24">
                {/* Header */}
                <PlanHeader />

                {/* Grid Layout */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-1 mb-40">
                    {cards.map((card, index) => (
                        <PlanCard
                            key={index}
                            icon={card.icon}
                            title={card.title}
                            description={card.description}
                        />
                    ))}
                </div>

                {/* Stats Row */}
                <StatsRow confidenceScore={confidenceScore} finalPlan={finalPlan} />

                {/* CTA */}
                <div className="flex flex-col items-center justify-center plan-cta">
                    {error && (
                        <p className="text-red-500 mb-4">{error}</p>
                    )}
                    <button
                        onClick={handleInitiateProtocol}
                        disabled={isSubmitting}
                        className="group relative inline-flex items-center gap-3 px-12 py-6 bg-[var(--fg)] text-[var(--bg)] rounded-full text-xl font-bold tracking-wide hover:scale-105 transition-all duration-300 disabled:opacity-50 disabled:hover:scale-100"
                    >
                        {isSubmitting ? (
                            <>
                                <Loader className="w-6 h-6 animate-spin" />
                                <span>Initiating...</span>
                            </>
                        ) : (
                            <>
                                <span>Initiate Protocol</span>
                                <ArrowRight className="w-6 h-6 group-hover:translate-x-1 transition-transform" />
                            </>
                        )}
                    </button>
                </div>
            </div>
        </main>
    );
}

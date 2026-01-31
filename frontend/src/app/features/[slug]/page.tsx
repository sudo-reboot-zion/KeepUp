'use client';

import { useParams } from 'next/navigation';
import { useEffect, useRef } from 'react';
import gsap from 'gsap';
import { getFeatureBySlug } from '@/lib/features-data';
import ReactNav from '@/components/layouts/Navbar';
import Footer from '@/components/layouts/Footer';
import {
    Target, TrendingUp, Calendar, Zap, Apple, Calculator, BookOpen, Clock,
    Moon, Activity, Heart, BarChart, Users, MessageCircle, Trophy, Sparkles,
    ArrowRight
} from 'lucide-react';


const iconMap: Record<string, any> = {
    Target, TrendingUp, Calendar, Zap, Apple, Calculator, BookOpen, Clock,
    Moon, Activity, Heart, BarChart, Users, MessageCircle, Trophy, Sparkles
};

export default function FeatureDetailPage() {
    const params = useParams();
    const slug = params.slug as string;
    const feature = getFeatureBySlug(slug);
    const heroRef = useRef<HTMLDivElement>(null);
    const containerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (heroRef.current && containerRef.current) {
            const tl = gsap.timeline();
            tl.fromTo(heroRef.current.querySelector('h1'),
                { y: 30, opacity: 0 },
                { y: 0, opacity: 1, duration: 1.2, ease: 'power4.out' }
            ).fromTo(heroRef.current.querySelector('p'),
                { y: 20, opacity: 0 },
                { y: 0, opacity: 1, duration: 1, ease: 'power3.out' },
                '-=0.8'
            ).fromTo(containerRef.current,
                { y: 40, opacity: 0 },
                { y: 0, opacity: 1, duration: 1, ease: 'power3.out' },
                '-=0.6'
            );
        }
    }, []);

    if (!feature) {
        return (
            <div className="min-h-screen bg-[var(--bg)] text-[var(--fg)] flex items-center justify-center">
                <div className="text-center">
                    <h1 className="text-4xl font-bold mb-4">Feature Not Found</h1>
                    <p className="text-[var(--fg)]/60">The feature you're looking for doesn't exist.</p>
                </div>
            </div>
        );
    }

    return (
        <>
            <div className="min-h-screen bg-[var(--bg)] text-[var(--fg)] transition-colors duration-300">
                <ReactNav containerRef={containerRef} />

                {/* Hero Section with Background Image */}
                <div
                    ref={heroRef}
                    className="relative h-[60vh] min-h-[500px] flex items-center justify-center overflow-hidden"
                    style={{
                        backgroundImage: `url(${feature.hero_image})`,
                        backgroundSize: 'cover',
                        backgroundPosition: 'center',
                    }}
                >
                    {/* Overlay for better text readability */}
                    <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" />

                    <div className="relative z-10 text-center px-6 max-w-4xl">
                        <h1 className="text-5xl md:text-7xl font-[var(--font-sfBold)] tracking-tight mb-6 text-white">
                            {feature.title}
                        </h1>
                        <p className="text-xl md:text-2xl text-white/90 font-[var(--font-ppMontreal)]">
                            {feature.subtitle}
                        </p>
                    </div>
                </div>

                {/* Content Sections */}
                <div ref={containerRef} className="max-w-6xl mx-auto px-6 py-20">
                    {feature.sections.map((section, index) => {
                        // Intro Section
                        if (section.type === 'intro') {
                            return (
                                <div key={index} className="mb-24">
                                    <h2 className="text-4xl md:text-5xl font-[var(--font-sfBold)] mb-6 text-[var(--fg)]">
                                        {section.heading}
                                    </h2>
                                    <p className="text-lg md:text-xl text-[var(--fg)]/70 leading-relaxed font-[var(--font-ppMontreal)]">
                                        {section.content}
                                    </p>
                                </div>
                            );
                        }

                        // Features/Benefits Grid
                        if (section.type === 'features' || section.type === 'benefits') {
                            return (
                                <div key={index} className="mb-24">
                                    <h2 className="text-3xl md:text-4xl font-[var(--font-sfBold)] mb-12 text-center text-[var(--fg)]">
                                        {section.heading}
                                    </h2>
                                    <div className="grid md:grid-cols-2 gap-8">
                                        {section.items?.map((item, itemIndex) => {
                                            const Icon = item.icon ? iconMap[item.icon] : null;
                                            return (
                                                <div
                                                    key={itemIndex}
                                                    className="bg-[var(--card)] border border-[var(--border)] rounded-2xl p-8 hover:border-[var(--primary)] transition-all duration-300 hover:shadow-lg hover:shadow-[var(--primary)]/10"
                                                >
                                                    {Icon && (
                                                        <div className="w-12 h-12 rounded-xl bg-[var(--primary)]/10 flex items-center justify-center mb-4">
                                                            <Icon className="w-6 h-6 text-[var(--primary)]" />
                                                        </div>
                                                    )}
                                                    <h3 className="text-xl font-[var(--font-sfBold)] mb-3 text-[var(--fg)]">
                                                        {item.title}
                                                    </h3>
                                                    <p className="text-[var(--fg)]/70 leading-relaxed">
                                                        {item.description}
                                                    </p>
                                                </div>
                                            );
                                        })}
                                    </div>
                                </div>
                            );
                        }

                        // How It Works Timeline
                        if (section.type === 'how-it-works') {
                            return (
                                <div key={index} className="mb-24">
                                    <h2 className="text-3xl md:text-4xl font-[var(--font-sfBold)] mb-12 text-center text-[var(--fg)]">
                                        {section.heading}
                                    </h2>
                                    <div className="space-y-6">
                                        {section.items?.map((item, itemIndex) => (
                                            <div
                                                key={itemIndex}
                                                className="flex gap-6 items-start bg-[var(--card)] border border-[var(--border)] rounded-2xl p-6 hover:border-[var(--primary)] transition-all duration-300"
                                            >
                                                <div className="flex-shrink-0 w-12 h-12 rounded-full bg-[var(--primary)] flex items-center justify-center text-white font-bold">
                                                    {itemIndex + 1}
                                                </div>
                                                <div>
                                                    <h3 className="text-xl font-[var(--font-sfBold)] mb-2 text-[var(--fg)]">
                                                        {item.title}
                                                    </h3>
                                                    <p className="text-[var(--fg)]/70 leading-relaxed">
                                                        {item.description}
                                                    </p>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            );
                        }

                        // CTA Section
                        if (section.type === 'cta') {
                            return (
                                <div key={index} className="text-center bg-gradient-to-br from-[var(--primary)]/10 to-[var(--primary)]/5 border border-[var(--primary)]/20 rounded-3xl p-12 md:p-16">
                                    <h2 className="text-3xl md:text-4xl font-[var(--font-sfBold)] mb-6 text-[var(--fg)]">
                                        {section.heading}
                                    </h2>
                                    <p className="text-lg md:text-xl text-[var(--fg)]/70 mb-8 max-w-2xl mx-auto">
                                        {section.content}
                                    </p>
                                    <button className="bg-[var(--primary)] text-white px-8 py-4 rounded-full font-[var(--font-sfBold)] text-lg hover:bg-[var(--primary)]/90 transition-all duration-300 hover:scale-105 inline-flex items-center gap-2">
                                        Get Started
                                        <ArrowRight className="w-5 h-5" />
                                    </button>
                                </div>
                            );
                        }

                        return null;
                    })}
                </div>
            </div>
            <Footer />
        </>
    );
}

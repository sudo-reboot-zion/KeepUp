"use client";
import React from 'react'
import { stickyCardsData } from '@/lib/data';
import Link from 'next/link';
import { ArrowUpRight } from 'lucide-react';

const StickyCard = () => {
    return (
        <section className="sticky-cards-section py-20">
            <div className="max-w-7xl mx-auto px-8 lg:px-16 mb-16 flex justify-between items-end">
                <h2 className="text-5xl md:text-6xl lg:text-7xl font-medium tracking-tight leading-[1.1] text-[var(--fg)] font-[family-name:var(--font-ppMontreal)] transition-colors duration-300">
                    Keep up with <br />
                    <span className="text-[var(--fg)]/90">the latest on OptimalYou</span>
                </h2>
                <div className="hidden md:flex gap-4 mb-4">
                    <div className="w-12 h-12 rounded-full border border-[var(--fg)]/20 flex items-center justify-center cursor-pointer hover:bg-[var(--fg)]/10 transition-colors">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="m15 18-6-6 6-6" /></svg>
                    </div>
                    <div className="w-12 h-12 rounded-full border border-[var(--fg)]/20 flex items-center justify-center cursor-pointer hover:bg-[var(--fg)]/10 transition-colors">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="m9 18 6-6-6-6" /></svg>
                    </div>
                </div>
            </div>

            <div className="sticky-cards-grid">
                {stickyCardsData.map((cardData, index) => {
                    return (
                        <Link
                            key={index}
                            href={`/features/${cardData.slug}`}
                            className="grid-card group/card"
                        >
                            <div className="grid-card-inner">
                                <div className="grid-card-image-container">
                                    <img src={cardData.image} alt={cardData.title} className="grid-card-image transition-transform duration-700 group-hover/card:scale-110" />
                                    <div className="grid-card-image-overlay">
                                        <h2 className="image-overlay-text">{cardData.title.split(' ').join('\n')}</h2>
                                    </div>
                                    <div className="absolute top-6 right-6 p-3 rounded-full bg-white/10 backdrop-blur-md opacity-0 group-hover/card:opacity-100 transition-all duration-300 translate-y-2 group-hover/card:translate-y-0">
                                        <ArrowUpRight className="text-white w-6 h-6" />
                                    </div>
                                </div>

                                <div className="grid-card-details">
                                    <div className="grid-card-text">
                                        <h2 className="grid-card-title group-hover/card:text-[var(--primary)] transition-colors">{cardData.title}</h2>
                                        <p className="grid-card-description">{cardData.description}</p>
                                    </div>

                                    <div className="grid-card-button flex items-center gap-2">
                                        Explore Feature
                                        {/* <ArrowUpRight size={18} className="transition-transform group-hover/card:translate-x-1 group-hover/card:-translate-y-1" /> */}
                                    </div>
                                </div>
                            </div>
                        </Link>
                    )
                })}
            </div>
        </section>
    )
}

export default StickyCard
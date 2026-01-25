import React from 'react';
import PrimaryButton from '../../common/PrimaryButton';
function HeroSection() {
    return (
        <section className="relative w-full h-screen flex items-center overflow-hidden bg-[var(--bg)] transition-colors duration-300">
            {/* Background Image with Overlay */}
            <div
                className="absolute inset-0 z-0 bg-cover bg-center bg-no-repeat opacity-60 transition-all duration-500 dark:filter-none invert"
                style={{ backgroundImage: "url('/assets/images/web-bg-3.svg')" }}
            />
            <div className="absolute inset-0 z-[1] bg-gradient-to-r from-[var(--bg)] via-[var(--bg)]/40 to-transparent transition-colors duration-300" />

            {/* Content */}
            <div className="relative z-10 max-w-7xl mx-auto px-8 lg:px-16 w-full pt-64">
                <div className="max-w-4xl">
                    <h1 className="text-5xl md:text-7xl lg:text-8xl font-bold tracking-tight leading-[1.05] mb-8 text-[var(--fg)] transition-colors duration-300">
                        The ultimate platform <br />
                        <span className="text-[var(--fg)]/90">for your optimal self.</span>
                    </h1>

                    <p className="text-lg md:text-xl text-[var(--fg)]/70 max-w-xl mb-12 leading-relaxed font-medium transition-colors duration-300">
                        Unlock your potential with AI-driven insights, personalized wellness plans,
                        and a community dedicated to growth. Everywhere you grow.
                    </p>

                    <PrimaryButton href="/register" className="px-6 py-2 text-base">
                        Get started
                    </PrimaryButton>
                </div>
            </div>
        </section>
    );
}

export default HeroSection;
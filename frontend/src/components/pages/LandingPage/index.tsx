"use client";

import ReactNav from '@/components/layouts/Navbar';
import React, { useRef } from 'react';

import Footer from '@/components/layouts/Footer';
import ReactLenis from 'lenis/react';
import StickyCard from '@/components/cards/StickyCard';
import HeroSection from './HeroSection';
import HowItWorks from './HowItWorks';



const LandingPage = () => {
  const containerRef = useRef<HTMLDivElement>(null);

  return (
    <>
      <ReactLenis root />
      <div className="react-nav-wrapper overflow-x-hidden bg-[var(--bg)] text-[var(--fg)] transition-colors duration-300">
        <ReactNav containerRef={containerRef} />

        <div ref={containerRef}>
          <HeroSection />
          <HowItWorks />
          <StickyCard />
        </div>

      </div>
      <Footer />
    </>
  );
};

export default LandingPage;
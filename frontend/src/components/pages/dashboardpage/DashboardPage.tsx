'use client';

import React from 'react';
import AppSidebar from '@/components/layout/AppSidebar';
import TopBar from '@/components/layout/TopBar';

/**
 * DashboardPage - Simplified "Blank" Dashboard.
 * Focuses on high-level status and navigation rather than the full protocol.
 */
export default function DashboardPage() {
  return (
    <div className="flex h-screen bg-background overflow-hidden transition-colors duration-300">
      <AppSidebar />

      <div className="flex-1 flex flex-col min-w-0">
        <TopBar />

        <main className="flex-1 p-8">
          <div className="max-w-4xl mx-auto">
            <div className="flex flex-col items-center justify-center h-[60vh] border border-dashed border-border rounded-[2.5rem] bg-card/50">
              <h1 className="text-4xl font-black text-foreground tracking-tighter uppercase mb-4">Command Center</h1>
              <p className="text-muted-foreground text-lg text-center max-w-md">
                Protocol initialized. Welcome to your personalized dashboard.
                Full schedule available in the <span className="text-primary font-bold">Schedule</span> tab.
              </p>

              <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6 w-full px-12">
                {[
                  { label: "Today's Status", value: "Ready" },
                  { label: "Current Phase", value: "Foundation" },
                  { label: "Week Progress", value: "0/3" }
                ].map((stat, i) => (
                  <div key={i} className="p-6 border border-border bg-background rounded-2xl">
                    <p className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest mb-1">{stat.label}</p>
                    <p className="text-xl font-black text-foreground uppercase">{stat.value}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
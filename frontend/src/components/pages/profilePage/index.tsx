'use client';

import React, { useState } from 'react';
import { useAppSelector } from '@/redux/hooks';
import AppSidebar from '@/components/layout/AppSidebar';
import TopBar from '@/components/layout/TopBar';
import ProfileHeader from './ProfileHeader';
import { User, Zap } from 'lucide-react';

/**
 * ProfilePage - Minimal Identity Hub.
 * Focused on core user attributes: Username, Resolution, and Streak.
 */
export default function ProfilePage() {
  const { user } = useAppSelector(state => state.auth);

  // Mock stats - focusing on the streak for the simplified profile
  const [stats] = useState({
    currentStreak: 7,
  });

  if (!user) {
    return (
      <div className="flex h-screen bg-background overflow-hidden transition-colors duration-300">
        <AppSidebar />
        <div className="flex-1 flex flex-col min-w-0">
          <TopBar />
          <main className="flex-1 flex items-center justify-center">
            <div className="text-center p-8 border border-dashed border-border rounded-[2.5rem] bg-card/50">
              <User size={48} className="mx-auto mb-4 text-muted-foreground opacity-20" />
              <h2 className="text-xl font-black text-foreground uppercase tracking-tight mb-2">Unauthorized Access</h2>
              <p className="text-muted-foreground text-sm max-w-xs">Please initialize your session to view sensitive protocol data.</p>
            </div>
          </main>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-background overflow-hidden transition-colors duration-300 font-[var(--font-sfReg)]">
      <AppSidebar />

      <div className="flex-1 flex flex-col min-w-0">
        <TopBar />

        <main className="flex-1 overflow-y-auto custom-scrollbar bg-card/5">
          <div className="max-w-4xl mx-auto px-8 py-16 space-y-12">

            {/* Minimal Identity Section */}
            <div className="bg-background border border-border rounded-[3rem] overflow-hidden shadow-2xl shadow-black/20">
              <ProfileHeader
                displayName={user.display_name}
                username={user.username}
                resolution={user.resolution || null}
              />

              {/* Basic Stats Bar - Integrated at bottom of header card */}
              <div className="flex items-center justify-center gap-16 py-10 border-t border-border bg-foreground/[0.02]">
                <div className="text-center space-y-1">
                  <p className="text-[10px] font-black text-muted-foreground uppercase tracking-[0.2em]">Active Streak</p>
                  <div className="flex items-center justify-center gap-2">
                    <Zap size={20} className="text-primary" />
                    <span className="text-4xl font-black text-foreground uppercase tracking-tight">{stats.currentStreak} Days</span>
                  </div>
                </div>
                <div className="h-10 w-px bg-border hidden sm:block" />
                <div className="text-center space-y-1">
                  <p className="text-[10px] font-black text-muted-foreground uppercase tracking-[0.2em]">Protocol Status</p>
                  <p className="text-2xl font-black text-primary uppercase tracking-tight">Optimized</p>
                </div>
              </div>
            </div>

            {/* Motivational Quote / Bio Segment */}
            <div className="px-12 text-center space-y-4">
              <p className="text-lg text-muted-foreground leading-relaxed italic opacity-60">
                "Protocol integrity maintained at 98.4%. Your trajectory remains within optimal biological parameters."
              </p>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
'use client';

import { useState, useRef } from 'react';
import { useAppSelector } from '@/redux/hooks';
import Navbar from '@/components/layouts/Navbar';
import { createLifeEvent } from '@/lib/lifeEventsApi';
import ProfileHeader from './ProfileHeader';
import ProfileQuickLinks from './ProfileQuickLinks';
import ProfileInfo from './ProfileInfo';
import ProfileStats from './ProfileStats';
import ProfilePreferences from './ProfilePreferences';
import ProfileEmail from './ProfileEmail';
import LifeEventForm, { LifeEventData } from './LifeEventForm';

// Subcomponents


export default function ProfilePage() {
  const { user } = useAppSelector(state => state.auth);
  const containerRef = useRef<HTMLDivElement>(null);
  const [showLifeEventForm, setShowLifeEventForm] = useState(false);

  // Mock stats - in a real app these would come from an API or Redux
  const [stats] = useState({
    currentStreak: 7,
    totalCheckIns: 42,
    milestonesEarned: 12,
  });

  const handleLifeEventSubmit = async (data: LifeEventData) => {
    try {
      await createLifeEvent(data);
      setShowLifeEventForm(false);
    } catch (error) {
      console.error('Failed to save life event:', error);
    }
  };

  if (!user) {
    return (
      <main className="min-h-screen bg-[var(--bg)] text-[var(--fg)] flex items-center justify-center">
        <Navbar containerRef={containerRef} />
        <div className="text-center">
          <p className="text-[var(--muted)]">Please log in to view your profile</p>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-[var(--bg)] text-[var(--fg)] pb-24 selection:bg-[var(--primary)] selection:text-[var(--bg)] font-[var(--font-ppMontreal)]">
      <Navbar containerRef={containerRef} />

      <div ref={containerRef} className="max-w-5xl mx-auto px-6 pt-32 space-y-px bg-[var(--border)] border-x border-[var(--border)]">

        <ProfileHeader
          displayName={user.display_name}
          username={user.username}
          resolution={user.resolution || null}
        />

        <ProfileQuickLinks />

        <ProfileInfo
          resolution={user.resolution || null}
          occupation={user.occupation || null}
        />

        <div className="grid md:grid-cols-2 bg-[var(--bg)] border-b border-[var(--border)]">
          <ProfileStats stats={stats} />
          <ProfilePreferences onRecordEvent={() => setShowLifeEventForm(true)} />
        </div>

        <ProfileEmail email={user.email} />

        {showLifeEventForm && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-6 bg-[var(--bg)]/80 backdrop-blur-sm">
            <div className="w-full max-w-2xl">
              <LifeEventForm
                onSubmit={handleLifeEventSubmit}
                onCancel={() => setShowLifeEventForm(false)}
              />
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
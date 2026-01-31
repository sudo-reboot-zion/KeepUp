'use client';

import React, { useState } from 'react';
import { useAppSelector } from '@/redux/hooks';
import AppSidebar from '@/components/layout/AppSidebar';
import TopBar from '@/components/layout/TopBar';
import ProfilePreferences from '../profilePage/ProfilePreferences';
import ProfileEmail from '../profilePage/ProfileEmail';
import ProfileQuickLinks from '../profilePage/ProfileQuickLinks';
import LifeEventForm, { LifeEventData } from '../profilePage/LifeEventForm';
import { createLifeEvent } from '@/lib/lifeEventsApi';
import { Settings as SettingsIcon, Shield, Bell, User, Zap } from 'lucide-react';

/**
 * SettingsPage - System Configuration Hub.
 * Houses preferences, security, and advanced protocol logs.
 */
export default function SettingsPage() {
    const { user } = useAppSelector(state => state.auth);
    const [showLifeEventForm, setShowLifeEventForm] = useState(false);

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
            <div className="flex h-screen bg-background overflow-hidden transition-colors duration-300">
                <AppSidebar />
                <div className="flex-1 flex flex-col min-w-0">
                    <TopBar />
                    <main className="flex-1 flex items-center justify-center">
                        <div className="text-center p-8 border border-dashed border-border rounded-[2.5rem] bg-card/50">
                            <User size={48} className="mx-auto mb-4 text-muted-foreground opacity-20" />
                            <h2 className="text-xl font-black text-foreground uppercase tracking-tight mb-2">Access Denied</h2>
                            <p className="text-muted-foreground text-sm max-w-xs">Authentication required to modify system parameters.</p>
                        </div>
                    </main>
                </div>
            </div>
        );
    }

    return (
        <div className="flex h-screen bg-background overflow-hidden transition-colors duration-300">
            <AppSidebar />

            <div className="flex-1 flex flex-col min-w-0">
                <TopBar />

                <main className="flex-1 overflow-y-auto custom-scrollbar bg-card/5">
                    <div className="max-w-4xl mx-auto px-8 py-10 space-y-10">

                        {/* Header Section */}
                        <div className="flex items-center justify-between">
                            <div>
                                <h1 className="text-3xl font-black text-foreground tracking-tighter uppercase">System Settings</h1>
                                <p className="text-sm text-muted-foreground">Configure your protocol preferences and security parameters.</p>
                            </div>
                            <SettingsIcon size={32} className="text-primary/20" />
                        </div>

                        <div className="grid grid-cols-1 gap-10">
                            {/* Preferences Section */}
                            <section className="bg-background border border-border rounded-[2.5rem] p-10 shadow-xl shadow-black/10">
                                <ProfilePreferences onRecordEvent={() => setShowLifeEventForm(true)} />
                            </section>

                            {/* Security & Authentication */}
                            <section className="bg-background border border-border rounded-[2.5rem] p-10 shadow-xl shadow-black/10 space-y-8">
                                <div className="flex items-center gap-3 border-b border-border pb-4">
                                    <Shield size={18} className="text-primary" />
                                    <h2 className="text-xs font-black uppercase tracking-widest text-foreground">Identity & Security</h2>
                                </div>
                                <ProfileEmail email={user.email} />
                            </section>

                            {/* Quick Connectivity */}
                            <section className="bg-background border border-border rounded-[2.5rem] p-10 shadow-xl shadow-black/10 space-y-6">
                                <div className="flex items-center gap-3 border-b border-border pb-4">
                                    <Zap size={18} className="text-secondary" />
                                    <h2 className="text-xs font-black uppercase tracking-widest text-foreground">Global Navigation</h2>
                                </div>
                                <ProfileQuickLinks />
                            </section>
                        </div>

                        {/* Footer Metadata */}
                        <div className="pt-10 border-t border-border flex justify-between items-center opacity-30">
                            <p className="text-[10px] font-mono uppercase tracking-[0.2em]">Config_Ver: 1.0.42_A</p>
                            <p className="text-[10px] font-mono uppercase tracking-[0.2em]">Secure_Link: Established</p>
                        </div>
                    </div>
                </main>
            </div>

            {showLifeEventForm && (
                <div className="fixed inset-0 z-[100] flex items-center justify-center p-6">
                    <div className="absolute inset-0 bg-black/80 backdrop-blur-md transition-opacity duration-300" onClick={() => setShowLifeEventForm(false)} />
                    <div className="relative w-full max-w-2xl bg-background border border-border rounded-[2.5rem] p-10 shadow-2xl animate-in zoom-in-95 duration-200">
                        <LifeEventForm
                            onSubmit={handleLifeEventSubmit}
                            onCancel={() => setShowLifeEventForm(false)}
                        />
                    </div>
                </div>
            )}
        </div>
    );
}

'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
    Dumbbell,
    Moon,
    Brain,
    Zap,
    Activity,
    Calendar,
    MessageSquare,
    ChevronRight,
    Play,
    Leaf,
    Coffee,
    Search,
    MoreHorizontal,
    Heart
} from 'lucide-react';
import { cn } from '@/lib/utils';
import AppSidebar from '@/components/layouts/AppSidebar';
import RightSidebar from './components/RightSidebar';

// Mock Data (Replace with real data later)
let MOCK_USER = {
    name: 'Gee',
    primaryGoal: 'fitness', // fitness, sleep, stress, wellness
    streak: 12,
    nextWorkout: 'Upper Body Power',
    sleepScore: 78,
    stressLevel: 'moderate'
};

const GOAL_CONFIG = {
    fitness: {
        icon: Dumbbell,
        title: "Sharpen Your Body with Professional Workouts",
        description: "Focus on compound movements today. Your recovery score is high.",
        action: "Join Now",
        color: "var(--primary)",
        agent: "Drill Sergeant"
    },
    sleep: {
        icon: Moon,
        title: "Master Your Sleep with Guided Routines",
        description: "Your sleep score was 78% last night. Let's aim for 8 hours.",
        action: "Start Sleep",
        color: "var(--secondary)",
        agent: "Dr. AI"
    },
    stress: {
        icon: Leaf,
        title: "Find Your Peace with Mindfulness",
        description: "Stress levels are moderate. A 10-minute breathing exercise will help.",
        action: "Start Calm",
        color: "var(--accent)",
        agent: "Zen Master"
    },
    wellness: {
        icon: Activity,
        title: "Optimize Vitality with Daily Checks",
        description: "Maintain your energy streak. A light active recovery session.",
        action: "Check In",
        color: "var(--primary)",
        agent: "Chef"
    }
};

const PROGRESS_CARDS = [
    { title: 'Morning Routine', count: '2/8', label: 'steps', icon: Zap, color: 'bg-purple-100 text-purple-600' },
    { title: 'Hydration', count: '3/8', label: 'cups', icon: Coffee, color: 'bg-pink-100 text-pink-600' },
    { title: 'Mindfulness', count: '6/12', label: 'mins', icon: Brain, color: 'bg-blue-100 text-blue-600' },
];

const RECOMMENDED_ITEMS = [
    { title: "Beginner's Guide to HIIT", category: "FITNESS", author: "Drill Sergeant", image: "bg-orange-100" },
    { title: "Optimizing Sleep Patterns", category: "SLEEP", author: "Dr. AI", image: "bg-indigo-100" },
    { title: "Reviving Mental Clarity", category: "WELLNESS", author: "Zen Master", image: "bg-green-100" },
];

export default function DynamicDashboard() {
    const [displayGoal, setDisplayGoal] = useState(MOCK_USER.primaryGoal);

    useEffect(() => {
        // Load specific goal from storage (simulating backend)
        if (typeof window !== 'undefined') {
            const category = localStorage.getItem('userPrimaryCategory');
            if (category) {
                MOCK_USER.primaryGoal = category;
                setDisplayGoal(category);
            }
        }
    }, []);

    const activeConfig = GOAL_CONFIG[displayGoal as keyof typeof GOAL_CONFIG] || GOAL_CONFIG.wellness;

    // Agents list for RightSidebar
    const agents = [
        { name: 'Drill Sergeant', role: 'Workout', icon: Dumbbell },
        { name: 'Dr. AI', role: 'Recovery', icon: Activity },
        { name: 'Chef', role: 'Nutrition', icon: Calendar },
        { name: 'Zen Master', role: 'Mindset', icon: Brain },
    ].sort((a, b) => (a.name === activeConfig.agent ? -1 : b.name === activeConfig.agent ? 1 : 0));

    return (
        <div className="min-h-screen bg-[var(--bg)] text-[var(--fg)] flex font-[family-name:var(--font-ppMontreal)]">
            <AppSidebar />

            {/* Main Content Area */}
            <div className="flex-1 flex flex-col h-screen overflow-y-auto pb-20 md:pb-0 px-8 py-6">
                {/* Search Bar */}
                <div className="w-full max-w-2xl mb-8">
                    <div className="relative">
                        <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
                        <input
                            type="text"
                            placeholder="Search your health plan..."
                            className="w-full bg-white border border-gray-100 rounded-2xl py-4 pl-12 pr-4 shadow-sm focus:outline-none focus:ring-2 focus:ring-[var(--primary)]/20 text-sm"
                        />
                    </div>
                </div>

                {/* Hero Banner (Purple Gradient) */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="w-full rounded-[2.5rem] bg-gradient-to-r from-[#8B5CF6] to-[#7C3AED] text-white p-10 relative overflow-hidden mb-10 shadow-xl shadow-purple-200"
                >
                    {/* Decorative Stars */}
                    <div className="absolute top-10 right-20 text-purple-300 opacity-50">
                        <svg width="40" height="40" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0L14 10L24 12L14 14L12 24L10 14L0 12L10 10z" /></svg>
                    </div>
                    <div className="absolute bottom-10 left-1/2 text-purple-400 opacity-30">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0L14 10L24 12L14 14L12 24L10 14L0 12L10 10z" /></svg>
                    </div>

                    <div className="relative z-10 max-w-xl">
                        <span className="inline-block px-3 py-1 rounded-full bg-white/20 text-xs font-bold mb-4 uppercase tracking-wider backdrop-blur-sm">
                            {displayGoal}
                        </span>
                        <h1 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">
                            {activeConfig.title}
                        </h1>
                        <button
                            onClick={() => alert(`Starting: ${activeConfig.title}`)}
                            className="bg-black text-white px-8 py-3 rounded-full font-bold flex items-center gap-2 hover:scale-105 transition-transform"
                        >
                            {activeConfig.action}
                            <div className="bg-white/20 rounded-full p-1">
                                <ChevronRight size={14} />
                            </div>
                        </button>
                    </div>
                </motion.div>

                {/* Progress Row */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
                    {PROGRESS_CARDS.map((card, idx) => (
                        <motion.div
                            key={idx}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.1 + idx * 0.1 }}
                            className="bg-white border border-gray-100 p-4 rounded-2xl flex items-center justify-between shadow-sm hover:shadow-md transition-shadow"
                        >
                            <div className="flex items-center gap-4">
                                <div className={cn("w-12 h-12 rounded-full flex items-center justify-center", card.color)}>
                                    <card.icon size={20} />
                                </div>
                                <div>
                                    <p className="text-xs text-gray-400 font-bold mb-1">{card.count} {card.label}</p>
                                    <h4 className="font-bold text-sm">{card.title}</h4>
                                </div>
                            </div>
                            <button className="text-gray-300 hover:text-gray-600">
                                <MoreHorizontal size={20} />
                            </button>
                        </motion.div>
                    ))}
                </div>

                {/* Continue Watching / Recommended */}
                <div className="flex items-center justify-between mb-6">
                    <h3 className="text-xl font-bold">Continue Progress</h3>
                    <div className="flex gap-2">
                        <button className="p-2 rounded-full border border-gray-200 hover:bg-gray-50 text-gray-400"><ChevronRight className="rotate-180" size={20} /></button>
                        <button className="p-2 rounded-full bg-[#8B5CF6] text-white"><ChevronRight size={20} /></button>
                    </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {RECOMMENDED_ITEMS.map((item, idx) => (
                        <motion.div
                            key={idx}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.2 + idx * 0.1 }}
                            className="group cursor-pointer"
                        >
                            <div className={cn("h-40 rounded-2xl mb-4 relative overflow-hidden", item.image)}>
                                {/* Placeholder Image Gradient */}
                                <div className="absolute inset-0 bg-gradient-to-br from-black/5 to-black/20" />
                                <button className="absolute top-3 right-3 p-2 rounded-full bg-black/20 text-white hover:bg-black/40 backdrop-blur-sm transition-colors">
                                    <Heart size={16} />
                                </button>
                            </div>
                            <div className="px-1">
                                <span className="text-[10px] font-bold text-[#8B5CF6] bg-[#8B5CF6]/10 px-2 py-1 rounded-md uppercase tracking-wider">
                                    {item.category}
                                </span>
                                <h4 className="font-bold text-lg mt-3 mb-2 leading-tight group-hover:text-[#8B5CF6] transition-colors">
                                    {item.title}
                                </h4>
                                <div className="flex items-center gap-2">
                                    <div className="w-6 h-6 rounded-full bg-gray-200" />
                                    <div className="flex flex-col">
                                        <span className="text-xs font-bold">{item.author}</span>
                                        <span className="text-[10px] text-gray-400">Mentor</span>
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </div>

                <div className="mt-10 flex justify-between items-center border-t border-gray-100 pt-6">
                    <h3 className="text-xl font-bold">Your Lesson</h3>
                    <button className="text-sm font-bold text-[#8B5CF6] hover:underline">See all</button>
                </div>
            </div>

            {/* Right Sidebar */}
            <RightSidebar user={MOCK_USER} agents={agents} />
        </div>
    );
}

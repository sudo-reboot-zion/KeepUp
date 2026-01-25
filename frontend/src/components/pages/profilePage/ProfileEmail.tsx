import React from 'react';
import { ArrowRight } from 'lucide-react';

interface ProfileEmailProps {
    email: string;
}

export default function ProfileEmail({ email }: ProfileEmailProps) {
    return (
        <div className="bg-black p-12 flex items-center justify-between group cursor-pointer hover:bg-white/[0.02] transition-colors border-t border-white/10">
            <div className="space-y-2">
                <p className="text-[10px] tracking-[0.2em] text-gray-500 font-bold uppercase">Email:</p>
                <p className="text-3xl md:text-4xl font-black tracking-tight group-hover:text-[var(--primaryColor)] transition-colors">
                    {email}
                </p>
            </div>
            <div className="w-16 h-16 border border-white/10 rounded-full flex items-center justify-center group-hover:border-[var(--primaryColor)] group-hover:bg-[var(--primaryColor)] group-hover:text-black transition-all">
                <ArrowRight className="w-8 h-8" />
            </div>
        </div>
    );
}

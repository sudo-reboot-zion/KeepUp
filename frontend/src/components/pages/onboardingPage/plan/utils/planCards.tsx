import { ReactElement } from 'react';
import { Target, TrendingUp, Clock, Flag, Calendar, ShieldCheck } from 'lucide-react';
import type { FinalPlan } from '@/types/onboarding.types';

interface PlanCardData {
    icon: ReactElement;
    title: string;
    description: string;
}

/**
 * Generate plan card data from final plan
 */
export function generatePlanCards(finalPlan: FinalPlan): PlanCardData[] {
    return [
        {
            icon: <Target className="w-8 h-8" />,
            title: "Primary Objective",
            description: finalPlan.interpreted_goal,
        },
        {
            icon: <Clock className="w-8 h-8" />,
            title: "Timeline",
            description: `${finalPlan.timeline_weeks || 12} Weeks to achieve your goal`,
        },
        {
            icon: <TrendingUp className="w-8 h-8" />,
            title: "Weekly Targets",
            description: finalPlan.weekly_target,
        },
        {
            icon: <Flag className="w-8 h-8" />,
            title: "First Milestone",
            description: finalPlan.first_milestone,
        },
        {
            icon: <Calendar className="w-8 h-8" />,
            title: "Schedule Structure",
            description: `${finalPlan.weekly_schedule?.[0]?.workouts_per_week || 3} workouts per week • Focus: ${finalPlan.weekly_schedule?.[0]?.focus || 'General Conditioning'}`,
        },
        {
            icon: <ShieldCheck className="w-8 h-8" />,
            title: "Safety Protocols",
            description: finalPlan.safety_notes?.[0] || "Standard safety protocols applied.",
        }
    ];
}

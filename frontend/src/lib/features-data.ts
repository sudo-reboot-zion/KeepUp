// Detailed feature data structured for easy backend migration
// This matches the format that would come from GET /api/features/{slug}

export interface FeatureSection {
    type: 'intro' | 'features' | 'benefits' | 'how-it-works' | 'cta';
    heading?: string;
    content?: string;
    items?: Array<{
        icon?: string;
        title: string;
        description: string;
    }>;
}

export interface FeatureDetail {
    id: string;
    slug: string;
    title: string;
    subtitle: string;
    hero_image: string;
    sections: FeatureSection[];
}

export const featuresData: Record<string, FeatureDetail> = {
    "custom-workout-plans": {
        id: "01",
        slug: "custom-workout-plans",
        title: "Custom Workout Plans",
        subtitle: "Your Personal Fitness Blueprint",
        hero_image: "/assets/images/bg-cron.svg",
        sections: [
            {
                type: "intro",
                heading: "Workouts That Evolve With You",
                content: "No two bodies are the same, and neither should your workout plan be. KEEP UP creates personalized workout schedules that adapt to your fitness level, goals, and progress. Whether you're just starting out or pushing for new personal records, our intelligent system designs routines that challenge you at just the right level."
            },
            {
                type: "features",
                heading: "What Makes Our Workout Plans Special",
                items: [
                    {
                        icon: "Target",
                        title: "Goal-Oriented Design",
                        description: "Every exercise is chosen to move you closer to your specific fitness goals, whether that's building strength, losing weight, or improving endurance."
                    },
                    {
                        icon: "TrendingUp",
                        title: "Progressive Overload",
                        description: "Our system automatically adjusts intensity, volume, and complexity as you get stronger, ensuring continuous improvement without plateaus."
                    },
                    {
                        icon: "Calendar",
                        title: "Flexible Scheduling",
                        description: "Life happens. Our adaptive scheduling works around your constraints, rearranging workouts to fit your busy lifestyle while maintaining effectiveness."
                    },
                    {
                        icon: "Zap",
                        title: "Variety & Engagement",
                        description: "Say goodbye to boring routines. We mix exercises, training styles, and intensities to keep your workouts fresh and exciting."
                    }
                ]
            },
            {
                type: "how-it-works",
                heading: "How It Works",
                items: [
                    {
                        title: "1. Assessment",
                        description: "We start by understanding your current fitness level, experience, available equipment, and time constraints."
                    },
                    {
                        title: "2. Personalization",
                        description: "Our AI analyzes your goals and creates a custom workout plan optimized for your success."
                    },
                    {
                        title: "3. Adaptation",
                        description: "As you complete workouts, the system learns and adjusts, ensuring you're always challenged but never overwhelmed."
                    },
                    {
                        title: "4. Progress Tracking",
                        description: "Watch your strength, endurance, and performance metrics improve week after week with detailed analytics."
                    }
                ]
            },
            {
                type: "cta",
                heading: "Ready to Transform Your Fitness?",
                content: "Join thousands who have already achieved their fitness goals with KEEP UP's personalized workout plans."
            }
        ]
    },
    "nutrition-guidance": {
        id: "02",
        slug: "nutrition-guidance",
        title: "Nutrition Guidance",
        subtitle: "Fuel Your Transformation",
        hero_image: "/assets/images/bg-phanty.svg",
        sections: [
            {
                type: "intro",
                heading: "Nutrition That Works For You",
                content: "Great fitness results don't happen in the gym alone. KEEP UP provides personalized nutrition guidance that complements your workout routine and lifestyle. We help you make informed dietary choices that fuel your body, support recovery, and accelerate your progress toward your goals."
            },
            {
                type: "features",
                heading: "Comprehensive Nutrition Support",
                items: [
                    {
                        icon: "Apple",
                        title: "Personalized Meal Plans",
                        description: "Get customized meal suggestions based on your dietary preferences, restrictions, and nutritional needs."
                    },
                    {
                        icon: "Calculator",
                        title: "Macro Tracking",
                        description: "Understand and optimize your protein, carbohydrate, and fat intake to match your fitness goals."
                    },
                    {
                        icon: "BookOpen",
                        title: "Nutritional Education",
                        description: "Learn the 'why' behind nutrition recommendations so you can make informed choices independently."
                    },
                    {
                        icon: "Clock",
                        title: "Meal Timing Optimization",
                        description: "Discover when to eat for maximum energy, performance, and recovery based on your workout schedule."
                    }
                ]
            },
            {
                type: "benefits",
                heading: "The Benefits You'll Experience",
                items: [
                    {
                        title: "Faster Results",
                        description: "Proper nutrition accelerates your fitness progress, helping you reach goals weeks or months faster."
                    },
                    {
                        title: "More Energy",
                        description: "Feel energized throughout the day with optimized meal timing and balanced nutrition."
                    },
                    {
                        title: "Better Recovery",
                        description: "Support muscle recovery and reduce soreness with targeted post-workout nutrition."
                    },
                    {
                        title: "Sustainable Habits",
                        description: "Build a healthy relationship with food that lasts beyond your resolution timeline."
                    }
                ]
            },
            {
                type: "cta",
                heading: "Nutrition Made Simple",
                content: "Stop guessing what to eat. Let KEEP UP guide you to better nutrition choices that support your transformation."
            }
        ]
    },
    "health-monitoring": {
        id: "03",
        slug: "health-monitoring",
        title: "Health Monitoring",
        subtitle: "Track What Matters Most",
        hero_image: "/assets/images/bg-elite.svg",
        sections: [
            {
                type: "intro",
                heading: "Your Complete Wellness Dashboard",
                content: "True health goes beyond just workouts and nutrition. KEEP UP's comprehensive health monitoring tracks your sleep patterns, stress levels, recovery metrics, and overall wellness indicators. Get a complete picture of your health and make data-driven decisions to optimize your wellbeing."
            },
            {
                type: "features",
                heading: "What We Monitor",
                items: [
                    {
                        icon: "Moon",
                        title: "Sleep Quality Tracking",
                        description: "Monitor your sleep duration, quality, and patterns to ensure you're getting the rest needed for optimal recovery and performance."
                    },
                    {
                        icon: "Activity",
                        title: "Stress Level Analysis",
                        description: "Track stress indicators and receive personalized recommendations to manage stress and maintain mental wellbeing."
                    },
                    {
                        icon: "Heart",
                        title: "Recovery Metrics",
                        description: "Understand how well your body is recovering from workouts with metrics like heart rate variability and readiness scores."
                    },
                    {
                        icon: "BarChart",
                        title: "Wellness Trends",
                        description: "Visualize long-term health trends to see how your lifestyle changes are impacting your overall wellbeing."
                    }
                ]
            },
            {
                type: "how-it-works",
                heading: "Smart Health Insights",
                items: [
                    {
                        title: "Continuous Monitoring",
                        description: "Track your health metrics automatically throughout the day with seamless integrations."
                    },
                    {
                        title: "Intelligent Analysis",
                        description: "Our AI identifies patterns and correlations between your sleep, stress, workouts, and nutrition."
                    },
                    {
                        title: "Actionable Recommendations",
                        description: "Receive personalized suggestions to improve your sleep quality, manage stress, and optimize recovery."
                    },
                    {
                        title: "Progress Visualization",
                        description: "See your health improvements over time with beautiful, easy-to-understand charts and reports."
                    }
                ]
            },
            {
                type: "cta",
                heading: "Take Control of Your Health",
                content: "Start monitoring the metrics that matter and make informed decisions about your wellbeing."
            }
        ]
    },
    "community-support": {
        id: "04",
        slug: "community-support",
        title: "Community Support",
        subtitle: "Transform Together",
        hero_image: "/assets/images/bg-prat.svg",
        sections: [
            {
                type: "intro",
                heading: "You're Not Alone in This Journey",
                content: "Achieving your goals is easier when you're surrounded by people who understand your challenges and celebrate your victories. KEEP UP's vibrant community connects you with like-minded individuals on similar transformation journeys, providing motivation, accountability, and support every step of the way."
            },
            {
                type: "features",
                heading: "Community Features",
                items: [
                    {
                        icon: "Users",
                        title: "Goal-Based Groups",
                        description: "Join communities focused on specific goals like weight loss, muscle building, or marathon training."
                    },
                    {
                        icon: "MessageCircle",
                        title: "Peer Support",
                        description: "Share experiences, ask questions, and get advice from others who've faced similar challenges."
                    },
                    {
                        icon: "Trophy",
                        title: "Milestone Celebrations",
                        description: "Celebrate your achievements with a community that genuinely cares about your success."
                    },
                    {
                        icon: "Sparkles",
                        title: "Accountability Partners",
                        description: "Connect with accountability partners who keep you motivated and on track toward your goals."
                    }
                ]
            },
            {
                type: "benefits",
                heading: "Why Community Matters",
                items: [
                    {
                        title: "3x Higher Success Rate",
                        description: "Studies show people with community support are 3 times more likely to achieve their fitness goals."
                    },
                    {
                        title: "Sustained Motivation",
                        description: "Stay motivated even on tough days with encouragement from people who understand your journey."
                    },
                    {
                        title: "Shared Knowledge",
                        description: "Learn from others' experiences, mistakes, and successes to accelerate your own progress."
                    },
                    {
                        title: "Lasting Friendships",
                        description: "Build meaningful connections with people who share your values and commitment to health."
                    }
                ]
            },
            {
                type: "cta",
                heading: "Join the KEEP UP Community",
                content: "Be part of a supportive community that will help you stay committed to your resolutions all year long."
            }
        ]
    }
};

// Helper function to get feature by slug (simulates API call)
export const getFeatureBySlug = (slug: string): FeatureDetail | null => {
    return featuresData[slug] || null;
};

// Get all feature slugs (useful for static generation)
export const getAllFeatureSlugs = (): string[] => {
    return Object.keys(featuresData);
};

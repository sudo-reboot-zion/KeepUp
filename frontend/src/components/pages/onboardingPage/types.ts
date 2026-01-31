export type Message = {
    id: string;
    text: string;
    sender: 'agent' | 'user';
    timestamp: Date;
    type?: 'text' | 'options';
    options?: string[];
};

export type UserGoal = 'fitness' | 'sleep' | 'stress' | 'wellness' | null;

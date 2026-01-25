import GoalStep from './GoalStep';
import PastAttemptsStep from './PastAttemptsStep';
import ConstraintsStep from './ConstraintsStep';
import OccupationStep from './OccupationStep';
import type { OccupationDetails, GoalDomain } from '@/types/onboarding.types';

interface StepContentProps {
    currentStep: number;
    formData: {
        domain?: GoalDomain;
        resolution_text: string;
        past_attempts: string;
        life_constraints: string[];
        occupation: string;
        occupation_details: OccupationDetails;
    };
    onUpdateText: (field: 'resolution_text' | 'past_attempts', value: string) => void;
    onUpdateDomain: (domain: GoalDomain) => void;
    onUpdateOccupation: (value: string) => void;
    onUpdateOccupationDetails: (details: Partial<OccupationDetails>) => void;
    onAddConstraint: (constraint: string) => void;
    onRemoveConstraint: (constraint: string) => void;
}

export default function StepContent({
    currentStep,
    formData,
    onUpdateText,
    onUpdateDomain,
    onUpdateOccupation,
    onUpdateOccupationDetails,
    onAddConstraint,
    onRemoveConstraint
}: StepContentProps) {
    return (
        <>
            {currentStep === 1 && (
                <GoalStep
                    domain={formData.domain}
                    value={formData.resolution_text}
                    onDomainChange={onUpdateDomain}
                    onChange={(value) => onUpdateText('resolution_text', value)}
                />
            )}

            {currentStep === 2 && (
                <PastAttemptsStep
                    value={formData.past_attempts}
                    onChange={(value) => onUpdateText('past_attempts', value)}
                />
            )}

            {currentStep === 3 && (
                <ConstraintsStep
                    constraints={formData.life_constraints}
                    onAdd={onAddConstraint}
                    onRemove={onRemoveConstraint}
                />
            )}

            {currentStep === 4 && (
                <OccupationStep
                    occupation={formData.occupation}
                    occupationDetails={formData.occupation_details}
                    onOccupationChange={onUpdateOccupation}
                    onDetailsChange={onUpdateOccupationDetails}
                />
            )}
        </>
    );
}

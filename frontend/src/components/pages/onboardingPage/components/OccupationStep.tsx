import { Briefcase } from 'lucide-react';
import type { OccupationDetails } from '@/types/onboarding.types';

interface OccupationStepProps {
    occupation: string;
    occupationDetails: OccupationDetails;
    onOccupationChange: (value: string) => void;
    onDetailsChange: (details: Partial<OccupationDetails>) => void;
}

export default function OccupationStep({
    occupation,
    occupationDetails,
    onOccupationChange,
    onDetailsChange
}: OccupationStepProps) {
    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-2xl font-bold mb-2">What do you do?</h2>
                <p className="text-[var(--fg)] opacity-60 text-sm mb-4">
                    Your job affects your health. We&apos;ll tailor your plan to your occupation.
                </p>
            </div>

            <div className="space-y-4">
                <div className="space-y-2">
                    <label className="text-sm font-medium text-[var(--fg)] opacity-60 ml-1">
                        Occupation
                    </label>
                    <select
                        value={occupation}
                        onChange={(e) => onOccupationChange(e.target.value)}
                        className="w-full bg-[var(--fg)]/5 border border-[var(--border)] rounded-xl px-4 py-3 text-[var(--fg)] focus:outline-none focus:border-[var(--primary)] focus:ring-1 focus:ring-[var(--primary)] transition-all"
                    >
                        <option value="">Select Occupation...</option>
                        <option value="developer">Developer / Tech / Desk Job</option>
                        <option value="nurse">Healthcare / Nurse / Doctor</option>
                        <option value="driver">Driver / Delivery / Trucking</option>
                        <option value="entrepreneur">Entrepreneur / Founder</option>
                        <option value="teacher">Teacher / Educator</option>
                        <option value="manual_labor">Manual Labor / Construction</option>
                        <option value="sales">Sales / Customer Service</option>
                        <option value="other">Other</option>
                    </select>
                </div>

                <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                        <label className="text-sm font-medium text-[var(--fg)] opacity-60 ml-1">
                            Hours/Week
                        </label>
                        <input
                            type="number"
                            value={occupationDetails.hours_per_week}
                            onChange={(e) => onDetailsChange({
                                hours_per_week: parseInt(e.target.value) || 0
                            })}
                            className="w-full bg-[var(--fg)]/5 border border-[var(--border)] rounded-xl px-4 py-3 text-[var(--fg)] focus:outline-none focus:border-[var(--primary)] focus:ring-1 focus:ring-[var(--primary)] transition-all"
                        />
                    </div>
                    <div className="space-y-2">
                        <label className="text-sm font-medium text-[var(--fg)] opacity-60 ml-1">
                            Schedule
                        </label>
                        <select
                            value={occupationDetails.schedule_type}
                            onChange={(e) => onDetailsChange({
                                schedule_type: e.target.value
                            })}
                            className="w-full bg-[var(--fg)]/5 border border-[var(--border)] rounded-xl px-4 py-3 text-[var(--fg)] focus:outline-none focus:border-[var(--primary)] focus:ring-1 focus:ring-[var(--primary)] transition-all"
                        >
                            <option value="9-5">Standard (9-5)</option>
                            <option value="shift">Shift Work</option>
                            <option value="flexible">Flexible</option>
                            <option value="night">Night Shift</option>
                            <option value="irregular">Irregular</option>
                        </select>
                    </div>
                </div>
            </div>

            <div className="bg-[var(--fg)]/5 border border-[var(--border)] rounded-xl p-4 flex items-start gap-3">
                <Briefcase className="w-5 h-5 text-[var(--primary)] shrink-0 mt-0.5" />
                <p className="text-xs text-[var(--fg)] opacity-60">
                    <strong>Why?</strong> Developers need eye rest. Nurses need leg recovery. We customize your daily tasks based on this.
                </p>
            </div>
        </div>
    );
}

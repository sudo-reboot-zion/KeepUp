

'use client';

import React, { useState, useEffect } from 'react';
import type { BiometricCheckRequest } from '@/types/safety.types';
import { useMedicalThresholds, useBiometricSafety } from '@/hooks/useSafety';
import AlertDisplay from './AlertDisplay';

interface BiometricReading {
    systolic: number;
    diastolic: number;
    heart_rate: number;
    weight: number;
}

interface BiometricMonitorProps {
    resolutionId: number;
    onSafetyStatusChange?: (safe: boolean) => void;
    showThresholds?: boolean;
    compact?: boolean;
}

/**
 * Metric indicator with threshold comparison
 */
const MetricIndicator: React.FC<{
    label: string;
    value: number;
    unit: string;
    min?: number;
    max?: number;
    normal?: { min: number; max: number };
    critical?: { min: number; max: number };
}> = ({ label, value, unit, normal, critical }) => {
    // Determine status
    let statusColor = 'text-green-600';
    let statusIcon = '✓';

    if (critical) {
        if (value < critical.min || value > critical.max) {
            statusColor = 'text-red-600';
            statusIcon = '✕';
        } else if (normal && (value < normal.min || value > normal.max)) {
            statusColor = 'text-yellow-600';
            statusIcon = '⚠️';
        }
    }

    return (
        <div className="border border-gray-200 rounded-lg p-3 mb-2">
            <div className="flex justify-between items-start mb-2">
                <label className="text-sm font-medium text-gray-700">{label}</label>
                <span className={`text-lg font-bold ${statusColor}`}>{statusIcon}</span>
            </div>
            <p className="text-2xl font-bold text-gray-900 mb-1">
                {value} <span className="text-sm text-gray-500">{unit}</span>
            </p>
            {normal && (
                <p className="text-xs text-gray-600">
                    Normal: {normal.min} - {normal.max}
                </p>
            )}
            {critical && (
                <p className="text-xs text-red-600">
                    Critical: &lt; {critical.min} or &gt; {critical.max}
                </p>
            )}
        </div>
    );
};

/**
 * Biometric Monitor Component
 */
export const BiometricMonitor: React.FC<BiometricMonitorProps> = ({
    resolutionId,
    onSafetyStatusChange,
    showThresholds = true,
    compact = false,
}) => {
    const { thresholds, isLoading: thresholdsLoading } = useMedicalThresholds();
    const { checkBiometrics, alerts, isSafe, isLoading, error } =
        useBiometricSafety(resolutionId);

    const [biometrics, setBiometrics] = useState<BiometricReading>({
        systolic: 0,
        diastolic: 0,
        heart_rate: 0,
        weight: 0,
    });

    // Notify parent of safety status changes
    useEffect(() => {
        onSafetyStatusChange?.(isSafe);
    }, [isSafe, onSafetyStatusChange]);

    const handleInputChange = (key: keyof BiometricReading, value: string) => {
        const numValue = parseFloat(value) || 0;
        setBiometrics((prev) => ({
            ...prev,
            [key]: numValue,
        }));
    };

    const handleCheckBiometrics = async () => {
        const request: BiometricCheckRequest = {
            systolic: biometrics.systolic,
            diastolic: biometrics.diastolic,
            heart_rate: biometrics.heart_rate,
            weight: biometrics.weight,
        };
        await checkBiometrics(request);
    };

    return (
        <div className={compact ? '' : 'border border-gray-200 rounded-lg p-6'}>
            {/* Header */}
            {!compact && (
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Biometric Monitor</h3>
            )}

            {/* Input Section */}
            <div className="mb-4">
                <h4 className="text-sm font-medium text-gray-700 mb-3">Enter Your Readings</h4>
                <div className="grid grid-cols-2 gap-3 mb-4">
                    <div>
                        <label className="block text-xs font-medium text-gray-600 mb-1">
                            Systolic BP (mmHg)
                        </label>
                        <input
                            type="number"
                            value={biometrics.systolic || ''}
                            onChange={(e) => handleInputChange('systolic', e.target.value)}
                            placeholder="e.g., 120"
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                            disabled={isLoading}
                        />
                    </div>
                    <div>
                        <label className="block text-xs font-medium text-gray-600 mb-1">
                            Diastolic BP (mmHg)
                        </label>
                        <input
                            type="number"
                            value={biometrics.diastolic || ''}
                            onChange={(e) => handleInputChange('diastolic', e.target.value)}
                            placeholder="e.g., 80"
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                            disabled={isLoading}
                        />
                    </div>
                    <div>
                        <label className="block text-xs font-medium text-gray-600 mb-1">
                            Heart Rate (bpm)
                        </label>
                        <input
                            type="number"
                            value={biometrics.heart_rate || ''}
                            onChange={(e) => handleInputChange('heart_rate', e.target.value)}
                            placeholder="e.g., 72"
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                            disabled={isLoading}
                        />
                    </div>
                    <div>
                        <label className="block text-xs font-medium text-gray-600 mb-1">
                            Weight (lbs)
                        </label>
                        <input
                            type="number"
                            value={biometrics.weight || ''}
                            onChange={(e) => handleInputChange('weight', e.target.value)}
                            placeholder="e.g., 170"
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                            disabled={isLoading}
                        />
                    </div>
                </div>

                {/* Check Button */}
                <button
                    onClick={handleCheckBiometrics}
                    disabled={isLoading || thresholdsLoading}
                    className="w-full bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white font-medium py-2 px-4 rounded-lg transition-colors"
                >
                    {isLoading ? 'Checking...' : 'Check Biometrics'}
                </button>
            </div>

            {/* Error Display */}
            {error && (
                <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-sm text-red-800">
                    Error: {error}
                </div>
            )}

            {/* Thresholds Section */}
            {showThresholds && thresholds && !thresholdsLoading && (
                <div className="mb-4 p-4 bg-gray-50 rounded-lg">
                    <h4 className="text-sm font-medium text-gray-700 mb-2">Medical Thresholds</h4>
                    <div className="text-xs text-gray-600 space-y-1">
                        <p>
                            BP Critical: &gt; {thresholds?.blood_pressure_critical?.systolic || thresholds?.bp_critical_high?.systolic}/
                            {thresholds?.blood_pressure_critical?.diastolic || thresholds?.bp_critical_high?.diastolic}
                        </p>
                        <p>HR Critical: &lt; {thresholds?.heart_rate_critical?.min || thresholds?.hr_critical_low} or &gt; {thresholds?.heart_rate_critical?.max || thresholds?.hr_critical_high}</p>
                        <p>Weight Change: &gt; {thresholds?.weight_change_per_week || thresholds?.weight_weekly_change_max} lbs/week</p>
                    </div>
                </div>
            )}

            {/* Alerts Section */}
            {alerts.length > 0 && (
                <div className="mb-4">
                    <h4 className="text-sm font-medium text-gray-700 mb-2">Safety Alerts</h4>
                    <AlertDisplay alerts={alerts} compact={true} />
                </div>
            )}

            {/* Current Reading Display */}
            {biometrics.systolic > 0 && (
                <div className="mt-4">
                    <h4 className="text-sm font-medium text-gray-700 mb-2">Current Readings</h4>
                    <div className="grid grid-cols-2 gap-2">
                        <MetricIndicator
                            label="Blood Pressure"
                            value={biometrics.systolic}
                            unit={`/${biometrics.diastolic} mmHg`}
                            normal={{ min: 90, max: 120 }}
                            critical={{
                                min: 90,
                                max: (thresholds?.blood_pressure_critical?.systolic ?? thresholds?.bp_critical_high?.systolic ?? 180),
                            }}
                        />
                        <MetricIndicator
                            label="Heart Rate"
                            value={biometrics.heart_rate}
                            unit="bpm"
                            normal={{ min: 60, max: 100 }}
                            critical={
                                thresholds?.heart_rate_critical
                                    ? {
                                        min: thresholds.heart_rate_critical.min || 40,
                                        max: thresholds.heart_rate_critical.max || 180,
                                    }
                                    : { min: 40, max: 180 }
                            }
                        />
                    </div>
                </div>
            )}

            {/* Safety Status */}
            <div className="mt-4 p-3 rounded-lg bg-gray-50 border border-gray-200">
                <div
                    className={`text-sm font-medium ${isSafe ? 'text-green-600' : 'text-red-600'}`}
                >
                    {isSafe ? '✓ Safe to proceed' : '⚠️ Safety concerns detected'}
                </div>
            </div>
        </div>
    );
};

export default BiometricMonitor;

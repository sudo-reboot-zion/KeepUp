/**
 * Safety Status Component
 * Displays overall safety status with biometric, confidence, and overtraining indicators
 */

'use client';

import React, { useState } from 'react';

interface SafetyStatusProps {
    overallSafe: boolean;
    riskLevel?: 'low' | 'medium' | 'high' | null;
    alertCount: number;
    showDetails?: boolean;
    onAlertClick?: () => void;
}

interface StatusIndicatorProps {
    label: string;
    safe: boolean;
    loading?: boolean;
    riskLevel?: 'low' | 'medium' | 'high' | null;
}

/**
 * Individual status indicator
 */
const StatusIndicator: React.FC<StatusIndicatorProps> = ({ label, safe, loading, riskLevel }) => {
    let bgColor = safe ? 'bg-green-100' : 'bg-red-100';
    let textColor = safe ? 'text-green-800' : 'text-red-800';
    let icon = safe ? '✓' : '✕';

    if (riskLevel === 'high') {
        bgColor = 'bg-red-100';
        textColor = 'text-red-800';
        icon = '⚠️';
    } else if (riskLevel === 'medium') {
        bgColor = 'bg-yellow-100';
        textColor = 'text-yellow-800';
        icon = '⚡';
    }

    return (
        <div className={`${bgColor} ${textColor} px-4 py-2 rounded-lg text-sm font-medium flex items-center gap-2`}>
            {loading ? (
                <span className="animate-spin">◌</span>
            ) : (
                <span className="text-lg">{icon}</span>
            )}
            <span>{label}</span>
        </div>
    );
};

/**
 * Risk Level Gauge
 */
const RiskLevelGauge: React.FC<{ level: 'low' | 'medium' | 'high' | null }> = ({ level }) => {
    if (!level) return null;

    const getGaugeStyles = () => {
        switch (level) {
            case 'low':
                return {
                    background: 'bg-gradient-to-r from-green-400 to-green-500',
                    label: 'Low Risk',
                    percentage: 25,
                };
            case 'medium':
                return {
                    background: 'bg-gradient-to-r from-yellow-400 to-yellow-500',
                    label: 'Medium Risk',
                    percentage: 50,
                };
            case 'high':
                return {
                    background: 'bg-gradient-to-r from-red-400 to-red-500',
                    label: 'High Risk',
                    percentage: 75,
                };
        }
    };

    const styles = getGaugeStyles();

    return (
        <div className="mt-4">
            <label className="text-sm font-medium text-gray-700 block mb-2">
                {styles?.label}
            </label>
            <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                <div
                    className={`${styles?.background} h-full transition-all duration-300`}
                    style={{ width: `${styles?.percentage}%` }}
                />
            </div>
        </div>
    );
};

/**
 * Safety Status Component
 */
export const SafetyStatus: React.FC<SafetyStatusProps> = ({
    overallSafe,
    riskLevel,
    alertCount,
    showDetails = true,
    onAlertClick,
}) => {
    const [expanded, setExpanded] = useState(false);

    return (
        <div className="rounded-lg border border-gray-200 bg-white p-6">
            {/* Main Status */}
            <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">Safety Status</h3>
                <div
                    className={`flex items-center gap-2 text-lg font-bold ${
                        overallSafe ? 'text-green-600' : 'text-red-600'
                    }`}
                >
                    <span className="text-2xl">{overallSafe ? '✓' : '⚠️'}</span>
                    <span>{overallSafe ? 'Safe' : 'Caution Required'}</span>
                </div>
            </div>

            {/* Alert Count */}
            {alertCount > 0 && (
                <div
                    className="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg cursor-pointer hover:bg-yellow-100 transition-colors"
                    onClick={onAlertClick}
                >
                    <p className="text-sm text-yellow-800 font-medium">
                        ⚠️ {alertCount} alert{alertCount > 1 ? 's' : ''} require attention
                    </p>
                </div>
            )}

            {/* Risk Level Gauge */}
            {riskLevel && <RiskLevelGauge level={riskLevel} />}

            {/* Expandable Details */}
            {showDetails && (
                <div className="mt-6 pt-4 border-t border-gray-200">
                    <button
                        onClick={() => setExpanded(!expanded)}
                        className="text-sm font-medium text-blue-600 hover:text-blue-700 flex items-center gap-2 mb-3"
                    >
                        <span>{expanded ? '▼' : '▶'}</span>
                        {expanded ? 'Hide Details' : 'Show Details'}
                    </button>

                    {expanded && (
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-3">
                            <StatusIndicator
                                label="Biometrics"
                                safe={overallSafe}
                            />
                            <StatusIndicator
                                label="Confidence Level"
                                safe={overallSafe}
                            />
                            <StatusIndicator
                                label="Overtraining Risk"
                                safe={overallSafe}
                                riskLevel={riskLevel}
                            />
                            <StatusIndicator
                                label="Medical Compliance"
                                safe={overallSafe}
                            />
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

/**
 * Compact Safety Header
 * For use in page headers or sidebars
 */
export const SafetyStatusCompact: React.FC<{
    safe: boolean;
    riskLevel?: 'low' | 'medium' | 'high' | null;
    alertCount?: number;
    onClick?: () => void;
}> = ({ safe, riskLevel, alertCount = 0, onClick }) => {
    const getStatusStyle = () => {
        if (!safe) return 'bg-red-100 text-red-800 border-red-300';
        if (riskLevel === 'high') return 'bg-red-100 text-red-800 border-red-300';
        if (riskLevel === 'medium') return 'bg-yellow-100 text-yellow-800 border-yellow-300';
        return 'bg-green-100 text-green-800 border-green-300';
    };

    const getStatusText = () => {
        if (!safe) return 'Caution Required';
        if (riskLevel === 'high') return 'High Risk';
        if (riskLevel === 'medium') return 'Medium Risk';
        return 'Safe';
    };

    return (
        <div
            onClick={onClick}
            className={`inline-flex items-center gap-2 px-3 py-2 rounded-lg border cursor-pointer transition-opacity hover:opacity-80 ${getStatusStyle()}`}
        >
            <span className="text-lg">{safe ? '✓' : '⚠️'}</span>
            <span className="text-sm font-medium">{getStatusText()}</span>
            {alertCount > 0 && (
                <span className="ml-1 text-xs font-bold bg-opacity-30 px-2 py-1 rounded">
                    {alertCount}
                </span>
            )}
        </div>
    );
};

export default SafetyStatus;

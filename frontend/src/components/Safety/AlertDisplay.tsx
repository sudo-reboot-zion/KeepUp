/**
 * Safety Alert Display Component
 * Shows safety alerts with severity levels, actions, and acknowledgment UI
 */

'use client';

import React, { useState } from 'react';
import type { SafetyAlert } from '@/types/safety.types';

interface AlertDisplayProps {
    alerts: SafetyAlert[];
    onDismiss?: (alertId: string) => void;
    onAcknowledge?: (alertId: string, action?: string) => void;
    isLoading?: boolean;
    compact?: boolean;
}

/**
 * Get severity level color and styling
 */
const getSeverityStyles = (severity?: string) => {
    const s = (severity ?? '').toLowerCase();
    switch (s) {
        case 'critical':
            return {
                container: 'bg-red-50 border-l-4 border-red-500',
                icon: '🔴',
                textColor: 'text-red-800',
                badgeColor: 'bg-red-100 text-red-800',
                buttonColor: 'bg-red-500 hover:bg-red-600 text-white',
            };
        case 'high':
            return {
                container: 'bg-orange-50 border-l-4 border-orange-500',
                icon: '🟠',
                textColor: 'text-orange-800',
                badgeColor: 'bg-orange-100 text-orange-800',
                buttonColor: 'bg-orange-500 hover:bg-orange-600 text-white',
            };
        case 'medium':
            return {
                container: 'bg-yellow-50 border-l-4 border-yellow-500',
                icon: '🟡',
                textColor: 'text-yellow-800',
                badgeColor: 'bg-yellow-100 text-yellow-800',
                buttonColor: 'bg-yellow-500 hover:bg-yellow-600 text-white',
            };
        case 'low':
            return {
                container: 'bg-blue-50 border-l-4 border-blue-500',
                icon: '🔵',
                textColor: 'text-blue-800',
                badgeColor: 'bg-blue-100 text-blue-800',
                buttonColor: 'bg-blue-500 hover:bg-blue-600 text-white',
            };
        default:
            return {
                container: 'bg-gray-50 border-l-4 border-gray-500',
                icon: '⚪',
                textColor: 'text-gray-800',
                badgeColor: 'bg-gray-100 text-gray-800',
                buttonColor: 'bg-gray-500 hover:bg-gray-600 text-white',
            };
    }
};

/**
 * Single alert card component
 */
const AlertCard: React.FC<{
    alert: SafetyAlert;
    onDismiss?: (id: string) => void;
    onAcknowledge?: (id: string, action?: string) => void;
    compact?: boolean;
}> = ({ alert, onDismiss, onAcknowledge, compact = false }) => {
    const [acknowledged, setAcknowledged] = useState(false);
    const styles = getSeverityStyles(alert.severity);

    const handleAcknowledge = () => {
        setAcknowledged(true);
        onAcknowledge?.(alert.id ?? '', 'acknowledged');
    };

    return (
        <div className={`${styles.container} p-4 rounded-lg mb-3 transition-all`}>
            <div className="flex items-start gap-3">
                <span className="text-2xl flex-shrink-0 mt-1">{styles.icon}</span>

                <div className="flex-grow">
                    {/* Header */}
                    <div className="flex items-center justify-between gap-2 mb-1">
                        <h3 className={`font-semibold ${styles.textColor}`}>{alert.type}</h3>
                        <span className={`text-xs px-2 py-1 rounded ${styles.badgeColor}`}>
                            {alert.severity}
                        </span>
                    </div>

                    {/* Message */}
                    <p className={`text-sm ${styles.textColor} mb-2`}>{alert.message}</p>

                    {/* Category (if not compact) */}
                    {!compact && alert.category && (
                        <p className={`text-xs ${styles.textColor} opacity-75 mb-2`}>
                            Category: {alert.category}
                        </p>
                    )}

                    {/* Actions */}
                    {!acknowledged && (
                        <div className="flex gap-2">
                            <button
                                onClick={handleAcknowledge}
                                className={`text-xs px-3 py-1 rounded transition-colors ${styles.buttonColor}`}
                            >
                                Acknowledge
                            </button>
                            {onDismiss && (
                                <button
                                    onClick={() => onDismiss?.(alert.id ?? '')}
                                    className="text-xs px-3 py-1 rounded bg-gray-300 hover:bg-gray-400 text-gray-800 transition-colors"
                                >
                                    Dismiss
                                </button>
                            )}
                        </div>
                    )}

                    {acknowledged && (
                        <p className="text-xs text-green-600 font-medium">✓ Alert acknowledged</p>
                    )}
                </div>
            </div>
        </div>
    );
};

/**
 * Alert Display Component
 */
export const AlertDisplay: React.FC<AlertDisplayProps> = ({
    alerts,
    onDismiss,
    onAcknowledge,
    isLoading = false,
    compact = false,
}) => {
    if (isLoading) {
        return (
            <div className="flex items-center justify-center py-4">
                <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
            </div>
        );
    }

    if (alerts.length === 0) {
        return (
            <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
                <p className="text-sm text-green-800">✓ No safety alerts at this time</p>
            </div>
        );
    }

    return (
        <div className={compact ? 'space-y-2' : 'space-y-3'}>
            {alerts.map((alert) => (
                <AlertCard
                    key={alert.id}
                    alert={alert}
                    onDismiss={onDismiss}
                    onAcknowledge={onAcknowledge}
                    compact={compact}
                />
            ))}
        </div>
    );
};

/**
 * Compact Alert Badge Component
 * Shows number of alerts with critical/high alerts highlighted
 */
export const AlertBadge: React.FC<{
    alerts: SafetyAlert[];
    onClick?: () => void;
}> = ({ alerts, onClick }) => {
    if (alerts.length === 0) {
        return (
            <div className="inline-flex items-center gap-1 bg-green-100 text-green-800 px-3 py-1 rounded-full text-xs font-medium cursor-pointer hover:bg-green-200 transition-colors"
                 onClick={onClick}
            >
                <span>✓</span>
                <span>Safe</span>
            </div>
        );
    }

    const criticalCount = alerts.filter(a => (a.severity ?? '').toLowerCase() === 'critical').length;
    const highCount = alerts.filter(a => (a.severity ?? '').toLowerCase() === 'high').length;
    const totalCount = alerts.length;

    let badgeColor = 'bg-blue-100 text-blue-800';
    let displayText = `${totalCount} alert${totalCount > 1 ? 's' : ''}`;

    if (criticalCount > 0) {
        badgeColor = 'bg-red-100 text-red-800';
        displayText = `${criticalCount} critical`;
    } else if (highCount > 0) {
        badgeColor = 'bg-orange-100 text-orange-800';
        displayText = `${highCount} high`;
    }

    return (
        <div
            className={`inline-flex items-center gap-1 ${badgeColor} px-3 py-1 rounded-full text-xs font-medium cursor-pointer hover:opacity-80 transition-opacity`}
            onClick={onClick}
        >
            <span>⚠️</span>
            <span>{displayText}</span>
        </div>
    );
};

export default AlertDisplay;

import { ArrowRight } from 'lucide-react';

interface ArrowButtonProps {
    onClick: () => void;
    disabled?: boolean;
    isLoading?: boolean;
    text: string;
    className?: string;
}

export default function ArrowButton({
    onClick,
    disabled = false,
    isLoading = false,
    text,
    className = ''
}: ArrowButtonProps) {
    return (
        <button
            onClick={onClick}
            disabled={disabled || isLoading}
            className={`inline-flex items-center gap-2 px-6 py-3 rounded-xl font-semibold transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed ${className}`}
        >
            <span>{isLoading ? 'Loading...' : text}</span>
            {!isLoading && <ArrowRight className="w-5 h-5" />}
        </button>
    );
}

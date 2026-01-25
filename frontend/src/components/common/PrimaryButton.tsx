import React from 'react';
import Link from 'next/link';
import { twMerge } from 'tailwind-merge';
import { clsx, type ClassValue } from 'clsx';

function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

interface PrimaryButtonProps {
    children: React.ReactNode;
    href?: string;
    onClick?: () => void;
    className?: string;
}

const PrimaryButton: React.FC<PrimaryButtonProps> = ({ children, href, onClick, className = '' }) => {
    const content = (
        <>
            {children}
            <div className="bg-[var(--bg)] rounded-full p-2 group-hover:translate-x-1 transition-transform duration-300 flex items-center justify-center">
                <svg
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="3"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    className="text-[var(--fg)]"
                >
                    <path d="M5 12h14M12 5l7 7-7 7" />
                </svg>
            </div>
        </>
    );

    const baseClasses = cn(
        "group inline-flex items-center gap-2 bg-[var(--fg)] text-[var(--bg)] px-6 py-3 rounded-full font-bold text-lg hover:opacity-90 transition-all duration-300 w-fit",
        className
    );

    if (href) {
        return (
            <Link href={href} className={baseClasses}>
                {content}
            </Link>
        );
    }

    return (
        <button onClick={onClick} className={baseClasses}>
            {content}
        </button>
    );
};

export default PrimaryButton;

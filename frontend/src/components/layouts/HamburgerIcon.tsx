"use client";

import React, { forwardRef } from "react";

interface HamburgerIconProps {
    isActive: boolean;
    onClick: () => void;
}

const HamburgerIcon = forwardRef<HTMLDivElement, HamburgerIconProps>(
    ({ isActive, onClick }, ref) => {
        return (
            <div
                className={`relative w-12 h-12 flex flex-col justify-center items-center border border-[var(--fg)] rounded-full cursor-pointer transition-all duration-300 hover:opacity-70 ${isActive ? "active" : ""
                    }`}
                ref={ref}
                onClick={onClick}
            >
                <span
                    className={`absolute w-[15px] h-[1.25px] bg-[var(--fg)] transition-all duration-750 ease-[cubic-bezier(0.87,0,0.13,1)] will-change-transform ${isActive
                        ? "translate-y-0 rotate-45 scale-x-[1.05]"
                        : "-translate-y-[3px]"
                        }`}
                ></span>
                <span
                    className={`absolute w-[15px] h-[1.25px] bg-[var(--fg)] transition-all duration-750 ease-[cubic-bezier(0.87,0,0.13,1)] will-change-transform ${isActive
                        ? "translate-y-0 -rotate-45 scale-x-[1.05]"
                        : "translate-y-[3px]"
                        }`}
                ></span>
            </div>
        );
    }
);

HamburgerIcon.displayName = "HamburgerIcon";

export default HamburgerIcon;

import { forwardRef, SVGProps } from "react";

const Logo = forwardRef<SVGSVGElement, SVGProps<SVGSVGElement>>((props, ref) => {
    return (
        <svg
            ref={ref}
            width="160"
            height="160"
            viewBox="0 0 20 20"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            {...props}
        >
            <g transform="translate(2, 3)">
                <path
                    d="M 7,0 5,5 v 9 h 9 L 16,8 V 5 H 10 V 2 C 10,0.895431 9.10457,0 8,0 Z"
                    stroke="#e3e4d8"
                    strokeWidth="0.5"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                />
                <path
                    d="M 3,5 H 0 v 9 h 3 z"
                    stroke="#e3e4d8"
                    strokeWidth="0.5"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                />
            </g>
        </svg>
    );
});

Logo.displayName = "Logo";

export default Logo;

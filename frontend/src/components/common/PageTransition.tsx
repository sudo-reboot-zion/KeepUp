"use client";

import { usePathname, useRouter } from "next/navigation";
import Logo from "./Logo";
import { useEffect, useRef, ReactNode } from "react";
import gsap from "gsap";

interface PageTransitionProps {
    children: ReactNode;
}

const PageTransition = ({ children }: PageTransitionProps) => {
    const router = useRouter();
    const pathname = usePathname();
    const overlayRef = useRef<HTMLDivElement>(null);
    const logoOverlayRef = useRef<HTMLDivElement>(null);
    const logoRef = useRef<SVGSVGElement>(null);
    const blocksRef = useRef<HTMLDivElement[]>([]);
    const isTransitioning = useRef(false);

    useEffect(() => {
        const createBlocks = () => {
            if (!overlayRef.current) return;
            overlayRef.current.innerHTML = "";
            blocksRef.current = [];

            for (let i = 0; i < 20; i++) {
                const block = document.createElement("div");
                block.className = "block";
                overlayRef.current.appendChild(block);
                blocksRef.current.push(block);
            }
        };

        createBlocks();

        gsap.set(blocksRef.current, { scaleX: 0, transformOrigin: "left" });

        if (logoRef.current) {
            const paths = logoRef.current.querySelectorAll("path");
            paths.forEach(path => {
                const length = path.getTotalLength();
                gsap.set(path, {
                    strokeDasharray: length,
                    strokeDashoffset: length,
                    fill: "transparent",
                });
            });
        }

        revealPage();

        const handleLinkClick = (e: MouseEvent) => {
            const target = (e.target as HTMLElement).closest('a');
            if (!target) return;

            const href = target.getAttribute("href");

            // Only handle internal links that aren't the current page
            if (href && href.startsWith("/") && !href.startsWith("//") && href !== pathname) {
                // Check if it's a real link and not a javascript: or mailto: etc
                if (target.target === "_blank") return;

                e.preventDefault();
                if (isTransitioning.current) return;
                isTransitioning.current = true;
                coverPage(href);
            }
        };

        // Use event delegation on document to catch all link clicks
        document.addEventListener("click", handleLinkClick);

        return () => {
            document.removeEventListener("click", handleLinkClick);
        };
    }, [pathname, router]);

    const coverPage = (url: string) => {
        if (!logoRef.current || !logoOverlayRef.current) {
            router.push(url);
            return;
        }

        const paths = logoRef.current.querySelectorAll("path");

        const tl = gsap.timeline({
            onComplete: () => {
                router.push(url);
            },
        });

        tl.to(blocksRef.current, {
            scaleX: 1,
            duration: 0.4,
            stagger: 0.02,
            ease: "power2.out",
            transformOrigin: "left",
        })
            .set(logoOverlayRef.current, { opacity: 1, visibility: "visible" }, "-=0.2")
            .to(
                paths,
                {
                    strokeDashoffset: 0,
                    duration: 1.5,
                    ease: "power2.inOut",
                    stagger: 0.1
                },
                "-=0.3"
            )
            .to(
                paths,
                {
                    fill: "#e3e4d8",
                    duration: 0.8,
                    ease: "power2.out",
                }
            );
    };

    const revealPage = () => {
        gsap.set(blocksRef.current, { scaleX: 1, transformOrigin: "right" });

        const tl = gsap.timeline({
            onComplete: () => {
                isTransitioning.current = false;
            }
        });

        if (logoOverlayRef.current) {
            tl.to(logoOverlayRef.current, {
                opacity: 0,
                duration: 0.4,
                ease: "power2.out",
                onComplete: () => {
                    gsap.set(logoOverlayRef.current, { visibility: "hidden" });
                }
            });
        }

        tl.to(blocksRef.current, {
            scaleX: 0,
            duration: 0.4,
            stagger: 0.02,
            ease: "power2.out",
            transformOrigin: "right",
        }, "-=0.2");
    };

    return (
        <>
            <div ref={overlayRef} className="transition-overlay"></div>
            <div ref={logoOverlayRef} className="logo-overlay">
                <div className="logo-container">
                    <Logo ref={logoRef} />
                </div>
            </div>
            {children}
        </>
    );
};

export default PageTransition;

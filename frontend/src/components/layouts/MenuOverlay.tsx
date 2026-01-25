"use client";

import React from "react";
import { navLinks, secondaryLinks } from "@/lib/data";
import { useRouter } from "next/navigation";
import { useAppSelector, useAppDispatch } from "@/redux/hooks";
import { logout } from "@/redux/slices/authSlice";
import NotificationBell from "./NotificationBell";
import { DoorOpen } from "lucide-react";

interface MenuOverlayProps {
    overlayRef: React.RefObject<HTMLDivElement | null>;
    contentRef: React.RefObject<HTMLDivElement | null>;
    mediaWrapperRef: React.RefObject<HTMLDivElement | null>;
    setColRef: (index: number) => (el: HTMLDivElement | null) => void;
    isOpen: boolean;
}

const MenuOverlay: React.FC<MenuOverlayProps> = ({
    overlayRef,
    contentRef,
    mediaWrapperRef,
    setColRef,
    isOpen,
}) => {

    const router = useRouter();
    const dispatch = useAppDispatch();
    const { isLoggedIn } = useAppSelector((state) => state.auth);
    const videoRef = React.useRef<HTMLVideoElement>(null);

    React.useEffect(() => {
        if (videoRef.current) {
            if (isOpen) {
                videoRef.current.play().catch(e => console.log("Video play failed:", e));
            } else {
                videoRef.current.pause();
                videoRef.current.currentTime = 0; // Optional: Reset video when closed
            }
        }
    }, [isOpen]);

    const handleLogout = async () => {
        await dispatch(logout());
        router.push("/");
    };

    return (
        <div
            ref={overlayRef}
            className="fixed top-0 left-0 w-screen h-screen bg-[var(--bg)] z-[100] overflow-hidden pointer-events-auto"
            style={{ clipPath: "polygon(0% 0%, 100% 0%, 100% 0%, 0% 0%)" }}
        >
            <div
                className="fixed top-0 left-0 w-screen h-[100svh] flex -translate-y-1/2 will-change-transform pointer-events-auto"
                ref={contentRef}
            >
                <div
                    className="flex-[2] opacity-0 will-change-opacity hidden lg:block"
                    ref={mediaWrapperRef}
                >
                    <video
                        ref={videoRef}
                        src="/assets/video/ai-video.mp4"
                        className="w-full h-full object-cover"
                        loop
                        muted
                        playsInline
                    />
                </div>

                <div className="flex-[3] relative flex flex-col justify-between p-8 lg:p-12">
                    <div className="flex flex-col lg:flex-row items-start lg:items-end gap-12 lg:gap-8 mt-24 lg:mt-0 lg:absolute lg:top-1/2 lg:left-1/2 lg:-translate-x-1/2 lg:-translate-y-1/2 w-full lg:w-3/4">
                        <div className="flex-[3] flex flex-col gap-2" ref={setColRef(0)}>
                            {navLinks.map(
                                (item) => (
                                    <div key={item.label} className="overflow-hidden">
                                        <a
                                            href={item.href}
                                            className="text-5xl lg:text-[3.5rem] font-medium leading-[1.2] hover:text-[var(--fg)]/60 transition-colors text-[var(--fg)]"
                                        >
                                            {item.label}
                                        </a>
                                    </div>
                                )
                            )}
                        </div>

                        <div className="flex-[2] flex flex-col gap-2" ref={setColRef(1)}>
                            {secondaryLinks.map((item) => (
                                <div key={item.label} className="overflow-hidden">
                                    <a
                                        href={item.href}
                                        className="text-[var(--fg)] text-xl lg:text-2xl font-medium hover:text-[var(--fg)]/60 transition-colors"
                                    >
                                        {item.label}
                                    </a>
                                </div>
                            ))}

                            {isLoggedIn && (
                                <>
                                    <div className="overflow-hidden mt-4">
                                        <div className="flex items-center gap-3 text-[var(--fg)] text-xl lg:text-2xl font-medium hover:text-[var(--fg)]/60 transition-colors cursor-pointer">
                                            <NotificationBell />
                                            <span>Notifications</span>
                                        </div>
                                    </div>

                                    <div className="overflow-hidden mt-2">
                                        <button
                                            onClick={handleLogout}
                                            className="flex items-center gap-3 text-red-500 text-xl lg:text-2xl font-medium hover:text-red-400 transition-colors"
                                        >
                                            <DoorOpen className="w-6 h-6" />
                                            <span>Logout</span>
                                        </button>
                                    </div>
                                </>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default MenuOverlay;

"use client";

import { useEffect } from "react";
import { useSelector } from "react-redux";
import { RootState } from "@/redux/store";

export default function ThemeWrapper({ children }: { children: React.ReactNode }) {
    const theme = useSelector((state: RootState) => state.ui.theme);

    useEffect(() => {
        const root = window.document.documentElement;
        if (theme === "dark") {
            root.classList.add("dark");
        } else {
            root.classList.remove("dark");
        }
    }, [theme]);

    return <>{children}</>;
}

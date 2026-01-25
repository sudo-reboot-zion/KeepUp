"use client";

import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "@/redux/store";
import { setTheme } from "@/redux/slices/uiSlice";
import { motion } from "framer-motion";
import { Sun, Moon } from "lucide-react";

const ThemeSwitcher: React.FC = () => {
    const dispatch = useDispatch();
    const theme = useSelector((state: RootState) => state.ui.theme);

    const toggleTheme = () => {
        const newTheme = theme === "light" ? "dark" : "light";
        dispatch(setTheme(newTheme));
    };

    return (
        <button
            onClick={toggleTheme}
            className="relative flex items-center justify-center w-10 h-10 rounded-full bg-[var(--fg)]/10 hover:bg-[var(--fg)]/20 transition-colors backdrop-blur-md border border-[var(--fg)]/10 overflow-hidden"
            aria-label="Toggle theme"
        >
            <motion.div
                initial={false}
                animate={{
                    y: theme === "light" ? -20 : 0,
                    opacity: theme === "light" ? 0 : 1,
                }}
                transition={{ duration: 0.2 }}
                className="absolute"
            >
                <Moon className="w-5 h-5 text-[var(--fg)]" />
            </motion.div>
            <motion.div
                initial={false}
                animate={{
                    y: theme === "light" ? 0 : 20,
                    opacity: theme === "light" ? 1 : 0,
                }}
                transition={{ duration: 0.2 }}
                className="absolute"
            >
                <Sun className="w-5 h-5 text-[var(--fg)]" />
            </motion.div>
        </button>
    );
};

export default ThemeSwitcher;

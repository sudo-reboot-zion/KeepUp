'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import gsap from 'gsap';
import { useAppDispatch, useAppSelector } from '@/redux/hooks';
import { loginAsync, clearError } from '@/redux/slices/authSlice';
import { Eye, EyeOff, Zap, AlertCircle } from 'lucide-react';

export default function LoginPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const formRef = useRef<HTMLDivElement>(null);
    const titleRef = useRef<HTMLHeadingElement>(null);

    const dispatch = useAppDispatch();
    const router = useRouter();
    const { isLoading, error } = useAppSelector(state => state.auth);

    useEffect(() => {
        // Clear any previous errors
        dispatch(clearError());

        // Entrance Animation
        const tl = gsap.timeline();

        tl.fromTo(titleRef.current,
            { y: 20, opacity: 0 },
            { y: 0, opacity: 1, duration: 0.6, ease: 'power2.out' }
        )
            .fromTo(formRef.current,
                { y: 20, opacity: 0 },
                { y: 0, opacity: 1, duration: 0.6, ease: 'power2.out' },
                "-=0.4"
            );
    }, [dispatch]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        const result = await dispatch(loginAsync({ email, password }));

        if (loginAsync.fulfilled.match(result)) {
            // Successfully logged in, redirect to dashboard
            router.push('/dashboard');
        }
    };

    return (
        <main className="min-h-screen bg-[var(--bg)] text-[var(--fg)] selection:bg-[var(--primary)] selection:text-[var(--bg)] flex flex-col">

            <div className="flex-grow flex items-center justify-center px-4 sm:px-6 relative overflow-hidden">
                {/* Background Ambient Glow */}
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-[var(--primary)] rounded-full blur-[150px] opacity-[0.05] pointer-events-none" />

                <div className="w-full max-w-[400px] space-y-8 relative z-10">

                    {/* Header Section */}
                    <div className="text-center space-y-6">
                        <div className="flex flex-col items-center gap-4">
                            <Link href="/">
                                <img
                                    src="/assets/images/keep-up-fixed.svg"
                                    alt="Keep Up Logo"
                                    className="w-48 h-auto object-contain nav-logo"
                                />
                            </Link>
                            <div className="flex items-center gap-2 text-xs font-bold tracking-[0.3em] text-[var(--fg)] opacity-60 uppercase">
                                <span>Stay</span>
                                <Zap className="w-4 h-4 text-[var(--secondary)] fill-[var(--secondary)]" />
                                <span>Ahead</span>
                            </div>
                        </div>

                        <div ref={titleRef} className="opacity-0">
                            <h1 className="text-3xl font-bold tracking-tight text-[var(--fg)]">
                                Welcome
                            </h1>
                            <p className="mt-2 text-sm text-[var(--fg)] opacity-60">
                                Log in to OptimalYou to continue.
                            </p>
                        </div>
                    </div>

                    {/* Card */}
                    <div
                        ref={formRef}
                        className="bg-[var(--card)] backdrop-blur-xl border border-[var(--border)] rounded-lg shadow-2xl p-8"
                    >
                        <form onSubmit={handleSubmit} className="space-y-5">
                            {/* Error Display */}
                            {error && (
                                <div className="bg-red-500/10 border border-red-500/50 rounded-md px-4 py-3 text-red-400 text-sm flex items-start gap-2">
                                    <AlertCircle className="w-5 h-5 shrink-0" />
                                    <div>{error}</div>
                                </div>
                            )}

                            <div className="space-y-1.5">
                                <label className="block text-sm font-bold text-[var(--fg)] ml-1">
                                    Email address<span className="text-[var(--secondary)]">*</span>
                                </label>
                                <input
                                    type="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="w-full bg-[var(--muted)] border border-[var(--border)] rounded-xl px-4 py-3 text-[var(--fg)] placeholder-[var(--fg)]/40 focus:outline-none focus:border-[var(--primary)] focus:ring-1 focus:ring-[var(--primary)] transition-all"
                                    placeholder="Enter your email"
                                    required
                                />
                            </div>

                            <div className="space-y-1.5">
                                <label className="block text-sm font-bold text-[var(--fg)] ml-1">
                                    Password<span className="text-[var(--secondary)]">*</span>
                                </label>
                                <div className="relative">
                                    <input
                                        type={showPassword ? "text" : "password"}
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                        className="w-full bg-[var(--muted)] border border-[var(--border)] rounded-xl px-4 py-3 text-[var(--fg)] placeholder-[var(--fg)]/40 focus:outline-none focus:border-[var(--primary)] focus:ring-1 focus:ring-[var(--primary)] transition-all"
                                        placeholder="Enter your password"
                                        required
                                    />
                                    <button
                                        type="button"
                                        onClick={() => setShowPassword(!showPassword)}
                                        className="absolute inset-y-0 right-0 flex items-center pr-3 text-[var(--fg)] opacity-40 hover:opacity-100 transition-colors"
                                    >
                                        {showPassword ? (
                                            <EyeOff className="h-5 w-5" />
                                        ) : (
                                            <Eye className="h-5 w-5" />
                                        )}
                                    </button>
                                </div>
                            </div>

                            <button
                                type="submit"
                                disabled={isLoading}
                                className="w-full flex justify-center py-3 px-4 border border-transparent rounded-xl shadow-sm text-sm font-bold text-[var(--bg)] bg-[var(--fg)] hover:bg-[var(--primary)] hover:text-[var(--fg)] hover:shadow-[0_0_20px_var(--primary)] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[var(--primary)] disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300"
                            >
                                {isLoading ? 'Authenticating...' : 'Continue'}
                            </button>
                        </form>

                        <div className="mt-6 text-center">
                            <p className="text-sm text-[var(--fg)] opacity-60">
                                Don&apos;t have an account?{' '}
                                <Link href="/register" className="font-medium text-[var(--accent)] hover:text-[var(--primary)] hover:underline">
                                    Sign up
                                </Link>
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Footer */}
            <footer className="py-8 text-center text-sm text-[var(--fg)] opacity-60">
                <div className="space-x-4">
                    <Link href="/terms" className="hover:text-[var(--fg)] hover:underline">Terms of service</Link>
                    <span className="text-[var(--fg)] opacity-40">|</span>
                    <Link href="/privacy" className="hover:text-[var(--fg)] hover:underline">Privacy policy</Link>
                </div>
                <p className="mt-4">
                    &copy; {new Date().getFullYear()} OptimalYou Inc. All rights reserved
                </p>
            </footer>
        </main>
    );
}

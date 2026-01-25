'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import gsap from 'gsap';
import { useAppDispatch, useAppSelector } from '@/redux/hooks';
import { registerAsync, clearError } from '@/redux/slices/authSlice';
import { Eye, EyeOff, Zap, AlertCircle } from 'lucide-react';

export default function RegisterPage() {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);


    const formRef = useRef<HTMLDivElement>(null);
    const rightColRef = useRef<HTMLDivElement>(null);

    const dispatch = useAppDispatch();
    const router = useRouter();
    const { isLoading, error } = useAppSelector(state => state.auth);

    useEffect(() => {
        dispatch(clearError());

        const tl = gsap.timeline();

        tl.fromTo(formRef.current,
            { x: -50, opacity: 0 },
            { x: 0, opacity: 1, duration: 0.8, ease: 'power3.out' }
        )
            .fromTo(rightColRef.current,
                { x: 50, opacity: 0 },
                { x: 0, opacity: 1, duration: 0.8, ease: 'power3.out' },
                "-=0.6"
            );
    }, [dispatch]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();


        const username = name.toLowerCase().replace(/\s+/g, '_');

        const result = await dispatch(registerAsync({
            username,
            email,
            password,
            display_name: name,
        }));

        if (registerAsync.fulfilled.match(result)) {
            router.push('/onboarding');
        }
    };

    return (
        <main className="min-h-screen bg-[var(--bg)] text-[var(--fg)] selection:bg-[var(--primary)] selection:text-[var(--bg)] flex">

            {/* Left Column - Form */}
            <div className="w-full lg:w-1/2 flex flex-col justify-center px-8 sm:px-12 lg:px-20 relative z-10">
                <div ref={formRef} className="max-w-md w-full mx-auto space-y-8 py-12">
                    {/* Logo */}



                    <div>
                        <h1 className="text-3xl font-bold tracking-tight text-[var(--fg)]">
                            Sign up for free
                        </h1>
                        <p className="mt-2 text-sm text-[var(--fg)] opacity-60">
                            Start your journey to your optimal self today.
                        </p>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-5">
                        {error && (
                            <div className="bg-red-500/10 border border-red-500/50 rounded-md px-4 py-3 text-red-400 text-sm flex items-start gap-2">
                                <AlertCircle className="w-5 h-5 shrink-0" />
                                <div>{error}</div>
                            </div>
                        )}

                        <div className="space-y-1.5">
                            <label className="block text-sm font-bold text-[var(--fg)] ml-1">
                                Full Name
                            </label>
                            <input
                                type="text"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                className="w-full bg-[var(--muted)] border border-[var(--border)] rounded-xl px-4 py-3 text-[var(--fg)] placeholder-[var(--fg)]/40 focus:outline-none focus:border-[var(--primary)] focus:ring-1 focus:ring-[var(--primary)] transition-all"
                                placeholder="John Doe"
                                required
                            />
                        </div>

                        <div className="space-y-1.5">
                            <label className="block text-sm font-bold text-[var(--fg)] ml-1">
                                Email address<span className="text-[var(--secondary)]">*</span>
                            </label>
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="w-full bg-[var(--muted)] border border-[var(--border)] rounded-xl px-4 py-3 text-[var(--fg)] placeholder-[var(--fg)]/40 focus:outline-none focus:border-[var(--primary)] focus:ring-1 focus:ring-[var(--primary)] transition-all"
                                placeholder="name@example.com"
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
                                    className="w-full bg-[var(--muted)] border border-[var(--border)] rounded-xl px-4 py-3 text-[var(--fg)] placeholder-[var(--fg)]/40 focus:outline-none focus:border-[var(--primary)] focus:ring-1 focus:ring-[var(--primary)] transition-all pr-10"
                                    placeholder="Create a password"
                                    required
                                />
                                <button
                                    type="button"
                                    onClick={() => setShowPassword(!showPassword)}
                                    className="absolute inset-y-0 right-0 flex items-center pr-3 text-[var(--fg)] opacity-40 hover:opacity-100 transition-opacity"
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
                            {isLoading ? 'Creating Account...' : 'Create Account'}
                        </button>

                        <p className="text-center text-sm text-gray-500 pt-4">
                            Already have an account?{' '}
                            <Link href="/login" className="font-medium text-[var(--accent)] hover:text-[var(--primary)] hover:underline">
                                Log in
                            </Link>
                        </p>
                    </form>
                </div>
            </div>

            {/* Right Column - Value Prop */}
            <div className="hidden lg:flex w-1/2 bg-[var(--muted)] relative overflow-hidden items-center justify-center p-12 border-l border-[var(--border)]">
                {/* Ambient Background */}
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-[var(--primary)] rounded-full blur-[120px] opacity-[0.1]" />
                <div className="absolute bottom-0 right-0 w-[400px] h-[400px] bg-[var(--accent)] rounded-full blur-[100px] opacity-[0.1]" />

                <div ref={rightColRef} className="relative z-10 w-full h-full flex items-center justify-center p-8">
                    <div className="flex flex-col items-center gap-6">
                        <Link href="/">
                            <img
                                src="/assets/images/keep-up-fixed.svg"
                                alt="Keep Up Logo"
                                className="w-full max-w-none h-auto object-contain drop-shadow-[0_0_60px_var(--primary)] filter brightness-110 contrast-125 nav-logo scale-150"
                            />
                        </Link>
                        <div className="flex items-center gap-3 text-2xl font-medium tracking-widest text-[var(--fg)] opacity-60 uppercase">
                            <span>Stay</span>
                            <Zap className="w-8 h-8 text-[var(--secondary)] fill-[var(--secondary)]" />
                            <span>Ahead</span>
                        </div>
                    </div>
                </div>
            </div>

        </main>
    );
}
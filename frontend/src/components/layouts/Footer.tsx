'use client';

import Link from 'next/link';
import { Heart } from 'lucide-react';

export default function Footer() {
    const currentYear = new Date().getFullYear();

    return (
        <footer className="relative bg-black text-white overflow-hidden pt-20 pb-10 border-t border-white/10">
            <div className="max-w-7xl mx-auto px-6 relative z-10">
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-8 mb-20">
                    {/* Brand Column */}
                    <div className="lg:col-span-4 flex flex-col justify-between h-full pr-8">
                        <div>
                            <div className="flex items-center gap-2 mb-6 -ml-4">
                                <div className="relative w-full max-w-[200px] lg:max-w-[300px] flex items-center -ml-2">
                                    <img
                                        src="/assets/images/keep-up-fixed.svg"
                                        alt="Keep Up Logo"
                                        className="w-48 h-auto object-contain"
                                    />
                                </div>
                            </div>
                            <h2 className="text-2xl md:text-3xl font-medium leading-tight text-white mb-8 pl-4">
                                Resolution Resilience.
                                <br />
                                <span className="text-gray-400">Everywhere you grow.</span>
                            </h2>
                        </div>

                        <div className="mt-auto pt-8 pl-4">
                            <p className="text-sm text-gray-500 flex items-center gap-1.5">
                                Built by a gee with
                                <Heart className="w-3.5 h-3.5 text-[#e6ccf5] fill-[#e6ccf5]" />
                            </p>
                        </div>
                    </div>

                    {/* Links Columns */}
                    <div className="lg:col-span-8 grid grid-cols-2 md:grid-cols-4 border-t border-b border-white/10 border-r border-white/10">
                        {/* Platform */}
                        <div className="flex flex-col space-y-6 border-l border-white/10 pl-8 py-8 md:py-2">
                            <h3 className="text-sm font-semibold text-white tracking-wide">Platform</h3>
                            <div className="flex flex-col space-y-4">
                                <Link href="/dashboard" className="text-sm text-gray-400 hover:text-white transition-colors">
                                    Dashboard
                                </Link>
                                <Link href="/performance" className="text-sm text-gray-400 hover:text-white transition-colors">
                                    Performance
                                </Link>
                                <Link href="/growth" className="text-sm text-gray-400 hover:text-white transition-colors">
                                    Growth
                                </Link>
                                <Link href="/intelligence" className="text-sm text-gray-400 hover:text-white transition-colors">
                                    Intelligence
                                </Link>
                            </div>
                        </div>

                        {/* Company */}
                        <div className="flex flex-col space-y-6 border-l border-white/10 pl-8 py-8 md:py-2">
                            <h3 className="text-sm font-semibold text-white tracking-wide">Company</h3>
                            <div className="flex flex-col space-y-4">
                                <Link href="/about" className="text-sm text-gray-400 hover:text-white transition-colors">
                                    About Us
                                </Link>
                                <Link href="/careers" className="text-sm text-gray-400 hover:text-white transition-colors">
                                    Careers
                                </Link>
                                <Link href="/contact" className="text-sm text-gray-400 hover:text-white transition-colors">
                                    Contact
                                </Link>
                            </div>
                        </div>

                        {/* Legal */}
                        <div className="flex flex-col space-y-6 border-l border-white/10 pl-8 py-8 md:py-2">
                            <h3 className="text-sm font-semibold text-white tracking-wide">Legal</h3>
                            <div className="flex flex-col space-y-4">
                                <Link href="/privacy" className="text-sm text-gray-400 hover:text-white transition-colors">
                                    Privacy Policy
                                </Link>
                                <Link href="/terms" className="text-sm text-gray-400 hover:text-white transition-colors">
                                    Terms of Service
                                </Link>
                            </div>
                        </div>

                        {/* Connect */}
                        <div className="flex flex-col space-y-6 border-l border-white/10 pl-8 py-8 md:py-2">
                            <h3 className="text-sm font-semibold text-white tracking-wide">Connect</h3>
                            <div className="flex flex-col space-y-4">
                                <Link href="https://twitter.com" target="_blank" className="text-sm text-gray-400 hover:text-white transition-colors">
                                    X (Twitter)
                                </Link>
                                <Link href="https://linkedin.com" target="_blank" className="text-sm text-gray-400 hover:text-white transition-colors">
                                    LinkedIn
                                </Link>
                                <Link href="https://instagram.com" target="_blank" className="text-sm text-gray-400 hover:text-white transition-colors">
                                    Instagram
                                </Link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Bottom Copyright Line */}
            <div className="relative z-10 max-w-7xl mx-auto px-6 border-t border-white/10 pt-8 mt-8 flex flex-col md:flex-row justify-between items-center gap-4">
                <p className="text-xs text-gray-600 uppercase">
                    © {currentYear} KEEP-UP. All rights reserved.
                </p>
            </div>
        </footer>
    );
}

export default function DebateHeader() {
    return (
        <div className="space-y-6">
            <h1 className="text-6xl md:text-7xl font-black tracking-tighter text-[var(--fg)] leading-[0.9]">
                The Council is <br />
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-[var(--primary)] to-[var(--accent)]">
                    Deliberating.
                </span>
            </h1>
            <p className="text-xl text-[var(--fg)] opacity-60 max-w-2xl border-l-2 border-[var(--primary)] pl-6">
                Watch as specialized AI agents debate, challenge, and refine your optimal plan in real-time.
            </p>
        </div>
    );
}

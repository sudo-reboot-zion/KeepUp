import type { AgentMessage } from '@/types/debate.types';
import type { DebateSummary } from '@/types/onboarding.types';
import { clean } from './textParser';

/**
 * Build message timeline from debate data
 */
export function buildMessageTimeline(debateData: DebateSummary | null): AgentMessage[] {
    if (!debateData) return [];

    const timeline: AgentMessage[] = [];

    // Add Goal Setting Agent's proposal
    debateData.agents?.forEach((agent, index) => {
        if (agent.agent === 'Goal Setting Agent' && agent.proposal) {
            timeline.push({
                id: `msg-${index}-proposal`,
                agent: agent.agent,
                role: agent.role,
                message: `I've analyzed your goal. Here's my recommendation:\n\n**Goal:** ${agent.proposal.interpreted_goal}\n**Weekly Target:** ${agent.proposal.weekly_target}\n**First Milestone:** ${agent.proposal.first_milestone}\n\n**Reasoning:** ${agent.proposal.reasoning}`,
                type: 'proposal',
                timestamp: Date.now() + index * 1000,
            });
        }

        // Add Failure Pattern Agent's challenge
        if (agent.agent === 'Failure Pattern Agent') {
            if (agent.analysis) {
                timeline.push({
                    id: `msg-${index}-analysis`,
                    agent: agent.agent,
                    role: agent.role,
                    message: `**Challenge Initiated**\n\nI've detected some concerning patterns:\n\n${agent.analysis.identified_patterns?.map(p => `• ${p}`).join('\n')}\n\n**Quit Probability:** ${Math.round((agent.analysis.quit_probability || 0) * 100)}%\n\n**My Concerns:**\n${agent.analysis.plan_concerns?.map(c => `• ${c}`).join('\n')}`,
                    type: 'challenge',
                    timestamp: Date.now() + (index + 1) * 1000,
                });
            }

            if (agent.challenge) {
                const stance = clean(agent.challenge.stance);
                const reasoning = clean(agent.challenge.reasoning);
                const counter = clean(agent.challenge.counter_proposal);

                const challengeMessage = [
                    stance ? `**${stance}**` : null,
                    reasoning,
                    counter ? `**Counter-Proposal:** ${counter}` : null
                ].filter(Boolean).join('\n\n');

                if (challengeMessage) {
                    timeline.push({
                        id: `msg-${index}-challenge`,
                        agent: agent.agent,
                        role: agent.role,
                        message: challengeMessage,
                        type: 'challenge',
                        timestamp: Date.now() + (index + 2) * 1000,
                    });
                }
            }
        }
    });

    // Add Meta-Coordinator synthesis
    if (debateData.synthesis) {
        timeline.push({
            id: 'synthesis',
            agent: 'Meta-Coordinator',
            role: 'The Judge',
            message: `**Synthesis Complete**\n\n${debateData.synthesis}\n\n${debateData.safety_adjustments && debateData.safety_adjustments.length > 0 ? `**Safety Adjustments Made:**\n${debateData.safety_adjustments.map(a => `• ${a}`).join('\n')}` : ''}`,
            type: 'synthesis',
            timestamp: Date.now() + timeline.length * 1000,
        });
    }

    return timeline;
}

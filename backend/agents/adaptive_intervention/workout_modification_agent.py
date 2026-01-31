"""
ENHANCED Workout Modification Agent
The safety cornerstone - prevents injuries with real biomechanical intelligence
"""
from typing import Dict, Any, List, Optional
from agents.base_agent import BaseAgent
from tools.rag_tool import rag_tool
from tools.tavily_search_tool import tavily_tool
from datetime import datetime
from agents.constraint_framework import INDIVIDUAL_AGENT_PROMPT


class WorkoutModificationAgent(BaseAgent):
    """
    Elite exercise science expert with:
    - RAG for injury prevention protocols
    - Tavily for latest research
    - Biomechanical risk assessment
    - Transparent reasoning
    - High confidence scoring
    """
    
    def __init__(self):
        super().__init__(
            name="Workout Modification Agent",
            description="Exercise science expert. Modifies workouts to prevent injury using cutting-edge research.",
            model="llama-3.3-70b-versatile"
        )
        
        # Risk thresholds
        self.SAFETY_SCORE_MIN = 0.7  # Below this = must modify
        self.HIGH_RISK_EXERCISES = [
            "barbell back squat", "deadlift", "overhead press",
            "clean and jerk", "snatch", "box jumps"
        ]
    
    async def analyze(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive workout safety analysis
        
        Flow:
        1. Identify all risk factors
        2. Query RAG for safety protocols
        3. Query Tavily for latest research (if needed)
        4. Generate modifications with reasoning
        5. Calculate confidence scores
        """
        
        # Extract inputs
        user_profile = input_data.get("user_profile", {})
        workout_plan = input_data.get("workout_plan", [])
        context = input_data.get("context", {})
        user_memory = input_data.get("user_memory", {})
        
        # Step 1: Comprehensive risk assessment
        risk_assessment = await self._comprehensive_risk_assessment(
            user_profile, workout_plan, context
        )
        
        # Step 2: Query knowledge sources
        safety_knowledge = await self._get_comprehensive_safety_knowledge(
            risk_assessment, user_profile
        )
        
        # Step 3: Generate modifications
        modifications = await self._generate_modifications(
            user_profile, workout_plan, context, 
            risk_assessment, safety_knowledge, user_memory
        )
        
        # Step 4: Calculate overall safety score
        safety_score = self._calculate_safety_score(
            modifications.get("modified_workout", []),
            risk_assessment
        )
        
        return {
            "modified": modifications.get("modified", False),
            "modified_workout": modifications.get("modified_workout", workout_plan),
            "modifications": modifications.get("modifications", []),
            "risk_assessment": risk_assessment,
            "safety_score": safety_score,
            "confidence": modifications.get("confidence", 0.0),
            "reasoning": modifications.get("reasoning", ""),
            "knowledge_sources": safety_knowledge.get("sources", []),
            "agent_name": self.name
        }
    
    async def _comprehensive_risk_assessment(
        self,
        user_profile: Dict[str, Any],
        workout_plan: List[Dict],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Multi-dimensional risk assessment
        """
        
        risk_factors = {
            "user_risks": [],
            "context_risks": [],
            "exercise_risks": [],
            "interaction_risks": []
        }
        
        # User-specific risks
        past_injuries = user_profile.get("past_injuries", [])
        if past_injuries:
            risk_factors["user_risks"].extend([
                {"type": "injury_history", "detail": injury, "severity": 0.7}
                for injury in past_injuries
            ])
        
        age = user_profile.get("age", 30)
        if age > 50:
            risk_factors["user_risks"].append({
                "type": "age", "detail": f"Age {age} - slower recovery", "severity": 0.5
            })
        elif age < 20:
            risk_factors["user_risks"].append({
                "type": "age", "detail": "Growth plate considerations", "severity": 0.3
            })
        
        fitness_level = user_profile.get("fitness_level", "beginner")
        if fitness_level == "beginner":
            risk_factors["user_risks"].append({
                "type": "fitness_level", "detail": "Beginner - form risk", "severity": 0.6
            })
        
        # Context risks
        sleep_quality = context.get("sleep_quality", 3)
        if sleep_quality <= 2:
            risk_factors["context_risks"].append({
                "type": "sleep", "detail": f"Poor sleep quality ({sleep_quality}/5)", "severity": 0.8
            })
        elif sleep_quality == 3:
            risk_factors["context_risks"].append({
                "type": "sleep", "detail": f"Average sleep quality ({sleep_quality}/5)", "severity": 0.4
            })
        
        stress_level = context.get("stress_level", "low")
        if stress_level == "high":
            risk_factors["context_risks"].append({
                "type": "stress", "detail": "High stress - cortisol elevated", "severity": 0.7
            })
        
        days_inactive = context.get("days_since_last_workout", 1)
        if days_inactive > 7:
            risk_factors["context_risks"].append({
                "type": "detraining", "detail": f"{days_inactive} days inactive", "severity": 0.6
            })
        
        # Exercise-specific risks
        for exercise in workout_plan:
            exercise_name = exercise.get("name", "").lower()
            
            # Check against high-risk list
            if any(risky in exercise_name for risky in self.HIGH_RISK_EXERCISES):
                risk_factors["exercise_risks"].append({
                    "type": "high_risk_movement",
                    "exercise": exercise.get("name"),
                    "detail": "Complex compound requiring technical proficiency",
                    "severity": 0.8
                })
            
            # Check if exercise conflicts with injury history
            for injury in past_injuries:
                if self._exercise_conflicts_with_injury(exercise_name, injury):
                    risk_factors["interaction_risks"].append({
                        "type": "injury_conflict",
                        "exercise": exercise.get("name"),
                        "injury": injury,
                        "severity": 0.9
                    })
        
        # Calculate overall risk score
        all_risks = (
            risk_factors["user_risks"] + 
            risk_factors["context_risks"] + 
            risk_factors["exercise_risks"] + 
            risk_factors["interaction_risks"]
        )
        
        if all_risks:
            avg_severity = sum(r["severity"] for r in all_risks) / len(all_risks)
        else:
            avg_severity = 0.1
        
        risk_factors["overall_risk_score"] = avg_severity
        risk_factors["total_risk_factors"] = len(all_risks)
        
        return risk_factors
    
    def _exercise_conflicts_with_injury(self, exercise: str, injury: str) -> bool:
        """Check if exercise stresses injured area"""
        conflict_map = {
            "knee": ["squat", "lunge", "leg press", "jump"],
            "shoulder": ["overhead press", "bench press", "pull-up", "row"],
            "back": ["deadlift", "squat", "row", "hyperextension"],
            "ankle": ["jump", "run", "calf raise"],
            "wrist": ["push-up", "plank", "overhead press"]
        }
        
        injury_lower = injury.lower()
        for body_part, exercises in conflict_map.items():
            if body_part in injury_lower:
                return any(ex in exercise for ex in exercises)
        
        return False
    
    async def _get_comprehensive_safety_knowledge(
        self,
        risk_assessment: Dict[str, Any],
        user_profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Query both RAG and Tavily for safety knowledge
        """
        
        knowledge_parts = []
        sources = []
        
        # Extract unique risk types
        all_risks = (
            risk_assessment.get("user_risks", []) +
            risk_assessment.get("context_risks", []) +
            risk_assessment.get("exercise_risks", []) +
            risk_assessment.get("interaction_risks", [])
        )
        
        risk_types = set(r.get("type") for r in all_risks)
        
        # Query RAG for each risk type
        for risk_type in list(risk_types)[:3]:  # Limit to 3 to avoid rate limits
            if risk_type == "injury_history":
                injuries = [r["detail"] for r in all_risks if r["type"] == "injury_history"]
                for injury in injuries[:2]:
                    result = await rag_tool.search_fitness(
                        f"{injury} injury prevention exercise modification", k=2
                    )
                    if result.get("success"):
                        knowledge_parts.append(result.get("context", ""))
                        sources.extend(result.get("sources", []))
            
            elif risk_type == "sleep":
                result = await rag_tool.search_recovery(
                    "exercise modification poor sleep recovery", k=2
                )
                if result.get("success"):
                    knowledge_parts.append(result.get("context", ""))
                    sources.extend(result.get("sources", []))
            
            elif risk_type == "high_risk_movement":
                exercises = [r["exercise"] for r in all_risks if r["type"] == "high_risk_movement"]
                for ex in exercises[:2]:
                    result = await rag_tool.search_fitness(
                        f"{ex} safety form cues injury prevention", k=2
                    )
                    if result.get("success"):
                        knowledge_parts.append(result.get("context", ""))
                        sources.extend(result.get("sources", []))
        
        # Use Tavily for latest research if high risk
        if risk_assessment.get("overall_risk_score", 0) > 0.7:
            tavily_result = await tavily_tool.search_fitness_research(
                "exercise modification injury prevention latest guidelines"
            )
            if tavily_result.get("success"):
                tavily_summary = tavily_result.get("answer", "")
                if tavily_summary:
                    knowledge_parts.append(f"LATEST RESEARCH:\n{tavily_summary}")
                    sources.append("Tavily (latest research)")
        
        combined_knowledge = "\n\n---\n\n".join(knowledge_parts)
        
        return {
            "knowledge": combined_knowledge if combined_knowledge else "No specific guidelines found.",
            "sources": list(set(sources))
        }
    
    async def _generate_modifications(
        self,
        user_profile: Dict[str, Any],
        workout_plan: List[Dict],
        context: Dict[str, Any],
        risk_assessment: Dict[str, Any],
        safety_knowledge: Dict[str, Any],
        user_memory: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Generate workout modifications with LLM"""
        
        system_prompt = self._build_comprehensive_system_prompt(
            safety_knowledge.get("knowledge", "")
        )
        
        user_prompt = self._build_comprehensive_user_prompt(
            user_profile, workout_plan, context, risk_assessment, user_memory
        )
        
        response = await self._call_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.1,  # Very low for safety-critical
            max_tokens=2000
        )
        
        return self._parse_json_response(response)
    
    def _build_comprehensive_system_prompt(self, knowledge: str) -> str:
        """Build system prompt with all safety knowledge"""
        constraint_prompt = INDIVIDUAL_AGENT_PROMPT.format(
            agent_name="Workout Modification Agent",
            specialty="preventing injuries through evidence-based exercise modification"
        )
        return constraint_prompt + f"""

You are an elite exercise physiologist and injury prevention specialist.

Your mandate: SAFETY FIRST. If in doubt, modify to be safer.

Scientific knowledge base:
{knowledge}

CRITICAL MODIFICATION RULES:
1. Past injury = NEVER stress that area (provide alternatives)
2. Poor sleep (<6h) = Reduce intensity 40-50% OR convert to active recovery
3. Beginner + complex movement = Replace with simpler alternative
4. High stress + high intensity = Recipe for injury, reduce both
3. Beginner + complex movement = Replace with simpler alternative
4. High stress + high intensity = Recipe for injury, reduce both
5. 7+ days inactive = Reduce volume 30%, focus on re-acclimation
6. MEMORY: Respect user feedback (e.g., "hates lunges") and failure patterns.

Response format (JSON only):
{{
    "modified": true,
    "modified_workout": [
        {{
            "name": "Exercise name",
            "sets": 3,
            "reps": 10,
            "intensity": "moderate",
            "form_cues": ["specific cue 1", "cue 2"],
            "alternatives": ["if this doesn't work, try..."]
        }}
    ],
    "modifications": [
        "Changed X to Y because [specific biomechanical reason]"
    ],
    "reasoning": "Detailed explanation of decision-making process with citations",
    "safety_score": 0.85,
    "confidence": 0.90
}}

Safety score scale:
0.9-1.0: Very safe, minimal risk
0.7-0.9: Safe with proper form
0.5-0.7: Moderate risk, modifications needed
<0.5: High risk, major changes required"""
    
    def _build_comprehensive_user_prompt(
        self,
        user_profile: Dict[str, Any],
        workout_plan: List[Dict],
        context: Dict[str, Any],
        risk_assessment: Dict[str, Any],
        user_memory: Dict[str, Any] = None
    ) -> str:
        """Build detailed analysis prompt"""
        
        workout_text = "\n".join([
            f"- {ex.get('name')}: {ex.get('sets')}x{ex.get('reps')}"
            for ex in workout_plan
        ])
        
        risks_text = "\n".join([
            f"⚠️ [{r.get('type')}] {r.get('detail')} (severity: {r.get('severity'):.2f})"
            for category in ["user_risks", "context_risks", "exercise_risks", "interaction_risks"]
            for r in risk_assessment.get(category, [])
        ])
        
        return f"""COMPREHENSIVE SAFETY ANALYSIS REQUEST

USER PROFILE:
- Fitness Level: {user_profile.get('fitness_level', 'unknown')}
- Age: {user_profile.get('age', 'unknown')}
- Past Injuries: {', '.join(user_profile.get('past_injuries', [])) or 'None'}

CURRENT CONTEXT:
- Sleep: {context.get('sleep_hours', 'unknown')}h
- Stress: {context.get('stress_level', 'unknown')}
- Days Inactive: {context.get('days_since_last_workout', 'unknown')}

RISK ASSESSMENT (Overall Risk: {risk_assessment.get('overall_risk_score', 0):.2f}):
{risks_text}

USER MEMORY & FEEDBACK:
{self._format_memory_for_prompt(user_memory)}

PROPOSED WORKOUT:
{workout_text}

YOUR TASK:
1. For EACH exercise, assess if it's safe given the risk profile
2. If unsafe, provide a SPECIFIC alternative with biomechanical rationale
3. Adjust volume/intensity based on context
4. Provide detailed form cues for injury prevention
5. Cite research from the knowledge base when making decisions

Generate the JSON response with modifications."""
    
    def _calculate_safety_score(
        self,
        modified_workout: List[Dict],
        risk_assessment: Dict[str, Any]
    ) -> float:
        """Calculate overall safety score of final workout"""
        
        base_score = 1.0
        
        # Deduct for remaining risks
        overall_risk = risk_assessment.get("overall_risk_score", 0)
        base_score -= (overall_risk * 0.3)
        
        # Deduct if high-risk exercises remain
        for exercise in modified_workout:
            name = exercise.get("name", "").lower()
            if any(risky in name for risky in self.HIGH_RISK_EXERCISES):
                base_score -= 0.1
        
        return max(0.1, min(1.0, base_score))

    def _format_memory_for_prompt(self, memory: Dict[str, Any]) -> str:
        """Format memory for prompt"""
        if not memory:
            return "No specific past feedback."
            
        lines = []
        
        # Feedback
        feedback = memory.get("by_type", {}).get("feedback", [])
        if feedback:
            lines.append("PAST FEEDBACK:")
            for item in feedback[:3]:
                content = item.get("content", {})
                lines.append(f"- {content.get('feedback', '')} (Confidence: {item.get('confidence', 0):.2f})")
        
        # Failure patterns
        failures = memory.get("by_type", {}).get("failure_pattern", [])
        if failures:
            lines.append("FAILURE PATTERNS:")
            for item in failures[:2]:
                content = item.get("content", {})
                lines.append(f"- {content.get('pattern', '')}")
                
        return "\n".join(lines) if lines else "No relevant memory found."



workout_modification_agent = WorkoutModificationAgent()
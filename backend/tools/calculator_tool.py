"""
Calculator Tool
Safe mathematical operations for agents.
"""
import math

class CalculatorTool:
    """
    Provides safe mathematical operations for agents.
    Useful for macro calculations, calorie deficits, etc.
    """
    
    @staticmethod
    def calculate_macros(calories: int, protein_pct: float, fat_pct: float, carb_pct: float) -> dict:
        """
        Calculate grams of macros based on calories and percentages.
        """
        if not math.isclose(protein_pct + fat_pct + carb_pct, 1.0, rel_tol=0.01):
            raise ValueError("Percentages must sum to 1.0")
            
        protein_cals = calories * protein_pct
        fat_cals = calories * fat_pct
        carb_cals = calories * carb_pct
        
        return {
            "protein_g": round(protein_cals / 4),
            "fats_g": round(fat_cals / 9),
            "carbs_g": round(carb_cals / 4)
        }
    
    @staticmethod
    def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> int:
        """
        Calculate BMR using Mifflin-St Jeor equation.
        """
        # Mifflin-St Jeor
        s = 5 if gender.lower() == "male" else -161
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + s
        return round(bmr)

    @staticmethod
    def calculate_tdee(bmr: int, activity_level: str) -> int:
        """
        Calculate TDEE based on activity level.
        """
        multipliers = {
            "sedentary": 1.2,
            "light": 1.375,
            "moderate": 1.55,
            "active": 1.725,
            "very_active": 1.9
        }
        multiplier = multipliers.get(activity_level.lower(), 1.2)
        return round(bmr * multiplier)

calculator_tool = CalculatorTool()

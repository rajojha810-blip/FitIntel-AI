import sys 
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from progress_analytics import get_daily_metrics, analyze_weight, analyze_protein, analyze_calories_and_steps

def generate_insights():
    data = get_daily_metrics()
    
    weight_data = analyze_weight(data)
    protein_data = analyze_protein(data)
    activity_data = analyze_calories_and_steps(data)
    
    insights = []

    # 1. Weight Rule
    weight_change = weight_data["Weight Change"]
    if weight_change < 0:
        insights.append(f" Positive Progress: Total weight lost is {abs(weight_change)} kg.")
    elif weight_change == 0:
        insights.append(" Weight Plateau: Your weight has remained static.")
    else:
        insights.append(f"Weight Gain: Weight increased by {weight_change} kg.")

    # 2. Protein Rule (Target: 130g)
    target_protein = 130
    avg_protein = protein_data["Average Protein"]
    if avg_protein < target_protein:
        deficit = round(target_protein - avg_protein, 2)
        insights.append(f" Protein Deficit: Avg protein is {avg_protein}g (Short by {deficit}g/day).")
    else:
        insights.append(f" Protein Target Met: Avg protein intake is {avg_protein}g.")

    # 3. Steps Rule (Target: 8000 Steps)
    target_steps = 8000
    avg_steps = activity_data["Average Steps"]
    if avg_steps < target_steps:
        insights.append(f"🚶 Activity Alert: Avg daily steps ({avg_steps}) are below the 8,000 target.")
    else:
        insights.append(f"🔥 Active Routine: Daily steps avg ({avg_steps}) is on point!")

    return insights

if __name__ == "__main__":
    print("\n==========================================")
    print("      FITINTEL AUTOMATED INSIGHTS ENGINE   ")
    print("==========================================\n")
    
    results = generate_insights()
    for index, insight in enumerate(results, 1):
        print(f"{index}. {insight}")
        
    print("\n==========================================\n")
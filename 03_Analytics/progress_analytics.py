from db_connection import get_connection
import pandas as pd

# 1. DATABASE FETCHING FUNCTION
def get_daily_metrics():
    connection = get_connection()
    query = """
    SELECT *
    FROM daily_metrics
    WHERE user_id = 1
    ORDER BY date;
    """
    df = pd.read_sql(query, connection)
    connection.close()
    return df

# 2. WEIGHT ANALYTICS FUNCTION
def analyze_weight(data):
    starting_weight = data["weight_kg"].iloc[0]
    current_weight = data["weight_kg"].iloc[-1]
    weight_change = current_weight - starting_weight
    average_weight = data["weight_kg"].mean()

    return {
        "Starting Weight": round(starting_weight, 2),
        "Current Weight": round(current_weight, 2),
        "Weight Change": round(weight_change, 2),
        "Average Weight": round(average_weight, 2)
    }

# 3. PROTEIN ANALYTICS FUNCTION
def analyze_protein(data):
    average_protein = data["protein_consumed_g"].mean()
    highest_protein = data["protein_consumed_g"].max()
    lowest_protein = data["protein_consumed_g"].min()

    return {
        "Average Protein": round(average_protein, 2),
        "Highest Protein": round(highest_protein, 2),
        "Lowest Protein": round(lowest_protein, 2)
    }

# 4. CALORIES & STEPS ANALYTICS FUNCTION
def analyze_calories_and_steps(data):
    average_calories = data["calories_consumed"].mean()
    average_steps = data["steps"].mean()
    highest_steps = data["steps"].max()

    return {
        "Average Calories": round(average_calories, 2),
        "Average Steps": round(average_steps),
        "Highest Steps": highest_steps
    }

# 5. MAIN EXECUTION (NO TABLE PRINTING TO PREVENT TERMINAL FREEZE)
if __name__ == "__main__":
    data = get_daily_metrics()

    print("\n==========================================")
    print(f"   FITINTEL ANALYTICS SUMMARY ({len(data)} Records)")
    print("==========================================")

    # Weight
    print("\n[1] WEIGHT ANALYSIS:")
    for k, v in analyze_weight(data).items():
        print(f" - {k}: {v}")

    # Protein
    print("\n[2] PROTEIN ANALYSIS:")
    for k, v in analyze_protein(data).items():
        print(f" - {k}: {v}")

    # Activity
    print("\n[3] CALORIES & STEPS ANALYSIS:")
    for k, v in analyze_calories_and_steps(data).items():
        print(f" - {k}: {v}")
    
    print("\n==========================================\n")
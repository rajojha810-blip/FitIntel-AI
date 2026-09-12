from db_connection import get_connection
import pandas as pd


def get_user_data():

    connection = get_connection()

    query = """
    SELECT *
    FROM users
    WHERE user_id = 1;
    """

    df = pd.read_sql(query, connection)

    connection.close()

    return df


def calculate_bmr(weight, height, age, gender):

    if gender.lower() == "male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    return round(bmr, 2)


def calculate_tdee(bmr, activity_level):

    activity_multipliers = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725
    }

    multiplier = activity_multipliers.get(activity_level, 1.2)

    return round(bmr * multiplier, 2)


def calculate_targets(weight, height, age, gender, activity_level, goal):

    bmr = calculate_bmr(weight, height, age, gender)

    tdee = calculate_tdee(bmr, activity_level)

    if goal.lower() == "fat loss":
        target_calories = tdee - 400
    elif goal.lower() == "muscle gain":
        target_calories = tdee + 250
    else:
        target_calories = tdee

    protein_target = weight * 1.8

    return {
        "BMR": round(bmr),
        "TDEE": round(tdee),
        "Target Calories": round(target_calories),
        "Protein Target": round(protein_target)
    }


if __name__ == "__main__":

    user = get_user_data().iloc[0]

    results = calculate_targets(
        user["initial_weight_kg"],
        user["height_cm"],
        user["age"],
        user["gender"],
        user["activity_level"],
        user["goal"]
    )

    print("\n===== FITINTEL CALCULATION ENGINE =====\n")

    for key, value in results.items():
        print(f"{key}: {value}")
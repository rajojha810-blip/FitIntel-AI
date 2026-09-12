import sys
import os
import importlib.util

# Load 03_Analytics modules dynamically
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load rule_engine
rule_engine_path = os.path.join(base_path, "03_Analytics", "rule_engine.py")
spec = importlib.util.spec_from_file_location("rule_engine", rule_engine_path)
rule_engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rule_engine)

# Load progress_analytics
analytics_path = os.path.join(base_path, "03_Analytics", "progress_analytics.py")
spec2 = importlib.util.spec_from_file_location("progress_analytics", analytics_path)
progress_analytics = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(progress_analytics)


def generate_ai_coaching_feedback():
    insights = rule_engine.generate_insights()
    data = progress_analytics.get_daily_metrics()
    weight_summary = progress_analytics.analyze_weight(data)
    
    current_w = weight_summary["Current Weight"]
    weight_diff = weight_summary["Weight Change"]

    print("\n" + "="*50)
    print("           FITINTEL AI COACH FEEDBACK        ")
    print("="*50 + "\n")

    print(f"🤖 AI Coach: 'Hello User! Here is your personal assessment based on your recent activity log.'\n")
    print(f"📌 Current Status: {current_w} kg (Overall Change: {weight_diff} kg)\n")
    
    print("💡 Key Action Items For You Today:")
    for idx, rule in enumerate(insights, 1):
        print(f"  {idx}. {rule}")
        
    print("\n🏋️ Coach Tip:")
    if weight_diff < 0:
        print("  'Great momentum! Keep your protein intake high to retain muscle mass while losing weight.'")
    else:
        print("  'Focus on increasing daily non-exercise activity (steps) and maintaining a consistent calorie deficit.'")

    print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    generate_ai_coaching_feedback()
import os
import subprocess

def run_planner(high_temp_triggered=False):
    try:
        env = os.environ.copy()
        env["PYTHONWARNINGS"] = "ignore"
        env["PYTHONLOGLEVEL"] = "WARNING"

        result = subprocess.run(
            ["pyperplan", "-s", "astar", "-H", "hff", "smart_domain.pddl", "problem.pddl"],
            capture_output=True, text=True, timeout=10, env=env
        )

        output = result.stdout.lower() + result.stderr.lower()

        if "plan length:" in output:
            if high_temp_triggered:
                print("FIRE PLAN FOUND by AI planner.")
            else:
                print("ALERT PLAN FOUND by AI planner.")
            return ["activate-safety"]
        else:
            print("SAFE PLAN FOUND by AI planner.")
            return []

    except Exception as e:
        print(f"Planner error: {e}")
        return []

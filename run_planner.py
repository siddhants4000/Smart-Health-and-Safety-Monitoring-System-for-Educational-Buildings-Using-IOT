import os
import subprocess

def run_planner():
    try:
        env = os.environ.copy()
        env["PYTHONWARNINGS"] = "ignore"
        env["PYTHONLOGLEVEL"] = "WARNING"

        result = subprocess.run(
            ["pyperplan", "-s", "astar", "-H", "hff", "smart_domain.pddl", "problem.pddl"],
            capture_output=True, text=True, timeout=10, env=env
        )

        output = result.stdout.lower() + result.stderr.lower()
        #print("?? PLANNER OUTPUT:\n", output)

        if "plan length:" in output:
            print("?? PLAN FOUND by AI planner.")
            return ["activate-safety"]
        else:
            print("?? NO PLAN FOUND.")
            return []

    except Exception as e:
        print(f"? Planner error: {e}")
        return []

def generate_problem_file(state):
    with open("problem.pddl", "w") as f:
        f.write("(define (problem building-scenario)\n")
        f.write("  (:domain smart-building)\n")
        f.write("  (:init\n")
        if state.get("dark"):
            f.write("    (dark)\n")
        if state.get("motion_detected"):
            f.write("    (motion-detected)\n")
        if state.get("sound_detected"):
            f.write("    (sound-detected)\n")
        f.write("    (led-off)\n")
        f.write("    (buzzer-off)\n")
        f.write("  )\n")
        f.write("  (:goal (and (led-on) (buzzer-on)))\n")
        f.write(")\n")


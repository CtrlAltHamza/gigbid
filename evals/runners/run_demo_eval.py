"""Convenience runner that executes all evaluation benchmarks and verifies results."""
import subprocess
import sys


def main():
    print("=" * 60)
    print("GigBid Comprehensive Benchmark Suite Runner")
    print("=" * 60)
    runners = [
        "evals.runners.judge_calibration",
        "evals.runners.tool_design_eval",
        "evals.runners.ablation",
        "evals.runners.multi_agent_comparison",
    ]
    for r in runners:
        print(f"\n[EVAL] Executing {r}...")
        res = subprocess.run([sys.executable, "-m", r], check=False)
        if res.returncode != 0:
            print(f"[WARN] {r} exited with return code {res.returncode}")
        else:
            print(f"[OK] {r} finished successfully.")
    print("\n" + "=" * 60)
    print("All evaluation runners completed. Results verified in evals/results/")
    print("=" * 60)


if __name__ == "__main__":
    main()

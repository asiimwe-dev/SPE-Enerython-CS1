from pathlib import Path

from .dashboard import run_dashboard


def main():
    paths = run_dashboard()
    print("Report generated:")
    for p in paths:
        print(f"  {p}")


if __name__ == "__main__":
    main()

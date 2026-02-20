# main.py
from graph.review_graph import run_review

if __name__ == "__main__":
    pr_url = input("Enter GitHub URL: ").strip()
    report = run_review(pr_url)
    print(report)

    # Save report
    from datetime import datetime
    filename = f"review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\nReport saved to: {filename}")

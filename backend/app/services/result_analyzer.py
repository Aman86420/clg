from typing import List

def analyze_results(results: List[dict]) -> dict:
    if not results:
        return {"average_score": 0, "total_attempts": 0, "best_score": 0}
    
    scores = [r["score"] for r in results]
    return {
        "average_score": sum(scores) / len(scores),
        "total_attempts": len(results),
        "best_score": max(scores),
        "latest_score": scores[-1] if scores else 0
    }

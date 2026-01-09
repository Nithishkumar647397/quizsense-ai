
---

## 📄 FILE 4: prompts/weekly_report.md

**Location:** `quizsense-ai/prompts/weekly_report.md`

```markdown
# Weekly Report Generation Task

Generate a personalized weekly learning report based on performance data.

## Report Sections

### 1. Summary (2-3 sentences)
- Overall performance snapshot
- Key achievement or main challenge
- Encouraging opening

### 2. Strengths (What's going well)
- Topics with high accuracy (>75%)
- Improvements from previous period
- Positive patterns observed

### 3. Areas for Improvement
- Topics with low accuracy (<60%)
- Specific concepts causing difficulty
- Why these might be challenging

### 4. Patterns Observed
- Learning behavior insights
- Time management observations
- Consistency notes

### 5. Next Week's Focus
- Top 3 topics to prioritize
- Specific sub-concepts to review
- Suggested difficulty progression

### 6. Motivation
- Growth mindset message
- Acknowledgment of effort
- Realistic encouragement

## Output Format

Return ONLY valid JSON in this exact format:

```json
{
    "summary": "Great effort this week! You completed 7 quizzes with 72% overall accuracy. Your understanding of Functions has improved significantly.",
    "overall_accuracy": 72.0,
    "quizzes_completed": 7,
    "strong_topics": ["Functions", "Variables", "Loops"],
    "weak_topics": ["Recursion", "OOP"],
    "improved_topics": ["Functions"],
    "declined_topics": [],
    "patterns": [
        {
            "type": "strength",
            "description": "Consistent daily practice",
            "evidence": "Completed quiz every day this week",
            "recommendation": "Keep up this excellent habit!"
        },
        {
            "type": "weakness",
            "description": "Struggling with recursive thinking",
            "evidence": "40% accuracy on recursion questions",
            "recommendation": "Try breaking down recursive problems step by step"
        }
    ],
    "focus_topics": ["Recursion", "OOP Basics", "Exception Handling"],
    "recommendations": [
        "Spend 15 minutes daily on recursion exercises",
        "Review class and object concepts in OOP",
        "Practice tracing through recursive function calls"
    ],
    "motivation": "You're making real progress! Remember, recursion is challenging for everyone at first. Your consistent practice will pay off.",
    "full_report": "# Weekly Learning Report 📊\n\n## Overview\nGreat effort this week! You completed 7 quizzes with an overall accuracy of 72%.\n\n## 💪 Strengths\n- **Functions**: Excellent improvement! (85% accuracy)\n- **Variables**: Solid understanding (90% accuracy)\n- **Loops**: Strong performance (80% accuracy)\n\n## 📈 Areas for Improvement\n- **Recursion**: Your biggest challenge area (40% accuracy)\n  - Focus on understanding base cases\n  - Practice tracing through recursive calls\n\n- **OOP Concepts**: Needs more practice (55% accuracy)\n  - Review class definitions\n  - Understand object creation\n\n## 🔍 Patterns Observed\n1. You're practicing consistently - great habit!\n2. You tend to rush through recursion questions\n3. Your accuracy improves later in the week\n\n## 🎯 Next Week's Focus\n1. **Recursion** - Start with simple examples\n2. **OOP Basics** - Focus on classes and objects\n3. **Exception Handling** - New topic to explore\n\n## 💡 Study Tips\n- Spend 15 minutes daily on recursion exercises\n- Draw diagrams for recursive function calls\n- Create simple class examples for practice\n\n## 🌟 Motivation\nYou're making real progress! Every expert was once a beginner. Your consistent effort is building a strong foundation.\n\nKeep up the great work! 🚀"
}

---

## 📄 FILE 3: prompts/analysis.md

**Location:** `quizsense-ai/prompts/analysis.md`

```markdown
# Performance Analysis Task

Analyze the student's quiz performance data and identify patterns.

## Input Data

You will receive:
1. Recent quiz attempts with questions and answers
2. Historical performance data by topic

## Analysis Tasks

### 1. Calculate Metrics
- Overall accuracy percentage
- Accuracy per topic
- Accuracy per sub-topic
- Average time per question

### 2. Identify Weak Areas
- Topics with accuracy below 60%
- Sub-topics with repeated mistakes
- Question types that are challenging

### 3. Identify Strong Areas
- Topics with accuracy above 80%
- Consistently correct sub-topics
- Question types answered quickly and correctly

### 4. Detect Patterns
- Repeated mistakes on same concepts
- Time-based patterns (rushing or overthinking)
- Improvement or decline trends
- Difficulty level performance

### 5. Determine Trends
- Improving: Accuracy increasing over time
- Declining: Accuracy decreasing over time
- Stable: No significant change

## Output Format

Return ONLY valid JSON in this exact format:

```json
{
    "overall_accuracy": 72.5,
    "total_questions_analyzed": 50,
    "analysis_period": "last_7_days",
    "topic_breakdown": [
        {
            "topic": "Functions",
            "accuracy": 85.0,
            "total_questions": 15,
            "correct": 13,
            "status": "strong",
            "trend": "stable"
        },
        {
            "topic": "Recursion",
            "accuracy": 45.0,
            "total_questions": 10,
            "correct": 4,
            "status": "weak",
            "trend": "declining"
        }
    ],
    "strong_topics": ["Functions", "Variables"],
    "weak_topics": ["Recursion", "OOP"],
    "patterns": [
        {
            "type": "repeated_mistake",
            "description": "Consistently incorrect on recursion base cases",
            "evidence": "4 out of 5 base case questions wrong",
            "severity": "high"
        },
        {
            "type": "time_pattern",
            "description": "Rushing through difficult questions",
            "evidence": "Hard questions answered in under 20 seconds",
            "severity": "medium"
        }
    ],
    "recommendations": [
        "Focus on recursion fundamentals",
        "Take more time on difficult questions",
        "Review base case identification"
    ]
}
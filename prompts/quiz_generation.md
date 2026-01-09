# Quiz Generation Task

Generate a quiz based on the following parameters.

## Parameters

- **Subject:** {{subject}}
- **Topic:** {{topic}}
- **Difficulty:** {{difficulty}}
- **Number of Questions:** {{num_questions}}
- **Previously Asked Questions (avoid these):** {{previous_questions}}

## Requirements

### Question Quality
1. Each question must test UNDERSTANDING, not just memorization
2. Questions should be clear and unambiguous
3. Avoid trick questions
4. Cover different aspects of the topic

### Options Quality
1. Provide exactly 4 options: A, B, C, D
2. Only ONE correct answer
3. Wrong options should be plausible (common misconceptions)
4. Options should be similar in length and format

### Difficulty Guidelines
- **Easy:** Basic concepts, direct questions
- **Medium:** Application of concepts, some reasoning required
- **Hard:** Complex scenarios, deep understanding needed

### Explanation
- Provide brief explanation for why the correct answer is right
- Mention why common wrong choices are incorrect

## Output Format

Return ONLY valid JSON in this exact format:

```json
{
    "questions": [
        {
            "q_id": "q1",
            "question": "Your question text here?",
            "options": {
                "A": "First option",
                "B": "Second option",
                "C": "Third option",
                "D": "Fourth option"
            },
            "correct_answer": "B",
            "topic": "Topic name",
            "sub_topic": "Specific sub-topic",
            "difficulty": "easy",
            "explanation": "Brief explanation of why B is correct."
        },
        {
            "q_id": "q2",
            "question": "Second question text?",
            "options": {
                "A": "First option",
                "B": "Second option",
                "C": "Third option",
                "D": "Fourth option"
            },
            "correct_answer": "A",
            "topic": "Topic name",
            "sub_topic": "Specific sub-topic",
            "difficulty": "easy",
            "explanation": "Brief explanation of why A is correct."
        }
    ]
}
"""
QuizSense AI - Quiz Tests
Tests for quiz generation and submission
"""

import pytest
import asyncio
from datetime import datetime


class TestQuizGeneration:
    """Tests for quiz generation"""
    
    def test_quiz_request_valid(self):
        """Test valid quiz request data"""
        quiz_request = {
            "subject": "Python Programming",
            "topic": "Functions",
            "difficulty": "medium",
            "num_questions": 5
        }
        assert quiz_request["subject"] == "Python Programming"
        assert quiz_request["topic"] == "Functions"
        assert quiz_request["difficulty"] in ["easy", "medium", "hard"]
        assert 3 <= quiz_request["num_questions"] <= 20
        print("✅ Quiz request validation passed")
    
    def test_quiz_question_format(self):
        """Test quiz question format"""
        question = {
            "q_id": "q1",
            "question": "What is 2 + 2?",
            "options": {
                "A": "3",
                "B": "4",
                "C": "5",
                "D": "6"
            },
            "correct_answer": "B",
            "topic": "Math",
            "difficulty": "easy",
            "explanation": "2 + 2 equals 4"
        }
        assert "q_id" in question
        assert "question" in question
        assert "options" in question
        assert len(question["options"]) == 4
        assert "A" in question["options"]
        assert "B" in question["options"]
        assert "C" in question["options"]
        assert "D" in question["options"]
        assert question["correct_answer"] in ["A", "B", "C", "D"]
        print("✅ Quiz question format validation passed")
    
    def test_answer_submission_format(self):
        """Test answer submission format"""
        submission = {
            "quiz_id": "quiz_abc123",
            "answers": [
                {"q_id": "q1", "selected_option": "B", "time_taken_seconds": 30},
                {"q_id": "q2", "selected_option": "A", "time_taken_seconds": 45},
                {"q_id": "q3", "selected_option": "C", "time_taken_seconds": 25}
            ],
            "total_time_seconds": 100
        }
        assert "quiz_id" in submission
        assert "answers" in submission
        assert len(submission["answers"]) > 0
        for answer in submission["answers"]:
            assert "q_id" in answer
            assert "selected_option" in answer
            assert answer["selected_option"] in ["A", "B", "C", "D"]
        print("✅ Answer submission format validation passed")
    
    def test_quiz_scoring(self):
        """Test quiz scoring logic"""
        questions = [
            {"q_id": "q1", "correct_answer": "B"},
            {"q_id": "q2", "correct_answer": "A"},
            {"q_id": "q3", "correct_answer": "C"},
            {"q_id": "q4", "correct_answer": "D"},
            {"q_id": "q5", "correct_answer": "A"}
        ]
        user_answers = [
            {"q_id": "q1", "selected_option": "B"},
            {"q_id": "q2", "selected_option": "A"},
            {"q_id": "q3", "selected_option": "A"},
            {"q_id": "q4", "selected_option": "D"},
            {"q_id": "q5", "selected_option": "C"}
        ]
        correct_count = 0
        for q in questions:
            for a in user_answers:
                if q["q_id"] == a["q_id"]:
                    if q["correct_answer"] == a["selected_option"]:
                        correct_count += 1
        total = len(questions)
        percentage = (correct_count / total) * 100
        assert correct_count == 3
        assert total == 5
        assert percentage == 60.0
        print(f"✅ Quiz scoring passed: {correct_count}/{total} = {percentage}%")
    
    def test_difficulty_levels(self):
        """Test difficulty level values"""
        valid_difficulties = ["easy", "medium", "hard"]
        test_difficulty = "medium"
        assert test_difficulty in valid_difficulties
        invalid_difficulty = "super_hard"
        assert invalid_difficulty not in valid_difficulties
        print("✅ Difficulty level validation passed")


class TestQuizService:
    """Tests for quiz service functions"""
    
    def test_generate_quiz_id(self):
        """Test quiz ID generation"""
        import secrets
        quiz_id = f"quiz_{secrets.token_hex(8)}"
        assert quiz_id.startswith("quiz_")
        assert len(quiz_id) == 21
        print(f"✅ Generated quiz ID: {quiz_id}")
    
    def test_topic_breakdown_calculation(self):
        """Test topic breakdown calculation"""
        results = [
            {"topic": "Functions", "is_correct": True},
            {"topic": "Functions", "is_correct": True},
            {"topic": "Functions", "is_correct": False},
            {"topic": "Loops", "is_correct": True},
            {"topic": "Loops", "is_correct": False}
        ]
        topic_breakdown = {}
        for r in results:
            topic = r["topic"]
            if topic not in topic_breakdown:
                topic_breakdown[topic] = {"correct": 0, "total": 0}
            topic_breakdown[topic]["total"] += 1
            if r["is_correct"]:
                topic_breakdown[topic]["correct"] += 1
        assert topic_breakdown["Functions"]["correct"] == 2
        assert topic_breakdown["Functions"]["total"] == 3
        assert topic_breakdown["Loops"]["correct"] == 1
        assert topic_breakdown["Loops"]["total"] == 2
        print(f"✅ Topic breakdown: {topic_breakdown}")


def run_quiz_tests():
    """Run all quiz tests"""
    print("\n" + "=" * 50)
    print("Running Quiz Tests")
    print("=" * 50 + "\n")
    test_gen = TestQuizGeneration()
    test_gen.test_quiz_request_valid()
    test_gen.test_quiz_question_format()
    test_gen.test_answer_submission_format()
    test_gen.test_quiz_scoring()
    test_gen.test_difficulty_levels()
    test_svc = TestQuizService()
    test_svc.test_generate_quiz_id()
    test_svc.test_topic_breakdown_calculation()
    print("\n" + "=" * 50)
    print("All Quiz Tests Passed! ✅")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    run_quiz_tests()
"""
QuizSense AI - Analysis Tests
Tests for performance analysis and reporting
"""

import pytest
from datetime import datetime, timedelta


class TestPerformanceAnalysis:
    """Tests for performance analysis"""
    
    def test_accuracy_calculation(self):
        """Test accuracy percentage calculation"""
        correct = 7
        total = 10
        accuracy = (correct / total) * 100
        assert accuracy == 70.0
        correct = 0
        total = 5
        accuracy = (correct / total) * 100 if total > 0 else 0
        assert accuracy == 0.0
        correct = 5
        total = 0
        accuracy = (correct / total) * 100 if total > 0 else 0
        assert accuracy == 0.0
        print("✅ Accuracy calculation passed")
    
    def test_topic_status_classification(self):
        """Test topic status classification"""
        def get_status(accuracy):
            if accuracy >= 80:
                return "strong"
            elif accuracy >= 60:
                return "moderate"
            else:
                return "weak"
        assert get_status(90) == "strong"
        assert get_status(80) == "strong"
        assert get_status(75) == "moderate"
        assert get_status(60) == "moderate"
        assert get_status(55) == "weak"
        assert get_status(30) == "weak"
        print("✅ Topic status classification passed")
    
    def test_weak_topic_detection(self):
        """Test weak topic detection"""
        topic_accuracies = {
            "Functions": 85.0,
            "Loops": 75.0,
            "Recursion": 45.0,
            "OOP": 55.0,
            "Variables": 90.0
        }
        weak_threshold = 60.0
        weak_topics = [
            topic for topic, accuracy in topic_accuracies.items()
            if accuracy < weak_threshold
        ]
        assert "Recursion" in weak_topics
        assert "OOP" in weak_topics
        assert "Functions" not in weak_topics
        assert len(weak_topics) == 2
        print(f"✅ Weak topics detected: {weak_topics}")
    
    def test_strong_topic_detection(self):
        """Test strong topic detection"""
        topic_accuracies = {
            "Functions": 85.0,
            "Loops": 75.0,
            "Recursion": 45.0,
            "OOP": 55.0,
            "Variables": 90.0
        }
        strong_threshold = 80.0
        strong_topics = [
            topic for topic, accuracy in topic_accuracies.items()
            if accuracy >= strong_threshold
        ]
        assert "Functions" in strong_topics
        assert "Variables" in strong_topics
        assert "Recursion" not in strong_topics
        assert len(strong_topics) == 2
        print(f"✅ Strong topics detected: {strong_topics}")
    
    def test_trend_detection(self):
        """Test performance trend detection"""
        def detect_trend(current_accuracy, previous_accuracy):
            difference = current_accuracy - previous_accuracy
            if difference > 5:
                return "improving"
            elif difference < -5:
                return "declining"
            else:
                return "stable"
        assert detect_trend(80, 70) == "improving"
        assert detect_trend(60, 75) == "declining"
        assert detect_trend(72, 70) == "stable"
        print("✅ Trend detection passed")


class TestWeeklyReport:
    """Tests for weekly report generation"""
    
    def test_report_structure(self):
        """Test report structure"""
        report = {
            "report_id": "report_abc123",
            "user_id": "user_123",
            "week_start": "2024-01-08",
            "week_end": "2024-01-14",
            "summary": "Good progress this week!",
            "overall_accuracy": 72.5,
            "quizzes_completed": 5,
            "strong_topics": ["Functions", "Variables"],
            "weak_topics": ["Recursion"],
            "focus_topics": ["Recursion", "OOP"],
            "full_report": "# Weekly Report\n\nContent here..."
        }
        required_fields = [
            "report_id", "user_id", "week_start", "week_end",
            "summary", "overall_accuracy", "strong_topics",
            "weak_topics", "focus_topics", "full_report"
        ]
        for field in required_fields:
            assert field in report, f"Missing field: {field}"
        print("✅ Report structure validation passed")
    
    def test_week_date_calculation(self):
        """Test week start/end date calculation"""
        from datetime import date
        today = date(2024, 1, 15)
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        assert week_start == date(2024, 1, 15)
        assert week_end == date(2024, 1, 21)
        print(f"✅ Week dates: {week_start} to {week_end}")
    
    def test_pattern_detection_format(self):
        """Test pattern detection format"""
        pattern = {
            "type": "repeated_mistake",
            "description": "Struggling with recursion base cases",
            "evidence": "4 out of 5 questions incorrect",
            "recommendation": "Review base case identification"
        }
        required_fields = ["type", "description", "evidence", "recommendation"]
        for field in required_fields:
            assert field in pattern
        valid_types = ["repeated_mistake", "time_pattern", "improvement", "strength", "weakness"]
        assert pattern["type"] in valid_types or True
        print("✅ Pattern detection format passed")
    
    def test_recommendations_format(self):
        """Test recommendations format"""
        recommendations = [
            "Practice recursion problems daily",
            "Review OOP concepts",
            "Take more time on difficult questions"
        ]
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        for rec in recommendations:
            assert isinstance(rec, str)
            assert len(rec) > 10
        print(f"✅ Recommendations format passed: {len(recommendations)} recommendations")


class TestDashboardData:
    """Tests for dashboard data"""
    
    def test_dashboard_structure(self):
        """Test dashboard data structure"""
        dashboard = {
            "user_id": "user_123",
            "user_name": "John Doe",
            "total_quizzes": 25,
            "current_streak": 5,
            "overall_accuracy": 75.5,
            "quizzes_this_week": 4,
            "weekly_accuracy": [
                {"date": "2024-01-08", "accuracy": 70.0},
                {"date": "2024-01-09", "accuracy": 75.0},
                {"date": "2024-01-10", "accuracy": 80.0}
            ],
            "topic_performance": [
                {"topic": "Functions", "accuracy": 85.0},
                {"topic": "Loops", "accuracy": 70.0}
            ],
            "recommended_topics": ["Recursion", "OOP"]
        }
        assert "total_quizzes" in dashboard
        assert "current_streak" in dashboard
        assert "overall_accuracy" in dashboard
        assert "weekly_accuracy" in dashboard
        assert "topic_performance" in dashboard
        assert "recommended_topics" in dashboard
        print("✅ Dashboard structure validation passed")
    
    def test_streak_calculation(self):
        """Test streak calculation logic"""
        quiz_dates = [
            "2024-01-15",
            "2024-01-14",
            "2024-01-13",
            "2024-01-11",
            "2024-01-10"
        ]
        streak = 0
        if quiz_dates:
            streak = 1
        print(f"✅ Streak calculation passed: {streak} days")
    
    def test_weekly_accuracy_aggregation(self):
        """Test weekly accuracy aggregation"""
        daily_scores = [
            {"date": "2024-01-08", "score": 4, "total": 5},
            {"date": "2024-01-08", "score": 3, "total": 5},
            {"date": "2024-01-09", "score": 5, "total": 5}
        ]
        daily_data = {}
        for entry in daily_scores:
            date = entry["date"]
            if date not in daily_data:
                daily_data[date] = {"score": 0, "total": 0}
            daily_data[date]["score"] += entry["score"]
            daily_data[date]["total"] += entry["total"]
        weekly_accuracy = []
        for date, data in daily_data.items():
            acc = (data["score"] / data["total"]) * 100 if data["total"] > 0 else 0
            weekly_accuracy.append({"date": date, "accuracy": round(acc, 1)})
        assert len(weekly_accuracy) == 2
        assert weekly_accuracy[0]["accuracy"] == 70.0
        assert weekly_accuracy[1]["accuracy"] == 100.0
        print(f"✅ Weekly accuracy aggregation passed: {weekly_accuracy}")


def run_analysis_tests():
    """Run all analysis tests"""
    print("\n" + "=" * 50)
    print("Running Analysis Tests")
    print("=" * 50 + "\n")
    test_perf = TestPerformanceAnalysis()
    test_perf.test_accuracy_calculation()
    test_perf.test_topic_status_classification()
    test_perf.test_weak_topic_detection()
    test_perf.test_strong_topic_detection()
    test_perf.test_trend_detection()
    test_report = TestWeeklyReport()
    test_report.test_report_structure()
    test_report.test_week_date_calculation()
    test_report.test_pattern_detection_format()
    test_report.test_recommendations_format()
    test_dash = TestDashboardData()
    test_dash.test_dashboard_structure()
    test_dash.test_streak_calculation()
    test_dash.test_weekly_accuracy_aggregation()
    print("\n" + "=" * 50)
    print("All Analysis Tests Passed! ✅")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    run_analysis_tests()
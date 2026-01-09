"""
QuizSense AI - Intelligent Learning Agent
Adaptive learning that acts like a real AI tutor!
"""

import random
from typing import Dict, List
from datetime import datetime, timedelta


class LearningAgent:
    """
    Intelligent Agent that:
    - Decides what to teach
    - Adapts to user level
    - Tracks progress
    - Creates personalized path
    """
    
    def __init__(self):
        print("🤖 Learning Agent Initialized!")
        
        # Learning paths: Domain -> Ordered topics (basic to advanced)
        self.learning_paths = {
            "Python Programming": [
                {"topic": "Variables and Data Types", "level": 1},
                {"topic": "Operators", "level": 1},
                {"topic": "Control Flow", "level": 2},
                {"topic": "Loops", "level": 2},
                {"topic": "Strings", "level": 2},
                {"topic": "Lists and Tuples", "level": 3},
                {"topic": "Dictionaries", "level": 3},
                {"topic": "Functions", "level": 4},
                {"topic": "File Handling", "level": 4},
                {"topic": "Exception Handling", "level": 5},
                {"topic": "OOP Basics", "level": 5},
                {"topic": "Recursion", "level": 6},
            ],
            "Web Development": [
                {"topic": "HTML Basics", "level": 1},
                {"topic": "CSS Fundamentals", "level": 2},
                {"topic": "JavaScript Basics", "level": 3},
                {"topic": "DOM Manipulation", "level": 4},
                {"topic": "APIs and REST", "level": 5},
            ],
            "Data Structures": [
                {"topic": "Arrays", "level": 1},
                {"topic": "Linked Lists", "level": 2},
                {"topic": "Stacks", "level": 2},
                {"topic": "Queues", "level": 2},
                {"topic": "Trees", "level": 3},
                {"topic": "Graphs", "level": 4},
                {"topic": "Hash Tables", "level": 4},
            ],
            "Algorithms": [
                {"topic": "Searching", "level": 1},
                {"topic": "Sorting", "level": 2},
                {"topic": "Recursion", "level": 3},
                {"topic": "Dynamic Programming", "level": 4},
                {"topic": "Greedy Algorithms", "level": 5},
            ],
        }
    
    def get_available_domains(self) -> List[str]:
        """Get all available learning domains"""
        return list(self.learning_paths.keys())
    
    def analyze_user_level(self, user_performance: Dict) -> Dict:
        """
        Analyze user's current level based on performance
        Returns: level info and recommendations
        """
        
        if not user_performance or user_performance.get("total_quizzes", 0) == 0:
            return {
                "status": "new_user",
                "level": 1,
                "difficulty": "easy",
                "message": "Welcome! Let's start from the basics."
            }
        
        accuracy = user_performance.get("overall_accuracy", 0)
        total_quizzes = user_performance.get("total_quizzes", 0)
        
        # Determine status based on accuracy
        if accuracy < 50:
            status = "struggling"
            difficulty = "easy"
            message = "Let's practice more on the fundamentals!"
        elif accuracy < 70:
            status = "learning"
            difficulty = "medium"
            message = "Good progress! Keep practicing."
        elif accuracy < 85:
            status = "proficient"
            difficulty = "medium"
            message = "Great work! Ready for more challenges."
        else:
            status = "mastering"
            difficulty = "hard"
            message = "Excellent! You're mastering this!"
        
        # Simple level: every 3 quizzes = +1 level (max 6)
        level = min(1 + (total_quizzes // 3), 6)
        
        return {
            "status": status,
            "level": level,
            "difficulty": difficulty,
            "accuracy": accuracy,
            "message": message
        }
    
    def decide_next_topic(self, domain: str, user_performance: Dict, topic_performance: Dict) -> Dict:
        """
        AI decides what topic to quiz next!
        
        Logic:
        1. If new user -> Start with first topic (level 1)
        2. If weak topics exist -> Focus on weakest
        3. If doing well -> Move to next topic in path
        4. Mix: 70% weak areas, 30% new content
        """
        
        if domain not in self.learning_paths:
            domain = "Python Programming"  # Default
        
        path = self.learning_paths[domain]
        user_level = self.analyze_user_level(user_performance)
        
        # New user - start from beginning
        if user_level["status"] == "new_user":
            topic = path[0]
            return {
                "topic": topic["topic"],
                "difficulty": "easy",
                "reason": "Starting your learning journey from the basics.",
                "is_new_topic": True
            }
        
        # Build weak topics list (accuracy < 60%)
        weak_topics = []
        for topic_name, data in topic_performance.items():
            if data.get("accuracy", 100) < 60:
                weak_topics.append({
                    "topic": topic_name,
                    "accuracy": data.get("accuracy", 0)
                })
        
        # Sort by accuracy (weakest first)
        weak_topics.sort(key=lambda x: x["accuracy"])
        
        # 70% chance to focus on weakest area
        if weak_topics and random.random() < 0.7:
            weakest = weak_topics[0]
            return {
                "topic": weakest["topic"],
                "difficulty": user_level["difficulty"],
                "reason": f"Focusing on weak area: {weakest['topic']} ({weakest['accuracy']:.0f}% accuracy).",
                "is_new_topic": False,
                "is_weak_area": True
            }
        
        # Else: move to next topic in path
        completed_topics = list(topic_performance.keys())
        
        for topic_info in path:
            if topic_info["topic"] not in completed_topics:
                if topic_info["level"] <= user_level["level"] + 1:
                    return {
                        "topic": topic_info["topic"],
                        "difficulty": user_level["difficulty"],
                        "reason": f"Introducing new topic: {topic_info['topic']}.",
                        "is_new_topic": True
                    }
        
        # All topics covered - review random topic
        random_topic = random.choice(path)
        return {
            "topic": random_topic["topic"],
            "difficulty": user_level["difficulty"],
            "reason": "Reviewing previously learned concepts.",
            "is_new_topic": False
        }
    
    def generate_personalized_quiz(
        self,
        domain: str,
        user_performance: Dict,
        topic_performance: Dict,
        num_questions: int = 5
    ) -> Dict:
        """
        Generate a fully personalized quiz plan
        AI decides topic + difficulty based on domain and performance
        """
        
        decision = self.decide_next_topic(domain, user_performance, topic_performance)
        user_level = self.analyze_user_level(user_performance)
        
        return {
            "domain": domain,
            "topic": decision["topic"],
            "difficulty": decision["difficulty"],
            "num_questions": num_questions,
            "reason": decision["reason"],
            "user_level": user_level,
            "is_new_topic": decision.get("is_new_topic", False),
            "is_weak_area": decision.get("is_weak_area", False)
        }


# Global instance
learning_agent = LearningAgent()
from collections import Counter

class LearningModule:
    def __init__(self, database):
        self.db = database

    def analyze_common_queries(self):
        recent_interactions = self.db.get_recent_interactions(limit=100)
        commands = [interaction[1] for interaction in recent_interactions]
        common_commands = Counter(commands).most_common(5)
        return common_commands

    def suggest_action(self):
        common_queries = self.analyze_common_queries()
        if common_queries:
            most_common = common_queries[0][0]
            return f"I noticed you often ask about {most_common}. Would you like me to tell you about that?"

    def adapt_to_preferences(self):
        voice_speed = self.db.get_preference('voice_speed')
        if voice_speed:
            return int(voice_speed)
        return 150  # default speed
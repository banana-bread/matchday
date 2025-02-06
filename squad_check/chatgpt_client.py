from openai import OpenAI
from squad_check.logger import logger

class ChatGptClient:
    """Handles ChatGPT queries for football match-related logic."""

    def __init__(self):
        self.client = OpenAI()

    def shirt_colour_conflict_exists(self, shirt1, shirt2):
        """Checks if there is a color conflict between two team shirts."""
        prompt = f"""
        You are a football referee checking if two teams have conflicting shirt colors.

        - Team 1 is wearing: **{shirt1}**
        - Team 2 is wearing: **{shirt2}**

        **Rules for a conflict:**
        - If both shirts are the same or **similar shades** (e.g., two dark colors like navy and black), return `"conflict": true`.
        - If one team is wearing a **light color** and the other a **dark color**, return `"conflict": false`.
        - If unsure, return `"conflict": true` to prevent issues.

        **Respond with a 1 for true, and a 0 for false ONLY**
        """

        return self._ask_chatgpt(prompt)

    def _ask_chatgpt(self, prompt):
        """Sends a structured query to ChatGPT and ensures JSON output."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,  # Zero to prevent creative responses
            )

            result = response.choices[0].message.content  # Extract response content
            return result  # Returns JSON string like: {"conflict": true}

        except Exception as e:
            logger.error("❌ OpenAI API Error", extra={
                "task_name": "ChatGptClient._ask_chatgpt",
                "error": str(e)
            })
            return None
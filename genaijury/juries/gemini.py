from genaijury.api_models.base import APIModel

class JuryModel:
    def __init__(self, api: APIModel):
        self.api = api
        # ... other Jury model setup ...

    def generate_jury_evaluation(self, preprompt: str, criterias: dict, image_paths: list[str] = []) -> dict:
        # 1. Optimization (optional)
        optimized_preprompt = self.optimize_prompt(preprompt, criterias)  # Placeholder - define optimization logic

        # 2. Prompt Construction
        full_prompt = self.build_jury_prompt(optimized_preprompt, criterias)

        # 3. Gemini API Call
        response_text = self.api.call(full_prompt, image_paths)

        # 4. Response Processing
        jury_evaluation = self.extract_dict(response_text, criterias)

        return jury_evaluation

    def build_jury_prompt(self):
        pass

    def optimize_prompt(self, preprompt: str, criterias: dict) -> str:
        # Load necessary criteria descriptions or examples
        criteria_descriptions = criterias["Criterias"]

        prompt_for_guidelines = (
            f"Act like a jury with Background: {preprompt}. And generate a guideline for scoring given inputs"  # Start with your base preprompt
            "Provide detailed scoring guideline. "
            "Include the following:\n"
            "* A **numerical rating scale** with detailed explanation about scoring system for that topic. Scores are 0 to 5\n"
            "* **One General Guideline** about how to approach the input based on jury background and user request:\n"
            "Write general guideline and list points to consider list at least 20 points and write only one guideline and scoring table\n"
        )

        # Add criteria to the prompt
        for criteria_name, description in criteria_descriptions.items():
            prompt_for_guidelines += f"  * **{criteria_name}** ({description})\n"

        # Request clear formatting
        prompt_for_guidelines += "Present the guidelines in a structured format, ideally a table or list. Write your answer in ``` code block ```\n"

        response = self.api.call(prompt_for_guidelines)  # Optional: Use the API to optimize the prompt

        # get text between two ``` marks, in a robust way
        try:
            optimized_prompt = response.split("```")[1]
        except Exception as e:
            optimized_prompt = response

        return optimized_prompt

    def extract_scoextract_dictres(self, response_text: str, criterias: dict) -> dict:
        # ... Logic to analyze Gemini's response and derive scores ...
        pass

from genaijury.api_models.base import APIModel
import re
import json
class JuryModel:
    def __init__(self, api: APIModel):
        self.api = api
        self.optimized_prompt = None
        # ... other Jury model setup ...

    def generate_jury_evaluation(self, criterias: dict, image_paths: list[str] = []) -> dict:

        if not self.optimized_prompt:
            raise ValueError("Optimized preprompt is not set. Please call optimize_prompt() first.")

        # 2. Prompt Construction
        full_prompt = self.build_jury_prompt(self.optimized_prompt, criterias)

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
        prompt_for_guidelines = (
            f"You are an expert with background {preprompt} tasked with helping someone create effective scoring guidelines for different input types. Here's how to approach this task:\n"

            "**. Develop a Tailored Prompt:** Provide the user with a new prompt template suitable for their input type. Include:\n"
            "   * **Instructions:** Clear and SHORT guidance on how to use the guidelines to evaluate submissions. Consider background information of the jury\n"
            "   * **Avoid Repetitive words**: Do not repeat same words along prompt. **\n"
            "   * **Detailed Scoring Table:** Outline a numerical scale (e.g., 0-5). For score level, include: \n"
            "       * **Clear and Short descriptions:** Define what constitutes exceptional (5), good (4), average  (3), etc. \n"
            "       * **Special Conditions:** Identify circumstances that might warrant higher or lower scores within a level.   \n"
            "Here are Criterias for that competition: \n\n"
        )
        # Add criteria to the prompt
        for criteria_name, description in criteria_descriptions.items():
            prompt_for_guidelines += f"  * {criteria_name}: ({description})\n"

        # Request clear formatting
        prompt_for_guidelines += "Write your answer in ``` code block ```\n"

        response = self.api.call(prompt_for_guidelines)  # Optional: Use the API to optimize the prompt

        # get text between two ``` marks, in a robust way
        try:
            optimized_prompt = response.split("```")[1]
        except Exception as e:
            optimized_prompt = response

        with open("optimized_prompt.txt", "w") as file:
            file.write(optimized_prompt)

        self.optimized_prompt = optimized_prompt
        return optimized_prompt

    def extract_dict(self, response_text: str) -> dict:
        start_index = response_text.find('{')
        end_index = response_text.rfind('}')
        if start_index == -1 or end_index == -1:
            raise ValueError("Invalid response_text format. Could not find '{' or '}'.")

        dict_str = response_text[start_index:end_index+1]
        dict_str = re.sub(r"[\n\t\a]", "", dict_str)  # Remove newline, tab, and bell characters

        try:
            extracted_dict = json.loads(dict_str)
            if not isinstance(extracted_dict, dict):
                raise ValueError("Extracted object is not a dictionary.")
            return extracted_dict
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError("Failed to convert extracted string to dictionary.") from e

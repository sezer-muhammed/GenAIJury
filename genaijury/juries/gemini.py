from genaijury.api_models.base import APIModel
from genaijury.database.base import DatabaseInterface
import re
import json
from pathlib import Path
from typing import Dict, List

class JuryModel:
    def __init__(self, api: APIModel, database: DatabaseInterface):
        self.api = api
        self.database = database  # Database object that implements DatabaseInterface
        self.optimized_prompt = None

    def generate_jury_evaluation(self, criterias: Dict, image_paths: List[str] = []) -> Dict:
        """
        Generates jury evaluation for a list of image paths based on given criteria.

        Args:
            criterias (Dict): A dictionary containing the evaluation criteria.
            image_paths (List[str], optional): A list of image paths to be evaluated. Defaults to [].

        Returns:
            Dict: A dictionary containing the jury evaluation results for each image path.
        """
        if not self.optimized_prompt:
            raise ValueError("Optimized preprompt is not set. Please call optimize_prompt() first.")

        jury_evaluation_results = {}
        for i, image_path in enumerate(image_paths):
            if not Path(image_path).exists():
                raise FileNotFoundError(f"Image file not found: {image_path}")
            full_prompt = self.build_jury_prompt(criterias)
            response_text = self.api.call(full_prompt, [image_path])
            # Process the response to extract evaluation
            jury_evaluation = self.extract_dict(response_text, criterias)

            # Add image path as Name field to jury_evaluation before saving
            jury_evaluation["Name"] = image_path
            jury_evaluation_results[f"{image_path}_run_{i}"] = jury_evaluation
            # Save the result into the database
            self.database.create(jury_evaluation)

        return jury_evaluation_results

    def build_jury_prompt(self, criterias: dict) -> str:
        criterias_str = json.dumps(criterias, ensure_ascii=False, indent=2).encode('utf8')

            # Build the prompt
        jury_prompt = f"""{self.optimized_prompt}\n\n
    Here are the criterias for that competition. Fill the given template: {criterias_str}\n\n
    First write a general analysis of the input, then score each criteria from 0 to 5 in json format.\n
    Make sure you write whole criterias in code block as json code. do not change structure of json. just fill template\n
    """

        return jury_prompt

    def optimize_prompt(self, preprompt: str, criterias: dict) -> str:

        prompt_for_guidelines = (
            f"You are an expert with background {preprompt} tasked with helping someone create effective scoring guidelines for different input types. Here's how to approach this task:\n"

            "**. Develop a Tailored Prompt:** Provide the user with a new prompt template suitable for their input type. Include:\n"
            "   * **Instructions:** Clear and SHORT guidance on how to use the guidelines to evaluate submissions. Consider background information of the jury\n"
            "   * **Avoid Repetitive words**: Do not repeat same words along prompt. **\n"
            "   * **Detailed Scoring Table:** Outline a numerical scale (e.g., 0-5). For score level, include: \n"
            "       * **Clear and Short descriptions:** Define what constitutes exceptional (5), good (4), average  (3), etc. \n"
            "       * **Special Conditions:** Identify circumstances that might warrant higher or lower scores within a level.   \n"
        )
        # Add criteria to the prompt
        criterias_str = json.dumps(criterias, ensure_ascii=False).encode('utf8')

        prompt_for_guidelines += f"Here are the criterias for that competition: {criterias_str}\n\n"

        # Request clear formatting
        prompt_for_guidelines += "Write your answer in ``` code block ```\n"

        response = self.api.call(prompt_for_guidelines)

        # get text between two ``` marks, in a robust way
        try:
            optimized_prompt = response.split("```")[1]
        except Exception as e:
            optimized_prompt = response

        with open("optimized_prompt.txt", "w") as file:
            file.write(optimized_prompt)

        self.optimized_prompt = optimized_prompt
        return optimized_prompt

    def extract_dict(self, response_text: str, criterias: dict) -> dict:
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

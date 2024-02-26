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

    def generate_jury_evaluation(self, criterias: Dict, submissions: List[str] = []) -> Dict:
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
        for i, submission in enumerate(submissions):
            max_attempts = 5
            attempts = 0
            jury_evaluation = None
            while attempts < max_attempts:
                attempts += 1
                try:
                    if not Path(submission).exists():
                        full_prompt = self.build_jury_prompt(criterias, submission)
                        response_text = self.api.call(full_prompt)

                    else:
                        full_prompt = self.build_jury_prompt(criterias)
                        response_text = self.api.call(full_prompt, [submission])
                    # Process the response to extract evaluation

                    jury_evaluation = self.extract_dict(response_text)

                    # Add image path as Name field to jury_evaluation before saving
                    jury_evaluation["Name"] = submission
                    jury_evaluation_results[f"{submission}_run_{i}"] = jury_evaluation
                    # Save the result into the database
                    self.database.create(jury_evaluation)
                    break
                except:
                    pass

        return jury_evaluation_results

    def build_jury_prompt(self, criterias: dict, submission: str = None) -> str:
        criterias_str = json.dumps(criterias, ensure_ascii=False, indent=2).encode('utf8')

            # Build the prompt
        jury_prompt = f"""{self.optimized_prompt}\n\n
    Here are the criterias for that competition. Fill the given json template: {criterias_str}\n\n
    First write a general analysis of the input, then score each criteria from 0 to 5 in json format.\n
    Make sure you write whole criterias in code block as json code. do not change structure of json. just fill the json template\n
    """

        if submission:
            jury_prompt += f"Here is the submission: {submission}\n\n"

        return jury_prompt

    def optimize_prompt(self, preprompt: str, criterias: dict) -> str:

        prompt_for_guidelines = (
            f"You are an expert with a background in {preprompt}, tasked with assisting in the creation of effective scoring guidelines for different input types. Approach this task as follows:\n"
            "\n"
            "- Develop a Guide: Craft a new Scoring Guide template including:\n"
            "   - Instructions: Provide clear, brief guidance on using the guidelines to assess submissions, taking into account the jurors' background knowledge.\n"
            "   - Detailed and Short Scoring Criteria: Present a numerical scale (e.g., 0-5) and for each score level, detail:\n"
            "       - Clear, short, concise descriptions: Describe what qualifies as exceptional (5), good (4), average (3), and so on.\n"
            "       - Special Conditions: Highlight any circumstances that may justify deviations from the typical score range.\n"
            "       - Only and Only write scoring guides for the given criterias below.\n"
        )

        # Add criteria to the prompt
        criterias_str = json.dumps(criterias, ensure_ascii=False).encode('utf8')

        prompt_for_guidelines += f"Here are the criterias for that competition: {criterias_str}\n\n"

        # Request clear formatting
        prompt_for_guidelines += "Write your answer in ``` code block ```\n"

        max_attempts = 5  # Set a maximum number of attempts to prevent infinite loops
        attempts = 0

        while attempts < max_attempts:
            attempts += 1

            try:
                response = self.api.call(prompt_for_guidelines)
                # Attempt to extract the text between triple backticks
                if "```" in response:
                    optimized_prompt = response.split("```")[1]
                    break  # Exit the loop if the optimized prompt is successfully extracted
                else:
                    optimized_prompt = None
            except Exception as e:
                optimized_prompt = None

            if attempts == max_attempts:
                optimized_prompt = None  # Use the last response received if max attempts are reached

        # Ensure optimized_prompt is set to response if no backticks were found after all attempts
        if optimized_prompt is None:
            raise ValueError("Failed to extract optimized prompt from response.")

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

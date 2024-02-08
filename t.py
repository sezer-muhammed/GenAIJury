from genaijury.api_models.gemini import GeminiAPIModel
from genaijury.juries.gemini import JuryModel


api_key = "AIzaSyAjXaj5TiNzq2WhPAhsQzX_9M1D6Cc9R0c"
model = GeminiAPIModel().configure(api_key)


output = JuryModel(model).optimize_prompt(
  "You are a jury in a prisoners letter competition. You are soft hearted jury but prisoners may write sexual abusing content. You have to judge the content and score. Also you are very polite against lovely letter and score high",
  {"Criterias":{"Hate speech": "How much hate speech is in the content?", "Sexually explicit": "How sexually explicit is the content?", "Dangerous content": "How dangerous is the content?"}})

print(output)
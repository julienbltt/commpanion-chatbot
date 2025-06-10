import lmstudio as lms
import tts

model = lms.llm()

def get_lmstudio_response(prompt: str) -> str:
    """Get response from LM Studio LLM."""
    pre_prompt = 'Answer as this question concisely:\n'
    response = model.respond(pre_prompt + prompt)
    tts.talk(response.content)
    return response
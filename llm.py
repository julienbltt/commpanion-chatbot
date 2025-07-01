import lmstudio as lms
import tts
import time
import re


class LMStudioResponder:
    """
    A wrapper around the LM Studio chat model to generate streaming responses.
    """

    CHUNK_REGEX = re.compile(r".*?[\.!?…](?:\s|$)") # Sentence-ending punctuation

    def __init__(self, model_name: str = None, system_prompt: str = None):
        """
        Initialize the LMStudioResponder.

        Args:
            model_name (str | None): Optional name of the model to use. Default: first llm load on the server
            system_prompt (str | None): Optional custom system prompt. Default: You are a friendly assistant. Answer concisely with 1 or 2 sentences. Never use emojis.
        """
        self.model = lms.llm(model_name) if model_name else lms.llm()
        self.chat = lms.Chat(
            system_prompt or "You are a vocal assistant. Answer concisely with 1 or 2 sentences. Never use emojis."
        ) 

    def _get_response_stream(self, prompt: str):
        """
        Generate a streaming response from the model.

        Args:
            prompt (str): The user prompt to respond to.

        Returns:
            Iterator over streaming chunks from the model.
        """
        self.chat.add_user_message(prompt)
        return self.model.respond_stream(
            self.chat,
            on_message=self.chat.append,
        )
    
    def _speak_chunks_from_stream(self, stream) -> str:
        """
        Process and speak response chunks as complete sentences.

        Args:
            stream: A streaming response from LM Studio.

        Returns:
            str: The complete spoken text.
        """
        buffer = ""
        full_text = ""

        for chunk in stream:
            content = chunk.content
            if not content:
                continue

            buffer += content
            full_text += content

            while (match := self.CHUNK_REGEX.match(buffer)):
                chunk_text = match.group(0).strip()
                if chunk_text:
                    tts.talk(chunk_text)
                buffer = buffer[match.end():]

        # Speak any leftover buffer
        remaining = buffer.strip()
        if remaining:
            tts.talk(remaining)

        return full_text

    def respond_and_speak(self, prompt: str) -> str:
        """
        Get a response from LM Studio and speak it sentence by sentence.

        Args:
            prompt (str): User input prompt.

        Returns:
            str: Full response text.
        """
        start_time = time.time()
        stream = self._get_response_stream(prompt)
        full_text = self._speak_chunks_from_stream(stream)
        print(f"\n\nResponse time: {time.time() - start_time:.3f} seconds")
        return full_text
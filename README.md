# commpanion-chatbot
The Commpanion ChatBot is an AI chat service developed for the Commpanion system.
## Service architecure
```mermaid
flowchart LR
    A((Microphone)) -->|Speak| B[S2T]
    B -->|text| C[LLM]
    C -->|text| D[T2S]
    D -->|speak| E((Speaker))
```
> **Microphone**: Lenovo ThinckReality A3 integrated microphone.<br>
> **Speaker**: Lenovo ThinckReality A3 integrated speakers.<br>
> **S2T**: AI model to convert speak to text.<br>
> **T2S**: AI modem to convert text to speak.<br>
> **LLM**: Large Language Model for chat.<br>

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
## Tools needs
- Python 3.11.x
- LM Studio with LLM model
- Lenovo ThinkReality A3
## Installation process
1. Clone repository `git clone https://github.com/julienbltt/commpanion-chatbot.git`
2. Create virtual envrironement `python3.11 -m venv .venv
3. Enter in virtual environnement. (command depending of your OS)
4. Download dependenties. `pip install -r requirements.txt
5. Download LM Studio.
6. Get a LLM.
7. Run application. `python main.py`

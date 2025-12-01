from typing import Dict, Any, List

class SessionMemory:
    def __init__(self):
        self._memory: Dict[str, Any] = {
            "conversation_history": [],
            "current_intent": None,
            "temp_data": {}
        }

    def add_message(self, role: str, content: str):
        self._memory["conversation_history"].append({"role": role, "content": content})

    def get_history(self) -> List[Dict[str, str]]:
        return self._memory["conversation_history"]

    def set_intent(self, intent: str):
        self._memory["current_intent"] = intent

    def get_intent(self) -> str:
        return self._memory.get("current_intent")

    def set_temp_data(self, key: str, value: Any):
        self._memory["temp_data"][key] = value

    def get_temp_data(self, key: str) -> Any:
        return self._memory["temp_data"].get(key)

    def clear(self):
        self._memory = {
            "conversation_history": [],
            "current_intent": None,
            "temp_data": {}
        }

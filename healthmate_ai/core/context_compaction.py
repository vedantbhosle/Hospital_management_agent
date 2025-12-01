from typing import List, Dict

class ContextCompaction:
    def __init__(self, max_messages: int = 10):
        self.max_messages = max_messages

    def compact(self, history: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Compacts the conversation history.
        Currently implements a sliding window approach.
        Future improvement: Use LLM to summarize older messages.
        """
        if len(history) <= self.max_messages:
            return history
        
        # Keep the system prompt if it exists (usually the first message)
        # and the last N messages.
        compacted = []
        if history and history[0]['role'] == 'system':
            compacted.append(history[0])
            remaining = history[1:]
        else:
            remaining = history

        compacted.extend(remaining[-self.max_messages:])
        return compacted

    def summarize_with_llm(self, history: List[Dict[str, str]]) -> str:
        # Placeholder for LLM-based summarization
        pass

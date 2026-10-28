from typing import NotRequired
from langgraph.graph import MessagesState


class TutorState(MessagesState):
    # Conversational state comes from MessagesState.messages.
    current_topic: NotRequired[str | None]
    current_question_id: NotRequired[str | None]
    score: NotRequired[int]
    attempts: NotRequired[int]

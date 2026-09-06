import json
import redis
from langchain_core.callbacks import BaseCallbackHandler
from app.core.config import settings
from typing import Any, Dict, List
from uuid import UUID

class RedisCallbackHandler(BaseCallbackHandler):
    """
    A custom LangChain callback handler that intercepts agent tool steps
    and LLM generations, and publishes them to Redis PubSub for the UI to consume.
    """
    def __init__(self, channel: str):
        self.channel = channel
        self.redis_client = redis.from_url(settings.REDIS_URL)

    def publish_progress(self, step: str, status: str = "running"):
        data = {
            "type": "agent_progress",
            "step": step,
            "status": status
        }
        self.redis_client.publish(self.channel, json.dumps(data))

    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: List[str] | None = None,
        metadata: Dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        tool_name = serialized.get("name", "tool")
        self.publish_progress(f"Using tool: {tool_name} with input {input_str}")

    def on_tool_end(
        self,
        output: Any,
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: List[str] | None = None,
        **kwargs: Any,
    ) -> Any:
        # We just update the status implicitly by publishing the next step
        pass

    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        *,
        run_id: UUID,
        parent_run_id: UUID | None = None,
        tags: List[str] | None = None,
        metadata: Dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Any:
        self.publish_progress("Agent is reasoning...")


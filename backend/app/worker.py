import time
import json
import redis
from app.core.celery_app import celery_app
from app.core.config import settings

# Initialize Redis client for pubsub
redis_client = redis.from_url(settings.REDIS_URL)

def publish_progress(channel: str, step: str, status: str = "running"):
    data = {
        "type": "agent_progress",
        "step": step,
        "status": status
    }
    redis_client.publish(channel, json.dumps(data))
    time.sleep(1) # Mock delay for UI to easily see stream

@celery_app.task(bind=True, name="process_document_task")
def process_document_task(self, document_id: int, file_path: str):
    channel = f"agent_progress_{document_id}"
    try:
        publish_progress(channel, "Instantiating AI Agent...")
        publish_progress(channel, f"Extracting text from PDF {file_path}...")
        publish_progress(channel, "Running Vector Search for relevant SOPs...")
        publish_progress(channel, "Synthesizing final response...")
        publish_progress(channel, "Document processing complete.", status="completed")
        return {"status": "success", "document_id": document_id}
    except Exception as e:
        publish_progress(channel, f"Error processing document: {str(e)}", status="error")
        return {"status": "error", "error": str(e)}

@celery_app.task(bind=True, name="process_chat_task")
def process_chat_task(self, conversation_id: str, message: str):
    channel = f"agent_progress_{conversation_id}"
    try:
        from app.ai.agent import get_agent_executor
        from app.ai.callbacks import RedisCallbackHandler
        
        publish_progress(channel, "Initializing AI Agent...", status="running")
        
        agent_executor = get_agent_executor()
        callbacks = [RedisCallbackHandler(channel=channel)]
        
        # Invoke the LangGraph Agent
        result = agent_executor.invoke(
            {"messages": [("user", message)]},
            config={"callbacks": callbacks}
        )
        
        # LangGraph returns a dictionary with 'messages', the last of which is the AI's response
        final_answer = result["messages"][-1].content if "messages" in result else "No response generated."
        
        publish_progress(channel, "Formulating response...", status="completed")
        
        # Publish the final assistant message
        final_message = {
            "type": "message",
            "role": "assistant",
            "content": final_answer
        }
        redis_client.publish(channel, json.dumps(final_message))
        
        return {"status": "success", "conversation_id": conversation_id}
    except Exception as e:
        publish_progress(channel, f"Error processing chat: {str(e)}", status="error")
        return {"status": "error", "error": str(e)}

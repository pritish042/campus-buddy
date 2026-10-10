"""Campus Buddy - College assistant agent built with Google ADK."""

import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from .tools import (
    get_timetable,
    get_canteen_menu,
    calculate_cgpa,
    add_reminder,
    list_reminders,
)

# Load environment variables from .env file if available
load_dotenv()

# Determine model configuration (qwen/qwen3.8-27b or openai/gpt-oss-120b on Groq)
DEFAULT_MODEL = "groq/qwen/qwen3.8-27b"
MODEL_NAME = os.getenv("ADK_MODEL", DEFAULT_MODEL)

# Setup LiteLLM backend
# max_tokens keeps responses concise and fits provider rate limits
# num_retries provides resilience against transient 429 rate limit spikes
MODEL = LiteLlm(
    model=MODEL_NAME,
    max_tokens=400,
    num_retries=5,
)

AGENT_INSTRUCTION = """You are Campus Buddy, an enthusiastic, friendly, and reliable AI assistant for college students.

Core Behavior & Rules:
1. Grounded Information:
   - For class schedules or timetable inquiries, ALWAYS call the `get_timetable` tool.
   - For canteen food or meal menus, ALWAYS call the `get_canteen_menu` tool.
   - NEVER invent classes, room numbers, timings, or canteen menu items.

2. Accurate Computations:
   - For CGPA or grade calculations, ALWAYS call the `calculate_cgpa` tool with the grade points and credits.
   - NEVER perform manual mental math or hallucinate GPA calculations.

3. Session Memory & Reminders:
   - When a student asks you to remember or take a note of a task, call `add_reminder`.
   - When a student asks what they have to do or what reminders they saved, call `list_reminders`.
   - If asked about notifications, clearly clarify that reminders are stored in the current chat session and do not trigger push/calendar notifications.

4. Clarifications:
   - If a student asks for a schedule or menu without specifying the day, or asks for CGPA without providing grades and credits, ask a short, polite clarifying question.

5. Formatting & Tone:
   - Pass days as full weekday names with the first letter capitalized (e.g., "Monday", "Friday").
   - Keep answers warm, concise, clear, and well-structured using bullet points.
"""

root_agent = Agent(
    name="campus_buddy",
    model=MODEL,
    description="A friendly campus assistant for first and second year college students.",
    instruction=AGENT_INSTRUCTION,
    tools=[
        get_timetable,
        get_canteen_menu,
        calculate_cgpa,
        add_reminder,
        list_reminders,
    ],
)

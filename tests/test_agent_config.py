"""Test agent structure, tool registration, and runner compatibility."""

import pytest
from campus_buddy.agent import root_agent
from campus_buddy.tools import (
    get_timetable,
    get_canteen_menu,
    calculate_cgpa,
    add_reminder,
    list_reminders,
)


def test_root_agent_metadata():
    assert root_agent.name == "campus_buddy"
    assert "assistant" in root_agent.description.lower()
    assert "timetable" in root_agent.instruction.lower() or "schedule" in root_agent.instruction.lower()


def test_root_agent_tools_registration():
    tool_names = [tool.__name__ if hasattr(tool, "__name__") else getattr(tool, "name", str(tool)) for tool in root_agent.tools]
    assert "get_timetable" in tool_names
    assert "get_canteen_menu" in tool_names
    assert "calculate_cgpa" in tool_names
    assert "add_reminder" in tool_names
    assert "list_reminders" in tool_names

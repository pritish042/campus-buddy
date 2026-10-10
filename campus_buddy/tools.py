"""Tools for Campus Buddy agent."""

import math
from typing import Any
from google.adk.tools import ToolContext
from .sample_data import SAMPLE_TIMETABLE, SAMPLE_CANTEEN_MENU


def get_timetable(day: str) -> dict[str, Any]:
    """Returns the class timetable for a given weekday.

    Args:
        day: Full weekday name (e.g., "Monday", "Tuesday", "Wednesday", "Thursday", "Friday").

    Returns:
        A dictionary containing the status, day name, and scheduled classes, or an error message.
    """
    if not isinstance(day, str):
        return {
            "status": "error",
            "message": "Day must be provided as a string (e.g. 'Monday').",
        }

    normalized_day = day.strip().lower()
    if not normalized_day:
        return {
            "status": "error",
            "message": "Please specify a weekday (e.g., 'Monday' to 'Friday').",
        }

    classes = SAMPLE_TIMETABLE.get(normalized_day)
    if not classes:
        return {
            "status": "error",
            "message": f"No classes found for '{day.strip()}'. Classes are scheduled Monday through Friday.",
        }

    return {
        "status": "success",
        "day": normalized_day.title(),
        "classes": classes,
    }


def get_canteen_menu(day: str) -> dict[str, Any]:
    """Returns the canteen menu for a given weekday.

    Args:
        day: Full weekday name (e.g., "Monday", "Tuesday", "Wednesday", "Thursday", "Friday").

    Returns:
        A dictionary containing the status, day name, and menu items, or an error message.
    """
    if not isinstance(day, str):
        return {
            "status": "error",
            "message": "Day must be provided as a string (e.g. 'Friday').",
        }

    normalized_day = day.strip().lower()
    if not normalized_day:
        return {
            "status": "error",
            "message": "Please specify a weekday (e.g., 'Monday' to 'Friday').",
        }

    menu = SAMPLE_CANTEEN_MENU.get(normalized_day)
    if not menu:
        return {
            "status": "error",
            "message": f"Canteen is closed on '{day.strip()}'. The canteen operates Monday through Friday.",
        }

    return {
        "status": "success",
        "day": normalized_day.title(),
        "menu": menu,
    }


def calculate_cgpa(grade_points: list[float], credits: list[int]) -> dict[str, Any]:
    """Calculates the Cumulative Grade Point Average (CGPA) as a credit-weighted average.

    Formula: CGPA = Sum(grade_point * credit) / Sum(credits)

    Args:
        grade_points: List of subject grade points (scale 0 to 10), e.g., [9.0, 8.0, 10.0].
        credits: List of subject credits in corresponding order, e.g., [4, 3, 3].

    Returns:
        A dictionary containing status and calculated CGPA, or a detailed error message.
    """
    if not isinstance(grade_points, (list, tuple)) or not isinstance(credits, (list, tuple)):
        return {
            "status": "error",
            "message": "Both grade_points and credits must be provided as lists.",
        }

    if not grade_points or not credits:
        return {
            "status": "error",
            "message": "Grade points and credits lists cannot be empty.",
        }

    if len(grade_points) != len(credits):
        return {
            "status": "error",
            "message": (
                f"Mismatched input lengths: received {len(grade_points)} grade points "
                f"and {len(credits)} credit values. Provide one credit value for each subject."
            ),
        }

    for idx, (gp, cr) in enumerate(zip(grade_points, credits)):
        if not isinstance(gp, (int, float)) or isinstance(gp, bool):
            return {
                "status": "error",
                "message": f"Grade point at index {idx} ({gp}) is not a valid number.",
            }
        if not math.isfinite(gp):
            return {
                "status": "error",
                "message": f"Grade point at index {idx} must be a finite number.",
            }
        if gp < 0.0 or gp > 10.0:
            return {
                "status": "error",
                "message": f"Grade point at index {idx} ({gp}) is outside the valid range [0, 10].",
            }

        if not isinstance(cr, (int, float)) or isinstance(cr, bool):
            return {
                "status": "error",
                "message": f"Credit at index {idx} ({cr}) is not a valid number.",
            }
        if not math.isfinite(cr):
            return {
                "status": "error",
                "message": f"Credit at index {idx} must be a finite number.",
            }
        if cr <= 0:
            return {
                "status": "error",
                "message": f"Credit at index {idx} ({cr}) must be a positive number greater than 0.",
            }

    total_credits = sum(credits)
    if total_credits <= 0:
        return {
            "status": "error",
            "message": "Total sum of credits must be greater than 0.",
        }

    weighted_sum = sum(gp * cr for gp, cr in zip(grade_points, credits))
    cgpa = round(weighted_sum / total_credits, 2)

    return {
        "status": "success",
        "cgpa": cgpa,
        "total_credits": total_credits,
    }


def add_reminder(task: str, tool_context: ToolContext) -> dict[str, Any]:
    """Saves a reminder for the student in the current session state.

    Args:
        task: Description of the task or item to remember.
        tool_context: ADK tool context providing access to session state.

    Returns:
        A dictionary containing the status, saved task, total reminders count, and note.
    """
    if not isinstance(task, str) or not task.strip():
        return {
            "status": "error",
            "message": "Task description cannot be blank or empty.",
        }

    clean_task = task.strip()
    reminders = tool_context.state.get("reminders", [])
    if not isinstance(reminders, list):
        reminders = []

    reminders.append(clean_task)
    tool_context.state["reminders"] = reminders

    return {
        "status": "success",
        "saved": clean_task,
        "total_reminders": len(reminders),
        "note": "Reminder saved in conversation session state (no push/scheduled notifications).",
    }


def list_reminders(tool_context: ToolContext) -> dict[str, Any]:
    """Lists all reminders saved by the student in this session.

    Args:
        tool_context: ADK tool context providing access to session state.

    Returns:
        A dictionary containing the status, list of reminders, and count.
    """
    reminders = tool_context.state.get("reminders", [])
    if not isinstance(reminders, list):
        reminders = []

    return {
        "status": "success",
        "reminders": reminders,
        "count": len(reminders),
    }

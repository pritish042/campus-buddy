"""Unit tests for Campus Buddy tools and state management."""

import pytest
import math
from campus_buddy.tools import (
    get_timetable,
    get_canteen_menu,
    calculate_cgpa,
    add_reminder,
    list_reminders,
)


class MockToolContext:
    """Mock ADK ToolContext to test session state read/write."""

    def __init__(self, state: dict | None = None):
        self.state = state if state is not None else {}


class TestTimetableTool:
    """Test get_timetable tool functionality and input normalization."""

    def test_get_monday_timetable_success(self):
        result = get_timetable("Monday")
        assert result["status"] == "success"
        assert result["day"] == "Monday"
        assert len(result["classes"]) == 3
        assert "09:00 Python Programming" in result["classes"]

    @pytest.mark.parametrize(
        "day_input, expected_day",
        [
            ("monday", "Monday"),
            ("  FRIDAY  ", "Friday"),
            ("Wednesday", "Wednesday"),
            ("thursday", "Thursday"),
            ("Tuesday", "Tuesday"),
        ],
    )
    def test_get_timetable_case_and_whitespace_normalization(self, day_input, expected_day):
        result = get_timetable(day_input)
        assert result["status"] == "success"
        assert result["day"] == expected_day
        assert isinstance(result["classes"], list)
        assert len(result["classes"]) > 0

    def test_get_timetable_weekend_returns_error(self):
        result = get_timetable("Saturday")
        assert result["status"] == "error"
        assert "No classes found for 'Saturday'" in result["message"]

    def test_get_timetable_empty_string_returns_error(self):
        result = get_timetable("   ")
        assert result["status"] == "error"
        assert "Please specify a weekday" in result["message"]

    def test_get_timetable_non_string_returns_error(self):
        result = get_timetable(123)  # type: ignore
        assert result["status"] == "error"
        assert "must be provided as a string" in result["message"]


class TestCanteenMenuTool:
    """Test get_canteen_menu tool functionality and input normalization."""

    def test_get_friday_menu_success(self):
        result = get_canteen_menu("Friday")
        assert result["status"] == "success"
        assert result["day"] == "Friday"
        assert "Chicken Biryani" in result["menu"]

    @pytest.mark.parametrize(
        "day_input, expected_day, expected_dish",
        [
            ("monday", "Monday", "Idli"),
            ("  Tuesday  ", "Tuesday", "Poori"),
            ("WEDNESDAY", "Wednesday", "Veg Biryani"),
            ("thursday", "Thursday", "Rajma Chawal"),
            ("friday", "Friday", "Pongal"),
        ],
    )
    def test_get_canteen_menu_normalization(self, day_input, expected_day, expected_dish):
        result = get_canteen_menu(day_input)
        assert result["status"] == "success"
        assert result["day"] == expected_day
        assert expected_dish in result["menu"]

    def test_get_canteen_menu_weekend_returns_error(self):
        result = get_canteen_menu("Sunday")
        assert result["status"] == "error"
        assert "Canteen is closed on 'Sunday'" in result["message"]

    def test_get_canteen_menu_blank_returns_error(self):
        result = get_canteen_menu("   ")
        assert result["status"] == "error"
        assert "Please specify a weekday" in result["message"]


class TestCgpaCalculatorTool:
    """Test calculate_cgpa math accuracy and robust input validation."""

    def test_calculate_cgpa_standard_case(self):
        # Grades: [9, 8, 10], Credits: [4, 3, 3] -> (9*4 + 8*3 + 10*3) / (4+3+3) = (36+24+30)/10 = 9.0
        result = calculate_cgpa([9, 8, 10], [4, 3, 3])
        assert result["status"] == "success"
        assert result["cgpa"] == 9.0
        assert result["total_credits"] == 10

    def test_calculate_cgpa_rounding(self):
        # Grades: [8.5, 9.2], Credits: [3, 4] -> (25.5 + 36.8) / 7 = 62.3 / 7 = 8.90
        result = calculate_cgpa([8.5, 9.2], [3, 4])
        assert result["status"] == "success"
        assert result["cgpa"] == 8.9

    def test_calculate_cgpa_rejects_empty_inputs(self):
        result = calculate_cgpa([], [])
        assert result["status"] == "error"
        assert "cannot be empty" in result["message"]

    def test_calculate_cgpa_rejects_mismatched_lengths(self):
        result = calculate_cgpa([9.0, 8.0], [4])
        assert result["status"] == "error"
        assert "Mismatched input lengths" in result["message"]

    def test_calculate_cgpa_rejects_grades_below_zero(self):
        result = calculate_cgpa([-1.0, 8.0], [3, 3])
        assert result["status"] == "error"
        assert "outside the valid range [0, 10]" in result["message"]

    def test_calculate_cgpa_rejects_grades_above_ten(self):
        result = calculate_cgpa([11.0, 8.0], [3, 3])
        assert result["status"] == "error"
        assert "outside the valid range [0, 10]" in result["message"]

    def test_calculate_cgpa_rejects_zero_or_negative_credits(self):
        result_zero = calculate_cgpa([9.0, 8.0], [0, 3])
        assert result_zero["status"] == "error"
        assert "must be a positive number greater than 0" in result_zero["message"]

        result_neg = calculate_cgpa([9.0, 8.0], [-2, 3])
        assert result_neg["status"] == "error"
        assert "must be a positive number greater than 0" in result_neg["message"]

    def test_calculate_cgpa_rejects_nan_and_inf(self):
        result_nan = calculate_cgpa([float("nan"), 8.0], [3, 3])
        assert result_nan["status"] == "error"
        assert "finite number" in result_nan["message"]

        result_inf = calculate_cgpa([9.0, 8.0], [float("inf"), 3])
        assert result_inf["status"] == "error"
        assert "finite number" in result_inf["message"]

    def test_calculate_cgpa_rejects_non_numeric_types(self):
        result = calculate_cgpa(["A", "B"], [4, 3])  # type: ignore
        assert result["status"] == "error"
        assert "not a valid number" in result["message"]


class TestReminderToolsAndSessionState:
    """Test add_reminder and list_reminders with session state and isolation."""

    def test_add_and_list_reminders_in_same_session(self):
        session_context = MockToolContext()

        # Add first reminder
        res1 = add_reminder("Submit Digital Logic lab report", session_context)
        assert res1["status"] == "success"
        assert res1["saved"] == "Submit Digital Logic lab report"
        assert res1["total_reminders"] == 1

        # Add second reminder
        res2 = add_reminder("Bring math notebook tomorrow", session_context)
        assert res2["status"] == "success"
        assert res2["total_reminders"] == 2

        # List reminders in same session
        list_res = list_reminders(session_context)
        assert list_res["status"] == "success"
        assert list_res["count"] == 2
        assert list_res["reminders"] == [
            "Submit Digital Logic lab report",
            "Bring math notebook tomorrow",
        ]

    def test_session_state_isolation_between_sessions(self):
        session1 = MockToolContext()
        session2 = MockToolContext()

        add_reminder("Lab submission", session1)
        assert len(list_reminders(session1)["reminders"]) == 1

        # New session starts completely empty
        assert len(list_reminders(session2)["reminders"]) == 0

    def test_reject_blank_or_whitespace_reminders(self):
        session = MockToolContext()

        res_empty = add_reminder("", session)
        assert res_empty["status"] == "error"
        assert "cannot be blank or empty" in res_empty["message"]

        res_spaces = add_reminder("    \n  \t ", session)
        assert res_spaces["status"] == "error"
        assert "cannot be blank or empty" in res_spaces["message"]

        assert len(list_reminders(session)["reminders"]) == 0

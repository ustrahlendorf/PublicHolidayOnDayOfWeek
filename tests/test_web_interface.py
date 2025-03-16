"""Tests for the web interface of the Public Holiday Analyzer."""

import pytest
import pandas as pd
from dataclasses import dataclass
import sys
from pathlib import Path

# Add src directory to Python path if not already added
src_path = str(Path(__file__).parent.parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from web_interface import on_year_change, update_holiday_data


@dataclass
class MockState:
    """Mock State class for testing."""
    def __init__(self):
        self.selected_year = 2024
        self.holiday_data = pd.DataFrame()
        self.notifications = []

    def notify(self, status, message):
        """Mock notify method."""
        self.notifications.append((status, message))


@pytest.fixture
def mock_state():
    """Fixture to provide a mock state for testing."""
    return MockState()


def test_valid_year_change(mock_state):
    """Test year change with valid input."""
    on_year_change(mock_state, None, "2025")
    assert mock_state.selected_year == 2025
    assert len(mock_state.notifications) == 1
    assert mock_state.notifications[0][0] == 'success'
    assert "2025" in mock_state.notifications[0][1]


def test_invalid_year_format(mock_state):
    """Test year change with invalid format."""
    original_year = mock_state.selected_year
    on_year_change(mock_state, None, "invalid")
    assert mock_state.selected_year == original_year
    assert len(mock_state.notifications) == 1
    assert mock_state.notifications[0][0] == 'error'
    assert "valid year" in mock_state.notifications[0][1]


def test_year_out_of_range(mock_state):
    """Test year change with out of range value."""
    original_year = mock_state.selected_year
    on_year_change(mock_state, None, "1900")
    assert mock_state.selected_year == original_year
    assert len(mock_state.notifications) == 1
    assert mock_state.notifications[0][0] == 'error'
    assert "between 1950 and 2099" in mock_state.notifications[0][1]


def test_holiday_data_update(mock_state):
    """Test holiday data update function."""
    update_holiday_data(mock_state)
    
    # Check if DataFrame was created
    assert isinstance(mock_state.holiday_data, pd.DataFrame)
    
    # Check DataFrame structure
    expected_columns = ["Wochentag", "Anzahl", "Feiertage"]
    assert all(col in mock_state.holiday_data.columns for col in expected_columns)
    
    # Check if we have all weekdays
    expected_weekdays = [
        "Montag", "Dienstag", "Mittwoch", "Donnerstag",
        "Freitag", "Samstag", "Sonntag"
    ]
    assert all(day in mock_state.holiday_data["Wochentag"].values for day in expected_weekdays)
    
    # Check data validity
    assert all(isinstance(count, int) for count in mock_state.holiday_data["Anzahl"])
    assert all(isinstance(holidays, str) for holidays in mock_state.holiday_data["Feiertage"])
    
    # Verify that days with no holidays have count 0
    zero_holiday_rows = mock_state.holiday_data[mock_state.holiday_data["Anzahl"] == 0]
    assert all(holidays == "" for holidays in zero_holiday_rows["Feiertage"])


def test_holiday_data_content(mock_state):
    """Test specific holiday data content."""
    update_holiday_data(mock_state)
    
    # Get data for a specific weekday that should have holidays
    monday_data = mock_state.holiday_data[mock_state.holiday_data["Wochentag"] == "Montag"].iloc[0]
    
    # Check if Ostermontag is in the holidays for Monday
    assert "Ostermontag" in monday_data["Feiertage"]
    
    # Total number of holidays should match the sum of Anzahl column
    total_holidays = mock_state.holiday_data["Anzahl"].sum()
    assert total_holidays > 0  # We should have some holidays
    assert total_holidays <= 20  # Reasonable maximum for a year 
"""Tests for the public holiday analyzer."""

from datetime import datetime

import pytest

from public_holiday_analyzer import analyze_holidays, format_holiday_table


def test_analyze_holidays_single_year():
    """Test analyzing holidays for a single year."""
    years = [2024]
    results = analyze_holidays(years)
    
    # Verify we have the expected holidays
    assert "Neujahr" in results
    assert "Karfreitag" in results
    assert "Ostermontag" in results
    assert "Tag der Arbeit" in results
    assert "Christi Himmelfahrt" in results
    assert "Pfingstmontag" in results
    assert "Tag der Deutschen Einheit" in results
    assert "1. Weihnachtstag" in results
    assert "2. Weihnachtstag" in results

    # Verify specific dates for 2024
    # New Year's Day 2024 is on Monday
    assert results["Neujahr"]["Montag"] == 1
    # Christmas Day 2024 is on Wednesday
    assert results["1. Weihnachtstag"]["Mittwoch"] == 1


def test_analyze_holidays_multiple_years():
    """Test analyzing holidays across multiple years."""
    years = [2024, 2025]
    results = analyze_holidays(years)
    
    # Each year should have one New Year's Day
    total_new_years = sum(count for weekday_counts in [results["Neujahr"].values()] for count in weekday_counts)
    assert total_new_years == 2


def test_format_holiday_table():
    """Test the table formatting function."""
    test_data = {
        "Neujahr": {"Montag": 1, "Dienstag": 0, "Mittwoch": 0, "Donnerstag": 0, "Freitag": 0, "Samstag": 0, "Sonntag": 0},
        "Karfreitag": {"Montag": 0, "Dienstag": 0, "Mittwoch": 0, "Donnerstag": 0, "Freitag": 1, "Samstag": 0, "Sonntag": 0}
    }
    years = [2024]
    
    table = format_holiday_table(test_data, years)
    
    # Verify table contains expected elements
    assert "Analyse für die Jahre: 2024" in table
    assert "Wochentag" in table
    assert "Anzahl" in table
    assert "Feiertage" in table
    
    # Normalize whitespace for content verification
    normalized_table = ' '.join(table.split())
    
    # Verify specific content
    assert "Montag | 1 | Neujahr" in normalized_table
    assert "Freitag | 1 | Karfreitag" in normalized_table
    assert "Dienstag | 0 |" in normalized_table


def test_analyze_holidays_empty_years():
    """Test analyzing holidays with empty years list."""
    with pytest.raises(ValueError):
        analyze_holidays([])


def test_format_table_empty_data():
    """Test formatting table with empty data."""
    with pytest.raises(ValueError):
        format_holiday_table({}, [2024]) 
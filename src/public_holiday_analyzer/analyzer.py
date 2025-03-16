"""Module for analyzing public holidays in Germany."""

from collections import defaultdict
from datetime import datetime
import logging
from typing import Dict, List, Tuple

import holidays


# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Create console handler with a higher log level
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
# Create formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
# Add the handler to the logger
logger.addHandler(console_handler)


# Mapping of holiday names from the holidays package to our expected names
HOLIDAY_NAME_MAPPING = {
    "Erster Mai": "Tag der Arbeit",
    "Erster Weihnachtstag": "1. Weihnachtstag",
    "Zweiter Weihnachtstag": "2. Weihnachtstag",
    "Tag der Deutschen Einheit": "Tag der Deutschen Einheit",
    "Christi Himmelfahrt": "Christi Himmelfahrt",
    "Ostermontag": "Ostermontag",
    "Karfreitag": "Karfreitag",
    "Pfingstmontag": "Pfingstmontag",
    "Neujahr": "Neujahr"
}


def analyze_holidays(years: List[int]) -> Dict[str, Dict[str, int]]:
    """
    Analyze German public holidays for given years and count their occurrences by weekday.
    
    Args:
        years: List of years to analyze
        
    Returns:
        Dictionary with holiday names as keys and weekday counts as values
        
    Raises:
        ValueError: If years list is empty
    """
    logger.info("Starting holiday analysis for years: %s", years)
    
    if not years:
        logger.error("Empty years list provided")
        raise ValueError("Years list cannot be empty")
        
    de_holidays = holidays.DE(language='de')
    holiday_weekday_counts: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    
    weekday_names = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    
    for year in years:
        logger.debug("Processing holidays for year %d", year)
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)
        for date in de_holidays[start_date:end_date]:
            original_name = de_holidays[date]
            name = HOLIDAY_NAME_MAPPING.get(original_name, original_name)
            if original_name != name:
                logger.debug("Mapped holiday name from '%s' to '%s'", original_name, name)
            weekday = weekday_names[date.weekday()]
            holiday_weekday_counts[name][weekday] += 1
            logger.debug("Found holiday '%s' on %s", name, weekday)
            
    logger.info("Completed holiday analysis. Found %d unique holidays", len(holiday_weekday_counts))
    return dict(holiday_weekday_counts)


def format_holiday_table(holiday_counts: Dict[str, Dict[str, int]], years: List[int]) -> str:
    """
    Format holiday analysis results as a table string showing total holidays per weekday.
    
    Args:
        holiday_counts: Dictionary with holiday counts by weekday
        years: List of years that were analyzed
        
    Returns:
        Formatted table string showing weekdays with their total holiday counts and holiday names
        
    Raises:
        ValueError: If holiday_counts is empty
    """
    logger.info("Formatting holiday table for %d holidays over years: %s", 
                len(holiday_counts), years)
    
    if not holiday_counts:
        logger.error("Empty holiday counts dictionary provided")
        raise ValueError("Holiday counts dictionary cannot be empty")
        
    weekday_names = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    
    # Calculate total holidays per weekday and collect holiday names
    weekday_totals = defaultdict(int)
    weekday_holidays = defaultdict(list)
    for holiday, counts_by_day in holiday_counts.items():
        for weekday, count in counts_by_day.items():
            if count > 0:
                weekday_totals[weekday] += count
                weekday_holidays[weekday].append(holiday)
    
    # Calculate column widths
    weekday_width = max(len(day) for day in weekday_names)
    count_width = max(3, len(str(max(weekday_totals.values()))))
    holidays_width = max(
        len(", ".join(holidays))
        for holidays in weekday_holidays.values()
    ) if weekday_holidays else 20
    
    # Create header
    header = (f"{'Wochentag':<{weekday_width}} | {'Anzahl':^{count_width}} | "
             f"{'Feiertage':<{holidays_width}}")
    separator = "-" * len(header)
    
    # Create rows
    rows = []
    for weekday in weekday_names:
        count = weekday_totals[weekday]
        holidays = ", ".join(sorted(weekday_holidays[weekday]))
        row = f"{weekday:<{weekday_width}} | {count:^{count_width}} | {holidays:<{holidays_width}}"
        rows.append(row)
        logger.debug("Added row for weekday '%s': %d holidays", weekday, count)
    
    # Combine all parts
    year_range = f"Analyse für die Jahre: {', '.join(map(str, sorted(years)))}"
    logger.info("Table formatting completed")
    return f"{year_range}\n\n{header}\n{separator}\n" + "\n".join(rows) 
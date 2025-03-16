"""Web interface for the Public Holiday Analyzer using Taipy."""

from datetime import datetime
import pandas as pd
from taipy.gui import Gui
from taipy.gui.state import State
from taipy.gui.gui_actions import notify
import socket

# Create initial static data
initial_data = {
    'Wochentag': ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag'],
    'Anzahl': [0, 0, 0, 0, 0, 0, 0],
    'Feiertage': ['', '', '', '', '', '', '']
}

# Initialize state variables
holiday_df = pd.DataFrame(initial_data)
selected_year = str(datetime.now().year)

def find_free_port(start_port=5000, max_port=5010):
    """Find a free port between start_port and max_port."""
    for port in range(start_port, max_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('', port))
                return port
            except OSError:
                continue
    raise RuntimeError(f"No free ports found between {start_port} and {max_port}")

def update_holiday_data(state: State):
    """Update the holiday data table for the given year."""
    try:
        year = int(state.selected_year)
        if 2024 <= year <= 2050:
            # Analyze holidays for the specified year
            from public_holiday_analyzer import analyze_holidays
            holiday_counts = analyze_holidays([year])
            
            # Calculate total holidays per weekday and collect holiday names
            weekday_totals = {}
            weekday_holidays = {}
            weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
            
            for weekday in weekdays:
                total = sum(counts.get(weekday, 0) for counts in holiday_counts.values())
                holidays = [name for name, counts in holiday_counts.items() if counts.get(weekday, 0) > 0]
                weekday_totals[weekday] = total
                weekday_holidays[weekday] = ", ".join(sorted(holidays)) if holidays else ""
            
            # Create new DataFrame
            new_data = {
                'Wochentag': weekdays,
                'Anzahl': [weekday_totals[day] for day in weekdays],
                'Feiertage': [weekday_holidays[day] for day in weekdays]
            }
            state.holiday_df = pd.DataFrame(new_data)
            return True
    except Exception as e:
        print(f"Error updating holiday data: {e}")
        return False

def on_year_change(state: State):
    """Handle year change event."""
    try:
        year = int(state.selected_year)
        if 2024 <= year <= 2050:
            notify(state, 'info', f'Analysiere Jahr {year}...')
            if update_holiday_data(state):
                notify(state, 'success', f'Analyse für {year} abgeschlossen')
            else:
                notify(state, 'error', f'Fehler bei der Analyse für {year}')
        else:
            notify(state, 'error', 'Bitte geben Sie ein Jahr zwischen 2024 und 2050 ein')
    except ValueError:
        notify(state, 'error', 'Bitte geben Sie ein gültiges Jahr ein')

# Define the page content with proper Taipy syntax
page = """
# 🎉 Deutscher Feiertagsanalysator

## Feiertagsverteilung nach Wochentag

<|layout|columns=1 1|
<|part|class_name=table-container|
<|{holiday_df}|table|width=100%|>
|>

<|part|class_name=input-container|
<|part|class_name=input-stack|
<|part|class_name=input-label|
**_Jahr zur Analyse eingeben (2024-2050):_**
|>
<|{selected_year}|input|class_name=year-input|>
<|Analysieren|button|on_action=on_year_change|class_name=analyze-button|>
|>
|>
|>

<style>
.table-container {
    width: 100%;
    margin-left: 20px;
    margin-right: 20px;
}
.input-container {
    margin-left: 40px;
    margin-top: 0px;
    padding-top: 20px;
}
.input-stack {
    display: flex;
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
}
.year-input {
    width: 100px;
    background-color: white !important;
    color: black !important;
    border: none !important;
    outline: none !important;
    border-radius: 4px !important;
}
.year-input input {
    border: none !important;
    outline: none !important;
}
.input-label {
    font-size: 1.4em !important;
    text-decoration: underline !important;
}
/* Target Taipy's MUI input classes */
.year-input .MuiOutlinedInput-root {
    border: none !important;
    outline: none !important;
    border-radius: 4px !important;
}
.year-input .MuiOutlinedInput-notchedOutline {
    border: none !important;
}
.year-input .MuiInputBase-root {
    border: none !important;
    border-radius: 4px !important;
}
.analyze-button {
    background-color: #ff0000 !important;
    color: white !important;
    width: fit-content;
}
.label {
    margin-bottom: 5px;
}
</style>
"""

if __name__ == "__main__":
    # Find an available port
    port = find_free_port()
    print(f"Starting server on port {port}")
    
    # Create GUI
    gui = Gui(page)
    gui.run(port=port, dark_mode=False) 
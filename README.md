# Public Holiday Analyzer

A Python application for analyzing the distribution of German public holidays across weekdays. Features both a web interface and a Python package.

## Features

- Analyze German public holidays for any year between 2024 and 2050
- Count holiday occurrences by weekday
- Generate formatted table output in German
- Modern web interface built with Taipy
- Use as a Python package in your own projects

## Web Interface

1. Start the web interface:
```bash
python src/web_interface.py
```

2. Open your web browser and navigate to the URL shown in the console (typically http://127.0.0.1:5000)
3. Enter a year between 2024 and 2050
4. Click "Analysieren" to see the holiday distribution

## Package Usage

```python
from public_holiday_analyzer import analyze_holidays, format_holiday_table

# Analyze holidays for specific years
years = [2024, 2025, 2026]
holiday_counts = analyze_holidays(years)

# Print formatted results
table = format_holiday_table(holiday_counts, years)
print(table)
```

You can also run the example script:
```bash
python src/example.py
```

## Installation

1. Clone this repository:
```bash
git clone https://github.com/ustrahlendorf/PublicHolidayOnDayOfWeek.git
cd PublicHolidayOnDayOfWeek
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Dependencies

- python-dateutil: Date manipulation utilities
- holidays: Public holiday definitions
- taipy: Web interface framework
- pytest: Testing framework
- Development tools: black, flake8, mypy, isort

## Project Structure

```
PublicHolidayOnDayOfWeek/
├── README.md
├── requirements.txt
├── tests/
│   └── test_analyzer.py
└── src/
    ├── example.py
    ├── web_interface.py
    └── public_holiday_analyzer/
        ├── __init__.py
        └── analyzer.py
```

## Testing

Run the tests using pytest:
```bash
pytest tests/
```

## License

This project is open source and available under the MIT License.

## Author

Created by Uwe Strahlendorf (@ustrahlendorf)

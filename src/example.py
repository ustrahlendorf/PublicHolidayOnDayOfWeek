"""Example usage of the public holiday analyzer."""

import argparse
from public_holiday_analyzer import analyze_holidays, format_holiday_table


def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Analyze German public holidays.')
    parser.add_argument('--year', type=int, default=2024,
                      help='Year to analyze (default: 2024)')
    
    args = parser.parse_args()
    
    # Analyze holidays for the specified year
    years = [args.year]
    
    # Get holiday statistics
    holiday_counts = analyze_holidays(years)
    
    # Format and print results
    table = format_holiday_table(holiday_counts, years)
    print(table)


if __name__ == "__main__":
    main() 
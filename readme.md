Expense Tracker

Description:

A simple cost tracker application that allows you to add, read, and view costs. It also generates a chart showing the distribution of costs by tag.

Features:

    Add new costs
    Read existing costs
    View costs sorted by ID, description, cost, date, or tag
    Filter costs by tag
    Generate a chart showing the distribution of costs by tag

Technologies:

    Python
    argparse
    datetime
    dataclasses
    csv
    pandas
    pickle
    matplotlib

Installation:

Clone the repository and install the dependencies using pip:

git clone https://github.com/bard/expens_track.py.git
cd expens_track
pip install -r requirements.txt

Usage:

To add new costs, use the write command:

python expens_track.py write

To read existing costs, use the read command:

python expens_track.py read

To generate a chart, use the chart command:

python expens_track.py chart

Example:

To add a new cost, you would first run the write command:

python cost_tracker.py write

Then, you would be prompted to enter the following information for each cost:

    Description
    Cost
    Date (YYYY-MM-DD)
    Tag

For example:

Description: Groceries
Cost: 50.00
Date: 2023-10-04
Tag: Food

To read the costs, you would run the read command:

python expens_track.py read

This will display a list of all costs, sorted by ID.

To filter the costs by tag, you can specify the tag when running the read command:

python expens_track.py read Food

This will display a list of all costs with the tag "Food".

To generate a chart, you would run the chart command:

python expens_track.py chart

This will create a pie chart showing the distribution of costs by tag.

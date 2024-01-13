Expense Tracker
A comprehensive cost tracker application that allows you to add, read, view, filter, and analyze your expenses with ease.
Features:
    • Add new costs: Seamlessly add details about your expenses, including description, cost, date, and tag.
    • Read existing costs: Efficiently retrieve all your expenses, organized by ID or filtered by specific tags.
    • View costs sorted: Explore your expenses in a structured manner, sorted by ID, description, cost, date, or tag.
    • Filter costs by tag: Narrow down the list of expenses by specifying desired tags, focusing on specific categories.
    • Generate cost distribution chart: Gain insights into your spending patterns by visualizing the distribution of costs across tags.
Technology Stack:
    • Core Python: Leverage the power of Python to handle data manipulation and user interaction.
    • argparse: Utilize argparse library for command-line argument parsing, enabling user-friendly control.
    • datetime: Employ datetime module to accurately manage timestamps for cost entries.
    • dataclasses: Employ dataclasses decorator to define a custom data structure for representing expenses.
    • csv, pandas, pickle: Utilize csv, pandas, and pickle libraries for data storage, manipulation, and persistence.
    • matplotlib: Leverage matplotlib library to create informative cost distribution charts.
Installation:
    1. Clone the repository using git: git clone https://github.com/bard/expens_track.py.git
    2. Navigate into the project directory: cd expens_track
    3. Install dependencies using pip: pip install -r requirements.txt
Usage:
    1. To add new costs, execute the following command:
       python expens_track.py write
    2. Provide detailed information for each cost, including:
        ◦ Description: Brief description of the expense 
        ◦ Cost: Numeric value of the expense 
        ◦ Date: Expense incurred date in YYYY-MM-DD format 
        ◦ Tag: Relevant category or label for the expense 
    3. To read existing costs, use the following command:
       python expens_track.py read
    4. View the list of all costs, ordered by ID by default.
    5. To filter costs by tag, specify the tag after the read command:
       python expens_track.py read Food
       This will display a list of all costs with the specified tag.
    6. To generate a cost distribution chart, execute the following command:
       python expens_track.py chart
    7. A pie chart will be displayed, showcasing the percentage of expenses attributed to each tag.
Error Handling:
    • Invalid input validation: The application checks for valid data formats and inputs, preventing errors due to invalid entries.
    • File handling errors: Robust file handling ensures data integrity, preventing issues with file operations.
    • Data handling exceptions: The code is equipped to handle exceptions that may arise during data processing and storage.

Expense Tracker

A Comprehensive Cost Tracker Application

Effortlessly track, manage, and analyze your expenses with our comprehensive expense tracker application.

Key Features:

    Seamless Cost Addition: Add detailed expense information, including description, cost, date, and tag, with ease.

    Effortless Expense Retrieval: Efficiently retrieve all your expenses, organized by ID or filtered by specific tags.

    Expense Sorting Flexibility: Explore your expenses in a structured manner, sorted by ID, description, cost, date, or tag.

    Targeted Cost Filtration: Narrow down the list of expenses by specifying desired tags, focusing on specific categories.

    Gain Insights through Cost Distribution Charts: Visualize the distribution of your expenses across tags to gain valuable insights into your spending patterns.

Technology Stack:

    Core Python: Leverage the power of Python for data manipulation, user interaction, and robust application development.

    argparse: Employ the argparse library for user-friendly command-line argument parsing, ensuring intuitive control over the application.

    datetime: Utilize the datetime module to accurately manage timestamps for cost entries, maintaining data integrity.

    dataclasses: Employ the dataclasses decorator to define a custom data structure for representing expenses, enhancing code organization and readability.

    csv, pandas, pickle: Utilize csv, pandas, and pickle libraries for seamless data storage, manipulation, and persistence.

    matplotlib: Leverage the matplotlib library to create informative cost distribution charts, enabling visual data analysis.

Installation:

    Clone the repository using git: git clone https://github.com/czekem/expens_track.py.git

    Navigate into the project directory: cd expens_track

    Install dependencies using pip: pip install -r requirements.txt

Usage:

    To add new costs, execute the following command:

    python expens_track.py write

    Provide detailed information for each cost, including:
        Description: A brief description of the expense
        Cost: The numeric value of the expense
        Date: The date the expense was incurred, in YYYY-MM-DD format
        Tag: A relevant category or label for the expense

    To view existing costs, use the following command:
    python expens_track.py read

    View the list of all costs, ordered by ID by default.

    To filter costs by tag, specify the tag after the read command:
    python expens_track.py read Food

    This will display a list of all costs with the specified tag.

    To generate a cost distribution chart, execute the following command:
    python expens_track.py chart

    A pie chart will be displayed, showcasing the percentage of expenses attributed to each tag.

Error Handling:

    Invalid Input Validation: The application checks for valid data formats and inputs, preventing errors due to invalid entries.

    File Handling Errors: Robust file handling ensures data integrity, preventing issues with file operations.

    Data Handling Exceptions: Thanks to library inquirer, the script is more resistant to handle the possible user errors.

I hope you enjoy using expense tracker application to manage your finances effectively.

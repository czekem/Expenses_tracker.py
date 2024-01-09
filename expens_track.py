import argparse
from typing import List, Dict
import click
import pandas as pd 
import pickle
import os
import csv
import xlrd 
import sqlite3
import inquirer
from collections import Counter

class Cost:
    """This class allow to create cost object, and use tag to check if it exists"""
    next_id = 1
    def __init__(self, description: str, cost: float, time: str, tag: str, id=None):
        self.id = Cost.next_id
        self.description = description
        self.cost = cost
        self.time = time
        self.tag = tag
        Cost.next_id += 1
    def __str__(self):
        return f'id: {self.id}, description: {self.description}, cost: {self.cost}, time: {self.time}, tag: {self.tag}'
   
    def __repr__(self):
        return f'id: {self.id!r}, description: {self.description!r}, cost: {self.cost!r}, time: {self.time!r}, tag: {self.tag!r}'

   
def cost_add() -> List[Cost]:
    """This function allow to add cost to the list, and return it as the cost_list"""
    costs_list = []
    while True:
        questions = [
            inquirer.Text('description', message="Please enter the description"),
            inquirer.Text('cost', message="Please enter the cost"),
            inquirer.Text('time', message="Please enter the time"),
            inquirer.Text('tag', message="Please enter the tag")
        ]
        answers = inquirer.prompt(questions)
        try:
            costs_list.append(Cost(answers['description'], answers['cost'], answers['time'], answers['tag']))
        except ValueError:
            print("Invalid input, please enter id, cost and time as numbers.")
        next_cost_value = input('Do you want to add another cost? (y/n): ').lower()
        if next_cost_value != 'y':
            break
    return costs_list


def format_file():
    """This function allow to check if the user want to save the file in csv, 
    xlsx or db format"""
    questions = [
       inquirer.List('format',
                    message="How do you want to save your file?",
                    choices=['csv', 'xlsx', 'db'],
                    ),
   ]
    answers = inquirer.prompt(questions)
    return answers['format']


def create_filename():
    """This function allow user to create filename under the name that they want"""
    filename = input('Enter file name: ')
    if os.path.isfile(filename):
        overwrite = [inquirer.List('format', message="File already exists. Do you want to overwrite it?", choices=['y', 'n'],)]
        if overwrite == 'y' or overwrite == 'yes':
            return filename
        else:
            return create_filename()
    else:
        try:
            file, extension = filename.rsplit('.', maxsplit=1)
            return file
        except ValueError:
            return filename


def save_file(filename: str, columns: List[str], values: List[List[str]], format: str) -> None: 
    """This function is saving named file, first checking if there is no file with such name,
    if it is not there, it will create new file and save it in the right format.
    If there is a file with such name, it will ask user if he wants to overwrite it,
    or add data to it."""
    df = pd.DataFrame({col: values[i] for i, col in enumerate(columns)})
    full_filename = filename + '.' + format 
    if os.path.isfile(full_filename):
        overwrite = input('File already exists. Do you want to overwrite it? (y/n): ').strip().lower()
        if overwrite == 'n':
            print('File not saved due to existing file.')
            question = input('Do you want to add data to the existing file? [y/n]: ').strip().lower()
            if question == 'n':
                return
            elif question == 'y':
                if format == 'csv':
                   df.to_csv(full_filename, mode='a', index=False, header=False)
                elif format == 'xlsx':
                   with pd.ExcelWriter(full_filename, engine='openpyxl', mode='a') as writer:
                       df.to_excel(writer, index=False, header=False)
                elif format == 'db':
                   # Handle database file here
                   pass
    else:
        if format == 'csv':
            df.to_csv(full_filename, index=False)
        elif format == 'xlsx':
            df.to_excel(full_filename, index=False)
        elif format == 'db':
            # Handle database file here
            pass
    print('File saved successfully.')


def file_open():
    """This function is opening the file that user will name to work with it"""
    filename = input("Please write the name of the file and it's extension:\n").lower()
    file, extension = filename.rsplit('.', maxsplit=1)
    if extension == 'csv':
        with open(filename, 'r', encoding='utf-8') as stream:
            reader = csv.DictReader(stream)
            entries = [Cost(id =int(row['id']), description=row['description'], cost=float(row['cost']), time=str(row['time']), tag=row['tag']) for row in reader]
        return entries
    elif extension == 'db':
        with open(filename, 'rb') as stream:
            entries = pickle.load(stream)
        return entries
    elif extension == 'xlsx':
        data = pd.read_excel(filename, sheet_name='Sheet1')
        entries = [Cost(id =int(row['id']), description=row['description'], cost=float(row['cost']), time=str(row['time']), tag=row['tag']) for index, row in data.iterrows()]
        return entries

def print_in_sorted_way(opening_file: List[Cost]):
    print('=ID= ==DESC== ==COST== ==DATE== ==TAG==')
    for cost in opening_file:
        if cost.cost >= 1000:
          print(f'{cost.id} {cost.description} {cost.cost}, {'''!!!''' if cost.cost >= 1000 else ''} {cost.time} {cost.tag}')  
        else:
            print(f'{cost.id} {cost.description} {cost.cost} {cost.time} {cost.tag}')
    df = pd.DataFrame({vars:(cost)for cost in opening_file})
    df.columns = ['ID', 'DESC','COST', 'DATE', 'TAG']

def tags_check(entries: List[Cost], tag_input: str) -> bool:
    """This function is checking for specyfic tag in file to group them"""
    for entry in entries:
        if tag_input in entry.tag:
            return True
    return False


def whole_tags(entries: List[Cost],tag_input: str) -> Dict[str, float]:
    """This function is allow to show the user 
    all costs that have specific tag"""
    costs_by_tag = {}
    for entry in entries:
        if entry.tag in costs_by_tag:
            costs_by_tag[entry.tag] += entry.cost
        else:
            costs_by_tag[entry.tag] = entry.cost
    return f' The total cost of {tag_input} is: {costs_by_tag[tag_input]}' 

def total_costs(entries: List[Cost]) -> float:
    total = 0
    for entry in entries:
        total += entry.cost
    return f'Total costs in column "cost" is: {total}'



@click.command
def main():
    """This script helps you to manage your costs.
    It's divided to 2 sections. First is to add costs 
    and second is to read them, also by tags"""
    choose_action = input('Do you want to write or read cost? (write/read): ').lower()
    if choose_action == 'write':
        cost_adding_list = cost_add()
        
        id = [entry.id for entry in cost_adding_list]
        description = [entry.description for entry in cost_adding_list]
        cost = [entry.cost for entry in cost_adding_list]
        time = [entry.time for entry in cost_adding_list]
        tag = [entry.tag for entry in cost_adding_list]
        
        format = format_file()
        filename = create_filename()
        saving_the_cost_list = save_file(filename, ['id', 'description', 'cost', 'time', 'tag'], [id, description, cost, time, tag], format=format)
    
    elif choose_action == 'read':
        opening_file = file_open()
        print_in_adjecent_columns = print_in_sorted_way(opening_file)
        tag_input = input('Please enter tag that you want to check:\n').lower()
        checking_tags = tags_check(opening_file, tag_input)
        print(f'Tag "{tag_input}" exists: {checking_tags}')
        print_data_with_tags = whole_tags(opening_file,tag_input)
        print(print_data_with_tags)
        total_cost = total_costs(opening_file)
        print(total_cost)


if __name__ == "__main__":
    main()

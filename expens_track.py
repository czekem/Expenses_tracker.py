import os
import glob
import csv
import pickle
from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

import pandas as pd
import click
import inquirer
import matplotlib.pyplot as plt


@dataclass
class Cost:
    """
    This class allow to create cost object, and use tag to check if it exists,
    and use 'big' to check if it is big cost
    """
    description: str
    cost: float
    time: str
    tag: str
    id: int = None
    big: str = None

    @property
    def next_id(cls):
        cls._next_id = getattr(cls, '_next_id', 1)
        cls._next_id += 1
        return cls._next_id

    def __post_init__(self):
        if self.id is None:
            self.id = self.next_id
        if self.cost >= 1000:
            self.big = '!!!'
        if self.description == '':
            raise ValueError('Please enter the description')
        elif self.cost <= 0:
            raise ValueError('Please enter the cost')
        elif self.time == '':
            raise ValueError('Please enter the date')
        elif self.tag == '':
            raise ValueError('Please enter the tag')
        elif self.cost != float(self.cost):
            raise ValueError('Please enter the cost as a number')

    def __str__(self):
        return f'id: {self.id}, description: {self.description}, cost: {self.cost}, time: {self.time}, tag: {self.tag}, big: {self.big}'

    def __repr__(self):
        return f'id: {self.id!r}, description: {self.description!r}, cost: {self.cost!r}, time: {self.time!r}, tag: {self.tag!r}'

    def __eq__(self, other):
        return (self.id == other.id, self.description == other.description, self.cost == other.cost, self.time == other.time, self.tag == other.tag, self.big == other.big)


def cost_add() -> List[Cost]:
    """
    This function allow to add cost to the list, and return it as the cost_list
    """
    costs_list = []
    while True:
        questions = [
            inquirer.Text('description', message="Please enter the description"),
            inquirer.Text('cost', message="Please enter the cost"),
            inquirer.Text('time', message="Please enter the date"),
            inquirer.Text('tag', message="Please enter the tag")
        ]
        answers = inquirer.prompt(questions)
        
        try:
            costs_list.append(Cost(answers['description'], float(answers['cost']), answers['time'], answers['tag']))
        except ValueError:
            print("Invalid input, please enter id, cost and time as numbers.")
        next_cost_value = input('Do you want to add another cost? (y/n): ').lower()
        if next_cost_value != 'y':
            break
    
    return costs_list


def format_file():
    """
    This function allow to check if the user want to save the file in csv, 
    xlsx or db format
    """
    questions = [
       inquirer.List('format',
                     message="How do you want to save your file?",
                     choices=['csv', 'xlsx', 'db'],
                     ),]
    answers = inquirer.prompt(questions)
    
    return answers['format']


def create_filename():
    """
    This function allow user to create filename under the name that they want
    """
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


def save_db(cost_adding_list, format, filename):
    """
    This function allow to save a db file
    """
    if format == 'db':
        if os.path.isfile(filename):
            overwrite = input('File already exist. Do you want to overwrite it? [y/n]: ').strip().lower()
            if overwrite == 'n':
                question = input('Do you want to add data to the existing file? [y/n]: ').strip().lower()
                if question == 'y':
                    full_filename = filename + '.' + format  # lub os.join(filename, format)
                    with open(full_filename, 'ab') as stream:
                        pickle.dump(cost_adding_list, stream)
                        print('The data for {full_filename} has been added.')
                else:
                    print('File not save due to the existing file.')
                    
        else:
            full_filename = filename + '.' + format 
            with open(full_filename, 'wb') as stream:
                pickle.dump(cost_adding_list, stream)
            print(f'File {full_filename} has been saved in database.')


def save_file(filename: str, columns: List[str], values: List[List[str]], format: str) -> None: 
    """This function is saving named file, 
    first checking if there is no file with such name,
    if it is not there, 
    it will create new file and save it in the right format.
    If there is a file with such name, it will ask user if he wants to
    overwrite it,
    or add data to it.
    """
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
                    existing_df = pd.read_excel(full_filename)
                    combined_df = pd.concat([existing_df, df], ignore_index=True)
                    combined_df.to_excel(full_filename, index=False)
    else:
        if format == 'csv':
            df.to_csv(full_filename, index=False)
        elif format == 'xlsx':
            df.to_excel(full_filename, index=False)
    print('File saved successfully.')


def file_open():
    """
    This function is opening the file that user will name to work with it
    """
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
    """
    This code is printing file data and values in sorted way
    """
    print('=ID= ==DESC== ==COST== ==DATE== ==TAG== ==BIG==')
    for cost in opening_file:
        print(f'{cost.id} {cost.description} {cost.cost}, { cost.cost} {cost.time} {cost.tag } {cost.tag} {cost.big} ')  # te wyrażenie zwracało tuple tak lepiej  # # print(f'{cost.id} {cost.description} {cost.cost, '!!!'} {cost.time} {cost.tag}')

    
def tags_check(entries: List[Cost], tag_input: str) -> bool:
    """
    This function is checking for specyfic tag in file to group them
    """
    for entry in entries:
        if tag_input in entry.tag:
            return True
        
    return False


def whole_tags(entries: List[Cost],tag_input: str) -> Dict[str, float]:
    """
    This function is allow to show the user 
    all costs that have specific tag
    """
    costs_by_tag = {}
    for entry in entries:
        if entry.tag in costs_by_tag:
            costs_by_tag[entry.tag] += entry.cost
        else:
            costs_by_tag[entry.tag] = entry.cost
            
    return f' The total cost of {tag_input} is: {costs_by_tag[tag_input]}'  # costs_by_tag[tag_input] # if We delete {tag_input} it will show all costs and tags names


def total_costs(entries: List[Cost]) -> float:
    """
    This function is calculating total costs in the selected file
    """
    total = 0
    for entry in entries:
        total += entry.cost
    print("Total costs in column 'cost' is: ", round(total, 2))


def creating_chart(file):
    """
    This function is creating chart
    """
    filename, extension = file.rsplit('.', maxsplit=1)
    if extension == 'csv':
        df = pd.read_csv(filename + '.csv')
    elif extension == 'xlsx':
        df = pd.read_excel(file)
    elif extension == 'db':
        df = pd.read_pickle(file)
        df = pd.DataFrame(df)
        
    grouped_data = df.groupby('tag')['cost'].sum()
    plt.figure(figsize=(10, 5))
    values = grouped_data.values
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(values, labels=grouped_data.index, autopct=lambda p: '{:.0f}'.format(p * sum(values)/100), startangle=90)

    plt.axis('equal')
    plt.title('Cost distribution per tag')
    plt.show()
    # plt.pie(grouped_data, labels=grouped_data.index, autopct='%1.1f%%') here is '%' divide 
    # plt.title('Cost distribution per tag')
    # plt.show()


@click.group()
def cli():
    pass


@cli.command()
def write():
    """
    This function allow user to add data to file,
    it core function to add the cost data and save it to file
    """
    
    cost_adding_list = cost_add()
        
    id = [entry.id for entry in cost_adding_list]
    description = [entry.description for entry in cost_adding_list]
    cost = [entry.cost for entry in cost_adding_list]
    time = [entry.time for entry in cost_adding_list]
    tag = [entry.tag for entry in cost_adding_list]
        
    format = format_file()
    filename = create_filename()
    if format == 'db':
        save_db(cost_adding_list, format, filename)
    else:
        save_file(filename, ['id', 'description', 'cost', 'time', 'tag'], [id, description, cost, time, tag], format=format)
    

@cli.command()
def read():
    """
    This function is allow user to read data from file
    """
    if read:
        opening_file = file_open()
        print_in_sorted_way(opening_file)
        tag_input = input('Please enter tag that you want to check:\n').lower()
        checking_tags = tags_check(opening_file, tag_input)
        print(f'Tag "{tag_input}" exists: {checking_tags}')
        print_data_with_tags = whole_tags(opening_file, tag_input)
        print(print_data_with_tags)
        total_cost = total_costs(opening_file)
        print(total_cost)
 
        
@cli.command()
def chart():
    """
    This function is creating chart
    base on the name and data of the file
    """
    file = input('Enter file name: ')
    creating_chart(file)


if __name__ == "__main__":
    cli()


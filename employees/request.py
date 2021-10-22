import sqlite3
import json
from models import Employee, Location

EMPLOYEES = [
    {
        "id": 1,
        "name": "Paul Rogan",
        "address": "444 Logan Road",
        "location_id": 1,
    },
    {
        "id": 2,
        "name": "Stephen Steven",
        "address": "7302 Justin Lane",
        "location_id": 2,
    },
    {
        "id": 3,
        "name": "Justin Crippen",
        "address": "1212 12th Wall Street",
        "location_id": 2
    }
]

def get_all_employees():
    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.address,
            a.location_id,
            l.id l_id,
            l.name location_name,
            l.address location_address
        FROM employee a
        JOIN Location l
            ON l.id = a.location_id
        """)
        employees = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            employee = Employee(row['id'], row['name'], row['address'],
                            row['location_id'])

            location = Location(row['l_id'], row['location_name'], row['location_address'])
            employee.location = location.__dict__
            employees.append(employee.__dict__)

    return json.dumps(employees)

def get_single_employee(id):
    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.address,
            a.location_id
        FROM employee a
        WHERE a.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        employee = Employee(data['id'], data['name'], data['address'],
        data['location_id'])

        return json.dumps(employee.__dict__)

def create_employee(employee):
    max_id = EMPLOYEES[-1]["id"]
    new_id = max_id + 1
    employee["id"] = new_id
    EMPLOYEES.append(employee)
    return employee

def delete_employee(id):
    employee_index = -1
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            employee_index = index
    if employee_index >= 0:
        EMPLOYEES.pop(employee_index)

def update_employee(id, new_employee):
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            EMPLOYEES[index] = new_employee
            break

def get_employees_by_location(location_id):

    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id
        FROM employee e
        WHERE e.location_id = ?
        """, ( location_id, ))

        employees = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            employee = Employee(row['id'], row['name'], row['address'], row['location_id'])
            employees.append(employee.__dict__)

    return json.dumps(employees)
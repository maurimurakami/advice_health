from app import db

def fetch_cars() -> dict:
    """Reads all cars and owners listed in database"""

    conn = db.connect()
    cars = conn.execute("select * from cars;").fetchall()
    owners = conn.execute("select * from owners;").fetchall()
    conn.close()

    owners_dict_by_id = {f'{x[0]}': x[1] for x in owners}
    owners_list = [{'id': owner[0], 'owner_name':owner[1]} for owner in owners]

    cars_list = []
    for car in cars:
        owner = owners_dict_by_id.get(f'{car[3]}')

        item = {
            'id': car[0],
            "color": car[1],
            "model": car[2],
            "owner": owner
        }
        cars_list.append(item)

    print(cars_list, owners_list)

    return cars_list, owners_list


def insert_new_car(color: str, model: str, owner: id) ->  int:
    """Insert new car to todo table."""

    conn = db.connect()
    owner_cars_query = f'''select count(*) from cars where owner = {owner}'''
    owner_cars = conn.execute(owner_cars_query).fetchall()

    if owner_cars[0][0] >= 3:
        return -1

    query = f'''
        insert into cars(color, model, owner) values('{color}', '{model}', {owner});
    '''
    conn.execute(query)
    query_results = conn.execute('''SELECT currval(pg_get_serial_sequence('cars', 'id'))''')
    query_results = [x for x in query_results]
    car_id = query_results[0][0]
    conn.close()

    return car_id


def insert_new_owner(owner_name: str) ->  int:
    """Insert new owner to todo table."""

    conn = db.connect()
    check_owner = f'''
        select * from owners where owner_name = '{owner_name}'
    '''
    owner = conn.execute(check_owner).fetchall()

    if owner:
        return -1

    query = f'''
        insert into owners(owner_name) values('{owner_name}');
    '''
    conn.execute(query)
    query_results = conn.execute('''SELECT currval(pg_get_serial_sequence('owners', 'id'))''')
    query_results = [x for x in query_results]
    car_id = query_results[0][0]
    conn.close()

    return car_id

def remove_car_by_id(car_id: int) -> None:
    """ remove entries based on car ID """
    conn = db.connect()
    query = f'''delete from cars where id={car_id};'''
    conn.execute(query)
    conn.close()
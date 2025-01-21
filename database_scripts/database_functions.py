# WHEN RETRIEVING DATA FROM THE DATABASE, MAKE SURE TO END THE RETRIEVAL CODE WITH .scalars() SO THAT YOU CAN ACCESS COLUMNS AS row.column_name


# Function for updating data in an existing row
def update_data(db, model, participant_number, data):
    print('\t--- UPDATE_DATA FUNCTION CALLED ---')
    # For format of data, check out the interface in backendDataObject.ts in the front-end folder
    # in the map 'components'
    for k in data.keys():
        print(f"{k}: {data[k]}")
    participant_row = model.query.get(participant_number)

    if not participant_row:
        print(f"\tERROR - PARTICIPANT ROW WAS NOT FOUND!")
        return
    
    for key, value in data.items():
        # Check if the attribute exists on the User model and update the value
        if hasattr(participant_row, key):
            setattr(participant_row, key, value)
        else:
            print(f"\tERROR - ATTRIBUTE '{key}' DOES NOT EXIST IN THE MODEL")

    db.session.commit()
    print(f"\tThe specified row had {len(data)} columns updated with the new data")
    print('\t--- UPDATE_DATA FUNCTION FINISHED ---')
    return


# Function for creating a new row in the database and retrieving the associated id
def new_data(db, model, data):
    print('\t--- NEW_DATA FUNCTION CALLED ---')
    # For format of data, check out the interface in backendDataObject.ts in the front-end folder
    # in the map 'components'

    # Create a new row for the database
    new_row = model(
        time_start=data['time_start'], 
        age=data['age'], 
        gender=data['gender'], 
        nationality=data['nationality'], 
        experience=data['experience'], 
        consumption=data['consumption']
    )
    print('\tNew_row variable generated using the model')
    db.session.add(new_row)
    db.session.commit()
    print(f'\tRow is added to the database with id "{new_row.id}"')
    print('\t--- NEW_DATA FUNCTION FINISHED ---')
    return new_row.id


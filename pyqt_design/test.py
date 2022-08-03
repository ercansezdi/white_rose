import db


if __name__ == "__main__":
    database = db.database("config")
    user = ["ercn","sezdi","5453034444","15ag0115","50"]
    result = database.add_user(user)
    #result = database.delete_user(user[2])
    
    user = ["sezdi","ercam","5453034444","15155115","45"]
    
    result = database.update_user(user)
    print(result)
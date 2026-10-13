import argparse

from pymongo import MongoClient


uri = "mongodb://localhost:27017"

client = MongoClient(uri)

db = client.my_database

# Creating a command line interface
parser = argparse.ArgumentParser(description='Working with cats ')
parser.add_argument('--action',
                    help=
                    'create_one,'
                    'create_many,'
                    'update_age,'
                    'update_features,'
                    'read_one,'
                    'read_all,'
                    'delete_one,'
                    'delete_all'
                    )    #CRUD action
parser.add_argument('--id')
parser.add_argument('--name')
parser.add_argument('--age')
parser.add_argument('--features', nargs='+')

arg = vars(parser.parse_args())

action = arg.get('action')
pk = arg.get('id')
name = arg.get('name')
age = arg.get('age')
features = arg.get('features')


def add_cat_features(name:str, feature:str) -> list | Exception:
    """
    Add a new characteristic to the `features` list of the cat named...
    :param name: name of the cat
    :param feature: feature of the cat
    :return: list or Exception
    """
    try:
        db.cats.update_one({"name": name}, {"$push": {'features': feature[0]}})
        result = find_one_cat(name)
        return result
    except Exception as e:
        return e


def create_one_cat(name:str, age:int, features:list) -> list | Exception:
    """
    Creating a document for one cat
    :param name: name of the cat
    :param age: age of the cat
    :param features: features of the cat
    :return: list or Exception
    """
    try:
        result = db.cats.insert_one({
        "name": name,
        "age": age,
        "features": features
        })
        return result
    except Exception as e:
        return e


# def create_many_cats(name:list, age:list, features:list[list]) -> list | Exception:
#     """
#     Creating a document for many cats
#     :param name: name of the cats
#     :param age: age of the cats
#     :param features: features of the cats
#     :return: list or Exception
#     """
#     try:
#         for i in range(len(name)):
#             create_one_cat(name[i], age[i], features[i])
#         result = find_all_cats()
#         return result
#     except Exception as e:
#         return e


def delete_one_cat(name:str) -> list | Exception:
    """
    Deleting a document for one cat
    :param name: name of the cat:
    :return: list or Exception
    """
    try:
        result = db.cats.delete_one({"name": name})
        return result
    except Exception as e:
        return e

def delete_all_cats() -> int | Exception:
    """
    Deleting all cats
    :return: number of deleted cats
    """
    try:
        result = db.cats.delete_many({})
        return result
    except Exception as e:
        return e


def find_all_cats() -> list:
    """
    Find all cats
    :return: list of documents for all cats
    """
    try:
        return db.cats.find()
    except Exception as e:
        return e


def find_one_cat(name:str) -> list:
    """
    Find a document for one cat
    :param name: name of the cat
    :return: list of documents
    """
    try:
        result = db.cats.find_one({"name": name})
        return result
    except Exception as e:
        return e


def update_cat_age(name:str, age:int) -> list | Exception:
    """
    Update an age for one cat
    :param name: name of the cat
    :param age: new age of the cat
    :return: list or Exception
    """
    try:
        db.cats.update_one({"name": name},
            { "$set": {
                'age': age}
            })
        result = find_one_cat(name)
        return result
    except Exception as e:
        return e



def main():
    match action:
        case 'create_one':
            result = create_one_cat(name, age, features)
            print(result)
        # case 'create_many':
        #     result = create_many_cats(name, age, features)
        #     print(result)
        case 'delete_one':
            result = delete_one_cat(name)
            print(result)
        case 'delete_all':
            result = delete_all_cats()
            print(result)
        case 'read_all':
            result = find_all_cats()
            print([cat for cat in result])
        case 'read_one':
            result = find_one_cat(name)
            print(result)
        case 'update_age':
            result = update_cat_age(name, age)
            print(result)
        case 'update_features':
            result = add_cat_features(name, features)
            print(result)
        case _:
            print('Unknown command')


if __name__ == "__main__":
    main()


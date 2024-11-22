from bson import ObjectId


def serialize_mongo_data(data):
    for key, value in data.items():
        if isinstance(value, ObjectId):
            data[key] = str(value)

    return data

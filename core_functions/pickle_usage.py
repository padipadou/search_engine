import pickle


def pickle_store(object_name, value, prefix_path="../"):
    file_path = "{}data/{}.pickle".format(prefix_path, object_name)

    with open(file_path, 'wb') as file_object:
        pickle.dump(value, file_object, pickle.HIGHEST_PROTOCOL)


def pickle_load(object_name, prefix_path="../"):
    file_path = "{}data/{}.pickle".format(prefix_path, object_name)

    with open(file_path, 'rb') as file_object:
        return pickle.load(file_object)


if __name__ == "__main__":
    pass
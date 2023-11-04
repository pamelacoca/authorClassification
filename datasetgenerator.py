import os
import random

class ds_gen:

    COUTINHO = "coutinho-dataset"
    DENSER = "denser-dataset"
    __PATH_TO_PARSED_DATA__ = "data/parsed/"

    def __get_paragraph__(self, filename):
        f = open(filename, "r", encoding="utf8")
        paragraph = f.read()
        f.close()
        return paragraph
    
    def __get_author_file_names__(self, path):
        author_file_names = os.listdir(path)
        return author_file_names
    
    def __get_index_from_file_name(self, file_name):
        return file_name.split("_")[1].split(".")[0]

    def __get_data__(self, path, dataset_size):
        paragraphs = {}
        author_file_names = self.__get_author_file_names__(path)
        for i, file_name in enumerate(author_file_names, 0):
            if i >= dataset_size:
                return paragraphs
            paragraph = self.__get_paragraph__(path+"/"+file_name)
            index = self.__get_index_from_file_name(file_name)
            paragraphs.update({index: paragraph})
        return paragraphs

    def __get_path_up_configuration__(self, go_up_on_path):
        path_up=""
        for _ in range(go_up_on_path):
            path_up+="../"
        return path_up

    def __get_author_data_path__(self, author, go_up_on_path):
        up_on_path = self.__get_path_up_configuration__(go_up_on_path)
        if(len(up_on_path) == 0):
            author_path = os.path.join(self.__PATH_TO_PARSED_DATA__, author)
        else: 
            author_path = os.path.join(up_on_path,self.__PATH_TO_PARSED_DATA__, author)
        author_abs_path = os.path.abspath(author_path)
        return author_abs_path
    
    def __get_author_data__(self, author, dataset_size, go_up_on_path):
        path = self.__get_author_data_path__(author, go_up_on_path)
        data = self.__get_data__(path, dataset_size)
        return data
    
    def __get_data_by_indices__(self, data, indices):
        selected_data = {}
        data_keys = list(data.keys())
        for index in indices:
            key = data_keys[index]
            selected_data.update({key: data[key]})
        return selected_data
    
    def get_dataset_from_author(self, author, proportion_training, dataset_size, go_up_on_path = 0):
        train_dataset = []
        test_dataset = []

        data = self.__get_author_data__(author, dataset_size, go_up_on_path)
        data_len = len(data)
        train_indices, test_indices = self.__get_indices__(data_len, proportion_training)

        train_dataset = self.__get_data_by_indices__(data, train_indices)
        test_dataset = self.__get_data_by_indices__(data, test_indices)

        return train_dataset, test_dataset

    def get_data_length(self, author, go_up_on_path = 0):
        path = self.__get_author_data_path__(author, go_up_on_path)
        author_file_names = self.__get_author_file_names__(path)
        return len(author_file_names)
    
    def __get_indices__(self, dataset_len, proportion_training):
        train_indices = []
        test_indices = []

        shuffled_indices = [*range(0,dataset_len)]
        random.shuffle(shuffled_indices)

        training_part = int(proportion_training * dataset_len)
        test_part = dataset_len - training_part

        train_counter = 0
        test_counter = 0

        for index in shuffled_indices:
            if(train_counter < training_part):
                train_indices.append(index)
                train_counter+=1
            elif(test_counter < test_part):
                test_indices.append(index)
                test_counter+=1


        return train_indices, test_indices
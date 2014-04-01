import csv
from tabulate import tabulate

from data_files.data import critics
from recommendations import sim_distance, sim_pearson


class Table:
    def __init__(self):
        self.output_file = ''
        self.output_data = []
        self.delimiter = ','

        horizontal_labels = self.get_horizontal_labels()
        horizontal_labels.insert(0, '')
        self.output_data.append(horizontal_labels)
        self.set_lines()

    def get_horizontal_labels(self):
        pass

    def set_lines(self):
        pass

    def save_file(self):
        with open('data_files/' + self.output_file, 'w') as fp:
            a = csv.writer(fp, delimiter=self.delimiter)
            a.writerows(self.output_data)

    def tabulate(self):
        return tabulate(self.output_data[1:], self.output_data[0], tablefmt="grid")



class BasicTable(Table):
    output_file = 'basic.csv'
    def get_horizontal_labels(self):
        movies = set()  # set of all the movies that we have data based on
        for critic in critics.keys():
            movies = movies | set(critics[critic].keys())
        return list(movies)

    def set_lines(self):
        for critic in critics:
            user_data = [critic]
            for movie in self.get_horizontal_labels(): # horizontal data = movies
                user_data.append(critics[critic].get(movie, None))
            self.output_data.append(user_data)


class SimilarityTable(Table):
    output_file = 'SimilarityEuclid.csv'
    def get_horizontal_labels(self):
        return critics.keys()

    def set_lines(self):
        for critic in critics:
            user_data = [critic]
            for person2 in critics.keys(): # horizontal data = movies
                user_data.append(round(sim_distance(critics, critic, person2), 2))
            self.output_data.append(user_data)

class SimilarityPearson(SimilarityTable):
    output_file = 'SimilarityPearson.csv'

    def set_lines(self):
        for critic in critics:
            user_data = [critic]
            for person2 in critics.keys():
                user_data.append(round(sim_pearson(critics, critic, person2), 2))
            self.output_data.append(user_data)


print 'Basic'
print BasicTable().tabulate()
print 'Similarity euclidean:'
print SimilarityTable().tabulate()
print 'Pearson:'
print SimilarityPearson().tabulate()

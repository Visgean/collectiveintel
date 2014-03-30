import csv
from tabulate import tabulate

from data import critics

class Table:
    output_file = ''
    output_data = []
    delimiter = ','

    def __init__(self):
        horizontal_labels = self.get_horizontal_labels()
        horizontal_labels.insert(0, '')
        self.output_data.append(horizontal_labels)
        self.set_lines()

    def get_horizontal_labels(self):
        pass

    def set_lines(self):
        pass

    def save_file(self):
        with open(self.output_file, 'w') as fp:
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



b = BasicTable()
print b.tabulate()

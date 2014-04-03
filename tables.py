from collections import Counter
import csv
from tabulate import tabulate

from data_files.data import critics
from recommendations import sim_distance, sim_pearson, top_matches, transform_preferences


class Table(object):
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

    def save_file(self, output_file):
        with open('data_files/' + output_file, 'w') as fp:
            a = csv.writer(fp, delimiter=self.delimiter)
            a.writerows(self.output_data)

    def tabulate(self):
        return tabulate(self.output_data[1:], self.output_data[0], tablefmt="grid", floatfmt='.2f')



class BasicTable(Table):
    def get_horizontal_labels(self, ):
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
    def get_horizontal_labels(self):
        return critics.keys()

    def set_lines(self):
        for critic in critics:
            user_data = [critic]
            for person2 in critics.keys(): # horizontal data = movies
                user_data.append(round(sim_distance(critics, critic, person2), 2))
            self.output_data.append(user_data)

class SimilarityPearson(SimilarityTable):
    def set_lines(self):
        for critic in critics:
            user_data = [critic]
            for person2 in critics.keys():
                user_data.append(round(sim_pearson(critics, critic, person2), 2))
            self.output_data.append(user_data)


class RecommendTable(Table):
    def __init__(self, target, similarity_alg = sim_pearson):
        self.target = target
        self.similarity_alg = similarity_alg
        super(RecommendTable, self).__init__()

    def get_horizontal_labels(self):
        movies = set()  # set of all the movies that we have data based on
        for critic in critics.keys():
            movies = movies | set(critics[critic].keys())
        movies_to_recommend = movies - set(critics[self.target].keys())  # set of all the movies that 'person' did not see yet

        self.movies_to_recommend = movies_to_recommend

        axe = ['Similarity']

        for movie in movies_to_recommend:
            axe.append(movie)
            axe.append('Similarity * {}'.format(movie))

        return axe

    def set_lines(self):
        others = list(critics.keys())  # creating another instance of critics keys
        others.remove(self.target)

        sum_rankings = Counter()
        n_rankings = Counter()

        for critic in others:
            similarity = self.similarity_alg(critics, self.target, critic)
            sum_rankings['__similarity__'] += similarity

            user_data = [critic, similarity]
            for movie in self.movies_to_recommend:
                ranking = critics[critic].get(movie, None)
                user_data.append(ranking)
                user_data.append(ranking * similarity if ranking else None)
                sum_rankings[movie] += ranking * similarity if ranking else 0
                n_rankings[movie] += 1

            self.output_data.append(user_data)

        total_line = ['Total', sum_rankings['__similarity__']]
        mean_line = ['Mean', None]

        for movie in self.movies_to_recommend:
            total_line.append(None)
            total_line.append(sum_rankings[movie])

            mean_line.append(None)
            mean_line.append(sum_rankings[movie]/n_rankings[movie])

        self.output_data.append(total_line)
        self.output_data.append(mean_line)

# print 'Basic'
# print BasicTable().tabulate()
# print 'Similarity euclidean:'
# print SimilarityTable().tabulate()
# print 'Pearson:'
# print SimilarityPearson().tabulate()
# print RecommendTable('Eva', similarity_alg=sim_distance).tabulate()
# print RecommendTable('Eva').tabulate()


critics = transform_preferences(critics)

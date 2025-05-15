import csv
import json

def movie_dataset_parser(filename):
    with open(filename,encoding='UTF-8') as csv_file:
        
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        data = {}
        name,genre,year,rating,votes,director = 0,2,3,5,6,7
        for index,movie in enumerate(csv_reader):
            if index == 100:
                break
            if movie[rating]:
                movie[rating] = str(round(float(movie[rating]) / 2, 1))
            else:
                movie[rating] = 0
            categories = [movie[genre],movie[rating],movie[votes],movie[director]]
            data[movie[name]+ "(" +movie[year]+")"] = categories
            #print(index)
    json_file = "movies.json"
    with open(json_file, "w",encoding='UTF-8') as jf:
        json.dump(dict(sorted(data.items())), jf, indent=4)
    print(len(data))
    return 

def main():
    movie_dataset_parser('movies.csv')
    
main()
import os

class Virgilio():

    def __init__(self, directory):
        self.directory = directory

    def read_canto_lines(self, canto_number):
        canto_path = os.path.join(self.directory, f"Canto_{canto_number}.txt")
        print(canto_path)

canti_dirname = '/home/emanueleg/Desktop/PP020125/canti'
virgilio = Virgilio(canti_dirname)
virgilio.read_canto_lines(1)

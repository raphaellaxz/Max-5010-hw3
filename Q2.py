import random


def gen_random_bases():
    return random.choice(["A", "C", "T", "G"])


def gen_genome():
    temp_genome = ""
    for i in range(0, 100):
        temp_genome += gen_random_bases()
    return temp_genome


class Bug:
    def __init__(self, genome=None):
        self.g_bases_count = None
        self.c_bases_count = None
        if genome:
            self.genome = genome
        else:
            self.genome = gen_genome()

    def get_fitness(self):
        if "AAA" in self.genome:
            if not self.g_bases_count:
                self.g_bases_count = self.genome.count("G")
            if not self.c_bases_count:
                self.c_bases_count = self.genome.count("C")
            return self.g_bases_count + self.c_bases_count + 5
        else:
            return 0

    def mutate_random_base(self):
        random_index = random.randint(0, len(self.genome) - 1)
        self.set_base(random_index, gen_random_bases())
        self.g_bases_count = None
        self.c_bases_count = None

    def set_base(self, index, bases):
        genome_list = list(self.genome)
        genome_list[index] = bases
        self.genome = "".join(genome_list)

    def __lt__(self, other):
        return self.get_fitness() < other.get_fitness()


def main():
    list_of_bugs = []
    for i in range(0, 10):
        list_of_bugs.append(Bug())
    for bug in list_of_bugs:
        bug.mutate_random_base()


if __name__ == "__main__":
    main()

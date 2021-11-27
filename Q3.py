from Q2 import Bug


class Population:
    def __init__(self):
        self.bug_list = []
        for i in range(50):
            self.bug_list.append(Bug())

    def create_offspring(self):
        new_pop = []
        for old_bug in self.bug_list:
            new_bug = Bug(old_bug.genome)
            new_bug.mutate_random_base()
            new_pop.append(old_bug)
            new_pop.append(new_bug)
        self.bug_list = new_pop

    def cull(self):
        sorted_bugs = sorted(self.bug_list)
        culled_list = []
        for i in range(int(len(sorted_bugs) / 2)):
            culled_list.append(sorted_bugs.pop())
        self.bug_list = culled_list

    def get_mean_fitness(self):
        sum_of_fitness = 0
        for bug in self.bug_list:
            sum_of_fitness += bug.get_fitness()
        return sum_of_fitness / len(self.bug_list)


def main():
    p = Population()
    for i in range(20):
        p.create_offspring()
        p.cull()
        print(p.get_mean_fitness())


if __name__ == "__main__":
    main()

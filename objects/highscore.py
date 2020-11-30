from objects.text import TextObject


class HighScoresTable:
    COUNT_NOTES_FOR_PRINT = 10

    def __init__(self, game, x=400, y=100):
        self.game = game
        self.x = x
        self.y = y
        self.score_strings = list()
        self.read_scores()
        self.count_new_scores = 0

    def read_scores(self):
        self.score_strings = list()
        with open('./data/highscores.txt', 'r') as fin:
            [self.score_strings.append(score.strip().split(' '))
             for score in fin.readlines()]
            for score in self.score_strings:
                score[1] = int(score[1])

    def write_scores(self):
        with open('./data/highscores.txt', 'w') as fout:
            out_strings = [score[0] + ' ' + str(score[1]) + '\n'
                           for score in self.score_strings]
            fout.writelines(out_strings)

    def add_new_score(self, score: str):
        self.score_strings.append([score.split(' ')[0],
                                   int(score.split(' ')[1])])
        self.count_new_scores += 1
        self.sort_scores()
        self.write_scores()

    def sort_scores(self):
        for i in range(len(self.score_strings)):
            for j in range(1, len(self.score_strings) - i):
                if self.score_strings[j - 1][1] < self.score_strings[j][1]:
                    self.score_strings[j - 1], self.score_strings[j] = \
                        self.score_strings[j], self.score_strings[j - 1]
                elif self.score_strings[j - 1][1] == self.score_strings[j][1]:
                    if self.score_strings[j - 1][0] > self.score_strings[j][0]:
                        self.score_strings[j - 1], self.score_strings[j] = \
                            self.score_strings[j], self.score_strings[j - 1]

    def process_logic(self):
        pass

    def process_event(self, event):
        pass

    def process_draw(self, y=100):
        header = TextObject(self.game, text='HIGHSCORES:', x=self.x, y=self.y)
        header.process_draw()
        i = 0
        while i < len(self.score_strings) and \
                i < HighScoresTable.COUNT_NOTES_FOR_PRINT:
            score = self.score_strings[i]
            text_score = score[0] + ' ' + str(score[1])
            y += 40
            score_bar = TextObject(self.game, text=text_score, x=self.x, y=y)
            i += 1
            score_bar.process_draw()

# -*- coding: utf-8; -*-

# Karasek - nie na początku
# Funkcyjne - nie na początku
# Orlef - od 13 sierpnia
# Ola Hamanowicz (z Marzeną) 17 rano

# Spektroskopia - rano i wieczorem w 2. bloku

import copy

COLL_LIMIT = 2
WORKSHOP_LIMIT = 4
PLAN_COLL_LIMIT = 6

SLOT_MIN_WORKSHOPS = [3,3,2,2,3,3]

WORKSHOP_DATA = [
{'id': 154,
 'name': u"Algebra liniowa i kombinatoryka",
 'prow': 'Rami Ayoush',

 'slots': [3],
},
{'id': 148,
 'name': u"Eskalacja uprawnień",
 'prow': u'Mateusz Pstruś',
},
{'id': 137,
 'name': u"Ewolucja wczesnego Wszechświata w modelu Wielkiego Wybuchu i w Inflacji",
 'prow': u'Maciej Konieczka',

 'slots': [1],
},
{'id': 161,
 'name': u"Funkcje arytmetyczne w teorii liczb",
 'prow': u'Paweł Karasek',

 'drop': True,
},
{'id': 130,
 'name': u"Gwiazdy zmienne",
 'prow': u'Marzena Śniegowska',

 'slots': [5,6],
},
{'id': 158,
 'name': u"Kombinatoryka podziałów",
 'prow': u'Michał Kotowski',

 'slots': [3,4],
},
{'id': 143,
 'name': u"Kryptografia symetryczna",
 'prow': u'Bartłomiej Surma',
},
{'id': 155,
 'name': u"Programowanie botów do gry StarCraft: Brood War",
 'prow': u'Robert Tomkowski',

 'slots': [3,4],
},
{'id': 153,
 'name': u"Programowanie funkcyjne",
 'prow': u'Krzysztof Gogolewski',

 'slots': [5],
},
{'id': 162,
 'name': u"Projekt zespołowy",
 'prow': u'Jakub Sygnowski',

 'slots': [3,4],
},
{'id': 141,
 'name': u"Raytracing",
 'prow': u'Paweł Marczewski',

 'slots': [5,6],
},
{'id': 139,
 'name': u"Spektroskopia zrób to sam",
 'prow': u'Łukasz Mioduszewski',

 'drop': True,
},
{'id': 159,
 'name': u"Struktury na Q",
 'prow': u'Damian Orlef',

 'slots': [5,6],
},
{'id': 142,
 'name': u"Synteza i analiza dźwięku",
 'prow': u'Patryk Hes',
},
{'id': 138,
 'name': u"Teoria grup z zastosowaniami w teorii liczb i kombinatoryce",
 'prow': u'Aleksander Horawa',
},
{'id': 134,
 'name': u"Termodynamika Pogody",
 'prow': u'Michalina Pacholska',
},
{'id': 129,
 'name': u"Topologia Kombinatoryczna",
 'prow': u'Piotr Suwara',
},
{'id': 151,
 'name': u"Tożsamości kombinatoryczne i zliczanie",
 'prow': u'Piotr Pakosz',
},
{'id': 150,
 'name': u"Tworzenie debuggerów",
 'prow': u'Michał Kowalczyk',
},
{'id': 132,
 'name': u"Złożoność komunikacyjna",
 'prow': u'Marcin Kotowski',

 'slots': [5,6],
},
]

COR = [
 [3, 0, 2, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 2, 2, 0, 0, 0],
 [0, 6, 0, 0, 0, 0, 2, 5, 0, 0, 3, 0, 0, 4, 0, 0, 1, 1, 5, 0],
 [2, 0, 9, 1, 5, 0, 1, 1, 0, 0, 1, 3, 0, 0, 2, 6, 3, 2, 0, 0],
 [0, 0, 1, 7, 0, 2, 2, 0, 0, 0, 1, 0, 4, 0, 6, 1, 0, 4, 0, 0],
 [0, 0, 5, 0, 10, 1, 1, 1, 1, 0, 1, 4, 0, 0, 2, 6, 2, 1, 0, 0],
 [0, 0, 0, 2, 1, 7, 1, 0, 0, 0, 0, 0, 1, 0, 5, 2, 1, 4, 0, 0],
 [1, 2, 1, 2, 1, 1, 11, 3, 1, 1, 6, 1, 3, 3, 3, 4, 1, 1, 2, 2],
 [1, 5, 1, 0, 1, 0, 3, 8, 2, 1, 5, 0, 0, 4, 0, 1, 1, 0, 4, 0],
 [0, 0, 0, 0, 1, 0, 1, 2, 5, 2, 2, 0, 0, 2, 1, 0, 0, 0, 0, 1],
 [0, 0, 0, 0, 0, 0, 1, 1, 2, 4, 3, 0, 0, 2, 0, 0, 0, 0, 1, 1],
 [1, 3, 1, 1, 1, 0, 6, 5, 2, 3, 11, 0, 2, 5, 2, 2, 1, 0, 3, 2],
 [0, 0, 3, 0, 4, 0, 1, 0, 0, 0, 0, 6, 0, 1, 0, 5, 0, 0, 0, 0],
 [0, 0, 0, 4, 0, 1, 3, 0, 0, 0, 2, 0, 8, 0, 6, 0, 1, 4, 0, 1],
 [0, 4, 0, 0, 0, 0, 3, 4, 2, 2, 5, 1, 0, 10, 1, 1, 1, 0, 4, 1],
 [0, 0, 2, 6, 2, 5, 3, 0, 1, 0, 2, 0, 6, 1, 14, 1, 2, 7, 0, 1],
 [2, 0, 6, 1, 6, 2, 4, 1, 0, 0, 2, 5, 0, 1, 1, 12, 3, 1, 0, 0],
 [2, 1, 3, 0, 2, 1, 1, 1, 0, 0, 1, 0, 1, 1, 2, 3, 7, 1, 1, 0],
 [0, 1, 2, 4, 1, 4, 1, 0, 0, 0, 0, 0, 4, 0, 7, 1, 1, 11, 1, 0],
 [0, 5, 0, 0, 0, 0, 2, 4, 0, 1, 3, 0, 0, 4, 0, 0, 1, 1, 6, 0],
 [0, 0, 0, 0, 0, 0, 2, 0, 1, 1, 2, 0, 1, 1, 1, 0, 0, 0, 0, 3],
]

class Workshop(object):
    def __init__(self, i, data):
        self.i = i
        self.name = data['name']
        self.typ = data.get('typ', '3')
        self.slots_allowed = data.get('slots', [1,2,5,6])

    def draw(self):
        return self.name[:20]

    def collWith(self, w):
        return COR[self.i][w.i]

    def participants(self):
        return COR[self.i][self.i]

WORKSHOPS = []

for i, data in enumerate(WORKSHOP_DATA):
    if not data.get('drop'):
        WORKSHOPS.append(Workshop(i, data))

class Slot(object):
    def __init__(self, n):
        self.n = n
        self.workshops = []

    def add(self, w1):
        if len(self.workshops) >= WORKSHOP_LIMIT:
            return False
        if self.n not in w1.slots_allowed:
            return False
        for w2 in self.workshops:
            if w1.collWith(w2) > COLL_LIMIT:
                return False
            if w1.collWith(w2) >= w1.participants()*0.5:
                return False
        self.workshops.append(w1)
        return True

    def remove(self, w):
        self.workshops.remove(w)

    def draw(self):
        return '(%d)<br>%s' % (self.badness(),
                           '<br>'.join(w.draw() for w in self.workshops))

    def badness(self):
        c = 0
        for w1 in self.workshops:
            for w2 in self.workshops:
                if w1 != w2:
                    c = max(c, w1.collWith(w2))
        return c


N_WORKSHOPS = len(WORKSHOPS)

class Plan(object):
    def __init__(self):
        self.slots = [Slot(1), Slot(2),
                      Slot(3), Slot(4),
                      Slot(5), Slot(6)]

    def badness(self):
        return sum(slot.badness() for slot in self.slots)

    def remove(self, i, w):
        self.slots[i].remove(w)

    def draw(self):
        return ('''<table>
                <tr><td>%s</td><td>%s</td><td>%s</td></tr>
                <tr><td>%s</td><td>%s</td><td>%s</td></tr>
                </table>
                <hr>
                ''' % tuple(self.slots[i].draw() for i in [0,2,4,1,3,5]))

    def find_all(self, i=0):
        if i == len(WORKSHOPS):
            for m, slot in zip(SLOT_MIN_WORKSHOPS, self.slots):
                if len(slot.workshops) < m:
                    return
            yield
            return
        w = WORKSHOPS[i]
        for slot in self.slots:
            if slot.add(w):
                if self.badness() <= PLAN_COLL_LIMIT:
                    for _ in self.find_all(i+1):
                        yield
                slot.remove(w)

def main():
    with open('plans.html', 'w') as f:
        i = 0
        p = Plan()
        print 'Searching...'
        for _ in p.find_all():
            i += 1
            f.write('''
                    <style>
                    td {
                        border: 1px solid black;
                        width: 15em;
                    }
                    </style>
                    ''')
            f.write(p.draw().encode('utf8'))
        print i

if __name__ == '__main__':
    main()

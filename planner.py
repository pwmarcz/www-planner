# -*- coding: utf-8; -*-

import re
import copy

'''

WWW Planner

Program do układania planu warsztatów na WWW. Uwzględnia możliwości
prowadzących, oraz preferencje uczestników, aby wygenerować jak najbardziej
bezkolizyjny plan.

Program zakłada istnienie 6 slotów - 1 i 2 to pierwszy slot warsztatowy
poranny i pierwszy wieczorny, 3 i 4 to drugi poranny i wieczorny, 5 i 6 to dwa
ostatnie. Każde warsztaty zajmują 1 z tych slotów.

Będziesz potrzebować
- listy warsztatów - do wklepania ręcznie,
- listy uczestników na warszatach - do wydostania z aplikacji WWW.

Instrukcja:

1. Wpisz warsztaty (http://warsztatywww.nstrefa.pl/listAllWorkshops) do
   tabelki WORKSHOP_DATA. 'id' to numer w aplikacji warsztatowej.

2. Wejdź na http://warsztatywww.nstrefa.pl/databaseRaw (uwaga - to
   niebezpieczne narzędzie!) i wklej tam zawartość zmiennej QUERY. Powinieneś
   dostać długą tabelkę. Wejdź w źródło (Ctrl-U) i przeklej całe "<table>" do
   pliku q.txt.

3. Uruchom "python planner.py", powinien wygenerować ci tabelkę do pliku
   plans.html z proponowanymi planami.

   Jeśli ci nie odpowiadają, pozmieniaj parametry poniżej i spróbuj jeszcze
   raz. Niższe parametry pozwalają na szybsze działanie programu, ale
   ograniczają przestrzeń poszukiwań.

Powodzenia!

'''

# PARAMETRY

# Maksymalna liczba wspólnych uczestników między dwoma blokami warsztatowymi w
# tym samym slocie
COLL_LIMIT = 4

# Maksymalna liczba warsztatów na jeden slot
WORKSHOP_LIMIT = 4

# Maksymalna liczba kolicji w sumie
PLAN_COLL_LIMIT = 15

# Minimalna liczba warsztatów na slot
SLOT_MIN_WORKSHOPS = [3,3,3,3,3,3]

# Dane o warsztatach
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

 'drop': True,
},
{'id': 161,
 'name': u"Funkcje arytmetyczne w teorii liczb",
 'prow': u'Paweł Karasek',

 'slots': [5,6],
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

# HACK - powtórzone

{'id': 139,
 'name': u"Spektroskopia zrób to sam",
 'prow': u'Łukasz Mioduszewski',

 'slots': [3],
},

{'id': 139,
 'name': u"Spektroskopia zrób to sam",
 'prow': u'Łukasz Mioduszewski',

 'slots': [4],
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

 'slots': [5,6],
},
{'id': 132,
 'name': u"Złożoność komunikacyjna",
 'prow': u'Marcin Kotowski',

 'slots': [5,6],
},
]

class Workshop(object):
    def __init__(self, i, data):
        self.i = i
        self.id = data['id']
        self.drop = data.get('drop', False)
        self.name = data['name']
        self.prow = data['prow']
        self.typ = data.get('typ', '3')
        self.slots_allowed = data.get('slots', [1,2,5,6])
        self.users = set()

    def draw(self):
        return '<b>%s</b> (%s)' % (self.name[:20], self.prow)

    def collWith(self, w):
        return len(self.users & w.users)

    def participants(self):
        return len(self.users)

WORKSHOPS = []

for i, data in enumerate(WORKSHOP_DATA):
    WORKSHOPS.append(Workshop(i, data))


######## WORKSHOP USERS

'''
Zapytanie wyciągające informację o uczestnikach.

Wytłumaczenie magicznych liczb jest pod adresem:
https://code.google.com/p/www-app/source/browse/enum.php
'''

QUERY = '''
select u.uid, u.name, wu.wid, w.title
  from
w1_edition_users eu
join w1_users u on eu.uid=u.uid
join w1_workshop_users wu on u.uid=wu.uid
join w1_workshops w on wu.wid=w.wid
  where
eu.edition=10 and  -- 10. edycja warsztatów
w.edition=10 and   -- jw.
eu.qualified=1 and -- uczestnicy zakwalifikowani na warsztaty
w.status=4 and     -- warszaty zostały zaakceptowane           (blockStatus)
w.type=1 and       -- warsztaty (nie luźny wykład)             (blockType)
participant>0;     -- zgłosił chęć uczestnictwa                (participantStatus)
'''

QUERY_RESULT_FILE = 'q.txt'

def parse_table(s):
    for row in re.findall(r'<tr>(.*?)</tr>', s):
        yield list(re.findall(r'<td>(.*?)</td>', row))

def read_query(table):
    for _i, _uid, name, wid, wtitle in table:
        wid = int(wid)
        for w in WORKSHOPS:
            if w.id == wid:
                w.users.add(name)

read_query(parse_table(open(QUERY_RESULT_FILE).read()))

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
        if w.drop:
            for _ in self.find_all(i+1):
                yield
            return
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
                        width: 20em;
                    }
                    </style>
                    ''')
            f.write(p.draw().encode('utf8'))
        print i

if __name__ == '__main__':
    main()

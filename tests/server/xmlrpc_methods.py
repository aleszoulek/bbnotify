def getAllBuilders():
    return ['failingBuilderB', 'failingBuilderA', 'passingBuilderX']

def getLastBuilds(builder_name, count):
    return {
        'passingBuilderX': [
            [
                'passingBuilderX',
                13,
                1290632470.720937,
                1290632903.109146,
                '1.2.X',
                '14695',
                'success',
                'successful',
            ]
        ],
        'failingBuilderA': [
            [
                'failingBuilderA',
                30,
                1290607051.566614,
                1290607063.804476,
                None,
                '565c4ceadfea6dabd80e615485e2b5b5418090e7',
                'failure',
                'project 1 test',
            ]
        ],
        'failingBuilderB': [
            [
                'failingBuilderB',
                30,
                1290607051.566614,
                1290607063.804476,
                None,
                '565c4ceadfea6dabd80e615485e2b5b5418090e7',
                'failure',
                'project 2 test',
            ]
        ],
    }[builder_name][:count]


METHODS = {
    'getAllBuilders': getAllBuilders,
    'getLastBuilds': getLastBuilds,
}

from collections import defaultdict

kb = [
    ({'ТС': 'Легковой', 'Двери': '4'},
     ('Тип', 'Седан')),
    ({'ТС': 'Легковой', 'Двери': '5'},
     ('Тип', 'Хэтчбек')),
    ({'ТС': 'Грузовой', 'Грузоподьемность': '3Т'},
     ('Тип', 'микроавтобус')),
    ({'ТС': 'Грузовой', 'Грузоподьемность': '10Т'},
     ('Тип', 'фургон')),
    ({'ТС': 'Грузовой', 'Грузоподьемность': '25Т'},
     ('Тип', 'тягач')),

    ({'Тип': 'Хэтчбек', 'Цена': 'дорогой'},
     ('Модель', 'Ford_Focus')),
    ({'Тип': 'Хэтчбек', 'Цена': 'стандарт'},
     ('Модель', 'Sitroen_Picasso')),
    ({'Тип': 'Хэтчбек', 'Цена': 'бюджетный'},
     ('Модель', 'Renault_Sandero')),
    ({'Тип': 'Седан', 'Цена': 'дорогой'},
     ('Модель', 'BMW_M3')),
    ({'Тип': 'Седан', 'Цена': 'стандарт'},
     ('Модель', 'Volkswagen_Jetta')),
    ({'Тип': 'Седан', 'Цена': 'стандарт'},
     ('Модель', 'Volkswagen_Jetta')),
    ({'Тип': 'Седан', 'Цена': 'бюджетный'},
     ('Модель', 'Dachia_Logan')),
]


features = defaultdict(set)
features_res = set()
features_cause = set()
for causes, (f_res, v_res) in kb:
    features_res.add(f_res)
    features[f_res].add(v_res)
    for f, v in causes.items():
        features_cause.add(f)
        features[f].add(v)


features_to_ask = features_cause - features_res


def find_rule(feature, discarded_rules):
    for i in range(len(kb)):
        if i in discarded_rules:
            continue
        s, (f, v) = kb[i]
        if f == feature:
            return i
    return -1


def check_rule(rule_num, context):
    s, (f, v) = kb[rule_num]
    rule_val, unknown_feature = compare(context, s)
    return rule_val, unknown_feature, v


def compare(context, rule_conditions):

    # check if context does not contradict rule_conditions
    for f, v in context:
        for rf, rv in rule_conditions.items():
            if f == rf and v != rv:
                return False, None

    # check if context has all features from rule_conditions (if not, return first unknown rule)
    context_features = set([f for f,v in context])
    rule_features = set([f for f,v in rule_conditions.items()])
    dif = rule_features.difference(context_features)
    if len(dif) > 0:
        return None, next(enumerate(dif))[1]

    return True, None


def has_question(feature):
    return feature in features_to_ask


def get_question(feature):
    return str(feature).capitalize() + '? ', features[feature]

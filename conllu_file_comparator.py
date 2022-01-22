import argparse
import statistics
from statistics import pstdev

from conllu import parse

UD_DEPRELS = {
    "nsubj",
    "obj",
    "iobj",
    "csubj",
    "ccomp",
    "xcomp",
    "obl",
    "vocative",
    "expl",
    "dislocated",
    "advcl",
    "advmod",
    "discourse",
    "nmod",
    "aux",
    "cop",
    "mark",
    "appos",
    "nummod",
    "acl",
    "amod",
    "det",
    "clf",
    "case",
    "conj",
    "cc",
    "fixed",
    "flat",
    "compound",
    "list",
    "parataxis",
    "orphan",
    "goeswith",
    "reparandum",
    "punct",
    "root",
    "dep",
}


def reinit_corerelations_listdict():
    global UD_DEPRELS
    core_relations_list = {deprel: [] for deprel in UD_DEPRELS}
    return core_relations_list


def reinit_corerelations_intdict():
    global UD_DEPRELS
    core_relations_int = {deprel: 0 for deprel in UD_DEPRELS}
    return core_relations_int


parser = argparse.ArgumentParser("CoNLL-U File Comparator utility")
parser.add_argument("gold_file", type=str, help="Path to gold standard CoNNL-U file")
parser.add_argument(
    "system_file", type=str, help="Path to system predicted CoNNL-U file"
)
args = parser.parse_args()

data_reference = open(args.gold_file, "r", encoding="utf-8").read()
data_reference_tokenlist = parse(data_reference)

data_test = open(args.system_file, "r", encoding="utf-8").read()
data_test_tokenlist = parse(data_test)

"""
Procurar entre os tokens de cada sentença do 'data_reference' as relações presentes na lista 'core_relations'
e verificar se elas estão corretas. 
"""

# Contagem da precisão
dict_precision_values = reinit_corerelations_listdict()

# Contagem da cobertura
dict_recall_values = reinit_corerelations_listdict()

# Contagem do número de sentenças de referencia que foram encontradas relações de cada tipo
dict_sentence_rel = reinit_corerelations_listdict()

# Contagem do número de relações core no córpus de teste
dict_count_core_relations = reinit_corerelations_intdict()


for i in range(len(data_reference_tokenlist)):
    # Recuperando as relações core presentes na sentença de referência

    core_relations_refsent = (
        reinit_corerelations_listdict()
    )  # Armazenar as relações core presentes na sentença de referencia
    core_relations_testsent_present = (
        reinit_corerelations_intdict()
    )  # Armazenar o número de relações presentes na sent de teste
    core_relations_testsent_correct = (
        reinit_corerelations_intdict()
    )  # Armazenar o número de relações corretas das presentes na sent de teste

    sentence = data_reference_tokenlist[i]
    for j in range(len(sentence)):
        token = sentence[j]
        token_deprel = token["deprel"].split(":")[0]
        if token_deprel in core_relations_refsent.keys():
            dest = token["form"].lower()
            org = sentence[token["head"] - 1]
            org = org["form"].lower()
            core_relations_refsent[token_deprel].append((dest, org))

    # Comparando as relações core da sentença de teste com as de referência, caso existam
    if i < len(data_test_tokenlist):
        sentence = data_test_tokenlist[i]
        for j in range(len(sentence)):
            token = sentence[j]
            token_deprel = token["deprel"].split(":")[0]
            if token_deprel in core_relations_refsent.keys():
                core_relations_testsent_present[token_deprel] += 1
                dest = token["form"].lower()
                org = sentence[token["head"] - 1]
                org = org["form"].lower()
                dict_count_core_relations[token_deprel] += 1
                if (dest, org) in core_relations_refsent[token_deprel]:
                    core_relations_testsent_correct[token_deprel] += 1

    # Calculando as medidas e colocando nas respectivas listas
    for key_ in dict_precision_values.keys():

        if len(core_relations_refsent[key_]) > 0:
            dict_recall_values[key_].append(
                core_relations_testsent_correct[key_]
                / len(core_relations_refsent[key_])
            )

        if core_relations_testsent_present[key_] > 0:
            dict_precision_values[key_].append(
                core_relations_testsent_correct[key_]
                / core_relations_testsent_present[key_]
            )

        if core_relations_testsent_correct[key_] > 0:
            dict_sentence_rel[key_].append(core_relations_testsent_correct[key_])


"""
Tendo então verificado as relações, pode-se calcular a precisão, cobertura, medida-f e desvio padrão das medidas do 
arquivo de teste.
"""

for key_ in dict_precision_values.keys():

    precision = (
        sum(dict_precision_values[key_]) / len(dict_precision_values[key_])
        if len(dict_precision_values[key_]) > 0
        else 0.0
    )
    recall = (
        sum(dict_recall_values[key_]) / len(dict_recall_values[key_])
        if len(dict_recall_values[key_]) > 0
        else 0.0
    )
    fmeasure = (2 * precision * recall) / (precision + recall + 1e-9)

    try:
        sd_precision = pstdev(dict_precision_values[key_])
        sd_recall = pstdev(dict_recall_values[key_])
    except statistics.StatisticsError:
        sd_precision = float("nan")
        sd_recall = float("nan")

    if dict_count_core_relations[key_] == 0:
        continue

    print('RELATION "' + str(key_) + '"')
    print()
    print(
        'Number of relations "' + str(key_) + '" in test corpus: ',
        dict_count_core_relations[key_],
    )
    print("Precision: ", precision)
    print("Recall: ", recall)
    print("F-measure: ", fmeasure)

    print("Standard Deviation (Precision): ", sd_precision)
    print("Standard Deviation (Recall): ", sd_recall)
    print("---------------------------")

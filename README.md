# Conllu-File-Comparator
Programa em Python que compara as relações de dependência entre um arquivo ".conllu" de teste e outro ".conllu" de referência.

O objetivo do programa é verificar a acurácia de um parser de dependências em relação a um arquivo de referência (anotação correta das sentenças), calculando a *precisão*, *cobertura*, *medida-f* e *desvio padrão da precisão e da cobertura* com relação a quatro relações de dependência

### Setup

```
pip3 install -r requirements.txt
```

### Execução do programa

O usuário deve fazer o download do `.zip` da pasta do repositório e descompactar. Para comparar os dois arquivos `.conllu` o usuário deve colocar os arquivos dentro da pasta descompactada do repositório e abrir o terminal dentro desse repositório (referenciando o repositório). Após isso, é só executar o programa inserindo o seguinte comando no terminal:<br>
```
python3 conllu_file_comparator.py caminho/gold_file.conllu caminho/system_file.conllu
```

O programa deverá dar uma saída no formato do resultado a seguir, exibindo a quantidade e as medidas precisão, cobertura, medida-f e desvio padrão das medidas precisão e cobertura de cada relação:
```
RELATION "nsubj"

Number of relations "nsubj" in test corpus:  517
Precision:  0.482774752129591
Recall:  0.4637883008356547
F-measure:  0.4730911084583783
Standard Deviation (Precision):  0.45746580432209805
Standard Deviation (Recall):  0.4615394258979827
---------------------------
RELATION "csubj"

Number of relations "csubj" in test corpus:  3
Precision:  1.0
Recall:  0.2777777777777778
F-measure:  0.4347826086956522
Standard Deviation (Precision):  0.0
Standard Deviation (Recall):  0.41573970964154905
---------------------------
RELATION "obj"

Number of relations "obj" in test corpus:  435
Precision:  0.535705596107056
Recall:  0.4774477447744775
F-measure:  0.5049017131046266
Standard Deviation (Precision):  0.4531379383644991
Standard Deviation (Recall):  0.4552742844836239
---------------------------
RELATION "iobj"

Number of relations "iobj" in test corpus:  11
Precision:  0.3333333333333333
Recall:  0.09615384615384616
F-measure:  0.14925373134328357
Standard Deviation (Precision):  0.4714045207910317
Standard Deviation (Recall):  0.2780160056692492
---------------------------
```


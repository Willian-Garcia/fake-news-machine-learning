# Explicação para o Pipeline de Treinamento de Modelo PLN

## Coleta e Limpeza de Dados

Nesta API temos como propósito criar um classificador de noticías para poder detectar se são notícias falsas ou verdadeiras utilizando o dataset "fake-and-real-news-dataset" (https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset), neste dataset os dados são divididos em dois arquivos .csv (Fake.csv e True.csv), com mais de 20 mil artigos em cada um deles, que incluem colunas de title("Título") e text("Texto").

Durante o treinamento do modelo(treinar_modelo.py) os dados são lidos utilizando:
```bash
fake = pd.read_csv("Fake.csv")
true = pd.read_csv("True.csv")
```

Os dois datasets são rotulados com suas respectivas classes("falsa" e "verdadeira") e unidos em um unico DataFrame, que utiliza a união entre o título e conteúdo para formar o campo completo de texto analisado:
```bash
df['texto'] = df['title'] + ' ' + df['text']
```

O processo de limpeza do texto não acontece durante o treinamento e sim na classificação. É utilizado a função preprocessar_texto no arquivo recomendacao_service.py para executar um pré-processamento leve:
```bash
def preprocessar_texto(texto: str) -> str:
    frases = tokenizer_sentencas.tokenize(texto)
    return " ".join(frases[:5])
```

Neste caso, ele divide o texto em sentenças usando o PunkSentenceTokenizer com base em pontuação e seleciona as primeiras 5 frases do texto, no entanto, não há nenhuma remoção explícita de "stopwords", pontuação, palavras em maiuscula/minuscula ou de caracteres especiais, isso se deve ao fato dos embeddings BERT esperarem textos "crus" lidados internamento pelo tokenizer do modelo, com isso não há nenhuma mudança perceptivel nos textos em relação aos originais.
Exemplo:

Texto original:
```bash
"NASA CONFIRMS THE DISCOVERY OF A NEW PLANET! This planet is 2x the size of Earth, and may contain liquid water..."
```
Após pré-processamento:
Se as 5 primeiras frases forem como o exemplo acima, o resultado seria:
```bash
"NASA CONFIRMS THE DISCOVERY OF A NEW PLANET! This planet is 2x the size of Earth, and may contain liquid water..."
```
## Vetorização de textos

Os modelos de Machine learning não tem capacidade de compreender o texto bruto diretamente(frases e parágrafos), pois eles utilizam números ao invés de palavras. A vetorização é o processo que converte textos em representações numéricas (vetores) que preservam o significado e a estrutura do contéudo original o máximo possível.
A vetorização é necessária pois permite que os modelos estáticos ou neurais consigam analisar padrões e relações entre palavras, transformando frases em entradas compátiveis com classificadores(Regressão Logística, Random Forest, Redes Neurais, etc) pois sem essa etapa, não seria possível aplicar nenhum algoritmo de classificação sobre os textos.
Esta API utiliza duas abordagens de vetorização: 
Embeddings com DistilBERT:
Nos arquivos treinar_modelos.py e recomendacao_service.py, cada texto é tokenizado usando o DistilBertTokenizer na qual o modelo DistilBertModel gera um vetor de 768 dimensões que representa o significado do texto com a saída sendo o vetor da posição do token ([CLS]) que resume a frase inteira e passa para o classificador (Logistic Regression):
```bash
outputs.last_hidden_state[:, 0, :]  # vetor [batch_size x 768]
```
Exemplo (ilustrativo):
Texto:
```bash
"NASA discovers new habitable planet."
```
Embedding gerado:
```bash
[ 0.123, -0.445, ..., 0.082 ]  # vetor de 768 dimensões
```

TF-IDF.
Para as explicações utilizamos na função explicar_por_tfidf() do arquivo recomendacao_service.py o TfidVectorizer nos corpus de textos para calcular a importância de cada palavra-chave que influencia a classificação, o TF-IDF distribui pesos maiores as palavras mais frequentes no texto mas que são raras no corpus global.
Exemplo (ilustrativo):
Texto:
```bash
"NASA confirms water on Mars."
```
TF-IDF vetor (com 5.000 dimensões, muitas com zero):
```bash
[0, 0.48, 0, 0.61, ..., 0]
```
Palavras com maior peso:
```bash
["confirms", "water", "Mars"]
```

## Treinamento do Modelo

Depois de coletar os dados dos datasets e rotular eles como "falsa" e "verdadeira" foi aplicado uma amostragem estratificada para evitar o desbalanceamento e sobrecarga de processamento, limitando a 1000 textos por classe com um total de 2000 amostras:
```bash
df_bal = df.groupby('label').apply(lambda x: x.sample(min(len(x), limite), random_state=42))
```

Após isso, o dataset foi dividido em conjuntos de treinamento (80%) e teste (20%):
```bash
X_train, X_test, y_train, y_test = train_test_split(X, y_labels, test_size=0.2, random_state=42)
```

Foi utilizado o DistilBERT para extrair embeddings semânticos dos textos onde cada texto é convertido em um vetor numérico de 768 dimensões utilizando o token [CLS], que representa o significado global da frase, neste caso o DistilBERT não foi ajustado e esta apenas sendo usado como extrator de características.
```bash
outputs.last_hidden_state[:, 0, :]  # vetor do token [CLS]
```

Após os embeddings serem gerados com o DistilBERT, eles são utilizados como entrada para um modelo de Regressão Logística, implementado via scikit-learn, a Regressão Logística é um modelo linear de classificação que vai avaliar as probabilidades entre duas ou mais classes com base em um função logística.
Foi configurado para permitir até 1000 iterações com balanceamento automatico das classes.
```bash
modelo = LogisticRegression(max_iter=1000, class_weight="balanced")
modelo.fit(X_train, y_train)
```

## Avaliação dos Modelos:

Depois do treinamento, o modelo é avaliado no conjunto de teste(20%) usando 3 métricas:
Acuracy(Acurácia)
Isto mede a proporção de previsões corretas sobre o total de previsões.
```bash
acurácia = (nº de previsões corretas) / (nº total de previsões)
```

Precision(Precisão):
Isto mede a proporção de verdadeiros positivos entre todas as previsões positivas.
```bash
precisão = VP / (VP + FP)
```

Recall(Revocação):
Isto mede a proporção de verdadeiros positivos entre todos os exemplos realmente positivos.
```bash
recall = VP / (VP + FN)
```

As métricas foram geradas usando o scikit-learn, após o modelo ser testado em treinar_modelo.py:
```bash
from sklearn.metrics import classification_report, accuracy_score

y_pred = modelo.predict(X_test)
print(classification_report(y_test, y_pred, target_names=y.classes_))
print("Acurácia:", round(accuracy_score(y_test, y_pred), 4))
```

Exemplo de Resultados Obtidos(ilustrativo)
              precision    recall  f1-score   support
falsa            0.91       0.90      0.91        200
verdadeira       0.90       0.91      0.90        200

accuracy                             0.905        400
macro avg         0.905      0.905     0.905       400
weighted avg      0.905      0.905     0.905       400

O modelo apresentou acurácia de 90,5%, indicando boa capacidade de generalização.
Precisão e recall estão equilibrados para ambas as classes, o que é ideal para problemas de classificação binária.
A simetria nas métricas entre classes sugere que o balanceamento no pré-processamento foi eficaz.
O uso de embeddings BERT + regressão logística demonstrou ser uma abordagem leve, eficiente e precisa mesmo sem fine-tuning.
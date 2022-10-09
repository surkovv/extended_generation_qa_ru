from rouge1_lemma import rouge1_lemma
print(rouge1_lemma(['деда'], ['Он у деда']))
print(rouge1_lemma(['деда'], ['Он у бабы']))
print(rouge1_lemma(['К лесу задом, к ней передом', '2020'], ['к лесу задом к мне передом', '2021']))


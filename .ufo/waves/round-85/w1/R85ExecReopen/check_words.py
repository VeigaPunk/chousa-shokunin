QUOTES = [
 ("Q1", "Provenance chains comprising only Entities can be formed using the prov:wasDerivedFrom property."),
 ("Q2", "A derivation is a transformation of one entity into another."),
 ("Q3", "then we can say that the bar chart prov:wasDerivedFrom the dataset."),
 ("Q4", "The properties prov:generatedAtTime and prov:invalidatedAtTime can be used to bound the starting and ending moments of an Entity's existence."),
 ("Q5", "Detailed provenance includes facets such as how the resource was generated, why it was generated, by whom, under what conditions"),
 ("Q6", "using what starting-data or source-resource, using what funding/resources, who owns the data, who should be given credit"),
 ("Q7", "Date on which the content on this web page was last reviewed for accuracy and/or completeness."),
]
for qid, q in QUOTES:
    words = q.split()
    print(f"{qid} words={len(words)} in_8_25={8 <= len(words) <= 25} :: {' '.join(words)}")

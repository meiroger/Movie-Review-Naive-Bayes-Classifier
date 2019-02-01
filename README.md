# Movie-Review-Naive-Bayes-Classifier

The tokenize function tokenizes a string of text into its individual words.
These tokenized words and their frequencies are stored into their respective dictionaries, positive or negative, and saved into a text file with the save function. This text file can be loaded with the load and loadfile functions.
The train function calculates the frequency of each word grouped by review sentinment.
The classify function classifies any given piece of text as either positive or negative with the Naive Bayes probability model.

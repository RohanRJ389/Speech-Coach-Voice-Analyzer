# import assemblyai as aai
import spacy
import language_tool_python
tool = language_tool_python.LanguageTool('en-US')

from libraryS2T import speech2Text

nlp = spacy.load("en_core_web_sm")

# aai.settings.api_key = "60e71d0431144820af129bbdff96088c"

audio_url = "./india.wav"

# config = aai.TranscriptionConfig(sentiment_analysis=True)

transcript =  speech2Text(audio_url)

# with open("sentiments1.txt", "a") as file:

#   for sentiment_result in transcript.sentiment_analysis:
#     file.write(sentiment_result.text + "-" + sentiment_result.sentiment + "\n"+"\n")
    

#Check metaphors
def detect_metaphors(text):

    doc = nlp(text)
    for token in doc:
        # Look for verbs that indicate a comparison ("is", "was")
        if token.pos_ == "VERB" and token.lemma_ in ["be", "is", "are", "was", "were"]:
            # Look for nouns that are subjects of the comparison
            subject = [child.text for child in token.children if child.dep_ == "nsubj"]
            if subject:
                # Check if the subject is followed by a metaphorical expression
                for child in token.children:
                    if child.dep_ == "attr" and child.text != subject[0]:
                        return True
        if token.pos_ == "VERB" and token.dep_ == "xcomp" and token.head.pos_ == "VERB" and token.head.dep_ == "advcl":
            # Check if the verb phrase is part of a metaphorical expression
            if token.head.head.pos_ == "VERB" and token.head.head.lemma_ in ["consider", "view", "regard", "see","act"]:
                return True
        # Look for verbs that indicate a comparison ("seem", "appear")
        if token.pos_ == "VERB" and token.lemma_ in ["seem", "appear"]:
            # Look for adjective phrases that are subjects of the comparison
            subject = [child.text for child in token.children if child.dep_ == "nsubj"]
            if subject:
                # Check if the subject is followed by a metaphorical expression
                for child in token.children:
                    if child.dep_ == "acomp" and child.text != subject[0]:
                        return True
                    

        if token.pos_ == "PRON" and token.dep_ == "nsubj":
            # Check if the pronoun is followed by a noun indicating an object of comparison
            for child in token.head.children:
                if child.dep_ == "attr" and child.pos_ == "NOUN":
                    return True
        # Look for nouns that are subjects of a verb
        if token.pos_ == "NOUN" and token.dep_ == "nsubj" and token.head.pos_ == "VERB":
            return True
        
        # Look for nouns that are objects of a verb (e.g., "heart of stone")
        # if token.pos_ == "NOUN" and token.dep_ == "dobj" and token.head.pos_ == "VERB":
        #     return True
        # Look for nouns that are part of a compound noun (e.g., "heartache")

        if token.pos_ == "NOUN" and token.dep_ == "compound":
            return True
        # Look for adjectives that are part of a verb's subject (e.g., "were icicles")
        if token.pos_ == "ADJ" and token.dep_ == "acomp":
            return True
        # Look for adjectives that are part of a noun phrase (e.g., "icicles because of the cold weather")
        if token.pos_ == "ADJ" and token.dep_ == "amod" and token.head.pos_ == "NOUN":
            return True
        
        if token.pos_ == "ADJ" and token.dep_ == "acomp":
            # Check if the adjective is part of a metaphorical expression
            if token.head.pos_ == "NOUN":
                return True
            
            
            
        #simile detection
        if token.text == "as" and token.dep_ == "prep":
            # Check if "as" is followed by an adjective or adverb
            if token.head.pos_ in ["ADJ", "ADV"]:
                return True
        if token.text == "like" and token.dep_ == "prep":
            # Check if "like" is followed by a determiner and a noun or proper noun
            if (token.i + 2) < len(doc):
                next_word = doc[token.i + 1]
                next_next_word = doc[token.i + 2]
                if next_word.pos_ == "DET" and next_next_word.pos_ in ["NOUN", "PROPN"]:
                    return True
                
    return False
metaphor_count=0
text_metaphor=transcript 
metaphor_found = detect_metaphors(text_metaphor)
if detect_metaphors==True:
    metaphor_count+=1
    

print("\n")
print(metaphor_count)


def count_questions(text):
    doc = nlp(text)
    question_count = 0
    for sentence in doc.sents:
        if sentence.text.strip().endswith("?"):
            question_count += 1
        elif sentence[0].lemma_ in ["who", "what", "when", "where", "why", "how"]:
            question_count += 1
    return question_count


def calculate_engagement_score(similes_detected, questions_detected):
    simile_weight=0.6
    question_weight=0.4
    simile_score = simile_weight * similes_detected
    question_score = question_weight * questions_detected
    engagement_min=0
    engagement_max=10
    engagement_score = simile_score + question_score
    normalized_score = ((engagement_score - engagement_min) / (engagement_max - engagement_min)) * 10
    return normalized_score




#grammatical error
def check_and_correct_paragraph(paragraph):
    # Split the paragraph into sentences
    sentences = paragraph.split(". ")
    mistaken_corrected_pairs = []

    # Iterate through each sentence
    for sentence in sentences:
        # Check for grammatical errors in the sentence
        matches = tool.check(sentence)
        
        # If grammatical errors are found, obtain the corrected version
        if matches:
            corrected_sentence = tool.correct(sentence)
            mistaken_corrected_pairs.append((sentence, corrected_sentence))
    
    return mistaken_corrected_pairs

text_grammar = transcript
mistaken_corrected_pairs = check_and_correct_paragraph(text_grammar)

# Append the mistaken-corrected pairs to the file
with open("corrected.txt", "a") as file:
    for mistaken, corrected in mistaken_corrected_pairs:
        file.write(f"Mistaken: {mistaken}\n")



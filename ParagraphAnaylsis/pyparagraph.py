import os
import csv
import re

root_path = os.getcwd()
data_path = os.path.join(root_path,"raw_data")

def loadfiles():
	files = []
	for file in os.listdir(data_path):
		if file.endswith(".txt"):
			files.append(os.path.join(data_path, file))
	return files

files = loadfiles()
for file in files:
	with open(file, 'r') as fh:
		text = fh.read()
		paragraphs = text.split("\n\n")
		for paragraph in paragraphs:
			words = paragraph.split(" ")
			ltr_tot = sum(len(word)for word in words)
			sentences = re.split("[.!?] ", paragraph)
			# for idx, sentence in enumerate(sentences):
			# 	print(f"{idx} : {sentence}")
			wrd_tot = sum(len(sentence.split(" ")) for sentence in sentences)
			word_cnt = len(words)
			sent_cnt = len(sentences)
			if word_cnt == 0:
				avg_ltr = 0
			else:
				avg_ltr = ltr_tot / word_cnt
			if sent_cnt == 0:
				avg_sent = 0
			else:
				avg_sent = wrd_tot / sent_cnt
			#print(paragraph)
			
			summary = (f"Paragraph Analysis\n"
						f"-----------------\n"
						f"Approximate Word Count: {word_cnt}\n"
						f"Approximate Sentence Count: {sent_cnt}\n"
						f"Average Letter Count: {avg_ltr}\n"
						f"Average Sentence Length: {avg_sent}\n"
					)
			print(summary)
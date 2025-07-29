from transformers import pipeline
from pypdf import PdfReader
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

def summarize_text(text, sentence_count=3):
	parser = PlaintextParser.from_string(text, Tokenizer("japanese"))
	summarizer = TextRankSummarizer()
	summary = summarizer(parser.document, sentence_count)
	return " ".join([str(sentence) for sentence in summary])

def extract_text_with_pypdf(pdf_path):
	reader = PdfReader(pdf_path)
	text = ""
	for page in reader.pages:
		t = page.extract_text()
		if t:
			text += t + "\n"
	return text

if __name__ == "__main__":
	result_text = extract_text_with_pypdf("japanese_txt.pdf")
	print(result_text)
	
	summary = summarize_text(result_text)
	print(summary)

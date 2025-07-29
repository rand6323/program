from fpdf import FPDF

def generate_pdf(pdf_path="japanese_txt.pdf", font_path="NotoSansJP-Regular.ttf", txt_file = None):
	pdf = FPDF(format="A4")
	pdf.set_auto_page_break(auto=True, margin=15)
	pdf.add_page()
	pdf.add_font("NotoCJK", "", font_path)
	pdf.set_font("NotoCJK", size=12)
	pdf.multi_cell(pdf.w - 2 * pdf.l_margin, 8, txt_file.strip(), align="L")
	pdf.output(pdf_path)
	print("PDFの出力が完了しました:", pdf_path)

if __name__ == "__main__":
	
	with open('./txt_file.txt', 'r', encoding='utf-8') as f:
		news_text = f.read()
	
	generate_pdf(txt_file=news_text)
	print("PDF が生成されました")

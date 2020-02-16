import numpy as np
from fpdf import FPDF

f = open("Captions.text", "r")
line1 = f.read()
data = line1.splitlines()
data = [i for i in data if len(i) > 0]
data = np.array(data)
data = np.delete(data, np.arange(0, data.size, 3))
data = data.tolist()
f.close()

infile = open("Captions.text", "r")
content = infile.readlines()
infile.close()


class PDF(FPDF):
    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'Note it', 1, 0, 'C')
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


# Instantiation of inherited class
pdf = PDF()
pdf.alias_nb_pages()
pdf.add_page()
pdf.set_font('Times', '', 12)
for i in range(1, 41):
    pdf.cell(0, 10, content[0] + str(i), 0, 1)
pdf.output('tuto2.pdf', 'F')

print(content[0])

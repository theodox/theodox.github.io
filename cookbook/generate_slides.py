#generates the slides from the templates
from string import Template

TOTAL = 90

placeholder = None
with open ("placeholder_template.txt", 'rt') as reader:
	placeholder = reader.read()

placeholder = Template(placeholder)
for idx in range (90):
	filename =  str(idx).zfill(2) + ".md"
	with open (filename, 'wt') as output:
		next = str(idx + 1).zfill(2)
		prev = str(idx - 1).zfill(2)
		output.write(placeholder.substitute(
			index = idx,
			next = next,
			prev = prev,
			total = TOTAL
			))
	print filename
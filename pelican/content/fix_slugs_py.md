import os

def fix_slug(s):
	lowered = s.lower()
	for char in ":.!?[]()& ":
		lowered = lowered.replace(char, "_")
	lowered = lowered.replace("__", "_")
	lowered = lowered.replace("__", "_")
	lowered = lowered.replace("__", "_")
	lowered = lowered.replace("_md", "")
	return lowered

def rewrite(f):
	result = []
	with open(f, 'rt') as handle:
		for line in handle:
Slug: '_in_line_
				s,_,rest = line.partition(":")
				rest = fix_slug(rest)
Slug: _"_+_rest
			result.append(line)

	with open(f, 'wt') as handle:
		handle.writelines(result)

for file in os.listdir("."):
	oldname = fix_slug(file)
	print file, oldname
	if file.endswith("md"):
		rewrite(file)

	os.rename(file, fix_slug(file) + ".md")
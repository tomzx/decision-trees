from generic.choose import choose

def askBoolean(question, default = None):
	result = choose(question, ['true', 'yes', 'y', 'false', 'no', 'n'], default)
	return result in ['true', 'yes', 'y']
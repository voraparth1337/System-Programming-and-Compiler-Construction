def replace_l(l, X, Y):
	for i,v in enumerate(l):
		if v == X:
			l.pop(i)
			l.insert(i, Y)
	return l

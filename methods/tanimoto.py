def tanimoto(v1, v2):
	c1, c2 shr = 0, 0, 0

	for i in range(len(v1):

		if v1[i] != 0: c1 += 1 # v1に存在
		if v2[i] != 0: c2 += 1 # v1に存在
		if v1[i] != 0 and v2[i] != 0: shr +=1 # 両者に存在
	
	return 1.0 - ( float( shr ) / ( c1 + c2 - shr ))
	

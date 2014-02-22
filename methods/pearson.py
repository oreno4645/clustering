from math import sqrt

def pearson( v1, v2) :

	sum1 = sum(v1)
	sum2 = sum(v2) 

	sum1Sq = sum([pow(v,2) for v in v1])
	sum2Sq = sum([pow(v,2) for v in v2])

	pSum = sum([v1[i]*v2[i] for i in range(len(v1))])

	num = pSum - (sum1 * sum2 / len(v1))
	den = sqrt((sum1Sq - pow(sum1,2) / len(v1)) * (sum2Sq - pow(sum2, 2)/len(v1)))
 
	if den == 0: return 0


	return 1.0 - num /den


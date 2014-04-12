import time
import random
import math

people = [('Seymour', 'BOS'),
					('Franny', 'DAL'),
					('Zooey', 'CAK'),
					('Walt', 'MIA'),
					('Buddy', 'ORD'),
					('Les', 'OMA')]
# ニューヨークのラガーディア空港
destination='LGA'

def geneticoptimize( domain, costf, popsize = 50, step = 1, 
											mutprob = 0.2, elite = 0.2, maxiter = 100 ):
	
	# 突然変異の操作
	def mutate( vec ):

		i = random.randint( 0, len( domain ) - 1 )
		if random.random() < 0.5 and vec[ i ] > domain[ i ][ 0 ]:
			return vec[ 0 : i ] + [ vec[ i ] - step ] + vec[ i + 1 : ]

		elif vec[ i ] < domain[ i ][ 1 ]:
			return vec[ 0 : i ] + [ vec[ i ] + step ] + vec[ i + 1 : ] 

	# 交叉の操作
	def crossover( r1, r2 ):

		i = random.randint( 1, len( domain ) - 2 )
		return r1[ 0 : i ] + r2[ i : ]


	# 初期個体群の構築
	pop = []
	for i in range( popsize ):
		
		vec = [ random.randint( domain[ i ][ 0 ], domain[ i ][ 1 ] )	for i in range( len( domain ) ) ]

		pop.append( vec )

	# 各世代の勝者数
	topelite = int( elite * popsize )

	# Main Loop
	for i in range( maxiter ):
		scores = [ ( costf( v ), v ) for v in pop ]
		scores.sort()
		ranked = [ v for ( s, v ) in scores ]
		
		# まず純粋な勝者
		pop = ranked[ 0 : topelite ]

		# 勝者に突然変異や交配を行ったものを追加
		while len ( pop ) < popsize:

			if random.random() < mutprob:

				# 突然変異
				c = random.randint( 0, topelite )
				pop.append( mutate( ranked[ c ] ) )
		
			else:

				# 交叉
				c1 = random.randint( 0, topelite ) 
				c2 = random.randint( 0, topelite ) 	
				pop.append( crossover( ranked[ c1 ], ranked[ c2 ] ) )

		# 現在のベストスコアを出力
		print scores[ 0 ][ 0 ]

	return scores[ 0 ][ 1 ]

import dorm
import optimization

#init_vec = [0,0,0,0,0,0,0,0,0,0]

dorm.printsolution( [0,0,0,0,0,0,0,0,0,0])

s = optimization.geneticoptimize( dorm.domain, dorm.dormcost )
dorm.printsolutions( s )

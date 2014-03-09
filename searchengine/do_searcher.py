import crawler
import searcher
import sys

reload(searcher)
e = searcher.searcher('searchindex.db')

# e.getmatchrows('get set')


# e.query( 'get set')

# e.calculatepagerank()

cur = e.con.execute( 'select * from pagerank order by score desc' )
# for i in range( 10 ): print cur.next()

e.query( 'get set')



# e.geturlname( )


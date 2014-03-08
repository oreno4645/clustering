import searcher
import sys

reload(searcher)
e = searcher.searcher('searchindex.db')
e.getmatchrows('functional programming')

# sys.exit()

e.query( 'functional programming')



## profiling

import cProfile

cProfile.runctx('self.some_method()', globals(), locals(), None, 'cumulative')

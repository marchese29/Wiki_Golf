from collections import deque
import re
import requests


class Node(object):
	"""Represents a single node in the Wiki-Graph."""
	def __init__(self, title):
		self.title = title
		self.dist = None
		self.refs = []
		self.previous = None


def run_BFS(start, finish):
	"""Performs a breadth-first search of the Wikipedia page graph to determine the distance between
	the provided page titles.

	This will perform a standard BFS with one hitch.  Instead of running to completion, we will stop
	searching once the destination page is reached.  This prevents us from downloading the entire
	contents of Wikipedia as well as saves time and memory.  The BFS will also be non-traditional in
	the sense that we are discovering the graph while we are searching it.

	The function accepts two parameters:
	str -- start: The title of the page to serve as the source of the BFS.
	str -- finish: The target page to stop the search at.

	"""

	# Generate the starting point
	start_node = Node(start)
	start_node.dist = 0
	queue = deque([start_node])

	# This while loop should never terminate at the starting point, but rather will return from the
	# inside once the finishing node is found.
	while len(queue) > 0:
		node = queue.popleft()
		found = False
		for ref in node.refs:
			if len([node for node in queue if node.title == ref]) == 0:
				new_node = Node(ref)
				new_node.dist = node.dist + 1
				new_node.previous = node
				queue.append(new_node)
			
			if ref == finish:
				found = True
				break

		if found:
			# TODO: Trace the nodes back to the source and return the result.
			pass

	# Holy Crap, we just downloaded the entirety of Wikipedia!
	return []

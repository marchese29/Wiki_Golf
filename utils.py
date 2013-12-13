from collections import deque
import re
import requests


def get_content(title):
	"""Retrieves the content of the wikipedia article associated with the provided title.

	This will perform a standard HTTP GET at the specified title as it would be plugged into the
	wikimedia API.

	The function accepts one parameter:
	str -- title: The title of the page in question.

	Returns: str -- The content of the page given in the arguments.

	"""
	req = requests.get(''.join([
		'http://en.wikipedia.org/w/api.php',
		'?action=query',
		'&prop=revisions',
		'&rvprop=content',
		'&format=xml',
		'&titles=' + title,
		'&redirects'
	]))

	return req.text


def get_links(content):
	"""Retrieves the links from the provided content and returns them as a list of strings.

	This function will parse the content using Python's built-in regex interpreter.  Each string in
	the list is of the form [[CONTENT]] where CONTENT is the title of the linked page in a format
	that matches the wikimedia standard.

	The function accepts one parameter:
	str -- content: The content to be parsed by the regex engine.

	Returns: list<str> -- A list of the links found in the content.

	"""
	pattern = r'\[\[(?!Category:)(?!File:)(?!Image:).*?\]\]'

	return re.findall(pattern, content)


def get_actual_title(title):
	"""Retrieves the final title for the provided title after redirects.

	This is helpful for bypassing multiple calls to the API to find the final endpoint after
	redirects.

	The function accepts one parameter:
	str -- title: The working title of the page in question.

	"""
	content = get_content(title)
	return re.match(r'[^"]*', re.match(r'".*"', re.match(r'title=".*?"', content)))


class Node(object):
	"""Represents a single node in the Wiki-Graph.

	The class has four member variables:
	list<str> -- refs: A list of titles that this node references in the page graph.
	integer -- dist: The distance from the source used in the graph.
	Node -- previous: A reference to the previous node in the BFS tree.
	str -- title: The actual title of this node after performing redirects.

	"""
	def __init__(self, title):
		"""Constructs a single instance of the Node class.

		The function accepts one parameter:
		str -- title: The title of the page that is represented by this node in the page graph.

		"""
		content = get_content(title)
		
		# Retrieve the references
		refs = get_links(content)
		refs_result = []
		for ref in refs:
			matches = re.findall(r'[^\[\|\]]+')
			(refs_result += matches[0]) if len(matches) == 1 else (refs_result += matches[1])
		self.refs = [get_actual_title(ref) for ref in refs_result]
		
		self.dist = None
		self.previous = None

		# Retrieve the literal title from the content
		self.title = re.match(r'[^"]*', re.match(r'".*"', re.match(r'title=".*?"', content)))


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

	Returns: list<str> -- A list of pages in order from the start parameter to the finish parameter.

	"""
	
	# Retrieve the actual finishing title
	actual_finish = get_actual_title(finish)

	# Keep track of the visited node titles
	visited = []

	# Pull the starting node
	start_node = Node(start)
	start_node.dist = 0

	# The queue for synchronizing the search
	queue = deque([start_node])

	# Although this could theoretically download the entirety of wikipedia, it should return from
	# the inside once reaching the ending node.
	while len(queue) > 0:
		node = queue.popleft()
		visited.append(node.title)

		# Note that ref has already been corrected to the potential redirect title.
		for ref in node.refs:
			if not ref in [node.title for node in queue] and not ref in visited:
				ref_node = Node(ref)
				ref_node.dist = node.dist + 1
				ref_node.previous = node

				# We check here if we have encountered the finish node.
				if ref == actual_finish:
					result = [ref]
					current = ref_node
					while current.previous:
						result.append(current.previous.title)
						current = current.previous
					return result.reverse()

	# Holy shit, we just downloaded Wikipedia!
	return []

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
	pass

import json
from urllib.error import HTTPError
from urllib.request import Request, urlopen


##################
# Help functions #
##################
def find_link(links, rel):
    """
    :param links:
    :return:
    """
    for lnk in links:
        # Each link consists of two parts (the URL, and the 'rel' attribute), separated by a semi-colon.
        parts = lnk.split(';')
        if rel in parts[1]:
            next_url = parts[0]
            # Remove the < and > characters that delineate the URL.
            return next_url.strip('<>')


def read_body(response):
    """
    :param response:
    :return:
    """
    body = response.read().decode('utf-8')
    return json.loads(body)


##############
# Main class #
##############
class CanvasAPI:
    def __init__(self, server_address=None, token=None):
        """
        :param server_address: the address to the canvas-lms server.
        e.g "www.canvas-lms.com"
        :param token: and auth token from canvas-lms.
        see https://canvas.instructure.com/doc/api/file.oauth.html for details
        :return: CanvasAPI object
        """
        self.server_address = server_address
        self.token = token

    def api_request(self, url, absolute=False, verbose=False):
        """
        :param url: string, the url for the request.
        e.g "courses" or "https://www.canvas-lms.com/api/v1/courses"
        :param absolute: boolean, notes if the url is absolute or relative.
        e.g "https://www.canvas-lms.com/api/v1/courses" or "courses"
        :param verbose: boolean, prints info to the cli.
        :return: urllib.response object with the response for the request.
        """
        # Gather connection/API information
        if self.server_address is None:
            raise ValueError('Property \'server_address\' must be set prior to calling callAPI.')
        if self.token is None:
            raise ValueError('Property \'token\' must be set prior to calling callAPI.')
        # If URL is absolute, then use it as it was provided.
        if absolute:
            request_url = url
        # Otherwise, augment the URL with the server address
        else:
            request_url = 'http://{}/api/v1/{}'.format(self.server_address, url)
        # Print to standard out only if verbose == True.
        if verbose:
            print('Attempting to retrieve {} ...'.format(request_url))
        # Create the request, adding in the oauth authorization token
        request = Request(url=request_url, headers={'Authorization': ' Bearer {}'.format(self.token)})

        try:
            # Try to make the call and return the urllib.response object.
            return urlopen(request)
        except HTTPError as e:
            # Catch any HTTP Errors as they occur.
            print('HTTP Error: {}, {}'.format(e.code, e.msg))
        return None

    def pages(self, url, absolute=False, verbose=False):
        """
        :param url: string, the url for the request.
        e.g "courses" or "https://www.canvas-lms.com/api/v1/courses"
        :param absolute: boolean, notes if the url is absolute or relative.
        e.g "https://www.canvas-lms.com/api/v1/courses" or "courses"
        :param verbose: boolean, prints info to the cli.
        :return: generator object, generates the pages of the response one by one.
        """
        # Make the initial call to the API to retrieve the first page.
        while True:
            # call the API to retrieve the page.
            response = self.api_request(url, absolute, verbose)
            # Send back the page if it's not None.
            if response:
                yield response
            else:
                break
            # Check if there are more pages of results.
            header = response.getheader('Link')
            # If there is a 'Link' header, then search for a 'next' link.
            if header:
                # All the links are separated by commas.
                url = find_link(header.split(','), 'next')
                # The url from the link will be absolute.
                absolute = True
                if url is None:
                    # If we didn't find a 'next' link, then stop.
                    break
            else:
                # If we didn't find a 'Link' header, stop.
                break

    def all(self, url, absolute=False, verbose=False):
        """
        :param url: string, the url for the request.
        e.g "courses" or "https://www.canvas-lms.com/api/v1/courses"
        :param absolute: boolean, notes if the url is absolute or relative.
        e.g "https://www.canvas-lms.com/api/v1/courses" or "courses"
        :param verbose: boolean, prints info to the cli.
        :return:
        """
        # A list to accumulate all of the results from all of the pages.
        results = []
        # Read all of the pages of results from this API call.
        for pg in self.pages(url, absolute, verbose):
            json_lst = read_body(pg)
            results += json_lst
        return results

#!/usr/bin/python2.4
#
# Copyright 2009 Empeeric LTD. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

VERSION = '0.3'
__version__ = VERSION

import simplejson
import urllib
import httplib2
import socket
import socks
from urllib2 import URLError
import urlparse
import string

BITLY_API_VERSION = "2.0.1"

TIMEOUT = 1 #SECONDS

VERBS_PARAM = { 
         'shorten':'longUrl',               
         'expand':'shortUrl', 
         'info':'shortUrl',
         'stats':'shortUrl',
         'errors':'',
}


class BitlyError(Exception):
  '''Base class for bitly errors'''
  
  @property
  def message(self):
    '''Returns the first argument used to construct this error.'''
    return self.args[0]
    

class BitlyTimeoutError(BitlyError):
    pass
    

class Api(object):

    ALLOWED_API_DOMAINS = {
        'bit.ly': 'http://api.bit.ly/',
        'j.mp': 'http://api.j.mp/',
    }

    domain = 'bit.ly'
    proxy_info = None
    
    def get_api_domain(self):
        return self.ALLOWED_API_DOMAINS[self.domain]
        
    """ API class for bit.ly """
    def __init__(self, login, apikey, domain=None, proxy_info=None):
        self.login = login
        self.apikey = apikey
        self._urllib = httplib2
        if domain is not None:
            self.domain = domain
        if proxy_info:
            self.proxy_info = proxy_info
        
    def shorten(self, longURLs, params={}):
        """ 
            Takes either:
            A long URL string and returns shortened URL string
            Or a list of long URL strings and returns a list of shortened URL strings.
        """
        want_result_list = True
        if not isinstance(longURLs, list):
            longURLs = [longURLs]
            want_result_list = False
            
        request = self._getURL("shorten", longURLs, params)
        result = self._fetchUrl(request)

        json = simplejson.loads(result)
        Api._CheckForError(json)
        
        results = json['results']

        res = [results[url].get('shortUrl', None) for url in longURLs]
        
        if want_result_list:
            return res
        else:
            return res[0]


    def expand(self, shortURL, params={}):
        """ Given a bit.ly url or hash, return long source url """
        request = self._getURL("expand",shortURL,params)
        result = self._fetchUrl(request)
        json = simplejson.loads(result)
        Api._CheckForError(json)
        return json['results'][string.split(shortURL, '/')[-1]]['longUrl']

    def info(self, shortURL, params={}):
        """ 
        Given a bit.ly url or hash, 
        return information about that page, 
        such as the long source url
        """
        request = self._getURL("info",shortURL,params)
        result = self._fetchUrl(request)
        json = simplejson.loads(result)
        Api._CheckForError(json)
        return json['results'][string.split(shortURL, '/')[-1]]

    def stats(self, shortURL, params={}):
        """ Given a bit.ly url or hash, return traffic and referrer data.  """
        request = self._getURL("stats",shortURL,params)
        result = self._fetchUrl(request)
        json = simplejson.loads(result)
        Api._CheckForError(json)
        return Stats.NewFromJsonDict(json['results'])

    def errors(self, params={}):
        """ Get a list of bit.ly API error codes. """
        request = self._getURL("errors","",params)
        result = self._fetchUrl(request)
        json = simplejson.loads(result)
        Api._CheckForError(json)
        return json['results']
        
    def setUrllib(self, urllib):
        '''Override the default urllib implementation.
    
        Args:
          urllib or httplib2
        '''
        self._urllib = urllib
    
    def _getURL(self, verb, paramVal, more_params={}): 
        if not isinstance(paramVal, list):
            paramVal = [paramVal]
        
        params = {
                  'version':BITLY_API_VERSION,
                  'format':'json',
                  'login':self.login,
                  'apiKey':self.apikey,
            }
            
        params.update(more_params)
        params = params.items() 
                
        verbParam = VERBS_PARAM[verb]   
        if verbParam:
            for val in paramVal:
                params.append(( verbParam, val ))
        encoded_params = urllib.urlencode(params)
        return "%s%s?%s" % (self.get_api_domain(), verb, encoded_params)
       
    def _fetchUrl(self, url):
        '''Fetch a URL
            
        Args:
          url: The URL to retrieve
            
        Returns:
          A string containing the body of the response.
        '''
        
        # Open and return the URL 
        try:
            if self._urllib is httplib2:
                params = {
                    'timeout': TIMEOUT
                }
                
                if self.proxy_info is not None:
                    try:
                        host = self.proxy_info['HOST']
                        port = self.proxy_info['PORT']
                    except KeyError, err:
                        raise ValueError('You should supply a value for HOST and PORT when working with proxies. %s' % err)

                    params.update(
                        {'proxy_info': httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP_NO_TUNNEL, host, port)}
                    )
                http = httplib2.Http(**params)
                resp, content = http.request(url)
                url_data = content
            else:
                url_data = self._urllib.urlopen(url=url).read()
                
        except (URLError, socket.error), err:
            # nasty bit of hack, i know but unfortunatly neither urllib2 ou httplib2 has a smart way of telling me 
            # that it was a timeout error
            if hasattr(err, 'reason') and err.reason == 'urlopen error timed out' or unicode(err) == u'timed out':
                raise BitlyTimeoutError('The url %s has timed out' % url)
            raise err
        
        return url_data
        

    @classmethod
    def _CheckForError(cls, data):
        """Raises a BitlyError if bitly returns an error message.
    
        Args:
          data: A python dict created from the bitly json response
        Raises:
          BitlyError wrapping the bitly error message if one exists.
        """
        # bitly errors are relatively unlikely, so it is faster
        # to check first, rather than try and catch the exception
        if 'ERROR' in data or data['statusCode'] == 'ERROR':
            raise BitlyError, data['errorMessage']
        for key in data['results']:            
            if type(data['results']) is dict and type(data['results'][key]) is dict:
                if 'statusCode' in data['results'][key] and data['results'][key]['statusCode'] == 'ERROR':
                    raise BitlyError, data['results'][key]['errorMessage'] 
       
class Stats(object):
    '''A class representing the Statistics returned by the bitly api.
    
    The Stats structure exposes the following properties:
    status.user_clicks # read only
    status.clicks # read only
    '''
    
    def __init__(self,user_clicks=None,total_clicks=None):
        self.user_clicks = user_clicks
        self.total_clicks = total_clicks
    
    @staticmethod
    def NewFromJsonDict(data):
        '''Create a new instance based on a JSON dict.
        
        Args:
          data: A JSON dict, as converted from the JSON in the bitly API
        Returns:
          A bitly.Stats instance
        '''
        return Stats(user_clicks=data.get('userClicks', None),
                      total_clicks=data.get('clicks', None))

        
if __name__ == '__main__':
    testURL1="http://www.yahoo.com"
    testURL2="http://www.cnn.com"
    a=Api(login="pythonbitly",apikey="R_06871db6b7fd31a4242709acaf1b6648")
    short=a.shorten(testURL1)    
    print "Short URL = %s" % short
    short=a.shorten(testURL1,{'history':1})    
    print "Short URL with history = %s" % short
    urlList=[testURL1,testURL2]
    shortList=a.shorten(urlList)
    print "Short URL list = %s" % shortList
    long=a.expand(short)
    print "Expanded URL = %s" % long
    info=a.info(short)
    print "Info: %s" % info
    stats=a.stats(short)
    print "User clicks %s, total clicks: %s" % (stats.user_clicks,stats.total_clicks)
    errors=a.errors()
    print "Errors: %s" % errors
    testURL3=["http://www.google.com"]
    short=a.shorten(testURL3) 
    print "Short url in list = %s" % short

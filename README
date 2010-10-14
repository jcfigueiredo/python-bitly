This library provides a pure python interface for the bit.ly API.

bit.ly (http://bit.ly) allows users to shorten, share, and track links (URLs). Reducing the URL length makes sharing easier. Bitly exposes a web services API (http://code.google.com/p/bitly-api/wiki/ApiDocumentation) and this library is intended to make it even easier for python programmers to use.

Using

The library provides a python wrapper around the bitly API and some of the bitly data model.

Model:

Currently only the part of the statistics data module is wrapped using the bitly.Stats class returned by the API bitly.stats() method.

API:

The API is exposed via the bitly.Api class.

To create an instance of the bitly.Api with login credentials (API calls required the client to be authenticated):

  >>> import bitly
  >>> api = bitly.Api(login='login', apikey='apikey') 

Apikey is available for each registered bit.ly user from the account page. You must obtain your own API key (its free and easy), please do not use the one provided with the code, which is intended for testing purposes only.

To shorten a long URL:

  >>> short=api.shorten("www.google.com")
  >>> print "Short URL = %s" % short
  Short URL = http://bit.ly/nHRnc

To shorten a long URL and save to the user's bit.ly history:

  >>> short=api.shorten("www.google.com",{'history':1})
  >>> print "Short URL with history = %s" % short
  Short URL = http://bit.ly/nHRnc

To expand a short URL:

  >>> long=api.expand(short)
  >>> print "Expanded URL = %s" % long
  Expanded URL = http://www.google.com/

To get statistics about the usage of a short URL:

  >>> stats=api.stats(short)
  >>> print "User clicks %s, total clicks: %s" % (stats.user_clicks,stats.total_clicks)
  User clicks 51, total clicks: 5707

To shorten multiple long URLs:

  >>> testURL1="www.yahoo.com"
  >>> testURL2="www.cnn.com"
  >>> urlList=[testURL1,testURL2]
  >>> shortList=api.shorten(urlList)
  >>> print "Short URL list = %s" % shortList
  Short URL list = [u'http://bit.ly/O8slj', u'http://bit.ly/o8VnH']

License¶

    Copyright 2009 Empeeric LTD. All Rights Reserved. 

    Licensed under the Apache License, Version 2.0 (the 'License'); you may not use this file except in compliance with the License. You may obtain a copy of the License at 

    http://www.apache.org/licenses/LICENSE-2.0 

    Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
#!/usr/bin/env python
#-*- coding:utf-8 -*-

from nose.tools import assert_raises

import bitly

def test_urls_shortening_scenario():

    api = bitly.Api(login='jcfigueiredo', apikey='R_1cf5dc0fa14c2df34261fb620bd256aa')
    yield should_raise_when_an_invalid_credential_is_provided
    yield should_have_an_API_authenticated_by_my_credentials, api
    yield should_shorten_an_url_consistently_when_a_single_string_urls_is_provided, api
    yield should_shorten_many_urls_consistently_when_a_list_of_urls_is_provided, api

def should_raise_when_an_invalid_credential_is_provided():
    api = bitly.Api(login='inexistent_login', apikey='or_invalid_key')
    assert_raises(bitly.BitlyError, api.shorten, 'http://anylong.url') 

def should_have_an_API_authenticated_by_my_credentials(api):
    assert api, 'Should have a valid API'

def should_shorten_an_url_consistently_when_a_single_string_urls_is_provided(api):
    url_to_be_shortened = 'http://globoesporte.globo.com/motor/formula-1/noticia/2010/10/apos-maus-resultados-ferrari-reforca-apoio-massa-no-fim-da-temporada.html'
    expected_url = 'http://bit.ly/9n93fw'

    shortened_url = api.shorten(longURLs=url_to_be_shortened)

    assert shortened_url == expected_url, 'The shortened version of %s url should\'ve been %s but was %s' % (url_to_be_shortened, expected_url, shortened_url)

def should_shorten_many_urls_consistently_when_a_list_of_urls_is_provided(api):
    urls_to_be_shortened = [ 'http://globoesporte.globo.com/motor/formula-1/noticia/2010/10/apos-maus-resultados-ferrari-reforca-apoio-massa-no-fim-da-temporada.html'
    ,
 'http://globoesporte.globo.com/basquete/noticia/2010/10/leandrinho-faz-19-pontos-na-vitoria-do-toronto-sobre-o-philadelphia.html'
    ]

    expected_urls = ['http://bit.ly/9n93fw','http://bit.ly/aprECg']

    shortened_urls = api.shorten(longURLs=urls_to_be_shortened)

    for expected_url in expected_urls:
        assert expected_url in shortened_urls, 'The list os shortened urls should contain %s but it wasn\'t found in %s' % (expected_url, shortened_urls)

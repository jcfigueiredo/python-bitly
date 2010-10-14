#!/usr/bin/env python
#-*- coding:utf-8 -*-

import bitly

def test_urls_shortening_scenario():

    api = bitly.Api(login='jcfigueiredo', apikey='R_1cf5dc0fa14c2df34261fb620bd256aa')

    i_have_an_API_validated_by_my_credentials(api)

def i_have_an_API_validated_by_my_credentials(api):
    assert api, 'Should have a valid API'
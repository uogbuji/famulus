# -*- encoding: utf-8 -*-
'''
Module name: xslt
Defined REST entry points:

http://purl.org/akara/services/demo/tocouch (tocouch)

Notes on security:

None
'''

import amara
#from amara.bindery import html
from amara.thirdparty import json, httplib2
from amara.lib import irihelpers, inputsource

from akara.services import simple_service
from akara import request, response, logger, module_config

TOCOUCH_SERVICE_ID = 'http://purl.org/akara/services/demo/tocouch'

H = httplib2.Http('/tmp/.cache')

COUCHBASE = module_config().get('couchbase', 'http://sforza.ogbuji.net:5984/famulus/')

@simple_service('GET', TOCOUCH_SERVICE_ID, 'tocouch', 'text/html')
def tocouch(**params):
    '''
    @xslt - URL to the XSLT transform to be applied
    all other query parameters are passed ot the XSLT processor as top-level params
    
    Sample request:
    curl --request POST --data-binary "@foo.xml" --header "Content-Type: application/xml" "http://localhost:8880/akara.xslt?@xslt=http://hg.akara.info/amara/trunk/raw-file/tip/demo/data/identity.xslt"
    
    You can check after the fact by visiting http://sforza.ogbuji.net:5984/test1/_all_docs
    
    Then get the id and surf there
    
    http://sforza.ogbuji.net:5984/test1/b10d978ced600227e663d6503b1abec4
    
    or just explore it in Futon
    
    http://sforza.ogbuji.net:5984/_utils/database.html?test1
    '''
    logger.debug('params: ' + repr(params))
    title = params['t'].decode('UTF-8')
    url = params['url'].decode('UTF-8')
    tags = params['tags'].decode('UTF-8').split(u',')
    desc = params.get('d', u'').decode('UTF-8')
    body = json.dumps({'title': title, 'url': url, 'tags': tags, 'desc': desc}, indent=4)
    headers = {}
    resp, content = H.request(COUCHBASE, 'POST', body, headers=headers)
    return '<div>Couch updated?</div><pre>%s</pre>'%body

#{'ld': '2', 'd': 'I gave a number of talks this spring on jQuery and especially on some of the recent additions made in jQuery 1.4.', 'tlt': '2', 'url': 'http://ejohn.org/', 'blt': '1', 'tt': 'totag', 'nd': '1', 'bt': 'via for to unread', 'tl': '6', 'u': 'uche', 'user': 'uche', 'ned': '1', 'bld': '1', 'net': '1', 'bbt': '1', 'dt': 'todescribe', 't': 'John Resig - JavaScript Programmer'}
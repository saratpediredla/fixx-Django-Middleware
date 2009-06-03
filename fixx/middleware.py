import sys
import httplib
import string
import base64
import simplejson as json
from django.conf import settings

class ExceptionLoggerMiddleware(object):
    """Log Django exceptions to fixx. 
    
    NOTE : Only works with fixx 1.8+
       
    This middleware class uses the fixx API to submit a new issue to your fixx instance everytime there is an exception in Django.
    
    In order for this middleware to work correctly, you will need the following parameters to be set in your settings.py.
    
    FIXX_URL : Base URL of your fixx installation without the 'http://' and trailing slash. Ex. example.com:9000 or fixx.mydomain.com:9000
    FIXX_USER : Username of account used to log the issue
    FIXX_PASSWORD : Password of the account used to log the issue
    FIXX_DEFAULT_AREA : The id for default area to log issues to
    
    Finally, you need to add this middleware to your MIDDLEWARE_CLASSES in settings.py
    """
    
    def process_exception(self, request, exception):
        print "logging exceptions"
        bug = {}
        bug["area"] = settings.FIXX_DEFAULT_AREA
        try:
            request_repr = repr(request)
        except:
            request_repr = 'Request repr() unavailable'
        bug["description"] = '%s<br/><br/>%s' % (self._get_traceback(sys.exc_info()), request_repr)
        bug["title"] = 'Django exception %s at http://%s%s ' % (type(exception), request.META['HTTP_HOST'], request.META['PATH_INFO']) 
        auth = 'Basic ' + string.strip(base64.encodestring(settings.FIXX_USER + ':' + settings.FIXX_PASSWORD))
        headers = {"Content-type": "application/json", "Accept": "application/json", "Authorization" : auth}
        h = httplib.HTTPConnection(settings.FIXX_URL)
        try:
            h.request("POST","/api/issues/", json.dumps(bug), headers)
            response = h.getresponse()
        except socket.error, e:
            pass

    def _get_traceback(self, exc_info):
        """Helper function to return the traceback as a string"""
        import traceback
        return '<br/>'.join(traceback.format_exception(*(exc_info or sys.exc_info())))
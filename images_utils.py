import base64
"""
Will base64 encode the content passed as string.
"""
def to_base64( content ):
    base64Content = base64.b64encode(content)
    base64Content = base64Content.decode('utf-8')
    return base64Content

"""
The parameter is expected to be a base64 string.
This method will add in front of it the mime type specific for png.
The result of this method can be embedded in the src attribute of an img tag in html for example.

"""
def base64_add_png_mimetype( base64Str ):
    return "data:image/png;base64," + base64Str

from bs4 import BeautifulSoup
import cairosvg

"""
Using the html page provided, it will look after the element with the css selector.
This needs to be a svg element.
If the svg element represented by cssSelector is found it will return an 'inlined' svg element.
Inside svgs, other svgs can be linked using the <use> tag. This function will find the referenced elements
and will repace the <use> tags with the actual content of the referenced svgs.
"""
def normalizeSvg( cssSelector, page ):
    print('Looking for css selector ' + cssSelector);
    soup = BeautifulSoup(page, 'html.parser')
    svgElement = soup.select(cssSelector)
    if len != 1:
        print("Found the html element represented by the css selector")
        elem = svgElement[0]
        #Check if this has svg tag
        if elem.name == 'svg':
            print("The html element represented by the css selector is a svg tag.")
            return inlineSvg( elem, soup )
        else:
            print("The html element represented by the css selector is not a svg tag")
    else:
        print('Error locating element')

"""
elem - SVG tag that needs to be inlined
soup - the BeautifulSoup object representing the page
Will search through all the children of elem to find use tags and retrieve all their xlink:href attributes.
Using the xlink:href values it will find the symbols defined somewhere else in the page and take their content and append it
to the initial svg tag
"""
def inlineSvg( elem, soup ):
    elements = resolveXLinkElements(elem, soup );
    for i in elements:
        elem.append(i)
    return elem

def resolveXLinkElements( elem, soup ):
    useTags = elem.find_all("use");
    symbolList = []
    symbolListElems = []
    #Gather all the references to symbols using xlink:href tag
    for useTag in useTags:
        if useTag['xlink:href'] not in symbolList:
            symbolList.append( useTag['xlink:href'] )
    for symbol in symbolList:
        #The symbol string already contains the '#' at the beginning
        #so no need to add it in the selector for the id
        symbolElem = soup.select("symbol" + symbol);
        #I expect to find a single symbol by its id
        if len(symbolElem) == 1:
            symbolListElems.append( symbolElem[0] )
            childRefs = resolveXLinkElements( symbolElem[0], soup )
            for childRefsElem in childRefs:
                symbolListElems.append(childRefsElem)
    return symbolListElems;

"""
Converts the content of a svg image into a png.
By content of a SVG image it is understood the SVG tag with its children: "<svg>...</svg>".
"""
def convertSvgToPng( svgStr):
    #output_width, output_height - are needed. Without specifying them a 'Division by Zero' error will happen
    #parent_width parent_height - are used to arrange the content of the svg image in the canvas of the final png image.
        #If they are not used, the content of the svg image might appear decentered (e.g.: Only some parts visible with the rest overflown
        # outside of the image)
    pngContent = cairosvg.svg2png(bytestring=svgStr, output_height=200, output_width=200,
                                    parent_height=200, parent_width=200)
    return pngContent

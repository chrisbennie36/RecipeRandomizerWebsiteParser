from fastapi import APIRouter
import requests
from bs4 import BeautifulSoup
from Domain.Dtos.WebsiteParserDto import WebsiteParserDto
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/webpageParser',
    tags=['webpageParser'],
)

@router.post("/")
async def ParseRecipeFromWebpage(website_parser_dto: WebsiteParserDto):
    webPageData = getWebpageData(website_parser_dto.url)
    if not webPageData or webPageData == '':
        logger.warning('Could not retrieve HTML string from the given URL')
        return
    
    soup = BeautifulSoup(webPageData, 'html.parser')

    title = parseWebpageElements(soup, 'h1')[0]

    logger.warning(f'Title is: {title}')
    if(title == ''):
        logging.warning('Website contains no h1 tags, attempting to parse the body')
        title = parseWebpageElements(soup, 'body')
        return title

    return formatTitle(title)

def formatTitle(title: str):
    #We want to strip out the author's name as this sometimes appears in the title as <Recipe name - author name>
    #But we want to keep legitemate words which make use of a -, so this is why we split on a dash with whitespace, rather than just a dash
    #Words with a dash will never come with a whitespace.
    if(' -' in title):
        title = title.split(' -')[0].strip()

    return title

def parseWebpageElements(soup: BeautifulSoup, element: str):
    parsedData = ''
    result = []
    for parsedData in soup.find_all(str):
        parsedDataString = parsedData.get_text()
        if isValidParsedData(parsedDataString):
            result.append(parsedDataString)

    return result

def isValidParsedData(parsedData: str):
    return '\n' not in parsedData and '{' not in parsedData and parsedData != ''
    
def getWebpageData(url: str):
    data = requests.get(url)
    return data.text
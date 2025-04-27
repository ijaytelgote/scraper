from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
import json
import asyncio
from typing import List, Optional
import html2text
import nest_asyncio
from playwright.async_api import async_playwright


class ExtractSchema(BaseModel):
    """
    A comprehensive data model for car listings that captures all essential details
    about a vehicle — from its brand and pricing to technical specifications and customer reviews.
    """
    job_titile: str = Field(..., description="job title")
    job_description: str=Field(...,description="jod description")


prompt = '''
    Extract useful information from the webpage considering the following fields and their meaning. Fill each field if information is available.
    Consider positive responses only, and ignore negative ones. like One Touch Down - No then dont include it.

    job_description and job_title

    Extract all required information completely and correctly.

    Do not include any incorrect or irrelevant details.

    Follow the exact output format provided for each part.

    No need to add extra information apart from how template is given.

    Your performance will be rewarded with a 7-star rating and a $5K bonus if all information is accurate and formatted correctly.

    '''


USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"


async def fetch_page(url, user_agent=USER_AGENT) -> str:
    # Launch browser and navigate to the URL
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context(user_agent=user_agent)
        page = await context.new_page()
        await page.goto(url)
        content = await page.content()
        await browser.close()

    # Convert HTML to Markdown
    markdown_converter = html2text.HTML2Text()
    markdown_converter.ignore_links = False
    return markdown_converter.handle(content)




async def main(url):
    auto_content = await fetch_page(url)
    from google.ai.generativelanguage_v1beta.types import Tool as GenAITool

    llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0.7,
    max_retries=2,
    groq_api_key=os.environ["GROQ_API_KEY"]



    parser = JsonOutputParser(pydantic_object=ExtractSchema)

    prompt = PromptTemplate(
        template="Answer the user query. Don't skip any logic of retrieval, I will give you 5 star and 500$ as bonus If you retrieve all the data correctly, Don't add false infomation or the information other that how template is.\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | llm | parser

    datas=chain.invoke({"query": auto_content},tools=[GenAITool(google_search={})])

    return datas



def scrap_upwork(link):
    nest_asyncio.apply()
    result1 =asyncio.run(main(link))
    return result1

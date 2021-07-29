from app.db.repositories.wordcount import WordCountRepository
from fastapi import APIRouter, Depends, Response
from loguru import logger
from starlette import status

from app.models.schemas.wordcount import WordCountRequest, WordCountResponse
from app.services.scraper import ScraperService, ScraperException
from app.db.session import async_session


async def get_word_count_repository():
    """Get DB session and initialize WordCountRepository"""
    try:
        session = async_session()
        yield WordCountRepository(session)
    finally:
        await session.close()


router = APIRouter()


@router.post(
    "/wordcount",
    status_code=status.HTTP_200_OK,
    response_model=WordCountResponse,
    tags=["wordcount"],
    summary="Get the word count in a given web page URL",
)
async def get_word_count(
    word_count_request: WordCountRequest,
    response: Response,
    word_count_repo: WordCountRepository = Depends(get_word_count_repository),
) -> WordCountResponse:
    """
    Get the count of how many times a word exists in a given web page URL

    If the word and web page URL was already requested in previous requests, the count returned will be the same

    - **word**: word to count in the web page
    - **url**: URL to the web page
    \f
    :param: word_count_request: HTTP Request body
    :param response: HTTP Response
    :param word_count_repo: repository where CRUD functions are located
    :return: Word count response (status, count)
    """
    word_count_result = await word_count_repo.get_word_count(
        word_count_request.word, word_count_request.url
    )
    api_status = "ok"
    if word_count_result == None:
        logger.info("Running scraper to get word count")
        s = ScraperService(word_count_request.url, word_count_request.word)
        try:
            word_count = s.run_and_get_word_count()
        except ScraperException:
            api_status = "failed to get URL content"
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return WordCountResponse(status=api_status, count=0)
        await word_count_repo.create_word_count(
            word_count_request.word, word_count, word_count_request.url
        )
    else:
        logger.info("Using word count from database")
        word_count = word_count_result.count
    return WordCountResponse(status=api_status, count=word_count)

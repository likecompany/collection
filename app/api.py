from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

from corecrud import Options, Returning, Values, Where
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Body, Depends
from likeinterface.exceptions import DecodeError, LikeAPIError
from likeinterface.methods import GetFile, GetMe, GetUser

from likeinterface.types import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from core.crud import crud
from core.depends import get_session
from core.interface import interface
from logger import logger
from orm import CollectionElementModel, CollectionModel
from requests import AddCollectionRequest, GetCollectionRequest
from responses import CollectionResponse
from schema import ApplicationResponse

router = APIRouter()


async def get_collection_core(
    session: AsyncSession,
    request: GetCollectionRequest,
) -> Tuple[Optional[User], CollectionModel]:
    collection = await crud.collections.select.one(
        Where(CollectionModel.name == request.name),
        Options(selectinload(CollectionModel.collection)),
        session=session,
    )
    if not collection:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="COLLECTION_NOT_EXISTS")

    try:
        user = await interface.request(method=GetUser(user_id=collection.user_id))
    except LikeAPIError:
        logger.info("User was not found! Unable to define collection creator")

        return None, collection

    return user, collection


@router.post(
    path="/getCollection",
    response_model=ApplicationResponse[CollectionResponse],
    status_code=status.HTTP_200_OK,
)
async def get_collection(
    session: AsyncSession = Depends(get_session),
    request: GetCollectionRequest = Body(...),
) -> Dict[str, Any]:
    user, collection = await get_collection_core(session=session, request=request)

    return {
        "ok": True,
        "result": {
            "id": collection.id,
            "name": collection.name,
            "user": user,
            "collection_elements": collection.collection_elements,
        },
    }


async def add_collection_core(
    session: AsyncSession, request: AddCollectionRequest
) -> Tuple[User, CollectionModel]:
    if await crud.collections.select.one(
        Where(CollectionModel.name == request.name),
        session=session,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="COLLECTION_EXISTS",
        )

    try:
        user = await interface.request(
            method=GetMe(access_token=request.access_token)
        )
    except LikeAPIError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ACCESS_DENIED",
        )

    for collection in request.collection:
        try:
            await interface.request(GetFile(file_id=collection.file_id))
        except DecodeError as e:
            logger.exception(e)

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"FILE_NOT_EXITS_{collection.file_id}",
            )

    collection_id = await crud.collections.insert.one(
        Values(
            {
                CollectionModel.user_id: user.id,
                CollectionModel.name: request.name,
            }
        ),
        Returning(CollectionModel.id),
        session=session,
    )

    await crud.collection_files.insert.many(
        Values(
            [
                {
                    CollectionElementModel.collection_id: collection_id,
                    CollectionElementModel.file_id: collection_element.file_id,
                    CollectionElementModel.rank: collection_element.rank,
                    CollectionElementModel.suit: collection_element.suit,
                }
                for collection_element in request.collection_elements
            ]
        ),
        Returning(CollectionElementModel.id),
        session=session,
    )

    return user, await crud.collections.select.one(
        Where(CollectionModel.id == collection_id),
        Options(selectinload(CollectionModel.collection_elements)),
        session=session,
    )


@router.post(
    path="/addCollection",
    response_model=ApplicationResponse[CollectionResponse],
    status_code=status.HTTP_200_OK,
)
async def add_collection(
    session: AsyncSession = Depends(get_session),
    request: AddCollectionRequest = Body(...),
) -> Dict[str, Any]:
    user, collection = await add_collection_core(session=session, request=request)

    return {
        "ok": True,
        "result": {
            "id": collection.id,
            "name": collection.name,
            "user": user,
            "collection_elements": collection.collection_elements,
        },
    }

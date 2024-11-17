from fastapi import (
    APIRouter,
    Query,
    Body,
    Cookie,
    Header,
    status,
    HTTPException,
)
from fastapi.encoders import jsonable_encoder


from pydantic import BaseModel, Field, HttpUrl
from typing import Annotated, Any, Literal, Union

from datetime import datetime, time, timedelta
from uuid import UUID

from api.dependencies import CommonQueryParams

# from app.routers.users import User

router = APIRouter(prefix="", tags=["items"])

fake_db = {}


class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type: str = "car"


class PlaneItem(BaseItem):
    type: str = "plane"
    size: int


# define a sub-model
class Image(BaseModel):
    url: HttpUrl
    name: str


# Item model
class Item(BaseModel):
    name: str = Field(examples=["Foo"])
    timestamp: datetime
    description: str | None = Field(
        default=None,
        title="The description of the item",
        max_length=300,
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    # tax: float | None = None
    tax: float = 10.5
    # set types - unique items
    # tags: set[str] = set()
    tags: list[str] = []
    summary: str | None = Field(default=None, title="Item summary", max_length=300)

    # Nested models
    image: list[Image] | None = None


# class Cookies(BaseModel):
#     session_id: str
#     fatebook_tracker: str | None = None
#     googall_tracker: str | None = None


# class CommonHeaders(BaseModel):
#     # forbid extra headers
#     model_config = {"extra", "forbid"}

#     host: str
#     save_data: bool
#     if_modified_since: str | None = None
#     traceparent: str | None = None
#     x_tag: list[str] = []


# class FilterParams(BaseModel):
#     model_config = {"extra": "forbid"}

#     limit: int = Field(100, gt=0, le=100)
#     offset: int = Field(0, ge=0)
#     order_by: Literal["created_at", "updated_at"] = "created_at"
#     tags: list[str] = []


# @router.post("/")
# async def create_item(item: Item):
#     item_dict = item.model_dump()
#     if item.tax:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@router.post(
    "/items/",
    response_model=Item,
    summary="Create an Item",
    status_code=status.HTTP_201_CREATED,
)
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item


# @router.get("/")
# async def read_items(
# ads_id: Annotated[str | None, Cookie()] = None
# x_token: Annotated[list[str] | None, Header()] = None
# cookies: Annotated[Cookies, Cookie()]
# headers: Annotated[CommonHeaders, Header()]
# ):
# return {"ads_id": ads_id}
# return {"X Tooken", x_token}
# return cookies
# return headers


@router.get("/items/", response_model=list[Item])
async def read_items(commons: CommonQueryParams):
    response = {}
    if commons.q:
        response.update({"q", commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response


# @router.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
# async def read_item(item_id: int):
#     if item_id not in items:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return {"item": items[item_id]}


@router.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    # if item_id == 3:
    #     raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return items[item_id]


@router.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_items(
    item_id: UUID,
    start_datetime: Annotated[datetime, Body()],
    end_datetime: Annotated[datetime, Body()],
    process_after: Annotated[timedelta, Body()],
    repeat_at: Annotated[time | None, Body()] = None,
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }


@router.put("/items/{item_id}", response_model=Item)
def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    # fake_db[item_id] = update_item_encoded
    items[item_id] = update_item_encoded
    return update_item_encoded


# @router.put("/items/{item_id}")
# async def update_item(
#     *,
#     item_id: int,
#     item: Annotated[
#         Item,
#         Body(
#             # embed=True,
#             openapi_examples={
#                 "normal": {
#                     "summary": "A normal example",
#                     "description": "A **normal** item works correctly.",
#                     "value": {
#                         "name": "Foo",
#                         "description": "A very nice Item",
#                         "price": 35.4,
#                         "tax": 3.2,
#                     },
#                 },
#                 "converted": {
#                     "summary": "An example with converted data",
#                     "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
#                     "value": {
#                         "name": "Bar",
#                         "price": "35.4",
#                     },
#                 },
#                 "invalid": {
#                     "summary": "Invalid data is rejected with an error",
#                     "value": {
#                         "name": "Baz",
#                         "price": "thirty five point four",
#                     },
#                 },
#             },
#         ),
#     ],
# ):
#     results = {
#         "item_id": item_id,
#         "item": item,
#     }
#     return results


# Partial update
@router.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.model_dump(exclude_unset=True)
    updated_item = stored_item_model.model_copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item


@router.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},
)
async def read_item_name(item_id: str):
    return items[item_id]


@router.get(
    "/items/{item_id}/public", response_model=Item, response_model_exclude=["tax"]
)
def read_item_public_data(item_id: str):
    return items[item_id]


@router.post("/items/images/multiple")
async def create_multiple_images(images: list[Image]):
    return images


# response with arbitrary dict
@router.get("/keyword-weights/", response_model=dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}

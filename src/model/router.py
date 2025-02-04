from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import (
    APIRouter,
    Header,
)
from fastapi.encoders import jsonable_encoder
from pydantic import (
    BaseModel,
    ConfigDict,
)

from src.exceptions import (
    PermissionDenied,
    PermissionDeniedWithPendingSubscription,
)
from src.model import service
from src.model.models import Model
from src.schemas import OKResponse
from src.user import service as user_service
from src.user.exception import (
    OperationOutOfLimit,
    OperationOutOfLimitWithPending,
)
from src.user.model import OperationType


model_router = APIRouter(prefix='/model')


class GenerateModelRequest(BaseModel):
    model: Model


def datetime_to_gmt_str(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo('UTC'))

    return dt.strftime('%Y-%m-%dT%H:%M:%S%z')


class OperationLimitErrorWithPending(BaseModel):
    model_config = ConfigDict(
        json_encoders={datetime: datetime_to_gmt_str},
        populate_by_name=True,
    )

    def serializable_dict(self, **kwargs):
        """Return a dict which contains only serializable fields."""
        default_dict = self.model_dump()

        return jsonable_encoder(default_dict)

    code: str
    message: str
    generations_limit: int
    next_sub: str
    operation: str


@model_router.post('', response_model=OKResponse)
async def generate_model(req: GenerateModelRequest):
    try:
        await user_service.check_subscription_limits(req.model.user_id, OperationType.CREATE_MODEL)
    except OperationOutOfLimit:
        raise PermissionDenied()

    await service.generate_model(req.model)

    return OKResponse(status=True)


# authorization is a user_id. Put it to the heaader "Authorization: user_id"
@model_router.post('/{model_name}/generate/prompt')
async def generate_image_by_promnt(model_name: str, authorization: str = Header(None)):
    try:
        await user_service.update_subscription_state(
            authorization,
            OperationType.GENERATE_BY_PROMNT,
        )
    except OperationOutOfLimit:
        raise PermissionDenied()
    except OperationOutOfLimitWithPending as e:
        err = OperationLimitErrorWithPending(
            operation=e.operation.value,
            message=e.detail,
            generations_limit=e.current_limit,
            next_sub=datetime_to_gmt_str(e.next_sub),
            code='operation_out_limit_with_pending',
        )
        raise PermissionDeniedWithPendingSubscription(err.model_dump())

    return OKResponse(status=True)


# authorization is a user_id. Put it to the heaader "Authorization: user_id"
@model_router.post('/{model_name}/generate/image')
async def generate_image_by_image(model_name: str, authorization: str = Header(None)):
    try:
        await user_service.update_subscription_state(
            authorization,
            OperationType.GENERATE_BY_IMAGE,
        )
    except OperationOutOfLimit:
        raise PermissionDenied()
    except OperationOutOfLimitWithPending as e:
        err = OperationLimitErrorWithPending(
            operation=e.operation.value,
            message=e.detail,
            generations_limit=e.current_limit,
            next_sub=datetime_to_gmt_str(e.next_sub),
            code='operation_out_limit_with_pending',
        )
        raise PermissionDeniedWithPendingSubscription(err.model_dump())

    return OKResponse(status=True)

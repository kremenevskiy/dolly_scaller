
from fastapi import APIRouter, Header
from pydantic import BaseModel
from src.exceptions import PermissionDenied
from src.model import service
from src.model.models import Model
from src.schemas import OKResponse
from src.user import service as user_service
from src.user.exception import OperationOutOfLimit
from src.user.model import OperationType, User


model_router = APIRouter(prefix="/model")


class GenerateRequest(BaseModel):
    user: User


class GenerateModelRequest(GenerateRequest):
    model: Model


@model_router.post("", response_model=OKResponse)
async def generate_model(req: GenerateModelRequest, authorization: str = Header(None)):
    try:
        await user_service.update_sub_state(req.user, OperationType.CREATE_MODEL)
    except OperationOutOfLimit:
        raise PermissionDenied()

    await service.generate_model(req.model)

    return OKResponse(status=True)


@model_router.post("/{model_name}/generate/promnt")
async def generate_image_by_promnt(model_name: str, user: User, authorization: str = Header(None)):
    try:
        await user_service.update_sub_state(user, OperationType.GENERATE_BY_PROMNT)
    except OperationOutOfLimit:
        raise PermissionDenied()

    return OKResponse(
            status=True
            )


@model_router.post("/{model_name}/generate/image")
async def generate_image_by_image(model_name: str, user: User, authorization: str = Header(None)):
    try:
        await user_service.update_sub_state(user, OperationType.GENERATE_BY_IMAGE)
    except OperationOutOfLimit:
        raise PermissionDenied()

    return OKResponse(
            status=True
            )

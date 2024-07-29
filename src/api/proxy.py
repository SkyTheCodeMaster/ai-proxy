from __future__ import annotations

import tomllib
from typing import TYPE_CHECKING

from yarl import URL
from aiohttp import web
from utils.authenticate import authenticate, Key, get_project_status, Approval
from aiohttp.web import Response

from utils.cors import add_cors_routes

if TYPE_CHECKING:
  from utils.authenticate import User
  from utils.extra_request import Request

with open("config.toml") as f:
  config = tomllib.loads(f.read())

routes = web.RouteTableDef()

@routes.post("/whisper/file/")
async def post_whisper_file(request: Request) -> Response:
  auth = await authenticate(request, cs=request.session)
  if isinstance(auth, Response):
    return auth

  if isinstance(auth, Key):
    # this means its a Key
    user: User = auth.user
  else:
    user: User = auth

  approval = await get_project_status(user, "whisper", cs=request.session)

  if approval != Approval.APPROVED:
    return Response(
      status=401,
      text="Please apply for project at https://auth.skystuff.cc/projects#whisper",
    )
  body = await request.read()

  url = URL(config["proxy"]["whisper"]).with_path("/api/whisper/transcribe/file/")
  async with request.session.post(url, data=body, headers=request.headers, params=request.query) as resp:
    return Response(
      status=resp.status, content_type=resp.content_type, body=resp.read()
    )

@routes.post("/whisper/raw/")
async def post_whisper_raw(request: Request) -> Response:
  auth = await authenticate(request, cs=request.session)
  if isinstance(auth, Response):
    return auth

  if isinstance(auth, Key):
    # this means its a Key
    user: User = auth.user
  else:
    user: User = auth

  approval = await get_project_status(user, "whisper", cs=request.session)

  if approval != Approval.APPROVED:
    return Response(
      status=401,
      text="Please apply for project at https://auth.skystuff.cc/projects#whisper",
    )
  body = await request.read()

  url = URL(config["proxy"]["whisper"]).with_path("/api/whisper/transcribe/raw/")
  async with request.session.post(url, data=body, headers=request.headers, params=request.query) as resp:
    return Response(
      status=resp.status, content_type=resp.content_type, body=resp.read()
    )

@routes.post("/chat/")
async def post_chat(request: Request) -> Response:
  auth = await authenticate(request, cs=request.session)
  if isinstance(auth, Response):
    return auth

  if isinstance(auth, Key):
    # this means its a Key
    user: User = auth.user
  else:
    user: User = auth

  approval = await get_project_status(user, "chat", cs=request.session)

  if approval != Approval.APPROVED:
    return Response(
      status=401,
      text="Please apply for project at https://auth.skystuff.cc/projects#chat",
    )
  body = await request.read()

  url = URL(config["proxy"]["chat"]).with_path("/api/chat/")
  async with request.session.post(url, data=body, headers=request.headers, params=request.query) as resp:
    return Response(
      status=resp.status, content_type=resp.content_type, body=resp.read()
    )

@routes.post("/emotion/")
async def post_emotion(request: Request) -> Response:
  auth = await authenticate(request, cs=request.session)
  if isinstance(auth, Response):
    return auth

  if isinstance(auth, Key):
    # this means its a Key
    user: User = auth.user
  else:
    user: User = auth

  approval = await get_project_status(user, "emotion", cs=request.session)

  if approval != Approval.APPROVED:
    return Response(
      status=401,
      text="Please apply for project at https://auth.skystuff.cc/projects#emotion",
    )
  body = await request.read()

  url = URL(config["proxy"]["emotion"]).with_path("/api/emotion/")
  async with request.session.post(url, data=body, headers=request.headers, params=request.query) as resp:
    return Response(
      status=resp.status, content_type=resp.content_type, body=resp.read()
    )

@routes.post("/diffusion/")
async def post_diffusion(request: Request) -> Response:
  auth = await authenticate(request, cs=request.session)
  if isinstance(auth, Response):
    return auth

  if isinstance(auth, Key):
    # this means its a Key
    user: User = auth.user
  else:
    user: User = auth

  approval = await get_project_status(user, "diffusion", cs=request.session)

  if approval != Approval.APPROVED:
    return Response(
      status=401,
      text="Please apply for project at https://auth.skystuff.cc/projects#diffusion",
    )
  body = await request.read()

  url = URL(config["proxy"]["diffusion"]).with_path("/api/diffusion/")
  async with request.session.post(url, data=body, headers=request.headers, params=request.query) as resp:
    return Response(
      status=resp.status, content_type=resp.content_type, body=resp.read()
    )


async def setup(app: web.Application) -> None:
  for route in routes:
    app.LOG.info(f"  ↳ {route}")
  app.add_routes(routes)
  add_cors_routes(routes, app)
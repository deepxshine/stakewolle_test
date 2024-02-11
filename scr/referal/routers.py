from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from fastapi_cache.decorator import cache

from database import get_async_session
from auth.base_config import current_user
from auth.models import User
from .models import ReferalCode, Member


router = APIRouter(prefix='/referal')


@router.post('/register_referal/{referal_code}')
async def create_member(referal_code, 
                        user: User = Depends(current_user), 
                        session: AsyncSession = Depends(get_async_session)):
    query = select(Member).where(Member.referal == user.id)
    result = await session.execute(query)
    member = result.mappings().first()
    if member:
        raise HTTPException(status_code=400, detail={
                    'status': 'error',
                    'detail': 'You`re alrady registraded'
                })

    query = select(ReferalCode).where(ReferalCode.referal_code == referal_code)
    result = await session.execute(query)
    try:
        referal_code = result.mappings().first()['ReferalCode']
    except TypeError:
        raise HTTPException(status_code=404, detail={
                    'status': 'error',
                    'detail': 'Referal code not found'
                })
    if referal_code.lifetime < datetime.utcnow():
        raise HTTPException(status_code=400, detail={
                'status': 'error',
                'detail': 'Lifetime referal is out'
        })
    if not referal_code.is_active:
        raise HTTPException(status_code=400, detail={
                'status': 'error',
                'detail': 'Referal doesn`t active'
        })
    if referal_code.creator == user.id:
        raise HTTPException(status_code=400, detail={
                'status': 'error',
                'detail': 'You can`t register with your referal code'
        })
    stmn = Member(
        referal=user.id,
        referal_code=referal_code.id,
        )
    
    session.add(stmn)
    await session.commit()
    await session.refresh(stmn)
    return {'status': 'sucseed',
            'detail': {
                'referal': user.id,
                'referal_code': referal_code.id,
            }}


@router.post('/create_referal_code')
async def create_referal_code(lifetime: datetime, 
                              user: User = Depends(current_user),
                              session:
                              AsyncSession = Depends(get_async_session)):
    try:
        if lifetime < datetime.utcnow():
            raise HTTPException(status_code=400, detail={
                    'status': 'error',
                    'detail': 'Lifetime can`t be less than tooday'
            })
    except TypeError:
        raise HTTPException(status_code=400, detail={
                    'status': 'error',
                    'detail': 'Error date format'
            })
    
    query = select(ReferalCode).where(
        ReferalCode.creator == user.id).where(
            ReferalCode.is_active)
    result = await session.execute(query)
    try:
        last_code = result.mappings().first()['ReferalCode']
        last_code.is_active = False
        await session.commit()
    except TypeError:
        pass
    query = select(ReferalCode).order_by(ReferalCode.id.desc())
    result = await session.execute(query)
    try:
        last = result.mappings().first()['ReferalCode'].referal_code
    except TypeError:
        new = '1'
    else:
        new = str(int(last) + 1)

    stmn = ReferalCode(
        creator=user.id,
        referal_code=new,
        is_active=True,
        lifetime=lifetime,
    )
    session.add(stmn)
    await session.commit()
    await session.refresh(stmn)
    return {'status': 'sucseed',
            'detail': {
                'creator': user.id,
                'referal_code': new,
                'is_active': True,
                'lifetime': lifetime,
                }}


@router.get("/referal")
@cache(20)
async def get_referal_code(email,
                           session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.email == email)
    result = await session.execute(query)
    try:
        user_id = result.mappings().first()['User'].id
    except TypeError:
        raise HTTPException(status_code=404, detail={
                    'status': 'error',
                    'detail': 'User is not found'
            })
    query = select(ReferalCode).where(
        ReferalCode.creator == user_id
        ).where(ReferalCode.is_active)
    result = await session.execute(query)
    print(result)
    try:
        referal_code = result.mappings().first()['ReferalCode']
        if not referal_code:
            raise HTTPException(status_code=404, detail={
                    'status': 'error',
                    'detail': 'referal code not found'
            })
        if referal_code.lifetime < datetime.now():
            raise HTTPException(status_code=400, detail={
                    'status': 'error',
                    'detail': 'Lifetime referal is out'
            })
        return referal_code
    except TypeError:
        raise HTTPException(status_code=404, detail={
                    'status': 'error',
                    'detail': 'referal code is not found'
            })


@router.get('/referers')
async def get_referers(pk: int, 
                       session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.id == pk)
    result = await session.execute(query)
    user = result.mappings().first()['User']
    print(user)
    if not user:
        raise HTTPException(status_code=400, detail={
                    'status': 'error',
                    'detail': 'user code is not found'
            })
    query = select(User).join(Member).join(ReferalCode).where(
        ReferalCode.creator == pk
    )
    result = await session.execute(query)
    if result:
        return result.mappings().all()
    raise HTTPException(status_code=404, detail={
                    'status': 'error',
                    'detail': 'referals not found'
            })


@router.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(current_user)]):
    return current_user

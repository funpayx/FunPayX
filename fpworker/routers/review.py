from fpx import Router, CurReview, Dependency
from sqlalchemy.ext.asyncio import AsyncSession

from fpworker.di_list import get_db


router = Router()

@router.on_new_review()
async def handle_new_review(review: CurReview, db: AsyncSession = Dependency(get_db)):
    pass
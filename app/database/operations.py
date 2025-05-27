from sqlalchemy import select, func
from app.database.database import async_session
from app.database.models import Category, Course
from app.config.config import CATEGORIES_PER_PAGE, COURSES_PER_PAGE

async def get_categories(page: int, per_page: int = CATEGORIES_PER_PAGE):
    offset = (page - 1) * per_page
    async with async_session() as session:
        result = await session.execute(
            select(Category).order_by(Category.id).limit(per_page).offset(offset)
        )
        categories = result.scalars().all()
    return categories

async def get_total_categories():
    async with async_session() as session:
        result = await session.execute(
            select(func.count(Category.id))
        )
        total = result.scalar()
    return total

async def get_courses(category_id: int, page: int, per_page: int = COURSES_PER_PAGE):
    offset = (page - 1) * per_page
    async with async_session() as session:
        result = await session.execute(
            select(Course).where(Course.category_id == category_id).order_by(Course.id).limit(per_page).offset(offset)
        )
        courses = result.scalars().all()
    return courses

async def get_total_courses(category_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(func.count(Course.id)).where(Course.category_id == category_id)
        )
        total = result.scalar()
    return total

async def get_course(course_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(Course).where(Course.id == course_id)
        )
        course = result.scalar_one_or_none()
    return course 
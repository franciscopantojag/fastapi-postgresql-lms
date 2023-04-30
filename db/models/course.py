import enum
from sqlalchemy import Enum, Column, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType
from .user import User
from ..setup import Base
from .mixins import BaseMixin


class ContentType(enum.Enum):
    lesson = 1
    quiz = 2
    assignment = 3


class Course(BaseMixin, Base):
    __tablename__ = "courses"

    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_by = relationship(User)
    sections = relationship("Section", back_populates="course", uselist=False)
    student_courses = relationship("StudentCourse", back_populates="course")


class Section(BaseMixin, Base):
    __tablename__ = "sections"

    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    course = relationship("Course", back_populates="sections")
    content_blocks = relationship("ContentBlock", back_populates="section")


class ContentBlock(BaseMixin, Base):
    __tablename__ = "content_blocks"

    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    type = Column(Enum(ContentType))
    url = Column(URLType, nullable=True)
    content = Column(Text, nullable=True)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)

    section = relationship("Section", back_populates="content_blocks")
    completed_content_blocks = relationship(
        "CompletedContentBlock", back_populates="content_block"
    )


class StudentCourse(BaseMixin, Base):
    """
    Students can be assigned to courses.
    """

    __tablename__ = "student_courses"

    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    completed = Column(Boolean, default=False)

    student = relationship(User, back_populates="student_courses")
    course = relationship("Course", back_populates="student_courses")


class CompletedContentBlock(BaseMixin, Base):
    """
    This shows when a student has completed a content block.
    """

    __tablename__ = "completed_content_blocks"

    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content_block_id = Column(
        Integer, ForeignKey("content_blocks.id"), nullable=False
    )
    url = Column(URLType, nullable=True)
    feedback = Column(Text, nullable=True)
    grade = Column(Integer, default=0)

    student = relationship(User, back_populates="student_content_blocks")
    content_block = relationship(
        ContentBlock, back_populates="completed_content_blocks"
    )

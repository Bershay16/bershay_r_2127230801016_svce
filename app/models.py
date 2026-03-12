from datetime import date
from typing import List, Optional

from sqlalchemy import BigInteger, Date, Index, String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class CPE(Base):
    __tablename__ = "cpes"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    cpe_title: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    cpe_22_uri: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    cpe_23_uri: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    reference_links: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text), nullable=True)
    cpe_22_deprecation_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    cpe_23_deprecation_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    __table_args__ = (
        Index("ix_cpes_cpe_title", "cpe_title"),
        Index("ix_cpes_cpe_22_uri", "cpe_22_uri"),
        Index("ix_cpes_cpe_23_uri", "cpe_23_uri"),
        Index("ix_cpes_cpe_22_dep_date", "cpe_22_deprecation_date"),
        Index("ix_cpes_cpe_23_dep_date", "cpe_23_deprecation_date"),
    )

    def __repr__(self) -> str:
        return f"<CPE id={self.id} title={self.cpe_title!r}>"

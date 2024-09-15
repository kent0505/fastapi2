from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column

class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)


class User(Base):
    username: Mapped[str]  = mapped_column(nullable=False, unique=True)
    phone:    Mapped[int]  = mapped_column(nullable=False)
    password: Mapped[str]  = mapped_column(nullable=False)
    role:     Mapped[str]  = mapped_column(nullable=False)

class Customer(Base):
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    phone:    Mapped[int] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

class Category(Base):
    title: Mapped[str] = mapped_column(nullable=False)

class Product(Base):
    title:       Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    price:       Mapped[int] = mapped_column(nullable=False)
    available:   Mapped[int] = mapped_column(nullable=False) # 0 or 1
    image:       Mapped[int] = mapped_column(nullable=False) # image id
    category:    Mapped[int] = mapped_column(nullable=False) # category id

class Order(Base):
    product:  Mapped[int] = mapped_column(nullable=False) # product id
    customer: Mapped[int] = mapped_column(nullable=False) # customer id
    amount:   Mapped[int] = mapped_column(nullable=False)
    date:     Mapped[int] = mapped_column(nullable=False) # timestamp
    address:  Mapped[str] = mapped_column(nullable=False) # lat + X + lon
    status:   Mapped[int] = mapped_column(nullable=False) # 0 cancel 1 in process 2 done

class Pickup(Base):
    product:  Mapped[int] = mapped_column(nullable=False) # product id
    customer: Mapped[int] = mapped_column(nullable=False) # customer id
    amount:   Mapped[int] = mapped_column(nullable=False)
    date:     Mapped[int] = mapped_column(nullable=False) # timestamp
    time:     Mapped[int] = mapped_column(nullable=False) # prepare time in timestamp
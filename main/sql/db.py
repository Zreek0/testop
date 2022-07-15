from sqlalchemy import Column, String, Numeric, Boolean
from . import SESSION, BASE

class opbase(BASE):
    __tablename__ = "opbase"
    website = Column(String, primary_key=True)
    link = Column(String)

    def __init__(self, website, link):
        self.website = website
        self.link = link


opbase.__table__.create(checkfirst=True)


def get(website):
    try:
        return SESSION.query(opbase).get(website)
    except:
        return None
    finally:
        SESSION.close()


def update(website, link):
    adder = SESSION.query(opbase).get(website)
    if adder:
        adder.link = link
    else:
        adder = opbase(
            website,
            link
        )
    SESSION.add(adder)
    SESSION.commit()

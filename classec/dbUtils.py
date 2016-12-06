from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import class_mapper
from json import dumps

Base = declarative_base()
engine = create_engine('mysql://root:root@110.110.110.164/cloud_assessment')

metadata = Base.metadata
Session = sessionmaker(bind = engine)


def serialize(model):
    """Transforms a model into a dictionary which can be dumped to JSON."""
    columns = [c.key for c in class_mapper(model.__class__).columns]
    return dict((c, getattr(model, c)) for c in columns)

def serialize_label(res):
    serialized_labels = [serialize(label) for label in res]
    return dumps(serialized_labels)

def FormattingOutputInDict(ExecResultKeys,ExecResultValues):
    """Transforms passed keys and values into dictionary"""
    finalResult = list()
    for result in ExecResultValues:
        finalResult.append(dict(zip(ExecResultKeys,result)))
    return finalResult





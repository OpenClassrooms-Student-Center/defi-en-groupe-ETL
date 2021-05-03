from .extract import extract
from .load import load, run_web_service
from .transform import transform

def run():
    extracted = extract()
    transformed = transform(extracted)
    load(transformed)
    run_web_service()

__all__ = ["extract", "load", "run_web_service", "transform", "run"]
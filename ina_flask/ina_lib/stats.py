import pandas as pd
from ina_flask.ina_lib import db
from ina_flask.ina_lib.db import DBSession, DbStats, DbStatus
from loguru import logger

db.init_db()


def get_statistics_of_video_link_openings():
    with DBSession() as session:
        query = session.query(DbStats).filter(DbStats.youtube_dl != "").all()

    results = []
    for item in query:
        results.append(db.to_dict(item))

    video_link_openings = (
        pd.DataFrame(results)
        .groupby("youtube_dl")
        .count()
        .sort_values(by="id", ascending=False)["id"]
        .to_dict()
    )

    total_requests = len(results)

    return {
        "total_requests": total_requests,
        "video_link_openings": video_link_openings,
    }

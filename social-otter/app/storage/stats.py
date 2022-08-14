from typing import List
from storage.store import DataStorage
from models.tracking_stats import TrackingStats


class TrackingStatsCRUD(DataStorage):
    def __init__(self, doc_id) -> None:
        super().__init__('daily_stats')
        self.doc_id = doc_id

    def create_doc(self, document):
        return super().create_doc(self.doc_id, document)

    def set_stats_doc(self, stats: TrackingStats) -> None:
        self.doc_ref(doc_id=self.doc_id).set(stats.dict())

    def update_tracking(self, trackings) -> None:
        self.doc_ref(doc_id=self.doc_id).update({
            "trackings": trackings
        })
    
    # def get_doc(self) -> TrackingStats:
    #     obj = self.doc_to_dict(doc_id=self.doc_id)
    #     return User(**obj) if obj else None

from typing import List
from storage.store import DataStorage
from models.user import User
from models.tracking_update import TrackingUpdate


def get_all_users(workflow_name, doc_id=None) -> List[User]:
    storage = DataStorage('users')
    collection = storage.db().collection('users')

    if doc_id:
        x = collection.document(doc_id).get()
        return [User(**{"id": x.id, **x.to_dict()})]

    results = collection.where('workflow_name', '==', workflow_name).stream()
    data: List[User] = []
    for x in results:
        data.append(User(**{"id": x.id, **x.to_dict()}))

    return [x for x in data if len(list(x.trackings.keys())) > 0]


class UserCRUD(DataStorage):
    def __init__(self, doc_id) -> None:
        super().__init__('users')
        self.doc_id = doc_id

    def create_doc(self, document):
        return super().create_doc(self.doc_id, document)

    def set_user_doc(self, user: User) -> None:
        self.doc_ref(doc_id=self.doc_id).set(user.dict())

    def get_doc(self) -> User:
        obj = self.doc_to_dict(doc_id=self.doc_id)
        return User(**obj) if obj else None

    def merge_tracking(self, tracking: TrackingUpdate) -> None:
        self.doc_ref(doc_id=self.doc_id).set({**tracking.dict()}, merge=True)

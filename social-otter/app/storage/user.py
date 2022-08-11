from typing import List
from storage.store import DataStorage
from models.user import User
from utils.termcolors import color


def get_all_users(workflow_name, id=None) -> List[User]:
    storage = DataStorage('users')
    if id:
        query_results = storage.db()\
            .collection('users')\
            .where('id', '==', id)\
            .stream()
    else:
        query_results = storage.db()\
            .collection('users')\
            .where('workflow_name', '==', workflow_name)\
            .stream()

    data = []
    for x in query_results:
        data.append(User(**{"id": x.id, **x.to_dict()}))
    return data


class UserCRUD(DataStorage):
    def __init__(self, doc_id) -> None:
        super().__init__('users')
        self.doc_id = doc_id

    def create_doc(self, document):
        return super().create_doc(self.doc_id, document)

    def set_user_doc(self, user: User) -> None:
        self.doc_ref(doc_id=self.doc_id).set(user.dict())

    def update_tracking(self, trackings) -> None:
        self.doc_ref(doc_id=self.doc_id).update({
            "trackings": trackings
        })
    
    def get_doc(self) -> User:
        obj = self.doc_to_dict(doc_id=self.doc_id)
        return User(**obj) if obj else None

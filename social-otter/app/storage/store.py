import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from config import settings

cred = credentials.Certificate(settings.firbase_creds)
firebase_admin.initialize_app(cred)


class DataStorage:
    def __init__(self, collection_name) -> None:
        self.collection_name = collection_name
        self._doc_ref = None

    def db(self):
        return firestore.client()

    def create_doc(self, doc_id, document):
        _ref = self.db().collection(self.collection_name).document(doc_id)
        _ref.set(document)

    def doc_ref(self, *, doc_id):
        if not self._doc_ref:
            self._doc_ref = self.db()\
                .collection(self.collection_name)\
                .document(doc_id)
        return self._doc_ref

    def doc_to_dict(self, *, doc_id) -> dict:
        return self.doc_ref(doc_id=doc_id).get().to_dict()

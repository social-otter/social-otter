from storage.store import DataStorage
from models.workflow import Workflow


class WorkflowCRUD(DataStorage):
    def __init__(self, doc_id) -> None:
        super().__init__('workflows')
        self.doc_id = str(doc_id)

    def create(self, document: Workflow):
        return super().create_doc(self.doc_id, document.dict())
    
    def set(self, document: Workflow) -> None:
        self.doc_ref(doc_id=self.doc_id).set(document.dict())

    def get(self) -> Workflow:
        return Workflow(**super().doc_to_dict(doc_id=self.doc_id))

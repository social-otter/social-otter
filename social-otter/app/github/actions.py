from pathlib import Path
from pydantic import BaseModel

# Docs
# https://docs.github.com/en/actions/security-guides/automatic-token-authentication
# https://docs.github.com/en/rest/actions/workflows


class GithubWorkflow(BaseModel):
    id: str

    @property
    def name(self) -> str:
        return f"tracking-workflow-{self.id}"

    @property
    def file(self) -> str:
        return f"{self.name}.yml"


def create_workflow(workflow: GithubWorkflow):
    template_path = Path(__file__).parent / 'template.yml'
    with open(template_path, 'r') as f:
        yml = f.read()

    yml = yml.format(**{
        "WORKFLOW_NAME": workflow.name,
        "WORKFLOW_ID": workflow.id
    })

    root = Path(__file__).parent.parent.parent.parent
    workflow_dir = Path(root, '.github', 'workflows', workflow.file)

    with open(workflow_dir, 'w') as f:
        f.write(str(yml))


# create_workflow(
#     GithubWorkflow(id="1")
# )

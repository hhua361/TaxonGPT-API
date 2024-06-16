import os
import openai
from typing import List, Union, Optional


def gptcelltype(input_data: Union[List[str], dict], tissuename: Optional[str] = None,
                model: str = 'text-davinci-003', topgenenumber: int = 10) -> str:
    """
    Annotate cell types by OpenAI GPT models.

    :param input_data: Either a list of genes or a differential gene table (dict with cluster as keys).
    :param tissuename: Optional name of the tissue.
    :param model: The OpenAI model to use.
    :param topgenenumber: Number of top differential genes to consider if input is a differential gene table.
    :return: Cell type annotations or the constructed prompt if API key is not set.
    """
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        print("Note: OpenAI API key not found: returning the prompt itself.")
        return ""

    prompt = "Identify cell types of {} cells using the following markers separately for each row. ".format(
        tissuename or "specified") + \
             "Only provide the cell type name. Do not show numbers before the name. " + \
             "Some can be a mixture of multiple cell types.\n"

    if isinstance(input_data, list):
        # If input is a custom list of genes.
        for gene in input_data:
            prompt += f"{gene}, "
        prompt = prompt[:-2]  # Remove the last comma and space.
    elif isinstance(input_data, dict):
        # If input is a differential gene table.
        for cluster, genes in input_data.items():
            selected_genes = genes[:topgenenumber] if len(genes) > topgenenumber else genes
            prompt += f"{cluster}: {', '.join(selected_genes)}\n"

    try:
        response = openai.Completion.create(
            engine=model,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""


# Example usage:
if __name__ == "__main__":
    input_genes = ['CD4', 'CD3D', 'CD14']  # Example list of genes.
    # For differential gene table, it would be a dict like {'cluster1': ['gene1', 'gene2'], ...}
    tissuename = 'human PBMC'
    annotations = gptcelltype(input_data=input_genes, tissuename=tissuename, model='text-davinci-003', topgenenumber=10)
    print("Cell Type Annotations:\n", annotations)

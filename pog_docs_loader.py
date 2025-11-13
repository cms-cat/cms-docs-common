"""
POG Documentation Links Loader

This module provides backward compatibility for loading POG documentation
from YAML into the original dataclass structure.

Usage:
    from pog_docs_loader import load_pog_docs, POG_DOCS

    # Use the loaded POG_DOCS dict (same structure as before)
    docs = POG_DOCS["BTV"]
    print(docs.fallback)  # https://btv-wiki.docs.cern.ch/
    print(docs.era.get("Run3-22CDSep23-Summer22-NanoAODv12"))
"""

from dataclasses import dataclass, field
from typing import Dict, Optional
from pathlib import Path
import yaml


@dataclass
class Docs:
    """Documentation links for a POG"""
    fallback: str  # lowest level doc - must always be defined
    Run2: Optional[str] = None  # Run2 specific documentation
    Run3: Optional[str] = None  # Run3 specific documentation
    era: Dict[str, str] = field(default_factory=dict)  # era specific documentation


def load_pog_docs(yaml_path: Optional[str] = None) -> Dict[str, Docs]:
    """
    Load POG documentation from YAML file into dataclass structure.

    Args:
        yaml_path: Path to pog-docs.yml file. If None, looks in same directory as this file.

    Returns:
        Dictionary mapping POG names to Docs objects
    """
    if yaml_path is None:
        yaml_path = Path(__file__).parent / "pog-docs.yml"
    else:
        yaml_path = Path(yaml_path)

    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)

    pog_docs = {}
    for pog_name, pog_data in data['pog_docs'].items():
        # Extract fields from YAML
        fallback = pog_data.get('fallback')
        if not fallback:
            raise ValueError(f"POG {pog_name} must have a 'fallback' URL")

        docs = Docs(
            fallback=fallback,
            Run2=pog_data.get('Run2'),
            Run3=pog_data.get('Run3'),
            era=pog_data.get('era', {})
        )
        pog_docs[pog_name] = docs

    return pog_docs


# Load POG_DOCS on module import for backward compatibility
POG_DOCS = load_pog_docs()


if __name__ == "__main__":
    # Example usage
    print("Loaded POG documentation:")
    for pog, docs in POG_DOCS.items():
        print(f"\n{pog}:")
        print(f"  Fallback: {docs.fallback}")
        if docs.Run2:
            print(f"  Run2: {docs.Run2}")
        if docs.Run3:
            print(f"  Run3: {docs.Run3}")
        if docs.era:
            print(f"  Eras: {len(docs.era)} specific era links")

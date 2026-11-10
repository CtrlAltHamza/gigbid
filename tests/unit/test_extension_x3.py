"""Unit tests for Signature Extension X3: Portfolio Builder."""

import os
import pytest
from extensions.portfolio_builder.extractor import RepoExtractor
from extensions.portfolio_builder.verifier import CodeASTVerifier
from extensions.portfolio_builder.generator import CaseStudyGenerator
from extensions.portfolio_builder.publisher import CaseStudyPublisher

def test_repo_extractor(tmp_path):
    repo_dir = tmp_path / "dummy_repo"
    repo_dir.mkdir()
    (repo_dir / "README.md").write_text("# Dummy Project\nTest project description.", encoding="utf-8")
    (repo_dir / "main.py").write_text("class CoreEngine:\n    def execute(self):\n        pass\n", encoding="utf-8")

    extractor = RepoExtractor(str(repo_dir))
    meta = extractor.extract_metadata()

    assert meta["repo_name"] == "dummy_repo"
    assert "Dummy Project" in meta["readme"]
    assert "main.py" in meta["source_files"]
    assert meta["total_files"] >= 2

def test_ast_symbol_verifier(tmp_path):
    repo_dir = tmp_path / "code_repo"
    repo_dir.mkdir()
    (repo_dir / "service.py").write_text(
        "class SemanticSearchService:\n"
        "    async def query_dense(self, q: str):\n"
        "        return []\n"
        "def compute_score():\n"
        "    return 1.0\n",
        encoding="utf-8"
    )

    verifier = CodeASTVerifier(str(repo_dir))
    symbols = verifier.extract_symbols_from_file("service.py")

    assert "SemanticSearchService" in symbols
    assert "query_dense" in symbols
    assert "compute_score" in symbols

    # Verify candidate symbols
    verified = verifier.verify_symbols_exist(
        ["SemanticSearchService", "query_dense", "HallucinatedClass"],
        ["service.py"]
    )
    assert verified["SemanticSearchService"] is True
    assert verified["query_dense"] is True
    assert verified["HallucinatedClass"] is False

def test_case_study_generation_and_publishing(tmp_path):
    repo_dir = tmp_path / "rag_repo"
    repo_dir.mkdir()
    (repo_dir / "retriever.py").write_text("class HybridRetriever:\n    pass\n", encoding="utf-8")

    extractor = RepoExtractor(str(repo_dir))
    meta = extractor.extract_metadata()

    verifier = CodeASTVerifier(str(repo_dir))
    generator = CaseStudyGenerator(verifier)

    study = generator.generate(
        meta,
        candidate_symbols=["HybridRetriever", "NonExistentModel"],
        domain_tag="ai_engineering"
    )

    assert study["id"].startswith("CS-EXT-")
    assert "HybridRetriever" in study["verified_symbols"]
    assert "NonExistentModel" not in study["verified_symbols"]
    assert study["verification_rate"] == 0.5
    assert "# High-Throughput Production Architecture" in study["markdown"]

    publisher = CaseStudyPublisher(base_data_dir=str(tmp_path / "personas"))
    saved_file = publisher.publish_to_persona("ai_engineer", study)
    assert os.path.exists(saved_file)
    with open(saved_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert "Case Study ID" in content


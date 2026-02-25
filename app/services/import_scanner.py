import os
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from app.models.team import Team
from app.models.model import Model
from app.models.model_version import ModelVersion, Framework, Stage
from app.schemas.team import TeamCreate
from app.schemas.model import ModelCreate
from app.schemas.model_version import ModelVersionCreate
from app.crud import team as team_crud
from app.crud import model as model_crud
from app.crud import model_version as version_crud


def parse_team_name(path_part: str) -> str:
    return path_part


def parse_model_name(path_part: str) -> str:
    match = re.match(r"(.+?)(?:_v\d+|_version|$)", path_part)
    if match:
        return match.group(1)
    return path_part


def parse_version(path_part: str) -> str:
    version_patterns = [
        r"v(\d+)",
        r"version[_-]?(\d+)",
        r"_(\d+)$",
    ]

    for pattern in version_patterns:
        match = re.search(pattern, path_part, re.IGNORECASE)
        if match:
            return match.group(1)

    return "imported"


def detect_framework(path: Path) -> Framework:
    framework_indicators = {
        Framework.PYTORCH: ["pytorch", "torch", ".pt", ".pth", "model.bin"],
        Framework.TENSORFLOW: ["tensorflow", "tf", ".pb", "saved_model", ".h5", ".keras"],
        Framework.SKLEARN: ["sklearn", "scikit", ".pkl", ".joblib"],
        Framework.XGBOOST: ["xgboost", "xgb", ".xgb"],
        Framework.LIGHTGBM: ["lightgbm", "lgbm", ".lgbm"],
        Framework.CATBOOST: ["catboost", ".cbm"],
    }

    path_str = str(path).lower()

    for file in path.rglob("*"):
        file_str = str(file).lower()
        for framework, indicators in framework_indicators.items():
            if any(ind in file_str for ind in indicators):
                return framework

    for framework, indicators in framework_indicators.items():
        if any(ind in path_str for ind in indicators):
            return framework

    return Framework.OTHER


async def scan_directory(base_path: str) -> Dict[str, any]:
    results = {
        "scanned": 0,
        "imported": 0,
        "skipped": 0,
        "errors": [],
    }

    base = Path(base_path)
    if not base.exists():
        results["errors"].append(f"Base path does not exist: {base_path}")
        return results

    for team_dir in base.iterdir():
        if not team_dir.is_dir():
            continue

        team_name = parse_team_name(team_dir.name)

        team = await team_crud.get_team_by_name(team_name)
        if not team:
            team = await team_crud.create_team(
                TeamCreate(name=team_name, description=f"Auto-imported from {team_dir.name}")
            )

        for model_dir in team_dir.iterdir():
            if not model_dir.is_dir():
                continue

            results["scanned"] += 1

            model_name = parse_model_name(model_dir.name)
            version_str = parse_version(model_dir.name)

            if not any(model_dir.iterdir()):
                results["skipped"] += 1
                continue

            model = await model_crud.get_model_by_name(team.id, model_name)
            if not model:
                model = await model_crud.create_model(
                    team.id,
                    ModelCreate(name=model_name, description=f"Auto-imported from {model_dir.name}")
                )

            existing_version = await version_crud.get_model_version_by_version(model.id, version_str)
            if existing_version:
                results["skipped"] += 1
                continue

            framework = detect_framework(model_dir)

            try:
                await version_crud.create_model_version(
                    model.id,
                    ModelVersionCreate(
                        version=version_str,
                        artifact_path=str(model_dir.absolute()),
                        framework=framework,
                        stage=Stage.DEVELOPMENT,
                        created_by="import_scanner",
                    )
                )
                results["imported"] += 1
            except Exception as e:
                results["errors"].append(f"Error importing {model_dir}: {str(e)}")

    return results

"""
Module de chargement et d'inspection des sessions d'enregistrement Pupil Labs Neon.
"""
import os
import json
from pathlib import Path
from typing import Dict, Any, Optional


class NeonSession:
    """Représente une session d'enregistrement issue du dispositif Pupil Labs Neon."""

    def __init__(self, session_path: str):
        self.session_path = Path(session_path)
        if not self.session_path.exists():
            raise FileNotFoundError(f"Dossier de session introuvable : {session_path}")
        
        self.info = self._load_json("info.json")
        self.wearer = self._load_json("wearer.json")

    def _load_json(self, filename: str) -> Dict[str, Any]:
        file_path = self.session_path / filename
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    @property
    def session_name(self) -> str:
        return self.session_path.name

    @property
    def wearer_name(self) -> str:
        return self.wearer.get("name", "Inconnu")

    @property
    def sampling_rate(self) -> Optional[int]:
        return self.info.get("gaze_frequency")

    @property
    def duration_seconds(self) -> Optional[float]:
        duration_ns = self.info.get("duration")
        if duration_ns is not None:
            return duration_ns / 1e9
        return None

    def list_available_streams(self) -> Dict[str, bool]:
        """Vérifie la présence des principaux flux oculaires et capteurs."""
        expected_streams = {
            "gaze": "gaze ps1.raw",
            "fixations": "fixations ps1.raw",
            "blinks": "blinks ps1.raw",
            "imu": "imu ps1.raw",
            "scene_video": "Neon Scene Camera v1 ps1.mp4",
            "sensor_video": "Neon Sensor Module v1 ps1.mp4",
            "calibration": "calibration.bin"
        }
        return {name: (self.session_path / fname).exists() for name, fname in expected_streams.items()}

    def summary(self) -> str:
        streams = self.list_available_streams()
        available = [k for k, v in streams.items() if v]
        dur = f"{self.duration_seconds:.2f} s" if self.duration_seconds else "N/A"
        freq = f"{self.sampling_rate} Hz" if self.sampling_rate else "N/A"
        
        return (
            f"=== Session Neon : {self.session_name} ===\n"
            f"- Porteur (Wearer) : {self.wearer_name}\n"
            f"- Fréquence : {freq}\n"
            f"- Durée : {dur}\n"
            f"- Flux disponibles : {', '.join(available)}"
        )


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        path = sys.argv[1]
        session = NeonSession(path)
        print(session.summary())
    else:
        print("Usage: python src/loader.py <chemin_vers_dossier_session>")

import subprocess
import sys
from pathlib import Path
import argparse
import logging

def setup_logger(verbose=False):
    """Konfiguruje logger na podstawie poziomu verbose."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Najniższy poziom - przechwytuje wszystko
    
    # Handler konsolowy
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG if verbose else logging.INFO)
    
    # Format logów
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    ch.setFormatter(formatter)
    
    logger.addHandler(ch)
    return logger

def is_git_repo(path=".", logger=None):
    """Sprawdza, czy podana ścieżka to repozytorium Git."""
    try:
        subprocess.run(
            ["git", "-C", path, "rev-parse", "--is-inside-work-tree"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if logger:
            logger.debug(f"Ścieżka {path} jest repozytorium Git")
        return True
    except subprocess.CalledProcessError:
        if logger:
            logger.debug(f"Ścieżka {path} nie jest repozytorium Git")
        return False
    
def actual_git_branch(logger=None):
    """Zwraca aktualną gałąź Git."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        branch = result.stdout.decode('utf-8').strip()
        if logger:
            logger.debug(f"Pobrano aktualną gałąź: {branch}")
        return branch
    except subprocess.CalledProcessError as e:
        error_msg = f"Błąd podczas pobierania aktualnej gałęzi: {e.stderr.decode('utf-8').strip()}"
        if logger:
            logger.error(error_msg)
        else:
            print(f"❌ {error_msg}")
        sys.exit(1)

def direct_branch_parent(logger=None):
    """Zwraca rodzica aktualnej gałęzi Git."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD^"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        parent = result.stdout.decode('utf-8').strip()
        if logger:
            logger.debug(f"Pobrano rodzica gałęzi: {parent}")
        return parent
    except subprocess.CalledProcessError as e:
        error_msg = f"Błąd podczas pobierania rodzica gałęzi: {e.stderr.decode('utf-8').strip()}"
        if logger:
            logger.error(error_msg)
        else:
            print(f"❌ {error_msg}")
        sys.exit(1)

def main():
    """Główna funkcja skryptu."""
    parser = argparse.ArgumentParser(description='Skrypt do sprawdzania repozytorium Git.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Tryb verbose - pokazuje więcej informacji')
    parser.add_argument('-m', '--message', type=str, help='Wiadomość do wyświetlenia')
    
    args = parser.parse_args()
    
    logger = setup_logger(args.verbose)
    current_dir = Path(".").resolve()
    
    logger.debug(f"Sprawdzanie katalogu: {current_dir}")
    
    if is_git_repo(logger=logger):
        logger.info(f"Katalog '{current_dir}' JEST repozytorium Git.")
    else:
        logger.error(f"Katalog '{current_dir}' NIE jest repozytorium Git.")
        sys.exit(1)
    
    actual_branch = actual_git_branch(logger=logger)
    
    logger.info(f"Aktualny katalog: {current_dir}")
    logger.info(f"Aktualna gałąź: {actual_branch}")
    
    if args.message:
        logger.info(f"Wiadomość: {args.message}")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3

from __future__ import annotations

import argparse
import logging
import subprocess
import sys
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import messagebox

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

import os

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

load_dotenv()

LOGIN_URL = "https://redmine.snappler.com/login"
SCRIPT_PATH = Path(__file__).resolve()
WAIT_TIMEOUT = 15
WINDOW_WIDTH = 500
TASK_HEIGHT = 75
BASE_HEIGHT = 80


@dataclass
class Task:
    name: str
    url: str


@dataclass
class TimeEntry:
    task: Task
    hours: float
    comment: str


@dataclass
class Config:
    user: str
    password: str
    cron_hour: int
    tasks: list[Task]

    @classmethod
    def from_env(cls) -> Config:
        user = os.getenv("REDMINE_USER", "")
        password = os.getenv("REDMINE_PASSWORD", "")
        cron_hour = int(os.getenv("CRON_HOUR", "15"))
        tasks = cls._load_tasks()
        return cls(user=user, password=password, cron_hour=cron_hour, tasks=tasks)

    @staticmethod
    def _load_tasks() -> list[Task]:
        tasks: list[Task] = []
        index = 1
        while True:
            name = os.getenv(f"TASK_{index}_NAME")
            url = os.getenv(f"TASK_{index}_URL")
            if not name or not url:
                break
            tasks.append(Task(name=name, url=url))
            index += 1
        return tasks

    def validate(self) -> list[str]:
        errors: list[str] = []
        if not self.user:
            errors.append("Falta REDMINE_USER en .env")
        if not self.password:
            errors.append("Falta REDMINE_PASSWORD en .env")
        if not self.tasks:
            errors.append("No hay tareas configuradas (TASK_1_NAME, TASK_1_URL, etc.)")
        if not 0 <= self.cron_hour <= 23:
            errors.append(f"CRON_HOUR debe ser entre 0 y 23 (actual: {self.cron_hour})")
        return errors


class MessageDialog:
    @staticmethod
    def show(title: str, message: str, *, is_error: bool = False) -> None:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        if is_error:
            messagebox.showerror(title, message, parent=root)
        else:
            messagebox.showinfo(title, message, parent=root)
        root.destroy()

    @staticmethod
    def error(message: str) -> None:
        MessageDialog.show("Error", message, is_error=True)

    @staticmethod
    def success(message: str) -> None:
        MessageDialog.show("Éxito", message)

    @staticmethod
    def info(message: str) -> None:
        MessageDialog.show("Info", message)


class HoursInputDialog:
    def __init__(self, tasks: list[Task]) -> None:
        self.tasks = tasks
        self.result: list[TimeEntry] | None = None
        self._task_entries: dict[str, dict[str, tk.Entry]] = {}

    def show(self) -> list[TimeEntry] | None:
        self._create_window()
        return self.result

    def _create_window(self) -> None:
        self.root = tk.Tk()
        self.root.title("Registro de Horas - Redmine")
        self.root.attributes("-topmost", True)
        self.root.resizable(False, False)
        self._center_window()
        self._create_widgets()
        self._bind_events()
        self.root.mainloop()

    def _center_window(self) -> None:
        self.root.update_idletasks()
        height = BASE_HEIGHT + (len(self.tasks) * TASK_HEIGHT)
        x = (self.root.winfo_screenwidth() // 2) - (WINDOW_WIDTH // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{WINDOW_WIDTH}x{height}+{x}+{y}")

    def _create_widgets(self) -> None:
        main_frame = tk.Frame(self.root, padx=20, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        for index, task in enumerate(self.tasks):
            self._create_task_frame(main_frame, task, focus_first=(index == 0))
        self._create_buttons(main_frame)

    def _create_task_frame(self, parent: tk.Frame, task: Task, *, focus_first: bool) -> None:
        task_frame = tk.LabelFrame(parent, text=task.name, padx=10, pady=5)
        task_frame.pack(fill=tk.X, pady=(0, 10))
        row_frame = tk.Frame(task_frame)
        row_frame.pack(fill=tk.X)

        tk.Label(row_frame, text="Horas:").pack(side=tk.LEFT)
        hour_entry = tk.Entry(row_frame, width=6, font=("Arial", 10), justify="center")
        hour_entry.insert(0, "0")
        hour_entry.pack(side=tk.LEFT, padx=(5, 15))

        tk.Label(row_frame, text="Comentario:").pack(side=tk.LEFT)
        comment_entry = tk.Entry(row_frame, width=30, font=("Arial", 10))
        comment_entry.pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)

        self._task_entries[task.name] = {"hours": hour_entry, "comment": comment_entry}
        if focus_first:
            hour_entry.focus_set()

    def _create_buttons(self, parent: tk.Frame) -> None:
        btn_frame = tk.Frame(parent)
        btn_frame.pack(fill=tk.X, pady=(5, 0))
        tk.Button(btn_frame, text="Cancelar", command=self._on_cancel, width=12).pack(side=tk.RIGHT)
        tk.Button(
            btn_frame, text="Registrar", command=self._on_submit, width=12, bg="#4CAF50", fg="white"
        ).pack(side=tk.RIGHT, padx=(0, 10))

    def _bind_events(self) -> None:
        self.root.bind("<Escape>", lambda _: self._on_cancel())

    def _on_submit(self) -> None:
        entries = self._collect_entries()
        if entries is None:
            return
        if not entries:
            messagebox.showwarning("Atención", "Debes asignar horas a al menos una tarea.", parent=self.root)
            return
        self.result = entries
        self.root.destroy()

    def _on_cancel(self) -> None:
        self.root.destroy()

    def _collect_entries(self) -> list[TimeEntry] | None:
        entries: list[TimeEntry] = []
        for task in self.tasks:
            widgets = self._task_entries[task.name]
            try:
                hours = float(widgets["hours"].get() or 0)
            except ValueError:
                messagebox.showwarning("Atención", f"Valor de horas inválido en {task.name}", parent=self.root)
                return None
            comment = widgets["comment"].get().strip()
            if hours > 0:
                entries.append(TimeEntry(task=task, hours=hours, comment=comment))
        return entries


class RedmineAutomation:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.driver: webdriver.Chrome | None = None

    def run(self, entries: list[TimeEntry]) -> None:
        try:
            self._init_driver()
            self._login()
            registered = self._register_entries(entries)
            self._show_summary(registered)
        finally:
            self._quit_driver()

    def _init_driver(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        if os.getenv("HEADLESS", "false").lower() == "true":
            options.add_argument("--headless")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)

    def _quit_driver(self) -> None:
        if self.driver:
            self.driver.quit()
            self.driver = None

    def _wait(self) -> WebDriverWait:
        if not self.driver:
            raise RuntimeError("Driver no inicializado")
        return WebDriverWait(self.driver, WAIT_TIMEOUT)

    def _login(self) -> None:
        if not self.driver:
            raise RuntimeError("Driver no inicializado")
        self.driver.get(LOGIN_URL)
        wait = self._wait()
        username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_field.send_keys(self.config.user)
        password_field = self.driver.find_element(By.ID, "password")
        password_field.send_keys(self.config.password)
        login_button = self.driver.find_element(By.NAME, "login")
        login_button.click()
        wait.until(EC.url_changes(LOGIN_URL))

    def _register_entries(self, entries: list[TimeEntry]) -> list[TimeEntry]:
        registered: list[TimeEntry] = []
        for entry in entries:
            self._register_single_entry(entry)
            registered.append(entry)
        return registered

    def _register_single_entry(self, entry: TimeEntry) -> None:
        if not self.driver:
            raise RuntimeError("Driver no inicializado")
        self.driver.get(entry.task.url)
        wait = self._wait()
        hours_field = wait.until(EC.presence_of_element_located((By.ID, "time_entry_hours")))
        hours_field.clear()
        hours_field.send_keys(str(entry.hours))
        comments_field = self.driver.find_element(By.ID, "time_entry_comments")
        comments_field.clear()
        comments_field.send_keys(entry.comment)
        submit_button = self.driver.find_element(By.NAME, "commit")
        submit_button.click()
        wait.until(EC.url_changes(entry.task.url))

    def _show_summary(self, entries: list[TimeEntry]) -> None:
        lines = [f"  - {e.task.name}: {e.hours}hs" for e in entries]
        summary = "\n".join(lines)
        total = sum(e.hours for e in entries)
        MessageDialog.success(f"Se registraron {total}hs correctamente:\n\n{summary}")


class CronManager:
    def __init__(self, hour: int) -> None:
        self.hour = hour

    def install(self) -> None:
        if not 0 <= self.hour <= 23:
            logger.error("CRON_HOUR debe ser un número entre 0 y 23 (actual: %s)", self.hour)
            sys.exit(1)
        cron_line = f"0 {self.hour} * * 1-5 DISPLAY=:0 /usr/bin/python3 {SCRIPT_PATH}"
        current_cron = self._get_current_cron()
        lines = self._filter_script_lines(current_cron)
        lines.append(cron_line)
        self._set_cron("\n".join(lines) + "\n")
        logger.info("Cron instalado correctamente.")
        logger.info("El script se ejecutará a las %s:00 de lunes a viernes.", self.hour)
        logger.info("")
        logger.info("Para verificar: crontab -l")
        logger.info("Para cambiar la hora: edita CRON_HOUR en .env y ejecuta --install de nuevo")

    def uninstall(self) -> None:
        current_cron = self._get_current_cron()
        if not current_cron:
            logger.info("No hay crontab configurado.")
            return
        lines = self._filter_script_lines(current_cron)
        if lines:
            self._set_cron("\n".join(lines) + "\n")
        else:
            subprocess.run(["crontab", "-r"], capture_output=True, check=False)
        logger.info("Cron desinstalado correctamente.")

    def _get_current_cron(self) -> str:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=False)
        return result.stdout if result.returncode == 0 else ""

    def _filter_script_lines(self, cron_content: str) -> list[str]:
        return [line for line in cron_content.strip().split("\n") if line and str(SCRIPT_PATH) not in line]

    def _set_cron(self, content: str) -> None:
        process = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE, text=True)
        process.communicate(input=content)
        if process.returncode != 0:
            logger.error("Error al modificar el cron.")
            sys.exit(1)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Automatización para registrar horas en Redmine")
    parser.add_argument("--install", action="store_true", help="Instala el cron job")
    parser.add_argument("--uninstall", action="store_true", help="Desinstala el cron job")
    return parser


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()
    config = Config.from_env()

    if args.install:
        CronManager(config.cron_hour).install()
        return

    if args.uninstall:
        CronManager(config.cron_hour).uninstall()
        return

    errors = config.validate()
    if errors:
        MessageDialog.error("\n".join(errors))
        sys.exit(1)

    dialog = HoursInputDialog(config.tasks)
    entries = dialog.show()

    if not entries:
        MessageDialog.info("Operación cancelada.")
        sys.exit(0)

    try:
        automation = RedmineAutomation(config)
        automation.run(entries)
    except Exception as e:
        MessageDialog.error(f"Error durante la automatización:\n\n{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

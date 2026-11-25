import argparse
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich import print as rprint

from .models import Task, Priority
from .storage import TaskStorage

console = Console()
storage = TaskStorage()


def cmd_add(args):
    task = Task(
        id=storage.next_id(),
        title=args.title,
        description=args.description or "",
        priority=Priority[args.priority.upper()],
        due_date=datetime.fromisoformat(args.due) if args.due else None,
    )
    storage.add(task)
    rprint(f"[green]✓[/green] Задача добавлена: [bold]{task.title}[/bold] (id={task.id})")


def cmd_list(args):
    tasks = storage.get_all()
    if args.pending:
        tasks = [t for t in tasks if not t.completed]
    if args.priority:
        prio = Priority[args.priority.upper()]
        tasks = [t for t in tasks if t.priority == prio]

    if not tasks:
        rprint("[yellow]Задач нет[/yellow]")
        return

    table = Table(title="Задачи")
    table.add_column("ID", style="cyan")
    table.add_column("Название")
    table.add_column("Приоритет")
    table.add_column("Статус")
    table.add_column("Срок")

    for t in sorted(tasks, key=lambda x: (x.completed, -x.priority.value, x.id)):
        status = "[green]✓[/green]" if t.completed else "[ ]"
        prio_color = {Priority.HIGH: "red", Priority.MEDIUM: "yellow", Priority.LOW: "green"}[t.priority]
        due = t.due_date.strftime("%Y-%m-%d") if t.due_date else "-"
        table.add_row(
            str(t.id),
            t.title,
            f"[{prio_color}]{t.priority.name}[/{prio_color}]",
            status,
            due,
        )

    console.print(table)


def cmd_done(args):
    task = storage.get_by_id(args.id)
    if not task:
        rprint(f"[red]Задача #{args.id} не найдена[/red]")
        return
    task.completed = True
    storage.save()
    rprint(f"[green]✓[/green] Задача #{args.id} отмечена как выполненная")


def cmd_delete(args):
    if storage.delete(args.id):
        rprint(f"[green]Задача #{args.id} удалена[/green]")
    else:
        rprint(f"[red]Задача #{args.id} не найдена[/red]")


def main():
    parser = argparse.ArgumentParser(description="CLI Task Manager")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Добавить задачу")
    p_add.add_argument("title")
    p_add.add_argument("-d", "--description")
    p_add.add_argument("-p", "--priority", choices=["low", "medium", "high"], default="medium")
    p_add.add_argument("--due", help="Срок в формате YYYY-MM-DD")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="Список задач")
    p_list.add_argument("--pending", action="store_true")
    p_list.add_argument("-p", "--priority")
    p_list.set_defaults(func=cmd_list)

    p_done = sub.add_parser("done", help="Отметить выполненной")
    p_done.add_argument("id", type=int)
    p_done.set_defaults(func=cmd_done)

    p_del = sub.add_parser("delete", help="Удалить задачу")
    p_del.add_argument("id", type=int)
    p_del.set_defaults(func=cmd_delete)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

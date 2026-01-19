from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from rich.style import Style
from test_by_ai.core.results import GlobalRunResult, TestStatus
from collections import defaultdict

console = Console()

def print_full_report(result: GlobalRunResult, metadata: dict):
    # 1. Header
    title = Text("test-by-ai", style="bold cyan")
    details = Text()
    details.append(f"Suites: {metadata.get('suites')}\n")
    details.append(f"Base URL: {metadata.get('base_url')}\n")
    details.append(f"Source: {metadata.get('source')}\n")
    details.append(f"Duration: {metadata.get('duration'):.2f}s")
    
    header_panel = Panel(
        details,
        title=title,
        border_style="cyan",
        expand=False
    )
    console.print(header_panel)
    console.print()

    # 2. Global Summary
    total_passed = sum(s.passed for s in result.suites)
    total_failed = sum(s.failed for s in result.suites)
    total_errors = sum(s.errors for s in result.suites)
    total_tests = sum(s.total for s in result.suites)
    endpoint_count = metadata.get('endpoint_count', 0)
    
    summary_table = Table(show_header=True, header_style="bold", box=None)
    summary_table.add_column("Endpoints")
    summary_table.add_column("Tests")
    summary_table.add_column("Passed", style="green")
    summary_table.add_column("Failed", style="red")

    summary_table.add_row(
        str(endpoint_count),
        str(total_tests),
        str(total_passed),
        str(total_failed + total_errors)
    )
    
    console.print(summary_table)
    console.print()

    if (total_failed + total_errors) == 0:
        console.print("[bold green]✔ All tests passed. API looks healthy.[/bold green]")
        if result.ai_analysis:
            _print_ai(result.ai_analysis)
        return

    # 3. Failures Detail
    console.print("[bold red]Failures detected:[/bold red]")
    
    for suite in result.suites:
        failures = [r for r in suite.results if r.status in (TestStatus.FAIL, TestStatus.ERROR)]
        if not failures:
            continue
            
        console.print(f"\n[bold]{suite.suite_name.upper()}[/bold]")
        
        # Group by endpoint (path)
        by_path = defaultdict(list)
        for f in failures:
            by_path[f.path].append(f)
            
        for path, fails in by_path.items():
            for f in fails:
                # Format: Method Path - Status (Code)
                # Cause: error message
                
                status_icon = "❌" if f.status == TestStatus.FAIL else "⚠"
                status_text = f"[red]{f.status.value}[/red]"
                code_text = f"({f.status_code})" if f.status_code else ""
                
                line1 = f"{status_icon} [bold cyan]{f.method}[/bold cyan] {f.path} {status_text} {code_text}"
                console.print(line1)
                
                # Cause (indented)
                if f.error_message:
                    # Clean up error message (max 2 lines)
                    err_lines = f.error_message.strip().split('\n')
                    short_err = err_lines[0][:120] # truncate
                    console.print(f"   ↳ {short_err}", style="dim")
    
    console.print()

    # 4. AI Section
    if result.ai_analysis:
        _print_ai(result.ai_analysis)

def _print_ai(analysis: str):
    console.print(Panel(Markdown(analysis), title="✨ AI Analysis", border_style="magenta", padding=(0, 1)))


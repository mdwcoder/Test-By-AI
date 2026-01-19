import argparse
import asyncio
import sys
import json
import time
from test_by_ai.core.runner import TestRunner
from test_by_ai.output import terminal
from test_by_ai.ai.gemini import GeminiProvider

def get_parser():
    parser = argparse.ArgumentParser(description="test-by-ai: AI-powered API Testing CLI")
    parser.add_argument("openapi_path", help="Path or URL to OpenAPI/Swagger JSON")
    parser.add_argument("--base-url", help="Override API Base URL")
    parser.add_argument("--suite", choices=["smoke", "contract", "negative", "all"], default="all", help="Test suite to run")
    parser.add_argument("--ai", choices=["gemini", "openai", "ollama"], help="Enable AI analysis")
    parser.add_argument("--save", nargs="?", const="auto", help="Save results to JSON file (auto or filename)")
    return parser

async def main_async():
    parser = get_parser()
    args = parser.parse_args()
    
    start_time = time.time()
    
    # Use console status like a spinner to hide noise during execution
    with terminal.console.status("[bold green]Running tests...[/bold green]"):
        try:
            runner = TestRunner(args.openapi_path, base_url=args.base_url)
            runner.load()
            
            ai_provider = None
            if args.ai == "gemini":
                try:
                    ai_provider = GeminiProvider()
                except ValueError:
                    pass # Output handled in report or ignored if silent
            
            suites = [args.suite]
            result = await runner.run(suites, ai_provider=ai_provider)
            
            duration = time.time() - start_time
            
            metadata = {
                "suites": args.suite,
                "base_url": runner.base_url,
                "source": args.openapi_path,
                "duration": duration,
                "endpoint_count": len(runner.endpoints)
            }
            
            # Print Final Report
            # Clear previous lines if needed? 
            # Status context manager handles cleaning itself usually.
            
        except Exception as e:
            terminal.console.print(f"[bold red]Error:[/bold red] {e}")
            sys.exit(1)

    # Print report strictly after execution
    terminal.print_full_report(result, metadata)

    # Save logic
    if args.save:
        should_save = True
        filename = args.save
    else:
        should_save = False
        # Ask only if fails? Or always? Prompt said "Por defecto: Preguntar" 
        # But for UX polish "Con mínimo ruido". 
        # We'll stick to requirement: "Preguntar... si el usuario no confirma (no guardar)"
        if sys.stdout.isatty():
             try:
                 terminal.console.print()
                 answer = terminal.console.input("[dim]Save results to JSON? [y/N]: [/dim]").strip().lower()
                 if answer == 'y':
                     should_save = True
                     filename = "auto"
             except:
                 pass

    if should_save:
        if not filename or filename == "auto":
            filename = f"results_{int(time.time())}.json"
        
        with open(filename, 'w') as f:
            json.dump(result.to_dict(), f, indent=2)
        terminal.console.print(f"[dim]Saved: {filename}[/dim]")
        
    sys.exit(1 if result.has_failures else 0)

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()

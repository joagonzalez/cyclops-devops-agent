from src.services.prompt_manager import PromptManager

def main() -> None:
    pm = PromptManager()

    # Example for LLM Call 1
    prompt1 = pm.render(
        "src/prompts/decompose_prompt.j2",
        {"user_prompt": "¿Cuál fue el uso promedio de CPU de los nodos de staging esta semana?"}
    )
    print("=== Prompt 1 ===")
    print(prompt1)
    print()

    # Example for LLM Call 2
    similar_metrics = [
        {"metric_name": "node_cpu_seconds_total", "description": "CPU seconds"},
        {"metric_name": "node_cpu_utilization", "description": "CPU utilization"},
    ]
    labels = ["instance", "job", "mode"]

    prompt2 = pm.render(
        "src/prompts/build_promql_prompt.j2",
        {
            "user_prompt": "¿Cuál fue el uso promedio de CPU de los nodos de staging esta semana?",
            "similar_metrics": similar_metrics,
            "labels": labels,
        }
    )
    print("=== Prompt 2 ===")
    print(prompt2)
    print()

    # Example for LLM Call 3
    prompt3 = pm.render(
        "src/prompts/summarize_results.j2",
        {
            "query_results": "[{'instance':'node1','value':0.75},{'instance':'node2','value':0.68}]",
            "user_prompt": "¿Cuál fue el uso promedio de CPU de los nodos de staging esta semana?",
        }
    )
    print("=== Prompt 3 ===")
    print(prompt3)
    print()

if __name__ == "__main__":
    main()

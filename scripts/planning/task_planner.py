"""
Chobi Task Planner

AIが生成したタスクを
・依存関係
・優先度
・複雑度

から実行順序に並べる
"""

from typing import List, Dict


class TaskPlanner:

    def __init__(self):
        pass

    def _priority_score(self, task: Dict) -> float:
        """
        タスクの優先度スコア
        """

        priority = task.get("priority", 5)
        complexity = task.get("complexity", 5)
        dependencies = len(task.get("depends_on", []))

        score = (priority * 10) - complexity - dependencies

        return score

    def resolve_dependencies(self, tasks: List[Dict]) -> List[Dict]:
        """
        依存関係を解決して順序を決める
        """

        resolved = []
        unresolved = tasks.copy()

        while unresolved:

            progress = False

            for task in unresolved[:]:

                deps = task.get("depends_on", [])

                if all(dep in [t["id"] for t in resolved] for dep in deps):

                    resolved.append(task)
                    unresolved.remove(task)
                    progress = True

            if not progress:
                # 循環依存など
                resolved.extend(unresolved)
                break

        return resolved

    def prioritize(self, tasks: List[Dict]) -> List[Dict]:
        """
        優先度ソート
        """

        return sorted(
            tasks,
            key=self._priority_score,
            reverse=True
        )

    def plan(self, tasks: List[Dict]) -> List[Dict]:
        """
        最終実行順序
        """

        tasks = self.resolve_dependencies(tasks)
        tasks = self.prioritize(tasks)

        return tasks
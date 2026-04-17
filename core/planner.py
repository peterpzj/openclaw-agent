"""
Planner - 任务规划器
将复杂任务拆解为子任务
"""
from typing import List, Dict, Any


class Planner:
    """任务规划器"""

    def __init__(self, max_steps: int = 10):
        self.max_steps = max_steps

    def plan(self, task: str) -> Dict[str, Any]:
        """
        规划任务步骤
        返回任务计划
        """
        # 简单实现：基于启发式规则
        steps = []
        current_step = {"task": task, "status": "pending"}

        # 检测任务复杂度
        if any(kw in task.lower() for kw in ["分析", "研究", "对比", "评估"]):
            steps.append({
                "action": "research",
                "description": "信息收集与研究",
                "status": "pending"
            })

        if any(kw in task.lower() for kw in ["写", "生成", "创建", "制作"]):
            steps.append({
                "action": "generate",
                "description": "内容生成",
                "status": "pending"
            })

        if any(kw in task.lower() for kw in ["优化", "改进", "完善"]):
            steps.append({
                "action": "improve",
                "description": "优化完善",
                "status": "pending"
            })

        if not steps:
            steps.append({
                "action": "execute",
                "description": "执行任务",
                "status": "pending"
            })

        return {
            "main_task": task,
            "steps": steps,
            "current_step": 0,
            "status": "planning"
        }

    def update_step_status(
        self,
        plan: Dict[str, Any],
        step_index: int,
        status: str = "completed"
    ) -> Dict[str, Any]:
        """更新步骤状态"""
        if 0 <= step_index < len(plan["steps"]):
            plan["steps"][step_index]["status"] = status
            plan["current_step"] = step_index + 1

            # 检查是否全部完成
            if all(s["status"] == "completed" for s in plan["steps"]):
                plan["status"] = "completed"

        return plan

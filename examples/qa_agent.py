"""
示例 Agent: 问答助手
"""
from typing import Dict, Any
from agents.base import BaseAgent
from core.engine import AgentEngine


class QAAgent(BaseAgent):
    """问答助手 Agent"""

    def __init__(self, engine: AgentEngine, **kwargs):
        system_prompt = """你是一个知识渊博的问答助手。
擅长回答各类问题，包括但不限于：
- 科学技术
- 生活常识
- 历史人文
- 健康养生

请用简洁、清晰的语言回答。"""
        super().__init__(
            name="QA助手",
            engine=engine,
            system_prompt=system_prompt,
            **kwargs
        )

    def think(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        # 使用 engine 进行对话
        response = self.engine.chat(
            messages=[{"role": "user", "content": task}],
            system=self.system_prompt
        )

        return {
            "question": task,
            "answer": response["content"],
            "agent": self.name
        }


# 使用示例
if __name__ == "__main__":
    engine = AgentEngine()
    agent = QAAgent(engine=engine)

    result = agent.run("什么是日间化疗？")
    print(f"问题: {result['question']}")
    print(f"回答: {result['answer']}")

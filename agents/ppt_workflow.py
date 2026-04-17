"""
PPT 工作流运行器
运行完整的三节点工作流并输出最终结果
"""
from agents.ppt_agent_v2 import PPTAgenV2, AnalystNode, DirectorNode, DesignerNode
from core.engine import AgentEngine
from typing import Dict, Any, Optional
import json


class PPTWorkflowRunner:
    """
    PPT 工作流运行器
    封装完整的三阶段工作流执行
    """

    def __init__(self, output_dir: str = "/tmp/ppt_workflow"):
        self.output_dir = output_dir
        self.engine = AgentEngine()

    def run_with_source(
        self,
        topic: str,
        source_material: str,
        num_achievements: int = 3,
        output_file: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        基于源文档运行完整工作流

        Args:
            topic: PPT 主题
            source_material: 源文档内容
            num_achievements: 提炼成就数量
            output_file: 可选，输出JSON文件路径

        Returns:
            完整工作流结果，包含三阶段输出
        """
        agent = PPTAgenV2(engine=self.engine, output_dir=self.output_dir)

        result = agent.run(
            source_material=source_material,
            topic=topic,
            num_achievements=num_achievements
        )

        # 保存结果
        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            result["output_file"] = output_file

        return result

    def run_stages_independently(
        self,
        topic: str,
        source_material: str,
        num_achievements: int = 3
    ) -> Dict[str, Any]:
        """
        独立运行每个阶段（用于调试或选择性执行）

        Returns:
            包含各阶段独立结果的字典
        """
        analyst = AnalystNode(self.engine)
        director = DirectorNode(self.engine)
        designer = DesignerNode(self.engine)

        # Stage 1: 分析提炼
        analysis = analyst.extract(
            source_material=source_material,
            topic=topic,
            num_achievements=num_achievements
        )

        # Stage 2: 大纲构建
        outline = director.build_outline(
            analysis=analysis,
            topic=topic
        )

        # Stage 3: 幻灯片生成
        slides = designer.generate_slides(
            outline=outline,
            analysis=analysis,
            topic=topic
        )

        return {
            "topic": topic,
            "stage1_analysis": analysis,
            "stage2_outline": outline,
            "stage3_slides": slides
        }


def demo_workflow():
    """
    演示工作流
    """
    runner = PPTWorkflowRunner()

    # 示例主题和源材料
    topic = "2024年度工作述职报告"

    source_material = """
    【工作成就概述】

    2024年度，我负责的项目取得了显著进展：

    成就1：门诊流程优化
    - 背景：原有门诊流程平均等待时间超过45分钟，患者满意度评分仅68分
    - 措施：引入智能预约系统，优化分诊流程，实施诊间结算
    - 结果：等待时间缩短至18分钟，满意度提升至92分，环比增长35%

    成就2：日间化疗服务扩展
    - 背景：化疗床位紧张，住院化疗患者平均等待床位时间3.5天
    - 措施：建立日间化疗中心，增加6个专用床位，实施标准化治疗路径
    - 结果：日均服务能力提升40%，等待时间降至0.5天，服务患者超2000人次

    成就3：医疗质量安全管理体系
    - 背景：原有质控体系分散，缺乏统一标准
    - 措施：建立多学科质控团队，实施PDCA循环管理，开展常态化督查
    - 结果：医疗不良事件下降62%，院内感染率控制在0.8%以下，达到三甲评审标准
    """

    print("🚀 开始运行 PPT 工作流...")
    print(f"📌 主题: {topic}")
    print("=" * 60)

    result = runner.run_with_source(
        topic=topic,
        source_material=source_material,
        num_achievements=3,
        output_file="/tmp/ppt_workflow_result.json"
    )

    print("\n" + "=" * 60)
    print("📊 工作流执行结果")
    print("=" * 60)

    # 打印分析结果
    print("\n🔬 Stage 1 - 内容提炼:")
    analysis = result["stages"]["analysis"]
    for i, ach in enumerate(analysis.get("achievements", []), 1):
        print(f"  {i}. {ach.get('name', 'N/A')}")
        print(f"     挑战: {ach.get('challenge', 'N/A')[:50]}...")
        print(f"     方案: {ach.get('solution', 'N/A')[:50]}...")

    # 打印大纲
    print("\n🎬 Stage 2 - 大纲构建:")
    outline = result["stages"]["outline"]
    print(f"  标题: {outline.get('presentation_title', 'N/A')}")
    for slide in outline.get("slides", [])[:5]:
        print(f"  第{slide.get('slide_number', '?')}页: [{slide.get('slide_type', 'N/A')}] {slide.get('title', 'N/A')}")

    # 打印幻灯片内容
    print("\n🎨 Stage 3 - 幻灯片生成:")
    slides = result["stages"]["slides"]
    print(f"  共生成 {len(slides)} 页")

    for slide in slides[:3]:
        print(f"\n  第{slide.get('slide_number', '?')}页: {slide.get('title', 'N/A')}")
        print(f"    要点: {', '.join(slide.get('bullet_points', [])[:2])}")
        print(f"    视觉: {slide.get('visual_suggestion', 'N/A')[:60]}...")

    print(f"\n💾 结果已保存: /tmp/ppt_workflow_result.json")

    return result


if __name__ == "__main__":
    demo_workflow()

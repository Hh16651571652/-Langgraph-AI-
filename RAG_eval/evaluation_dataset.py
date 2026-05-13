"""
RAG 评估测试集
包含问题、参考答案和检索到的上下文
用于评估 RAG 系统的检索质量和生成质量
"""

# 评估数据集格式：
# {
#     "question": "用户问题",
#     "ground_truth": "标准答案（人工标注）",
#     "contexts": ["检索到的文档片段1", "文档片段2", ...],
#     "answer": "LLM生成的答案"
# }

EVALUATION_DATASET = [
    {
        "question": "新员工入职需要完成哪些手续？",
        "ground_truth": "新员工入职需要完成以下手续：1. 签署雇佣合同和保密协议；2. 完成I-9表格验证；3. 设置直接存款；4. 参加新员工导向培训；5. 领取公司设备和访问权限。",
        "expected_categories": ["入职文件"],
        "difficulty": "easy"
    },
    {
        "question": "公司的远程工作政策是什么？",
        "ground_truth": "公司支持远程工作，员工可以在获得经理批准的情况下远程工作。远程工作需要保持良好的沟通，确保工作效率，并遵守公司的安全政策。",
        "expected_categories": ["就业政策"],
        "difficulty": "medium"
    },
    {
        "question": "如何申请年假？",
        "ground_truth": "员工可以通过公司内部系统提交休假申请，需要提前至少2周通知经理。年假天数根据工作年限确定，工作满1年可获得15天年假。",
        "expected_categories": ["福利和优待"],
        "difficulty": "easy"
    },
    {
        "question": "公司的薪酬结构是怎样的？",
        "ground_truth": "公司采用市场竞争力的薪酬体系，包括基本工资、绩效奖金和股权激励。薪酬每年进行一次审查和调整。",
        "expected_categories": ["就业政策"],
        "difficulty": "medium"
    },
    {
        "question": "OKR是什么？如何设定OKR？",
        "ground_truth": "OKR是Objectives and Key Results的缩写，即目标与关键成果法。设定OKR需要：1. 明确季度目标（Objective）；2. 设定3-5个可衡量的关键结果（Key Results）；3. 确保目标具有挑战性但可实现。",
        "expected_categories": ["操作文档"],
        "difficulty": "hard"
    },
    {
        "question": "公司的投诉政策是什么？",
        "ground_truth": "公司有明确的投诉政策，员工可以通过HR部门或匿名渠道提出投诉。所有投诉都会在5个工作日内得到回应，并进行公正调查。",
        "expected_categories": ["就业政策"],
        "difficulty": "medium"
    },
    {
        "question": "如何进行一对一会议（One on One）？",
        "ground_truth": "一对一会议是经理与定期举行的私人会议，通常每周或每两周一次。会议内容包括：工作进展、职业发展、反馈和问题解决。员工应提前准备议程。",
        "expected_categories": ["操作文档"],
        "difficulty": "medium"
    },
    {
        "question": "公司的健康保险覆盖范围是什么？",
        "ground_truth": "公司提供全面的健康保险，包括医疗、牙科和视力保险。员工可以选择不同的保险计划，公司承担80%的保费。",
        "expected_categories": ["福利和优待"],
        "difficulty": "easy"
    },
    {
        "question": "什么是产品宣言（Product Manifesto）？",
        "ground_truth": "产品宣言是公司产品的核心价值观和指导原则，强调用户体验、创新和质量。它指导产品团队的决策和开发方向。",
        "expected_categories": ["入职文件"],
        "difficulty": "hard"
    },
    {
        "question": "公司如何进行招聘和候选人筛选？",
        "ground_truth": "公司招聘流程包括：1. 简历筛选；2. 电话面试；3. 技术面试；4. 文化契合度面试；5. 背景调查。整个过程通常需要2-3周。",
        "expected_categories": ["操作文档", "招聘文件"],
        "difficulty": "hard"
    },
    {
        "question": "员工的带薪休假政策是怎样的？",
        "ground_truth": "公司提供带薪年假、病假和节假日。工作满1年可获得15天年假、10天病假和11个法定假日。",
        "expected_categories": ["福利和优待"],
        "difficulty": "easy"
    },
    {
        "question": "如何进行有效的会议？",
        "ground_truth": "有效会议的要点：1. 提前发送议程；2. 控制会议时间在30-60分钟；3. 确保每个人都有发言机会；4. 记录行动项和责任人；5. 会后发送会议纪要。",
        "expected_categories": ["操作文档"],
        "difficulty": "medium"
    },
    {
        "question": "公司的行为准则是什么？",
        "ground_truth": "公司行为准则要求员工：1. 保持专业和尊重；2. 避免利益冲突；3. 保护公司机密；4. 遵守法律法规；5. 营造包容的工作环境。",
        "expected_categories": ["就业政策"],
        "difficulty": "medium"
    },
    {
        "question": "新员工欢迎礼包包含什么？",
        "ground_truth": "新员工欢迎礼包包括：公司手册、品牌商品（T恤、水杯）、办公用品、团队介绍材料和导师联系方式。",
        "expected_categories": ["入职文件"],
        "difficulty": "easy"
    },
    {
        "question": "公司如何处理薪资和股权补偿？",
        "ground_truth": "薪资每月发放，股权补偿按照授予计划分期归属（通常4年）。员工可以查看详细的股权授予协议。",
        "expected_categories": ["就业政策"],
        "difficulty": "hard"
    },
    {
        "question": "如何进行预算规划？",
        "ground_truth": "预算规划流程：1. 收集各部门需求；2. 分析历史数据；3. 制定季度预算；4. 管理层审批；5. 月度跟踪和调整。",
        "expected_categories": ["操作文档"],
        "difficulty": "hard"
    },
    {
        "question": "公司的推荐奖金政策是什么？",
        "ground_truth": "员工成功推荐候选人入职可获得推荐奖金，通常为2000-5000美元，根据职位级别而定。奖金在候选人通过试用期后发放。",
        "expected_categories": ["福利和优待"],
        "difficulty": "medium"
    },
    {
        "question": "什么是Sabbatical（学术休假）政策？",
        "ground_truth": "工作满5年的员工可申请为期1个月的带薪学术休假，用于学习、旅行或个人发展。需要提前3个月申请。",
        "expected_categories": ["福利和优待"],
        "difficulty": "hard"
    },
    {
        "question": "公司如何保护员工隐私？",
        "ground_truth": "公司严格遵守隐私保护政策，员工个人信息仅用于合法业务目的，不会未经同意分享给第三方。员工有权访问和更正自己的信息。",
        "expected_categories": ["就业政策"],
        "difficulty": "medium"
    },
    {
        "question": "如何进行Hack Week活动？",
        "ground_truth": "Hack Week是公司每季度举办的创新活动，员工可以自由组队，在一周内开发创意项目。最后进行展示和评选，优秀项目可能纳入产品路线图。",
        "expected_categories": ["操作文档"],
        "difficulty": "medium"
    }
]

# 评估指标说明
METRICS_DESCRIPTION = {
    "context_precision": "上下文精确率 - 检索到的文档中有多少是真正相关的",
    "context_recall": "上下文召回率 - 是否检索到了所有相关文档",
    "faithfulness": "忠诚度 - 生成的答案是否忠实于检索到的上下文（无幻觉）",
    "answer_relevancy": "答案相关性 - 答案是否与问题相关",
    "answer_similarity": "答案相似度 - 生成答案与标准答案的语义相似度",
    "answer_correctness": "答案准确性 - 答案的事实正确性"
}

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
    },
    # ===== 新增问题（21-60）=====
    {
        "question": "公司的毒品和酒精政策是什么？",
        "ground_truth": "公司禁止在工作场所使用非法毒品。工作期间严禁饮酒，但在特定庆祝活动时可少量饮用啤酒或葡萄酒。违反政策可能导致纪律处分或解雇。",
        "expected_categories": ["就业政策"],
        "difficulty": "medium"
    },
    {
        "question": "员工可以享受哪些学习和发展福利？",
        "ground_truth": "公司提供继续教育津贴、行业会议差旅补贴、导师项目和在线课程报销。员工每年有学习预算用于技能提升。",
        "expected_categories": ["福利和优待"],
        "difficulty": "easy"
    },
    {
        "question": "如何申请学术休假（Sabbatical）？",
        "ground_truth": "工作满5年的员工可申请12周带薪学术休假。需提前4周通知团队，并提交休假计划。休假期间薪资正常发放。",
        "expected_categories": ["福利和优待"],
        "difficulty": "hard"
    },
    {
        "question": "公司的平等就业机会政策是什么？",
        "ground_truth": "公司是平等就业机会雇主，禁止基于种族、肤色、宗教、性别、性取向、年龄、残疾等特征的歧视。为残障求职者提供合理便利。",
        "expected_categories": ["就业政策"],
        "difficulty": "medium"
    },
    {
        "question": "新员工入职首日的安排是什么？",
        "ground_truth": "入职首日上午10点开始，包括设备配置、欢迎仪式、团队午餐和庆祝 activities。下午5点结束，完成一项对外公开产出。",
        "expected_categories": ["入职文件"],
        "difficulty": "easy"
    },
    {
        "question": "公司如何处理知识产权和发明？",
        "ground_truth": "员工需签署《专有信息与发明转让协议》，在职期间创造的知识产权归公司所有。离职后仍受协议约束。",
        "expected_categories": ["招聘文件", "就业政策"],
        "difficulty": "hard"
    },
    {
        "question": "远程办公的网络和环境要求是什么？",
        "ground_truth": "远程办公需要高速稳定网络、安静无干扰环境、私密会议空间。长期远程办公需提前2周申请并提交方案。",
        "expected_categories": ["就业政策"],
        "difficulty": "medium"
    },
    {
        "question": "公司的内推奖金政策详情是什么？",
        "ground_truth": "员工成功内推可获得5000美元奖金。候选人需在推荐后180天内首次入职，推荐人需在候选人入职前30天在职。奖金在入职90天内发放。",
        "expected_categories": ["福利和优待", "招聘文件"],
        "difficulty": "medium"
    },
    {
        "question": "病假如何累积和使用？",
        "ground_truth": "每工作30小时累积1小时病假，上限为5天。病假需向汇报创始人报备，无需医疗证明。超额不结转至下一年。",
        "expected_categories": ["福利和优待"],
        "difficulty": "easy"
    },
    {
        "question": "公司的任意雇佣政策是什么意思？",
        "ground_truth": "公司与员工为任意雇佣关系，双方可随时终止雇佣，无需理由。仅CEO有权修改此条款，需双方签署书面文件。",
        "expected_categories": ["就业政策"],
        "difficulty": "hard"
    },
    {
        "question": "新晋父母休假的时长和待遇如何？",
        "ground_truth": "全职员工可享受12周带薪新晋父母休假，适用于生育或收养。休假需在出生/收养后1年内使用，薪资由加州政策和公司补足差额。",
        "expected_categories": ["福利和优待"],
        "difficulty": "medium"
    },
    {
        "question": "如何设定个人OKR？",
        "ground_truth": "每季度设定3-5个目标，每个目标最多4个关键成果。目标需包含说明和对齐，关键成果必须可量化。每季度必须包含一个学习/成长目标。",
        "expected_categories": ["操作文档"],
        "difficulty": "hard"
    },
    {
        "question": "公司的医疗保险费用由谁承担？",
        "ground_truth": "公司承担员工个人医保的85%和家属医保的50%，剩余部分由员工承担。保险于入职次月1日起生效，通过TriNet管理。",
        "expected_categories": ["福利和优待"],
        "difficulty": "medium"
    },
    {
        "question": "员工可以放弃公司医保吗？",
        "ground_truth": "员工可以放弃TriNet医保，每月获得25美元医疗豁免补贴。放弃后需自行安排其他保险。",
        "expected_categories": ["福利和优待"],
        "difficulty": "easy"
    },
    {
        "question": "公司的伤残保险覆盖范围是什么？",
        "ground_truth": "全体员工享有短期伤残保险、长期伤残保险和身故伤残保险。保额为年薪1倍，65岁起有年龄限制。",
        "expected_categories": ["福利和优待"],
        "difficulty": "medium"
    },
    {
        "question": "技术岗位的薪资标准是多少？",
        "ground_truth": "技术岗5年以上经验年薪120000美元，5年以下经验年薪100000美元。每年1月调整以匹配市场水平。",
        "expected_categories": ["就业政策"],
        "difficulty": "easy"
    },
    {
        "question": "非技术岗位的薪资标准是多少？",
        "ground_truth": "非技术岗5年以上经验年薪100000美元，5年以下经验年薪70000美元。创始人的年薪固定为50000美元。",
        "expected_categories": ["就业政策"],
        "difficulty": "easy"
    },
    {
        "question": "员工可以用降薪换取股权吗？",
        "ground_truth": "可以，年薪减少5000美元可换取额外约0.1%股权。新员工默认授予41963股期权，约占已发行股份的0.9%。",
        "expected_categories": ["就业政策"],
        "difficulty": "medium"
    },
    {
        "question": "股权的行权期和锁定期是多长？",
        "ground_truth": "股权行权期为6年，锁定期为1年。行权期比行业标准长，鼓励员工长期陪伴、共同成长。",
        "expected_categories": ["就业政策"],
        "difficulty": "medium"
    },
    {
        "question": "社区的骚扰行为如何定义？",
        "ground_truth": "以被骚扰者主观感受为准，令对方不适即构成骚扰。包括冒犯言论、色情图片、恐吓、跟踪、不当肢体接触等。",
        "expected_categories": ["就业政策"],
        "difficulty": "medium"
    },
    {
        "question": "遭遇社区骚扰应该联系谁？",
        "ground_truth": "立即联系B（b@getclef.com）或任意创始人。投诉对象是某位创始人时，由其余创始人处理。严重情况启动外部调查。",
        "expected_categories": ["就业政策"],
        "difficulty": "medium"
    },
    {
        "question": "公司的开门政策是什么？",
        "ground_truth": "开门政策鼓励员工主动反馈不满、顾虑或困难。员工可向直属创始人、任意创始人或指定负责人投诉。公司禁止对善意投诉者实施报复。",
        "expected_categories": ["就业政策"],
        "difficulty": "medium"
    },
    {
        "question": "面对面会议的强制时段是什么？",
        "ground_truth": "太平洋时间上午10:30至下午1:00为强制面对面会议时段，需至少提前24小时预约。超出时段需提前一周安排。",
        "expected_categories": ["操作文档"],
        "difficulty": "easy"
    },
    {
        "question": "远程参会的要求是什么？",
        "ground_truth": "远程参会需使用视频会议、安静环境、高速网络。禁止电话接入或在公共场所接入。组织者需提前提供视频链接。",
        "expected_categories": ["操作文档"],
        "difficulty": "easy"
    },
    {
        "question": "创新攻坚周的时间安排是什么？",
        "ground_truth": "每季度第六周为创新攻坚周，暂停常规项目。员工组建最多4人的跨职能团队，围绕Clef相关方向开展短期项目研发。",
        "expected_categories": ["操作文档"],
        "difficulty": "medium"
    },
    {
        "question": "攻坚周项目的提案要求是什么？",
        "ground_truth": "任何人均可提出项目提案，唯一要求是项目需与Clef相关。周五工作日结束时各团队需向全公司展示成果，随后举办庆祝活动。",
        "expected_categories": ["操作文档"],
        "difficulty": "medium"
    },
    {
        "question": "一对一会谈的核心目的是什么？",
        "ground_truth": "一对一会谈聚焦员工个人感受、成长与信任建立，议程由员工主导。与普通工作会议不同，普通会议聚焦工作安排与状态同步。",
        "expected_categories": ["操作文档"],
        "difficulty": "medium"
    },
    {
        "question": "OKR的理想平均分是多少？为什么不能得10分？",
        "ground_truth": "OKR理想平均分为7分，因为目标需激进。10分代表目标设定过低，未达到挑战自我、推动成长的目的。OKR不用于绩效评估。",
        "expected_categories": ["操作文档"],
        "difficulty": "hard"
    },
    {
        "question": "如何跟踪OKR的执行进展？",
        "ground_truth": "每周一对一沟通时必须同步OKR，包括进展、卡点、所需帮助及目标调整需求。季度末先给每个关键成果打分，目标得分取关键成果平均分。",
        "expected_categories": ["操作文档"],
        "difficulty": "medium"
    },
    {
        "question": "产品的核心价值主张是什么？",
        "ground_truth": "核心价值是清晰易懂（Clarity），聚焦消除用户身份相关负面联想，提供正向体验。产品永远简单、不吓人，让用户掌控和保护身份。",
        "expected_categories": ["入职文件"],
        "difficulty": "hard"
    },
    {
        "question": "Clef认为用户登录时的核心负面情绪有哪些？",
        "ground_truth": "愧疚（做不到最佳安全做法）、焦虑（怕忘密码）、恐惧（怕身份泄露）。长期负面情绪会让用户将羞耻感与身份绑定。",
        "expected_categories": ["入职文件"],
        "difficulty": "hard"
    },
    {
        "question": "招聘的主要渠道有哪些？",
        "ground_truth": "主要通过内部推荐、主动招聘、主动投递三种渠道。需保持渠道畅通，关注各渠道偏见，确保符合团队建设目标与价值观。",
        "expected_categories": ["招聘文件", "操作文档"],
        "difficulty": "medium"
    },
    {
        "question": "内部推荐的主要风险是什么？如何应对？",
        "ground_truth": "主要风险是团队同质化。应对措施包括在推荐午餐会上强调多元化重要性，主动挖掘本地社区潜在候选人，探索抵消偏见的组织层面方法。",
        "expected_categories": ["招聘文件"],
        "difficulty": "hard"
    },
    {
        "question": "推荐午餐会的作用和时间是什么？",
        "ground_truth": "每月第二个周二举办推荐午餐会，同步开放岗位信息，全员梳理线上人脉筛选潜在候选人。员工可先与意向候选人沟通。",
        "expected_categories": ["招聘文件"],
        "difficulty": "easy"
    },
    {
        "question": "主动招聘的负责人是谁？",
        "ground_truth": "每个开放岗位需指定一名团队成员作为招聘负责人，前10名员工招聘由创始人负责。负责人需撰写岗位描述，主动寻找适配人选。",
        "expected_categories": ["招聘文件"],
        "difficulty": "medium"
    },
    {
        "question": "录用通知书生效需要满足哪些条件？",
        "ground_truth": "需签署录用通知书、完成保密协议签署、通过身份/工作资质核验。录用通知书构成完整协议，取代此前所有不一致表述。",
        "expected_categories": ["招聘文件"],
        "difficulty": "medium"
    },
    {
        "question": "员工是否可以兼职？",
        "ground_truth": "不允许，录用岗位为全职岗位，员工不得兼职，也不得从事与公司利益冲突的工作。",
        "expected_categories": ["招聘文件", "就业政策"],
        "difficulty": "easy"
    },
    {
        "question": "学习预算的重置周期是什么？",
        "ground_truth": "学习预算每年年初重置。当年6月入职员工的学习预算上限为2000美元，演讲支持次数上限为2次。",
        "expected_categories": ["福利和优待"],
        "difficulty": "easy"
    },
    {
        "question": "学习预算可以用于哪些支出？",
        "ground_truth": "可用于课程/学费（含线上）、专业书籍、学习视频、导师项目、行业会议门票、机票、酒店等。需经审批后实报实销。",
        "expected_categories": ["福利和优待"],
        "difficulty": "medium"
    },
    {
        "question": "员工参加行业会议演讲可获得什么支持？",
        "ground_truth": "可获得机票+酒店最高1000美元报销，每年最多4次。演讲支持与学习预算相互独立，不占用学习预算额度。",
        "expected_categories": ["福利和优待"],
        "difficulty": "medium"
    },
    {
        "question": "公司对员工邮箱和网络使用的隐私政策是什么？",
        "ground_truth": "员工对办公空间内的公司财产无隐私权。公司可随时监控、访问、阅读和复制员工的工作邮件及网络使用情况。邮箱密码不得透露给他人。",
        "expected_categories": ["就业政策"],
        "difficulty": "medium"
    },
    {
        "question": "年假如何累积？未休完可否折现？",
        "ground_truth": "年假每月累积1.25天，一年合计15天。无折现政策，默认当年使用。申请需提前1周安排并录入共享日历。",
        "expected_categories": ["福利和优待"],
        "difficulty": "easy"
    },
    {
        "question": "慢性病或重症员工可获得哪些支持？",
        "ground_truth": "可与创始人沟通远程办公、弹性工时、伤残假及其他支持方案。病假用完后无法工作可申请伤残假。",
        "expected_categories": ["福利和优待"],
        "difficulty": "medium"
    },
    {
        "question": "学术休假期间假期时长是否累积？",
        "ground_truth": "年假、病假、学术休假时长均不累积。休假不影响原有工作年限累计，返岗后需向团队做休假汇报。",
        "expected_categories": ["福利和优待"],
        "difficulty": "medium"
    },
    {
        "question": "连续工作10年可申请几次学术休假？",
        "ground_truth": "可申请2次，每满5年一次。每次为12周连续带薪学术休假，需围绕一个核心主题/活动。",
        "expected_categories": ["福利和优待"],
        "difficulty": "easy"
    },
    {
        "question": "入职前需要完成哪些准备事项？",
        "ground_truth": "需完成：1. 入职文书办理（签署录用通知书和专有信息协议）；2. 账户创建（Google Apps、Slack、Trello）；3. 背景资料学习；4. 对接Patricia完成薪资福利配置；5. 在团队共享日历添加入职事项。",
        "expected_categories": ["入职文件"],
        "difficulty": "hard"
    },
    {
        "question": "入职首周的核心安排是什么？",
        "ground_truth": "首周核心是学习公司规范、协作方式、工具使用等，逐步参与工作。入职一周后进行首次一对一沟通，讲解OKRs，新员工需制定本季度OKRs。",
        "expected_categories": ["入职文件"],
        "difficulty": "medium"
    },
    {
        "question": "公司对员工办公设备的搜查权是什么？",
        "ground_truth": "公司有权随时、无需预警搜查员工办公区的公司财产。员工给公司电脑上锁后，钥匙/密码副本必须交给任意创始人。",
        "expected_categories": ["就业政策"],
        "difficulty": "medium"
    },
    {
        "question": "标注'私人/机密'的工作邮件公司能查看吗？",
        "ground_truth": "可以，标注无效。公司可随时访问、监控、阅读、复制所有工作邮件。员工邮箱里的邮件属于公司财产，员工无隐私权。",
        "expected_categories": ["就业政策"],
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

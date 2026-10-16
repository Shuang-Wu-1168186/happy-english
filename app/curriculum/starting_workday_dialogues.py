"""Coherent dialogue scenes for the Starting the Workday course.

The original import split four vocabulary examples into unrelated turns.  This
module keeps the vocabulary coverage, but every scene now has a concrete
purpose, an answer to the previous turn, and a clear next action.
"""

from __future__ import annotations


MATERIAL_CODE = "software-workplace-starting-the-workday"


def turn(speaker: str, english: str, chinese: str) -> dict[str, str]:
    return {"speaker": speaker, "english": english, "chinese": chinese}


def dialogue(title: str, scenario: str, *turns: dict[str, str]) -> dict:
    return {"title": title, "scenario": scenario, "turns": list(turns)}


# The order deliberately mirrors the four vocabulary cards, then uses paired
# and complete conversations.  It retains the six-to-eight dialogue density
# expected by the generic lesson renderer without using disconnected fillers.
LESSON_DIALOGUES = {
    "morning-greetings-at-work": [
        dialogue(
            "1. Greeting a colleague at the door",
            "早上到办公室，Maya 和 Leo 在门口相遇。",
            turn("Maya", "Good morning, Leo. How was your commute?", "早上好，Leo。你上班路上顺利吗？"),
            turn("Leo", "Good morning, Maya. It was smooth, thanks. How about yours?", "早上好，Maya。很顺利，谢谢。你呢？"),
            turn("Maya", "Pretty good. I’m glad we both made it in before stand-up.", "也不错。很高兴我们都赶在站会前到了。"),
        ),
        dialogue(
            "2. Taking a few minutes to settle in",
            "站会前，Leo 刚到工位。",
            turn("Maya", "Do you need anything before stand-up?", "站会前你需要什么吗？"),
            turn("Leo", "I just need five minutes to settle in and check the overnight alerts.", "我只需要五分钟安顿一下，查看昨晚的告警。"),
            turn("Maya", "Of course. I’ll save you a seat and send you the agenda.", "当然。我给你留个座位，再把议程发给你。"),
        ),
        dialogue(
            "3. Arranging a catch-up after stand-up",
            "Maya 想了解 Leo 昨晚处理的问题。",
            turn("Maya", "I saw you were working on the payment issue late yesterday. Can we catch up after stand-up?", "我看到你昨晚还在处理支付问题。我们站会后能同步一下吗？"),
            turn("Leo", "Yes. I found a useful log entry, but I need to explain the context.", "可以。我找到了一条有用的日志，不过需要说明一下背景。"),
            turn("Maya", "Great. Let’s meet by the whiteboard at nine thirty.", "太好了。九点半我们在白板旁碰面。"),
        ),
        dialogue(
            "4. Getting started on a fix",
            "两人准备开始修复结账问题。",
            turn("Maya", "Are we ready to get started on the checkout fix?", "我们可以开始修复结账问题了吗？"),
            turn("Leo", "Almost. I’m waiting for the test account to be reset.", "快了。我在等测试账号重置。"),
            turn("Maya", "I’ll reset it now, then we can begin together.", "我现在就去重置，然后我们一起开始。"),
        ),
        dialogue(
            "5. Greeting before stand-up",
            "Leo 到得稍晚，Maya 确认他是否能赶上站会。",
            turn("Maya", "Good morning, Leo. Are you joining stand-up now?", "早上好，Leo。你现在来参加站会吗？"),
            turn("Leo", "In a minute. I need another moment to settle in and check one deployment alert.", "马上。我还需要一点时间安顿下来，查看一条部署告警。"),
            turn("Maya", "No problem. I’ll tell the team you’ll be there shortly.", "没问题。我会告诉团队你马上到。"),
            turn("Leo", "Thanks. I’ll join as soon as I’ve checked it.", "谢谢。我查完就来。"),
        ),
        dialogue(
            "6. Turning a catch-up into a shared start",
            "站会结束后，两人约好一起处理问题。",
            turn("Leo", "Can we catch up for ten minutes after stand-up?", "站会后我们能聊十分钟吗？"),
            turn("Maya", "Sure. Is it about the payment retry issue?", "当然。是关于支付重试问题吗？"),
            turn("Leo", "Yes. Once we agree on the approach, we can get started on the fix.", "对。我们确定方案后，就可以开始修复。"),
            turn("Maya", "Sounds good. Bring the logs and I’ll bring the ticket.", "听起来不错。你带日志，我带任务单。"),
        ),
        dialogue(
            "7. A complete morning check-in",
            "早晨站会前，Maya 和 Leo 从问候自然过渡到当天的协作。",
            turn("Maya", "Good morning, Leo. Did you get a chance to look at the overnight alert?", "早上好，Leo。你有时间看昨晚的告警了吗？"),
            turn("Leo", "Good morning. I just arrived, so I need a few minutes to settle in and read the logs.", "早上好。我刚到，需要几分钟安顿一下并看看日志。"),
            turn("Maya", "Take your time. Can we catch up after stand-up?", "慢慢来。我们站会后能同步一下吗？"),
            turn("Leo", "Yes. I want to show you what I found before we change anything.", "可以。改动之前我想先给你看看我发现的情况。"),
            turn("Maya", "Great. After that, we can get started on the fix together.", "太好了。之后我们就可以一起开始修复。"),
            turn("Leo", "Perfect. I’ll bring the logs to the meeting room.", "很好。我会把日志带到会议室。"),
        ),
    ],
    "asking-what-someone-is-working-on": [
        dialogue(
            "1. Checking a colleague’s current task",
            "站会后，Maya 想知道 Leo 正在处理什么。",
            turn("Maya", "What is your current task this morning?", "你今天上午正在处理什么任务？"),
            turn("Leo", "I’m updating the error messages for failed payments.", "我在更新支付失败时的错误提示。"),
            turn("Maya", "Thanks. I’ll review the copy once you push a draft.", "谢谢。你提交初稿后，我会帮你看看文案。"),
        ),
        dialogue(
            "2. Asking about a workstream",
            "Maya 确认 Leo 是否仍在支付相关的工作流上。",
            turn("Maya", "Which workstream are you on today?", "你今天负责哪个工作方向？"),
            turn("Leo", "I’m staying on the payments workstream, but I’m moving from the API to the checkout screen.", "我还在支付工作流上，不过会从接口转到结账页面。"),
            turn("Maya", "Good to know. I’ll route the customer question about checkout to you.", "了解。我会把客户关于结账的问题转给你。"),
        ),
        dialogue(
            "3. Reading the sprint board",
            "Maya 在计划会议前查看团队看板。",
            turn("Maya", "I noticed your card moved to In Review on the sprint board.", "我看到你的卡片在冲刺看板上移到了“评审中”。"),
            turn("Leo", "Right. I’ve finished the code and asked Priya to review it.", "对。我已经完成代码，并请 Priya 做评审。"),
            turn("Maya", "Great. I’ll keep an eye on it before planning.", "很好。计划会前我会关注它的进展。"),
        ),
        dialogue(
            "4. Asking for task context",
            "Maya 准备评审 Leo 的改动。",
            turn("Maya", "Before I review this pull request, can you give me the task context?", "在我评审这个拉取请求之前，你能介绍一下任务背景吗？"),
            turn("Leo", "The change stops duplicate charges when a customer retries a payment.", "这项改动是为了防止客户重试支付时被重复扣款。"),
            turn("Maya", "That helps. I’ll focus on the retry path in my review.", "这就清楚了。我会重点查看重试路径。"),
        ),
        dialogue(
            "5. Matching a task to its workstream",
            "两人避免在同一项工作上重复投入。",
            turn("Maya", "What is your current task after stand-up?", "站会后你当前要做什么？"),
            turn("Leo", "I’m finishing the payment-error copy; it belongs to the checkout workstream.", "我在完成支付错误提示文案；它属于结账工作流。"),
            turn("Maya", "Okay. I’ll take the reporting task so our work doesn’t overlap.", "好的。我来处理报表任务，避免我们工作重叠。"),
            turn("Leo", "Perfect. I’ll post an update when the copy is ready.", "很好。文案准备好后我会发个更新。"),
        ),
        dialogue(
            "6. Explaining a card before moving it",
            "Leo 希望看板上的状态和任务说明一致。",
            turn("Leo", "Can you move the card on the sprint board after the review?", "评审结束后你能把卡片移到冲刺看板的下一列吗？"),
            turn("Maya", "Sure. First, can you add the task context to the ticket?", "可以。不过先把任务背景补充到任务单里，可以吗？"),
            turn("Leo", "I’ll add a short note about the duplicate-charge case now.", "我现在就补一条关于重复扣款场景的说明。"),
            turn("Maya", "Thanks. Then the board will make sense to the whole team.", "谢谢。这样整个团队看这张看板就能理解了。"),
        ),
        dialogue(
            "7. Finding the right work before a review",
            "Maya 通过任务、工作流、看板和背景快速了解 Leo 的进展。",
            turn("Maya", "What is your current task now?", "你现在的当前任务是什么？"),
            turn("Leo", "I’m finishing the payment-error copy for the checkout screen.", "我在完成结账页面的支付错误提示文案。"),
            turn("Maya", "So you’re still on the payments workstream?", "所以你还在支付工作流上，对吗？"),
            turn("Leo", "Yes. I’ll move the card on the sprint board when the review is complete.", "对。评审完成后我会更新冲刺看板上的卡片。"),
            turn("Maya", "Before I review it, please add the task context to the ticket.", "在我评审之前，请先把任务背景补充到任务单里。"),
            turn("Leo", "Will do. I’ll explain the duplicate-charge case in the first paragraph.", "好的。我会在第一段说明重复扣款的场景。"),
        ),
    ],
    "talking-about-todays-tasks": [
        dialogue(
            "1. Starting with a to-do list",
            "Maya 和 Leo 在站会后确认当天最先处理的事。",
            turn("Maya", "What is at the top of your to-do list today?", "你今天待办清单的第一项是什么？"),
            turn("Leo", "First I’m reproducing the checkout bug, then I’ll write a regression test.", "我先复现结账缺陷，然后写一个回归测试。"),
            turn("Maya", "That order makes sense. Send me the test when it is ready.", "这个顺序很合理。测试写好后发给我。"),
        ),
        dialogue(
            "2. Confirming planned work",
            "Maya 确认数据迁移是否在 Leo 当天的计划中。",
            turn("Maya", "Is the migration part of your planned work today?", "数据迁移是你今天计划中的工作吗？"),
            turn("Leo", "Yes. I’ll prepare the validation script after I finish the bug fix.", "是的。修完缺陷后，我会准备校验脚本。"),
            turn("Maya", "Great. I’ll ask QA to reserve time for the validation.", "很好。我会请测试同事预留时间做验证。"),
        ),
        dialogue(
            "3. Clarifying task ownership",
            "团队要确定谁来推进登录改动。",
            turn("Maya", "Who has task ownership for the OAuth change?", "OAuth 改动由谁负责？"),
            turn("Leo", "I do. I’ll coordinate the API change and the client update.", "我负责。我会协调接口改动和客户端更新。"),
            turn("Maya", "Perfect. I’ll direct questions about that change to you.", "很好。关于这项改动的问题我会都转给你。"),
        ),
        dialogue(
            "4. Protecting a time block",
            "Maya 想约测试讨论，Leo 说明自己的专注时间。",
            turn("Maya", "Can we meet about the tests at eleven?", "我们十一点能聊一下测试吗？"),
            turn("Leo", "I’ve reserved a time block from ten to noon for the refactor.", "我已经预留了十点到十二点的时间块做重构。"),
            turn("Maya", "No problem. I’ll send an invite for twelve fifteen instead.", "没问题。我改发十二点十五分的邀请。"),
        ),
        dialogue(
            "5. Turning a to-do list into a plan",
            "两人把当天的事情排出先后顺序。",
            turn("Maya", "What is on your to-do list after the bug fix?", "修完缺陷后，你的待办清单上还有什么？"),
            turn("Leo", "The planned work is to validate the migration and update the release notes.", "计划中的工作是校验迁移，并更新发布说明。"),
            turn("Maya", "Okay. I’ll review the release notes while you run the validation.", "好的。你跑校验时，我来评审发布说明。"),
            turn("Leo", "That will keep us moving without waiting on each other.", "这样我们就不用互相等待，可以继续推进。"),
        ),
        dialogue(
            "6. Assigning work and protecting focus time",
            "Leo 说明任务负责人和可打扰的时间。",
            turn("Maya", "Do you have task ownership for the refactor as well?", "这项重构也是由你负责吗？"),
            turn("Leo", "Yes, but I need a two-hour time block to finish the risky part.", "是的，不过我需要两个小时的时间块完成风险最高的部分。"),
            turn("Maya", "I’ll handle incoming questions until then.", "那之前我来处理其他人提来的问题。"),
            turn("Leo", "Thanks. I’ll share the branch as soon as the refactor is ready.", "谢谢。重构完成后我会马上分享分支。"),
        ),
        dialogue(
            "7. A clear plan for the day",
            "Maya 和 Leo 共同确认当天计划、负责人和专注时间。",
            turn("Maya", "What is at the top of your to-do list today?", "你今天待办清单的第一项是什么？"),
            turn("Leo", "The planned work starts with the checkout bug, then the migration validation.", "计划中的工作先是结账缺陷，然后是迁移校验。"),
            turn("Maya", "Do you have task ownership for both?", "这两项都是由你负责吗？"),
            turn("Leo", "I own the bug fix. Priya owns the migration, but I’m helping with the validation.", "缺陷修复由我负责。迁移由 Priya 负责，不过我会协助校验。"),
            turn("Maya", "When should we avoid interrupting you?", "我们什么时候最好不要打扰你？"),
            turn("Leo", "I’ve blocked a time block from ten to noon for the bug fix. After that, I’m available.", "我预留了十点到十二点的时间块修缺陷。之后我就有时间了。"),
        ),
    ],
    "talking-about-yesterdays-progress": [
        dialogue(
            "1. Giving a progress update",
            "站会开始前，Maya 请 Leo 简要回顾昨天的工作。",
            turn("Maya", "Could you give me a progress update from yesterday?", "你能给我一个昨天的进度更新吗？"),
            turn("Leo", "Sure. I finished the API contract tests and fixed two validation errors.", "当然。我完成了接口契约测试，还修复了两个校验错误。"),
            turn("Maya", "Great. I’ll mention that in the stand-up notes.", "很好。我会在站会记录中写上这些。"),
        ),
        dialogue(
            "2. Reporting a completed task",
            "Maya 整理团队日报，需要确认已经完成的内容。",
            turn("Maya", "Which completed task should I add to the daily update?", "我应该把哪项已完成任务写进日报？"),
            turn("Leo", "Please add the password-reset flow. It passed review yesterday afternoon.", "请写上密码重置流程。它昨天下午通过了评审。"),
            turn("Maya", "Got it. I’ll link the pull request as well.", "明白。我也会附上拉取请求链接。"),
        ),
        dialogue(
            "3. Identifying remaining work",
            "Leo 的改动还差最后几项工作。",
            turn("Maya", "Is there any remaining work before we can release the change?", "发布这个改动前还有剩余工作吗？"),
            turn("Leo", "Yes. I still need to update the error messages and ask QA to retest.", "有。我还需要更新错误提示，并请测试同事重新验证。"),
            turn("Maya", "Okay. I’ll make sure QA has the test steps.", "好的。我会确保测试同事拿到测试步骤。"),
        ),
        dialogue(
            "4. Summarising yesterday’s outcome",
            "经理想知道一天结束时的实际结果。",
            turn("Maya", "What was yesterday’s outcome for the migration work?", "迁移工作昨天的结果是什么？"),
            turn("Leo", "The outcome was positive: the dry run completed without data loss.", "结果很好：演练运行完成，没有数据丢失。"),
            turn("Maya", "Excellent. I’ll update the risk note to reflect that.", "太好了。我会更新风险说明，反映这个结果。"),
        ),
        dialogue(
            "5. Connecting progress with a completed task",
            "Maya 需要知道昨天完成的内容是否已经体现在进度里。",
            turn("Maya", "Can you give me a progress update on the checkout work?", "你能更新一下结账功能的进度吗？"),
            turn("Leo", "The main completed task was the retry logic; it is now covered by tests.", "主要完成的任务是重试逻辑；现在已经有测试覆盖了。"),
            turn("Maya", "Great. I’ll move that item to done after stand-up.", "很好。站会后我会把那项移到“完成”。"),
            turn("Leo", "Thanks. I’ll start on the error messages next.", "谢谢。我接下来开始处理错误提示。"),
        ),
        dialogue(
            "6. Using yesterday’s outcome to plan what remains",
            "两人根据昨天的结果安排今天的收尾工作。",
            turn("Maya", "What was yesterday’s outcome from the staging test?", "预发布测试昨天的结果是什么？"),
            turn("Leo", "It passed, so the remaining work is only documentation and QA sign-off.", "测试通过了，所以剩余工作只有文档和测试确认。"),
            turn("Maya", "That is manageable. I’ll draft the documentation while you contact QA.", "这很好处理。我来起草文档，你去联系测试同事。"),
            turn("Leo", "Perfect. We should be ready for release this afternoon.", "很好。今天下午应该就能准备好发布。"),
        ),
        dialogue(
            "7. A complete yesterday-to-today update",
            "Maya 和 Leo 用昨天的进展来安排今天的下一步。",
            turn("Maya", "Could you give me a progress update from yesterday before stand-up?", "站会前你能给我一个昨天的进度更新吗？"),
            turn("Leo", "The completed task was the payment retry logic, along with the API contract tests.", "已完成的任务是支付重试逻辑和接口契约测试。"),
            turn("Maya", "What remaining work is left on that ticket?", "那张任务单还有哪些剩余工作？"),
            turn("Leo", "I need to update the customer-facing error message and ask QA to retest.", "我需要更新面向客户的错误提示，并请测试同事重新验证。"),
            turn("Maya", "So yesterday’s outcome was that the technical part is ready?", "也就是说，昨天的结果是技术部分已经准备好了吗？"),
            turn("Leo", "Exactly. Today is about checking the wording and getting final approval.", "没错。今天主要是确认文案并拿到最终批准。"),
        ),
    ],
    "talking-about-blockers": [
        dialogue(
            "1. Naming a blocker early",
            "Leo 在站会上说明为什么任务暂时无法推进。",
            turn("Maya", "You marked the ticket as blocked. What is the blocker?", "你把任务单标为阻塞了。阻塞问题是什么？"),
            turn("Leo", "The staging environment is rejecting our test payment account.", "预发布环境拒绝了我们的测试支付账号。"),
            turn("Maya", "I’ll ask the platform team to check the account configuration.", "我会请平台团队检查账号配置。"),
        ),
        dialogue(
            "2. Explaining a technical dependency",
            "Maya 判断问题能否由当前团队解决。",
            turn("Maya", "Can we fix this ourselves, or is there a technical dependency?", "这个问题我们能自己修复，还是有技术依赖？"),
            turn("Leo", "There is a technical dependency on the identity service team releasing their change.", "它依赖身份服务团队发布他们的改动。"),
            turn("Maya", "Okay. I’ll ask them for an expected release time.", "好的。我会问他们预计的发布时间。"),
        ),
        dialogue(
            "3. Raising an access issue",
            "Leo 无法进入需要配置的系统。",
            turn("Leo", "I can’t run the deployment because I have an access issue with the configuration store.", "我无法执行部署，因为我没有配置存储的访问权限。"),
            turn("Maya", "Do you already have a support ticket open?", "你已经提交支持工单了吗？"),
            turn("Leo", "Yes. I included the error message and the account name.", "提交了。我写了错误信息和账号名称。"),
        ),
        dialogue(
            "4. Setting an expectation for waiting time",
            "Maya 需要向团队说明何时可能恢复工作。",
            turn("Maya", "How much waiting time should we expect from the platform team?", "我们预计要等平台团队多久？"),
            turn("Leo", "They said about thirty minutes, but I’ll update the ticket if it takes longer.", "他们说大约三十分钟，不过如果更久我会更新任务单。"),
            turn("Maya", "Thanks. I’ll move the review until after their response.", "谢谢。我会把评审推迟到他们回复之后。"),
        ),
        dialogue(
            "5. Linking a blocker to its dependency",
            "两人确认阻塞的来源并决定如何跟进。",
            turn("Maya", "I saw the blocker tag on your ticket. Which technical dependency is holding us up?", "我看到你的任务单有阻塞标签。是哪项技术依赖卡住了我们？"),
            turn("Leo", "We need the identity service team to deploy their token change first.", "我们需要身份服务团队先部署他们的令牌改动。"),
            turn("Maya", "I’ll message their lead and ask whether we can test against a temporary version.", "我会联系他们的负责人，问能否先用临时版本测试。"),
            turn("Leo", "That would let us keep moving while we wait for the full release.", "这样在等正式发布时我们也能继续推进。"),
        ),
        dialogue(
            "6. Combining an access issue with waiting time",
            "Leo 说明了权限问题和短期计划。",
            turn("Maya", "Is the deployment delay still an access issue?", "部署延迟还是权限问题吗？"),
            turn("Leo", "Yes. Support is resetting my role, and the waiting time should be about thirty minutes.", "是的。支持团队正在重置我的角色，等待时间大概三十分钟。"),
            turn("Maya", "While we wait, can you prepare the release notes?", "等待期间，你能先准备发布说明吗？"),
            turn("Leo", "Sure. That way I can deploy as soon as the access is restored.", "可以。这样权限恢复后我就能马上部署。"),
        ),
        dialogue(
            "7. Explaining a blocker with a recovery plan",
            "站会上，Leo 清楚说明问题、依赖、权限和等待安排。",
            turn("Maya", "What is blocking the checkout release?", "是什么阻塞了结账功能的发布？"),
            turn("Leo", "The blocker is a technical dependency: the identity service change has not reached staging yet.", "阻塞问题是一项技术依赖：身份服务的改动还没有到预发布环境。"),
            turn("Maya", "Do you also have an access issue there?", "你在那边也有访问权限问题吗？"),
            turn("Leo", "No, my access is fine. The team expects about thirty minutes of waiting time before their deployment finishes.", "没有，我的权限没问题。他们预计还要等待大约三十分钟才能完成部署。"),
            turn("Maya", "Okay. Please prepare the test plan while we wait and update us at ten thirty.", "好的。等待期间请准备测试计划，并在十点半向我们更新。"),
            turn("Leo", "Will do. I’ll start the tests as soon as their change is available.", "好的。他们的改动一可用，我就开始测试。"),
        ),
    ],
    "asking-for-a-quick-chat": [
        dialogue(
            "1. Requesting a quick chat",
            "Maya 需要在评审前确认一个问题。",
            turn("Maya", "Have you got a minute for a quick chat about the review?", "你有一分钟快速聊一下评审的事吗？"),
            turn("Leo", "Yes, I can spare a minute. What do you need?", "有，我可以抽一分钟。你需要什么？"),
            turn("Maya", "I want to confirm the expected error message before I leave a comment.", "我想在留言前确认一下预期的错误提示。"),
        ),
        dialogue(
            "2. Finding a calendar slot",
            "两人需要安排一个稍长的讨论。",
            turn("Maya", "I think this needs more than a minute. Do you have a calendar slot this afternoon?", "我觉得这件事不止要一分钟。你下午有日历时间段吗？"),
            turn("Leo", "I have fifteen minutes free at three thirty.", "我三点半有十五分钟空闲。"),
            turn("Maya", "Great. I’ll send an invite with the ticket link.", "太好了。我会发邀请并附上任务单链接。"),
        ),
        dialogue(
            "3. Avoiding an unnecessary context switch",
            "Leo 正在专注排查问题，Maya 先确认是否适合打断。",
            turn("Maya", "Is now a good time to talk about the customer report?", "现在适合聊客户报告吗？"),
            turn("Leo", "Could we wait ten minutes? I’m in the middle of a context switch while debugging.", "我们能等十分钟吗？我正在调试，中途切换任务会打断思路。"),
            turn("Maya", "Of course. I’ll write down the question so we can pick it up then.", "当然。我会把问题写下来，十分钟后再聊。"),
        ),
        dialogue(
            "4. Calling a small team huddle",
            "问题需要多个人一起快速决定。",
            turn("Maya", "The API change affects QA and support too. Should we have a team huddle?", "接口改动也影响测试和支持团队。我们要不要开个团队短会？"),
            turn("Leo", "Yes, a ten-minute huddle would be faster than separate messages.", "要，开十分钟短会会比单独发消息更快。"),
            turn("Maya", "I’ll invite them now and state the decision we need.", "我现在邀请他们，并写清楚需要做的决定。"),
        ),
        dialogue(
            "5. Moving a quick chat to the calendar",
            "临时问题变成需要专门讨论的话题。",
            turn("Maya", "Have you got a minute for a quick chat about the migration?", "你有一分钟快速聊一下迁移吗？"),
            turn("Leo", "I do, but the data question may need more time than that.", "有，不过数据问题可能不止一分钟能说清。"),
            turn("Maya", "Then let’s use the calendar slot you have at three thirty.", "那我们就用你三点半的日历时间段。"),
            turn("Leo", "Good idea. Send the question first so I can prepare.", "好主意。先把问题发给我，我可以准备一下。"),
        ),
        dialogue(
            "6. Choosing between focus time and a team huddle",
            "Maya 避免打断 Leo，同时保证团队及时决策。",
            turn("Maya", "Could we pull you into a team huddle now?", "我们现在能请你参加一个团队短会吗？"),
            turn("Leo", "I’m in the middle of a difficult context switch, so I’d rather join in ten minutes.", "我正处在一个很难切换任务的阶段，所以希望十分钟后再参加。"),
            turn("Maya", "That works. I’ll collect the questions first and start when you join.", "可以。我先收集问题，等你来再开始。"),
            turn("Leo", "Thanks. I’ll finish this debug step and be there at ten past.", "谢谢。我完成这一步调试，十分钟后到。"),
        ),
        dialogue(
            "7. Choosing the right way to talk",
            "Maya 根据问题的紧急程度、时间和参与人安排沟通。",
            turn("Maya", "Have you got a minute for a quick chat about the release note?", "你有一分钟快速聊一下发布说明吗？"),
            turn("Leo", "Yes, but I’m close to finishing this debug step, and a context switch now would slow me down.", "有，不过我快完成这一步调试了，现在切换任务会让我慢下来。"),
            turn("Maya", "No problem. Do you have a calendar slot after lunch?", "没问题。午饭后你有日历时间段吗？"),
            turn("Leo", "I have fifteen minutes at one thirty.", "我一点半有十五分钟。"),
            turn("Maya", "Great. If QA also has questions, we can turn it into a short team huddle.", "很好。如果测试同事也有问题，我们可以把它变成一个短的团队会议。"),
            turn("Leo", "Perfect. Send the invite and I’ll come prepared.", "很好。发邀请吧，我会准备好。"),
        ),
    ],
    "checking-someones-availability": [
        dialogue(
            "1. Checking availability",
            "Maya 想约 Leo 讨论客户问题。",
            turn("Maya", "What is your availability after stand-up?", "站会后你什么时候有空？"),
            turn("Leo", "I’m free for twenty minutes before the planning meeting.", "计划会前我有二十分钟空闲。"),
            turn("Maya", "Great. Let’s use that time for the customer question.", "太好了。我们就用那段时间讨论客户问题。"),
        ),
        dialogue(
            "2. Respecting focus time",
            "Leo 需要一段不被打扰的时间完成复杂任务。",
            turn("Maya", "Can I ask you to review this now?", "我现在可以请你评审这个吗？"),
            turn("Leo", "I’m in focus time until eleven. Could you send it over, and I’ll look then?", "我十一点前都在专注工作。你可以先发给我，我到时看吗？"),
            turn("Maya", "Absolutely. I’ll add the key questions to the pull request.", "当然。我会把关键问题写在拉取请求里。"),
        ),
        dialogue(
            "3. Choosing a meeting window",
            "两人要避开各自已有的会议。",
            turn("Maya", "When is your best meeting window this afternoon?", "你下午最适合开会的时间段是什么时候？"),
            turn("Leo", "Between three and four works well; my other meetings finish by then.", "三点到四点很合适；那之前我的其他会议都结束了。"),
            turn("Maya", "Perfect. I’ll book thirty minutes at three.", "很好。我订三点的三十分钟。"),
        ),
        dialogue(
            "4. Setting expectations for response time",
            "Leo 下午会参加培训，需要提前说明回复速度。",
            turn("Maya", "Can you keep an eye on the support channel this afternoon?", "你下午能关注一下支持频道吗？"),
            turn("Leo", "I can, but my response time may be slow while I’m in the security workshop.", "可以，不过我参加安全培训时回复可能会比较慢。"),
            turn("Maya", "Thanks for letting me know. I’ll cover urgent questions during the workshop.", "谢谢你提前说。我会在培训期间处理紧急问题。"),
        ),
        dialogue(
            "5. Planning around focus time",
            "Maya 在约会前先了解 Leo 的空闲时间和专注安排。",
            turn("Maya", "What is your availability for a design review today?", "你今天什么时候有空做设计评审？"),
            turn("Leo", "I have focus time until two, but I’m free after that.", "我两点前有专注时间，之后有空。"),
            turn("Maya", "Okay. I’ll send the design now and book us for two thirty.", "好的。我现在把设计发给你，并订两点半的时间。"),
            turn("Leo", "That gives me enough time to read it before we talk.", "这样我有足够时间在讨论前阅读。"),
        ),
        dialogue(
            "6. Matching a meeting window to response time",
            "两人既安排了会议，也明确了不在线时如何处理紧急消息。",
            turn("Maya", "Does the meeting window from three to three thirty still work?", "三点到三点半的开会时间还合适吗？"),
            turn("Leo", "Yes. After that I’ll be in training, so my response time will be slower.", "合适。之后我要去培训，回复速度会慢一些。"),
            turn("Maya", "I’ll make our decisions clear in the notes before you go.", "你走之前，我会在记录里写清楚我们的决定。"),
            turn("Leo", "Thanks. That will let the team continue without waiting for me.", "谢谢。这样团队不用等我也能继续推进。"),
        ),
        dialogue(
            "7. Scheduling without interrupting work",
            "Maya 结合 Leo 的时间、专注工作和回复节奏安排讨论。",
            turn("Maya", "What is your availability for a short design review today?", "你今天什么时候有空做一个简短的设计评审？"),
            turn("Leo", "I’m in focus time until two, but I have a meeting window from two thirty to three.", "我两点前都在专注工作，不过两点半到三点有开会时间。"),
            turn("Maya", "That works. I’ll send the document now so you can read it before then.", "可以。我现在发文档，这样你到时前可以先看。"),
            turn("Leo", "Great. After three I’m in training, so my response time may be slow.", "很好。三点后我要培训，所以回复可能会慢。"),
            turn("Maya", "I’ll capture any follow-up questions in the document instead of expecting an immediate reply.", "我会把后续问题记在文档里，不要求你马上回复。"),
            turn("Leo", "Perfect. I’ll answer them when the workshop ends.", "很好。培训结束后我会回复。"),
        ),
    ],
    "prioritising-tasks": [
        dialogue(
            "1. Naming the top priority",
            "Maya 和 Leo 在早上确认最重要的工作。",
            turn("Maya", "What is your top priority this morning?", "你今天上午的最高优先级是什么？"),
            turn("Leo", "The checkout bug is my priority because it is stopping a small group of customers from paying.", "结账缺陷是我的优先级，因为它让一小部分客户无法付款。"),
            turn("Maya", "Okay. I’ll take the documentation task so you can focus on that.", "好的。我来处理文档任务，让你专注于它。"),
        ),
        dialogue(
            "2. Responding to an urgent request",
            "支持团队刚刚转来一个影响客户的问题。",
            turn("Maya", "Support has sent an urgent request about failed payments. Can you look now?", "支持团队刚转来一个支付失败的紧急请求。你现在能看吗？"),
            turn("Leo", "Yes. I’ll pause the refactor and check whether it is the same checkout bug.", "可以。我会暂停重构，看看是否是同一个结账缺陷。"),
            turn("Maya", "Thanks. I’ll tell support when you have an initial answer.", "谢谢。你有初步结论后我会通知支持团队。"),
        ),
        dialogue(
            "3. Explaining business impact",
            "Maya 需要判断一个问题是否足够紧急。",
            turn("Maya", "Why should we move this ticket ahead of the refactor?", "为什么要把这张任务单排在重构前面？"),
            turn("Leo", "The business impact is high because customers cannot complete their orders.", "业务影响很大，因为客户无法完成订单。"),
            turn("Maya", "That is clear. I’ll mark it as critical and notify the team.", "很清楚。我会把它标为严重，并通知团队。"),
        ),
        dialogue(
            "4. Making a trade-off",
            "团队讨论是先快速恢复服务，还是先完成彻底重构。",
            turn("Maya", "Can we fix this quickly without making the code harder to maintain?", "我们能快速修复，同时不让代码更难维护吗？"),
            turn("Leo", "The trade-off is speed now versus a cleaner solution later.", "这里的取舍是现在更快恢复，还是以后得到更干净的方案。"),
            turn("Maya", "Let’s ship the safe short-term fix and create a follow-up refactor ticket.", "我们先发布安全的短期修复，再创建一张后续重构任务单。"),
        ),
        dialogue(
            "5. Reordering work for an urgent request",
            "Leo 调整当天计划，先处理影响客户的问题。",
            turn("Maya", "Is the checkout bug still your first priority?", "结账缺陷仍然是你的第一优先级吗？"),
            turn("Leo", "Yes. The urgent request from support confirms that customers are still affected.", "是的。支持团队的紧急请求证实客户仍然受到影响。"),
            turn("Maya", "Then I’ll move the refactor to tomorrow and update the sprint board.", "那我把重构移到明天，并更新冲刺看板。"),
            turn("Leo", "Thanks. I’ll post an update as soon as I have a fix.", "谢谢。我一有修复方案就会发更新。"),
        ),
        dialogue(
            "6. Choosing a safe trade-off",
            "两人基于影响范围选择解决方案。",
            turn("Maya", "What is the business impact if we wait for the full refactor?", "如果等完整重构，业务影响是什么？"),
            turn("Leo", "Customers may keep failing at checkout, so the trade-off favors a small safe patch now.", "客户可能继续在结账时失败，所以取舍更倾向于现在先做一个小而安全的补丁。"),
            turn("Maya", "Agreed. Let’s document the limitation and schedule the refactor next sprint.", "同意。我们记录这个限制，并把重构排到下个迭代。"),
            turn("Leo", "I’ll include that plan in the release note.", "我会把这个计划写进发布说明。"),
        ),
        dialogue(
            "7. Setting priorities with the right context",
            "Maya 和 Leo 在紧急客户问题、业务影响和长期质量之间做出清楚选择。",
            turn("Maya", "We have the checkout bug, a refactor, and an urgent request from support. What is the priority?", "我们有结账缺陷、一个重构任务，还有支持团队的紧急请求。优先级怎么排？"),
            turn("Leo", "The checkout bug comes first because the urgent request shows customers are actively affected.", "结账缺陷优先，因为紧急请求说明客户正在受影响。"),
            turn("Maya", "What is the business impact if we delay the refactor?", "如果推迟重构，业务影响是什么？"),
            turn("Leo", "Low for this week. The real trade-off is fixing payments now or spending time on cleaner code first.", "这周影响不大。真正的取舍是现在修支付问题，还是先花时间做更干净的代码。"),
            turn("Maya", "Let’s fix payments now and put the refactor at the top of next sprint.", "我们现在先修支付问题，把重构放到下个迭代的最高优先级。"),
            turn("Leo", "Agreed. I’ll update the ticket and start on the patch.", "同意。我会更新任务单并开始做补丁。"),
        ),
    ],
    "giving-a-quick-status-update": [
        dialogue(
            "1. Giving a brief status update",
            "Maya 在团队频道询问账户迁移的最新情况。",
            turn("Maya", "Can you give me a quick status update on the account migration?", "你能快速更新一下账户迁移的状态吗？"),
            turn("Leo", "The data copy is complete, and I’m checking the validation report now.", "数据复制已经完成，我正在查看校验报告。"),
            turn("Maya", "Thanks. I’ll let the team know that the migration is progressing.", "谢谢。我会告诉团队迁移正在推进。"),
        ),
        dialogue(
            "2. Describing work in progress",
            "Leo 说明数据导入还没有结束。",
            turn("Maya", "Is the import finished yet?", "导入完成了吗？"),
            turn("Leo", "Not yet. The final batch is still work in progress, but the earlier batches look healthy.", "还没有。最后一批仍在进行中，不过前面的批次看起来正常。"),
            turn("Maya", "Okay. I’ll wait before I ask QA to start their checks.", "好的。我会等一等再请测试同事开始检查。"),
        ),
        dialogue(
            "3. Naming the next step",
            "Maya 想知道 Leo 完成校验后要做什么。",
            turn("Maya", "What is your next step once the report is clean?", "报告没有问题后，你的下一步是什么？"),
            turn("Leo", "My next step is to run the migration against staging with production-like data.", "我的下一步是在预发布环境用接近生产的数据运行迁移。"),
            turn("Maya", "Great. I’ll make sure the staging window is reserved.", "很好。我会确保预发布环境的时间窗口预留好。"),
        ),
        dialogue(
            "4. Raising a delivery risk",
            "Leo 需要让团队知道一个可能影响发布时间的因素。",
            turn("Maya", "Is there anything that could delay today’s release?", "有什么可能影响今天发布的因素吗？"),
            turn("Leo", "The only delivery risk is the vendor’s response time on the API limit increase.", "唯一的交付风险是供应商提高接口限额的回复时间。"),
            turn("Maya", "Thanks. I’ll flag that in the release channel and prepare a fallback.", "谢谢。我会在发布频道标注这一点，并准备备用方案。"),
        ),
        dialogue(
            "5. Updating work in progress",
            "Maya 需要一句能让团队理解当前进度的更新。",
            turn("Maya", "What should I put in the project channel as a status update?", "我应该在项目频道里发什么状态更新？"),
            turn("Leo", "Say that the data import is work in progress and that the first validation checks have passed.", "写数据导入正在进行中，并且第一轮校验已经通过。"),
            turn("Maya", "Got it. I’ll add that we expect another update at noon.", "明白。我会加上我们预计中午再更新一次。"),
            turn("Leo", "Perfect. That sets the right expectation without overpromising.", "很好。这样既能设定正确预期，也不会过度承诺。"),
        ),
        dialogue(
            "6. Pairing the next step with a risk",
            "两人把接下来的行动和潜在风险一起说清楚。",
            turn("Maya", "What is the next step after the staging run?", "预发布运行后的下一步是什么？"),
            turn("Leo", "I’ll ask QA to test it, but the delivery risk is still the vendor API limit.", "我会请测试同事验证，不过交付风险仍然是供应商的接口限额。"),
            turn("Maya", "I’ll contact the vendor now so we are not waiting at the end.", "我现在就联系供应商，避免最后才等待。"),
            turn("Leo", "Thanks. I’ll prepare the QA checklist while you do that.", "谢谢。你联系时我会准备测试清单。"),
        ),
        dialogue(
            "7. A concise update with a clear plan",
            "Leo 用进度、进行中的工作、下一步和风险向团队汇报。",
            turn("Maya", "Can you give the team a quick status update on the migration?", "你能给团队快速更新一下迁移状态吗？"),
            turn("Leo", "The data copy is complete. The final validation batch is still work in progress.", "数据复制已经完成。最后一批校验仍在进行中。"),
            turn("Maya", "What is your next step after that?", "之后你的下一步是什么？"),
            turn("Leo", "I’ll run the migration in staging and hand it to QA for testing.", "我会在预发布环境运行迁移，然后交给测试同事验证。"),
            turn("Maya", "Do we have any delivery risk?", "我们有交付风险吗？"),
            turn("Leo", "Only the vendor API limit. You’re following up while I prepare the checklist.", "只有供应商的接口限额。你来跟进，我则准备检查清单。"),
        ),
    ],
    "wrapping-up-the-day": [
        dialogue(
            "1. Posting an end-of-day update",
            "下班前，Maya 确认 Leo 是否已把进展同步给团队。",
            turn("Maya", "Have you posted an end-of-day update in the project channel?", "你在项目频道发下班前更新了吗？"),
            turn("Leo", "Yes. I wrote that the checkout fix is ready for QA and linked the pull request.", "发了。我写了结账修复已经可以让测试同事验证，并附上了拉取请求。"),
            turn("Maya", "Great. I’ll add the expected test time so everyone knows what happens next.", "很好。我会加上预计测试时间，让大家知道接下来会怎样。"),
        ),
        dialogue(
            "2. Writing a useful handover note",
            "Leo 要把夜间可能需要的信息交给值班同事。",
            turn("Maya", "Does the on-call engineer have enough information for tonight?", "今晚值班工程师有足够的信息吗？"),
            turn("Leo", "Yes. My handover note explains how to restart the failed job and where to find the logs.", "有。我的交接说明写了如何重启失败任务，以及在哪里找日志。"),
            turn("Maya", "Perfect. I’ll tag the on-call engineer so they see it.", "很好。我会提醒值班工程师查看。"),
        ),
        dialogue(
            "3. Moving a carry-over task to tomorrow",
            "一项工作没有必要在当天匆忙做完。",
            turn("Maya", "Are you finishing the dashboard cleanup before you leave?", "你离开前会完成仪表盘清理吗？"),
            turn("Leo", "No. It is a carry-over task for tomorrow because the release work came first today.", "不会。它是要延续到明天的任务，因为今天发布工作优先。"),
            turn("Maya", "That is sensible. I’ll move it to tomorrow’s board.", "这样很合理。我会把它移到明天的看板上。"),
        ),
        dialogue(
            "4. Confirming tomorrow’s plan",
            "Maya 和 Leo 在离开前核对明早的安排。",
            turn("Maya", "What is the first item in your tomorrow’s plan?", "你明日计划的第一项是什么？"),
            turn("Leo", "I’ll start by reviewing QA feedback on the checkout fix.", "我会先查看测试同事对结账修复的反馈。"),
            turn("Maya", "Okay. I’ll make sure their notes are in the ticket before you start.", "好的。我会确保你开始前，他们的备注已经放进任务单。"),
        ),
        dialogue(
            "5. Making the end-of-day update actionable",
            "两人把当天进展和夜间交接信息连起来。",
            turn("Maya", "What did you include in the end-of-day update?", "你在下班前更新里写了什么？"),
            turn("Leo", "I said the fix is ready for QA, and I linked the handover note for the on-call engineer.", "我写了修复已经可以给测试同事验证，并附上了给值班工程师的交接说明。"),
            turn("Maya", "Excellent. I’ll add the expected QA result time before I log off.", "很好。我下线前会加上预计拿到测试结果的时间。"),
            turn("Leo", "Thanks. That should make the evening handoff clear.", "谢谢。这样晚间交接就清楚了。"),
        ),
        dialogue(
            "6. Carrying work into a realistic tomorrow plan",
            "Leo 把未完成的工作放进明天的明确安排。",
            turn("Maya", "Will the dashboard cleanup be a carry-over task?", "仪表盘清理会成为延续到明天的任务吗？"),
            turn("Leo", "Yes. My tomorrow’s plan is to review QA feedback first, then finish the cleanup.", "会。我的明日计划是先看测试反馈，然后完成清理。"),
            turn("Maya", "That order works. I’ll leave the cleanup ticket at the top of your list after QA.", "这个顺序合适。我会把清理任务放在测试之后的待办首位。"),
            turn("Leo", "Perfect. I’ll pick it up first thing after the review.", "很好。评审完我就马上继续做。"),
        ),
        dialogue(
            "7. Closing the day with a handoff and a plan",
            "下班前，Maya 和 Leo 确认团队已收到进展、交接和明天安排。",
            turn("Maya", "Before you go, have you posted an end-of-day update?", "你走之前，发下班前更新了吗？"),
            turn("Leo", "Yes. It says the checkout fix is with QA, and the handover note is linked for the on-call engineer.", "发了。上面写着结账修复正在由测试同事验证，也附上了给值班工程师的交接说明。"),
            turn("Maya", "What will happen to the dashboard cleanup?", "仪表盘清理怎么办？"),
            turn("Leo", "It is a carry-over task. My tomorrow’s plan is to finish it after I review QA feedback.", "它会延续到明天。我的明日计划是在查看测试反馈后完成它。"),
            turn("Maya", "Great. I’ll put that order in the ticket so the team can see it.", "很好。我会把这个顺序写进任务单，让团队看到。"),
            turn("Leo", "Thanks. That gives everyone a clear handoff for tomorrow.", "谢谢。这样大家就有一份清楚的明天交接。"),
        ),
    ],
}


EXPECTED_EXPRESSIONS = {
    "morning-greetings-at-work": (
        ("good morning",),
        ("settle in",),
        ("catch up",),
        ("get started",),
        ("good morning", "settle in"),
        ("catch up", "get started"),
        ("good morning", "settle in", "catch up", "get started"),
    ),
    "asking-what-someone-is-working-on": (
        ("current task",),
        ("workstream",),
        ("sprint board",),
        ("task context",),
        ("current task", "workstream"),
        ("sprint board", "task context"),
        ("current task", "workstream", "sprint board", "task context"),
    ),
    "talking-about-todays-tasks": (
        ("to-do list",),
        ("planned work",),
        ("task ownership",),
        ("time block",),
        ("to-do list", "planned work"),
        ("task ownership", "time block"),
        ("to-do list", "planned work", "task ownership", "time block"),
    ),
    "talking-about-yesterdays-progress": (
        ("progress update",),
        ("completed task",),
        ("remaining work",),
        ("yesterday’s outcome",),
        ("progress update", "completed task"),
        ("remaining work", "yesterday’s outcome"),
        ("progress update", "completed task", "remaining work", "yesterday’s outcome"),
    ),
    "talking-about-blockers": (
        ("blocker",),
        ("technical dependency",),
        ("access issue",),
        ("waiting time",),
        ("blocker", "technical dependency"),
        ("access issue", "waiting time"),
        ("blocker", "technical dependency", "access issue", "waiting time"),
    ),
    "asking-for-a-quick-chat": (
        ("quick chat",),
        ("calendar slot",),
        ("context switch",),
        ("team huddle",),
        ("quick chat", "calendar slot"),
        ("context switch", "team huddle"),
        ("quick chat", "calendar slot", "context switch", "team huddle"),
    ),
    "checking-someones-availability": (
        ("availability",),
        ("focus time",),
        ("meeting window",),
        ("response time",),
        ("availability", "focus time"),
        ("meeting window", "response time"),
        ("availability", "focus time", "meeting window", "response time"),
    ),
    "prioritising-tasks": (
        ("priority",),
        ("urgent request",),
        ("business impact",),
        ("trade-off",),
        ("priority", "urgent request"),
        ("business impact", "trade-off"),
        ("priority", "urgent request", "business impact", "trade-off"),
    ),
    "giving-a-quick-status-update": (
        ("status update",),
        ("work in progress",),
        ("next step",),
        ("delivery risk",),
        ("status update", "work in progress"),
        ("next step", "delivery risk"),
        ("status update", "work in progress", "next step", "delivery risk"),
    ),
    "wrapping-up-the-day": (
        ("end-of-day update",),
        ("handover note",),
        ("carry-over task",),
        ("tomorrow’s plan",),
        ("end-of-day update", "handover note"),
        ("carry-over task", "tomorrow’s plan"),
        ("end-of-day update", "handover note", "carry-over task", "tomorrow’s plan"),
    ),
}


DISCONNECTED_FILLERS = (
    "that is useful context. what do you need from me?",
    "that makes sense. let’s make the next step explicit.",
    "thanks for raising it early. we can avoid rework now.",
    "good point. i’ll add that to the task and keep an eye on it.",
    "i’ll take that forward and let the team know what changes.",
    "i’ll follow up with the right person after this chat.",
)


def validate_dialogues() -> list[str]:
    """Return content-integrity errors so imports cannot reintroduce filler scenes."""
    errors: list[str] = []
    if set(LESSON_DIALOGUES) != set(EXPECTED_EXPRESSIONS):
        return ["Dialogue and expression lesson sets differ."]

    for lesson_code, expected_groups in EXPECTED_EXPRESSIONS.items():
        dialogues = LESSON_DIALOGUES[lesson_code]
        if len(dialogues) != len(expected_groups):
            errors.append(f"{lesson_code}: expected {len(expected_groups)} dialogues, got {len(dialogues)}.")
            continue
        for index, (scene, expected_terms) in enumerate(zip(dialogues, expected_groups), start=1):
            turns = scene.get("turns")
            if not scene.get("title") or not scene.get("scenario"):
                errors.append(f"{lesson_code} dialogue {index}: missing title or scenario.")
            if not isinstance(turns, list) or len(turns) < 3:
                errors.append(f"{lesson_code} dialogue {index}: needs at least three turns.")
                continue
            speakers = [line.get("speaker", "") for line in turns]
            if len(set(speakers)) < 2:
                errors.append(f"{lesson_code} dialogue {index}: needs two speakers.")
            if any(speakers[pos] == speakers[pos - 1] for pos in range(1, len(speakers))):
                errors.append(f"{lesson_code} dialogue {index}: speakers must alternate.")
            text = " ".join(str(line.get("english", "")) for line in turns).casefold()
            for line in turns:
                if not line.get("english") or not line.get("chinese"):
                    errors.append(f"{lesson_code} dialogue {index}: every turn needs English and Chinese.")
            for term in expected_terms:
                if term.casefold() not in text:
                    errors.append(f"{lesson_code} dialogue {index}: missing expression '{term}'.")
            for filler in DISCONNECTED_FILLERS:
                if filler in text:
                    errors.append(f"{lesson_code} dialogue {index}: contains disconnected filler.")
    return errors
